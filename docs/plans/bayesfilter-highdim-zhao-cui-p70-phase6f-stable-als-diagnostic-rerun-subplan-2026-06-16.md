# P70 Phase 6f Subplan: Stable ALS Diagnostic Rerun Gate

metadata_date: 2026-06-16
status: LOCAL_CHECKS_PASSED_CLAUDE_AGREE_PENDING_USER_APPROVAL_FOR_EXACT_COMMAND
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6f
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Freeze the exact post-Phase-6e repaired diagnostic rerun contract and command.
Phase 6f exists because Phase 6e changed the fixed-core ALS solve, but did not
run the P70 repaired diagnostic.  Phase 6f may prepare and review the rerun
gate; it must not execute the diagnostic command until the user explicitly
approves the exact command in this subplan.

The diagnostic question is still the original Phase 6 lower gate: does the
repaired fixed branch activate declared rank channels and keep normalizer,
holdout, replay, and condition diagnostics bounded on the bounded P70 rows?

## Entry Conditions Inherited From Phase 6e

Phase 6f may begin only after:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-result-2026-06-16.md`
  has status
  `PHASE6E_IMPLEMENTED_LOCAL_CHECKS_PASSED_CLAUDE_AGREE_PHASE7_BLOCKED`;
- Phase 6e local checks passed:
  `42 passed, 2 warnings` for the focused fixed-fit and P70 wrapper tests;
- Claude returned `VERDICT: AGREE` on the Phase 6e implementation/result;
- no repaired Phase 6 diagnostic has been run after the stable ALS repair;
- Phase 7 remains blocked.

## Required Artifacts

If Phase 6f reaches only planning/review:

- Phase 6f subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-subplan-2026-06-16.md`;
- updated visible execution ledger;
- updated Claude review ledger;
- updated stop handoff.

If the exact diagnostic command is later explicitly approved and run:

- Phase 6f result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-result-2026-06-16.md`;
- diagnostic JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-2026-06-16.json`;
- updated visible execution ledger;
- updated Claude review ledger;
- updated stop handoff.

The Phase 6f JSON path is intentionally fresh.  It must not overwrite the
original failed Phase 6 artifact:

`docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostics-2026-06-16.json`.

## Exact Diagnostic Command Pending User Approval

