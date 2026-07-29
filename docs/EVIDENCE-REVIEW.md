# Why enterprise AI does not pay back: an evidence review

**Compiled 30 July 2026.** Every claim below is tied to a named source with a verification
date. Where a source could not be re-reached, that is stated at the claim rather than hidden.

This document exists to answer one question — *why do so many firms get no return on AI?* —
and to test one proposed answer: that firms should deploy AI first into the departments that
generate additional profit (marketing, sales, customer support), and should digitise internal
processes.

The short version: **the second half of that proposal is well supported and almost nobody
does it. The first half is not a strategy, because it is already what almost everybody does.**

---

## 1. The size of the problem, and how much to trust the headline number

The number in circulation is that **95% of organisations are getting zero return** from
generative AI, against $30–40 billion of enterprise investment. It comes from MIT Project
NANDA, *The GenAI Divide: State of AI in Business 2025* (Challapally, Pease, Raskar, Chari,
July 2025).

Two cautions belong next to that number, and they are not decoration:

- **Provenance.** The primary PDF was read and quoted directly on 2026-07-29. On 2026-07-30 it
  was no longer reachable — `nanda.media.mit.edu` returns HTML rather than the PDF, and the
  Wayback Machine returns the same. The independent reviewer panel attempted retrieval
  separately and reported the same result. The quotations here are therefore from a document
  verified once, at first hand, and not re-verifiable today. Treat as **second-hand until the
  PDF is recovered.** A widely repeated derivative claim — that roughly half of GenAI budgets
  go to sales and marketing — could **not** be traced to the primary document and is not used
  here.
- **Method.** The finding rests on self-reported enterprise responses (roughly 150 interviews,
  a 350-person survey, 300 public deployments), non-probability sampling, and no audited P&L.
  It is a survey of what executives *say* their return was. That matters enormously, for
  reasons developed in §5.

A more defensible anchor for the same phenomenon, from a source that is reachable and
nationally representative:

> **Only 39% of respondents attribute any EBIT impact at all to AI, and most of those say it
> is under 5% of EBIT.** — McKinsey, *The State of AI* survey series.
> *(Exact figures shift between editions; the specific edition and page should be pinned
> before this is cited in a paper.)*

And from the Federal Reserve, on the state of measurement itself:

