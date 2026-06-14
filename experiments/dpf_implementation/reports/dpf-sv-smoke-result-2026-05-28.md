# DPF Stochastic Volatility Smoke Result

## Decision

`DPF_SV_SMOKE_PASSED`

DPF implementation next step authorized: experimental follow-up only.

## Smoke Question

Can BayesFilter-owned experimental classical PF code produce finite, schema-valid, reproducible smoke diagnostics on a small stochastic-volatility model?

Answer: yes for this bounded fixture.  The local clean-room runner emitted finite, schema-valid, reproducible diagnostics under the declared CPU-only contract.

## Model Definition

```text
x_0 ~ Normal(mu, sigma^2 / (1 - phi^2))
x_t = mu + phi (x_{t-1} - mu) + sigma eta_t, eta_t ~ Normal(0, 1)
y_t | x_t ~ Normal(0, beta^2 exp(x_t))
```

- parameters: `{'mu': -0.7, 'phi': 0.95, 'sigma': 0.25, 'beta': 0.65, 'stationary_variance': 0.6410256410256409}`
- horizon: `30`
- fixture seed: `20260528`

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| decision | `DPF_SV_SMOKE_PASSED` | first stochastic-volatility smoke artifact completed |
| primary criterion status | `pass` | finite rows, schema validation, reproducibility digest, checksum agreement, and loose smoke caps passed |
| veto diagnostic status | `not_triggered` | CPU-only, finite-value, schema, checksum, reference-identity, and boundary vetoes did not fire |
| schema validation | `pass` | `0` errors |
| reproducibility digest | `pass` | `a00f71f0839fe162ce0be3cbb36190ae5472eb743914c4ef6ecfb5f4142cf177` |
| median filtered-mean RMSE cap | `pass` | `0.035854` <= `1.25` |
| median log-likelihood delta cap | `pass` | `0.170559` <= `15.0` |
| CPU-only import discipline | `pass` | `CUDA_VISIBLE_DEVICES=-1` before NumPy import |
| main uncertainty | `single_fixture_smoke_only` | one simulated SV path and one high-particle engineering reference do not establish accuracy or posterior validity |
| next justified action | `experimental_follow_up_plan` | add a reviewed multi-seed/SV-parameter ladder or soft-resampling component smoke under `experiments/dpf_implementation/` |
| not concluded | `strictly_limited` | no production, HMC, posterior, monograph, banking/model-risk, or learned/neural OT claim |

## Reference Row

| Role | Seed | N | Log likelihood | Min ESS | Resampling count |
| --- | ---: | ---: | ---: | ---: | ---: |
| reference | 9901 | 4096 | -23.282639 | 1725.616208 | 3 |

## Candidate Rows

| Seed | N | Log likelihood | Mean RMSE to reference | Loglik delta | Min ESS | Resampling count |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 101 | 256 | -23.453198 | 0.038841 | 0.170559 | 117.174398 | 3 |
| 102 | 256 | -23.290914 | 0.028787 | 0.008275 | 94.964998 | 3 |
| 103 | 256 | -23.533138 | 0.035854 | 0.250499 | 103.409162 | 4 |

## Run Manifest

