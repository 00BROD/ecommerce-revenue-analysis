# Business Analysis Case: Acquisition-Channel Budget Reallocation

> A BABOK-structured business-analysis wrapper around the data analysis in [ANALYSIS.md](ANALYSIS.md). Where ANALYSIS.md shows *the numbers*, this shows *the business reasoning* — need, stakeholders, current vs future state, requirements, acceptance criteria, and a governed change strategy. Each section is tagged to its BABOK v3 Knowledge Area / technique.

---

## 1. Problem / Business Need  ·  *[Strategy Analysis — BACCM: Need]*

Marketing allocates acquisition budget by **CAC** (cost to acquire). The Discount channel has the lowest CAC, so it keeps winning budget. But CAC measures *cost*, never *value* — so we may be scaling the cheapest customers to acquire and the least valuable to keep.

**Who feels the pain:** Growth owns a budget that looks efficient on the dashboard while blended customer value quietly erodes. Finance sees acquisition spend rise faster than revenue.

## 2. Stakeholders  ·  *[BA Planning & Monitoring — Stakeholder List/Map + RACI]*

| Stakeholder | Interest | Influence | Needs from this analysis |
|---|---|---|---|
| Head of Growth | Hit growth targets efficiently | High | A defensible rule for where the next dollar goes |
| Performance-Marketing Lead | Channel performance | High | Which channels to scale / cut |
| Finance | Spend vs return | Medium | Revenue impact, stated assumptions |
| CMO | Brand + growth balance | Medium | One-line decision + risk |

**RACI for the reallocation decision:** Head of Growth **A** · Performance-Marketing Lead **R** · Finance **C** · CMO **I**.

## 3. Current State  ·  *[Strategy Analysis — Analyze Current State]*

- Channels funded on **CAC efficiency**; Discount ranks "best" and is ~18% of acquisition.
- Reality, measured on equal 90-day windows per customer:

| Channel | Avg 90-day revenue | Repeat rate |
|---|--:|--:|
| Referral | $265 | 44.0% |
| Organic | $255 | 44.5% |
| Paid Search | $228 | 45.4% |
| Paid Social | $208 | 43.9% |
| **Discount** | **$142** | **34.9%** |

The lowest-CAC channel delivers **~45% less 90-day value** and the worst retention. Decision rule and reality are misaligned.

## 4. Future State & Objectives  ·  *[Strategy Analysis — Define Future State]*

- **New decision rule:** rank channels on **90-day contribution per acquisition dollar**, not CAC alone.
- **Measurable objective:** lift blended 90-day revenue per acquired customer by reallocating away from low-value acquisition, validated within 2 quarters.

## 5. Gap Analysis & Change Strategy  ·  *[Strategy Analysis — Define Change Strategy]*

**Gap:** decisions are made on a metric (CAC) that ignores the value half of the equation.
**Change strategy:**
1. Re-rank channel mix on 90-day value (already computed).
2. Reallocate ~50% of Discount acquisition volume toward Referral (highest-value, under-scaled) via a referral program.
3. **Transition control:** run a **holdout test** before full reallocation — do not move 100% on observational evidence.

## 6. Requirements  ·  *[RLCM — Prioritize + Trace]*

| # | Requirement | Traces to | Priority |
|---|---|---|---|
| R1 | Reporting must surface **90-day contribution by channel**, not just CAC | §3 finding | High |
| R2 | Acquisition budget rules must rank channels by value-per-dollar | §4 objective | High |
| R3 | Stand up a **referral program** to absorb reallocated volume | §5 step 2 | Medium |
| R4 | Reallocation must be gated by a **holdout/geo test** | §5 step 3 | High |
| R5 | Capture **channel-level CAC/spend** to compute true contribution margin | §8 gap | Medium |

## 7. Acceptance / Evaluation Criteria  ·  *[Acceptance and Evaluation Criteria]*

- **Pass:** blended 90-day revenue/customer rises with no increase in blended CAC, and the holdout shows reallocated spend produces ≥ Referral-grade value (CI excludes zero).
- **Guardrail:** total acquired customers must not fall >10% (don't starve the funnel).
- **Fail/rollback:** holdout shows no value lift, or volume guardrail breached.

## 8. Risks & Assumptions  ·  *[Risk Analysis and Management]*

| Risk / assumption | Mitigation |
|---|---|
| Referral can't absorb redirected volume | Phase reallocation; cap; measure CPA as it scales |
| Per-customer value assumed constant under reallocation | Validate with holdout, not extrapolation |
| **No ad-spend/margin data** → impact framed in revenue, not margin | Implement R5; recompute on contribution |
| Observational data ≠ causal | Holdout test before full commitment |

## 9. Recommendation & Quantified Value  ·  *[Financial Analysis · Decision Analysis]*

Move ~50% of Discount volume (~519 customers/period) to Referral-grade acquisition:

```
519 × ($265 − $142) ≈ $64K incremental 90-day revenue  ≈  ~$255K annualized run-rate
```

Stated assumptions (held value constant, Referral absorbs volume) and **gated on a holdout test**. Concentration supports it: the **top 20% of customers drive ~60% of revenue** (Pareto), so customer *quality* compounds — exactly what Discount under-delivers.

## 10. Solution Evaluation Plan  ·  *[Solution Evaluation — Measure Solution Performance]*

- **Measure:** 90-day revenue/customer by channel, blended CAC, total acquisition volume — monthly.
- **When:** read the holdout at full 90-day maturity (no peeking).
- **Scale criteria:** holdout confirms ≥ Referral-grade value → expand reallocation.
- **Kill criteria:** no value lift or volume guardrail breached → roll back, keep Discount at current share.

---

*BABOK Knowledge Areas exercised here: Strategy Analysis · BA Planning & Monitoring · Requirements Life Cycle Management · Requirements Analysis & Design Definition · Solution Evaluation. Elicitation & Collaboration is addressed separately in [ELICITATION-PLAN.md](ELICITATION-PLAN.md).*
