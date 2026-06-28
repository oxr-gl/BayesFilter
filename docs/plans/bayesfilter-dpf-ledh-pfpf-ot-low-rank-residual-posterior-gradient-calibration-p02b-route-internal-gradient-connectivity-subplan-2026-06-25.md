# P02B Route-Internal Gradient Connectivity Subplan

Date: 2026-06-25

Status: `REVISED_FOR_CLAUDE_R2_REVIEW`

## Phase Objective

P02B is a repair-loop diagnostic after P02A localized the failing low-rank
candidate to a likelihood/final-particle gradient-connectivity problem.  It
does not repair the algorithm and does not advance to P03.  It tests where the
gradient path from `theta` first becomes disconnected or nonfinite inside one
low-rank route execution.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Which internal low-rank route tensor first loses connected finite gradient to `theta` on the P02 failing probes, and was the P02A disconnected readout a tape-pattern artifact? |
| Candidate/mechanism under test | Locked P02 low-rank candidate `r16_eps0p25_alpha1em08_it120` on `lgssm_small_exact_ref`, commit `01213338c7037c468f38b01d013e4ce13526c9e4`, with P02 settings `num_particles=1024`, `time_steps=12`, `dtype=float32`, TF32 enabled, XLA enabled, low-rank route only, `rank=16`, `assignment_epsilon=0.25`, `alpha=1.0e-8`, `max_projection_iterations=120`, `particle_chunk_size=64`. |
| Expected failure mode | Either the P02A diagnostic used an invalid tape pattern, or the route loses gradient through LEDH flow, corrected log weights, low-rank projection factors, transported particles, or carried uniform log weights. |
| Promotion criterion | A trusted GPU/XLA JSON/Markdown artifact classifies same-tape and P02A-style separated-tape gradients to `theta` as connected/disconnected and finite/nonfinite for required probes `91003:center` and `91002:qr_plus`, and records component/block-sensitive gradients for the required internal tensors. |
| Promotion veto | Missing trusted GPU/XLA provenance, corrupt artifact, missing required probes, missing A/B tape control, missing component/block-sensitive gradient checks, or failing to distinguish diagnostic-tape artifact from route-internal disconnection. |
| Continuation veto | Artifact cannot be produced after one focused harness repair, TensorFlow GPU/XLA cannot run, or the diagnostic itself changes the route computation relative to P02/P02A. |
| Repair trigger | First disconnected/nonfinite internal tensor identifies a narrow candidate operation for a future repair plan. |
| Explanatory diagnostics | Route values, route outputs, factor validity, Dykstra projection residuals, projection iterations, floor-hit/min-denominator summaries if available, and device/provenance. |
| Must not conclude | No threshold calibration, P03 handoff, posterior correctness, HMC readiness, default readiness, statistical superiority, source-faithfulness claim, or scientific validity. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is the P02/P02A gradient failure caused by the P02A separated-tape diagnostic or by a specific low-rank route-internal operation? |
| Exact baseline/comparator | P02 result note: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02-reproduction-determinism-result-2026-06-24.md`; P02 raw JSON/Markdown: `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.json` and `.md` with stale internal phase/title metadata quarantined by the P02 result note; P02A result note: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-result-2026-06-25.md`; P02A JSON/Markdown: `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.json` and `.md`; git commit `01213338c7037c468f38b01d013e4ce13526c9e4`. |
| Primary pass/fail criterion | A focused trusted GPU/XLA artifact records A/B tape-control outcomes plus component/block-sensitive connected/finite gradients to `theta` for one same-tape route execution at key internal tensors. |
| Veto diagnostics | Missing trusted GPU output, missing XLA/TF32/provenance, missing required probes, missing A/B tape-control readout, non-identical route settings, route output nonfinite before gradient tests, artifact fields too coarse to localize the first break, or missing next-step/final checkpoints needed for H5. |
| Explanatory diagnostics | Intermediate scalar values, component/block gradient summaries, selected scalar-entry gradient vectors, factor/particle validity, factor residuals, row/column residuals, projection iterations, and route output devices. |
| What will not be concluded | P02B cannot certify a repair.  Even if it localizes the issue, P02A and full P02 must rerun after any patch. |
| Artifact | `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-route-internal-gradient-connectivity-2026-06-25.json` plus Markdown/log and result note. |

## Hypotheses

| ID | Hypothesis | Diagnostic discriminator |
| --- | --- | --- |
| H1 | P02A tape artifact: nested separated tapes caused false disconnection. | In the same diagnostic harness, same seed/probe/settings, the P02A-style separated-tape readout reproduces disconnected likelihood/final-particle gradients while the same-tape route execution reports connected finite likelihood/final-particle gradients. |
| H2 | LEDH flow/log-weight layer emits nonfinite gradients before low-rank resampling. | `post_flow`, `pre_flow_log_density`, `forward_log_det`, `corrected_log_weights`, or `incremental` is disconnected/nonfinite before `low_rank_transport`. |
| H3 | Low-rank Dykstra projection backward pass is unstable. | Gradients are connected/finite through `normalized_log_weights` and `post_flow`, but first become nonfinite at `q_factor`, `r_factor`, `g_weights`, or projection residual diagnostics. |
| H4 | Low-rank particle centering/scaling stop-gradient or landmark kernel weakens/severs factor gradients. | Gradients are connected to `post_flow` but disconnected/nonfinite for `scaled_x`, assignment kernels, or selected landmark/factor outputs. |
| H5 | Uniform log-weight reset removes the carried likelihood path across time. | Current-step gradients are connected through factors/particles, but required post-resampling `resampled_log_weights`, next-step `pre_flow`, next-step corrected/incremental log weights, or final likelihood/final particles lose connectivity after uniform log-weight reset. |

