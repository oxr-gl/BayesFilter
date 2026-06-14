# P39 Result: SV Gaussian-Mixture CUT4 Comparator

metadata_date: 2026-06-06
phase: P39

Status: `PASS_P39_LOCAL_IMPLEMENTATION_AND_GOVERNANCE`.

## Decision Table

| Field | Status |
|---|---|
| Decision | Implemented and locally verified as an experimental highdim-scoped transformed-SV Gaussian-mixture CUT4 comparator. |
| Primary criterion | `PASS`: one-step and two-step scalar transformed-mixture CUT4 fixtures agree with the dense transformed-mixture reference inside declared local tolerances. |
| Veto diagnostics | `PASS`: mixture weights/variances valid; transformed observations finite; dense reference finite; component weights normalize; CUT4 diagnostics finite; no native-SV equivalence or production-default claim. |
| Main uncertainty | Same-target transformed-mixture TT lane is not implemented; current scalar fixture validates mixture bookkeeping and Gaussian component-update reduction, not nonlinear CUT4 accuracy. |
| Next justified action | Build a same-target transformed-mixture TT comparison lane or a nonlinear transformed-mixture fixture before making stronger TT/CUT4 comparison claims. |
| What is not concluded | No exact native SV likelihood, no KSC importance reweighting, no full KSC sampler, no CNS generalized-SV estimator, no paper-scale result, no derivative/GPU/HMC/DSGE readiness, no production default. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `7ccb9c39883471c2d5ec2891cbf33b9ed436bada` |
| Run timestamp | `2026-06-06 22:55:37 HKT` |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p39-sv-mixture-cut4-master-plan-2026-06-06.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p39-sv-mixture-cut4-result-2026-06-06.md` |
| Code artifact | `bayesfilter/highdim/sv_mixture_cut4.py` |
| Test artifact | `tests/highdim/test_p39_sv_mixture_cut4.py` |
| Documentation artifact | `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`, Section `sec:bf-hd-sv-mixture-cut4` |
| Bibliography artifact | `docs/references.bib` entries `kim1998stochasticvolatility`, `chib2002mcmcsv` |
| CPU/GPU status | CPU-only verification; `CUDA_VISIBLE_DEVICES=-1` used for TensorFlow pytest commands. |
| Random seeds | N/A: deterministic tiny fixtures and deterministic quadrature rules. |
| Data version | N/A: synthetic scalar observations only. |
| Wall time | Focused P39 tests 4.78s; guardrail suite 15.50s; LaTeX build completed. |

## Implemented Scope

- Added `SVLogChiSquareGaussianMixture`, `SVMixtureCut4Result`,
  `ksc_1998_log_chi_square_mixture`,
  `transformed_sv_observations`,
  `scalar_sv_mixture_dense_reference`, and
  `scalar_sv_mixture_cut4_filter` in `bayesfilter/highdim/sv_mixture_cut4.py`.
- Exported the comparator only from `bayesfilter.highdim`; no top-level
  `bayesfilter` export was added.
- Documented the transformed SV mixture route, component CUT4 update,
  simple-SV recursion, CNS-style generalized template boundary, TT comparison
  boundary, and claim boundary in Chapter 34.
- Added P39 source-support, claim-support, omitted-paper-risk, Claude review,
  and traceability records.

## KSC Convention Audit

After Claude code/governance iteration 2 passed, Codex inspected the accessible
Kim--Shephard--Chib working-paper PDF.  The source text supports:

- log-square transform `log y_t^2 = h_t + log epsilon_t^2`;
- moments `E log epsilon_t^2 = -1.2704` and variance approximately `4.93`;
- offset transform `y_t^* = log(y_t^2 + c)`;
- Table 4 seven-component probabilities, tabulated locations, and variances;
- component law using locations shifted by `-1.2704`.

The implementation was corrected to use effective component means
`a_j - 1.2704` for `log(epsilon_t^2)`.  The focused tests now check that the
fixture mixture mean is close to `-1.2704` and variance is close to `pi^2/2`.

## Verification

| Command | Result |
|---|---|
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p39_sv_mixture_cut4.py` | `6 passed, 2 warnings in 4.78s` |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p39_sv_mixture_cut4.py tests/highdim/test_p30_stochastic_volatility.py tests/highdim/test_p30_sv_short_sequential_tt_value_path.py tests/highdim/test_p30_cut4_statistical_comparators.py tests/highdim/test_public_api_highdim.py tests/test_v1_public_api.py` | `34 passed, 2 warnings in 15.50s` |
| `python -m compileall -q bayesfilter/highdim/sv_mixture_cut4.py tests/highdim/test_p39_sv_mixture_cut4.py` | Passed |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `docs/` | Passed; `docs/main.pdf` rebuilt, 294 pages |

Warnings were TensorFlow Probability `distutils` deprecation warnings and
pre-existing LaTeX overfull/underfull box noise; neither is a P39 veto.

## Claude Review Loop

| Iteration | Verdict | Outcome |
|---|---|---|
| Plan/doc iteration 1 | `BLOCKED_P39_PLAN_DOC_GOVERNANCE` | Fixed CUT4 definition, mixture table, source/claim boundaries, scalar fixture non-claim, and TT boundary. |
| Plan/doc iteration 2 | `PASS_P39_PLAN_DOC_GOVERNANCE` | Plan/doc governance accepted with KSC exact table convention noted for recheck. |
| Code/governance iteration 1 | `BLOCKED_P39_CODE_GOVERNANCE` | Fixed CUT4-G degree wording, ambiguous point-count diagnostic, and missing `dim >= 3` padding-boundary test. |
| Code/governance iteration 2 | `PASS_P39_CODE_GOVERNANCE_SUPERSEDED_BY_KSC_SHIFT_AUDIT` | Prior blockers fixed; superseded by Codex KSC convention audit. |
| Code/governance iteration 3 | `SUPERSEDED_TIMEOUT` | Broad final review worker stayed silent for roughly fifteen minutes and was stopped by exact review label. |
| Code/governance iteration 3B | `PASS_P39_CODE_GOVERNANCE_ITER3B` | Narrow blocker-only final review passed for KSC shift, overclaim boundary, diagnostics, and CUT4-G padding/degree guardrails. |

## Interpretation

The P39 comparator is a coherent local implementation target: it transforms
scalar SV observations, approximates log-chi-square noise by the KSC
seven-component shifted Gaussian mixture, performs component-wise additive
Gaussian CUT4 updates, and collapses component moments back to one Gaussian.
On the tiny scalar fixtures, CUT4 agrees with the dense transformed-mixture
reference because the conditional component observation is linear Gaussian.

This is useful as the least-change bridge between SV and the existing CUT4
machinery.  It should not be read as native SV exactness or as evidence that
CUT4 is accurate for every nonlinear SV extension.

## Post-Run Red Team

| Risk | Status |
|---|---|
| The run could pass while testing the wrong target. | Mitigated by explicit target naming: transformed finite-mixture SV, not native SV. |
| The KSC table convention could be stale or shifted incorrectly. | Mitigated by source audit and moment test; still recheck against published PDF before publication if needed. |
| Dense reference and CUT4 could share the same coding bug. | Partially mitigated by independent dense-grid path versus structural CUT4 path; both still share the same mixture fixture and transformed target. |
| TT comparison could be overread. | Mitigated by non-claim: existing TT lane is native SV and explanatory only unless same-target mixture TT is built. |
| CNS section could sound implemented. | Mitigated by claim boundary: CNS is a derivation template/context only; exact CNS equation anchors remain source-governance gaps. |
