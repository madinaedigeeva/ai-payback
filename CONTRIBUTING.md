# Contributing

Thank you for considering a contribution to AI Payback Assessment. This project
exists to make one narrow thing measurable, and the most useful contributions
are the ones that improve the measurement.

## The kind of contribution that helps most

The specification in `src/ai_payback/spec/` is the substance of the project.
Coefficients, mappings, questions and sources should be **arguable from
evidence**, and the best way to help is to disagree with a specific line and
name the source you would put in its place.

- Open an issue naming the exact file, section and line, and quote the source
  (with a DOI, URL and page number where the claim appears).
- If the source is behind a paywall, quote the relevant sentence and provide
  the bibliographic identifier so a reviewer can request the paper.
- Contributions that would make a barrier easier to interpret without changing
  what it measures are welcome under the same rule.

## What will not be accepted

- **Synthetic or simulated assessment data.** The tool's usefulness depends on
  the distinction between real and invented data being preserved. A benchmark
  built on fictional inputs is worse than no benchmark.
- Changes that add tracking, telemetry, analytics or any form of usage
  reporting. This is a measurement tool; it must not itself measure its users.
- Contributions that pad the specification with untested barriers, or increase
  the question count without evidence of construct validity.
- LLM-generated text passed off as an authored source. Prose is welcome; a
  citation to a machine-produced summary in place of the underlying literature
  is not.

## Development

Setup, tests and lint checks are documented in the
[README](README.md#contributing). In brief:

```bash
python -m venv venv && venv/bin/pip install -e ".[dev]"
venv/bin/python -m pytest && venv/bin/ruff check . && venv/bin/ai-payback validate
```

Continuous integration runs the same three commands on Python 3.10, 3.11, 3.12
and 3.13 on Linux. A pull request that reduces coverage or leaves a lint
warning will not merge.

### Working on the specification

The specification files in `src/ai_payback/spec/` are the machine-readable
part. Every change to them must:

1. Keep the file valid — `ai-payback validate` must succeed.
2. Update `taxonomy_version` in `barriers.yaml` when a barrier changes, and
   summarise the reason in the changelog at the top of that file.
3. Preserve the `nist: []` marker on barriers with no AI RMF mapping. Absence
   is meaningful in this project; do not delete the marker to make the file
   look tidier.

### Coding style

Python code follows the settings in `pyproject.toml`. `ruff` handles the rest;
formatting is not negotiated in review.

## Reporting issues

Bugs and questions belong in
[GitHub Issues](https://github.com/madinaedigeeva/ai-payback/issues). When you
open an issue, include:

- what you ran, exactly (`ai-payback` command and its arguments);
- what happened, including the full traceback if any;
- what you expected instead;
- the version (`ai-payback --version`) and the Python version.

## Reporting a security issue

Please do not open a public issue for a security problem. Email
[madina.edigeeva2001@gmail.com](mailto:madina.edigeeva2001@gmail.com) with a
subject beginning `ai-payback security:` and a description of the issue and
the version affected. You will get a first response within seven days.

## Pull requests

- Small, single-purpose pull requests are easier to review and easier to
  revert.
- Reference the issue the pull request closes.
- Include a test for a behaviour change or a bug fix. A change that cannot be
  tested is a design signal worth discussing in the pull request.
- The commit message should say **why** the change is needed. The code shows
  what changed.

## Code of Conduct

Participation in this project is governed by the
[Contributor Covenant](CODE_OF_CONDUCT.md). By contributing, you agree to
abide by its terms.

## Licence

Contributions are accepted under the same [Apache-2.0](LICENSE) licence as the
project. You retain your copyright; you grant the project the right to
distribute your contribution under that licence.
