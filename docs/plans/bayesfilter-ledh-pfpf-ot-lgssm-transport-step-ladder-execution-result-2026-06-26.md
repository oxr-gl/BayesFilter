# LEDH-PFPF-OT LGSSM Transport Step-Ladder Execution Result

Date: 2026-06-26

## Decision Table

| Field | Status |
|---|---|
| decision | Mixed result: low-step `8` transport is clearly under-converged, but the high-budget `80`/`100` run does not fully clear the all-time row-residual gate, and covariance contraction remains large. |
| primary criterion status | Partial H1 support; H2 remains live for worst-time row residuals; H3 remains live after high-budget rows improve. |
| veto diagnostic status | Planned CPU/XLA ladder vetoed by timeout/artifact failure; CPU non-XLA fallback completed and is diagnostic-only. |
| main uncertainty | Whether higher finite budgets clear the worst-time row residuals, or whether a transport normalization/application issue remains at those times. |
| next justified action | Run a focused worst-time row-residual budget diagnostic before changing production transport or the LGSSM statistical harness; after row residuals clear, test reset covariance semantics. |
| forbidden conclusions | No gradient correctness, SIR correctness, GPU/XLA performance, HMC readiness, posterior correctness, production readiness, or broad scientific validity is concluded. |

## Manifest

| Field | Value |
|---|---|
| plan | `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-transport-normalization-step-ladder-plan-2026-06-26.md` |
| reviewed plan | Claude exact-path review returned `VERDICT: AGREE` |
| diagnostic script | `docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py` |
| planned CPU/XLA command | `/usr/bin/timeout 600 python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py --device-scope cpu --num-particles 128 --dense-parity-particles 64 --seed-count 10 --state-dims 1 2 --settings 0.5:8 0.5:20 0.5:80 0.5:100 --xla --output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-transport-step-ladder-2026-06-26.json --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-transport-step-ladder-2026-06-26.md` |
| planned CPU/XLA result | Timed out twice at 600s; no JSON/markdown artifact was written. The second run emitted a CPU-XLA slow-compile alarm, so this is a diagnostic-harness compile blocker, not transport evidence. |
| fallback command | `/usr/bin/timeout 600 python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py --device-scope cpu --num-particles 128 --dense-parity-particles 64 --seed-count 10 --state-dims 1 2 --settings 0.5:8 0.5:20 0.5:80 0.5:100 --no-xla --output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-transport-step-ladder-nonxla-fallback-2026-06-26.json --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-transport-step-ladder-nonxla-fallback-2026-06-26.md` |
| fallback artifact | `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-transport-step-ladder-nonxla-fallback-2026-06-26.json` and `.md` |
| fallback scope | CPU-only, GPU hidden with `CUDA_VISIBLE_DEVICES=-1`, `xla=False`, diagnostic only. |
| fallback runtime | `546.0411859090091` seconds |

## Evidence Summary

The fallback result shows that `8` finite Sinkhorn steps is badly
under-converged:

| State dim | Steps | t0 shared row residual | max per-time row residual | total value delta to Kalman | t0 post/pre covariance trace |
|---:|---:|---:|---:|---:|---:|
| 1 | 8 | `9.198693e-01` | `9.933776e-01` | `0.417087` | `0.361629` |
| 1 | 20 | `4.573679e-02` | `3.427538e-01` | `0.294254` | `0.575943` |
| 1 | 80 | `3.746748e-04` | `1.887238e-02` | `0.288316` | `0.589902` |
| 1 | 100 | `8.296967e-05` | `1.509064e-02` | `0.288315` | `0.589902` |
| 2 | 8 | `9.619392e-01` | `8.698454e-01` | `0.932990` | `0.274686` |
| 2 | 20 | `3.862303e-02` | `8.457744e-02` | `0.849392` | `0.338653` |
| 2 | 80 | `1.937151e-05` | `5.374432e-03` | `0.849000` | `0.339203` |
| 2 | 100 | `1.668930e-06` | `3.241181e-03` | `0.848999` | `0.339203` |

Dense/streaming parity on the shared cloud remained good
(`<= 2.384e-07`) and dense column residuals stayed at about `5.960e-07` to
`7.153e-07`.

The high-budget shared-cloud row residuals pass by `80`/`100`, but the
all-time row residual gate still fails at later times:

- state dimension 1, `steps=100`: max row residual `1.509064e-02` at time 8;
- state dimension 2, `steps=100`: max row residual `3.241181e-03` at time 7.

The known-contract thresholded comparator did not provide a clean row-residual
pass on the shared cloud:

| State dim | Exact/thresholded row residual | Exact/thresholded column residual | Iterations | Manual fixed100 row residual | Max particle diff |
|---:|---:|---:|---:|---:|---:|
| 1 | `3.052992e-02` | `5.960464e-07` | `25` | `8.296967e-05` | `2.991748e-02` |
| 2 | `2.642703e-02` | `5.960464e-07` | `25` | `1.668930e-06` | `1.614141e-02` |

This weakens a simple H4 story in which the manual fixed-step route is worse
than the thresholded route. Here manual fixed `100` is better on the shared
row-residual metric, while the thresholded route appears to stop on potential
changes before satisfying the row-marginal diagnostic.

## Interpretation

The result supports under-convergence as a real part of the bug: moving from
`8` to `80`/`100` greatly reduces row residuals and improves the 1D value gap.
However, it does not justify simply updating the LGSSM harness to `100` steps:

- full-time row residuals still exceed the `1e-3` gate at worst times;
- the value gap remains large after `80`/`100` steps (`0.288315` in 1D and
  `0.848999` in 2D);
- covariance contraction remains substantial at time 0 (`0.589902` in 1D and
  `0.339203` in 2D);
- the thresholded comparator's row residual also fails, so it cannot be used
  as a passing oracle for row normalization.

## Next Move

Run a smaller focused budget diagnostic rather than the full CPU/XLA ladder:

1. Target the worst residual times from the fallback result: 1D time 8 and 2D
   time 7.
2. Use the same `N=128`, 10-seed, CPU diagnostic fixture, but only the needed
   state dimensions and budgets, e.g. `steps=100,200,400`.
3. Record all-time row residual, column residual, dense/streaming parity, value
   delta, and covariance trace ratios.
4. If all-time row residual clears below `1e-3` and the value/covariance gap
   remains, move to reset covariance semantics.
5. If all-time row residual does not clear with larger finite budgets, inspect
   transport-from-potentials normalization/application before any production
   patch.

Do not launch N1000 GPU/XLA or change production transport from this fallback
alone.
