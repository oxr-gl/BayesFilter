# P8j Phase 5d Result: LEDH OT Larger-Count Feasibility

metadata_date: 2026-06-17
status: BLOCKED_RUNTIME_AND_MC_SE
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 5d
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Do not run `N=128` under the current Phase 5d budget.  The `N=64` adaptive LEDH OT one-rung probe is finite and transport-valid, but MC SE remains high and runtime projects poorly. |
| Primary criterion status | Failed for larger-count feasibility.  The probe did not show MC-SE improvement and did not justify an adjacent `N=128` rung. |
| Veto diagnostic status | No nonfinite transport, no untrusted GPU, no model/data/default change, no `N=8`, no leaderboard or gradient/HMC claim.  Runtime projection is the active stop condition. |
| Main uncertainty | Whether a different variance-reduction or resampling design would lower MC SE enough; particle count scaling alone is not supported by this probe. |
| Next justified action | Draft/review Phase 5e as a decision gate: preserve SIR DPF cells as blocked, request human direction for a variance-reduction program, or explicitly narrow the leaderboard scope. |
| What is not concluded | No selected SIR d18 DPF count, no leaderboard completion, no DPF gradient correctness, no HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity, no production readiness. |

## Required Checks

Pre-run checks:

```bash
python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8j or sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-result-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-subplan-2026-06-17.md
```

Results:

- `py_compile`: passed;
- focused P8j/SIR tests: `11 passed, 32 deselected, 2 warnings`;
- `git diff --check`: passed.

Post-run checks:

- Phase 5d JSON parse: passed;
- `py_compile`: passed;
- focused P8j/SIR tests: `11 passed, 32 deselected, 2 warnings`;
- `git diff --check`: passed.

## Runtime Audit

Phase 5c adaptive LEDH OT runtimes:

| N | Runtime seconds | MC SE |
| --- | --- | --- |
| 16 | `217.711056` | `38.680160007903105` |
| 32 | `395.196029` | `41.269063039967556` |

The reviewed Phase 5d subplan permitted `N=64,128` only if runtime projection
was acceptable.  Because `N=32` was already about `395` seconds and MC SE did
not improve, Phase 5d ran a one-rung `N=64` runtime/MC-SE probe before any
`N=128` adjacent rung.

## Trusted GPU Diagnostic

Command:

```bash
MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8j-sir-particle-tuning-stage0 --row sir --algorithms ledh_pfpf_alg1_ukf_current --horizons 20 --particles 64 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8j-profile-manifest-phase P8J_PHASE5D_LEDH_OT_LARGER_COUNT_RUNTIME_PROBE --p8j-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-subplan-2026-06-17.md --p8j-sinkhorn-epsilon-policy cost_mean_max_nominal --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-2026-06-17.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-2026-06-17.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-selected-blocked-2026-06-17.csv
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-2026-06-17.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-selected-blocked-2026-06-17.csv`

## Result Summary

Status:

- `executed_p8j_sir_particle_tuning_stage0_with_blockers`

Rung:

| N | Finite | Transport | Trusted GPU | MC SE | Mean log likelihood | Runtime seconds |
| --- | --- | --- | --- | --- | --- | --- |
| 64 | true | true | true | `39.529955624675594` | `-1898.1430440058189` | `789.755664` |

Transport diagnostics at first resampling event:

| Nominal epsilon | Effective epsilon | Cost mean | Cost max | Row residual |
| --- | --- | --- | --- | --- |
| `1.0` | `124.06696001363679` | `124.06696001363679` | `348.85224874280505` | `4.440892098500626e-16` |

Selected/blocker record:

| Algorithm | Selected count | Blocker |
| --- | --- | --- |
| `ledh_pfpf_alg1_ukf_current` | none | `BLOCK_P8J_SIR_PARTICLE_TUNING_MISSING_NEXT_RUNG` |

Interpretation:

- The adaptive Sinkhorn repair remains numerically effective at `N=64`.
- MC SE remains roughly flat relative to `N=16,32`, not approaching the
  approximate `4.7` to `4.9` threshold.
- `N=64` took `789.755664` seconds.  A five-seed `N=128` adjacent rung is not
  justified under the current `1800` second budget because runtime would likely
  dominate and MC SE trend does not support simple particle-count scaling.
- The selected/blocker CSV reports `MISSING_NEXT_RUNG` because only one rung
  was intentionally run.  The scientific/engineering blocker is the combined
  runtime and MC-SE trend.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `94069066a70df6f1f0f2b53d32b9d452bd67f891` |
| Dirty state | Large pre-existing dirty/untracked worktree; unrelated work preserved. |
| Environment | TensorFlow/TensorFlow Probability P8j SIR tuning harness with explicit adaptive Sinkhorn policy. |
| CPU/GPU status | Local tests intentionally CPU-hidden; GPU diagnostic ran trusted/escalated and TensorFlow used `/device:GPU:0`. |
| Seeds | `81120,81121,81122,81123,81124` |
| Candidate counts | `64` only, by reviewed one-rung runtime-probe branch. |
| Runtime budget | `1800` seconds |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-result-2026-06-17.md` |

## Post-Run Red Team

Strongest alternative explanation:

- The high MC SE may be driven by estimator variance, resampling frequency, or
  model/weight degeneracy rather than a particle count too small by a modest
  factor.

What would overturn the blocker:

- A reviewed variance-reduction or alternative resampling plan showing lower
  MC SE at feasible runtime, or an explicit human decision to accept a narrower
  non-DPF leaderboard scope.

Weakest part of the evidence:

- `N=128` was not run.  The decision not to run it is based on runtime
  projection plus weak MC-SE trend, not direct `N=128` measurement.

## Handoff

Do not proceed to Phase 6.  Phase 5e should be a decision gate, not an
automatic larger-count ladder.
