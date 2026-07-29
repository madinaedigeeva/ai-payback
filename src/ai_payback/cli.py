"""Command line interface.

    ai-payback questions                 print the instrument
    ai-payback template > my.yaml        write a blank assessment to fill in
    ai-payback run my.yaml               score it and render the report
    ai-payback validate                  check the specification is consistent
    ai-payback sources                   list sources and provenance tiers
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from .models import Assessment
from .report import to_json, to_markdown
from .scoring import ScoringError, score
from .spec import Spec, SpecError, load_spec
from .tco import CostError, payback, total_cost_of_ownership


def _load_assessment(path: Path) -> Assessment:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping at the top level")
    return Assessment(
        organisation=str(data.get("organisation", "unnamed organisation")),
        responses={str(k): int(v) for k, v in (data.get("responses") or {}).items()},
        direct_costs={str(k): float(v) for k, v in (data.get("direct_costs") or {}).items()},
        omitted_costs={str(k): float(v) for k, v in (data.get("omitted_costs") or {}).items()},
        currency=str(data.get("currency", "USD")),
        net_monthly_benefit=(
            float(data["net_monthly_benefit"])
            if data.get("net_monthly_benefit") is not None
            else None
        ),
        elapsed_months=(
            int(data["elapsed_months"]) if data.get("elapsed_months") is not None else None
        ),
        notes=data.get("notes"),
        benefit_conversion=data.get("benefit_conversion"),
    )


def cmd_questions(spec: Spec, _: argparse.Namespace) -> int:
    scale = spec.framework.get("response_scale", [])
    print("Answer every question on this scale:\n")
    for point in scale:
        print(f"  {point['value']}  {point['label']:<10} {point['description']}")
    print()
    for layer_id in spec.layer_ids:
        print(f"\n=== {spec.layer_names[layer_id]} "
              f"(weight {spec.weights[layer_id]:.0%}) ===")
        for barrier in spec.barriers_in_layer(layer_id):
            print(f"\n{barrier.id} — {barrier.name}")
            for question in barrier.questions:
                print(f"  [{question.id}] {question.text}")
    return 0


def cmd_template(spec: Spec, _: argparse.Namespace) -> int:
    lines = [
        "# AI Payback Assessment input.",
        "# Answer 0-4. Leave a question out rather than guessing:",
        "# unanswered questions are excluded from the score, not counted as zero.",
        "",
        "organisation: \"\"",
        "currency: USD",
        "",
        "# Months since the programme began. Used only for the J-curve caveat.",
        "elapsed_months:",
        "",
        "# Net benefit per month, in the currency above. Leave empty if unknown —",
        "# no payback figure will be produced, which is the correct outcome.",
        "net_monthly_benefit:",
        "",
        "# What specifically changes when the benefit is realised? A contract",
        "# ended, a hire not made, overtime reduced, volume absorbed without",
        "# hiring, a price or conversion rate moved — and who decides it, by when.",
        "# Leave empty if there is no answer yet. The payback figure will still be",
        "# produced, with a caveat: 95.7% of AI-using firms record no employment",
        "# change at all, which is what an unconverted saving looks like.",
        "benefit_conversion:",
        "",
        "responses:",
    ]
    for layer_id in spec.layer_ids:
        lines.append(f"  # --- {spec.layer_names[layer_id]} ---")
        for barrier in spec.barriers_in_layer(layer_id):
            lines.append(f"  # {barrier.id} {barrier.name}")
            for question in barrier.questions:
                lines.append(f"  # {question.text}")
                lines.append(f"  {question.id}:")
        lines.append("")
    lines.append("direct_costs:")
    for item in spec.cost_model.get("direct_cost_items", []):
        lines.append(f"  # {item['note']}")
        lines.append(f"  {item['id']}:")
    lines.append("")
    lines.append("# Cost categories most often left out of AI budgets.")
    lines.append("# Anything you leave empty is reported as UNPRICED, never guessed.")
    lines.append("omitted_costs:")
    for category in spec.cost_model.get("omitted_cost_categories", []):
        lines.append(f"  # {category['name']}")
        lines.append(f"  {category['id']}:")
    print("\n".join(lines))
    return 0


def cmd_run(spec: Spec, args: argparse.Namespace) -> int:
    assessment = _load_assessment(Path(args.input))
    readiness = score(assessment, spec)
    cost = total_cost_of_ownership(assessment, spec, preset=args.preset)
    payback_result = payback(assessment, cost, spec)
    if args.format == "json":
        print(to_json(assessment, readiness, cost, payback_result, spec))
    else:
        print(to_markdown(assessment, readiness, cost, payback_result, spec))
    return 0


def cmd_validate(spec: Spec, _: argparse.Namespace) -> int:
    print(f"specification directory: {spec.dir}")
    print(f"framework version:       {spec.version}")
    print(f"layers:                  {len(spec.layer_ids)}")
    print(f"barriers:                {len(spec.barriers)}")
    print(f"questions:               {len(spec.questions)}")
    print(f"sources:                 {len(spec.source_ids)}")
    print(f"SEI capability areas:    {len(spec.sei_capability_areas())}")
    unmapped = [b.id for b in spec.barriers if not b.maps_to_nist]
    print(f"barriers with no NIST mapping: {len(unmapped)}  ({', '.join(unmapped)})")
    print("\nvalidation passed")
    return 0


def cmd_sources(spec: Spec, _: argparse.Namespace) -> int:
    for source_id, data in spec.sources.get("sources", {}).items():
        print(f"[{data.get('tier', '?'):<10}] {source_id}")
        print(f"             {data.get('title', '').strip()[:100]}")
        if data.get("url"):
            print(f"             {data['url']}")
        print()
    excluded = spec.sources.get("unverified", {})
    if excluded:
        print("EXCLUDED — claims found unverifiable, not used anywhere:\n")
        for key, data in excluded.items():
            print(f"  {key}: {' '.join(str(data.get('claim', '')).split())[:150]}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-payback",
        description="Assess whether an enterprise AI adoption programme is positioned to pay back.",
    )
    parser.add_argument("--spec-dir", default=None, help="override the specification directory")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("questions", help="print the diagnostic instrument")
    sub.add_parser("template", help="print a blank assessment file")
    sub.add_parser("validate", help="check the specification is internally consistent")
    sub.add_parser("sources", help="list sources with their provenance tiers")

    run = sub.add_parser("run", help="score an assessment and render the report")
    run.add_argument("input", help="path to a filled-in assessment YAML file")
    run.add_argument(
        "--preset",
        default="none",
        help="cost preset; 'none' (default) makes no estimates at all",
    )
    run.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        spec = load_spec(args.spec_dir)
    except SpecError as exc:
        print(f"specification error: {exc}", file=sys.stderr)
        return 2

    handlers = {
        "questions": cmd_questions,
        "template": cmd_template,
        "run": cmd_run,
        "validate": cmd_validate,
        "sources": cmd_sources,
    }
    try:
        return handlers[args.command](spec, args)
    except (ScoringError, CostError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"file not found: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
