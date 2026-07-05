# P1 Result: One-Half Target And Recovery Contract

Date: 2026-06-27

## Status

`PASS_P1_ONE_HALF_CONTRACT_READY_FOR_P2`

## Decision

`PASS_P1_ONE_HALF_CONTRACT_READY_FOR_P2`

The Meta OT-aligned retained-Sinkhorn refit will predict **one canonicalized dual half**:
- **target half:** `canonical_log_u`

The complementary half will be recovered teacher-consistently from the retained Sinkhorn update rule:
- **recovery rule:** `log_v = g_from_f(log_u)` under the same teacher geometry, source weights, target weights, and epsilon.

This contract is now the controlling target/recovery rule for the refit program.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact one-half latent target should BayesFilter predict to stay as close as possible to the Meta OT donor-core route, and how will the complementary half be recovered teacher-consistently? |
| Baseline/comparator | Meta OT donor-core decomposition from the completed source-faithful closure program and the current BayesFilter dual-pair retained-Sinkhorn route. |
| Primary pass criterion | A result artifact freezes the one-half target, the gauge/canonicalization policy, the complementary-half recovery path, and the new route vocabulary for teacher-data and deployment. |
| Veto diagnostics | Ambiguous target half; no explicit recovery path; hidden fallback to free prediction of both halves; gauge convention left unspecified. |
| Explanatory diagnostics | Convenience of one half vs the other, implementation aesthetics, and latent-loss convenience only. |
| Not concluded | P1 does not yet update code or train the new route. |

## Why `canonical_log_u` Is The Chosen Half

### 1. It is the BayesFilter object already canonicalized explicitly
The current retained-Sinkhorn teacher-data runner already stores:
- `canonical_log_u`
- `canonical_log_v`
- `canonical_gauge_policy = mean_log_u_zero`

That means BayesFilter already has a stable gauge-fixed target representation on the `log_u` side.

### 2. It matches the donor-core one-half retained-teacher story cleanly
The chosen Meta OT donor-core route predicts **one dual half** and recovers the other half teacher-consistently. For BayesFilter's fixed-target retained-Sinkhorn lane, `canonical_log_u` is the cleanest first half to elevate into the donor-aligned target.

### 3. It keeps the current canonicalization convention intact
The current local gauge convention is:
- `mean_log_u_zero`

Retaining that convention avoids introducing a second gauge policy during the refit.

## Frozen Gauge / Canonicalization Rule

The one-half target contract is:
- store and predict `canonical_log_u`
- under the existing gauge policy `mean_log_u_zero`

Operationally:
- teacher-generated `(log_u, log_v)` remain canonicalized with `mean(log_u)=0`
- the predicted one-half target is the canonicalized `log_u`
- the complementary `log_v` is recovered from the teacher-side update rule rather than predicted freely as a second independent output.

## Frozen Complementary Recovery Rule

The complementary recovery path is now frozen as:
- given predicted `canonical_log_u`,
- recover `log_v` by applying the retained Sinkhorn teacher-side potential update under the same fixed geometry/cost, source weights, target weights, and epsilon.

This is the BayesFilter counterpart of the Meta OT donor-core `g_from_f(...)` story.

### Required semantic rule
The recovered half is **teacher-derived**, not a second free student output.

Any route that predicts both halves directly may still exist as historical comparison or alternative local path, but it is not the donor-aligned refit route.

## Updated Route Vocabulary

For the refit program, the core route must now use the following language:
- **learned object:** `canonical_log_u`
- **recovered object:** `log_v` obtained teacher-consistently from the retained update rule
- **optimized object:** student parameters for the one-half predictor
- **deployed object:** corrected retained-Sinkhorn barycentric output / replay object after complementary recovery and corrective Sinkhorn refinement

## Teacher-Data Consequences For P2

The updated teacher-data contract must preserve at least:
- `particles`
- `weights`
- `epsilon`
- `canonical_log_u` as the primary learned half-target
- sufficient teacher-side information to recover or validate the complementary half under the same teacher route
- `teacher_barycentric` / replay-critical corrected output information
- existing manifests / reproducibility digest / split metadata

The current data runner may continue to store `canonical_log_v` for audit/debugging, but it should no longer define the primary donor-aligned learned target.

## Deployment Consequences

The deployment path that must remain unchanged at the semantic level is:
1. predict `canonical_log_u`,
2. recover `log_v` teacher-consistently,
3. run corrective retained Sinkhorn,
4. evaluate corrected replay/residual behavior.

This preserves the donor-retained-teacher semantics while keeping BayesFilter's local corrected-route checks.

## What P1 Does Not Conclude

P1 does **not** conclude:
- that `canonical_log_u` is the only mathematically possible one-half target,
- that the current code already implements the one-half route,
- that objective-based training will work without further refit,
- or that the old dual-pair path should be deleted.

P1 only freezes the donor-aligned one-half target/recovery contract so P2/P3 can refit data and student code coherently.

## Next Step

Advance to:
- `docs/plans/bayesfilter-neural-ot-metaot-refit-p2-teacher-data-subplan-2026-06-27.md`

P2 will now refit the teacher-data and manifest contract so the one-half donor-aligned route becomes the new controlling artifact family for later training and heldout replay evaluation.
