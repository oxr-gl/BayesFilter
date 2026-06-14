# P10 Zhao-Cui TT Paper-Code Crosswalk Ledger

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui, JMLR 2024.
- Companion code `DeepTransport/tensor-ssm-paper-demo`.

what_is_not_concluded:
- No claim that every theorem is implemented.
- No claim that code results reproduce paper figures in this environment.
- No claim that BayesFilter has implemented the method.

## Crosswalk

| Paper object | Paper anchor | Code path | Audit status |
|---|---|---|---|
| SSM transition and observation densities | Equations (1)--(3) | `models/ssmodel.m`; model folders `models/kalman`, `models/sv`, `models/sir_austria`, `models/pp` | `CODE_PRESENT` |
| Filtering, parameter, path, smoothing marginals | Equations (5)--(8) | `full_sol.smooth`, `pre_sol.smooth`, `theta_pdf`, `plot_stats` | `CODE_PRESENT_FOR_EXAMPLES` |
| Recursive posterior update | Equations (9)--(11) | `Y_sol.fun_into_sirt`, `full_sol.fun_into_sirt`, `pre_sol.fun_post` | `CODE_PRESENT` |
| Algorithm 1 nonseparable approximation | Eq. (12), Algorithm 1(a) | `fun_into_sirt` combines previous approximate density, transition, likelihood | `CODE_PRESENT` |
| Algorithm 1 separable TT approximation | Algorithm 1(b) | `TTIRT`/`TTSIRT`; `TTFun.cross` | `CODE_PRESENT` |
| Algorithm 1 integration/normalizer | Algorithm 1(c), normalizing constant \(c_t\) | `marginalise`; `sirt.z`; `logmarginal_likelihood` in `full_sol` | `CODE_PRESENT_WITH_SCALAR_SCOPE_CAVEAT` |
| Squared-TT defensive approximation | Eq. (13), Lemma 1 | `SIRT.potential_to_density`; `TTSIRT`; `obj.z = obj.fun_z + obj.tau` | `CODE_PRESENT` |
| Marginal density formula | Proposition 2, Eq. (14) | `@TTSIRT/marginalise.m`; QR/mass matrix recursion; `ys`, `ms` | `CODE_PRESENT` |
| Conditional KR maps | Eqs. (17)--(20), Proposition 4 | `eval_irt`, `eval_cirt`, `eval_rt`, `eval_rt_jac` | `CODE_PRESENT` |
| Particle filter accompanying TT | Algorithm 3, Eq. (23) | `Y_sol.solve`, `full_sol.solve`, `push_samples`, weights/ESS; exact Algorithm 3 structure partly distributed | `CODE_PRESENT_BUT_NOT_ISOLATED_AS_SINGLE_FUNCTION` |
| Path estimation/smoothing | Algorithm 4 | `full_sol.smooth`, `pre_sol.smooth`, `smooth_t` | `CODE_PRESENT` |
| Preconditioned replacements | Algorithm 5, Eq. (33)--(35) | `pre_sol.m` with options `pifg`, `fg`, `fgeta`, `g`, `geta` | `CODE_PRESENT_COMPLEX` |
| Error propagation | Theorem 7, Theorem 8 | Not directly executable; informs chapter limitations | `PAPER_THEORY_ONLY` |

## Main Finding

The companion code and the paper align on the central architecture: recursive
construction of an unnormalized joint posterior approximation over
`(x_t, theta, x_{t-1})`, TT/SIRT approximation, marginalization, conditional
KR maps, sample generation, weighting, and smoothing.

The code is research code rather than a minimal pedagogical implementation.
The paper algorithms are distributed across classes and inherited methods.
This is acceptable for implementation evidence, but Chapter 35 must present a
clean BayesFilter-level pseudocode rather than telling readers to infer the
method from MATLAB classes.

Decision:
`PAPER_CODE_CROSSWALK_PASS_WITH_REPRODUCTION_BLOCKED`
