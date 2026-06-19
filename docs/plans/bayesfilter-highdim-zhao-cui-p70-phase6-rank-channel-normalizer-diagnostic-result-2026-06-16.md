# P70 Phase 6 Result: Bounded Rank-Channel And Normalizer Diagnostic

metadata_date: 2026-06-16
status: PHASE6_BLOCKED_CONDITION_NUMBER_VETO_FIRST_ROW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6
executor: Codex
reviewer: pending Claude read-only review

## Decision

The exact user-approved Phase 6 command was run once:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6_rank_channel_normalizer_diagnostic.py
```

The diagnostic did not complete the first row.  It failed during the first
bounded repaired row, `rank_candidate_1_2_fit36`, because the repaired fixed
fit returned `HighDimStatus.CONDITION_NUMBER_VETO`.  The source-route helper
therefore raised:

```text
ValueError: fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO
```

Under the Phase 6 terminal rule, this is a scientific/engineering veto, not an
infrastructure-only interruption.  No identical rerun was attempted, and no
threshold, row, rank, degree, sweep, ridge, or initializer change was made
after observing the output.

Phase 7 remains blocked.  The next justified action is a narrow blocker-repair
phase that preserves condition-number diagnostics before raising and audits
why the first repaired row is ill-conditioned.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the Phase 5 repaired fixed fitting machinery activate declared rank channels and keep normalizer/holdout/replay/condition diagnostics bounded on the bounded diagnostic rows? |
| Baseline/comparator | P69 Phase 5c constant-path one-sweep diagnosis. |
| Primary criterion | Failed before row completion: the first row did not return `HighDimStatus.OK`; it hit `CONDITION_NUMBER_VETO`. |
| Veto diagnostics | Condition-number veto triggered on the first repaired diagnostic row. |
| Explanatory diagnostics | The wrapper wrote only the run-start JSON artifact before the exception; no fitted row payload was available. |
| Not concluded | No rank-channel activation result, no normalizer result, no holdout/replay result, no d18 correctness, no rank/degree promotion, no scaling, no HMC readiness, no adaptive Zhao--Cui parity, no author-code failure claim, and no claim that the original bug is fixed. |
| Artifact preserving result | This result note and the partial JSON run-start artifact below. |

## Run Manifest

| Field | Value |
| --- | --- |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6_rank_channel_normalizer_diagnostic.py` |
| Exit status | `1` |
| CPU/GPU status | CPU-only intended with `CUDA_VISIBLE_DEVICES=-1`; TensorFlow emitted CUDA plugin/cuInit messages despite CPU hiding. |
| Git HEAD | `5fdd0819ce0eb2994fb0509e66d9e9cce5f2d47c` |
| Dirty worktree | yes, many unrelated and P70 runbook artifacts present |
| Random seeds | model simulation `5901`; step-1 holdout/replay seeds `7301/7401` and `7311/7501`; step-2 holdout/replay process seeds `7402` and `7502` |
| JSON artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostics-2026-06-16.json` |
| JSON status | `P70_PHASE6_DIAGNOSTIC_RUNNING`, partial run-start artifact only |

## Observed Failure

The command entered the first row:

```text
rank_candidate_1_2_fit36, degree=1, rank=2, fit_sample_count=36
```

The failure occurred in the repaired fixed-TTSIRT source-route helper:

```text
_p59_fixed_ttsirt_transport_from_values
  raise ValueError(f"fixed_ttsirt_fit_status_{fit_result.status.value}")
ValueError: fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO
```

The relevant Phase 5/P70 settings were:

- seeded-channel initialization: `fixed_hmc_seeded_channel_paths_v1`;
- canonical repeated sweep;
- `max_sweeps=4`;
- ridge `1e-10`;
- condition warning `1e10`;
- condition veto `1e14`.

Because the helper raises immediately on non-OK fit status, the current
diagnostic artifact does not expose the actual per-core condition-number
records for the failed fit.  That is now the immediate blocker: we need a
diagnostic-safe way to preserve the failed `FixedTTFitter` status records
before the source-route helper raises.

## Decision Table

| Item | Status |
| --- | --- |
| Primary criterion | Failed: first row did not return `HighDimStatus.OK`. |
| Veto diagnostic status | Failed by condition-number veto. |
| Main uncertainty | The per-core condition numbers and design-matrix shape records are not preserved in the failed-row JSON because the helper raises before returning fit diagnostics. |
| Next justified action | Phase 6b condition-veto capture and repair-planning phase. |
| What is not concluded | No evidence yet on rank-channel activation, normalizer boundedness, holdout/replay boundedness, validation, scaling, HMC readiness, or correctness of the repaired fixed variant. |

## Stop-Rule Compliance

The Phase 6 terminal rule was followed:

- the exact approved command was run once;
- the command failed with an engineering veto, not an infrastructure-only
  interruption;
- no rerun was attempted;
- no threshold, row, rank, degree, ridge, sweep, or initializer was changed;
- no second diagnostic variant was launched under the same approval.

## Next Handoff

Draft and review Phase 6b:

`P70 Phase 6b: Condition-Veto Capture And Repair Planning`

Phase 6b should be narrow.  It may patch the diagnostic path so a
condition-number-veto fit returns or records fit diagnostics before raising,
and it may run fast synthetic/local tests for that behavior.  It must not run
another repaired four-row diagnostic until a reviewed subplan and explicit
user approval authorize an exact command.
