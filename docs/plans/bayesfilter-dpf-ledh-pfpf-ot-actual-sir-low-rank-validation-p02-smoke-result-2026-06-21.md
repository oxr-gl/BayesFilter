# P02 Tiny Actual-SIR Route Smoke Result

Date: 2026-06-21

Status: `PASS`

## Phase Objective

Run the smallest actual-SIR route diagnostics that prove both streaming and
low-rank paths execute on the real actual-SIR workload before expensive paired
GPU ladder runs.

## Artifacts

| Artifact | Path |
| --- | --- |
| Smoke aggregate JSON | `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21.json` |
| Smoke aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21.md` |
| Row JSON | `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t3-n128.json` |
| Row Markdown | `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t3-n128.md` |
| Row JSON | `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t20-n256.json` |
| Row Markdown | `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t20-n256.md` |

## Checks Run

| Row | Command Scope | Result |
| --- | --- | --- |
| `B=1,T=3,N=128` | CPU-hidden, both routes, `warmups=0`, `repeats=1` | `PASS` |
| `B=1,T=20,N=256` | CPU-hidden, both routes, `warmups=0`, `repeats=1` | `PASS` |

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Actual-SIR semantics | `PASS` for both rows. |
| Route-fired evidence | `PASS`; streaming and low-rank invocation counts equal active resampling step counts. |
| Finite outputs | `PASS`; log likelihood, filtered means/variances, ESS, final particles, and final log weights finite. |
| Low-rank nonmaterialization | `PASS`; low-rank transport sentinel shapes end in `[0,0]` and materialization flag is false. |
| Low-rank factor diagnostics | `PASS`; finite nonnegative `Q,R`, positive `g`, and factor residual below `5e-3`. |
| Paired comparability | `PASS` under the predeclared engineering OR gates. The `B=1,T=20,N=256` row has filtered-variance relative L2 above `0.75`, but filtered-variance RMS is below `25.0`, so the variance gate passes by its RMS alternative. |

## Notes

These smoke runs were CPU-hidden. Their runtime ratios are explanatory only and
cannot support promotion, speedup, GPU, or large-N claims.

TensorFlow emitted CUDA initialization warnings even with
`CUDA_VISIBLE_DEVICES=-1`; the artifacts record CPU output devices and no
logical GPUs.

## Nonclaims

- No large-N performance claim.
- No speedup claim.
- No posterior correctness claim.
- No HMC readiness claim.
- No public API/default/production readiness claim.

## Next Phase Handoff

Advance to P03 paired actual-SIR ladder. P03 must run in a trusted GPU context
with GPU1 preferred unless busy, GPU0 fallback only if recorded, same physical
GPU UUID for paired support rows, and exact `warmups=1`, `repeats=3` timing for
promotion-screen rows.
