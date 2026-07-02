# Streaming Manual VJP Phase 7 Subplan: GPU Memory Ladder

status: READY_FOR_CLAUDE_REVIEW
date: 2026-06-23
phase: S7-GPU-MEMORY-LADDER

## Phase Objective

Run a trusted GPU memory and feasibility ladder for the new opt-in streaming
blockwise manual VJP route, advancing to `N=10000` only if earlier rungs pass.
S7 must produce either a valid `N=10000` actual-gradient artifact for the new
route or a blocker result that explicitly prevents S8/P82 FD advancement.

## Entry Conditions

- S6 result status is `PASSED`.
- S6 bounded Claude result review returned `VERDICT: AGREE`.
- The route under test is exactly:
  `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys`.
- The old replay route
  `manual_streaming_finite_sinkhorn_stopped_scale_keys` is not the S7 route and
  must not be used as evidence for S7 success.
- `transport_ad_mode="full"` remains forbidden.
- GPU commands may be run only with trusted/elevated permissions.
- No P82 FD comparison may run in S7.

## Required Artifacts

- S7 result or blocker result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-gpu-memory-ladder-result-2026-06-23.md`
- Trusted GPU preflight note inside the S7 result.
- Rung JSON artifacts, all under `docs/plans/`:
  - `bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n100-gpu-tf32-2026-06-23.json`
  - `bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json`
  - `bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n2500-gpu-tf32-2026-06-23.json`
  - `bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n5000-gpu-tf32-2026-06-23.json`
  - `bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json`
- N10000 progress JSON if the N10000 rung is launched:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n10000-progress-2026-06-23.json`
- Refreshed S8 handoff subplan only if S7 has a valid N10000 artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase8-p82-handoff-subplan-2026-06-23.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-execution-ledger-2026-06-23.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-claude-review-ledger-2026-06-23.md`
- Updated visible stop handoff:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-stop-handoff-2026-06-23.md`

## Required Checks/Tests/Reviews

Before execution, run a skeptical plan audit.  The audit must confirm:

- the route is the new blockwise route, not the old replay route;
- the harness CLI accepts and records the new route string;
- no Zhao-Cui comparator is used;
- no P82 FD comparison is launched;
- no `transport_ad_mode="full"` route is used;
- no CPU-only result is treated as GPU evidence;
- the commands answer S7 memory/feasibility questions, not FD consistency or
  posterior correctness.

Implementation work is limited to harness plumbing if needed:

- Add the new route string to `--transport-gradient-mode` choices in
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`.
- Extend `tests/highdim/test_p82_regression_fd_harness_protocol.py` so the CLI
  accepts the new route and `streaming_batched_ledh_pfpf_ot_value_core_tf`
  forwards the exact new route string.
- Do not change defaults: existing default remains `raw` in those harnesses.
- Do not edit `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py` in
  S7 unless a focused pre-GPU test proves the regression harness cannot execute
  the new route without that edit.  The S7 rungs execute
  `benchmark_p8p_regression_fd_reparameterization.py`; standalone
  parameterized-harness CLI exposure can be deferred to S8/P82 handoff if
  needed.

CPU-hidden pre-GPU checks:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
```

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

```text
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-gpu-memory-ladder-subplan-2026-06-23.md
```

Trusted/elevated GPU preflight:

```text
nvidia-smi
```

```text
MPLCONFIGDIR=/tmp python -c "import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices()); print(tf.config.list_physical_devices('GPU'))"
```

Trusted/elevated S7 GPU rungs use the same actual-gradient harness with
`--fd-mode ad-only`, five seeds, `--seed-microbatch-size 1`,
`--ad-evaluation-mode reverse-gradient`, and the new route.  Run rungs
sequentially and stop at the first failure.

N100 smoke rung:

