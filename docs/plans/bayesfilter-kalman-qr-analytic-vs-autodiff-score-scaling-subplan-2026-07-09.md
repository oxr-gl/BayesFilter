# Kalman QR Analytic Vs Autodiff Score Scaling Subplan

Date: 2026-07-09

Owning root: `/home/ubuntu/python/BayesFilter`

## Status

`PLAN_READY_FOR_BOUNDED_BENCHMARK`

## Skeptical Audit

Status: passed for a bounded timing diagnostic.

- Wrong baseline: the comparator is the same QR square-root Kalman log
  likelihood differentiated by TensorFlow `GradientTape`, not a covariance-form
  Kalman filter or a different likelihood.
- Proxy metrics: warm wall time and compile time are engineering diagnostics
  only. They do not certify posterior correctness, HMC readiness, production
  readiness, or statistical superiority.
- Missing stop conditions: stop or mark the row invalid if either method emits
  a nonfinite value/score, if analytical and autodiff values disagree beyond
  tolerance, if score residual exceeds tolerance, if the selected device is not
  recorded, or if the artifact is not written.
- Unfair comparisons: keep parameter dimension fixed at two so state and
  measurement dimensions are the scaling variables. Use the dynamic QR value
  loop for autodiff so the comparison is not confounded by Python time unroll.
- Hidden assumptions: the benchmark uses dense, time-invariant, square-root QR
  LGSSMs with equal state and measurement dimensions `(10, 10)`, `(20, 20)`,
  `(30, 30)`, `T=120`, fixed observations, and a two-parameter family.
- Stale context: current public QR analytical score authority is
  `tf_qr_sqrt_kalman_score`; this run does not change that API or any default.
- Environment mismatch: GPU/XLA is the default target. CPU-only or non-JIT runs
  must be labeled debug/reference exceptions if used.
- Artifact adequacy: JSON and Markdown artifacts under `docs/benchmarks/` must
  preserve command, environment, device visibility, timings, finite checks, and
  value/score agreement diagnostics.

Reason to proceed: the requested benchmark is small enough to run as a focused
diagnostic after recording the comparator, vetoes, and nonclaims.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | How do warm-call computation times vary with state/measurement dimension for analytical QR score versus autodiff score at `T=120`? |
| Candidate or mechanism under test | Public analytical QR square-root score propagation in `tf_qr_sqrt_kalman_score`. |
| Comparator | TensorFlow `GradientTape` score of the dynamic QR square-root log likelihood. |
| Expected failure mode | XLA compilation failure for QR gradients, slow compile time, nonfinite numerical output, or score disagreement from a derivative-law mismatch. |
| Promotion criterion | No promotion. The run answers a descriptive timing question only. |
| Promotion veto | Any row with nonfinite outputs or failed value/score parity cannot be used for a timing ratio interpretation. |
| Continuation veto | TensorFlow runtime unavailable, all rows fail to compile/run, or artifacts cannot be written. |
| Repair trigger | XLA failure triggers an explicitly labeled non-JIT debug/reference rerun or a smaller diagnostic row. |
| Explanatory diagnostics | Compile+first-call time, warm-call median/mean/min/max, output devices, value residual, score max-abs residual, and score relative residual. |
| What must not be concluded | No HMC readiness, posterior correctness, production default change, or statistically supported ranking is concluded. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific or engineering question | Measure descriptive speed scaling for analytical QR score and autodiff score across `(state_dim, measurement_dim) = (10,10), (20,20), (30,30)` with `T=120`. |
| Exact baseline/comparator | Autodiff is `GradientTape` over `tf_qr_sqrt_kalman_log_likelihood_while_loop` on the same observations, parameters, and model tensors. |
| Primary pass/fail criterion | Each reported timing row must have finite value/score outputs and pass analytical-vs-autodiff value/score agreement tolerances. |
| Veto diagnostics | Nonfinite outputs, value residual above `1e-8`, score max residual above `1e-5`, missing timing samples, missing device manifest, or missing artifact. |
| Explanatory only | Runtime medians, runtime ratios, compile+first-call time, device placement, and TensorFlow warning text. |
| Not concluded if passed | Passing rows do not prove analytical QR is universally faster, statistically superior, HMC-ready, or production-ready for all LGSSMs. |
| Artifact | `docs/benchmarks/kalman_qr_analytic_vs_autodiff_score_scaling_2026-07-09.json` and matching Markdown result note. |

## Planned Command

```bash
python scripts/benchmark_kalman_qr_analytic_vs_autodiff_score.py \
  --dimensions 10 20 30 \
  --timesteps 120 \
  --warmups 2 \
  --repeats 7 \
  --jit-compile
```