## Planned Diagnostic Shape

Create a new focused script:

`docs/benchmarks/benchmark_low_rank_ledh_route_internal_gradient_connectivity.py`

The script must:

- reuse P02/P02A fixture builders and probe definitions;
- run the locked low-rank route settings;
- use one `tf.GradientTape(persistent=True)` per probe and one same-tape route
  execution;
- include an A/B control in the same script/harness:
  - A: same-tape route execution with internal tensors watched and measured;
  - B: P02A-style separated-tape readout on the same seed/probe/settings,
    preserving the P02A readout pattern closely enough to reproduce or falsify
    the prior `LOW_RANK_LIKELIHOOD_GRADIENT_DISCONNECTED` observation;
  - compare A/B connectedness and finite-gradient status for `value`,
    `log_likelihood`, and final particles;
- expose per-step or selected-step tensors without changing the route math;
- record for each named tensor:
  - scalar/vector value summary;
  - whole-tensor `reduce_sum` gradient connectedness/finite status;
  - selected scalar-entry gradients, including first, middle, and last finite
    entries when the tensor has more than one element;
  - per-block reduction gradients for vector/matrix/particle tensors, with at
    least leading, middle, and trailing blocks;
  - finite masks and component counts for tensor values and gradients;
  - gradient vector when small;
- include at least these probes by default:
  - `91003:center`;
  - `91002:qr_plus`;
- support a CPU-hidden tiny smoke mode for tests, clearly labeled
  `cpu_hidden_debug_only`.

Minimum tensor checkpoints:

- `scaled_Q`, `scaled_R`;
- `pre_flow`;
- `post_flow`;
- `pre_flow_log_density`;
- `forward_log_det`;
- `transition_log_density`;
- `observation_log_density`;
- `corrected_log_weights`;
- `normalized_weights`;
- `incremental_log_likelihood`;
- `normalized_log_weights`;
- `scaled_x`;
- `eps_q`, `eps_r`, `eps_g`;
- `q_factor`, `r_factor`, `g_weights`;
- `transported_particles`;
- `resampled_log_weights`;
- next-step `pre_flow`;
- next-step `corrected_log_weights`;
- next-step `incremental_log_likelihood`;
- final particles;
- final `log_likelihood`.

For H5, next-step and final likelihood checkpoints are mandatory.  If they
cannot be captured without changing route math, P02B must write
`P02B_BLOCKED_H5_UNDECIDABLE` instead of passing.

## Skeptical Plan Audit

| Check | Status |
| --- | --- |
| Wrong baseline | Guarded: exact P02/P02A result notes, raw artifacts, commit, failing probes, fixture, and candidate settings are pinned above. |
| Proxy metrics as promotion criteria | Guarded: residuals and timings are explanatory only; promotion is localization of gradient connectivity. |
| Missing stop conditions | Guarded: stop after artifact; no P03 or repair unless a later reviewed plan authorizes it. |
| Unfair comparison | Guarded: same seed/probe, route settings, dtype, TF32, XLA, device, fixture, and same-harness A/B tape-control readouts are required. |
| Hidden assumptions | Guarded: P02 raw phase metadata is quarantined; P02B is a diagnostic, not a repair. |
| Stale context | Guarded: plan references the P02A Claude-converged stop state. |
| Environment mismatch | Guarded: CPU smoke is harness-only; trusted GPU/XLA artifact with trust basis `owner_designated_managed_session_visible_gpu_trusted`, TF32/XLA/device metadata, and visible GPU provenance is required for the route failure question. |
| Artifact mismatch | Guarded: output filenames and result note are P02B-specific; raw artifact records phase `LOW_RANK_ROUTE_INTERNAL_GRADIENT_CONNECTIVITY`; missing A/B or component/block fields veto the artifact. |

Audit result: `PASS_AFTER_R1_REVISIONS_FOR_PLAN_REVIEW`.  Execution begins only
after Claude read-only review converges or a human explicitly overrides review.

## Commands

Local harness checks after implementation:

```bash
python -m py_compile docs/benchmarks/benchmark_low_rank_ledh_route_internal_gradient_connectivity.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_route_internal_gradient_connectivity.py -q
```

Trusted GPU/XLA diagnostic command after review and local checks:

```bash
python docs/benchmarks/benchmark_low_rank_ledh_route_internal_gradient_connectivity.py \
  --case-id lgssm_small_exact_ref \
  --seed-probes 91003:center,91002:qr_plus \
  --num-particles 1024 \
  --time-steps 12 \
  --low-rank-rank 16 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-alpha 1.0e-8 \
  --low-rank-max-projection-iterations 120 \
  --particle-chunk-size 64 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-route-internal-gradient-connectivity-2026-06-25.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-route-internal-gradient-connectivity-2026-06-25.md \
  --quiet
```

Stdout/stderr:
`docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02b-route-internal-gradient-connectivity-gpu.log`

## Stop/Handoff

Stop after the P02B artifact and result review.  If the diagnostic localizes a
confirmed first break, write a result note and propose the smallest future
repair.  Do not patch the low-rank solver in P02B unless the plan is explicitly
revised and reviewed.