Prepared command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6_rank_channel_normalizer_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-2026-06-16.json
```

Do not run this command until the user explicitly approves this exact command.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After the Phase 6e stable ALS repair, does the bounded P70 repaired diagnostic complete and pass the lower structural gates for rank-channel activity, normalizer boundedness, holdout/replay boundedness, and condition diagnostics? |
| Baseline/comparator | Original Phase 6 run, which failed on `rank_candidate_1_2_fit36` with `CONDITION_NUMBER_VETO`; Phase 6c root-cause evidence; Phase 6e stable ALS implementation. |
| Primary pass criterion | The exact command exits `0`; the JSON status is `P70_PHASE6_DIAGNOSTIC_COMPLETED`; `gate_summary.overall_status` is `pass`; every executed row has a `pass` row gate; no captured failed fit is present; no step gate reports condition-number veto, rank-channel failure, hard row-adequacy failure, nonfinite/defensive-only normalizer, holdout/replay missingness, branch-identity drift, or normalized holdout/replay residual above the frozen threshold. |
| Veto diagnostics | Nonzero exit status; missing JSON; JSON status not completed; `gate_summary.overall_status != pass`; captured failed fit; any non-OK fixed fit; condition-number veto; hard row-adequacy failure; `rank_channel_activity_failed`; nonfinite target or fit output; defensive-only or nonfinite normalizer; normalized holdout/replay residual above `10`; missing/disjointness-failing holdout/replay diagnostics; threshold drift from Phase 4/5/6e; output path overwrites the original Phase 6 JSON; any Phase 7 launch. |
| Explanatory diagnostics | Fit residuals, channel scores, basis-channel norms, raw holdout/replay residuals, target-scale summaries, condition warnings, scale-spread diagnostics, unscaled normal-condition diagnostics, weighted ESS, below-preferred row status. |
| Not concluded | No d18 correctness, no rank/degree promotion, no scaling, no HMC readiness, no adaptive Zhao--Cui parity, no source-faithfulness closure, no author-code failure claim. |
| Artifact preserving result | Phase 6f result note and fresh Phase 6f diagnostic JSON if the command is later approved and run. |

## Required Local Checks Before Asking For Approval

Run these checks while drafting/reviewing the Phase 6f gate.  These checks do
not execute the diagnostic command.

```bash
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-result-2026-06-16.md
rg -n "PHASE6E_IMPLEMENTED_LOCAL_CHECKS_PASSED_CLAUDE_AGREE|42 passed|sqrt|fixed_hmc_adaptation" docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-result-2026-06-16.md
rg -n "_solve_scaled_augmented_ridge|scaled_augmented_condition_number|unscaled_normal_condition_veto|objective_preserving_column_scaling" bayesfilter/highdim/fitting.py
rg -n -e "--output|P70_PHASE6_DIAGNOSTIC_ABORTED_ON_FAILED_FIT|p70_phase6_gate_summary|DEFAULT_OUTPUT" scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p70_phase6_diagnostic_script.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-claude-review-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-stop-handoff-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-gated-execution-runbook-2026-06-16.md
```

## Claude Review Requirements

Before asking the user for approval to run the diagnostic, Claude must review
this subplan as read-only reviewer.  Claude must check:

- the exact command and fresh output path;
- that Phase 6f does not overwrite the original Phase 6 failed artifact;
- that Phase 6e unit-test evidence is not treated as diagnostic success;
- that the primary pass criterion is row-gate based, not fit-residual based;
- that threshold values remain frozen;
- that Phase 7 remains blocked unless a later Phase 6f result passes and is
  separately reviewed.

Claude cannot authorize execution.  Only the user may approve the exact
diagnostic command.

Claude review result:

- Claude returned `VERDICT: AGREE`.
- Claude found the baseline correct: original Phase 6 failure, Phase 6c
  diagnosis, and Phase 6e repair.
- Claude found the primary criteria structural and not proxy metrics.
- Claude found the fresh Phase 6f JSON path protects the original failed Phase
  6 artifact.
- Claude found Phase 7 remains blocked and no source-faithfulness or
  validation claim is implied.
- Minor caution from Claude: keep threshold drift anchored to current
  script/wrapper semantics at execution time.

## Execution Rules If User Later Approves

If the user approves the exact command, run it once visibly in this session.
Then:

1. If the command exits nonzero because a scientific or engineering veto trips,
   write the Phase 6f result as a blocker and stop.  Do not rerun, retune, or
   change rows.
2. If the command exits zero but `gate_summary.overall_status != pass`, write
   the Phase 6f result as a lower-gate failure and stop.
3. If the command exits zero and every primary gate passes, write the Phase 6f
   result and send it to Claude for read-only review.  Phase 7 is still not
   launched; the next safe step would be drafting a Phase 7 subplan and asking
   for explicit approval.
4. If the command fails before producing any JSON because of an infrastructure
   interruption, record the infrastructure failure and ask the user before any
   identical rerun.

## Forbidden Claims/Actions

- Do not run the exact diagnostic command before explicit user approval.
- Do not run the default-output command for Phase 6f, because it would risk
  overwriting the original Phase 6 artifact.
- Do not run the P69 diagnostic script directly.
- Do not run a broad rank/degree ladder.
- Do not run GPU/HMC, d18 validation, or PDF/document builds.
- Do not change thresholds after seeing output.
- Do not use low/high branch closeness as a gate.
- Do not claim the fixed variant works unless the Phase 6f lower gate passes
  and the result is reviewed.
- Do not claim source-faithfulness for the stable ALS repair.
- Do not proceed to Phase 7 in this phase.

## Exact Next-Phase Handoff Conditions

Phase 6f planning may close and ask for user approval only after:

- local checks pass or failures are recorded;
- Claude returns `VERDICT: AGREE` on this subplan, or a blocker is written;
- the visible execution ledger and stop handoff are refreshed;
- the exact command and fresh output path are stated to the user.

If the user later approves and the diagnostic passes, Phase 6f result review
may authorize drafting a Phase 7 subplan.  It does not authorize running a
Phase 7 ladder.

If the diagnostic fails or is not approved, Phase 7 remains blocked.

## Stop Conditions

Stop and write a blocker if:

- Claude finds a material flaw and five repair-review rounds do not converge;
- the wrapper cannot write to a fresh output path without code changes;
- local checks show the wrapper gate semantics are stale;
- the proposed command would overwrite the original Phase 6 artifact;
- a threshold is missing or would need to be set after seeing output;
- the diagnostic would require GPU/HMC, validation, or ladder execution.

## Skeptical Plan Audit

The main risks are wrong baseline and proxy promotion.  The baseline is the
original Phase 6 condition-veto failure plus Phase 6e's stable ALS
implementation, not the Phase 6e unit tests alone.  Fit residuals, condition
warnings, and scale-spread diagnostics are explanatory.  The primary gate is
the predeclared row-gate status in the diagnostic JSON.  The plan also uses a
fresh Phase 6f JSON path so the original failed Phase 6 artifact remains
auditable.
