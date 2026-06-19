# P8e Result: LEDH SV Adapter Repair

Date: 2026-06-15

Status: `PASS_P8E_LEDHPFPF_SV_ADAPTER_FINITE_EXECUTION_REPAIRED`

## Summary

The P8d `ledh_pfpf_alg1_ukf_current` failures on the two SV-style rows were
reproduced as adapter-boundary failures and repaired without changing the shared
Algorithm 1 core.

The repaired P8d callbacks now use a log-square Gaussian surrogate only for the
LEDH/UKF flow observation, while the PF-PF correction continues to use the raw
SV observation likelihood. Bootstrap DPF still receives raw observations. The
repair also computes the raw zero-mean SV likelihood in log-scale form to avoid
overflow before log-probability evaluation.

## Files Changed

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8e-ledh-sv-adapter-repair-plan-2026-06-15.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8e-ledh-sv-adapter-repair-result-2026-06-15.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8f-dpf-particle-count-tuning-subplan-2026-06-15.md`

Unrelated dirty Zhao-Cui/monograph files were present before this lane work and
were not modified for P8e.

## Repair Details

| Row | LEDH flow observation | Flow covariance | Correction likelihood |
|---|---|---:|---|
| `zhao_cui_sv_actual_nongaussian_T1000` | `log(y_t^2 + 1e-6) - 2 log(beta)` | `2.0` | raw `N(0, beta^2 exp(h_t))` |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `log(y_t^2 + 1e-6)` | `2.0` | raw `N(0, exp(tau h_t))` |

The artifact cells now include `ledh_observation_adapter` metadata and per-seed
Algorithm 1 route identifiers. The metadata explicitly says the surrogate is
for flow construction only and is not a same-target transformed-SV claim.

## Checks

| Check | Result |
|---|---|
| `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q` | Passed: `11 passed, 2 warnings` in `75.91s` |
| `git diff --check` | Passed |
| Full-horizon one-seed CPU-only LEDH diagnostic, `N=8`, seed `81120` | Passed finite on both repaired rows |
| Full-horizon five-seed CPU-only LEDH cell diagnostic, `N=8`, seeds `[81120, 81121, 81122, 81123, 81124]` | Passed finite on both repaired rows in `725.942s` |

TensorFlow printed CUDA plugin/cuInit warnings despite
`CUDA_VISIBLE_DEVICES=-1`. Per local policy, these are not GPU diagnostics; the
checks were deliberate CPU-only checks.

## Focused Diagnostic Results

One-seed full-horizon `N=8` LEDH diagnostic:

| Row | Finite | Log likelihood | ESS min | ESS mean | Horizon |
|---|---:|---:|---:|---:|---:|
| `zhao_cui_sv_actual_nongaussian_T1000` | true | `-1128.3768371510744` | `1.0` | `1.112587039679976` | `1000` |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | true | `-1571.2325255907094` | `1.0000000149469448` | `1.351394932776367` | `1008` |

Five-seed full-horizon `N=8` LEDH cell diagnostic:

| Row | Status | Mean log likelihood | MC SE | ESS min |
|---|---|---:|---:|---:|
| `zhao_cui_sv_actual_nongaussian_T1000` | `executed_numeric_dpf_5seed_value` | `-1113.1003607523965` | `9.675676380953814` | `1.0` |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `executed_numeric_dpf_5seed_value` | `-1575.1889140248452` | `2.376146467555768` | `1.0000000000008549` |

## Decision Table

| Field | Status |
|---|---|
| Decision | Close P8e adapter blocker as repaired for finite current Algorithm 1 execution on the two SV-style rows. |
| Primary criterion status | Passed: focused one-seed and five-seed full-horizon CPU-only LEDH runs are finite on both rows. |
| Veto diagnostic status | Passed: bootstrap raw observations preserved; LEDH surrogate is flow-only; raw correction likelihood preserved; no Algorithm 1 core refactor; no Zhao-Cui/source-route or model-data substitution. |
| Main uncertainty | Particle count `8` is far too small for serious DPF accuracy or ranking. ESS is near 1 on both repaired rows. |
| Next justified action | Execute reviewed P8f particle-count tuning under a separate evidence contract before any serious P8d DPF comparison run. |
| Not concluded | No particle-count adequacy, no filter ranking, no DPF gradient certification, no posterior correctness, and no scientific validation of LEDH for paper-scale high-dimensional settings. |

## Next Subplan Review

P8f was drafted and reviewed as the next gated phase:

- local Codex review checked consistency, correctness, feasibility, artifact
  coverage, and boundary safety;
- Claude read-only local-file review round 1 returned `VERDICT: REVISE`;
- Codex patched the P8f subplan to use relative ESS, mandatory next-rung
  confirmation, staged CPU feasibility checks, per-cell runtime stop rules, and
  explicit tuning verdict fields;
- Claude read-only local-file review round 2 returned `VERDICT: AGREE`.

## Post-Run Red-Team Note

Strongest alternative explanation: the repair may only make the current small
particle-count run finite, while leaving severe particle degeneracy. The ESS
diagnostics support this concern.

What would overturn the decision: a later focused diagnostic showing that the
adapter metadata is bypassed, the correction no longer uses raw likelihoods, or
the same rows again emit non-finite corrected weights with the repaired
callbacks.

Weakest evidence: all full-horizon diagnostics used `N=8`, which is a wiring
regression setting only.
