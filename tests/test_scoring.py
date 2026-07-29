"""Scoring behaviour, especially the parts that must never quietly invent data."""

from __future__ import annotations

import pytest

from ai_payback import Assessment, ScoringError, load_spec, score
from ai_payback.spec import Spec


@pytest.fixture(scope="module")
def spec() -> Spec:
    return load_spec()


def _answer_all(spec: Spec, value: int) -> dict[str, int]:
    return {q.id: value for q in spec.questions}


def test_all_zeros_is_the_bottom_band(spec: Spec) -> None:
    result = score(Assessment("Zero Ltd", _answer_all(spec, 0)), spec)
    assert result.score == pytest.approx(0.0)
    assert result.band_id == "CRITICAL"
    assert result.is_complete


def test_all_fours_is_the_top_band(spec: Spec) -> None:
    result = score(Assessment("Four Ltd", _answer_all(spec, 4)), spec)
    assert result.score == pytest.approx(4.0)
    assert result.band_id == "COMPOUNDING"


def test_uniform_answers_reproduce_themselves(spec: Spec) -> None:
    """A weighted mean of a constant is that constant, whatever the weights."""
    for value in (0, 1, 2, 3, 4):
        result = score(Assessment("Flat Ltd", _answer_all(spec, value)), spec)
        assert result.score == pytest.approx(float(value))


def test_people_process_dominates_the_score(spec: Spec) -> None:
    """Strong people and process must beat strong technology. That is the thesis."""
    strong_people = {
        q.id: (4 if spec.barrier(q.barrier_id).layer == "PEOPLE_PROCESS" else 0)
        for q in spec.questions
    }
    strong_tech = {
        q.id: (0 if spec.barrier(q.barrier_id).layer == "PEOPLE_PROCESS" else 4)
        for q in spec.questions
    }
    assert (
        score(Assessment("People Ltd", strong_people), spec).score
        > score(Assessment("Tech Ltd", strong_tech), spec).score
    )


def test_unanswered_questions_are_not_scored_as_zero(spec: Spec) -> None:
    """The central fairness property: not answering is not the same as failing."""
    one = next(q for q in spec.questions)
    partial = score(Assessment("Partial Ltd", {one.id: 4}), spec)
    everything = score(Assessment("Full Ltd", _answer_all(spec, 4)), spec)

    assert partial.layers  # scored without error
    assert not partial.is_complete
    assert partial.coverage < 1.0
    assert partial.unanswered_question_ids
    # The one answered barrier scores 4, so it must not be dragged to zero.
    answered_barrier = next(
        bs
        for layer in partial.layers
        for bs in layer.barrier_scores
        if bs.barrier_id == one.barrier_id
    )
    assert answered_barrier.score == pytest.approx(4.0)
    assert everything.is_complete


def test_coverage_is_reported_accurately(spec: Spec) -> None:
    subset = list(spec.questions)[:10]
    result = score(Assessment("Ten Ltd", {q.id: 2 for q in subset}), spec)
    assert result.coverage == pytest.approx(10 / len(spec.questions))


def test_weakest_barriers_are_ranked_lowest_first(spec: Spec) -> None:
    responses = _answer_all(spec, 3)
    for question in spec.barrier("PP-04").questions:
        responses[question.id] = 0
    result = score(Assessment("Weak Ltd", responses), spec)
    assert result.weakest_barriers[0].barrier_id == "PP-04"


def test_weight_override_changes_the_result_and_travels_with_it(spec: Spec) -> None:
    strong_tech = {
        q.id: (0 if spec.barrier(q.barrier_id).layer == "PEOPLE_PROCESS" else 4)
        for q in spec.questions
    }
    flat = {"ALGORITHMS": 1 / 3, "TECH_DATA": 1 / 3, "PEOPLE_PROCESS": 1 / 3}
    default_result = score(Assessment("A", strong_tech), spec)
    flat_result = score(Assessment("A", strong_tech), spec, weights=flat)

    assert flat_result.score > default_result.score
    assert flat_result.weights == pytest.approx(flat)
    assert default_result.weights["PEOPLE_PROCESS"] == pytest.approx(0.70)


@pytest.mark.parametrize(
    "weights",
    [
        {"ALGORITHMS": 0.5, "TECH_DATA": 0.5, "PEOPLE_PROCESS": 0.5},  # sums to 1.5
        {"ALGORITHMS": 1.0},  # missing layers
        {"ALGORITHMS": 0.1, "TECH_DATA": 0.2, "PEOPLE_PROCESS": 0.6, "MADE_UP": 0.1},
    ],
)
def test_bad_weight_overrides_are_rejected(spec: Spec, weights: dict) -> None:
    with pytest.raises(ScoringError):
        score(Assessment("A", _answer_all(spec, 2)), spec, weights=weights)


@pytest.mark.parametrize("value", [-1, 5, 99])
def test_out_of_scale_responses_are_rejected(spec: Spec, value: int) -> None:
    one = next(q for q in spec.questions)
    with pytest.raises(ScoringError):
        score(Assessment("A", {one.id: value}), spec)


def test_unknown_question_id_is_rejected(spec: Spec) -> None:
    with pytest.raises(ScoringError):
        score(Assessment("A", {"NOT-A-QUESTION": 2}), spec)


def test_boolean_is_not_accepted_as_a_response(spec: Spec) -> None:
    """True would silently become 1 and quietly corrupt a score."""
    one = next(q for q in spec.questions)
    with pytest.raises(ScoringError):
        score(Assessment("A", {one.id: True}), spec)  # type: ignore[dict-item]


def test_empty_assessment_is_rejected(spec: Spec) -> None:
    with pytest.raises(ScoringError):
        score(Assessment("Nobody", {}), spec)
