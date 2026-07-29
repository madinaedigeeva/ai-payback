"""Total cost of ownership and payback.

The design rule for this module: never invent a number the user did not
supply. A category the user left unpriced is reported as unpriced. A preset,
if enabled, produces an explicitly labelled illustrative range and never
replaces the user's own figures.
"""

from __future__ import annotations

from .models import Assessment, CostLine, CostResult, PaybackResult
from .spec import Spec, load_spec

PRESET_NONE = "none"


class CostError(ValueError):
    """The cost inputs cannot be used as supplied."""


def _omitted_categories(spec: Spec) -> list[dict]:
    return list(spec.cost_model.get("omitted_cost_categories", []))


def _direct_items(spec: Spec) -> list[dict]:
    return list(spec.cost_model.get("direct_cost_items", []))


def available_presets(spec: Spec | None = None) -> dict[str, dict]:
    spec = spec or load_spec()
    return dict(spec.cost_model.get("presets", {}))


def total_cost_of_ownership(
    assessment: Assessment,
    spec: Spec | None = None,
    *,
    preset: str = PRESET_NONE,
) -> CostResult:
    """Compute total cost of ownership under a named preset.

    With the default preset the total is the sum of what the user supplied and
    nothing else, and the unpriced categories are named in the result. That
    total is a floor, not an estimate, and the report says so.
    """
    spec = spec or load_spec()

    presets = spec.cost_model.get("presets", {})
    if preset not in presets:
        raise CostError(
            f"unknown preset {preset!r}; available: {sorted(presets)}"
        )

    problems = [
        f"{key}: cost must not be negative"
        for key, value in {**assessment.direct_costs, **assessment.omitted_costs}.items()
        if value < 0
    ]
    known_direct = {item["id"] for item in _direct_items(spec)}
    known_omitted = {cat["id"] for cat in _omitted_categories(spec)}
    problems += [
        f"unknown direct cost item: {k}"
        for k in assessment.direct_costs
        if k not in known_direct
    ]
    problems += [
        f"unknown omitted cost category: {k}"
        for k in assessment.omitted_costs
        if k not in known_omitted
    ]
    if problems:
        raise CostError("cost inputs are not usable:\n  - " + "\n  - ".join(problems))

    lines: list[CostLine] = []
    direct_total = 0.0

    for item in _direct_items(spec):
        item_id = str(item["id"])
        amount = assessment.direct_costs.get(item_id)
        if amount is not None:
            direct_total += float(amount)
        lines.append(
            CostLine(
                id=item_id,
                name=str(item["name"]),
                amount=float(amount) if amount is not None else None,
                priced=amount is not None,
                category="direct",
                source="user",
            )
        )

    use_preset_ranges = preset != PRESET_NONE
    unpriced: list[str] = []
    extra_low = 0.0
    extra_high = 0.0

    for category in _omitted_categories(spec):
        cat_id = str(category["id"])
        amount = assessment.omitted_costs.get(cat_id)

        if amount is not None:
            lines.append(
                CostLine(
                    id=cat_id,
                    name=str(category["name"]),
                    amount=float(amount),
                    priced=True,
                    category="omitted",
                    source="user",
                )
            )
            continue

        unpriced.append(cat_id)
        share_range = category.get("preset_share_range")

        if use_preset_ranges and share_range:
            low = direct_total * float(share_range[0])
            high = direct_total * float(share_range[1])
            extra_low += low
            extra_high += high
            lines.append(
                CostLine(
                    id=cat_id,
                    name=str(category["name"]),
                    amount=None,
                    priced=False,
                    category="omitted",
                    source=preset,
                    low=low,
                    high=high,
                )
            )
        else:
            lines.append(
                CostLine(
                    id=cat_id,
                    name=str(category["name"]),
                    amount=None,
                    priced=False,
                    category="omitted",
                    source="user",
                )
            )

    user_omitted_total = sum(
        float(v) for k, v in assessment.omitted_costs.items() if k in known_omitted
    )
    base = direct_total + user_omitted_total

    return CostResult(
        currency=assessment.currency,
        direct_total=direct_total,
        lines=tuple(lines),
        preset=preset,
        total_low=base + extra_low,
        total_high=base + extra_high,
        unpriced_category_ids=tuple(unpriced),
    )


def payback(
    assessment: Assessment,
    cost: CostResult,
    spec: Spec | None = None,
) -> PaybackResult:
    """Compute payback in months, or refuse and say why.

    A refusal is a result. The library will not substitute a benchmark benefit
    for one the user did not supply, because that would mean inventing the
    answer to the question being asked.
    """
    spec = spec or load_spec()
    benefit = assessment.net_monthly_benefit

    if benefit is None:
        return PaybackResult(
            computed=False,
            refusal_reason=(
                "No net monthly benefit was supplied. Payback cannot be computed "
                "from the cost side alone, and substituting a benchmark benefit "
                "would mean inventing the answer."
            ),
            elapsed_months=assessment.elapsed_months,
        )

    if benefit <= 0:
        return PaybackResult(
            computed=False,
            refusal_reason=(
                "Net monthly benefit is zero or negative, so the programme does "
                "not pay back under the supplied figures."
            ),
            elapsed_months=assessment.elapsed_months,
        )

    caveat = None
    horizon = spec.j_curve_horizon_months
    if assessment.elapsed_months is not None and assessment.elapsed_months < horizon:
        caveat = (
            f"This programme is {assessment.elapsed_months} months old, below the "
            f"{horizon}-month horizon in the framework. {spec.j_curve_statement}"
        )

    return PaybackResult(
        computed=True,
        months_low=cost.total_low / benefit,
        months_high=cost.total_high / benefit,
        refusal_reason=None,
        j_curve_caveat=caveat,
        elapsed_months=assessment.elapsed_months,
        caveats=_payback_caveats(assessment),
    )


def _payback_caveats(assessment: Assessment) -> tuple[str, ...]:
    """Conditions under which a computed payback figure is unsafe to rely on.

    Currently one, and it is the most common way an AI business case turns out
    to be wrong: a benefit that nobody converts into a decision never reaches
    the accounts. This is barrier PP-14, and it is a caveat rather than a
    refusal because the user may hold a conversion plan the assessment does not
    record.
    """
    if assessment.has_conversion_path:
        return ()
    return (
        "No conversion path was recorded for this benefit. A time or cost saving "
        "reaches the accounts only when someone ends a contract, declines to "
        "backfill a role, reduces overtime, absorbs additional volume without "
        "hiring, or moves a price or conversion rate. Nationally, 95.7% of "
        "AI-using firms report no AI-driven employment change at all over six "
        "months (U.S. Census Bureau, CES-WP-26-25, April 2026, Table 4) - which "
        "is what an unconverted saving looks like in aggregate. Until the "
        "conversion is named, owned and dated, treat this figure as a "
        "theoretical maximum rather than a forecast. See barrier PP-14.",
    )
