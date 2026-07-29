# Methodology

Version 0.1.0 · 2026-07-29

This document states what the instrument does, what each number rests on, and
where it can be wrong. It is written to be argued with. Every coefficient,
mapping and modelling step below can be checked against `src/ai_payback/spec/sources.yaml`,
which records a provenance tier and a verification date for each source.

---

## 1. The problem

Enterprise AI adoption has a measurement gap, and it is documented by the
institutions that set the standards rather than asserted here.

**MIT Project NANDA**, *The GenAI Divide: State of AI in Business 2025*
(Challapally, Pease, Raskar, Chari; July 2025), from 150 leader interviews, a
350-employee survey and 300 public deployments:

> Despite $30–40 billion in enterprise investment into GenAI, this report
> uncovers a surprising result in that 95% of organizations are getting zero
> return.

> Just 5% of integrated AI pilots are extracting millions in value, while the
> vast majority remain stuck with no measurable P&L impact.

**NIST AI Risk Management Framework 1.0** (NIST AI 100-1, January 2023) has four
functions and 72 subcategories. A full-text search of the published document
returns:

| Term | Occurrences |
|---|---|
| "return on investment" | 0 |
| "ROI" | 0 |
| "payback" | 0 |
| "profitab*" | 0 |
| "financial return" | 0 |
| "economic value" | 0 |
| "adoption" | 0 |
| "cost-benefit" | 1 |

The single occurrence reads:

> Emerging knowledge and methods to better inform harm/cost-benefit tradeoffs
> will continue to be developed and debated by businesses, governments,
> academia, and civil society.

That is not a defect. The AI RMF manages risk and trustworthiness, which is what
it is for, and it says openly that cost-benefit method remains an open area.

**The SEI/Accenture AI Adoption Maturity Model v1.0** (Carnegie Mellon
University Software Engineering Institute, 2026, DM26-0590) covers 8 dimensions,
25 capability areas and 5 maturity levels. It mentions ROI 26 times, and
contains zero occurrences of "payback" or "financial". What it does is
**require the artifact**:

- "Example Artifacts • **ROI analysis**" — for Aligned AI (Level 3), in the
  Workflow Re-Engineering and Operations dimensions.
- Monitoring capability area, Practice 3: "Collect cost and revenue data along
  with model outputs to support **ROI analysis**."
- Business Workflow Innovation, Practice 4: "Prioritize candidate business
  processes and workflows for AI adoption according to estimated improvements
  and ROI against business goals."
- AI Strategy Development: "Define and monitor the **costs and implications of
  failed adoption**."
- And: "the January 2026 SEI Accenture survey found that only **31%** of
  organizations rely on business value and ROI prioritization when assessing and
  developing their AI adoption roadmap."

**The gap this instrument addresses is therefore specific and narrow.** The
maturity model requires an ROI analysis as evidence of maturity and does not
define how to produce one, because financial modelling is an economic and
management discipline rather than a software-engineering process capability.
That boundary is reasonable. This project supplies an open method on the other
side of it.

## 2. What the instrument measures

Three things, kept deliberately separate so that a weakness in one is never
disguised by a strength in another.

**Readiness** — a weighted mean of 60 answers about organisational conditions,
on a 0–4 scale. It is not a probability and not a forecast.

**Cost of ownership** — the sum of what the organisation actually costed,
across direct categories and the categories most often omitted. With default
settings it makes no estimates, and reports a **floor** rather than an estimate.

**Payback** — total cost divided by net monthly benefit, or an explicit refusal
when the benefit is unknown.

## 3. The three layers and their weights

Layers follow BCG's allocation principle, verified against BCG's own
publications:

> The 10-20-70 Rule: Focus 10% of your AI efforts on algorithms, 20% on the
> underlying technology and data, and 70% on people and processes.
> — BCG, *CEO's Guide to Maximizing Value Potential from AI*, 3 July 2024

Restated in BCG's later work: "BCG has established a guiding principle of
10/20/70 for resource allocation" (BCG, *Scaling AI Requires New Processes, Not
Just New Tools*, 2026). Survey basis given as the 2023–24 BCG Build for the
Future C-level (Gen)AI Surveys, N = 735.

### A naming note, and a correction to the source paper

Yedigeyeva (2026) presents the identical allocation as "the 70-20-10 rule",
ordering the shares largest first. BCG's own name is **10-20-70**, ordered
algorithms → technology and data → people and processes. The substance is the
same; this instrument uses BCG's ordering to stay aligned with the source.

### The contestable step

**BCG states 10-20-70 as an allocation of *effort*. BCG does not state it as a
set of importance weights for scoring an assessment.** Using the effort
allocation as an importance weighting is this project's own modelling step and
is the single most contestable choice in the specification.

The reasoning: if 70% of the work that determines whether a transformation
sticks is people and process, a weakness there should dominate an assessment of
whether it will stick.

That is an inference, not a finding. It is stated here rather than buried so it
can be rejected. The weights are configurable, and every result carries the
weight vector that produced it, so results computed under different weights are
never silently compared.

## 4. The barriers

Twenty barriers, drawn from Yedigeyeva (2026) and corroborated where possible
against the primary sources that paper cites.

