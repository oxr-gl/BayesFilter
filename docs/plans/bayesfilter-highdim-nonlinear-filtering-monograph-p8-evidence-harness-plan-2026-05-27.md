# P8 BayesFilter Evidence Harness and Benchmarks Plan

## Question

Can a focused CPU-only harness exercise existing BayesFilter nonlinear models
and high-dimensional extensions without making unsupported performance claims?

## Evidence Contract

Baseline:

- Existing BayesFilter nonlinear testing fixtures.
- Existing V1 nonlinear benchmark schema discipline.

Primary criterion:

- The harness records finite/shape/dtype status, point counts, runtime, CPU/GPU
  policy, seed policy, comparator id, labels, and non-implication text for
  existing Model B and block high-dimensional extensions.

Veto diagnostics:

- GPU commands run without escalation.
- CPU-only commands fail to hide GPU.
- CUT4 high-dimensional skipped rows are omitted rather than recorded.
- Timings are interpreted as broad speedup or production policy evidence.

Explanatory diagnostics:

- Runtime, memory, point counts, XLA compile status when CPU-only XLA succeeds.

Non-implications:

- Passing P8 does not certify high-dimensional filtering, HMC, GPU, or XLA
  readiness.

## Chapter-Use Restriction

P8 rows may be cited in chapters only as BayesFilter implementation
diagnostics: finite execution, shape/dtype behavior, point growth, skip labels,
CPU-only/XLA compile status, and runtime for exact tested cells.  They must not
be cited as algorithmic superiority, posterior accuracy, convergence,
high-dimensional validity, NAWM suitability, or production performance
evidence.

Artifacts:

- `docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py`
- `docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.json`
- `docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.md`

## Exit Label

`P8_HARNESS_ACCEPTED` if rows are bounded, reproducible, and conservative.

## Stop Rules

Stop P8 with a blocker if the harness cannot emit required manifest fields,
cannot record skipped high-dimensional CUT4 rows, or cannot keep CPU-only device
policy explicit.