> Adoption is 18% of firms (BTOS) and 41% of workers (RPS), and the effects on productivity
> and employment are **not yet measured**; the sustainability of AI infrastructure investment
> is stated as an open question.
> — Jeffrey S. Allen, *Monitoring AI Adoption in the U.S. Economy*, FEDS Notes, Board of
> Governors of the Federal Reserve System, 3 April 2026,
> [doi:10.17016/2380-7172.4032](https://doi.org/10.17016/2380-7172.4032)

**What this means.** Nobody has yet measured the return on enterprise AI with instruments that
would satisfy an economist. The "95%" is a survey of impressions. That is not a reason to
dismiss it — impressions are what drive the next budget cycle — but it is a reason to be
precise about what is actually established.

---

## 2. The best evidence available: where AI is actually deployed

The strongest data source on this question is a US government working paper published in
April 2026:

> Kathryn Bonney, Cory Breaux, Emin Dinlersoz, Lucia Foster (U.S. Census Bureau), John
> Haltiwanger (University of Maryland), Aditya Pande — ***The Microstructure of AI Diffusion:
> Evidence from Firms, Business Functions, and Worker Tasks*, CES Working Paper 26-25**, U.S.
> Census Bureau Center for Economic Studies, April 2026.
> [PDF](https://www2.census.gov/library/working-papers/2026/adrm/ces/CES-WP-26-25.pdf) ·
> [landing page](https://www.census.gov/library/working-papers/2026/adrm/CES-WP-26-25.html)
> *Verified 2026-07-30: 79 pages, retrieved and parsed in full.*

It draws on the 2026 AI supplement to the Business Trends and Outlook Survey, is **nationally
representative** with weights reflecting the universe of US firms, and covers the reference
period **November 2025 – January 2026**. This is not a vendor survey of self-selected
enterprises. It is the closest thing that exists to ground truth.

### 2.1 Headline adoption

| Measure | Firm-weighted | Employment-weighted |
|---|---|---|
| Firms using AI in a business function | **18%** | 32% |
| Firms where workers use AI in tasks | 23% | 41% |
| Expected within six months | 22% | — |

Very large firms in Information, Professional Services and Finance reach **50–60%** (60–70%
employment-weighted). Filtered to top executives and owners at very large firms in those
sectors, it reaches **80%**.

### 2.2 Which functions — the finding that matters most here

Across 15 business functions, conditional on using AI in at least one:

| Rank | Function | Firm-weighted adoption |
|---|---|---|
| **1** | **Sales and Marketing** | **52%** (48% employment-weighted) |
| 2 | Strategy and Business Development | 45% |
| 3 | IT | 41% |
| 4 | R&D | (next, figure in Figure 7) |

Latent class analysis of AI-using firms produces five types:

| Firm type | Share of AI users | Behaviour |
|---|---|---|
| **Minimalist Adopters** | **37%** | Low probability of use across all functions |
| **Marketing Specialists** | **31%** | High in Sales and Marketing, low elsewhere; also customer service and public communications |
| Administrative Integrators | 15% | Management, Strategy, Finance, HR, PR, Legal |
| Technical Strategists | 12% | R&D, IT, Strategy |
| **Comprehensive Adopters** | **4%** | High probability across almost the entire functional set |

The paper's own summary of this: *"across almost all industries, AI-using firms are most likely
to fall into the minimalist or marketing specialist categories."*

Depth is shallow: **57%** of adopting firms use AI in three or fewer of fifteen functions, and
**24%** in exactly one. About 1% use it in all fifteen.

**This is the direct test of the proposal under examination.** "Deploy first into marketing,
sales and support" describes the behaviour of roughly two thirds of every AI-using firm in the
United States. It is the market default, not a differentiator. A recommendation that the
majority already follows cannot explain why the majority is not getting a return — and cannot
be the fix for it.

That is a statement about the recommendation's *information content*, not a causal claim that
marketing deployment causes low returns. The distinction matters, and §4 explains why the
causal version does not survive.

### 2.3 The size inversion nobody quotes

Employment-weighted, the ranking flips: **IT first, then Finance and Accounting, then Sales
and Marketing.**

Small firms deploy into marketing. Large firms deploy into IT and back office. The firms with
the capital and the data engineering capacity are already doing the thing the "back office is
underrated" argument recommends. What looks like a *strategic* difference is substantially a
*firm size and capability* difference.

Expected future increases are largest in sales and marketing, strategy, **customer service**,
and finance and accounting — so the concentration is set to deepen, not correct.

### 2.4 Complementary investment — and its absence

Changes to data management and storage practices, the complementary capital investment that
the productivity literature treats as the precondition for returns, occur in only **7–8% of
firms**. The least common organisational adjustment of all is hiring staff trained in AI.

Meanwhile **16%** of AI-using firms report replacing equipment and software with AI. The
paper's conclusion:

> *"in the current phase of diffusion, AI is serving more frequently as a substitute for legacy
> capital than for tasks and labor."*

### 2.5 Employment — the fact that breaks the naive cost-savings story

| AI-driven employment change, last six months | Firm-weighted | Employment-weighted |
|---|---|---|
| Increased | 2.3% | 3.7% |
| **Decreased** | **2.0%** | 2.4% |
| **No change** | **95.7%** | 93.9% |

Hold onto this table. It is the single most important number in this document, and §5 explains
why.

### 2.6 What correlates with performance

Regression analysis (linear probability models) finds a robust positive association between
firm commercial performance and the **breadth** of AI integration — functional breadth,
worker-task integration and operational investment together.

**The authors state explicitly that these are correlations, not causal estimates**, and name
the direction of future work as establishing causality. Two confounds are obvious and are not
controlled for:

- **Reverse causality** — firms that are already performing well have the slack to experiment
  across many functions.
- **Omitted variable** — digital maturity and management quality plausibly drive both broad
  adoption and good performance. (This is the Bloom–Van Reenen management-practices problem.)

And the paper's own J-curve language cuts against reading breadth as a simple prescription:

> *"broader structural investments and functional integration are likely the primary drivers of
> long-term productivity takeoff, **even if they depress measured performance in the short
> run**."*

If breadth depresses measured performance in the short run, then a small firm limiting itself
to one cheap reversible use case is not obviously making a mistake. It may be exercising
option value. That possibility has to be taken seriously rather than assumed away.

---

## 3. Where the causal evidence actually is

Almost all "AI ROI" numbers are surveys. Three bodies of work are different — they are field
experiments or staggered rollouts with control groups.

**Customer support — the strongest result in the literature.**
Erik Brynjolfsson, Danielle Li, Lindsey R. Raymond, **"Generative AI at Work"**, *The Quarterly
Journal of Economics* **140(2)**, May 2025, pp. 889–942
([QJE](https://academic.oup.com/qje/article/140/2/889/7990658); NBER WP 31161).
5,172 customer-support agents at a large software firm, staggered rollout supplemented by a
randomised controlled trial.

- **+15%** issues resolved per hour on average
- **+34–36%** for agents in the bottom skill quintile
- Near zero, with small quality declines, for the most experienced agents
- Improved customer sentiment, improved employee retention, evidence of worker learning

**Software development.** Field experiments with several thousand developers report large
increases in completed tasks. (*Effects of Generative AI on High-Skilled Work: Evidence from
Three Field Experiments with Software Developers*, Management Science, 2025.)

**Consulting-style knowledge work.** Task-level experiments show large speed gains on tasks
inside the tool's competence and *degradation* on tasks outside it.

**What the support result does and does not say.** It is a **throughput and quality** effect —
issues resolved per hour, handle time, first-contact resolution — concentrated among novices.
It is **not** a measurement of customer retention or churn reduction, and the paper does not
claim to be. Anyone citing it as evidence that "AI retains unhappy customers" has misread it.
Right department, wrong mechanism.

It also carries an external-validity limit that is rarely quoted: one large software firm, one
task type with an unusually clean outcome metric. Customer support is the function where AI
gains are easiest to *demonstrate* partly because it is the function where output is easiest to
*count*. That observation turns out to be the key to everything else here.

---

## 4. The hypothesis that failed, and why recording that matters

The working hypothesis for this review was:

> **Attribution asymmetry.** Firms deploy AI where value is most *visible*, not where it is
> most *measurable*. Revenue-side functions have structurally the hardest attribution;
> cost-side and back-office functions have effects that land in the P&L within 60–90 days.
> Therefore "AI shows no ROI" is partly an artefact of *where* AI was deployed.

It was put to two independent reviewers with instructions to destroy it. Both did, converging
on the same two objections from different directions. **The hypothesis is withdrawn.** The
reasons are worth preserving, because they are more informative than the hypothesis was.

**Objection 1 — marketing is the most instrumented function in business, not the least.**
Multi-touch attribution, marketing mix modelling, return on ad spend, geo-holdouts and
incrementality testing are mature quantitative disciplines with two decades of investment
behind them. A firm wanting to test AI-generated ad copy can run a holdout and read a
statistically significant result in days. The premise was inverted.

**Objection 2 — back-office savings do *not* land in the P&L. This is the decisive one.**
If an AI tool saves 100 staff thirty minutes a day, payroll does not change. Nobody is
dismissed; no contract is cancelled. The time is absorbed as organisational slack. The saving
is real at the level of the task and invisible at the level of the accounts.

**And this objection is confirmed by the primary source in §2.5, which I had already read.**
95.7% of AI-using firms report no employment change. If back-office AI produced trivially
bookable savings, that table would not look like that. My own evidence contradicted my own
claim, and I did not notice until two independent reviewers pointed at it.

**A third objection, on naming.** The phrase collides with attribution theory in social
psychology. The precise established term is **actor–observer asymmetry** (Jones & Nisbett,
1971, following Heider, 1958), not "attribution asymmetry" — one reviewer overstated the exact
collision — but the vocabulary is close enough that a management or information-systems referee
would read it as the psychology concept. *(Worth knowing if it is ever revived: Malle's 2006
meta-analysis of 173 studies found the actor–observer effect itself to be very small,
d = −0.016 to 0.095 —
[PubMed 17073526](https://pubmed.ncbi.nlm.nih.gov/17073526/).)*

**A fourth, on circularity.** The hypothesis tried to use the NANDA self-reported zero-return
survey as evidence that self-reporting mismeasures returns. That is circular, and it would have
been caught in review.

---

## 5. What survives, and it is better than what failed

Both objections are correct. Put them side by side and they do not cancel — they compose.

> **Front office:** the money is real but the *attribution* of it to AI is buried in noise.
> Marketing has attribution infrastructure at the *channel* level, but almost no firm runs a
> dedicated holdout to isolate the marginal contribution of an internal writing assistant —
> and the firms that dominate marketing-first adoption are small firms that own none of that
> infrastructure in the first place.
>
> **Back office:** the *attribution* is clean — handle time, entries processed, tickets closed
> — but the money never appears, because converting a time saving into cash requires somebody
> to cancel a contract, reduce overtime, decline to backfill a role, or absorb more volume
> without hiring. The Census employment table says that decision is essentially never taken:
> 95.7% no change.

**So both sides fail, for opposite reasons.** One has the cash without the proof; the other
has the proof without the cash. The "95% get zero return" statistic aggregates two structurally
different failures into one number, which is why it is so hard to act on.

This reframing has an immediate practical consequence, and it is the most useful thing in this
document:

> **The department is the wrong unit of decision.**
>
> The right question is not *"does this department generate revenue?"* but **"if this works,
> what specifically changes, who decides it, and when?"** If the answer is "nothing in
> particular" — no contract cancelled, no hire avoided, no additional volume taken on, no price
> or conversion change anyone will attribute — then the return will be zero regardless of which
> department it was deployed in. That is not a technology outcome. It is a decision that was
> never made.

**On originality.** The components are not new and must be cited, not claimed. Slack absorption
and mismeasurement are standard in the IT productivity literature — Brynjolfsson, *The
Productivity Paradox of Information Technology*, CACM 36(12), 1993; Brynjolfsson, Rock and
Syverson, *The Productivity J-Curve: How Intangibles Complement General Purpose Technologies*,
American Economic Journal: Macroeconomics 13(1), 2021, pp. 333–372. Deployment visibility bias
appears in practitioner form in the NANDA report itself. What may be publishable is the
**synthesis plus the operational consequence**, framed as a hypothesis with cited antecedents —
never as a priority claim.

---

## 6. Verdict on the proposal under test

| Claim | Verdict | Evidence |
|---|---|---|
| Deploy first into **marketing and sales** | **Not a strategy — it is the default.** 52% adoption, #1 of 15 functions; 68% of AI-using firms are minimalists or marketing-only | Census CES-WP-26-25 §2.2 |
| Deploy into **customer support** | **Best-evidenced department in the literature** — but for throughput, not retention | Brynjolfsson, Li & Raymond, QJE 140(2) 2025 |
| Purpose is **to retain unhappy customers** | **Mechanism not supported.** The measured effect is issues-per-hour and handle time. Churn was not the outcome variable | QJE 140(2) 2025 |
| **Change internal processes / redesign** | **Strongly supported.** Workflow redesign is the single largest EBIT lever identified; ~55% of high performers redesigned vs ~20% of others | McKinsey State of AI |
| **Digitise everything** | **Right direction, wrong scope.** Complementary data investment happens in only 7–8% of firms, so it is genuinely neglected — but doing it *everywhere first* is the J-curve trap, depressing measured performance before any takeoff | Census §2.4, §2.6; Brynjolfsson, Rock & Syverson 2021 |

**A defence of the original intuition that should be recorded.** Marketing-first may be
*rational* rather than mistaken. Those tools are self-serve, cost tens of dollars per seat,
need no security review, no ERP integration and no data engineering, and can be abandoned
without loss. That is low-regret option value under uncertainty. The correct criticism is not
"firms are being stupid" — it is that **a low-regret first move is not the same thing as a
payback strategy, and firms are mistaking one for the other.**

---

## 7. Failure mechanisms not yet in the instrument

Both reviewers independently judged the existing 20-barrier taxonomy incomplete. Cross-checking
their lists against the taxonomy in `ai-payback` v0.1, most were already covered. Six were not:

| # | Mechanism | Why it matters | Covered? |
|---|---|---|---|
| 1 | **No pre-deployment baseline** | Nobody logged handle time, error rate or rework before deployment, so improvement cannot be demonstrated even where it occurred | ❌ new |
| 2 | **No conversion path for the saving** | Time saved is absorbed as slack; no contract cancelled, no hire avoided, no volume added. §5. Census: 95.7% no employment change | ❌ new — **the central one** |
| 3 | **Verification tax** | A senior reviewer spending twenty minutes checking a five-second generation can cost more than writing from scratch. Consumes micro-gains in exactly the high-stakes work where AI is pitched hardest | ❌ new |
| 4 | **Vendor incentive misalignment** | Seat and token pricing rewards consumption, not efficiency. Successful adoption *raises* variable cost, unlike conventional software | ❌ new |
| 5 | **Shadow AI and tool sprawl** | Ten teams buy ten tools; no consolidation, no shared evaluation, knowledge siloed, spend invisible | ❌ new |
| 6 | **Simpler alternative never tested** | Rules, RPA or a better SQL query would solve much of the problem more cheaply and more reliably; AI is selected for signalling value | ❌ new |

Already covered, and confirmed by the cross-check: retrieval grounding (TD-05), model and
vendor churn (AL-01), drift (AL-03), data quality (TD-01), legacy integration (TD-02),
inference cost escalation (TD-04), compliance and security (cost model), workflow redesign
(PP-03), change management (PP-02), front-office investment bias (PP-08), benefit siloing
(PP-12), J-curve (framework).

---

## 8. Sources, with provenance tier

| Source | Tier | Verified |
|---|---|---|
| U.S. Census Bureau CES-WP-26-25, *The Microstructure of AI Diffusion*, April 2026 | **primary** — US government, nationally representative | 2026-07-30, full text retrieved and parsed |
| Federal Reserve FEDS Notes, Allen, *Monitoring AI Adoption in the U.S. Economy*, 3 Apr 2026, doi:10.17016/2380-7172.4032 | **primary** — US central bank | 2026-07-30 |
| Brynjolfsson, Li & Raymond, "Generative AI at Work", QJE 140(2), May 2025, pp. 889–942 | **primary** — peer-reviewed, top-five economics journal | 2026-07-30 |
| Brynjolfsson, Rock & Syverson, "The Productivity J-Curve", AEJ: Macroeconomics 13(1), 2021, pp. 333–372 | **primary** — peer-reviewed | prior session |
| NIST AI RMF 1.0 (NIST AI 100-1), January 2023 | **primary** — US federal standard | 2026-07-29 |
| SEI/Accenture *AI Adoption Maturity Model* v1.0, DM26-0590, 2026 | **published** — CMU SEI, FFRDC | 2026-07-29 |
| McKinsey *The State of AI* survey series | **analyst** — consultancy, self-selected respondents | edition and page still to be pinned |
| BCG 10-20-70 allocation principle | **analyst** — consultancy, N=735 | 2026-07-29 |
| MIT NANDA *The GenAI Divide*, July 2025 | **published, now unreachable** — read first-hand 2026-07-29; PDF not retrievable 2026-07-30 via direct fetch or Wayback | ⚠️ second-hand until recovered |
| "~50% of GenAI budgets go to sales and marketing" | **excluded** — could not be traced to the primary document | not used |

---

## 9. Honest limits of this review

- Nothing here is causal about *function choice*. The Census findings are descriptive and
  correlational, and the authors say so. This review does not claim that deploying into
  marketing causes low returns; it claims that doing so is the market default and therefore
  cannot be the differentiator that explains success.
- The 95% figure rests on self-report and is currently second-hand. It should not be leaned on
  for anything load-bearing.
- The reframing in §5 is a **hypothesis with cited antecedents**, not a finding. Testing it
  properly needs either restricted-access BTOS microdata through a Federal Statistical Research
  Data Center — a process measured in many months — or firm-level data with exogenous variation
  in measurement capability.
- The synthesis has not been peer reviewed. It has been attacked by two independent AI
  reviewers, which is a weaker filter and no substitute.

---

## 10. What follows from this

1. Reformulate the paper around the symmetric-measurement-failure framing in §5, as a
   hypothesis with full attribution to prior work — **never as a priority claim**.
2. Add the six missing mechanisms in §7 to the instrument, and make mechanism 2 change the
   *payback logic*, not merely add a question: an assessment with no named conversion path
   should be flagged, because the evidence says that is the condition under which return is
   near-certain to be zero.
3. Pin the McKinsey edition and page. Recover the NANDA PDF or drop it entirely.
