# P8j Phase 3 Result: Algorithm 1 UKF LEDH SIR Smoke

metadata_date: 2026-06-17
status: PASS_PENDING_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Local Phase 3 gate passed; await Claude review before Phase 4. |
| Primary criterion status | Passed locally.  Focused SIR DPF tests passed and one-seed N=4 no-OT Algorithm 1 UKF LEDH smoke is finite. |
| Veto diagnostic status | No local veto fired.  Result is explicitly no-OT, one-seed/N=4 smoke only. |
| Main uncertainty | Claude has not yet reviewed the Phase 3 result or Phase 4 subplan.  No OT evidence exists yet. |
| Next justified action | Claude review of Phase 3 result and Phase 4 OT-resampled SIR smoke subplan. |
| What is not concluded | No OT-resampled LEDH-PFPF-OT SIR evidence, no five-seed value, no particle-count tuning, no leaderboard refresh, no score/Hessian/theta-gradient/HMC/NUTS readiness. |

## Checks Run

Focused SIR DPF tests:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf"
```

Result:

- `3 passed, 32 deselected, 2 warnings`

Diff check:

```bash
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-subplan-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md
```

Result:

- passed

## Smoke Artifact

Command: one-seed N=4 no-OT Algorithm 1 UKF LEDH smoke via
`_dpf_single_run(..., resampling_route="none")`, deliberate CPU-only with
`CUDA_VISIBLE_DEVICES=-1`.

Artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-2026-06-17.json`

Summary:

| Field | Value |
| --- | --- |
| Status | `executed_one_seed_ledh_alg1_sir_smoke` |
| Row | `zhao_cui_spatial_sir_austria_j9_T20` |
| Algorithm | `ledh_pfpf_alg1_ukf_current` |
| Resampling route | `none` |
| Particle count | `4` |
| Seed | `81120` |
| Log likelihood | `-1870.5584816857702` |
| Average log likelihood | `-93.52792408428851` |
| Minimum ESS | `1.0` |
| Mean ESS | `1.01222212562663` |
| Resampling count | `0` |

Route identifiers:

- `method_generation`: `li_coates_algorithm1_ukf_covariance_lifecycle`;
- `flow_source_route`: `li_coates_2017_algorithm1_ledh_pfpf`;
- `resampling_route`: `none`;
- `previous_ledh_pfpf_ot_evidence_status`: `quarantined`.

Smoke nonclaims:

- one-seed N=4 no-OT LEDH smoke only;
- not OT-resampled LEDH-PFPF-OT evidence;
- not five-seed DPF value evidence;
- not particle-count adequacy;
- not leaderboard completion;
- not score, Hessian, theta-gradient, HMC, or NUTS evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Recorded by later release artifacts; current worktree is dirty. |
| Dirty state | Repository had substantial pre-existing dirty/untracked work outside P8j. |
| Commands | Focused pytest, `git diff --check`, one-seed no-OT LEDH smoke. |
| Environment | TensorFlow/TensorFlow Probability, deliberate CPU-only. |
| CPU/GPU status | `CUDA_VISIBLE_DEVICES=-1`; TensorFlow emitted CUDA initialization warnings but GPU was intentionally hidden. |
| Data version | Current local P8 source-scope/adapter matrix and SIR synthetic dataset generator. |
| Seeds | Smoke seed `81120`. |
| Output artifacts | This result and the Phase 3 smoke JSON. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-result-2026-06-17.md` |

## Handoff

Phase 4 may not execute until Claude reviews this Phase 3 result and the Phase
4 OT-resampled LEDH-PFPF-OT SIR smoke subplan.  A finite Phase 3 smoke does not
establish the OT route, tuning, leaderboard, or gradient/HMC readiness.
