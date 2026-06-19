# P69 Phase 2 Result: Holdout/Replay Implementation And Focused Tests

metadata_date: 2026-06-15
status: P69_PHASE2_HOLDOUT_REPLAY_IMPLEMENTATION_PASSED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 2 implementation is complete.  Bounded Claude review returned
`VERDICT: AGREE`; one residual-risk patch was applied and rechecked.

The implementation exposes post-fit holdout and replay diagnostics for the
P59/P67 Zhao--Cui SIR fixed-HMC adaptation path without passing diagnostic
points to `FixedTTFitter.fit`, without changing P67 thresholds, and without
rerunning the adjacent ladder.

## Skeptical Plan Audit

Passed before implementation checks.

- Baseline/comparator: P68 behavior plus the Phase 1 design contract.
- Wrong-baseline risk: old P60 low/high closeness is not used as a promotion
  criterion.
- Proxy-promotion risk: finite holdout/replay residuals are diagnostic only,
  not filtering correctness or convergence.
- Hidden-route-change risk: diagnostic batches reuse the fitted frame and shift
  and are evaluated after the TT fit; they are not appended to the fit sample
  batch.
- Environment risk: checks were CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Material defect found and fixed: the P67 budget diagnostic logic was still
  treating the fitter-internal absent holdout as a budget blocker.  Phase 2 now
  records that old field as `fitter_internal_holdout_unavailable_steps` and
  uses the new post-fit holdout/replay record for the reviewed blocker status.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the code expose reviewed post-fit holdout/replay diagnostics without changing fixed-branch fitting, row thresholds, or ladder execution? |
| Baseline/comparator | P68 manifest behavior and Phase 1 design contract. |
| Primary criterion | Satisfied locally: Task 0 passed; focused compile and pytest checks pass; P59 manifests expose `holdout_replay_diagnostics_by_step`; P67 budget diagnostics distinguish finite, missing, nonfinite, route-mismatch, and branch-drift states. |
| Veto diagnostics | No threshold changes; no ladder rerun; no GPU/HMC command; no diagnostic points passed to `FixedTTFitter.fit`; no adaptive source-faithful claim. |
| Explanatory diagnostics | Fit residuals, condition summaries, post-fit holdout/replay residuals, point/target/weight hashes, frame hash, and branch hashes. |
| Not concluded | No adjacent-ladder stability, no rank-channel activity conclusion, no degree-instability diagnosis, no d18 correctness, no d50/d100 scaling, no HMC readiness. |

## Task 0 Feasibility Checkpoint

Task 0 passed and is recorded in:

`docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-task0-diagnostic-cloud-feasibility-2026-06-15.md`

The implemented rule is a separate deterministic diagnostic batch:

- use the same source-route push/resampling ingredients as the fitted branch;
- reuse the fitted coordinate frame and fitted shift constant;
- use separate recorded diagnostic seeds/rules;
- evaluate the shifted square-root target on the diagnostic batch;
- evaluate the already fitted square-root TT after fitting;
- record diagnostic hashes and branch identity before and after evaluation.

## Implementation Summary

- Added P69 status constants in
  `bayesfilter/highdim/source_route.py:149`.
- Added source-route diagnostic batch construction in
  `bayesfilter/highdim/source_route.py:2491`.
- Wired step 1 and step 2 P59 assembly to build holdout/replay diagnostic
  batches and expose `holdout_replay_diagnostics_by_step` in
  `bayesfilter/highdim/source_route.py:2808` and
  `bayesfilter/highdim/source_route.py:3027`.
- Extended fixed TTSIRT transport construction to return fit-quality and
  post-fit holdout/replay diagnostics in
  `bayesfilter/highdim/source_route.py:3184`.
- Added post-fit residual, hash, route-match, finite-value, and branch-identity
  diagnostics in `bayesfilter/highdim/source_route.py:3306`.
- Patched aggregate missing-channel semantics so a completely unsupplied
  diagnostic channel reports missing rather than route mismatch; this was a
  residual risk from Claude review and is covered by a focused test.
