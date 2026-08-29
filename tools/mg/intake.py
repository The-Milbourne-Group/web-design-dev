"""Lead intake. One entry point for every channel that actually exists.

A lead arrives as text — a web form POST written to a file, a forwarded
enquiry email, a note typed after a phone call. This parses whatever structure
is present, records the rest verbatim, and never guesses a value it cannot see.
An unparsed field becomes missing information, not an invention.
"""
from __future__ import annotations

import json
import re

from . import model as m

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?:(?:\+\d{1,3}[\s-]?)?(?:\(?\d{2,5}\)?[\s.-]?){2,4}\d{2,5})")
URL = re.compile(r"(?:https?://)?(?:www\.)?([a-z0-9-]+(?:\.[a-z]{2,}){1,2})(?:/\S*)?", re.I)

# "Label: value" pairs, as a web form or a structured enquiry produces.
FIELD = re.compile(r"^\s*([A-Za-z][A-Za-z /_-]{1,30}?)\s*[:=]\s*(.+?)\s*$", re.M)

# Which record field each incoming label maps to. Anything unrecognised is kept
# in the raw enquiry rather than dropped.
ALIASES = {
    "company": "company", "organisation": "company", "organization": "company",
    "business": "company", "company name": "company",
    "name": "contact", "contact": "contact", "full name": "contact",
    "your name": "contact", "from": "contact",
    "email": "email", "e-mail": "email", "email address": "email",
    "phone": "phone", "telephone": "phone", "mobile": "phone", "tel": "phone",
    "role": "role", "title": "role", "job title": "role", "position": "role",
    "website": "website", "site": "website", "url": "website", "web": "website",
    "industry": "industry", "sector": "industry",
    "size": "size", "employees": "size", "headcount": "size", "staff": "size",
    "source": "source", "referrer": "source", "how did you hear": "source",
    "how did you hear about us": "source", "referred by": "source",
    "message": "problem", "enquiry": "problem", "inquiry": "problem",
    "problem": "problem", "details": "problem", "comments": "problem",
    "subject": "subject",
    "outcome": "outcome_wanted", "goal": "outcome_wanted",
    "desired outcome": "outcome_wanted", "objective": "outcome_wanted",
}

NOISE = {"re", "fwd", "sent", "to", "cc", "bcc", "date", "reply-to"}


def parse(text: str) -> dict:
    """Extract what is actually present. Returns {fields, raw, missing}."""
    text = text.strip()
    out: dict[str, str] = {}

    # A form or API may hand us JSON directly.
    if text.startswith("{"):
        try:
            data = json.loads(text)
            for k, v in data.items():
                key = ALIASES.get(str(k).strip().lower())
                if key and v:
                    out.setdefault(key, str(v).strip())
            out["_raw"] = text
            return _finish(out, text)
        except json.JSONDecodeError:
            pass

    for label, value in FIELD.findall(text):
        lab = label.strip().lower()
        if lab in NOISE:
            continue
        key = ALIASES.get(lab)
        if key and value and not value.startswith("<"):
            out.setdefault(key, value.strip())

    # Free-text fallbacks for the three things almost every enquiry carries.
    if "email" not in out:
        found = EMAIL.search(text)
        if found:
            out["email"] = found.group(0)
    if "website" not in out:
        for cand in URL.findall(text):
            if "@" in cand or cand.lower().endswith((".png", ".jpg")):
                continue
            if "email" in out and cand.split(".")[0] in out["email"]:
                out["website"] = cand
                break
    if "phone" not in out:
        found = PHONE.search(re.sub(r"\d{4}-\d{2}-\d{2}", "", text))
        if found and len(re.sub(r"\D", "", found.group(0))) >= 9:
            out["phone"] = found.group(0).strip()

    # The body of a plain email is the enquiry, when no field labelled it.
    if "problem" not in out:
        body = _body(text)
        if body:
            out["problem"] = body
    return _finish(out, text)


def _body(text: str) -> str:
    """Everything after the header block of a forwarded email."""
    lines = text.splitlines()
    start = 0
    for i, ln in enumerate(lines):
        if FIELD.match(ln):
            start = i + 1
        elif ln.strip() == "" and start:
            start = i + 1
            break
    body = "\n".join(lines[start:]).strip()
    body = re.split(r"\n\s*(?:--|Sent from|Kind regards|Best regards|Regards|Thanks)\b",
                    body, maxsplit=1)[0].strip()
    return " ".join(body.split())[:1200]


def _clean_name(value: str) -> str:
    """`Dan Whitfield <dan@example.com>` -> `Dan Whitfield`."""
    value = re.sub(r"<[^>]*>", "", value).strip().strip('"').strip()
    return value.rstrip(",;").strip()


def _finish(out: dict, raw: str) -> dict:
    if out.get("contact"):
        cleaned = _clean_name(out["contact"])
        # A bare address in the From: line is the email, not a name.
        if cleaned and not EMAIL.fullmatch(cleaned):
            out["contact"] = cleaned
        else:
            out.setdefault("email", out["contact"].strip("<> "))
            out["contact"] = ""
    fields = {k: v for k, v in out.items() if not k.startswith("_") and v}
    missing = [k for k in ("company", "contact", "source", "problem", "outcome_wanted")
               if not fields.get(k)]
    return {"fields": fields, "raw": raw.strip(), "missing": missing}


def to_opportunity(parsed: dict, slug: str | None = None) -> m.Opportunity:
    f = parsed["fields"]
    company = f.get("company") or f.get("contact") or "unnamed-enquiry"
    opp = m.Opportunity(slug=slug or m.slugify(company), created_on=m.today())
    opp.company.name = f.get("company", "")
    opp.company.website = f.get("website", "")
    opp.company.industry = f.get("industry", "")
    opp.company.approximate_size = f.get("size", "")
    opp.qualification.source = f.get("source", "")
    opp.qualification.problem = f.get("problem", "")
    opp.qualification.desired_outcome = f.get("outcome_wanted", "")
    if f.get("contact") or f.get("email"):
        opp.contacts.append(m.Contact(
            name=f.get("contact", ""), role=f.get("role", ""),
            email=f.get("email", ""), phone=f.get("phone", "")))
    return opp