- command: `python -m experiments.dpf_implementation.runners.run_sv_smoke`
- branch: `main`
- commit: `1bf1f9d7492709182a84478f19bac1dac0d48050`
- dirty state summary: `M docs/main.pdf
 M docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md
 M docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md
 M experiments/controlled_dpf_baseline/README.md
?? .local_sources/
?? docs/plans/bayesfilter-dpf-implementation-dpf0-citation-coverage-register-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf0-claim-extraction-plan-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf0-claim-ledger-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf0-result-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf0a-doc-patch-register-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-ledger-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-plan-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-baseline-plan-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf1-reference-test-contract-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf1-result-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf1-student-comparison-context-register-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf2-bias-proxy-ledger-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf2-component-spec-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf2-deferred-neural-path-register-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf2-differentiable-resampling-plan-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf2-resampling-test-contract-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf2-result-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf3-excluded-flow-risk-register-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf3-kernel-pff-exclusion-check-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf3-particle-flow-pfpf-plan-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf3-result-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf4-differentiable-objective-gradient-contract-plan-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf4-downstream-evidence-requirements-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf4-gradient-contract-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf4-objective-classification-ledger-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf4-result-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf5-benchmark-ladder-matrix-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf5-cpu-gpu-runtime-policy-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf5-result-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf5-seed-uncertainty-policy-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-benchmark-ladder-plan-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-spec-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-api-review-plan-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-decision-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf6-result-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-dpf7-final-audit-implementation-handoff-plan-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-final-audit-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-handoff-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-master-program-2026-05-28.md
?? docs/plans/bayesfilter-dpf-implementation-sv-test-plan-2026-05-28.md
?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-2026-05-27.md
?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-audit-2026-05-27.md
?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-result-2026-05-27.md
?? docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-review-2026-05-27.md
?? experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-final-archive-result.md
?? experiments/dpf_implementation/`
- python: `3.11.14`
- numpy: `2.1.3`
- CPU-only: `True`
- pre-import `CUDA_VISIBLE_DEVICES`: `-1`
- started at UTC: `2026-05-27T20:11:21Z`
- ended at UTC: `2026-05-27T20:11:21Z`
- runtime seconds: `0.063390`
- artifact paths: `['experiments/dpf_implementation/reports/outputs/dpf_sv_smoke_2026-05-28.json', 'experiments/dpf_implementation/reports/dpf-sv-smoke-result-2026-05-28.md']`

## Veto Diagnostics

- CPU-only pre-import assertion passed.
- Candidate and reference rows share model and observation checksums.
- JSON schema/content validation passed.
- Fixed-seed reproducibility digest matched.
- All rows reported finite log-likelihood, filtered mean, and ESS summaries.

## Interpretation

The experimental clean-room bootstrap/SIR particle filter produced finite, schema-valid, reproducible smoke diagnostics on the fixed stochastic-volatility fixture.  Candidate/reference residuals passed only loose smoke sanity caps.

## Red-Team Note

The strongest alternative explanation is that this runner is internally consistent on one small simulated fixture while still being inaccurate, poorly tuned, or unsuitable for posterior inference on other stochastic-volatility settings.

A result that would overturn this smoke pass would be any rerun showing non-finite weights, checksum drift, failed reproducibility, schema failure, or candidate/reference residuals above the declared smoke caps.

## What Is Not Concluded

- No production readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No learned or neural OT promotion is concluded.
- No banking or model-risk claim is concluded.
- No monograph claim is concluded without separate review.
- The high-particle reference is an engineering comparator, not exact truth.

## Review Record

- Claude reviewer command: `claude -p --model claude-opus-4-7 --effort max`
- Iteration 1: `REJECT`.
- Claude blocking findings: the computation, CPU-only discipline, schema/reproducibility gates, model definition, comparator semantics, and proxy discipline were mostly compliant, but the markdown result note still had pending review metadata and did not include all required decision-table fields.
- Codex audit: agreed with Claude.  The defect was documentation/result-note compliance, not the SV smoke computation.
- Patch after iteration 1: expanded the decision table with primary criterion, veto status, main uncertainty, next action, and non-conclusion rows; added an explicit smoke-question answer; recorded iteration-1 review findings.
- Iteration 2: `REJECT`.
- Claude iteration-2 findings: substantive plan compliance, smoke-question answer, CPU-only discipline, schema/reproducibility gates, comparator semantics, proxy discipline, and boundary discipline were compliant, but the review record still left iteration 2 as pending/submitted.
- Codex iteration-2 audit: agreed with Claude.  The defect remained review-record bookkeeping only.
- Patch after iteration 2: recorded iteration 2 as `REJECT` with findings and converted the current-review note into an explicit instruction that the reviewer should judge the current artifact on substance and may authorize a metadata-only final acceptance update.
- Iteration 3: `ACCEPT`.
- Claude iteration-3 findings: no substantive blocker remained; the result note, JSON schema/reproducibility/environment fields, CPU-only discipline, comparator semantics, proxy limits, and boundary discipline are consistent with the approved plan.
- Codex iteration-3 audit: accepted Claude's findings and applied this metadata-only final review update.
- Final review status: accepted.
