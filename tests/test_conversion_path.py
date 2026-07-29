"""The conversion-path caveat (barrier PP-14).

A time or cost saving reaches the accounts only when someone converts it into a
decision. The Census Bureau's 2026 AI supplement finds 95.7% of AI-using firms
record no AI-driven employment change at all over six months, which is what an
unconverted saving looks like in aggregate.

The design decision under test: this is a *caveat*, not a refusal. The figure is
still produced, because the user may hold a conversion plan the assessment file
does not record. Suppressing the number would be as dishonest as hiding the
caveat.
"""

from __future__ import annotations

import json

import pytest

from ai_payback import (
    Assessment,
    load_spec,
    payback,
    score,
    to_json,
    to_markdown,
    total_cost_of_ownership,
)
from ai_payback.spec import Spec


@pytest.fixture(scope="module")
def spec() -> Spec:
    return load_spec()


def _assessment(**kwargs) -> Assessment:
    base = {
        "organisation": "Example Ltd",
        # Enough responses for score() to have something to work on; the values
        # are arbitrary and nothing here depends on the readiness figure.
        "responses": {"PP-14-Q1": 0, "PP-14-Q2": 1, "TD-01-Q1": 2, "AL-01-Q1": 3},
        "direct_costs": {"licences": 120_000.0, "internal_labour": 80_000.0},
        "net_monthly_benefit": 20_000.0,
        "elapsed_months": 24,
    }
    base.update(kwargs)
    return Assessment(**base)


def test_missing_conversion_path_produces_a_caveat(spec: Spec) -> None:
    a = _assessment()
    result = payback(a, total_cost_of_ownership(a, spec), spec)
    assert result.computed, "a caveat must not suppress the figure"
    assert result.months_low == pytest.approx(10.0)
    assert len(result.caveats) == 1
    assert "PP-14" in result.caveats[0]


def test_named_conversion_path_removes_the_caveat(spec: Spec) -> None:
    a = _assessment(
        benefit_conversion=(
            "BPO contract for tier-1 triage not renewed in March; "
            "owner: COO; decision date 2027-01-31."
        )
    )
    result = payback(a, total_cost_of_ownership(a, spec), spec)
    assert result.computed
    assert result.caveats == ()


def test_whitespace_is_not_a_conversion_path(spec: Spec) -> None:
    a = _assessment(benefit_conversion="   \n  ")
    assert not a.has_conversion_path
    result = payback(a, total_cost_of_ownership(a, spec), spec)
    assert len(result.caveats) == 1


def test_the_caveat_cites_its_primary_source(spec: Spec) -> None:
    """A claim carrying a number must carry where the number came from."""
    a = _assessment()
    caveat = payback(a, total_cost_of_ownership(a, spec), spec).caveats[0]
    assert "95.7%" in caveat
    assert "CES-WP-26-25" in caveat
    assert "Census" in caveat


def test_a_refusal_is_still_a_refusal_not_a_caveat(spec: Spec) -> None:
    """No benefit supplied outranks the caveat: there is nothing to caveat."""
    a = _assessment(net_monthly_benefit=None)
    result = payback(a, total_cost_of_ownership(a, spec), spec)
    assert not result.computed
    assert result.caveats == ()
    assert "inventing the answer" in result.refusal_reason


def test_the_caveat_reaches_the_rendered_report(spec: Spec) -> None:
    a = _assessment()
    cost = total_cost_of_ownership(a, spec)
    markdown = to_markdown(a, score(a, spec), cost, payback(a, cost, spec), spec)
    assert "Read this before using the figure" in markdown
    assert "95.7%" in markdown


def test_the_caveat_reaches_the_json(spec: Spec) -> None:
    a = _assessment()
    cost = total_cost_of_ownership(a, spec)
    payload = json.loads(to_json(a, score(a, spec), cost, payback(a, cost, spec), spec))
    assert len(payload["payback"]["caveats"]) == 1
    assert payload["assessment"]["benefit_conversion"] is None


def test_pp14_exists_and_carries_the_census_evidence(spec: Spec) -> None:
    barrier = spec.barrier("PP-14")
    assert "CENSUS-BTOS-2026" in barrier.evidence
    assert "95.7%" in (barrier.evidence_quote or "")


def test_the_six_new_barriers_are_present(spec: Spec) -> None:
    for barrier_id in ("PP-13", "PP-14", "PP-15", "PP-16", "PP-17", "TD-06"):
        assert spec.barrier(barrier_id).questions, f"{barrier_id} has no questions"


def test_nanda_is_no_longer_claimed_as_primary(spec: Spec) -> None:
    """The PDF became unreachable on 2026-07-30; the tier must reflect that."""
    nanda = spec.source("MIT-NANDA-2025")
    assert nanda["tier"] == "published"
    assert "DOWNGRADED" in nanda["tier_note"]


def test_the_census_paper_is_registered_as_primary(spec: Spec) -> None:
    census = spec.source("CENSUS-BTOS-2026")
    assert census["tier"] == "primary"
    assert census["verified_on"] == "2026-07-30"
    assert any("95.7%" in fact for fact in census["verified_facts"])
