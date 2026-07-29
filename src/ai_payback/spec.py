"""Loading and validating the framework specification.

The specification lives in YAML under `spec/`, not in Python. A user who
disagrees with a weight, a barrier or a source can edit the specification and
re-run without touching code, and can diff two specifications to see exactly
what changed between two results.
"""

from __future__ import annotations

import functools
from pathlib import Path
from typing import Any

import yaml

from .models import Barrier, Question

_SPEC_DIRNAME = "spec"
_REQUIRED_FILES = ("framework.yaml", "barriers.yaml", "cost_model.yaml", "sources.yaml")


class SpecError(RuntimeError):
    """The specification is missing, malformed, or internally inconsistent."""


def default_spec_dir() -> Path:
    """Locate the bundled specification.

    Installed packages carry `spec/` inside the package directory. A source
    checkout keeps it at the repository root, which is where it belongs for
    review and diffing.
    """
    packaged = Path(__file__).resolve().parent / _SPEC_DIRNAME
    if packaged.is_dir():
        return packaged
    repo_root = Path(__file__).resolve().parents[2] / _SPEC_DIRNAME
    if repo_root.is_dir():
        return repo_root
    raise SpecError(
        "specification directory not found; looked in "
        f"{packaged} and {repo_root}"
    )


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SpecError(f"missing specification file: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SpecError(f"{path.name} is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise SpecError(f"{path.name} must contain a mapping at the top level")
    return data


class Spec:
    """The loaded framework, validated for internal consistency."""

    def __init__(self, spec_dir: Path | str | None = None) -> None:
        self.dir = Path(spec_dir) if spec_dir else default_spec_dir()
        for name in _REQUIRED_FILES:
            if not (self.dir / name).is_file():
                raise SpecError(f"missing specification file: {self.dir / name}")

        self.framework = _load_yaml(self.dir / "framework.yaml")
        self._barriers_raw = _load_yaml(self.dir / "barriers.yaml")
        self.cost_model = _load_yaml(self.dir / "cost_model.yaml")
        self.sources = _load_yaml(self.dir / "sources.yaml")

        self.barriers: tuple[Barrier, ...] = self._parse_barriers()
        self._validate()

    # ------------------------------------------------------------- accessors

    @property
    def version(self) -> str:
        return str(self.framework.get("framework_version", "unknown"))

    @property
    def weights(self) -> dict[str, float]:
        raw = self.framework.get("weights", {})
        return {
            layer_id: float(raw[layer_id])
            for layer_id in self.layer_ids
            if layer_id in raw
        }

    @property
    def layer_ids(self) -> tuple[str, ...]:
        return tuple(str(layer["id"]) for layer in self.framework.get("layers", []))

    @property
    def layer_names(self) -> dict[str, str]:
        return {str(layer["id"]): str(layer["name"]) for layer in self.framework.get("layers", [])}

    @property
    def bands(self) -> list[dict[str, Any]]:
        return list(self.framework.get("readiness_bands", []))

    @property
    def j_curve_horizon_months(self) -> int:
        return int(self.framework.get("j_curve", {}).get("default_horizon_months", 18))

    @property
    def j_curve_statement(self) -> str:
        return str(self.framework.get("j_curve", {}).get("statement", "")).strip()

    @functools.cached_property
    def questions(self) -> tuple[Question, ...]:
        return tuple(q for barrier in self.barriers for q in barrier.questions)

    @functools.cached_property
    def question_ids(self) -> set[str]:
        return {q.id for q in self.questions}

    def barriers_in_layer(self, layer_id: str) -> tuple[Barrier, ...]:
        return tuple(b for b in self.barriers if b.layer == layer_id)

    def barrier(self, barrier_id: str) -> Barrier:
        for b in self.barriers:
            if b.id == barrier_id:
                return b
        raise KeyError(barrier_id)

    def source(self, source_id: str) -> dict[str, Any]:
        sources = self.sources.get("sources", {})
        if source_id not in sources:
            raise KeyError(source_id)
        return dict(sources[source_id])

    @property
    def source_ids(self) -> set[str]:
        return set(self.sources.get("sources", {}))

    def sei_capability_areas(self) -> set[str]:
        """Every SEI capability area referenced anywhere in the specification."""
        areas: set[str] = set()
        for barrier in self.barriers:
            areas.update(barrier.sei)
        for category in self.cost_model.get("omitted_cost_categories", []):
            areas.update(category.get("sei_capability_areas", []) or [])
        return areas

    # -------------------------------------------------------------- parsing

    def _parse_barriers(self) -> tuple[Barrier, ...]:
        parsed: list[Barrier] = []
        for entry in self._barriers_raw.get("barriers", []):
            barrier_id = str(entry["id"])
            questions = tuple(
                Question(
                    id=str(q["id"]),
                    text=" ".join(str(q["text"]).split()),
                    barrier_id=barrier_id,
                )
                for q in entry.get("questions", [])
            )
            parsed.append(
                Barrier(
                    id=barrier_id,
                    name=str(entry["name"]),
                    layer=str(entry["layer"]),
                    description=" ".join(str(entry.get("description", "")).split()),
                    evidence=tuple(str(e) for e in entry.get("evidence", [])),
                    sei=tuple(str(s) for s in entry.get("sei", [])),
                    nist=tuple(str(n) for n in entry.get("nist", [])),
                    questions=questions,
                    evidence_note=(
                        " ".join(str(entry["evidence_note"]).split())
                        if entry.get("evidence_note")
                        else None
                    ),
                    evidence_quote=(
                        " ".join(str(entry["evidence_quote"]).split())
                        if entry.get("evidence_quote")
                        else None
                    ),
                )
            )
        return tuple(parsed)

    # ----------------------------------------------------------- validation

    def _validate(self) -> None:
        problems: list[str] = []

        if not self.barriers:
            problems.append("barriers.yaml defines no barriers")

        layer_ids = set(self.layer_ids)
        if not layer_ids:
            problems.append("framework.yaml defines no layers")

        weights = self.framework.get("weights", {})
        for layer_id in layer_ids:
            if layer_id not in weights:
                problems.append(f"no weight defined for layer {layer_id}")
        weight_total = sum(float(weights[k]) for k in layer_ids if k in weights)
        if layer_ids and abs(weight_total - 1.0) > 1e-9:
            problems.append(f"layer weights sum to {weight_total}, expected 1.0")

        seen_barriers: set[str] = set()
        seen_questions: set[str] = set()
        known_sources = self.source_ids
        for barrier in self.barriers:
            if barrier.id in seen_barriers:
                problems.append(f"duplicate barrier id: {barrier.id}")
            seen_barriers.add(barrier.id)
            if barrier.layer not in layer_ids:
                problems.append(f"{barrier.id}: unknown layer {barrier.layer}")
            if not barrier.questions:
                problems.append(f"{barrier.id}: has no questions")
            if not barrier.evidence:
                problems.append(f"{barrier.id}: has no evidence source")
            for source_id in barrier.evidence:
                if source_id not in known_sources:
                    problems.append(f"{barrier.id}: unknown source id {source_id}")
            for question in barrier.questions:
                if question.id in seen_questions:
                    problems.append(f"duplicate question id: {question.id}")
                seen_questions.add(question.id)
                if not question.text:
                    problems.append(f"{question.id}: empty question text")

        for layer_id in layer_ids:
            if not self.barriers_in_layer(layer_id):
                problems.append(f"layer {layer_id} has no barriers")

        bands = self.bands
        if not bands:
            problems.append("framework.yaml defines no readiness bands")
        for band in bands:
            lo, hi = band.get("range", (None, None))
            if lo is None or hi is None or lo >= hi:
                problems.append(f"band {band.get('id')}: invalid range {band.get('range')}")

        for category in self.cost_model.get("omitted_cost_categories", []):
            for barrier_id in category.get("barriers", []) or []:
                if barrier_id not in seen_barriers:
                    problems.append(
                        f"cost category {category.get('id')}: unknown barrier {barrier_id}"
                    )

        if problems:
            raise SpecError(
                "specification failed validation:\n  - " + "\n  - ".join(problems)
            )


@functools.lru_cache(maxsize=4)
def load_spec(spec_dir: str | None = None) -> Spec:
    """Load and cache the specification."""
    return Spec(spec_dir)
