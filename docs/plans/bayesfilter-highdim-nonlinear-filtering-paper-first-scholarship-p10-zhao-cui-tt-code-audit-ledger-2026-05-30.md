# P10 Zhao-Cui TT Code Audit Ledger

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Companion code `DeepTransport/tensor-ssm-paper-demo`, commit `80034dccb99eb1d86284a1839b4a12067d13b9da`.
- Embedded `deep-tensor.dev` package.

what_is_not_concluded:
- No production readiness.
- No BayesFilter implementation readiness.
- No posterior accuracy on BayesFilter target models.
- No HMC convergence.
- No full analytical-gradient implementation.
- No permission to copy companion code into production `bayesfilter/`.

## Repository Snapshot

Audit clone:
`/tmp/bayesfilter-p10-zhao-cui-tensor-ssm-paper-demo`

Remote HEAD:
`80034dccb99eb1d86284a1839b4a12067d13b9da`.

The repository is real and substantial.  It contains:
- `eg1_kalman/main_script.m`
- `eg2_sv/mainscript.m`
- `eg2_sv/mainscriptSP500.m`
- `eg3_sir/mainscript.m`
- `eg4_predatorprey/mainscript.m`
- `models/` state-space model and solver classes
- `deep-tensor.dev/` continuous tensor-train and SIRT/IRT machinery

## License

The top-level `LICENSE.md` states LGPL-3.0-or-later.  The embedded
`deep-tensor.dev` directory also carries LGPL/GPL license files.  This supports
inspection and local reproduction as research evidence, but it is not a green
light to copy code into proprietary or production `bayesfilter/` modules.  A
clean-room implementation or explicit license decision is required before any
production use.

## Runtime And Dependencies

The README states MATLAB 2021a and MATLAB 2023a.  The code uses MATLAB classes,
Statistics Toolbox-style functions such as `datasample`, `mvnpdf`, `normcdf`,
and plotting.

This environment has neither `matlab` nor `octave` on PATH:
- `command -v matlab`: not found
- `command -v octave`: not found

## Core Code Paths

State-space model shell:
- `models/ssmodel.m` stores dimensions, parameters, state/observation arrays,
  `complete`, and `push_samples`.
- `push_samples` propagates samples through `st_process`, then updates weights
  using `like`.

Basic sequential TT solver:
- `models/Y_sol.m` stores `SIRTs`, samples, weights, transforms `L`, `mu`,
  ESS, and `logmarginal_likelihood`.
- `Y_sol.solve` alternates sample propagation, ESS-triggered reapproximation,
  inverse Rosenblatt sampling from `SIRTs`, and weight updates.

Full squared/non-squared solver:
- `models/full_sol.m` uses the augmented variable ordering
  `(theta, x_t, x_{t-1})`.
- `full_sol.reapprox` builds the approximate posterior density at each time
  using `TTIRT` or `TTSIRT`.
- `full_sol.reapprox` accumulates
  `sol.logmarginal_likelihood = sol.logmarginal_likelihood + log(sirt.z) - const`.

Preconditioned solver:
- `models/pre_sol.m` implements Gaussian/tempered/preconditioned variants.
- It builds preconditioner `SIRTs`, maps `Tu2x` and `Tx2u`, and then builds a
  second SIRT for the residual/preconditioned posterior.

Continuous TT and transport substrate:
- `deep-tensor.dev/src/@TTFun/TTFun.m` builds functional TT approximations.
- `deep-tensor.dev/src/@TTFun/cross.m` implements ALS/cross with methods
  `fix_rank`, `random`, and `amen`.
- `deep-tensor.dev/src/@TTFun/local_truncate.m` uses SVD truncation controlled
  by `local_tol`, `min_rank`, and `max_rank`.
- `deep-tensor.dev/src/SIRT.m` and `deep-tensor.dev/src/IRT.m` convert
  potentials to squared or ordinary density approximations.
- `deep-tensor.dev/src/@TTSIRT/marginalise.m` computes marginal factors and
  `obj.z = obj.fun_z + obj.tau`.
- `deep-tensor.dev/src/AbstractIRT.m` exposes `eval_pdf`,
  `eval_potential`, `eval_irt`, `eval_cirt`, and `eval_rt_jac`.

## Evidence Assessment

The code implements the method family, not merely a plotting script.  It
contains recursive SSM solvers, TT approximation classes, squared-TT
nonnegativity machinery, KR map evaluation, conditional inverse map evaluation,
preconditioning variants, and example models.

The code is not currently a BayesFilter-ready backend:
- MATLAB runtime is required.
- The implementation is not TensorFlow/JAX/Python.
- It relies on random enrichment, data-split initialization/debug samples,
  SVD truncation, ESS triggers, and adaptive choices.
- It does not expose an analytical derivative of the learned TT cores with
  respect to state-space parameters.

Decision:
`CODE_AUDIT_PASS_FOR_RESEARCH_EVIDENCE_CONDITIONAL_FOR_PROMOTION`
