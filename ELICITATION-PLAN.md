# Elicitation Plan — Acquisition-Channel Analysis

> *Honesty note:* this dataset is synthetic, so no live stakeholder elicitation occurred. This documents the **elicitation approach I would run** on a real engagement — the BABOK *Elicitation & Collaboration* discipline — and the assumptions this analysis currently makes *in place of* answered questions. It is a plan, not a claim that interviews happened.

## BACCM framing
- **Need:** confirm whether acquisition budget is allocated on the right metric.
- **Primary stakeholder:** Head of Growth (decision owner).
- **Context to learn:** how budget decisions are actually made today, and what constraints exist.

## Elicitation techniques I'd use  ·  *[BABOK §10 techniques]*

| Technique | Applied here |
|---|---|
| **Interviews** | 1:1 with Head of Growth + Performance-Marketing Lead: how is budget set, what's the current decision rule, what counts as success? |
| **Document Analysis** | Review existing CAC dashboards, channel reports, the data dictionary, prior test readouts. |
| **Workshop** | Align Growth + Finance on a shared definition of "channel value" (CAC vs contribution) before changing the rule. |
| **Observation** | Sit in on a budget-planning meeting to see the real decision process, not the stated one. |

## Questions I'd need answered (currently assumptions)

| Open question | Assumption made in this analysis | Risk if wrong |
|---|---|---|
| Is CAC truly the current decision rule? | Yes — budget follows lowest CAC | Recommendation aims at the wrong rule |
| What's the target payback window? | 90 days is a fair value horizon | Wrong window changes channel ranking |
| Can Referral scale, and at what CPA? | It can absorb redirected volume | Reallocation stalls / CPA spikes |
| Is there channel-level spend/margin data? | Not available — impact framed in revenue | Can't compute true contribution |
| Who signs off on a budget reallocation? | Head of Growth (A), Finance (C) | Change stalls without right approver |

## Collaboration / sign-off  ·  *[Elicitation & Collaboration — Confirm + Communicate]*
- Confirm elicitation results back to stakeholders before acting (avoid acting on a misheard need).
- Communicate the finding as a one-page exec summary + one chart (done in ANALYSIS.md), not a SQL walkthrough.

---
*This file plus [BUSINESS-ANALYSIS.md](BUSINESS-ANALYSIS.md) bring the project's BABOK coverage to 5 of 6 Knowledge Areas. The honest residual gap: real, executed stakeholder elicitation — best demonstrated from live work experience, not synthetic data.*
