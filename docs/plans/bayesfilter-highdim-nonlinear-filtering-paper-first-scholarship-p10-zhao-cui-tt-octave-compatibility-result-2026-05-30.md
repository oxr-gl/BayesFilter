# P10 Zhao-Cui TT Octave Compatibility Result

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Companion code `DeepTransport/tensor-ssm-paper-demo`, audit clone commit `80034dccb99eb1d86284a1839b4a12067d13b9da`.

what_is_not_concluded:
- No production BayesFilter implementation.
- No claim that all companion examples run under Octave.
- No claim that the reduced smoke reproduces paper figures.
- No posterior accuracy claim.
- No HMC readiness or analytical-gradient implementation claim.
- No permission to copy LGPL/GPL companion code into production modules.

## Environment

Octave is available through:

```text
/usr/bin/octave-cli
```

The working command form is:

```text
octave-cli --quiet --no-gui <script.m>
```

The plain `octave --version` command hung once inside the Codex sandbox, while
`octave-cli --quiet --no-gui --eval "disp(OCTAVE_VERSION)"` returned 6.4.0.
Therefore all smoke commands used `octave-cli` with shell `timeout`.

## Audit Clone

Patched clone:

```text
/tmp/bayesfilter-p10-zhao-cui-tensor-ssm-paper-demo
```

The production `bayesfilter/` package was not edited.  The patch is an audit
port only.

## Compatibility Patch Summary

The companion code targets MATLAB 2021a/2023a.  Octave 6.4 required the
following audit-copy changes:

- removed MATLAB property-validation annotations from selected classes,
  including `ssmodel`, `Y_sol`, `Domain`, `Oned`, `Piecewise`, `Lagrange1`,
  `Lagrangep`, `LagrangeRef`, `Recurr`, `Spectral`, `SpectralCDF`,
  `PiecewiseCDF`, `OnedCDF`, `ApproxFun`, and `AbstractIRT`;
- replaced abstract-method prototype blocks with ordinary stub methods in
  base classes that Octave otherwise refused to parse;
- added `octave_compat/` shims for `normcdf`, `normpdf`, `norminv`, `mvnpdf`,
  `datasample`, `rng`, and `vpa`;
- patched `@TTFun/local_truncate.m` to replace MATLAB
  `cumsum(x,'reverse')` with `flipud(cumsum(flipud(x)))`;
- patched `models/ESS.m` to avoid `sum(...,'omitnan')`;
- added a Kalman `transition.m` density matching the Kalman `st_process.m`
  for the audit smoke, because the Kalman folder did not include a transition
  density file although `full_sol.fun_into_sirt` calls `transition`;
- added `octave_compat/p10_octave_kalman_smoke.m`, a reduced Kalman run with
  `T=1`, `N=64`, `rank=4`, `max_als=1`, and no plotting.

## Smoke Command

```text
timeout 60s octave-cli --quiet --no-gui \
  /tmp/bayesfilter-p10-zhao-cui-tensor-ssm-paper-demo/octave_compat/p10_octave_kalman_smoke.m
```

## Smoke Result

Status:

```text
OCTAVE_REDUCED_KALMAN_SMOKE_PASS
```

Observed output included:

```text
FTT approximation at time 1 because ESS = 30.11 / 64.
Enhanced ESS is 30.11.
>> ALS completed, TT ranks
>> 3  3  3  3  2  3  3  1
The total ESS is 39.52 out of 64.
P10_OCTAVE_SMOKE_DONE
-4.6262
```

Octave still prints an exit warning:

```text
error: ignoring const execution_exception& while preparing to exit
```

The process exit code was 0 for the successful smoke.

## Interpretation

The successful reduced smoke materially improves the P10 evidence.  The
Zhao-Cui companion code is not merely static MATLAB text: after a bounded
Octave compatibility patch, the Kalman path reaches the TT/SIRT approximation
step, completes one ALS pass, constructs TT ranks, samples through the inverse
Rosenblatt path, reports ESS, and returns a finite log-marginal-likelihood
accumulator.

This is still not scientific replication.  The full paper demo uses
`T=50`, `N=5000`, `rank=30`, plotting, and MATLAB-oriented defaults.  The
Octave smoke is intentionally reduced and does not validate posterior
accuracy, parameter learning quality, smoothing, or high-dimensional
performance.

## Decision

The earlier P10 reproducibility status should be upgraded from
`REPRODUCIBILITY_STATIC_AUDIT_PASS_RUN_BLOCKED` to:

```text
REPRODUCIBILITY_REDUCED_OCTAVE_SMOKE_PASS_FULL_DEMO_NOT_REPLICATED
```

This supports promoting Zhao-Cui as a code-backed TT filtering/transport
candidate, while keeping the analytical-gradient and full-replication claims
conditional.
