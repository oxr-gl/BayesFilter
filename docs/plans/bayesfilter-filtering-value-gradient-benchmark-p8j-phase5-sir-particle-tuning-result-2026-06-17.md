# P8j Phase 5 Result: SIR d18 Particle-Count Tuning

metadata_date: 2026-06-17
status: BLOCKED_REPAIR_REQUIRED
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 5 did not select a SIR d18 DPF particle count; Phase 6 leaderboard refresh is blocked. |
| Primary criterion status | Failed.  No requested SIR DPF cell passed five-seed finite, MC SE, adjacent-rung, runtime, trusted-GPU, and route/transport gates. |
| Veto diagnostic status | Two blockers fired: bootstrap failed MC SE at `N=16,32,64`; LEDH OT failed nonfinite/transport execution at first seed for `N=16,32,64`. |
| Main uncertainty | Whether bootstrap can pass with a higher particle ladder and whether LEDH OT needs a scale-adaptive Sinkhorn repair for SIR d18. |
| Next justified action | Draft and review a Phase 5b repair subplan. |
| What is not concluded | No particle-count adequacy, no leaderboard completion, no score/Hessian/theta-gradient/HMC/NUTS readiness, no source-faithful TT/SIRT or MATLAB parity. |

## Checks Run

Pre-implementation focused tests:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf or p8j"
```

Result:

- `7 passed, 32 deselected, 2 warnings`

After adding the P8j tuning harness:

```bash
python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf or p8j"
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Results:

- focused P8j/SIR tests: `8 passed, 32 deselected, 2 warnings`;
- full P8d numeric test file: `40 passed, 2 warnings`;
- `git diff --check`: passed.

## Trusted GPU Probe

Trusted `nvidia-smi` before tuning:

- NVIDIA-SMI `590.57`;
- driver `591.86`;
- CUDA reported by driver `13.1`;
- GPU `NVIDIA GeForce RTX 4080 SUPER`;
- memory at probe time `2845 MiB / 16376 MiB`.

Trusted TensorFlow GPU probe before tuning:

- `tf.test.is_built_with_cuda()`: true;
- physical GPUs: `["/physical_device:GPU:0"]`;
- logical GPUs: `["/device:GPU:0"]`;
- tiny matmul device: `/job:localhost/replica:0/task:0/device:GPU:0`.

## Implementation Patch

Implemented a P8j-specific tuning path in
`scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`:

- `--p8j-sir-particle-tuning-stage0`;
- `filter_bench.p8j_sir_particle_tuning.v1` JSON schema;
- SIR-only admission;
- fixed seed-list enforcement: `81120,81121,81122,81123,81124`;
- historical `N=8` rejection;
- bootstrap route variant `p8j_sir_d18_bootstrap`;
- LEDH OT route variant `p8j_sir_d18_ot_resampled_alg1`;
- structured failed-rung accounting for Sinkhorn failures.

Added focused tests in
`tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py` for:

- selected-count schema;
- trusted-GPU/five-seed/fixed-seed/`N=8` guards;
- LEDH transport blocker;
- failed profile preservation without crash;
- CSV writing.

## Tuning Command

```bash
MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8j-sir-particle-tuning-stage0 --row sir --algorithms bootstrap_dpf_current,ledh_pfpf_alg1_ukf_current --horizons 20 --particles 16,32,64 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8j-profile-manifest-phase P8J_PHASE5_SIR_PARTICLE_TUNING --p8j-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-subplan-2026-06-17.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-2026-06-17.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-2026-06-17.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-selected-blocked-2026-06-17.csv
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-2026-06-17.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-selected-blocked-2026-06-17.csv`

Run status:

- `executed_p8j_sir_particle_tuning_stage0_with_blockers`

Summary:

| Field | Value |
| --- | --- |
| Evaluated rungs | `6` |
| Selected cells | `0` |
| Blocked cells | `2` |
| All requested cells accounted | `true` |

Selected/blocker records:

| Algorithm | Selected count | Blocker |
| --- | --- | --- |
| `bootstrap_dpf_current` | none | `BLOCK_P8J_SIR_PARTICLE_TUNING_MC_SE` |
| `ledh_pfpf_alg1_ukf_current` | none | `BLOCK_P8J_SIR_PARTICLE_TUNING_NONFINITE` |

## Rung Summary

Bootstrap DPF:

| N | Finite | Trusted GPU | MC SE | Mean log likelihood | Runtime seconds |
| --- | --- | --- | --- | --- | --- |
| 16 | true | true | `12.659167675738635` | `-844.8064166047814` | `8.401567` |
| 32 | true | true | `8.798108527576609` | `-849.5775887165115` | `7.999578` |
| 64 | true | true | `7.222663617629848` | `-832.224234113714` | `7.981323` |

Bootstrap failed the MC SE gate because the threshold is
`max(2.0, 0.0025 * abs(mean_log_likelihood))`, approximately `2.08` to `2.12`
for these rungs.

LEDH OT:

| N | Finite | Trusted GPU | Transport | Failure |
| --- | --- | --- | --- | --- |
| 16 | false | false | false | `FloatingPointError: Sinkhorn row residual exceeded tolerance envelope` |
| 32 | false | false | false | `FloatingPointError: Sinkhorn row residual exceeded tolerance envelope` |
| 64 | false | false | false | `FloatingPointError: Sinkhorn row residual exceeded tolerance envelope` |

The LEDH OT failure occurred on seed `81120` for each tested count before
five-seed evidence could be accumulated.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `94069066a70df6f1f0f2b53d32b9d452bd67f891` |
| Dirty state | `387` git-status-short entries in run manifest; substantial pre-existing dirty/untracked work outside P8j remains. |
| Environment | TensorFlow/TensorFlow Probability P8j SIR particle tuning harness. |
| CPU/GPU status | Trusted/escalated GPU command; TensorFlow saw `/device:GPU:0`. |
| Seeds | `81120,81121,81122,81123,81124` |
| Candidate counts | `16,32,64`; historical `N=8` rejected by the harness. |
| Runtime budget | `1800` seconds. |
| Wall time | `43.965054` seconds. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-result-2026-06-17.md` |

## Post-Run Red Team

Strongest alternative explanation:

- Bootstrap may pass at a higher particle count, so the MC SE blocker is a
  tuning-range failure, not evidence against bootstrap DPF on SIR.
- LEDH OT may need scale-adaptive Sinkhorn settings or state normalization for
  SIR d18, so the nonfinite blocker is a solver/configuration failure, not
  evidence against the LEDH-PFPF idea.

What would overturn the blocker:

- A reviewed Phase 5b repair showing finite LEDH OT transport diagnostics on
  SIR d18 with five fixed seeds and a higher/adjacent particle ladder; or
- a reviewed bootstrap-only leaderboard scope if the user explicitly accepts
  narrowing Phase 6 to bootstrap after a higher-count bootstrap ladder passes.

Weakest part of the evidence:

- The LEDH OT rung currently stops after the first failed seed per count, so it
  preserves the first failure but does not characterize failure frequency
  across all five seeds.

## Handoff

Do not proceed to Phase 6 leaderboard refresh.  Phase 5b repair planning is the
next justified step.
