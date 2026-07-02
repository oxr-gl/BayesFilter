# Phase 3 Subplan: GPU/XLA/TF32 Route Smoke

Date: 2026-06-30

Status: `DRAFT_PENDING_PHASE2`

## Phase Objective

Run the smallest trusted GPU/XLA/TF32 SIR diagnostic that proves the material
route is available and that the Phase 2 reporting fields survive actual
TensorFlow/XLA execution.

## Entry Conditions Inherited From Previous Phase

- Phase 2 local checks passed.
- Diagnostic reporting emits the Phase 1 gate fields.
- GPU/CUDA commands will be escalated per `AGENTS.md`.

## Required Artifacts

- Phase result: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-result-2026-06-30.md`
- JSON output: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json`
- Optional progress JSON if the command supports it.
- Updated Phase 4 subplan.

## Required Checks, Tests, And Reviews

Escalated checks:

```bash
nvidia-smi
python docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py --device-scope visible --cuda-visible-devices 0 --expect-device-kind gpu --dtype float32 --tf32-mode enabled --manual-reverse-compiler xla --num-particles 16 --time-steps 1 --batch-seeds 81120,81121 --candidate-steps 10 --theta 0.02,-0.01,0.01 --base-step 0.001 --regression-offsets -3,-2,-1,0,1,2,3 --trim-extreme-values 0 --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.md
```

The transport gradient-mode string is the current value of
`core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE` and must be
rechecked in Phase 0 inventory before execution.

Earlier drafts used `benchmark_p8p_regression_fd_reparameterization.py` with
`--fd-mode ad-only`.  That remains useful as a route smoke, but it does not
emit the Phase 2 `route_prerequisites` field.  Phase 3 therefore uses the SIR
Sinkhorn diagnostic itself.

Review:

- Claude review required if the smoke result is used to advance to a material
  Phase 4 run or if the command has to be changed materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the SIR manual reverse route run under trusted GPU/XLA/TF32 and emit finite route metadata? |
| Baseline/comparator | Route metadata and finite AD-only manual reverse score, not FD agreement. |
| Primary criterion | Escalated GPU visible, tensors on GPU, TF32 enabled, compiler XLA, manual score route, finite objective/score/MCSE, and `route_prerequisites.route_prerequisite_pass == true`. |
| Veto diagnostics | CPU tensors, XLA disabled, TF32 disabled, nonfinite score, dense/full transport autodiff, missing metadata, or failed route prerequisite gate. |
| Explanatory diagnostics | Runtime, memory, per-seed MCSE, compiler warmup metadata. |
| Not concluded | No FD agreement, no material SIR gradient validation, no HMC readiness. |

## Forbidden Claims And Actions

- Do not interpret this as a gradient correctness result.
- Do not use CPU fallback as a pass.
- Do not change default TF32/GPU policy.
- Do not run a long N ladder in this phase.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- GPU/XLA/TF32 route smoke passes;
- result artifact records route metadata and nonclaims;
- Phase 4 command remains within reviewed resource bounds.

## Stop Conditions

- Escalated GPU probe fails.
- TensorFlow cannot see GPU in trusted execution.
- Manual reverse XLA route fails before material diagnostics.
- Smoke command needs environment setup or package changes.

## End-Of-Phase Close Protocol

1. Run required escalated local checks.
2. Write the Phase 3 result.
3. Refresh Phase 4 subplan.
4. Review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
