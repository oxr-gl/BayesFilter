# P10 Zhao-Cui TT Reproducibility Ledger

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui JMLR 2024.
- `DeepTransport/tensor-ssm-paper-demo`, commit `80034dccb99eb1d86284a1839b4a12067d13b9da`.

what_is_not_concluded:
- No scientific replication claim.
- No posterior accuracy claim.
- No BayesFilter model validation.
- No HMC readiness.
- No production readiness.

## Intended Smoke

The smallest intended smoke was the Kalman demo:

```text
cd /tmp/bayesfilter-p10-zhao-cui-tensor-ssm-paper-demo/eg1_kalman
run main_script.m
```

The README says to first run `deep-tensor.dev/load_dir.m` and then run the
`main_script` in each `eg*` directory.  The Kalman script sets:
- `name = 'kalman'`
- `d = 2`, `m = 3`, `n = 3`
- `T = 50`
- `N = 5e3`
- `rank = 30`
- squared and non-squared variants through `full_sol`

## Environment Result

The local environment is blocked:
- `command -v matlab`: not found
- `command -v octave`: not found

Status:
`ENVIRONMENT_BLOCKED_NO_MATLAB_OR_OCTAVE`

This is not an algorithmic failure.  It means this P10 pass cannot honestly
claim executed reproduction in the current environment.

## Static Run-Path Audit

The Kalman run path is understandable from code:
- `eg1_kalman/main_script.m` constructs `ssmodel`, calls `setup`, generates data
  with `complete`, constructs `full_sol`, and runs `solve`.
- `models/kalman/setup.m` fixes RNG for `theta` and `C`, then shuffles RNG.
- `models/kalman/st_process.m` defines state propagation.
- `models/kalman/like.m` defines Gaussian observation likelihood.
- `models/kalman/theta_pdf.m` computes an analytic/reference parameter density
  used for L1 comparison plots.
- `models/full_sol.m` drives the squared and non-squared TT approximations and
  stores a log-marginal-likelihood accumulator.

## Reproducibility Decision

`REPRODUCIBILITY_STATIC_AUDIT_PASS_RUN_BLOCKED`

The code has a credible executable path, but a replicated numerical result was
not produced in this environment.  Any chapter claim must therefore say
"companion code exists and its run path was audited; local execution was
blocked by missing MATLAB/Octave," unless a later MATLAB run is performed.
