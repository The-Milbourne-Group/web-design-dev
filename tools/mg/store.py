"""Persistence. The repository is the system of record.

`clients/<slug>/opportunity.json` holds the structured record; every markdown
artifact beside it is rendered from that record. Adding a database or an
external CRM would create a second source of truth for client knowledge, which
`MASTER.md` §5.3 forbids and `clients/README.md` already assigns to this
directory (Tier 7).
"""
from __future__ import annotations

import json
from pathlib import Path

from . import model as m
from .governance import repo_root

RECORD = "opportunity.json"


def clients_dir(root: Path) -> Path:
    return root / "clients"


def opp_dir(root: Path, slug: str) -> Path:
    return clients_dir(root) / slug


def exists(root: Path, slug: str) -> bool:
    return (opp_dir(root, slug) / RECORD).exists()


def load(root: Path, slug: str) -> m.Opportunity:
    path = opp_dir(root, slug) / RECORD
    if not path.exists():
        raise FileNotFoundError(
            f"No opportunity {slug!r}. `mg list` shows what exists."
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    opp = m.from_dict(m.Opportunity, data)
    opp.slug = slug
    return opp


def save(root: Path, opp: m.Opportunity) -> Path:
    d = opp_dir(root, opp.slug)
    d.mkdir(parents=True, exist_ok=True)
    (d / "QA").mkdir(exist_ok=True)
    path = d / RECORD
    path.write_text(
        json.dumps(m.to_dict(opp), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def all_slugs(root: Path) -> list[str]:
    cd = clients_dir(root)
    if not cd.is_dir():
        return []
    return sorted(
        p.name for p in cd.iterdir()
        if p.is_dir() and not p.name.startswith("_") and (p / RECORD).exists()
    )


def load_all(root: Path) -> list[m.Opportunity]:
    return [load(root, s) for s in all_slugs(root)]


def write_artifact(root: Path, slug: str, filename: str, content: str) -> Path:
    d = opp_dir(root, slug)
    d.mkdir(parents=True, exist_ok=True)
    p = d / filename
    p.write_text(content, encoding="utf-8")
    return p
