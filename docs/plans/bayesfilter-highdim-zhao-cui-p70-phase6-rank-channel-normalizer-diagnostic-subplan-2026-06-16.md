# P70 Phase 6 Subplan: Bounded Rank-Channel And Normalizer Diagnostic Rerun

metadata_date: 2026-06-16
status: READY_PENDING_USER_APPROVAL_FOR_EXACT_DIAGNOSTIC_COMMAND
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run a bounded repaired diagnostic that exercises the Phase 5 fixed fitting
machinery on the same diagnostic question as P69 Phase 5c: whether declared
rank channels now activate and whether normalizer, holdout, replay, and
condition diagnostics remain bounded under predeclared gates.

Phase 6 must not run a validation ladder, d18 correctness run, GPU/HMC command,
or broad sweep.  It is a bounded diagnostic, not a promotion phase.

## Entry Conditions Inherited From Phase 5

Phase 6 may begin only after Phase 5 produces:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-result-2026-06-16.md`;
- focused test evidence for seeded-channel initialization, canonical schedule
  validation, row adequacy, channel activity, and policy payloads;
- refreshed Phase 6 subplan;
- Claude `VERDICT: AGREE` for Phase 5;
- explicit user approval to run the Phase 6 diagnostic.

The runbook's executable diagnostic approval gate remains binding.  Phase 5
test success alone does not authorize a repaired diagnostic command.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-result-2026-06-16.md`.
- Diagnostic JSON artifact under `docs/plans/` with a P70 Phase 6 filename.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.
- Refreshed Phase 7 subplan only if Phase 6 lower gates pass.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the Phase 5 repaired fixed fitting machinery activate declared rank channels and keep normalizer/holdout/replay/condition diagnostics bounded on the bounded diagnostic rows? |
| Baseline/comparator | P69 Phase 5c result and its current constant-path one-sweep diagnosis. |
| Primary pass criterion | For every executed repaired diagnostic row: row adequacy is not hard-failed; the fitter returns `HighDimStatus.OK`; extra declared channels pass the Phase 4 activity predicate; normalizer predicates pass; holdout and replay diagnostics exist, are finite, are disjoint from fit rows, and have normalized residuals at most 10; no condition-number veto. |
| Veto diagnostics | Any hard row-adequacy failure; nonfinite target or fit output; `rank_channel_activity_failed`; defensive-only or nonfinite normalizer; normalized holdout/replay residual above 10; branch identity drift; condition-number veto; missing diagnostic row identity; threshold mismatch from Phase 4/5. |
| Explanatory diagnostics | Fit residual, per-channel scores, basis-channel norms, raw holdout/replay residuals, target-value scale summaries, weighted ESS, condition warnings, below-preferred row status. |
| Not concluded | No d18 correctness, no rank/degree promotion, no scaling, no HMC readiness, no adaptive Zhao--Cui parity, no author-code failure claim. |
| Artifact preserving result | Phase 6 result and diagnostic JSON artifact, with the exact approved command, run manifest, primary criterion status, veto status, explanatory diagnostics, and nonclaims. |

## Required Checks/Reviews Before Execution

Before running any diagnostic command:

```bash
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-result-2026-06-16.md
rg -n "PHASE5|24 passed|fixed_hmc_seeded_channel_paths_v1|canonical" docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-result-2026-06-16.md
rg -n "p70_fixed_hmc_seeded_channel_fit_v1|rank_channel_activity_failed|branch_fit_row_adequacy_failed|fixed_hmc_seeded_channel_paths_v1" bayesfilter/highdim/source_route.py
rg -n "canonical_repeated_axis|legacy_permutation|malformed_repeated" tests/highdim/test_fixed_branch_fit.py
```

Then restate this evidence contract in chat and ask for explicit user approval
for the exact diagnostic command.  Do not run the command before approval.

Claude review:

- Review the Phase 6 subplan before any diagnostic run.
- Check that thresholds match Phase 4/5.
- Check that the primary pass criterion does not use in-sample residual as a
  promotion criterion.
- Check that Phase 6 cannot authorize Phase 7 unless lower gates pass.

## Candidate Diagnostic Scope

The initial diagnostic should be the smallest command that compares the P69
Phase 5c baseline question under the repaired P70 code.  The command must be
filled in only after inspecting the current diagnostic script surface and
confirming whether the existing P69 script can be adapted safely or a new P70
script is required.

The P69 Phase 5c script was inspected and should not be run directly for Phase
6 because its metadata, output path, evidence contract, and result schema are
P69-specific.  Phase 6 therefore uses a P70 wrapper that reuses the bounded P69
four-row reconstruction mechanics but writes a P70 Phase 6 artifact and applies
the predeclared P70 gate assessment.

Prepared command, pending explicit user approval:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6_rank_channel_normalizer_diagnostic.py
```

Prepared diagnostic artifact path:

`docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostics-2026-06-16.json`

Wrapper preparation checks already run before approval:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p70_phase6_diagnostic_script.py
git diff --check -- scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-stop-handoff-2026-06-16.md
```

Check results:

- compileall passed;
- focused wrapper pytest: `5 passed, 2 warnings in 3.11s`;
- `git diff --check` passed.

The approved diagnostic scope is terminal:

- one exact approved command is run once and then execution stops for
  assessment;
- if the command fails for infrastructure-only reasons before producing a
  diagnostic artifact, at most one identical rerun may be requested from the
  user with the same command and the infrastructure failure recorded;
- if any scientific or engineering veto trips, Phase 6 records the failure and
  returns to planning; it must not retune thresholds, change rows, change rank
  or degree, run a second diagnostic variant, or promote explanatory metrics
  under the same approval;
- if the diagnostic passes, Phase 6 still stops after writing the result; any
  Phase 7 ladder requires a new reviewed subplan and explicit user approval.

The Phase 6 result artifact is mandatory after any attempted diagnostic run
and must record:

- exact command actually run;
- CPU/GPU status and environment choice;
- git state summary;
- random seeds or `N/A`;
- diagnostic JSON artifact path;
- primary criterion status row by row;
- every veto diagnostic and whether it passed, failed, or was not applicable;
- explanatory diagnostics without using them as promotion criteria;
- nonclaims listed in this subplan;
- next justified action.

Forbidden at this phase:

- no broad rank/degree ladder;
- no GPU/HMC command;
- no d18 validation launch;
- no threshold change after observing repaired output;
- no low/high branch closeness gate;
- no source-faithful claim for the seeded initializer or UKF-guided branch.

## Exact Next-Phase Handoff Conditions

Phase 7 may start only if Phase 6 produces:

- reviewed Phase 6 result;
- diagnostic JSON artifact;
- every primary lower gate passes or a blocker result explains failure;
- no threshold changes after observing output;
- refreshed Phase 7 subplan with a new evidence contract;
- Claude `VERDICT: AGREE`;
- explicit user approval for Phase 7 if a ladder run is proposed.

If Phase 6 fails a lower gate, Phase 7 remains blocked.

## Stop Conditions

Stop and write a blocker if:

- user approval for the diagnostic command is absent;
- no bounded command can be stated without broad script rewrites;
- the diagnostic script would silently change thresholds or route semantics;
- row/holdout/replay identities cannot be preserved;
- Phase 6 would require GPU/HMC or validation-ladder execution;
- Claude and Codex do not converge after five material review rounds.

## Skeptical Plan Audit

The main Phase 6 risk is treating a better fit residual or nonzero channel
score as validation.  The primary gate therefore requires structural activity
and bounded normalizer/holdout/replay/condition diagnostics together.  Fit
residual remains explanatory only.
