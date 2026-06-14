# P8d Filter Benchmark Gap-Closure Plan

metadata_date: 2026-06-13
status: `PAUSED_NOT_READY_FOR_EXECUTION`

## Safety Correction

As of 2026-06-13 15:55 local inspection, this P8d plan must not be
launched as a benchmark run.  The P8d runner is a partial draft copied from
the P8c runner and still contains P8c metadata/status strings, LGSSM-only DPF
dispatch, and pending non-LGSSM deterministic dispatch.  It compiles, but it
has not passed focused tests, Claude read-only review, or a skeptical
execution audit.

Valid current evidence remains the P8c artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-summary-2026-06-13.md`

The P8d runner is intentionally disabled until the phases below are completed
and reviewed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining P8c benchmark holes be converted into reviewed numeric value/score cells wherever the existing TensorFlow implementation already supports the model/filter target, while preserving true target-inapplicable cells? |
| Baseline | P8c numeric artifact `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json` and runner `scripts/filtering_value_gradient_benchmark_run_p8_numeric.py`. |
| Primary criterion | Every target-compatible non-DPF deterministic cell has a finite value and, where TensorFlow autodiff is contractually meaningful, a finite score; every DPF value-compatible cell has a five-seed stochastic value summary with MC standard error; remaining cells are only structured not-applicable or explicitly diagnostic-no-gradient. |
| Veto diagnostics | A proxy route is reported as native; exact Kalman is run outside LGSSM or declared KSC mixture; spatial SIR P8 no-free-theta score is filled with a P44 diagnostic theta; old LEDH-PFPF-OT is used; DPF values lack five seeds; score coordinate/provenance is missing; nonfinite values are hidden as executed. |
| Explanatory diagnostics | Runtime, ESS, DPF sample standard deviation, Hessian availability, score norms, and cell nonclaims. |
| Not concluded | Full filter ranking, Bayesian estimation readiness, exact nonlinear likelihood truth, native generalized-SV/CNS production readiness, or DPF gradient validity. |
| Artifacts | P8d JSON/CSV/Markdown result tables, this plan, focused tests, and a Claude read-only review result note. |

## Skeptical Plan Audit

Audit status: `PASS_WITH_TARGET_SCOPE_RESTRICTIONS`.

The user asked to fill remaining cells. Literal filling is unsafe for these cells:

- exact Kalman outside LGSSM or the declared KSC Gaussian-mixture surrogate;
- spatial SIR score/Hessian cells under the current P8 source row, because the row has `truth_theta=[]`;
- DPF gradients/Hessians, because no reviewed gradient contract exists.

Those cells must stay structured not-applicable or value-only. The remaining gaps are implementation adapters and DPF callbacks.

## Closure Phases

### Phase P8d-1: Deterministic Model Adapters

Add a runner-local adapter registry that regenerates the P8 synthetic datasets by seed and exposes:

- actual SV native raw-observation dense quadrature value/score using `StochasticVolatilitySSM`;
- KSC transformed-SV mixture value/score using `independent_panel_sv_mixture_kalman_filter` or CUT4 mixture wrappers;
- predator-prey additive-Gaussian structural sigma-point value/score using the P30/P44 model contract;
- generalized SV native dense value/score using `NativeGeneralizedSVSSM` at the P8 prior-mean synthetic row;
- spatial SIR value-only structural route, keeping score/Hessian as `not_applicable_no_free_theta`.

### Phase P8d-2: Zhao-Cui Adapters

Use only existing reviewed source-route substitutes:

- scalar exact transformed SV and KSC transformed SV use fixed-design scalar/factorized Zhao-Cui routes when feasible;
- predator-prey uses the existing multistate fixed-design TT value route at the P8 horizon if it passes the smoke budget;
- spatial SIR uses P59 execution-only source-route result as a value-cell execution status, not as accuracy or gradient evidence;
- generalized SV remains non-Zhao-Cui unless an existing same-target Zhao-Cui route is available; otherwise it must be an explicit structured route gap, not a silent hole.

### Phase P8d-3: DPF Callback Adapters

Provide non-LGSSM callbacks for bootstrap DPF and LEDH-PFPF Alg1:

- actual SV and KSC SV use scalar state transition and raw/transformed observation callbacks as declared;
- predator-prey uses additive-Gaussian transition and identity observation callbacks;
- generalized SV uses native two-state transition and raw observation callbacks;
- spatial SIR value callbacks may execute only if finite with the source-route no-free-theta row.

All DPF value cells require exactly seeds `[81120, 81121, 81122, 81123, 81124]`.

### Phase P8d-4: Audit And Launch

Run focused tests, JSON/CSV validation, `git diff --check`, and Claude read-only review. Launch the CPU-only P8d run only after the audit passes.

## Stop Rules

Do not stop merely because a missing adapter is inconvenient. Stop only if:

- the target contract is genuinely not applicable;
- the existing implementation cannot expose the model/filter route without writing new algorithmic code beyond adapter closure;
- a focused smoke run is nonfinite or exceeds the supervised-run budget;
- Claude identifies a material route/provenance mismatch.

## Nonclaims

- This plan does not make exact Kalman valid outside LGSSM/KSC surrogate.
- This plan does not certify DPF gradients.
- This plan does not convert spatial SIR execution-only evidence into accuracy.
- This plan does not use old LEDH-PFPF-OT evidence.
