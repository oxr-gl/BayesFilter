# P8j Phase 5c Result: Scale-Adaptive Sinkhorn Repair Gate

metadata_date: 2026-06-17
status: PARTIAL_PASS_EXECUTION_REPAIR_MC_SE_BLOCKED
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 5c
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | The explicit scale-adaptive Sinkhorn repair fixed the LEDH OT nonfinite transport blocker for `N=16,32` five-seed full SIR d18 trajectories, but no LEDH particle count was selected because MC SE remains far above the gate. |
| Primary criterion status | Partial pass.  Finite/trusted-GPU/transport-valid full trajectories were produced, but particle adequacy failed MC SE and the `N=16,32` ladder is blocked. |
| Veto diagnostic status | No SIR model/data mutation; repair is opt-in; no `N=8`; trusted GPU evidence; no leaderboard, gradient/HMC, or source-faithfulness claim. |
| Main uncertainty | Whether larger LEDH OT particle counts reduce MC SE enough, and whether runtime remains acceptable. |
| Next justified action | Draft/review Phase 5d for a larger-count LEDH OT scale-adaptive ladder and preserve bootstrap MC-SE blocker unless a separate higher-count plan is approved. |
| What is not concluded | No selected SIR d18 particle count, no leaderboard completion, no DPF gradient correctness, no HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity, no production readiness. |

## Implementation Patch

Implemented an explicit opt-in Sinkhorn epsilon policy:

- `sinkhorn_epsilon_policy="fixed"` remains the default;
- `sinkhorn_epsilon_policy="cost_mean_max_nominal"` sets the effective epsilon
  at each Sinkhorn OT event to `max(nominal_epsilon, pairwise_cost_mean)`;
- diagnostics record nominal epsilon, effective epsilon, cost scale, residuals,
  and the repair classification;
- the P8j tuning CLI accepts `--p8j-sinkhorn-epsilon-policy`;
- the normal fixed-epsilon path is unchanged unless the policy is explicitly
  requested.

Files touched for this phase:

- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`

## Checks Run

Pre-implementation checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8j or sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-result-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-subplan-2026-06-17.md
```

Results:

- `10 passed, 32 deselected, 2 warnings`;
- `git diff --check`: passed.

Implementation checks:

```bash
python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8j or sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-subplan-2026-06-17.md
```

Results:

- `py_compile`: passed;
- focused P8j/SIR tests: `11 passed, 32 deselected, 2 warnings`;
- `git diff --check`: passed.

Post-run checks:

- Phase 5c JSON parse: passed;
- focused P8j/SIR tests: `11 passed, 32 deselected, 2 warnings`;
- `py_compile`: passed;
- `git diff --check`: passed.

## Trusted GPU Diagnostic

Command:

```bash
MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8j-sir-particle-tuning-stage0 --row sir --algorithms ledh_pfpf_alg1_ukf_current --horizons 20 --particles 16,32 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8j-profile-manifest-phase P8J_PHASE5C_SCALE_ADAPTIVE_SINKHORN_REPAIR --p8j-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-subplan-2026-06-17.md --p8j-sinkhorn-epsilon-policy cost_mean_max_nominal --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-ledh-ot-2026-06-17.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-ledh-ot-2026-06-17.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-ledh-ot-selected-blocked-2026-06-17.csv
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-ledh-ot-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-ledh-ot-2026-06-17.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-ledh-ot-selected-blocked-2026-06-17.csv`

The first attempt failed before numerical execution because
`_p8j_sir_profile_dpf_prefix()` was missing the new policy parameter.  This was
patched and rechecked before the trusted GPU retry.

## Result Summary

Status:

- `executed_p8j_sir_particle_tuning_stage0_with_blockers`

Selected/blocker record:

| Algorithm | Selected count | Blocker |
| --- | --- | --- |
| `ledh_pfpf_alg1_ukf_current` | none | `BLOCK_P8J_SIR_PARTICLE_TUNING_MC_SE` |

Rungs:

| N | Finite | Transport | Trusted GPU | MC SE | Mean log likelihood | Runtime seconds |
| --- | --- | --- | --- | --- | --- | --- |
| 16 | true | true | true | `38.680160007903105` | `-1950.047451072786` | `217.711056` |
| 32 | true | true | true | `41.269063039967556` | `-1937.4458233804648` | `395.196029` |

MC SE threshold:

- `max(2.0, 0.0025 * abs(mean_log_likelihood))`, about `4.88`;
- both rungs exceed this threshold by a wide margin.

First-event transport diagnostics:

| N | Nominal epsilon | Effective epsilon | Cost mean | Cost max | Row residual |
| --- | --- | --- | --- | --- | --- |
| 16 | `1.0` | `116.56402657134574` | `116.56402657134574` | `237.97475859459587` | `2.220446049250313e-16` |
| 32 | `1.0` | `114.54449395149925` | `114.54449395149925` | `249.7021917558023` | `3.3306690738754696e-16` |

Interpretation:

- The scale-adaptive policy repairs the Sinkhorn row-residual nonfinite blocker
  observed in Phase 5 for the tested LEDH OT rungs.
- The repair does not make `N=16` or `N=32` adequate particle counts.
- Runtime increased materially because full trajectories now execute all
  resampling events.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `94069066a70df6f1f0f2b53d32b9d452bd67f891` |
| Dirty state | Large pre-existing dirty/untracked worktree; unrelated work preserved. |
| Environment | TensorFlow/TensorFlow Probability P8j SIR tuning harness with explicit adaptive Sinkhorn policy. |
| CPU/GPU status | Local tests intentionally CPU-hidden; GPU diagnostic ran trusted/escalated and TensorFlow used `/device:GPU:0`. |
| Seeds | `81120,81121,81122,81123,81124` |
| Candidate counts | `16,32` |
| Runtime budget | `1800` seconds |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-result-2026-06-17.md` |

## Post-Run Red Team

Strongest alternative explanation:

- Scale-adaptive epsilon may be a numerically stable but overly diffuse OT
  relaxation; finite transport does not prove statistical efficiency.
- MC SE remains high and may require much larger counts, a different resampling
  threshold, or a separate variance-reduction plan.

What would overturn the current blocker:

- A reviewed larger-count adaptive LEDH OT ladder that passes finite,
  transport, trusted-GPU, MC SE, runtime, and adjacent-rung gates.

Weakest part of the evidence:

- Only `N=16,32` were tested under the adaptive policy; those counts are
  sufficient to show execution repair but not particle adequacy.

## Handoff

Do not proceed to Phase 6.  Phase 5d should focus on larger-count LEDH OT
adaptive tuning and runtime/variance feasibility, or preserve a blocker if the
cost is too high.
