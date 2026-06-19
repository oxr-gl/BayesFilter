# P8p Phase 3h Result: Dense-vs-Streaming Transport AD Contract

Date: 2026-06-19

Status: `LOCALIZED_TO_SHARED_ANNEALED_TRANSPORT_AD_CONTRACT`

## Objective

Compare the repaired P8p regression-FD diagnostic under active-all dense
transport against the earlier active-all streaming transport result.  The goal
was to determine whether the AD/FD mismatch is specific to the streaming
memory-saving transport implementation or shared by the annealed transport
contract.

## Artifacts

- Subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3h-dense-streaming-transport-ad-contract-subplan-2026-06-19.md`
- Dense JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3h-dense-transport-ad-contract-n64-gpu-tf32-2026-06-19.json`
- Streaming comparator:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-adaptive-higher-particle-regression-fd-n64-gpu-tf32-2026-06-19.json`
- Patched scripts:
  - `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  - `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `9bcad31f0d9b21731b3915083d86834b43730f51` |
| TensorFlow | `2.19.1` |
| Device | trusted GPU, `/GPU:0`, RTX 4080 SUPER observed in run log |
| Precision | `float32`, TF32 enabled |
| Target | P8p parameterized SIR d18 diagnostic |
| Horizon / particles | `T=3`, `N=64` |
| Seeds | `81120,81121,81122,81123,81124` |
| Transport policy | `active-all` |
| Transport plan mode | `dense` |
| Window policy | AD-signal-scaled nested regression windows |
| Wall time | `109.967` seconds |

## Checks

Passed before the GPU diagnostic:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3h-dense-streaming-transport-ad-contract-subplan-2026-06-19.md
```

Trusted GPU placement passed.  The dense JSON records
`transport_plan_mode = dense` and `tf32_execution_enabled = true`.

## Dense Transport Result

Dense active transport produced clean slope plateaus but retained the same
AD/FD mismatch pattern as streaming active transport.

| Direction | Dense AD | Dense regression slopes | Residual pattern | Status |
| --- | ---: | ---: | --- | --- |
| `rho` | `-5.653861` | `[-7.597587, -7.603932, -7.613634]` | AD is about `1.95` above FD slope | Fails AD agreement |
| `tau_perp_given_rho` | `35.056801` | `[43.206558, 43.370956, 43.823383]` | AD is about `8.1` to `8.8` below FD slope | Fails AD agreement |
| `omega_perp_given_rho_tau` | `60.415493` | `[62.320889, 62.599293, 62.199398]` | AD is about `1.8` to `2.2` below FD slope | Fails AD agreement |

The slope plateaus were strong enough to answer the localization question:
this is not a noisy-FD failure.

## Comparison To Streaming

Streaming Phase 3f and dense Phase 3h agree qualitatively:

| Direction | Streaming AD / slopes | Dense AD / slopes | Interpretation |
| --- | --- | --- | --- |
| `rho` | AD `-5.64`, slopes about `-7.6` | AD `-5.65`, slopes about `-7.6` | Same mismatch |
| `tau_perp` | AD `35.31`, slopes about `43.7` | AD `35.06`, slopes about `43.5` | Same mismatch |
| `omega_perp` | AD `60.82`, slopes about `62.8` | AD `60.42`, slopes about `62.4` | Same smaller mismatch |

Dense mode is therefore not the repair.  The primary discrepancy is shared by
the annealed transport AD contract.

## Interpretation

Phase 3h localizes the primary blocker one level deeper:

- Phase 3g showed that skipping transport mostly removes the large mismatch.
- Phase 3h shows that dense and streaming active transport both fail similarly.
- Therefore the issue is likely in shared annealed transport differentiation
  semantics, not only streaming chunking.

The strongest candidate remains deliberate stopped quantities in the transport
core, especially stopped centering/scale and stopped Sinkhorn potential keys.
Those may be numerically useful, but they mean the exposed AD derivative is a
surrogate gradient rather than the finite-difference derivative of the forward
value.

## Decision Table

| Decision | Primary diagnostic status | Veto status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Do not treat dense transport as a fix.  Move to a shared annealed-transport AD-contract ablation. | Dense and streaming both fail AD agreement with stable FD slopes. | Phase 3 remains blocked for active-all transport. | Which stopped term accounts for the mismatch, and whether the intended contract should be full forward-value AD or an explicit stabilized surrogate gradient. | Add opt-in transport AD-mode switches for stopped centering/scale and stopped Sinkhorn keys; run a small dense transport ablation before touching defaults. | No HMC readiness, no full-horizon stability, no exact likelihood correctness, no posterior validity, no leaderboard ranking, no production/default readiness. |

## Handoff

The next phase should add an opt-in diagnostic transport AD mode, not alter the
default route.  Minimum useful ablations:

1. current mode: stopped scale and stopped Sinkhorn keys;
2. differentiable scale with stopped keys;
3. stopped scale with differentiable keys;
4. fully differentiable scale and keys, if numerically stable.

Run these first at `T=3`, `N=64`, TF32, active-all dense transport, using the
same semantic-orthogonal adaptive regression-FD protocol.  Promote nothing to
HMC until active-all Phase 3 passes under a documented transport-gradient
contract.
