"""Scoring an assessment into a readiness result.

Two rules govern this module.

First, an unanswered question is never treated as a zero. Scoring a missing
answer as "absent" turns an incomplete assessment into a bad one and would let
an organisation look worse simply for not finishing the form. Unanswered items
are excluded from the mean and reported by id.

Second, nothing here is a probability. The output is a weighted mean on the
0-4 response scale, and the bands are descriptive labels for regions of that
scale.
"""

from __future__ import annotations

from .models import Assessment, BarrierScore, LayerScore, ReadinessResult
from .spec import Spec, load_spec


class ScoringError(ValueError):
    """The assessment cannot be scored as supplied."""


def _band_for(score: float, spec: Spec) -> dict:
    bands = spec.bands
    for band in bands:
        low, high = band["range"]
        if low <= score < high:
            return band
    # The top of the scale is inclusive in the highest band.
    return bands[-1]


def score_barrier(barrier_id: str, assessment: Assessment, spec: Spec) -> BarrierScore:
    barrier = spec.barrier(barrier_id)
    answered: list[int] = []
    unanswered: list[str] = []
    for question in barrier.questions:
        value = assessment.responses.get(question.id)
        if value is None:
            unanswered.append(question.id)
        else:
            answered.append(value)

    score = sum(answered) / len(answered) if answered else 0.0
    return BarrierScore(
        barrier_id=barrier.id,
        name=barrier.name,
        layer=barrier.layer,
        score=score,
        answered=len(answered),
        total_questions=len(barrier.questions),
        unanswered_question_ids=tuple(unanswered),
    )


def score_layer(layer_id: str, assessment: Assessment, spec: Spec) -> LayerScore:
    barrier_scores = tuple(
        score_barrier(b.id, assessment, spec) for b in spec.barriers_in_layer(layer_id)
    )
    scored = [bs for bs in barrier_scores if bs.answered > 0]
    layer_score = sum(bs.score for bs in scored) / len(scored) if scored else 0.0
    return LayerScore(
        layer_id=layer_id,
        name=spec.layer_names[layer_id],
        score=layer_score,
        weight=spec.weights[layer_id],
        barrier_scores=barrier_scores,
    )


def score(
    assessment: Assessment,
    spec: Spec | None = None,
    *,
    weights: dict[str, float] | None = None,
    weakest: int = 5,
) -> ReadinessResult:
    """Score an assessment.

    `weights` overrides the specification's layer weights. An override must
    cover every layer and sum to 1.0; the resulting weights travel with the
    result so that two results are never compared across different weightings.
    """
    spec = spec or load_spec()

    problems = assessment.validate_responses(spec.question_ids)
    if problems:
        raise ScoringError("assessment is not usable:\n  - " + "\n  - ".join(problems))

    if not assessment.responses:
        raise ScoringError("assessment contains no responses")

    effective_weights = dict(spec.weights)
    if weights is not None:
        missing = set(spec.layer_ids) - set(weights)
        if missing:
            raise ScoringError(f"weight override is missing layers: {sorted(missing)}")
        unknown = set(weights) - set(spec.layer_ids)
        if unknown:
            raise ScoringError(f"weight override has unknown layers: {sorted(unknown)}")
        total = sum(weights.values())
        if abs(total - 1.0) > 1e-9:
            raise ScoringError(f"weight override sums to {total}, expected 1.0")
        effective_weights = {k: float(v) for k, v in weights.items()}

    layers = tuple(
        LayerScore(
            layer_id=ls.layer_id,
            name=ls.name,
            score=ls.score,
            weight=effective_weights[ls.layer_id],
            barrier_scores=ls.barrier_scores,
        )
        for ls in (score_layer(lid, assessment, spec) for lid in spec.layer_ids)
    )

    overall = sum(layer.weighted_contribution for layer in layers)
    band = _band_for(overall, spec)

    all_barrier_scores = [bs for layer in layers for bs in layer.barrier_scores]
    answered_ids = set(assessment.responses)
    unanswered = tuple(sorted(spec.question_ids - answered_ids))
    coverage = len(answered_ids & spec.question_ids) / len(spec.question_ids)

    ranked = sorted(
        (bs for bs in all_barrier_scores if bs.answered > 0),
        key=lambda bs: (bs.score, bs.barrier_id),
    )

    return ReadinessResult(
        score=overall,
        band_id=str(band["id"]),
        band_label=str(band["label"]),
        band_meaning=" ".join(str(band["meaning"]).split()),
        layers=layers,
        weights=effective_weights,
        framework_version=spec.version,
        coverage=coverage,
        unanswered_question_ids=unanswered,
        weakest_barriers=tuple(ranked[:weakest]),
    )