- Updated P67 budget diagnostics to use the new post-fit holdout/replay channel
  while preserving old fitter-internal holdout absence as explanatory metadata
  in `scripts/p67_author_sir_adjacent_ladder_diagnostics.py:242`.
- Exported P69 statuses through `bayesfilter.highdim`.
- Added focused P59/P67 tests in
  `tests/highdim/test_p59_author_sir_step_spec_assembly.py:19` and
  `tests/highdim/test_p59_author_sir_step_spec_assembly.py:219`.

## Focused Test Coverage

The required Phase 2 cases are covered by:

- finite holdout diagnostics:
  `test_p67_budget_diagnostics_accept_finite_holdout_and_replay`;
- finite replay diagnostics:
  `test_p67_budget_diagnostics_accept_finite_holdout_and_replay`;
- missing holdout diagnostics:
  `test_p67_budget_diagnostics_distinguish_missing_holdout`;
- missing replay diagnostics:
  `test_p67_budget_diagnostics_distinguish_missing_replay`;
- nonfinite holdout diagnostics:
  `test_p67_budget_diagnostics_distinguish_nonfinite_holdout`;
- nonfinite replay diagnostics:
  `test_p67_budget_diagnostics_distinguish_nonfinite_replay`;
- branch identity drift:
  `test_p67_budget_diagnostics_treat_branch_identity_drift_as_veto`;
- route mismatch:
  `test_p67_budget_diagnostics_treat_route_mismatch_as_veto`;
- aggregate missing-channel semantics:
  `test_p69_aggregate_status_treats_unsupplied_channel_as_missing`;
- real P59 manifest exposure and branch-hash invariance:
  `test_p59_9b_assembles_two_author_sir_36d_step_specs`.

## Checks Run

CPU-only compile check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

Result: passed.

Targeted pytest:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

Result after Claude residual-risk patch: `23 passed, 2 warnings in 329.62s
(0:05:29)`.

Warnings: TensorFlow Probability deprecation warnings about `distutils`
version classes.  No test failures.

Focused residual-risk check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_p69_aggregate_status_treats_unsupplied_channel_as_missing
```

Result: `1 passed, 2 warnings in 2.72s`.

Text checks:

```bash
rg -n "post_fit_diagnostic_only|BLOCK_BRANCH_IDENTITY_DRIFT|diagnostic_only_unless_predeclared|fixed_hmc_adaptation" bayesfilter/highdim/source_route.py scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim
rg -n "log_marginal_abs_delta|normalizer_increment_abs_delta|probe_log_density_median_abs_delta|retained_log_density_median_abs_delta" scripts/p67_author_sir_adjacent_ladder_diagnostics.py
```

Result: required terms and unchanged P67 threshold definitions are present.

## Source-Governance Classification

Classification: `fixed_hmc_adaptation`.

This phase preserves the author's source-route ingredients as the local
fixed-variant target, but the new holdout/replay diagnostics are a local
post-fit diagnostic adaptation.  They are not claimed to be an adaptive
Zhao--Cui source-faithful algorithm.

Local source anchors preserved:

- author push/resample/frame route:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:46-70`;
- author sample split context:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:95-98`;
- author TTSIRT/normalizer route:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:116-124`;
- author weighted frame construction:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47`.

## Nonclaims

- No adjacent-ladder stability has been established.
- No d18 correctness claim has been established.
- No degree-ladder structural diagnosis has been established.
- No d50/d100 scaling claim has been established.
- No HMC readiness or production-readiness claim has been established.
- No adaptive Zhao--Cui parity claim has been established.

## Next-Phase Handoff

Phase 3 may proceed.  Claude returned `VERDICT: AGREE` for this Phase 2 result
and the bounded implementation/test evidence; the accepted residual-risk patch
was rechecked locally.

Phase 3 must rerun the adjacent ladder under the refreshed subplan without
changing thresholds and with the new holdout/replay diagnostics treated as
veto/explanatory diagnostics under the predeclared contract.