| Layer | Barriers | Count |
|---|---|---|
| People and processes | PP-01 … PP-12 | 12 |
| Technology and data | TD-01 … TD-05 | 5 |
| Algorithms | AL-01 … AL-03 | 3 |

Each barrier carries its evidence source ids, a mapping to SEI capability areas,
and a mapping to NIST AI RMF subcategories where one exists.

### A result the mapping itself produces

**Seven of the twenty barriers map to no NIST AI RMF subcategory at all:**
PP-01, PP-02, PP-03, PP-07, PP-08, PP-12 and TD-04.

Six of the seven sit in the people-and-process layer — the layer BCG's
allocation says carries 70% of the work. This is not an omission in the
mapping; it is a measurement of the gap. The barriers most associated with
failure to realise return are economic and organisational, and a risk framework
does not address them because that is not what a risk framework is for.

## 5. The cost model

Six categories that published work reports as routinely absent from AI budgets:
integration and customisation; data preparation and quality; training and change
management; infrastructure scaling and data transfer; compliance, security and
legal; ongoing maintenance and evaluation.

**What is asserted:** the category structure. It is supported by Yedigeyeva
(2026) and corroborated by the capability areas of the SEI model.

**What is not asserted:** the percentage shares. Yedigeyeva (2026) reports them,
but attributes them upstream only to unnamed consulting analysts, and no
reachable primary document was found for the ranges. They ship as an optional
preset, `yedigeyeva_2026_illustrative`, **off by default**, and every line it
produces is labelled *illustrative* inline in the report.

The related claim that total AI programme cost is underestimated by 40–60% is
recorded in `src/ai_payback/spec/sources.yaml` under `unverified` and **is not implemented
anywhere.**

## 6. Payback

```
payback_months = total_cost_of_ownership / net_monthly_benefit
```

Simple, undiscounted, deliberately. An organisation that cannot yet name its
omitted costs is not helped by a discount rate.

Three refusals are built in:

1. **No benefit supplied** → no figure. Substituting a benchmark benefit would
   mean inventing the answer to the question being asked.
2. **Benefit ≤ 0** → no figure, and a plain statement that the programme does
   not pay back under the supplied numbers.
3. **Programme younger than the horizon** (default 18 months) → figure given,
   J-curve caveat attached, and the programme is never characterised as
   underperforming on cost data alone.

### The J-curve

After Brynjolfsson, Rock and Syverson (*The Economics of Artificial
Intelligence: An Agenda*, University of Chicago Press, 2019, pp. 23–57), via
Yedigeyeva (2026): measured productivity commonly falls before it rises, because
complementary intangible investment is expensed immediately while its returns
arrive later. A negative early return is not by itself evidence of failure, and
a positive one is not by itself evidence of success.

## 7. Provenance discipline

Every source in `src/ai_payback/spec/sources.yaml` carries a tier:

| Tier | Meaning |
|---|---|
| `primary` | Published by the organisation that produced the finding, reachable, and verified against the document itself |
| `published` | A peer-reviewed publication reporting the finding |
| `analyst` | A named commercial analyst or consultancy, published |
| `unverified` | Circulates in the literature; no reachable primary document found. **Never used as a default.** |

`verified_on` records the date the document was fetched and the quoted text
confirmed inside it — not merely that a URL returned 200.

Four claims are published in the `unverified` pool and used nowhere: the
hidden-cost percentage shares, a Gartner abandonment figure, an S&P Global
abandonment trend, an IBM compute-cost trend, and a pair of BCG use-case counts.
They are listed so that a reader can see exactly what was excluded and argue
that it should not have been.

## 8. What this cannot do

- **It cannot predict return.** There is no validated relationship between the
  readiness score and any financial outcome, and none is claimed. Establishing
  one would require outcome data this project does not have.
- **It cannot benchmark you against others.** v0.1 contains no comparison data.
  If a benchmark is ever published it will be built from real submitted
  assessments and never from synthetic data.
- **It inherits its sources' limitations.** NANDA's build-versus-buy figures are
  self-reported, from an interview sample rather than a random sample; the
  report says so and this instrument treats them as directional only.
- **It does not audit your answers.** An organisation that scores itself
  generously gets a generous score. The instrument is a structured
  conversation, not an inspection.
- **The weights are an inference** (section 3), and if that inference is wrong
  the ranking of layers is wrong with it.

## 9. Roadmap

**v0.2** — an open benchmark from real submitted assessments, published with its
own DOI, under an explicit consent and anonymisation policy. No synthetic data,
ever.

**v0.3** — sensitivity analysis over the weights, so a user can see how much of
a result depends on the contestable step in section 3.

**Alongside** — an English-language description of the framework submitted to a
peer-reviewed venue, so that the method is reviewed by people who are not its
author.

## 10. Citation

Software: see `CITATION.cff`.

The framework operationalises: Yedigeyeva, M. K. (2026). Problems of
implementing artificial intelligence in enterprises. Reasons for low return on
investment and management solutions. *Ekonomika i upravlenie: problemy,
resheniya*, 11(5), 263–280.
https://doi.org/10.36871/ek.up.p.r.2026.05.11.027
