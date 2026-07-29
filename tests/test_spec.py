"""The specification must be internally consistent and honestly sourced.

These tests are the guard against the failure this project most needs to avoid:
a coefficient or a claim entering the framework without a traceable source.
"""

from __future__ import annotations

import itertools

import pytest

from ai_payback import SpecError, load_spec
from ai_payback.spec import Spec


@pytest.fixture(scope="module")
def spec() -> Spec:
    return load_spec()


def test_spec_loads_and_validates(spec: Spec) -> None:
    assert spec.version
    assert spec.barriers
    assert spec.questions


def test_layer_weights_sum_to_one(spec: Spec) -> None:
    assert sum(spec.weights.values()) == pytest.approx(1.0)


def test_weights_match_bcg_allocation(spec: Spec) -> None:
    """The weights must stay equal to the BCG effort shares they came from.

    If someone changes a weight without changing the declared effort share, the
    documented derivation silently stops describing the code. That is exactly
    the drift this test exists to catch.
    """
    for layer in spec.framework["layers"]:
        assert spec.weights[layer["id"]] == pytest.approx(layer["bcg_effort_share"])


def test_every_barrier_has_a_known_source(spec: Spec) -> None:
    known = spec.source_ids
    for barrier in spec.barriers:
        assert barrier.evidence, f"{barrier.id} has no evidence"
        for source_id in barrier.evidence:
            assert source_id in known, f"{barrier.id} cites unknown source {source_id}"


def test_every_source_has_tier_url_and_verification_date(spec: Spec) -> None:
    for source_id, data in spec.sources["sources"].items():
        assert data.get("tier"), f"{source_id} has no provenance tier"
        assert data.get("url"), f"{source_id} has no URL"
        assert data.get("verified_on"), f"{source_id} has no verification date"


def test_no_unverified_source_is_used_as_evidence(spec: Spec) -> None:
    """Claims in the unverified pool must never be cited by a barrier."""
    unverified_ids = set(spec.sources.get("unverified", {}))
    for barrier in spec.barriers:
        assert not (set(barrier.evidence) & unverified_ids), (
            f"{barrier.id} cites an unverified claim"
        )


def test_ids_are_unique(spec: Spec) -> None:
    barrier_ids = [b.id for b in spec.barriers]
    question_ids = [q.id for q in spec.questions]
    assert len(barrier_ids) == len(set(barrier_ids))
    assert len(question_ids) == len(set(question_ids))


def test_question_ids_are_prefixed_with_their_barrier(spec: Spec) -> None:
    for barrier in spec.barriers:
        for question in barrier.questions:
            assert question.id.startswith(barrier.id), (
                f"{question.id} does not belong to {barrier.id} by name"
            )


def test_every_layer_has_barriers(spec: Spec) -> None:
    for layer_id in spec.layer_ids:
        assert spec.barriers_in_layer(layer_id), f"layer {layer_id} is empty"


def test_people_process_layer_is_the_largest(spec: Spec) -> None:
    """The 70 in 10-20-70 is the finding. It must survive refactoring."""
    assert spec.weights["PEOPLE_PROCESS"] > spec.weights["TECH_DATA"]
    assert spec.weights["TECH_DATA"] > spec.weights["ALGORITHMS"]


def test_bands_cover_the_whole_scale_without_gaps(spec: Spec) -> None:
    ranges = sorted(tuple(band["range"]) for band in spec.bands)
    assert ranges[0][0] == 0.0
    assert ranges[-1][1] == 4.0
    for (_, previous_high), (next_low, _) in itertools.pairwise(ranges):
        assert previous_high == next_low, "bands must be contiguous"


def test_cost_categories_reference_real_barriers(spec: Spec) -> None:
    barrier_ids = {b.id for b in spec.barriers}
    for category in spec.cost_model["omitted_cost_categories"]:
        for barrier_id in category.get("barriers") or []:
            assert barrier_id in barrier_ids


def test_only_the_no_estimate_preset_is_on_by_default(spec: Spec) -> None:
    """Shipping a preset that invents numbers by default would be dishonest."""
    presets = spec.cost_model["presets"]
    enabled = [k for k, v in presets.items() if v.get("enabled_by_default")]
    assert enabled == ["none"]


def test_illustrative_presets_declare_their_tier(spec: Spec) -> None:
    for category in spec.cost_model["omitted_cost_categories"]:
        if category.get("preset_share_range"):
            assert category.get("preset_source")
            assert category.get("preset_tier")


def test_missing_spec_directory_is_an_error(tmp_path) -> None:
    with pytest.raises(SpecError):
        Spec(tmp_path)


def test_the_three_version_strings_agree() -> None:
    """A result must be traceable to one version, not three that drifted apart.

    `__version__`, the distribution version and the framework version are set in
    three different files and were briefly inconsistent in 0.2.0 development.

    Read with a regex rather than `tomllib`, which is 3.11+ while this package
    supports 3.10. Only one field is needed, so a parser is not warranted.
    """
    import re
    from pathlib import Path

    import ai_payback

    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    match = re.search(
        r'^version = "([^"]+)"', pyproject.read_text(encoding="utf-8"), re.MULTILINE
    )
    assert match, "no version line found in pyproject.toml"
    distribution_version = match.group(1)

    assert ai_payback.__version__ == distribution_version == load_spec().version
