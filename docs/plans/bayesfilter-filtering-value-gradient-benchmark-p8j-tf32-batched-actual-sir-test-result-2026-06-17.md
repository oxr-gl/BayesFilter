# P8j TF32 Batched Actual-SIR Test Result

metadata_date: 2026-06-17
status: PASS_ENGINEERING_FEASIBILITY_NOT_PARTICLE_ADEQUACY
plan: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-test-plan-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | The TF32/GPU batched streaming path is useful for actual SIR d18 engineering feasibility. |
| Primary criterion status | Passed.  The trusted GPU actual-SIR `B=5,T=20,D=18,M=9,N=64` probe was finite, ran on GPU with TF32 enabled, used the nonlinear prior-mean hook, and cleared the 5x runtime gate. |
| Veto diagnostic status | No active veto for the engineering feasibility gate.  Existing linear-path tests still pass; SIR semantics are recorded; no leaderboard, MC-SE, HMC, or source-faithfulness claim is made. |
| Main uncertainty | The probe is an experimental streaming adapter with fixed process covariance and graph-compatible SIR transition copy; it is not scalar Algorithm 1 UKF covariance-lifecycle parity and does not solve the MC-SE particle adequacy blocker. |
| Next justified action | Draft/review a follow-on batched SIR particle-tuning feasibility ladder, with explicit parity/route decision before promotion into the P8j leaderboard lane. |
| What is not concluded | No selected SIR d18 particle count, no leaderboard completion, no MC-SE adequacy, no exact likelihood correctness, no DPF gradient correctness, no HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity, no production/default readiness. |

## Claude Review

Plan review converged in two rounds:

- Round 1: `VERDICT: REVISE`
  - required dedicated nonlinear-prior tests;
  - required actual-SIR semantics artifact fields;
  - required unambiguous timing envelope.
- Round 2: `VERDICT: AGREE`
  - confirmed the repaired plan fixed the material blockers.

Review artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-test-claude-review-round-01-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-test-claude-review-round-02-2026-06-17.md`

## Implementation

Patched the experimental batched streaming path with an opt-in nonlinear prior
mean hook:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`

Added focused coverage:

- `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py`

Added standalone actual-SIR probe:

- `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`

The existing linear/LGSSM path remains the default when no prior-mean callback
is supplied.

## Checks Run

Plan-required local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py -q -k "nonlinear_prior_mean"
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf"
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
```

Results:

- `py_compile`: passed;
- nonlinear-prior tests: `2 passed, 8 deselected`;
- SIR DPF route tests: `3 passed, 40 deselected, 2 warnings`;
- `git diff --check`: passed.

Trusted GPU preflight:

```bash
nvidia-smi
```

Result: trusted context saw NVIDIA GeForce RTX 4080 SUPER with CUDA available.

## Actual-SIR Probe

Command:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 64 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-probe-2026-06-17.md
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-probe-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-probe-2026-06-17.md`

Summary:

| Field | Value |
| --- | --- |
| Shape | `B=5,T=20,D=18,M=9,N=64` |
| Seeds | `81120,81121,81122,81123,81124` |
| Device | `/job:localhost/replica:0/task:0/device:GPU:0` |
| Precision | `float32`, TF32 enabled |
| Finite output | `true` |
| Compile plus first call | `13.474980568978935s` |
| Warm-call timings | `0.1629901621490717s`, `0.1688134572468698s` |
| Mean warm-call time | `0.16590180969797075s` |
| Scalar comparator | P8j Phase 5d scalar actual-SIR adaptive LEDH OT `N=64` five-seed trusted-GPU runtime `789.755664s` |
| Speedup vs scalar comparator | `4760.380043097625x` |

The probe JSON records:

- `actual_sir_callbacks_used: true`;
- callback usage limited to initial particles, covariances, observations, and
  route metadata;
- graph-compatible SIR transition copy used inside XLA because the model
  validation path uses eager `.numpy()` checks;
- nonlinear prior-mean hook used;
- no scalar Algorithm 1 UKF covariance-lifecycle parity claim.

## Interpretation

The batched TF32/GPU path removes the dominant scalar runtime blocker for this
feasibility probe.  It is now reasonable to plan a reviewed batched SIR
particle-tuning feasibility ladder.

However, this result does not resolve the earlier P8j MC-SE blocker.  It also
does not establish equivalence to the scalar Li-Coates Algorithm 1 UKF
covariance lifecycle.  The new adapter is an experimental streaming
LEDH-PFPF-OT SIR route with fixed process covariance and graph-compatible SIR
transition copy.

## Post-Run Red Team

Strongest alternative explanation:

- The speedup may partly come from route differences, especially fixed process
  covariance and the experimental streaming flow, not merely batching/TF32.

What would overturn the engineering conclusion:

- A route-parity test showing the batched adapter no longer tracks the intended
  SIR transition/observation target, or a larger tuning ladder showing runtime
  no longer scales usefully at needed particle counts.

Weakest part of the evidence:

- This was one `N=64` feasibility rung, not an adjacent-rung MC-SE or
  leaderboard tuning ladder.

## Handoff

Next work should create a reviewed follow-on subplan for a batched actual-SIR
particle-tuning feasibility ladder.  That subplan must decide whether route
parity to scalar Algorithm 1 UKF covariance lifecycle is required before any
leaderboard promotion, or whether the experimental streaming adapter remains a
separate repair candidate.
