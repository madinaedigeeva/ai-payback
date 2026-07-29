"""Data structures for the AI Payback Assessment.

Every result object carries the inputs and the framework version that produced
it. Results computed under different weights or different framework versions
are therefore never silently comparable, which is the point.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

MIN_RESPONSE = 0
MAX_RESPONSE = 4


@dataclass(frozen=True)
class Question:
    """A single diagnostic item, answered on the 0-4 scale."""

    id: str
    text: str
    barrier_id: str


@dataclass(frozen=True)
class Barrier:
    """A named obstacle to realising return, with its provenance and mappings."""

    id: str
    name: str
    layer: str
    description: str
    evidence: tuple[str, ...]
    sei: tuple[str, ...]
    nist: tuple[str, ...]
    questions: tuple[Question, ...]
    evidence_note: str | None = None
    evidence_quote: str | None = None

    @property
    def maps_to_nist(self) -> bool:
        """False for barriers that are purely economic or organisational.

        Not an omission. The AI RMF is a risk framework, and the absence of a
        mapping is itself part of what this project documents.
        """
        return bool(self.nist)


@dataclass(frozen=True)
class BarrierScore:
    barrier_id: str
    name: str
    layer: str
    score: float
    answered: int
    total_questions: int
    unanswered_question_ids: tuple[str, ...] = ()

    @property
    def is_complete(self) -> bool:
        return not self.unanswered_question_ids


@dataclass(frozen=True)
class LayerScore:
    layer_id: str
    name: str
    score: float
    weight: float
    barrier_scores: tuple[BarrierScore, ...]

    @property
    def weighted_contribution(self) -> float:
        return self.score * self.weight


@dataclass(frozen=True)
class ReadinessResult:
    """The output of scoring an assessment.

    `score` is a weighted mean on the 0-4 response scale. It is not a
    probability, a percentage, or a forecast of any financial outcome.
    """

    score: float
    band_id: str
    band_label: str
    band_meaning: str
    layers: tuple[LayerScore, ...]
    weights: dict[str, float]
    framework_version: str
    coverage: float
    unanswered_question_ids: tuple[str, ...] = ()
    weakest_barriers: tuple[BarrierScore, ...] = ()

    @property
    def is_complete(self) -> bool:
        return not self.unanswered_question_ids


@dataclass(frozen=True)
class CostLine:
    """One line of the cost model.

    `priced` distinguishes a category the user costed at zero from one the user
    never costed at all. Conflating those two is the failure this class exists
    to prevent.
    """

    id: str
    name: str
    amount: float | None
    priced: bool
    category: str  # "direct" or "omitted"
    source: str  # "user" or the id of the preset that supplied it
    low: float | None = None
    high: float | None = None

    @property
    def is_illustrative(self) -> bool:
        return self.source != "user"


@dataclass(frozen=True)
class CostResult:
    """Total cost of ownership under an explicit, named model."""

    currency: str
    direct_total: float
    lines: tuple[CostLine, ...]
    preset: str
    total_low: float
    total_high: float
    unpriced_category_ids: tuple[str, ...] = ()

    @property
    def is_floor_only(self) -> bool:
        """True when nothing was estimated, so the total is a floor not an estimate."""
        return self.preset == "none"

    @property
    def has_illustrative_lines(self) -> bool:
        return any(line.is_illustrative for line in self.lines)


@dataclass(frozen=True)
class PaybackResult:
    """A payback figure, or an explicit refusal to produce one.

    A refusal is a first-class result. The library never substitutes a
    benchmark benefit for a benefit the user did not supply.
    """

    computed: bool
    months_low: float | None = None
    months_high: float | None = None
    refusal_reason: str | None = None
    j_curve_caveat: str | None = None
    elapsed_months: int | None = None


@dataclass
class Assessment:
    """The complete input to an assessment run."""

    organisation: str
    responses: dict[str, int] = field(default_factory=dict)
    direct_costs: dict[str, float] = field(default_factory=dict)
    omitted_costs: dict[str, float] = field(default_factory=dict)
    currency: str = "USD"
    net_monthly_benefit: float | None = None
    elapsed_months: int | None = None
    notes: str | None = None

    def validate_responses(self, valid_question_ids: set[str]) -> list[str]:
        """Return a list of problems. An empty list means the input is usable."""
        problems: list[str] = []
        for qid, value in self.responses.items():
            if qid not in valid_question_ids:
                problems.append(f"unknown question id: {qid}")
            if not isinstance(value, int) or isinstance(value, bool):
                problems.append(f"{qid}: response must be an integer, got {type(value).__name__}")
            elif not MIN_RESPONSE <= value <= MAX_RESPONSE:
                problems.append(
                    f"{qid}: response {value} outside the scale {MIN_RESPONSE}-{MAX_RESPONSE}"
                )
        for key, value in {**self.direct_costs, **self.omitted_costs}.items():
            if value < 0:
                problems.append(f"{key}: cost must not be negative")
        if self.net_monthly_benefit is not None and not isinstance(
            self.net_monthly_benefit, (int, float)
        ):
            problems.append("net_monthly_benefit must be a number")
        if self.elapsed_months is not None and self.elapsed_months < 0:
            problems.append("elapsed_months must not be negative")
        return problems

    def to_dict(self) -> dict[str, Any]:
        return {
            "organisation": self.organisation,
            "responses": dict(self.responses),
            "direct_costs": dict(self.direct_costs),
            "omitted_costs": dict(self.omitted_costs),
            "currency": self.currency,
            "net_monthly_benefit": self.net_monthly_benefit,
            "elapsed_months": self.elapsed_months,
            "notes": self.notes,
        }
