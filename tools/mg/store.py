"""Persistence. The repository is the system of record.

`clients/<slug>/opportunity.json` holds the structured record; every markdown
artifact beside it is rendered from that record. Adding a database or an
external CRM would create a second source of truth for client knowledge, which
`MASTER.md` §5.3 forbids and `clients/README.md` already assigns to this
directory (Tier 7).

Writes are atomic and every save keeps the previous version. A half-written
record and an overwritten record are the two ways this system could lose a
client's discovery, so neither is left to chance.
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path

from . import model as m
from . import growth as gr
from .governance import repo_root

RECORD = "opportunity.json"
BACKUP_DIR = ".history"
KEEP_VERSIONS = 20


class RecordError(Exception):
    """A record exists but cannot be read as one."""


def clients_dir(root: Path) -> Path:
    return root / "clients"


def opp_dir(root: Path, slug: str) -> Path:
    return clients_dir(root) / slug


def record_path(root: Path, slug: str) -> Path:
    return opp_dir(root, slug) / RECORD


def exists(root: Path, slug: str) -> bool:
    return record_path(root, slug).exists()


# --------------------------------------------------------------------------
# Load
# --------------------------------------------------------------------------

def load(root: Path, slug: str) -> m.Opportunity:
    path = record_path(root, slug)
    if not path.exists():
        raise FileNotFoundError(
            f"No opportunity {slug!r}. `mg list` shows what exists."
        )
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        raise RecordError(f"Cannot read {path}: {e}") from e
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        backups = list_backups(root, slug)
        hint = (f"\n  {len(backups)} earlier version(s) are intact. "
                f"Recover with:  mg restore {slug}"
                if backups else
                "\n  No earlier version exists to restore from.")
        raise RecordError(
            f"{path} is not valid JSON (line {e.lineno}, column {e.colno}: {e.msg}).\n"
            f"  The file was not modified.{hint}"
        ) from e
    if not isinstance(data, dict):
        raise RecordError(f"{path} does not contain an opportunity record.")

    opp = m.from_dict(m.Opportunity, data)
    opp.slug = slug
    problems = m.validate(opp)
    if problems:
        raise RecordError(
            f"{path} is readable but not a valid opportunity:\n"
            + "\n".join(f"    - {p}" for p in problems)
            + f"\n  Fix the file, or recover the previous version:  mg restore {slug}"
        )
    return opp


def load_quietly(root: Path, slug: str) -> tuple[m.Opportunity | None, str]:
    """Load without raising — for commands that sweep every opportunity."""
    try:
        return load(root, slug), ""
    except (RecordError, FileNotFoundError) as e:
        return None, str(e).splitlines()[0]


# --------------------------------------------------------------------------
# Save — atomic, with history
# --------------------------------------------------------------------------

def save(root: Path, opp: m.Opportunity) -> Path:
    problems = m.validate(opp)
    if problems:
        raise RecordError(
            "Refusing to save an invalid record:\n"
            + "\n".join(f"    - {p}" for p in problems)
        )
    d = opp_dir(root, opp.slug)
    d.mkdir(parents=True, exist_ok=True)
    (d / "QA").mkdir(exist_ok=True)
    path = d / RECORD

    _sweep_temp(d)
    if path.exists():
        _archive(d, path)

    payload = json.dumps(m.to_dict(opp), indent=2, ensure_ascii=False) + "\n"
    _atomic_write(path, payload)
    return path


def _sweep_temp(d: Path, max_age_s: int = 300) -> None:
    """Remove abandoned temp files.

    A hard kill (SIGKILL, power loss) cannot run the cleanup handler, so a
    `.tmp-*` file survives. It is harmless — the rename never happened, so the
    record is intact — but it should not accumulate.
    """
    import time
    now = time.time()
    for tmp in d.glob(".tmp-*"):
        try:
            if now - tmp.stat().st_mtime > max_age_s:
                tmp.unlink(missing_ok=True)
        except OSError:
            pass


def _atomic_write(path: Path, text: str) -> None:
    """Write via a temp file in the same directory, then rename.

    A rename within one filesystem is atomic, so an interrupted save leaves the
    previous record whole rather than a truncated file.
    """
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _archive(d: Path, path: Path) -> None:
    hist = d / BACKUP_DIR
    hist.mkdir(exist_ok=True)
    stamp = m.now().replace(":", "").replace("-", "")
    dest = hist / f"{stamp}.json"
    n = 1
    while dest.exists():
        dest = hist / f"{stamp}-{n}.json"
        n += 1
    try:
        shutil.copy2(path, dest)
    except OSError:
        return
    versions = sorted(hist.glob("*.json"))
    for old in versions[:-KEEP_VERSIONS]:
        old.unlink(missing_ok=True)


def list_backups(root: Path, slug: str) -> list[Path]:
    hist = opp_dir(root, slug) / BACKUP_DIR
    return sorted(hist.glob("*.json"), reverse=True) if hist.is_dir() else []


def restore(root: Path, slug: str, index: int = 0) -> Path:
    """Restore the Nth most recent archived version (0 = latest)."""
    backups = list_backups(root, slug)
    if not backups:
        raise RecordError(f"No archived versions for {slug}.")
    if index >= len(backups):
        raise RecordError(f"Only {len(backups)} version(s) archived for {slug}.")
    src = backups[index]
    json.loads(src.read_text(encoding="utf-8"))   # refuse to restore a corrupt one
    path = record_path(root, slug)
    if path.exists():
        _archive(opp_dir(root, slug), path)
    _atomic_write(path, src.read_text(encoding="utf-8"))
    return src


# --------------------------------------------------------------------------
# Listing
# --------------------------------------------------------------------------

def all_slugs(root: Path) -> list[str]:
    cd = clients_dir(root)
    if not cd.is_dir():
        return []
    return sorted(
        p.name for p in cd.iterdir()
        if p.is_dir() and not p.name.startswith("_") and (p / RECORD).exists()
    )


def load_all(root: Path) -> list[m.Opportunity]:
    """Every readable record. Unreadable ones are reported by `mg check`."""
    out = []
    for s in all_slugs(root):
        opp, _ = load_quietly(root, s)
        if opp is not None:
            out.append(opp)
    return out


def load_all_with_errors(root: Path) -> tuple[list[m.Opportunity], list[tuple[str, str]]]:
    good, bad = [], []
    for s in all_slugs(root):
        opp, errmsg = load_quietly(root, s)
        (good.append(opp) if opp is not None else bad.append((s, errmsg)))
    return good, bad


def find_duplicates(root: Path, company: str, email: str = "",
                    exclude: str = "") -> list[tuple[str, str]]:
    """Existing opportunities that look like the same organisation."""
    key = _norm(company)
    hits: list[tuple[str, str]] = []
    if not key and not email:
        return hits
    for opp in load_all(root):
        if opp.slug == exclude:
            continue
        if key and _norm(opp.company.name) == key:
            hits.append((opp.slug, f"same company name ({opp.company.name})"))
            continue
        if email:
            for cont in opp.contacts:
                if cont.email and cont.email.lower() == email.lower():
                    hits.append((opp.slug, f"same contact email ({cont.email})"))
                    break
    return hits


def _norm(name: str) -> str:
    import re
    n = re.sub(r"[^a-z0-9 ]", " ", (name or "").lower())
    drop = {"ltd", "limited", "llc", "inc", "plc", "the", "group", "co", "company"}
    return " ".join(w for w in n.split() if w not in drop)


def write_artifact(root: Path, slug: str, filename: str, content: str) -> Path:
    d = opp_dir(root, slug)
    d.mkdir(parents=True, exist_ok=True)
    _atomic_write(d / filename, content)
    return d / filename


# --------------------------------------------------------------------------
# Targets — pre-contact prospects, upstream of the client pipeline
# --------------------------------------------------------------------------
#
# A target lives in `growth/`, not `clients/`. `clients/README.md` creates a
# directory at qualification, when a lead already exists; a target has not been
# contacted and may never become one. Filing every researched company under
# `clients/` would flood the pipeline and corrupt the buyer-evidence base that
# D-021 is tested against.

TARGET_RECORD = "target.json"


def growth_dir(root: Path) -> Path:
    return root / "growth"


def target_dir(root: Path, slug: str) -> Path:
    return growth_dir(root) / slug


def target_exists(root: Path, slug: str) -> bool:
    return (target_dir(root, slug) / TARGET_RECORD).exists()


def load_target(root: Path, slug: str) -> "gr.Target":
    path = target_dir(root, slug) / TARGET_RECORD
    if not path.exists():
        raise FileNotFoundError(
            f"No target {slug!r}. `mg target list` shows what exists."
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        backups = list_target_backups(root, slug)
        hint = (f"\n  {len(backups)} earlier version(s) intact — `mg target restore {slug}`"
                if backups else "")
        raise RecordError(
            f"{path} is not valid JSON (line {e.lineno}, column {e.colno}: {e.msg}).\n"
            f"  The file was not modified.{hint}"
        ) from e
    t = m.from_dict(gr.Target, data)
    t.slug = slug
    problems = gr.validate(t)
    if problems:
        raise RecordError(
            f"{path} is readable but not a valid target:\n"
            + "\n".join(f"    - {p}" for p in problems)
        )
    return t


def save_target(root: Path, t: "gr.Target") -> Path:
    problems = gr.validate(t)
    if problems:
        raise RecordError(
            "Refusing to save an invalid target:\n"
            + "\n".join(f"    - {p}" for p in problems)
        )
    d = target_dir(root, t.slug)
    d.mkdir(parents=True, exist_ok=True)
    path = d / TARGET_RECORD
    _sweep_temp(d)
    if path.exists():
        _archive(d, path)
    _atomic_write(path, json.dumps(m.to_dict(t), indent=2, ensure_ascii=False) + "\n")
    return path


def list_target_backups(root: Path, slug: str) -> list[Path]:
    hist = target_dir(root, slug) / BACKUP_DIR
    return sorted(hist.glob("*.json"), reverse=True) if hist.is_dir() else []


def all_target_slugs(root: Path) -> list[str]:
    gd = growth_dir(root)
    if not gd.is_dir():
        return []
    return sorted(
        p.name for p in gd.iterdir()
        if p.is_dir() and not p.name.startswith("_") and (p / TARGET_RECORD).exists()
    )


def load_all_targets(root: Path) -> tuple[list["gr.Target"], list[tuple[str, str]]]:
    good, bad = [], []
    for slug in all_target_slugs(root):
        try:
            good.append(load_target(root, slug))
        except (RecordError, FileNotFoundError) as e:
            bad.append((slug, str(e).splitlines()[0]))
    return good, bad


def find_target_duplicates(root: Path, company: str, email: str = "",
                           exclude: str = "") -> list[tuple[str, str]]:
    key = _norm(company)
    hits: list[tuple[str, str]] = []
    targets, _ = load_all_targets(root)
    for t in targets:
        if t.slug == exclude:
            continue
        if key and _norm(t.company.name) == key:
            hits.append((t.slug, f"same company ({t.company.name})"))
            continue
        if email:
            for cont in t.contacts:
                if cont.email and cont.email.lower() == email.lower():
                    hits.append((t.slug, f"same contact email ({cont.email})"))
                    break
    return hits


def write_target_artifact(root: Path, slug: str, filename: str, content: str) -> Path:
    d = target_dir(root, slug)
    d.mkdir(parents=True, exist_ok=True)
    _atomic_write(d / filename, content)
    return d / filename
