"""Rendering the assessment as a report.

The Markdown report is the deliverable: the ROI analysis document that AI
adoption maturity frameworks ask an organisation to hold but do not define how
to produce.

Every figure in it is traceable. Illustrative figures are labelled as such on
the line where they appear, not in a footnote, so that a reader skimming the
table cannot mistake a preset for a measurement.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date
from typing import Any

from .models import Assessment, CostResult, PaybackResult, ReadinessResult
from .spec import Spec, load_spec


def _fmt_money(value: float | None, currency: str) -> str:
    if value is None:
        return "—"
    return f"{value:,.0f} {currency}"


def _fmt_months(value: float | None) -> str:
    return "—" if value is None else f"{value:,.1f}"


def to_json(
    assessment: Assessment,
    readiness: ReadinessResult,
    cost: CostResult,
    payback_result: PaybackResult,
    spec: Spec | None = None,
) -> str:
    """Machine-readable result, for storing or diffing across runs."""
    spec = spec or load_spec()
    payload: dict[str, Any] = {
        "generated": date.today().isoformat(),
        "framework": {
            "name": spec.framework.get("identity", {}).get("name"),
            "version": spec.version,
            "implements": spec.framework.get("identity", {}).get("implements"),
        },
        "assessment": assessment.to_dict(),
        "readiness": {
            "score": round(readiness.score, 4),
            "band": readiness.band_id,
            "band_label": readiness.band_label,
            "coverage": round(readiness.coverage, 4),
            "weights": readiness.weights,
            "complete": readiness.is_complete,
            "unanswered": list(readiness.unanswered_question_ids),
            "layers": [
                {
                    "id": layer.layer_id,
                    "name": layer.name,
                    "score": round(layer.score, 4),
                    "weight": layer.weight,
                    "barriers": [asdict(bs) for bs in layer.barrier_scores],
                }
                for layer in readiness.layers
            ],
        },
        "cost": {
            "currency": cost.currency,
            "preset": cost.preset,
            "direct_total": cost.direct_total,
            "total_low": cost.total_low,
            "total_high": cost.total_high,
            "floor_only": cost.is_floor_only,
            "unpriced_categories": list(cost.unpriced_category_ids),
            "lines": [asdict(line) for line in cost.lines],
        },
        "payback": asdict(payback_result),
        "disclaimers": spec.framework.get("disclaimers", {}),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def to_markdown(
    assessment: Assessment,
    readiness: ReadinessResult,
    cost: CostResult,
    payback_result: PaybackResult,
    spec: Spec | None = None,
) -> str:
    """Render the ROI analysis document."""
    spec = spec or load_spec()
    identity = spec.framework.get("identity", {})
    out: list[str] = []
    w = out.append

    w(f"# AI adoption payback analysis — {assessment.organisation}")
    w("")
    w(
        f"Generated {date.today().isoformat()} with "
        f"{identity.get('name', 'AI Payback Assessment')} v{spec.version}."
    )
    w("")

    # ------------------------------------------------------------- readiness
    w("## 1. Readiness")
    w("")
    w(f"**{readiness.score:.2f} of 4.00 — {readiness.band_label}**")
    w("")
    w(readiness.band_meaning)
    w("")
    if not readiness.is_complete:
        w(
            f"> Coverage {readiness.coverage:.0%}. "
            f"{len(readiness.unanswered_question_ids)} of "
            f"{len(spec.question_ids)} questions were not answered. Unanswered "
            "questions are excluded from the mean, not scored as zero, so this "
            "figure describes only what was assessed."
        )
        w("")

    w("| Layer | Score | Weight | Contribution |")
    w("|---|---|---|---|")
    for layer in readiness.layers:
        w(
            f"| {layer.name} | {layer.score:.2f} | {layer.weight:.0%} "
            f"| {layer.weighted_contribution:.2f} |"
        )
    w("")
    w(
        "Weights follow BCG's 10-20-70 allocation. Using an allocation of effort "
        "as a set of scoring weights is this framework's own modelling step and "
        "is not a finding of BCG's — see `src/ai_payback/spec/framework.yaml`, "
        "`weights.derivation`."
    )
    w("")

    # ----------------------------------------------------------- weak points
    if readiness.weakest_barriers:
        w("## 2. Where the exposure is")
        w("")
        w("| Barrier | Layer | Score | Answered |")
        w("|---|---|---|---|")
        for bs in readiness.weakest_barriers:
            layer_name = spec.layer_names.get(bs.layer, bs.layer)
            w(
                f"| {bs.barrier_id} {bs.name} | {layer_name} | {bs.score:.2f} "
                f"| {bs.answered}/{bs.total_questions} |"
            )
        w("")
        for bs in readiness.weakest_barriers:
            barrier = spec.barrier(bs.barrier_id)
            w(f"**{barrier.id} — {barrier.name}.** {barrier.description}")
            if barrier.evidence_quote:
                w("")
                w(f"> {barrier.evidence_quote}")
            w("")
            if barrier.sei:
                w(f"- SEI capability areas: {', '.join(barrier.sei)}")
            if barrier.nist:
                w(f"- NIST AI RMF: {', '.join(barrier.nist)}")
            else:
                w(
                    "- NIST AI RMF: no corresponding subcategory. This barrier is "
                    "economic and organisational, and the AI RMF is a risk "
                    "framework."
                )
            w(f"- Evidence: {', '.join(barrier.evidence)}")
            w("")

    # ------------------------------------------------------------------ cost
    w("## 3. Cost of ownership")
    w("")
    if cost.is_floor_only:
        w(
            "**No estimates were applied.** Every figure below was supplied by "
            "the organisation. Categories left unpriced are shown as unpriced "
            "and are not guessed at, so the total is a **floor**, not an "
            "estimate — the real number is higher by whatever the unpriced "
            "categories cost."
        )
    else:
        w(
            f"**Preset `{cost.preset}` is active.** Lines marked *illustrative* "
            "were produced by applying published share ranges to the direct "
            "cost total. They are not measurements of this organisation and "
            "must be replaced with its own figures before the analysis is used "
            "in a business case."
        )
    w("")
    w("| Item | Amount | Basis |")
    w("|---|---|---|")
    for line in cost.lines:
        if line.priced:
            basis = "supplied"
            amount = _fmt_money(line.amount, cost.currency)
        elif line.low is not None:
            basis = f"*illustrative — preset `{line.source}`*"
            amount = (
                f"{_fmt_money(line.low, cost.currency)} – "
                f"{_fmt_money(line.high, cost.currency)}"
            )
        else:
            basis = "**unpriced**"
            amount = "—"
        w(f"| {line.name} | {amount} | {basis} |")
    w("")
    w(f"- Direct costs supplied: **{_fmt_money(cost.direct_total, cost.currency)}**")
    if cost.total_low == cost.total_high:
        w(f"- Total cost of ownership: **{_fmt_money(cost.total_low, cost.currency)}**")
    else:
        w(
            f"- Total cost of ownership: **{_fmt_money(cost.total_low, cost.currency)} – "
            f"{_fmt_money(cost.total_high, cost.currency)}**"
        )
    if cost.unpriced_category_ids:
        w(f"- Unpriced categories: {', '.join(cost.unpriced_category_ids)}")
    w("")

    # --------------------------------------------------------------- payback
    w("## 4. Payback")
    w("")
    if payback_result.computed:
        if payback_result.months_low == payback_result.months_high:
            w(f"**{_fmt_months(payback_result.months_low)} months.**")
        else:
            w(
                f"**{_fmt_months(payback_result.months_low)} – "
                f"{_fmt_months(payback_result.months_high)} months.**"
            )
        w("")
        w(
            "Simple payback: total cost of ownership divided by net monthly "
            "benefit. No discounting."
        )
        if payback_result.j_curve_caveat:
            w("")
            w(f"> **J-curve caveat.** {payback_result.j_curve_caveat}")
    else:
        w(f"**Not computed.** {payback_result.refusal_reason}")
    w("")

    # ----------------------------------------------------------- disclaimers
    w("## 5. Scope and limits")
    w("")
    disclaimers = spec.framework.get("disclaimers", {})
    for key in ("not_predictive", "not_advice", "not_affiliated"):
        text = disclaimers.get(key)
        if text:
            w(f"- {' '.join(str(text).split())}")
    w("")
    w(
        "Sources for every coefficient and mapping used above are recorded in "
        "`src/ai_payback/spec/sources.yaml`, with a provenance tier for each and an explicit "
        "list of claims that were found unverifiable and therefore excluded."
    )
    w("")
    return "\n".join(out)
