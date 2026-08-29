# WEB_STANDARDS.md
# THE MILBOURNE GROUP
## WEB PRODUCT CRAFT SOURCE OF TRUTH

**System:** Delivery / Product
**Purpose:** Define the quality standards for the websites and web applications the company builds for clients — strategy, design, and implementation craft.
**Authority:** Tier 3. Authoritative for web product craft standards.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Every client web deliverable and the company's own website.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Change to craft standards, accessibility target, or performance baseline.
**Related:** `DELIVERY.md` (lifecycle), `TECH_STACK.md` (technology selection), `BRAND.md` (company brand), `sops/delivery/QA.md`

---

## 1. Purpose

`DELIVERY.md` governs *when* work happens. `TECH_STACK.md` governs *what
technology* is chosen. This document governs *how good the product must be*.

It previously lived inside `MASTER.md` §11, where it duplicated
`TECH_STACK.md` §5 and violated the constitution's own rule against holding
domain content. Web craft standards now have one home.

---

## 2. Website Strategy

A website is a business system, not a visual deliverable.

Before significant implementation, establish:

- Business objective
- Target audience
- User intent
- Primary conversion
- Secondary conversions
- Competitive context
- Brand position
- Trust requirements
- Technical constraints

**Page standard.** Every significant page must answer:

1. Who is this for?
2. What problem exists?
3. What outcome is desired?
4. Why should the user trust this business?
5. What should happen next?

A page that cannot answer all five is not ready to build.

---

## 3. Design Standards

Design priority order — when these conflict, the higher item wins:

1. Information hierarchy
2. Clarity
3. Usability
4. Accessibility
5. Conversion
6. Brand differentiation
7. Visual polish

Aesthetics never outrank usability or client objectives.

Do not add visual complexity without purpose.

Maintain consistent systems for typography, spacing, components, interaction
states, and responsive behavior. Ad-hoc one-off styling is technical debt.

### 3.1 Accessibility Baseline

Target **WCAG 2.1 Level AA** unless a client requirement sets a higher bar.
Where a project cannot meet it, record the gap and the reason in the project
brief — do not silently ship below baseline.

Always verify: keyboard navigability, visible focus states, text alternatives,
colour contrast, form labelling, heading order, and motion/reduced-motion
handling.

### 3.2 Responsive Behavior

Verify layout, readability, and interaction at small, medium, and large
viewports. Responsive is a functional requirement, not a design preference.

---

## 4. Implementation Standards

Prefer:

- Clear architecture and maintainable code
- Reusable components
- Semantic HTML
- Accessible interfaces
- Responsive layouts
- Explicit error handling
- Secure defaults
- Performance-conscious implementation
- Minimal dependencies

Avoid:

- Dead code
- Duplicate logic
- Hidden assumptions
- Unnecessary dependencies
- Premature abstraction

Repository-specific implementation rules belong in that repository's
`CLAUDE.md`, which may add detail but may not lower these standards.

---

## 5. Performance

Performance is a conversion and credibility factor, not a nicety.

Verify before launch: page weight, image optimisation and correct formats,
render-blocking resources, font loading strategy, and behaviour on a
constrained connection.

A specific numeric performance budget depends on the approved stack
(`TECH_STACK.md` §3, D-039). Record measured baselines at launch so
regression is detectable.

---

## 6. Content and Trust

Client-facing copy follows the claims standard in `BRAND.md` §6 — for the
client's claims as well as the company's. Do not publish client claims that
are unverifiable on their face (unsupported statistics, unearned
certifications, invented testimonials). Raise them with the client instead.

---

## 7. Definition of Ready to Launch

A web product is launch-ready only when `sops/delivery/LAUNCH.md` has been
completed and its verification record shows what was checked and what was not.

Meeting this document's standards is necessary but not sufficient: the
delivery quality gates in `DELIVERY.md` §6 also apply.
