# P69 Phase 2 Task 0: Diagnostic-Cloud Feasibility Checkpoint

metadata_date: 2026-06-15
status: P69_PHASE2_TASK0_FEASIBILITY_PASSED
parent_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-subplan-2026-06-15.md
executor: Codex

## Decision

The diagnostic-cloud feasibility checkpoint passes with a constrained rule.

Phase 2 may implement post-fit holdout/replay diagnostics by constructing a
separate deterministic diagnostic batch through the same source-route ingredients
used by the fitted branch, then evaluating the already fitted square-root TT on
that batch.  The implementation must not split or remove rows from the current
ALS fit batch, must not pass diagnostic points to `FixedTTFitter.fit`, and must
verify that fit and density branch hashes are unchanged by diagnostics.

## Feasible Source-Route Cloud

The current code exposes the required ingredients:

| Ingredient | Current anchor | Feasibility result |
| --- | --- | --- |
| Previous sample batch at \(t=1\) | `bayesfilter/highdim/source_route.py:2235-2260` | Prior samples are deterministic under seed `6301`. |
| Previous retained prefix at \(t>1\) | `bayesfilter/highdim/source_route.py:2263-2281` | Previous retained physical samples are available and uniformly reweighted. |
| Push and augmentation | `bayesfilter/highdim/source_route.py:2284-2328` | Pushed and augmented samples are deterministic under `process_noise_seed=6400+t` and can be repeated with a separate recorded diagnostic seed. |
| Deterministic weighted resampling | `bayesfilter/highdim/source_route.py:2331-2351` | The current fit route uses deterministic quantile positions and recorded indices. |
| Local coordinate frame and target construction | `bayesfilter/highdim/source_route.py:2354-2480` | The fit helper returns the frame, local points, shifted square-root target values, shift, weights, and manifest. |
| Source target evaluation in same frame | `bayesfilter/highdim/source_route.py:470-540`; `bayesfilter/highdim/source_route.py:5837-5906` | A diagnostic local batch can be mapped to physical points and evaluated with the same shifted target convention. |
| Fixed TT evaluation | `bayesfilter/highdim/tt.py:199-223` | The fitted `FunctionalTT` can be evaluated after fitting without changing cores. |
| Branch identity | `bayesfilter/highdim/fitting.py:573-610` | Fitted branch hashes are deterministic manifests and can be compared before/after diagnostic evaluation. |

## Deterministic Rule To Implement

For each step \(t\):

1. Keep the existing fit data unchanged.
2. Build the fitted branch exactly as P68 did.
3. Construct a separate diagnostic batch using the same source-route model,
   observations, coordinate frame, target shift, and previous retained object.
4. Use recorded diagnostic seeds or deterministic index rules distinct from the
   fit route:
   - fit route uses current seeds `6301` and `6400+t`;
   - diagnostic route should use explicit diagnostic seeds, for example
     `7301` for the \(t=1\) prior diagnostic batch and `7400+t` for diagnostic
     process noise, or an equivalent named rule recorded in the manifest.
5. Map diagnostic local points through the fitted frame and evaluate the same
   shifted square-root target convention.
6. Evaluate the fitted `FunctionalTT` on diagnostic local points.
7. Record weighted RMS residuals, finite status, hashes, and branch before/after
   equality.

This is disjoint from the fitted ALS rows because the fitted ALS rows remain the
current `fit_data.local_fit_points`, while the diagnostic rows are generated
from a separate recorded diagnostic construction.  It is not an adaptive
Zhao--Cui data split claim; it is a `fixed_hmc_adaptation` diagnostic.

## Implementation Constraint

The current helper `_p59_author_sir_source_fit_data_for_step` computes its own
frame from the same data it returns.  Phase 2 should not use that helper
unchanged for diagnostics if doing so would create a new diagnostic frame or
shift.  Instead, implement a small diagnostic helper that reuses the fitted
frame and fitted shift, then evaluates the target on separate diagnostic
physical/local points.  If this proves more invasive than expected, stop with
`BLOCK_HOLDOUT_REPLAY_DESIGN_NEEDS_ROUTE_CHANGE`.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can Phase 2 identify a concrete source-route diagnostic cloud and deterministic split/replay rule before implementation edits? |
| Primary criterion status | Passed: concrete ingredients and a deterministic diagnostic-seed rule are identified. |
| Veto diagnostic status | No change to fit batch, no use of fitter holdout status path, no threshold change, no ladder rerun, no adaptive parity claim. |
| Main uncertainty | Exact helper shape is still an implementation question; the stop condition remains active if reusing the fitted frame/shift is not clean. |
| Next justified action | Implement post-fit diagnostics with branch-hash invariants and focused tests. |
| Not concluded | No implemented diagnostic yet, no ladder rerun, no validation pass, no d18 correctness. |

