# P69 Phase 3 Result: Adjacent Ladder Rerun With Holdout/Replay Evidence

metadata_date: 2026-06-15
status: P69_PHASE3_ADJACENT_LADDER_RERUN_PASSED_WITH_DEGREE_BLOCK
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 3 produced the required adjacent-ladder artifact.  Claude review
converged after one handoff patch.  The new P69 holdout/replay diagnostics
remove the previous diagnostic-availability ambiguity: every executed row is
interpretable under the Phase 3 veto checks.

The adjacent-ladder result remains blocked because the degree ladder exceeds
all four frozen P67 thresholds.  The rank ladder passes with zero deltas.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | With post-fit holdout/replay diagnostics available, what does the adjacent rank/degree ladder say about the fixed-HMC adaptation branch? |
| Baseline/comparator | P68 adjacent-ladder behavior without post-fit holdout/replay diagnostics. |
| Primary criterion | Satisfied as a diagnostic run: all five rows are interpretable; source invariants pass; holdout/replay diagnostics are present and finite; branch identity does not drift; thresholds are unchanged. |
| Top-level ladder status | `P67_ADJACENT_FIXED_BUDGET_SCREEN_BLOCKED`. |
| Rank ladder | `P67_ADJACENT_FIXED_BUDGET_SCREEN_PASSED`; all metric deltas are zero. |
| Degree ladder | `P67_ADJACENT_FIXED_BUDGET_SCREEN_BLOCKED`; all four frozen threshold checks fail. |
| Not concluded | No d18 correctness, no d50/d100 scaling, no HMC readiness, no adaptive Zhao--Cui parity, no theorem-level convergence result. |

## Commands And Artifacts

Pre-run checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
rg -n "log_marginal_abs_delta|normalizer_increment_abs_delta|probe_log_density_median_abs_delta|retained_log_density_median_abs_delta" scripts/p67_author_sir_adjacent_ladder_diagnostics.py
```

Result: passed.

Immediate inherited pre-run pytest evidence after Phase 2 Claude repair:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

Result: `23 passed, 2 warnings in 329.62s (0:05:29)`.

Adjacent-ladder rerun:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p67_author_sir_adjacent_ladder_diagnostics.py --output docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-diagnostics-2026-06-15.json
```

Result: completed in `1283.596` seconds with top-level status
`P67_ADJACENT_FIXED_BUDGET_SCREEN_BLOCKED`.

Output artifact:

`docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-diagnostics-2026-06-15.json`

Environment note: TensorFlow printed CUDA factory/cuInit messages even though
the run was launched with `CUDA_VISIBLE_DEVICES=-1`.  This run is recorded as
CPU-only intent in the JSON run manifest.

## Frozen Thresholds

The Phase 3 JSON records the unchanged thresholds:

| Metric | Threshold |
| --- | ---: |
| `log_marginal_abs_delta` | `5.0` |
| `normalizer_increment_abs_delta` | `5.0` |
| `probe_log_density_median_abs_delta` | `10.0` |
| `retained_log_density_median_abs_delta` | `10.0` |

## Row Veto Table

Every row has `budget_limited = false`,
`holdout_replay_resolution_status =
PASS_HOLDOUT_REPLAY_DIAGNOSTICS_AVAILABLE`, no missing fit-resolution fields,
no branch-identity drift, no route mismatch, no holdout/replay unavailable
steps, no holdout/replay nonfinite steps, and no condition warning/veto steps.

| Row | Degree | Rank | Fit samples | Status | Holdout/replay | Veto blockers |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `base_candidate_1_2_fit16` | 1 | 2 | 16 | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | available | none |
| `rank_candidate_1_2_fit36` | 1 | 2 | 36 | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | available | none |
| `rank_stronger_1_3_fit36` | 1 | 3 | 36 | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | available | none |
| `degree_candidate_1_2_fit24` | 1 | 2 | 24 | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | available | none |
| `degree_stronger_2_2_fit24` | 2 | 2 | 24 | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | available | none |

## Ladder Outcomes

Rank ladder:

- candidate row: `rank_candidate_1_2_fit36`;
- stronger row: `rank_stronger_1_3_fit36`;
- authorized difference: `fit_rank`;
- unauthorized comparison differences: none;
- status: `P67_ADJACENT_FIXED_BUDGET_SCREEN_PASSED`;
- deltas:
  - `log_marginal_abs_delta = 0.0`;
  - `normalizer_increment_abs_deltas = [0.0, 0.0]`;
  - `probe_log_density_median_abs_delta = 0.0`;
  - `retained_log_density_median_abs_delta = 0.0`.

Degree ladder:

- candidate row: `degree_candidate_1_2_fit24`;
- stronger row: `degree_stronger_2_2_fit24`;
- authorized difference: `fit_degree`;
- unauthorized comparison differences: none;
- status: `P67_ADJACENT_FIXED_BUDGET_SCREEN_BLOCKED`;
- blockers:
  - `log_marginal_delta_threshold_exceeded`;
  - `normalizer_increment_delta_threshold_exceeded`;
  - `probe_log_density_delta_threshold_exceeded`;
  - `retained_log_density_delta_threshold_exceeded`;
- deltas:
  - `log_marginal_abs_delta = 39.90354896700583`;
  - `normalizer_increment_abs_deltas = [59.54048065746218, 19.636931690456336]`;
  - `probe_log_density_median_abs_delta = 21.25481599004719`;
  - `retained_log_density_median_abs_delta = 335.22761346150156`.

## Residual Diagnostics

The residuals are finite but not promotion criteria.

| Row | Step 1 holdout/replay RMS | Step 2 holdout/replay RMS | Fit residuals |
| --- | --- | --- | --- |
| `base_candidate_1_2_fit16` | `2.7417e36 / 5.5416e36` | `2.8019e13 / 8.3370e12` | `0.03695, 0.10826` |
| `rank_candidate_1_2_fit36` | `0.99360 / 0.62014` | `0.52320 / 0.48381` | `0.09574, 0.04261` |
| `rank_stronger_1_3_fit36` | `0.99360 / 0.62014` | `0.52320 / 0.48381` | `0.09574, 0.04261` |
| `degree_candidate_1_2_fit24` | `1632.87149 / 454.63170` | `2.4530e14 / 1.0103e16` | `0.08235, 0.10991` |
| `degree_stronger_2_2_fit24` | `2.6313e18 / 4.7148e19` | `2.7613e6 / 4.1804e6` | `0.04045, 0.00242` |

Interpretation discipline:

- The rank row's identical metrics and identical post-fit residuals are
  evidence for a Phase 4 rank-channel activity diagnosis, not a convergence
  proof.
- The degree row's finite but unstable metrics are evidence for a Phase 4
  degree/basis sensitivity diagnosis, not a paper failure or d18 correctness
  verdict.

## Nonclaims

- No structural rank convergence proof.
- No d18 filtering correctness claim.
- No d50 or d100 scaling claim.
- No HMC production-readiness claim.
- No adaptive Zhao--Cui parity claim.
- No claim that whole-batch hash disjointness proves pointwise set
  disjointness.

## Next-Phase Handoff

Phase 4 may proceed after Claude R2 returned `VERDICT: AGREE`.  Phase 4 should
diagnose:

- whether the rank zero-delta result reflects inactive rank channels,
  deterministic degeneracy, or a metric-insensitive comparison;
- whether degree instability reflects basis/domain sensitivity, design
  coverage, overfitting, target scaling, or structural sensitivity of the fixed
  variant.

Phase 4 must not tune thresholds, change the route, or claim correctness.
