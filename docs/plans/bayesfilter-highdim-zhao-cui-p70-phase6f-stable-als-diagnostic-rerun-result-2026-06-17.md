# P70 Phase 6f Result: Stable ALS Diagnostic Rerun

metadata_date: 2026-06-17
status: PHASE6F_BLOCKED_LOWER_GATE_FAILURE_AND_RANK3_CONDITION_VETO_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-subplan-2026-06-16.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

The exact user-approved Phase 6f command was run once:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6_rank_channel_normalizer_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-2026-06-16.json
```

The command exited with status `1`.  The fresh Phase 6f JSON was written:

`docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-2026-06-16.json`.

The Phase 6f lower gate did not pass.  Phase 7 remains blocked.

## Main Result

The Phase 6e stable ALS repair removed the row-1 condition veto on this
specific rerun: the first row, `rank_candidate_1_2_fit36`, completed both time
steps with `fit_status=OK`, channel activity `ok`, row adequacy `ok`, and no
condition veto.  This is not a general stability claim, because the run still
failed and the second row hit a scaled augmented condition veto.  The first row
also failed the lower gate because holdout and replay residuals are far above
the predeclared normalized residual threshold.

The run then entered the second row, `rank_stronger_1_3_fit36`, and aborted
with a captured failed fit:

```text
fit_status: CONDITION_NUMBER_VETO
termination_reason: scaled_augmented_condition_number_veto
stop_condition_triggered: CONDITION_NUMBER_VETO
```

The failed second-row fit reached a scaled augmented condition number of about
`2.986e14`, above the frozen condition-number veto `1e14`.

## Row-Gate Summary

| Row | Diagnostic status | Gate result | Main reason |
| --- | --- | --- | --- |
| `rank_candidate_1_2_fit36` | completed | fail | Holdout/replay normalized residuals fail by many orders of magnitude. |
| `rank_stronger_1_3_fit36` | aborted | fail | Captured failed fit with scaled augmented condition-number veto. |
| `degree_candidate_1_2_fit24` | not reached | N/A | Terminal rule stopped after second-row failed fit. |
| `degree_stronger_2_2_fit24` | not reached | N/A | Terminal rule stopped after second-row failed fit. |

The JSON gate summary reports:

- `status`: `P70_PHASE6_DIAGNOSTIC_ABORTED_ON_FAILED_FIT`;
- `gate_summary.overall_status`: `fail`;
- `gate_summary.failed_label`: `rank_stronger_1_3_fit36`;
- `gate_summary.exit_status`: `1`;
- `continued_after_failed_row`: `false`.

## Important Interpretation Notes

Two reporting/gate-schema issues were discovered while inspecting the JSON.
They are not the reason the run failed, and they do not make the diagnostic
pass.  The authoritative saved row payload plus a recomputed gate still fails
decisively by holdout/replay normalized residual veto.  The schema issues only
affect how the failed first-row gate reasons should be read.

1. The saved row payload contains finite holdout/replay residuals, but the
   stored gate summary serialized them as `raw_residual: null` and labeled
   them `*_residual_nonfinite`.  Recomputing the gate from the saved JSON gives
   finite residuals but still fails the normalized residual veto.

2. The normalizer payload uses `sqrt_square_normalizer`, while the gate expects
   `sqrt_tt_normalizer`.  The saved first-row normalizers are finite and large:
   step 1 `sqrt_square_normalizer = 1.285e25`; step 2
   `sqrt_square_normalizer = 3.478e30`.  Therefore the stored
   `missing_sqrt_tt_normalizer` reason is a schema mismatch, not evidence of
   defensive-only normalizer collapse.

The genuine first-row lower-gate failure is holdout/replay instability, not
condition-number failure and not defensive-only normalizer collapse.

## First-Row Details

For `rank_candidate_1_2_fit36`:

- step 1 fit residual: `0.007559528132877981`;
- step 2 fit residual: `0.008141842755077238`;
- step 1 condition max: `5.561259975501979e6`;
- step 2 condition max: `1.056048043304995e6`;
- no condition warning or veto was reported for either step.

Recomputed from the saved JSON:

| Step | Target RMS | Holdout residual | Holdout normalized | Replay residual | Replay normalized |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `0.31221508319781655` | `1.985986193810201e10` | `6.36095531794631e10` | `7.338111173012788e10` | `2.350338458300373e11` |
| 2 | `0.29094386307700393` | `4.290990987942154e10` | `1.474851864054084e11` | `1.6554131788275293e11` | `5.689802703930525e11` |

The frozen normalized residual veto is `10.0`.

## Second-Row Details

For `rank_stronger_1_3_fit36`:

- fit rank: `3`;
- fit degree: `1`;
- target dimension: `36`;
- ridge: `1e-08`;
- max sweeps: `4`;
- initialization: `fixed_hmc_seeded_channel_paths_v1`;
- condition gate target: `scaled_augmented_solved_system`;
- condition-number veto: `1e14`;
- accepted update records before veto: `78`;
- failing update record: core index `6`, sweep index `1`;
- failing scaled augmented condition number: `2.985651508224343e14`;
- unscaled normal condition number at the failing update: `inf`;
- column scale spread at the failing update: `67108864.0`.

The stable ALS repair therefore removed the row-1 condition veto on this
specific rerun, but it did not establish general stability and did not remove
condition fragility for the rank-3 row.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the bounded P70 diagnostic pass after Phase 6e stable ALS? |
| Baseline/comparator | Original Phase 6 condition-veto failure, Phase 6c root-cause evidence, and Phase 6e stable ALS implementation. |
| Primary criterion | Failed: command exited `1`; JSON status is aborted; `gate_summary.overall_status` is `fail`; not every row gate passed. |
| Veto diagnostics | Failed by first-row holdout/replay normalized residual veto and second-row captured condition-number veto. |
| Explanatory diagnostics | First-row fit residuals are small and conditions are bounded, but these are explanatory only.  Gate-schema issues were found for normalizer field naming and NumPy scalar residual recognition. |
| Not concluded | No fixed-variant success, no d18 correctness, no rank/degree promotion, no scaling, no HMC readiness, no adaptive Zhao--Cui parity, no source-faithfulness closure, no author-code failure claim. |
| Artifact preserving result | This result note and `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-2026-06-16.json`. |

## Run Manifest

| Field | Value |
| --- | --- |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6_rank_channel_normalizer_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-2026-06-16.json` |
| Exit status | `1` |
| Git HEAD | `94069066a70df6f1f0f2b53d32b9d452bd67f891` |
| Working tree | Dirty before and after run; unrelated pre-existing changes preserved. |
| CPU/GPU status | CPU-only intended with `CUDA_VISIBLE_DEVICES=-1`; TensorFlow emitted CUDA plugin/cuInit messages despite CPU hiding. |
| Environment | `CUDA_VISIBLE_DEVICES=-1`, `MPLCONFIGDIR=/tmp` |
| Elapsed time | `342.405` seconds in JSON run manifest. |
| Random seeds | model simulation `5901`; step-1 holdout/replay seeds `7301/7401` and `7311/7501`; step-2 holdout/replay seeds `7402` and `7502`. |
| JSON artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-2026-06-16.json` |

## Stop-Rule Compliance

- The exact approved command was run once.
- The diagnostic stopped after the captured failed second row.
- No rerun was attempted.
- No threshold, row, rank, degree, ridge, sweep, or initializer was changed
  after observing output.
- No Phase 7 command was run.

## Next Justified Action

Draft a narrow Phase 6g blocker-analysis subplan before any further
implementation or diagnostic run.  Phase 6g should:

- repair the gate-schema issues without changing thresholds:
  `sqrt_square_normalizer` versus `sqrt_tt_normalizer`, and NumPy scalar
  residual recognition before JSON serialization;
- audit why first-row fit residual is small while holdout/replay residuals are
  enormous;
- audit why the rank-3 row reaches a scaled augmented condition veto despite
  the objective-preserving stabilization;
- keep Phase 7 blocked unless a later reviewed diagnostic result passes the
  lower gate.

## Claude Review

Claude first returned `VERDICT: REVISE`, requesting two wording repairs:

- treat the gate-summary versus row-payload mismatch as a reporting/schema bug,
  not the reason the run failed;
- narrow the Phase 6e conclusion to say row-1 condition veto was removed only
  on this specific rerun, not generally fixed.

After those repairs, Claude returned `VERDICT: AGREE`.

Claude agreed that Phase 6f failed, Phase 7 remains blocked, row-1 still fails
the lower gate by holdout/replay normalized residual veto, row-2 still fails by
scaled augmented condition-number veto, and the schema issue affects reporting
rather than the scientific outcome.
