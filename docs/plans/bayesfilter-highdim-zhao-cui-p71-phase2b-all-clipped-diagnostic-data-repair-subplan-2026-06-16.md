# P71 Phase 2b Subplan: All-Clipped Diagnostic Data Repair

metadata_date: 2026-06-16
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 2b

## Phase Objective

Repair the Phase 2 execution-only blocker
`diagnostic_data_all_local_entries_clipped` without changing the Zhao-Cui
source route, P70 thresholds, rank/degree choices, seeds, or validation claim
boundaries.

The repair must make all-clipped holdout/replay diagnostic data observable and
nonfatal for the execution-only ladder when the diagnostic channel is not a
Phase 2 promotion criterion.  It must not silently treat all-clipped diagnostics
as valid holdout/replay evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed source-anchor/current-evidence reset.
- Phase 1 passed condition-veto diagnostic capture and Claude review.
- Phase 2 direct execution-only reproduction failed before manifest creation.
- Focused P59 execution-only pytest failed on the same
  `diagnostic_data_all_local_entries_clipped` blocker.
- No d18 accuracy, rank convergence, scaling, or HMC claim has been made.

## Required Artifacts

- Phase 2b result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2b-all-clipped-diagnostic-data-repair-result-2026-06-16.md`.
- Focused code/test patch limited to diagnostic-data handling.
- Updated P71 visible execution ledger.
- Refreshed Phase 2 handoff if the rerun command or evidence contract changes.

## Required Checks/Tests/Reviews

Before code edits, inspect:

```bash
rg -n "diagnostic_data_all_local_entries_clipped|holdout_replay_diagnostics|P69_HOLDOUT_REPLAY|p59_author_sir_validation_ladder" bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py
```

After code edits, run CPU-only focused checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_validation_ladder.py
git diff --check -- bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2b-all-clipped-diagnostic-data-repair-subplan-2026-06-16.md
```

Claude read-only review is required before rerunning Phase 2 execution-only
reproduction if implementation code changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can all-clipped post-fit diagnostic data be represented without crashing the execution-only ladder or pretending the diagnostic is valid? |
| Baseline/comparator | Phase 2 blocker: step-1 holdout/replay diagnostic data raised `diagnostic_data_all_local_entries_clipped` before the execution-only result could be built. |
| Primary criterion | Focused tests show all-clipped diagnostic data is recorded as unavailable/nonfinite/route-mismatch diagnostic metadata while execution-only result construction can continue with explicit nonclaims. |
| Veto diagnostics | Treating all-clipped diagnostics as valid holdout/replay evidence; changing source-route model semantics; changing thresholds/seeds/ranks/degrees/ridge/sweeps; hiding the diagnostic failure; promoting execution-only evidence to accuracy/rank/scaling/HMC claims. |
| Explanatory diagnostics | `local_clip_fraction`, `local_max_abs_before_clip`, diagnostic construction label, coordinate frame hash, holdout/replay availability status, and branch identity stability. |
| Not concluded | No d18 accuracy, no holdout/replay validation, no same-route rank convergence, no d50/d100 scaling, no HMC readiness. |
| Artifact | Phase 2b result note plus focused test output. |

## Proposed Repair Shape

Preferred narrow repair:

- Replace the raw `ValueError("diagnostic_data_all_local_entries_clipped")`
  abort in the post-fit diagnostic-data builder with a structured diagnostic
  result that marks the holdout/replay channel unavailable for validation.
- Preserve `local_clip_fraction = 1.0`, `local_max_abs_before_clip`, source
  seeds, diagnostic construction label, coordinate frame hash, and a clear
  status such as `diagnostic_data_all_local_entries_clipped`.
- Ensure `_p69_post_fit_holdout_replay_diagnostics` reports the channel as not
  available or route-mismatched, so later phases cannot use it as validation
  evidence.
- Allow Phase 2 execution-only result construction to continue only because
  Phase 2's primary criterion is execution-only finite values/ESS/branch hashes
  and explicit nonclaims, not holdout/replay validation.

Acceptable alternate repair if the preferred shape is too invasive:

- Catch the all-clipped diagnostic-data exception in
  `p59_author_sir_step_spec_assembly` and omit the affected diagnostic channel
  with structured missing-diagnostic metadata.  This is acceptable only if the
  manifest explicitly records that holdout/replay diagnostics are unavailable
  and not validation evidence.

## Forbidden Claims/Actions

- Do not change the SIR model, observations, source-route density callbacks, or
  transport target.
- Do not change P70 thresholds, row/rank/degree/sweep/ridge/initializer
  settings, or seeds after seeing the failure.
- Do not call clipped diagnostic data a valid holdout/replay diagnostic.
- Do not run d18 accuracy, rank convergence, d50/d100, GPU, or HMC commands.
- Do not proceed to Phase 3 until Phase 2 rerun passes its reviewed gate.

## Exact Next-Phase Handoff Conditions

Phase 2 may be rerun only if Phase 2b produces:

- focused tests passing for structured all-clipped diagnostic handling;
- local compile/diff checks passing;
- Claude `VERDICT: AGREE` for the implementation gate;
- an updated ledger that preserves the Phase 2 execution-only evidence
  contract and nonclaims.

## Stop Conditions

Stop and write a blocker if:

- all-clipped diagnostic data cannot be represented without changing source
  route semantics;
- the only available repair would silently validate clipped diagnostics;
- focused tests cannot distinguish unavailable diagnostics from valid
  holdout/replay diagnostics;
- Claude and Codex do not converge after five material review rounds.

