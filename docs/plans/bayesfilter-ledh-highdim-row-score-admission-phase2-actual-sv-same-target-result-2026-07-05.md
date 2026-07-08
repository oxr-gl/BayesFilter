# Phase 2 Result: Actual-SV Same-Target Adapter And Score

Date: 2026-07-06

Status: `BLOCK_PHASE2_ACTUAL_SV_ROW_TARGET_BRIDGE_UNREVIEWED`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Do not admit the current actual-SV LEDH value or score row yet. The current GPU/XLA route is not the old Gaussian-closure Lane-B scalar, but the repo still lacks a reviewed row-target bridge from the executed raw-likelihood-corrected LEDH scalar to the declared transformed actual-SV leaderboard row. |
| Primary criterion status | Passed by precise blocker: the current code path was traced exactly, the old Gaussian-closure explanation was ruled out for this LEDH runner, and the remaining blocker was narrowed to row-target admission rather than generic plumbing. |
| Veto diagnostic status | Passed: no autodiff score was admitted, no Gaussian-closure surrogate was mislabeled as the leaderboard target, and no unreviewed raw-to-transformed bridge was promoted as settled. |
| Main uncertainty | Whether the current raw-likelihood-corrected LEDH scalar should be admitted as the transformed row target after an explicit reviewed bridge is written, or whether the row must be rewired to consume the transformed target directly. |
| Next justified action | Advance to Phase 3 with a clearer transformed-SV target discipline: KSC must be treated as its own target family and must not inherit actual-SV Gaussian-closure language by analogy. |
| What is not concluded | No admitted actual-SV LEDH value row, no admitted actual-SV LEDH score row, no HMC readiness, and no claim that the current runner already closes the transformed-row contract. |

## Question Answered

Phase 2 asked:

- Does the current LEDH actual-SV row compute the declared transformed actual-SV
  scalar, and if not, what exactly is wrong?

Answer:

- The current LEDH actual-SV runner is not the old augmented-noise Gaussian
  innovation scalar.
- It drives the flow with a `log(y_t^2)` surrogate observation, but its
  importance correction uses the raw actual-SV observation density.
- That means the current runner is more precise than the old Gaussian-closure
  story, but the repo still does not contain a reviewed row-target admission
  artifact proving that this executed scalar is the declared transformed
  leaderboard row target, or an explicitly accepted constant-offset equivalent.

So the correct Phase 2 close is:

- not `wrong because it is Gaussian closure`;
- not `already admitted same-target`;
- instead: `blocked because the row-target bridge is still unreviewed`.

## Evidence

Current row target:

- The source-scope contract defines
  `zhao_cui_sv_actual_nongaussian_T1000` as
  `stochastic_volatility_transformed_actual_nongaussian`:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
- The July 3 LEDH row ledger and closeout keep this row blocked as
  `blocked_no_reviewed_current_gpu_xla_ledh_row_adapter`:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json`
  and
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md`

Corrected transformed-target note:

- The corrected derivation note says the transformed target is one exact
  `z_t = log(y_t^2)` target and rejects the old Gaussian-closure scalar as
  same-target evidence:
  `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`

Current LEDH callback trace:

- `_dpf_sv_callbacks(...)` constructs
  `ledh_flow_observations = log(y_t^2 + 1e-6) - 2 log(beta)` for the flow:
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:1541`
- The same callback declares
  `target_observation_density = raw_zero_mean_sv_normal_log_density`
  and marks the adapter as a BayesFilter extension adapter for non-Gaussian SV
  flow, not source-core Algorithm 1 evidence:
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:1624`
- The generic LEDH runner call for this row passes the surrogate-transformed
  observations into the flow update, but the importance correction uses
  `target_observation_log_density(...)` evaluated against the original raw
  observations:
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:1989`
  and
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:3376`
- The core Algorithm 1 implementation confirms that `observation` drives the
  UKF flow update while `observation_log_density_fn(...)` enters the corrected
  log weights:
  `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:1`
  and
  `tests/test_ledh_pfpf_alg1_ukf_tf.py:474`

Why this is not the old Gaussian-closure blocker:

- The rejected Lane-B Gaussian-closure routes in
  `bayesfilter/highdim/sv_mixture_cut4.py`
  explicitly accumulate a Gaussian innovation scalar and declare
  `not exact transformed same-target admission`.
- The current LEDH actual-SV callback does not use that scalar in the
  importance correction. It uses the raw actual-SV observation log density
  instead.

What remains missing:

- The repo still lacks a reviewed admission artifact proving that the current
  raw-likelihood-corrected LEDH scalar is the exact declared transformed row
  target, or an admitted constant-offset equivalent for leaderboard purposes.
- Existing artifacts still correctly say that no reviewed current LEDH adapter
  proves that target identity.

## Plain Scientific Classification

The current actual-SV LEDH runner is not the old Gaussian-closure surrogate
that the corrected derivation note rejects.

Instead, the current runner is:

1. a surrogate-observation flow proposal;
2. followed by raw actual-SV likelihood importance correction.

That is a materially different object from the old Gaussian-closure scalar.

However, the declared leaderboard row is still the transformed actual-SV row,
and the repo has not yet written and reviewed the exact bridge between that row
contract and the current GPU/XLA runner.

Therefore:

- current actual-SV LEDH row admission: blocked;
- reason: row-target bridge unreviewed;
- not because the current runner is merely reusing the old Gaussian-closure
  scalar.

## Required Checks Run

```bash
rg -n "actual[-_ ]SV|transformed actual-SV|log\\(y_t\\^2\\)|blocked_no_reviewed_current_gpu_xla_ledh_row_adapter|wrong relative to the stated target|same-target" docs/plans docs/chapters bayesfilter docs/benchmarks experiments tests
```

Result: passed; the transformed-row contract, corrected derivation note, July 3
blocker language, and current callback traces were all located.

```bash
git diff --check -- docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase2-actual-sv-same-target-result-2026-07-05.md docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase3-ksc-sv-same-target-subplan-2026-07-05.md docs/plans/bayesfilter-ledh-highdim-row-score-admission-visible-execution-ledger-2026-07-05.md docs/reviews/ledh-highdim-row-score-admission-phase2-review-bundle-2026-07-06.md
```

Result: pending until this phase close patch is complete, then rerun.

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Answered directly: the current runner is not the old Gaussian-closure scalar, but the transformed-row admission bridge is still unreviewed. |
| Baseline/comparator | Passed: source-scope row contract, corrected derivation note, July 3 row ledger/closeout, callback trace, and core LEDH implementation agree with this narrower classification. |
| Primary criterion | Passed by blocker: the exact executed object is now clearer than before, and the remaining blocker is explicit. |
| Veto diagnostics | Passed: no wrong scalar was admitted and no autodiff score evidence was promoted. |
| Explanatory diagnostics | The scalar-SV graph route remains useful as historical fixed-randomness gradient evidence for its own scoped objective, not as leaderboard row admission proof. |
| Not concluded | No actual-SV row promotion and no score repair yet. |

## Next-Phase Handoff

Phase 3 should proceed with a tighter transformed-SV boundary:

- KSC remains a distinct surrogate row and must not inherit actual-SV target
  language casually.
- Actual-SV Phase 2 clarified that LEDH flow-surrogate language and
  importance-correction language must be separated explicitly.
- The current actual-SV blocker is now narrow enough that KSC can advance
  without pretending the actual-SV row is already admitted.
