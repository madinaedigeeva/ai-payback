# Changelog

All notable changes to this project are recorded here. Because the substance of
this project is a *specification* rather than an API, changes to the framework,
the taxonomy and the source registry are recorded with the same weight as
changes to code — and a result produced under one framework version is never
silently comparable with one produced under another.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-07-30

Driven by an evidence review against primary sources and two independent
adversarial reviews of the v0.1.0 taxonomy. The review is published in full at
`docs/EVIDENCE-REVIEW.md`.

### Added

- **Six barriers**, taking the taxonomy from 20 to 26 and the instrument from 60
  to 78 questions:
  - `PP-13` No pre-deployment baseline — improvement cannot be demonstrated
    because nothing was measured before.
  - `PP-14` **No conversion path for the saving** — the most consequential
    addition; see below.
  - `PP-15` Verification tax — review cost exceeding the work saved.
  - `PP-16` Shadow AI and tool sprawl — uncoordinated purchasing, invisible spend.
  - `PP-17` Simpler alternative never tested — rules or RPA would have done it
    more cheaply and more predictably.
  - `TD-06` Vendor incentive misalignment — metered pricing rewards
    consumption, not results.
- **Conversion-path caveat in the payback calculation.** `Assessment` gains
  `benefit_conversion`. When a benefit is supplied without one, `payback()`
  returns the figure *with* an explicit caveat citing its source, rendered above
  the fold in Markdown and present in the JSON. This is a caveat and not a
  refusal: the user may hold a conversion plan the assessment file does not
  record, and suppressing the number would be as dishonest as hiding the caveat.
- **Two primary sources**, both verified against the document on 2026-07-30:
  - `CENSUS-BTOS-2026` — U.S. Census Bureau CES Working Paper 26-25, *The
    Microstructure of AI Diffusion*, April 2026. Nationally representative.
    Now the strongest evidence base in the specification.
  - `BLR-QJE-2025` — Brynjolfsson, Li & Raymond, "Generative AI at Work",
    *Quarterly Journal of Economics* 140(2), 2025. Carries a `scope_note`
    recording that the measured effect is throughput, **not** customer
    retention — a distinction routinely got wrong.
- `CHANGELOG.md`, this file.
- Eleven tests covering the new behaviour (60 total, from 49).

### Changed

- **`MIT-NANDA-2025` downgraded from `primary` to `published`.** The quotations
  were read and confirmed against the primary PDF on 2026-07-29. On 2026-07-30
  the document was no longer retrievable — `nanda.media.mit.edu` returns HTML
  rather than a PDF, the mirror returns a one-page stub, and the Wayback Machine
  returns HTML. An independent reviewer attempted retrieval separately and
  reported the same. The quotations are retained with their original
  verification date, because a 403 or a redirect is not proof a document does
  not exist — but nothing load-bearing may now rest on them.
- Taxonomy version 0.1.0 → 0.2.0; framework version 0.1.0 → 0.2.0.
- Barriers with no NIST AI RMF mapping: 7 → 8. The new one is `PP-14`, which is
  worth stating plainly — the single most consequential economic barrier in the
  taxonomy has no counterpart in the leading AI risk framework. That is not a
  criticism of the AI RMF, which manages risk rather than return. It is the gap.

### Notes on what was considered and rejected

- A per-function *attribution difficulty weighting* was designed and then
  **dropped**. The hypothesis behind it — that revenue-side functions are
  structurally harder to attribute than cost-side ones — did not survive review:
  marketing is among the most instrumented functions in business, and
  back-office savings do not reach the P&L either. Shipping a weighting with no
  empirical basis would have put an invented number into a tool whose entire
  claim is that it does not invent numbers. The reasoning is preserved in
  `docs/EVIDENCE-REVIEW.md` §4 so that the rejection is auditable.

## [0.1.0] — 2026-07-29

Initial release. 20 barriers, 60 questions, three layers weighted 10/20/70,
total-cost-of-ownership model with six routinely-omitted cost categories, simple
payback with explicit refusal, Markdown and JSON reporting, five sources with
provenance tiers and a published pool of excluded claims.
