# AI Payback Assessment

An open instrument for assessing whether an enterprise AI adoption programme is
positioned to pay back — and for producing the ROI analysis document that AI
adoption maturity frameworks ask organisations to hold, but do not define how to
produce.

```bash
pip install ai-payback
ai-payback template > my-assessment.yaml   # fill it in
ai-payback run my-assessment.yaml          # get the analysis
```

---

## Why this exists

Enterprise AI adoption has a measurement gap, and the gap is documented by the
same organisations that set the standards.

**MIT Project NANDA**, in *The GenAI Divide: State of AI in Business 2025*,
reports that despite $30–40 billion of enterprise investment, "95% of
organizations are getting zero return," and that the cause is organisational
rather than technical.

**NIST's AI Risk Management Framework** (AI RMF 1.0) has 72 subcategories across
four functions. A full-text search of the published framework returns **zero**
occurrences of "return on investment", "payback", "profitability", "economic
value" or "adoption". The framework manages risk, which is its job. On
cost-benefit method it says only that this "will continue to be developed and
debated".

**The SEI/Accenture AI Adoption Maturity Model** measures process capability
across 8 dimensions and 25 capability areas. It lists **"ROI analysis"** among
the example artifacts required for Aligned AI (Level 3). It directs
organisations to "collect cost and revenue data along with model outputs to
support ROI analysis". And it reports that only **31%** of organisations
actually use business value and ROI to prioritise their AI roadmap.

So the leading maturity model requires the artifact, and the leading risk
framework declares the method an open question. This project is one attempt at
the method — an operational economic companion to a requirement that already
exists.

It does not claim to correct or complete either framework. Leaving financial
modelling out of a software-engineering maturity model is a reasonable boundary,
not an oversight.

## What it does

1. **Scores 60 diagnostic questions** across 20 barriers, grouped into three
   layers — algorithms, technology and data, people and processes — weighted
   10 / 20 / 70 after BCG's allocation principle.
2. **Builds a total cost of ownership** across the categories that published
   work reports as routinely omitted from AI budgets: integration, data
   preparation, training and change management, infrastructure scaling,
   compliance, and ongoing maintenance.
3. **Computes simple payback**, or refuses to and says why.
4. **Renders the analysis** as Markdown or JSON, with every figure traceable to
   its source.

## What it is not

- **Not a predictive model.** It does not forecast return. It scores conditions
  that published research associates with failure to realise return.
- **Not a benchmark of your organisation against others.** There is no
  comparison dataset in v0.1. When there is one, it will be built from real
  submitted assessments, never from synthetic data.
- **Not advice.** It produces an input to a decision, not the decision.
- **Not affiliated** with NIST, CMU SEI, Accenture, MIT, Project NANDA or BCG.
  Every mapping to their published work is this project's own reading of public
  documents.

## Design commitments

These are enforced by tests, not just stated.

**An unanswered question is never scored as zero.** Scoring a blank as "absent"
would turn an incomplete assessment into a bad one. Unanswered items are
excluded from the mean and reported by id, with a coverage figure.

**An unpriced cost is never treated as zero.** A category you costed at zero and
a category you never costed are different facts, and the report distinguishes
them. With the default settings, the total is stated as a **floor**, not an
estimate.

**No number is invented.** With the default preset the tool applies no
estimates at all. There is an optional preset that applies published share
ranges to produce an illustrative range — it is off by default, every line it
produces is labelled *illustrative* inline, and the report says the figures must
be replaced with your own before use in a business case.

**Payback is refused rather than fabricated.** If you do not supply a net
monthly benefit, no payback figure is produced. Substituting a benchmark benefit
would mean inventing the answer to the question being asked.

**Every coefficient carries a provenance tier.** Sources are recorded in
[`sources.yaml`](src/ai_payback/spec/sources.yaml) as `primary`, `published`,
`analyst` or `unverified`, each with the date its content was checked. Claims
that could not be traced to a reachable primary document are listed in an
`unverified` section and are **not used anywhere in the framework** — they are
published so you can see exactly what was excluded and disagree.

**The most contestable choice is stated, not buried.** BCG states 10-20-70 as an
allocation of *effort*. Using it as a set of *scoring weights* is this project's
own inference, not a finding of BCG's. It is documented in
[`framework.yaml`](src/ai_payback/spec/framework.yaml) under
`weights.derivation`, the weights are configurable, and every result carries the
weight vector that produced it.

## The specification is data, not code

Everything substantive lives in YAML under [`src/ai_payback/spec/`](src/ai_payback/spec/):

| File | Contents |
|---|---|
| `framework.yaml` | Layers, weights and their derivation, response scale, score bands, J-curve caveat |
| `barriers.yaml` | 20 barriers, 60 questions, mapped to SEI capability areas and NIST AI RMF subcategories |
| `cost_model.yaml` | Direct and omitted cost categories, presets, payback rules |
| `sources.yaml` | Every source with a provenance tier and verification date, plus the excluded pool |

Disagree with a weight, a barrier or a source? Edit the specification, re-run,
and diff the two results. You do not need to touch the code, and you can show
exactly what your change did.

## Usage

```bash
ai-payback questions          # print the instrument
ai-payback template           # blank assessment file to fill in
ai-payback run a.yaml         # score and report (Markdown)
ai-payback run a.yaml --format json
ai-payback run a.yaml --preset yedigeyeva_2026_illustrative
ai-payback validate           # check the specification is consistent
ai-payback sources            # sources and provenance tiers
```

As a library:

```python
from ai_payback import Assessment, load_spec, score, total_cost_of_ownership, payback, to_markdown

spec = load_spec()
a = Assessment(
    organisation="Example Ltd",
    responses={"PP-01-Q1": 2, "PP-01-Q2": 1},
    direct_costs={"licences": 100_000, "internal_labour": 150_000},
    net_monthly_benefit=25_000,
    elapsed_months=24,
)
readiness = score(a, spec)
cost = total_cost_of_ownership(a, spec)
print(to_markdown(a, readiness, cost, payback(a, cost, spec), spec))
```

## Method

Full derivation, mappings and limitations: [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

The framework operationalises Yedigeyeva, M. K. (2026), *Problems of
implementing artificial intelligence in enterprises. Reasons for low return on
investment and management solutions*, **Ekonomika i upravlenie: problemy,
resheniya** 11(5), pp. 263–280,
[doi:10.36871/ek.up.p.r.2026.05.11.027](https://doi.org/10.36871/ek.up.p.r.2026.05.11.027).

## Contributing

The most useful contribution is disagreement with a specific coefficient,
mapping or question, backed by a source. Open an issue naming the `src/ai_payback/spec/` line
and the source you would put in its place.

Contributions of synthetic or simulated assessment data will be declined. A
benchmark built on invented data would be worse than no benchmark.

## Licence

Apache-2.0. See [LICENSE](LICENSE).

## Citation

See [CITATION.cff](CITATION.cff), or use the GitHub "Cite this repository"
button.
