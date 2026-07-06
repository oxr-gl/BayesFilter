# P01 LGSSM Exact-Kalman Gate Result

Date: 2026-06-24

Status: `FAIL_STOP_P01_HARD_ROUTE_DIAGNOSTIC_VETO`

## Phase Summary

P01B launched after P01A implementation checks passed and the user approved
trusted-GPU runtime. The initial all-in-one P01B command initialized GPU1 and
logged XLA compilation, but it produced no partial JSON/Markdown artifact after
a long interval and emitted retracing warnings. That attempt was stopped as a
command-pattern defect, not as a candidate result.

P01B was repaired into row-level trusted-GPU artifacts without changing the
candidate, pinned cases, seeds, tolerances, or pass/fail criteria. The repaired
row pattern produced trusted-GPU/TF32/XLA evidence for the small LGSSM exact
reference case.

The low-rank route passed seeds `91001` and `91002`, but failed seed `91003`
on a predeclared hard route diagnostic:

- `factor_marginal_residual_threshold`;
- observed max factor marginal residual: `0.006653338670730591`;
- threshold: `0.005`;
- projection iterations used: `120`, equal to the locked cap.

The same row's Kalman quality metrics were within the loose P01 tolerances, but
the route diagnostic is still a hard screen under the P01 evidence contract.
P01 therefore stops before medium/informative LGSSM cases and before P02.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Stop model-suite promotion run at P01; do not hand off to P02 execution. |
| Primary criterion status | `FAIL`: P01 requires hard finite/provenance/nonmaterialization/route diagnostics and pinned Kalman-error screens; one low-rank row failed the factor residual hard screen. |
| Veto diagnostic status | `ACTIVE`: `lgssm_small_exact_ref:91003:low_rank:factor_marginal_residual_threshold`. |
| Main uncertainty | The failure is a route-diagnostic/tuning residual failure, not a Kalman quality failure on this row. It may be repairable by a reviewed solver/tuning plan, but cannot be waived inside this promotion run after seeing results. |
| Next justified action | Write a repair/blocker plan for the low-rank solver residual or keep low-rank as optional-route-only for model-suite promotion. |
| What is not being concluded | No model-suite recommendation, no broad algorithm rejection, no statistical superiority claim, no posterior correctness claim, no HMC readiness, no package/API/default readiness, and no scientific-validity claim. |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Does the locked low-rank route preserve LGSSM filtering quality against exact Kalman references while retaining route/provenance validity? |
| Baseline/comparator | Exact Kalman for quality; streaming GPU/TF32 route as paired comparator. |
| Primary pass criterion | Low-rank must pass hard finite/provenance/nonmaterialization/route diagnostics and pinned Kalman-error screens across all P01 cases and seeds. |
| Result | `FAIL`: a hard route diagnostic failed before the full P01 ladder completed. |
| Veto diagnostics | Active: factor marginal residual threshold exceeded on low-rank seed `91003`. |
| Artifact | Aggregate JSON/Markdown, row artifacts, logs, this result, execution ledger. |

## Run Artifacts

Aggregate artifacts:

- `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24.json`
- `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24.md`

All-in-one attempt log:

- `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/p01-lgssm-kalman.log`

Trusted-GPU row artifacts:

- `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24-row-lgssm_small_exact_ref-seed91001-streaming.json`
- `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24-row-lgssm_small_exact_ref-seed91001-low_rank.json`
- `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24-unit-lgssm_small_exact_ref-seed91002-both.json`
- `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24-unit-lgssm_small_exact_ref-seed91003-both.json`

## Observed Rows

| Case | Seed | Route | Status | Mean RMSE | Var RMSE | Loglik abs delta | Factor residual | Projection iterations | Vetoes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `lgssm_small_exact_ref` | 91001 | `streaming` | `PASS` | `0.11871645985323664` | `0.24329509510026948` | `1.6849708557128906` | `0.0` | `0` | `[]` |
| `lgssm_small_exact_ref` | 91001 | `low_rank` | `PASS` | `0.12217001485398285` | `0.24310161641213188` | `1.7836189270019531` | `1.4901161193847656e-08` | `23` | `[]` |
| `lgssm_small_exact_ref` | 91002 | `streaming` | `PASS` | `0.07618801517128287` | `0.24296367584811704` | `0.7851638793945312` | `0.0` | `0` | `[]` |
| `lgssm_small_exact_ref` | 91002 | `low_rank` | `PASS` | `0.07568809588464864` | `0.2422572738230752` | `0.7917766571044922` | `1.4901161193847656e-08` | `19` | `[]` |
| `lgssm_small_exact_ref` | 91003 | `streaming` | `PASS` | `0.06622548366293084` | `0.24285652711380687` | `0.8682975769042969` | `0.0` | `0` | `[]` |
| `lgssm_small_exact_ref` | 91003 | `low_rank` | `FAIL` | `0.06638920035056725` | `0.24245469677909753` | `0.8644542694091797` | `0.006653338670730591` | `120` | `['factor_marginal_residual_threshold']` |

## Rows Not Run

- `lgssm_medium_exact_ref`, seeds `91011,91012,91013`, both routes: not run
  because P01 stopped after the earlier hard route diagnostic veto.
- `lgssm_informative_obs_stress`, seeds `91021,91022,91023`, both routes: not
  run because P01 stopped after the earlier hard route diagnostic veto.

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Failed on one low-rank route diagnostic. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Kalman RMSE/log-likelihood differences are descriptive for completed rows; the veto is diagnostic threshold failure, not ranking. |
| Default-readiness | Not supported by P01. |
| Next evidence needed | A reviewed repair/tuning plan for the low-rank projection residual, or a closeout preserving low-rank as optional-route-only for model-suite promotion. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4`; working tree dirty. |
| Commands | Trusted GPU precheck; P01A compile/tests; all-in-one P01B attempt stopped as command-pattern defect; row-level trusted-GPU P01B artifacts. |
| Environment | Local repository environment, `/home/ubuntu/python/BayesFilter`. |
| CPU/GPU status | Trusted GPU1 selected with `CUDA_VISIBLE_DEVICES=1`; row artifacts report GPU outputs and TF32 recorded `True`. |
| Data version | Deterministic LGSSM fixtures generated by P01 harness. |
| Random seeds | Completed: `91001,91002,91003` for small case. Not run: medium/informative seeds due to hard veto. |
| Wall time | See row artifacts/logs. |
| Output artifact paths | Aggregate JSON/Markdown, row JSON/Markdown, logs, this result. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-subplan-2026-06-24.md` |
| Result file | This file. |

## Post-Run Red-Team Note

The strongest alternative explanation is that the locked projection iteration
cap or residual threshold is too strict for one otherwise quality-acceptable
row. That is a repair/tuning question, not a basis to continue the current
promotion run as if P01 passed. The candidate did not fail Kalman quality on
the observed row, but it failed a predeclared hard route diagnostic.

## Handoff

Do not execute P02 under the current promotion run. The safe next options are:

- write a focused repair plan for the low-rank projection residual and rerun
  the P01 gate under reviewed criteria; or
- proceed to P08-style closeout with final status
  `LOW_RANK_LEDH_REPAIR_REQUIRED` or `LOW_RANK_LEDH_OPTIONAL_ROUTE_ONLY`.
