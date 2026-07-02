# Phase 1 Subplan: Tiny GPU/XLA Full-Route Smoke

Date: 2026-07-01

Status: `READY_FOR_PHASE0_RESULT_REVIEW`

## Phase Objective

Run the smallest trusted GPU/XLA diagnostic that exercises the corrected
manual total-derivative finite-Sinkhorn route with `transport_ad_mode="full"`.
The phase asks only whether the route compiles/runs on GPU/XLA and returns
finite value and gradient.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result passed.
- Trusted GPU probe succeeded.
- Local focused CPU float64 repair checks passed.
- The corrected target remains total derivative of the finite fixed-Sinkhorn
  scalar.
- Phase 0 static dispatch proof shows the Phase 1 selector pair reaches
  `_filterflow_manual_streaming_finite_transport_total_vjp`.

## Required Artifacts

- JSON output:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-2026-07-01.json`.
- Result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-result-2026-07-01.md`.
- Updated Phase 2 or Phase 3 subplan depending on outcome.
- Claude review ledger entry.

## Required Checks, Tests, Reviews

Candidate command, subject to Phase 0 refresh:

```bash
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode ad-only \
  --batch-seeds 81120,81121 \
  --time-steps 1 \
  --num-particles 16 \
  --theta 0.02,-0.01,0.01 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-2026-07-01.json
```

Post-run JSON gate check must verify:

- output tensors are on GPU;
- compiler mode is `xla` and `jit_compile` is true;
- transport mode records `transport_ad_mode="full"`;
- gradient mode records the manual streaming finite transport route;
- Phase 0 static dispatch proof showed that this selector pair reaches the
  total-derivative helper;
- objective and gradient are finite;
- seed MCSE is finite;
- status is pass.

Claude review:

- Review Phase 1 result read-only.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the corrected `transport_ad_mode="full"` manual route run under trusted GPU/XLA/TF32 at tiny SIR size? |
| Baseline/comparator | Same route CPU repair establishes the mathematical target; Phase 1 compares only route metadata and finite outputs, not numerical equality to CPU. |
| Primary criterion | Phase 0 dispatch proof is present; GPU tensors, XLA JIT manual-reverse unit, `transport_ad_mode="full"`, finite objective, finite gradient, finite MCSE, output artifact present. |
| Veto diagnostics | Dispatch proof absent; CPU fallback; XLA not used; route metadata not full; stopped route claimed as score; nonfinite output; missing artifact; OOM; TensorFlow/XLA unsupported op. |
| Explanatory diagnostics | Runtime, compile timing, gradient values, MCSE, GPU memory if emitted. |
| Not concluded | No material particle-count viability, no HMC readiness, no posterior correctness, no production promotion. |
| Artifact preserving result | Phase 1 JSON and result markdown. |

The current CLI gradient-mode string
`manual_streaming_finite_sinkhorn_stopped_scale_keys` is a legacy selector for
the manual finite streaming route.  For this phase, it is not the derivative
claim.  The derivative claim is valid only if the output metadata also records
`transport_ad_mode="full"` and the run uses the full total-derivative branch.
If the metadata records `transport_ad_mode="stabilized"`, the phase fails.
If Phase 0 did not prove the selector pair reaches the total-derivative helper,
the phase fails even if metadata says `full`.

## Forbidden Claims And Actions

- Do not call finite output a correctness proof for the nonlinear likelihood.
- Do not continue to the particle ladder if route metadata does not prove the
  full route ran.
- Do not relax pass/fail criteria after seeing results.
- Do not use non-escalated GPU failures as hardware conclusions.

## Exact Next-Phase Handoff Conditions

If Phase 1 passes:

- write Phase 1 result;
- draft or refresh Phase 3 particle ladder subplan;
- send Phase 1 result and Phase 3 subplan to Claude.

If Phase 1 fails because the existing harness cannot exercise the full route:

- write Phase 1 blocker result;
- activate Phase 2 harness repair subplan.

If Phase 1 fails because the corrected route is incompatible with XLA or GPU:

- write a blocker result and stop unless the failure is clearly a small harness
  issue.

## Stop Conditions

- OOM or repeated XLA compilation failure.
- Output artifact absent or malformed.
- Route metadata shows `transport_ad_mode!="full"`.
- Claude review returns `VERDICT: REVISE` for a nonfixable boundary issue or the
  same blocker fails five review rounds.