```text
MPLCONFIGDIR=/tmp timeout 1200 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 100 --batch-seeds 81120,81121,81122,81123,81124 --seed-microbatch-size 1 --ad-evaluation-mode reverse-gradient --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "S7 blockwise streaming actual-gradient N100 GPU TF32" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 128 --dtype float32 --tf32-mode enabled --basis-set raw --output docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n100-gpu-tf32-2026-06-23.json
```

N1000 rung:

```text
MPLCONFIGDIR=/tmp timeout 1800 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 1000 --batch-seeds 81120,81121,81122,81123,81124 --seed-microbatch-size 1 --ad-evaluation-mode reverse-gradient --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "S7 blockwise streaming actual-gradient N1000 GPU TF32" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --output docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json
```

N2500 rung:

```text
MPLCONFIGDIR=/tmp timeout 2400 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 2500 --batch-seeds 81120,81121,81122,81123,81124 --seed-microbatch-size 1 --ad-evaluation-mode reverse-gradient --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "S7 blockwise streaming actual-gradient N2500 GPU TF32" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --output docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n2500-gpu-tf32-2026-06-23.json
```

N5000 rung:

```text
MPLCONFIGDIR=/tmp timeout 3600 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 5000 --batch-seeds 81120,81121,81122,81123,81124 --seed-microbatch-size 1 --ad-evaluation-mode reverse-gradient --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "S7 blockwise streaming actual-gradient N5000 GPU TF32" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --output docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n5000-gpu-tf32-2026-06-23.json
```

N10000 rung:

```text
MPLCONFIGDIR=/tmp timeout 7200 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120,81121,81122,81123,81124 --seed-microbatch-size 1 --ad-evaluation-mode reverse-gradient --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "S7 blockwise streaming actual-gradient N10000 GPU TF32" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --progress-output docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n10000-progress-2026-06-23.json --output docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json
```

Each rung JSON must be validated before advancing to the next rung.  Validation
is exact-path and key-based:

- `status == "pass"`;
- `primary_pass is true`;
- `device_scope == "visible"`;
- `expect_device_kind == "gpu"`;
- `output_devices` is nonempty and every entry contains `GPU`;
- `shape.num_particles` equals the rung particle count;
- `shape.batch_size == 5`;
- `shape.seed_microbatch_size == 1`;
- `shape.seed_microbatch_count == 5`;
- `batch_seeds == [81120, 81121, 81122, 81123, 81124]`;
- `transport.transport_plan_mode == "streaming"`;
- `transport.gradient_mode ==
  "manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys"`;
- `transport.transport_ad_mode == "stabilized"`;
- `transport.dense_transport_matrix_materialized is false`;
- `regression_fd.fd_mode == "ad-only"`;
- `regression_fd.ad_evaluation_mode == "reverse-gradient"`;
- `objective` is finite;
- every value in `gradient_values` is finite;
- for every entry in `monte_carlo_gradient_noise`, `standard_error_of_batch_mean`
  is finite.

If a key is missing, has a wrong value, or records nonfinite data, the rung
fails and S7 stops with a blocker result.  The S7 result must summarize these
exact validation checks for each launched rung.

