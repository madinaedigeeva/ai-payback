"""AI Payback Assessment.

An open instrument for assessing whether an enterprise AI adoption programme is
positioned to pay back, and for producing the ROI analysis document that AI
adoption maturity frameworks ask organisations to hold but do not define.

It is not a predictive model. It scores declared organisational conditions
against published evidence, computes cost under an explicit and user-visible
cost model, and shows its reasoning.

    >>> from ai_payback import Assessment, load_spec, score
    >>> spec = load_spec()
    >>> a = Assessment(organisation="Example Ltd", responses={"PP-01-Q1": 2})
    >>> result = score(a, spec)
    >>> result.band_label
    'Exposed'
"""

from __future__ import annotations

from .models import (
    Assessment,
    Barrier,
    BarrierScore,
    CostLine,
    CostResult,
    LayerScore,
    PaybackResult,
    Question,
    ReadinessResult,
)
from .report import to_json, to_markdown
from .scoring import ScoringError, score, score_barrier, score_layer
from .spec import Spec, SpecError, load_spec
from .tco import CostError, available_presets, payback, total_cost_of_ownership

__version__ = "0.1.0"

__all__ = [
    "Assessment",
    "Barrier",
    "BarrierScore",
    "CostError",
    "CostLine",
    "CostResult",
    "LayerScore",
    "PaybackResult",
    "Question",
    "ReadinessResult",
    "ScoringError",
    "Spec",
    "SpecError",
    "__version__",
    "available_presets",
    "load_spec",
    "payback",
    "score",
    "score_barrier",
    "score_layer",
    "to_json",
    "to_markdown",
    "total_cost_of_ownership",
]
