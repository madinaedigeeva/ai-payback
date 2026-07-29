"""Cost, payback and report behaviour.

The properties under test here are the honesty guarantees: unpriced is not
zero, illustrative is labelled, and a payback figure is refused rather than
fabricated when the benefit is unknown.
"""

from __future__ import annotations

import json

import pytest

from ai_payback import (
    Assessment,
    CostError,
    load_spec,
    payback,
    score,
    to_json,
    to_markdown,
    total_cost_of_ownership,
)
from ai_payback.spec import Spec

PRESET = "yedigeyeva_2026_illustrative"


@pytest.fixture(scope="module")
def spec() -> Spec:
    return load_spec()


@pytest.fixture
def priced(spec: Spec) -> Assessment:
    return Assessment(
        organisation="Example Ltd",
        responses={q.id: 2 for q in spec.questions},
        direct_costs={"licences": 100_000, "inference": 50_000, "internal_labour": 150_000},
        currency="USD",
        net_monthly_benefit=25_000,
        elapsed_months=24,
    )


# ------------------------------------------------------------------- cost

def test_default_preset_makes_no_estimates(spec: Spec, priced: Assessment) -> None:
    cost = total_cost_of_ownership(priced, spec)
    assert cost.preset == "none"
    assert cost.is_floor_only
    assert cost.total_low == cost.total_high == pytest.approx(300_000)
    assert not cost.has_illustrative_lines
    assert cost.unpriced_category_ids  # named, not silently dropped


def test_unpriced_is_distinguishable_from_zero(spec: Spec, priced: Assessment) -> None:
    cost = total_cost_of_ownership(priced, spec)
    unpriced = [line for line in cost.lines if not line.priced]
    assert unpriced
    for line in unpriced:
        assert line.amount is None  # not 0.0


def test_a_user_zero_is_priced_not_unpriced(spec: Spec, priced: Assessment) -> None:
    """Costing a category at zero is a decision and must be recorded as one."""
    priced.omitted_costs["compliance_security_legal"] = 0.0
    cost = total_cost_of_ownership(priced, spec)
    line = next(line for line in cost.lines if line.id == "compliance_security_legal")
    assert line.priced
    assert line.amount == 0.0
    assert "compliance_security_legal" not in cost.unpriced_category_ids


def test_illustrative_preset_widens_the_range_and_labels_it(
    spec: Spec, priced: Assessment
) -> None:
    cost = total_cost_of_ownership(priced, spec, preset=PRESET)
    assert cost.total_high > cost.total_low > 300_000
    assert cost.has_illustrative_lines
    for line in cost.lines:
        if line.low is not None:
            assert line.is_illustrative
            assert line.source == PRESET


def test_preset_never_overrides_a_user_figure(spec: Spec, priced: Assessment) -> None:
    priced.omitted_costs["data_preparation"] = 12_345
    cost = total_cost_of_ownership(priced, spec, preset=PRESET)
    line = next(line for line in cost.lines if line.id == "data_preparation")
    assert line.amount == 12_345
    assert line.source == "user"
    assert not line.is_illustrative


def test_category_with_no_reported_share_is_never_estimated(
    spec: Spec, priced: Assessment
) -> None:
    """Yedigeyeva names ongoing maintenance but gives no share. None is invented."""
    cost = total_cost_of_ownership(priced, spec, preset=PRESET)
    line = next(line for line in cost.lines if line.id == "ongoing_maintenance")
    assert line.low is None
    assert not line.priced


def test_unknown_preset_is_rejected(spec: Spec, priced: Assessment) -> None:
    with pytest.raises(CostError):
        total_cost_of_ownership(priced, spec, preset="wishful_thinking")


def test_negative_and_unknown_costs_are_rejected(spec: Spec, priced: Assessment) -> None:
    with pytest.raises(CostError):
        total_cost_of_ownership(
            Assessment("A", direct_costs={"licences": -1}), spec
        )
    with pytest.raises(CostError):
        total_cost_of_ownership(
            Assessment("A", direct_costs={"unicorns": 10}), spec
        )


# ---------------------------------------------------------------- payback

def test_payback_is_refused_without_a_benefit(spec: Spec, priced: Assessment) -> None:
    priced.net_monthly_benefit = None
    cost = total_cost_of_ownership(priced, spec)
    result = payback(priced, cost, spec)
    assert not result.computed
    assert result.months_low is None
    assert "inventing the answer" in result.refusal_reason


def test_payback_is_refused_on_non_positive_benefit(spec: Spec, priced: Assessment) -> None:
    priced.net_monthly_benefit = 0
    cost = total_cost_of_ownership(priced, spec)
    assert not payback(priced, cost, spec).computed


def test_payback_arithmetic(spec: Spec, priced: Assessment) -> None:
    cost = total_cost_of_ownership(priced, spec)
    result = payback(priced, cost, spec)
    assert result.computed
    assert result.months_low == pytest.approx(300_000 / 25_000)


def test_j_curve_caveat_attaches_to_young_programmes(spec: Spec, priced: Assessment) -> None:
    priced.elapsed_months = 4
    cost = total_cost_of_ownership(priced, spec)
    result = payback(priced, cost, spec)
    assert result.computed
    assert result.j_curve_caveat and "4 months old" in result.j_curve_caveat


def test_no_j_curve_caveat_for_mature_programmes(spec: Spec, priced: Assessment) -> None:
    assert payback(
        priced, total_cost_of_ownership(priced, spec), spec
    ).j_curve_caveat is None


# ----------------------------------------------------------------- report

def test_markdown_report_states_the_floor_and_the_derivation(
    spec: Spec, priced: Assessment
) -> None:
    cost = total_cost_of_ownership(priced, spec)
    md = to_markdown(priced, score(priced, spec), cost, payback(priced, cost, spec), spec)
    assert "# AI adoption payback analysis — Example Ltd" in md
    assert "floor" in md
    assert "10-20-70" in md
    assert "not a finding of BCG" in md
    assert "not predict return on investment" in md


def test_markdown_labels_illustrative_lines_inline(spec: Spec, priced: Assessment) -> None:
    cost = total_cost_of_ownership(priced, spec, preset=PRESET)
    md = to_markdown(priced, score(priced, spec), cost, payback(priced, cost, spec), spec)
    assert "*illustrative" in md
    assert "must be replaced with its own figures" in md


def test_markdown_reports_a_refusal_rather_than_omitting_payback(
    spec: Spec, priced: Assessment
) -> None:
    priced.net_monthly_benefit = None
    cost = total_cost_of_ownership(priced, spec)
    md = to_markdown(priced, score(priced, spec), cost, payback(priced, cost, spec), spec)
    assert "**Not computed.**" in md


def test_json_report_is_valid_and_carries_provenance(spec: Spec, priced: Assessment) -> None:
    cost = total_cost_of_ownership(priced, spec)
    payload = json.loads(
        to_json(priced, score(priced, spec), cost, payback(priced, cost, spec), spec)
    )
    assert payload["framework"]["version"] == spec.version
    assert payload["readiness"]["weights"]["PEOPLE_PROCESS"] == 0.70
    assert payload["cost"]["floor_only"] is True
    assert payload["disclaimers"]["not_predictive"]
