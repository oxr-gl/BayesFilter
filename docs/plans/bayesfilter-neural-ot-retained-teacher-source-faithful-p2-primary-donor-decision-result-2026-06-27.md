# P2 Result: Primary Donor Decision

Date: 2026-06-27

## Status

`PASS_P2_PRIMARY_DONOR_LOCKED_READY_FOR_P3`

## Decision

`PASS_P2_PRIMARY_DONOR_LOCKED_READY_FOR_P3`

BayesFilter will treat **Meta OT** as the **primary donor route** for the retained-teacher neural-OT source-faithful closure program.

`UNOT` is explicitly **deferred**, not rejected.

It remains the strongest secondary donor if later phases show that BayesFilter needs a more operator-style discrete entropic OT route or that Meta OT's donor-core decomposition fails on a blocker that UNOT can better satisfy.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Given the audited donor evidence from P1, which single donor route should BayesFilter treat as the primary source-faithful target for retained-teacher neural OT: Meta OT or UNOT? |
| Baseline/comparator | The P1 donor-anchor audit result, the earlier fit note, and the retained-teacher chapter definition in `docs/chapters/ch32d_retained_teacher_neural_ot.tex`. |
| Primary pass criterion | A decision result chooses exactly one primary donor, explicitly defers the other, and records the reasons in terms of predicted object match, retained correction semantics, adaptation burden, and route fit. |
| Veto diagnostics | No forced donor decision; trying to keep both donors active at once; choosing on vague preference rather than the audited comparison table; silently mixing donor concepts before a decision. |
| Explanatory diagnostics | Secondary strengths of the deferred donor, optional future value, and unresolved donor-specific risks. |
| Not concluded | P2 does not yet port code or prove source faithfulness. |

## Decision Table

| Field | Meta OT | UNOT | P2 reading |
| --- | --- | --- | --- |
| Official donor repo confirmed | Yes | Yes | Tie |
| Visible license signal from repo page | CC BY-NC 4.0 | MIT | Favors UNOT for permissiveness, but not enough to override semantic fit without a full license blocker decision |
| Predicted object fit to retained-teacher chapter | single dual / solver-native latent state | dual-derived latent / log-scaling operator state | Favors Meta OT |
| Corrective teacher semantics fit | explicit corrected Sinkhorn retained-teacher story | compatible, but more operator-centric | Favors Meta OT |
| Deployment object fit | corrected teacher output after warm-start | corrected Sinkhorn-style or reconstructed transport object | Slight edge to Meta OT |
| Framework adaptation burden | JAX/OTT to TF/TFP | Torch/FNO/operator stack to TF/TFP | Both medium-to-high; no clear winner |
| Representation bridge to unordered particle clouds | nontrivial but conceptually smaller | larger bridge from grid/resolution-centric operator inputs | Favors Meta OT |
| Route fit for first faithful retained-teacher closure | strongest warm-start donor | strongest secondary discrete entropic/operator donor | Favors Meta OT |

## Why Meta OT Is First

### 1. Closest semantic match to the BayesFilter retained-teacher chapter definition
BayesFilter's chapter definition for this lane is:
- learn a teacher-native solver latent,
- preserve the teacher correction step,
- deploy the corrected teacher output.

Among the audited donors, Meta OT is the clearest direct match to this retained-teacher story.

### 2. Cleaner warm-start donor before wider operator adaptation
Meta OT is the cleaner route for the question:
> can BayesFilter learn solver-native state so the same teacher problem is solved from a better starting point?

That is the narrowest faithful question to answer before deciding whether BayesFilter needs the richer operator framing represented by UNOT.

### 3. Smaller representation leap for the first closure attempt
UNOT remains highly relevant, but its route carries a larger bridge from grid / resolution-centric measure/operator inputs into BayesFilter's unordered particle-cloud setting.

For the first source-faithful closure pass, BayesFilter should choose the donor that minimizes semantic branching before port/decomposition. That donor is Meta OT.

## Why UNOT Is Deferred Rather Than Rejected

UNOT remains valuable because:
- it is strongly aligned with discrete entropic OT,
- it predicts a dual-derived latent object highly relevant to Sinkhorn-style retained-teacher routes,
- it may become the better donor if BayesFilter later decides that an operator-style dual/log-scaling route is the right long-term representation.

UNOT is therefore deferred for two specific future scenarios:
1. Meta OT donor-core decomposition reveals a blocker that makes its route materially less faithful or less portable than expected.
2. BayesFilter later needs a donor whose core strength is operator-style dual/log-scaling prediction across richer problem families.

## Deferred-Donor Return Conditions

BayesFilter may reopen UNOT as the primary donor only if one or more of the following occur during P3/P4:
- Meta OT donor-core extraction is blocked by license, runability, or dependency constraints that cannot be cleanly isolated,
- Meta OT's actual donor-core predicted object is found to be less compatible with the BayesFilter retained-teacher route than the current paper-level reading suggests,
- the BayesFilter adapter boundary shows that a dual/log-scaling operator donor is the closer faithful route after all,
- or Meta OT decomposition reveals that BayesFilter would need a larger semantic redesign than UNOT would.

Until then, UNOT is explicitly secondary.

## P3 Target Lock

P3 will now target **Meta OT** specifically.

The required decomposition target is:
- the narrowest Meta OT retained-teacher path that shows
  - what latent object is predicted,
  - how the complementary dual information is recovered,
  - how the corrective teacher solve is retained,
  - and what parts of the donor repo are core method versus experiment shell.

## P3 Blocker Checks To Answer

The next phase must answer at minimum:
1. **Exact donor-core object**
   - What exact dual or solver-native object does the source implementation actually predict?
2. **Complementary-state recovery path**
   - Where in the donor route is the complementary dual information recovered?
3. **Corrective teacher closure path**
   - What exact source module/function preserves the final corrective teacher solve?
4. **Core vs benchmark separation**
   - Which donor files are core retained-teacher method and which are experiment scaffolding only?
5. **License / runability blocker check**
   - Is the donor route decomposable or portable in practice, and what explicit blockers exist if not?

## What P2 Does Not Conclude

P2 does **not** conclude:
- that Meta OT can be copied directly into BayesFilter,
- that Meta OT is license-cleared for direct reuse,
- that UNOT is wrong or irrelevant,
- that BayesFilter has already achieved source faithfulness,
- or that the annealed LEDH route is already closed under Meta OT.

P2 only locks the first donor target for source-faithful closure.

## Next Step

Advance to P3 under:
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p3-minimal-port-subplan-2026-06-27.md`

P3 must now decompose or minimally port the Meta OT donor-core route before any further custom neural-OT design proceeds.