After GPU rungs, write the S7 result and request bounded exact-path Claude
review of that result.  If S7 passes, refresh S8 and review it before any P82
FD command.  If S7 blocks, update the visible stop handoff and do not advance
to S8/P82.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the new blockwise streaming manual VJP route produce finite five-seed SIR d18 actual gradients through `N=10000` under trusted GPU/TF32 without the prior replay-gradient OOM route? |
| Baseline/comparator | Prior P82 old-route N10000 OOM, S6 local route checks, and smaller S7 rungs; no FD comparator in S7. |
| Primary pass criterion | The N10000 ad-only run exits 0 and writes JSON satisfying every exact JSON validation key listed in this subplan, including GPU placement, five seeds, `seed_microbatch_size=1`, `transport_plan_mode=streaming`, `gradient_mode=manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, finite objective, finite gradient components, finite seed-gradient MCSE, and `dense_transport_matrix_materialized=false`. |
| Veto diagnostics | Trusted GPU preflight fails; any rung times out, OOMs, or exits nonzero; missing JSON; GPU not visible; output tensors not on GPU; wrong route metadata; wrong particle count or seed count; nonfinite objective/gradient/MCSE; `transport_ad_mode=full`; FD comparison launched; unsupported HMC/default/posterior/scientific-superiority claim. |
| Explanatory only | Runtime, per-seed gradient contributions, seed SD/SE, device placement, TF32 metadata, chunk sizes, TensorFlow allocator warnings, progress file, and smaller-rung memory trends. |
| Not concluded | No FD agreement, no posterior correctness, no HMC/default readiness, no production readiness, no scientific superiority, no Zhao-Cui source-faithfulness. |
| Artifact | S7 result plus rung JSONs, ledgers, and stop handoff. |

## Forbidden Claims/Actions

- Do not run P82 FD comparison in S7.
- Do not change pass/fail criteria after seeing rung results.
- Do not use `transport_ad_mode="full"`.
- Do not use the old replay route as S7 success evidence.
- Do not describe CPU-only or non-trusted GPU runs as GPU evidence.
- Do not change default route, default policy, public API exposure, HMC policy,
  model/funding boundaries, or scientific criteria.
- Do not claim FD agreement, posterior correctness, HMC/default readiness,
  production readiness, scientific superiority, or Zhao-Cui source-faithfulness.

## Exact Next-Phase Handoff Conditions

Advance to S8 only if:

- S7 result passes bounded Claude exact-path review;
- the N10000 JSON exists and satisfies the primary criterion;
- S8 subplan is refreshed to hand off exactly that N10000 actual-gradient JSON
  to downstream governed FD planning;
- the visible stop handoff is updated to
  `S7_PASSED_READY_FOR_S8_SUBPLAN_REVIEW`.

If any S7 rung fails, S7 must write the same S7 result path with
`status: BLOCKED`, record the failing rung, preserve any partial artifacts, and
update the visible stop handoff with an explicit prohibition on S8/P82
advancement.

## Stop Conditions

Stop and write an S7 blocker result if:

- CPU-hidden harness plumbing checks fail and cannot be repaired within S7
  scope;
- trusted GPU preflight fails;
- any rung OOMs, times out, exits nonzero, or fails metadata/finite checks;
- output artifact is missing or records the wrong route, CPU placement, wrong
  seed count, wrong particle count, or `transport_ad_mode="full"`;
- S7 would require FD evidence, default-policy changes, or scientific-claim
  changes to pass;
- S7 result or S8 subplan fails to converge under bounded Claude review within
  five rounds for the same blocker.

## Skeptical Plan Audit

Audit result before execution: pass after this refresh.  The old S7 draft was
not acceptable because it reused the prior P82 route
`manual_streaming_finite_sinkhorn_stopped_scale_keys`, while S7 must test the
new blockwise route built and locally validated in S2-S6.  This refreshed plan
repairs that by requiring harness CLI plumbing for the new route before GPU
work, pinning the exact route string in every rung command, and making wrong
route metadata a hard veto.  The S7 commands use only
`benchmark_p8p_regression_fd_reparameterization.py`, so standalone
`benchmark_p8p_parameterized_sir_gradient.py` CLI exposure is not a required S7
target unless focused checks prove otherwise.  The plan remains S7
memory/feasibility only and does not authorize P82 FD, default-route changes,
or scientific claims.

## End-Of-Phase Protocol

1. Run required CPU-hidden harness checks.
2. Run trusted/elevated GPU preflight.
3. Run GPU rungs sequentially, stopping at the first failure.
4. Validate each JSON for route, device, finite, seed, particle, and
   transport metadata.
5. Write the S7 result or blocker.
6. Draft or refresh S8 only if S7 passes; otherwise update the stop handoff to
   block S8/P82.
7. Request bounded exact-path Claude review, repairing visibly and looping at
   most five rounds for the same blocker.
