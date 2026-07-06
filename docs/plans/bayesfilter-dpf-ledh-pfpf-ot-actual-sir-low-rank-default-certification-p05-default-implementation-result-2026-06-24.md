# P05 Default-Route Implementation And Focused Tests Result

Date: 2026-06-24

Status: `PASS_P05_READY_FOR_P06_SKIP_OR_APPROVAL`

## Phase Objective

Make the locked low-rank route the bounded default-certification route for the
actual-SIR d18 GPU/TF32 LEDH-PFPF-OT validation lane, while preserving explicit
streaming comparator/fallback access and all nonclaims.

P05 did not change BayesFilter public exports, package-level defaults,
dependencies, model files, HMC behavior, or scientific claims.

## Entry Conditions

- P00 through P04 passed.
- P04 passed the N4096 resource-boundary gate for
  `r16_eps0p25_alpha1em08_it120`.
- P05 subplan was refreshed after P04 and reviewed with Claude Opus/max.
- Claude review round 1 returned `VERDICT: REVISE`; the issues were fixed.
- Claude review round 2 returned `VERDICT: AGREE`.
- P05 execution stayed inside the reviewed write set.

## Skeptical Pre-Implementation Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: streaming remains explicit as `--route streaming`, and paired comparator mode remains explicit as `--route both`. |
| Proxy metric promoted | Guarded: P05 does not use P03/P04 timing as statistical superiority or posterior evidence. |
| Missing stop conditions | Guarded by exact write set, focused tests, no-NumPy scan, metadata scan, and boundary nonclaims. |
| Unfair comparison | Guarded: P05 does not create new benchmark comparisons. |
| Hidden assumptions | Guarded: package-level/public API/broad product/HMC/scientific boundaries remain nonclaims. |
| Stale context | Guarded: P05 was refreshed after P04 and after default-surface discovery. |
| Environment mismatch | Guarded: focused tests were CPU-hidden/unit tests; no new GPU runtime evidence is claimed. |
| Artifact mismatch | Guarded: this result names exact changed files, tests, and next-phase handoff. |

Audit conclusion: the scoped P05 implementation was valid because it was
bounded to the reviewed actual-SIR validation/reporting surface and did not
cross public API, package-level default, broad product, HMC, model-file,
dependency, or scientific-claim boundaries.

## Changes Made

Changed files:

- `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
- `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
- `tests/test_actual_sir_low_rank_route_validation.py`
- `tests/test_actual_sir_low_rank_tuning_grid.py`

Behavioral scope:

- The direct actual-SIR route-validation harness now defaults to
  `--route low_rank`.
- The direct harness low-rank defaults are locked to:
  - rank `16`;
  - assignment epsilon `0.25`;
  - alpha `1e-8`;
  - max projection iterations `120`;
  - convergence threshold `1e-6`;
  - denominator floor `1e-30`.
- The grid wrapper now points `PLAN_PATH` at the current default-certification
  master program.
- The grid wrapper default candidate grid now enumerates the locked candidate
  only by default: `r16_eps0p25_alpha1em08_it120`.
- The grid wrapper still defaults to `--route both` so paired streaming versus
  low-rank comparison remains the default aggregate/grid mode.
- The direct harness still accepts `--route streaming` and `--route both`.
- Nonclaim wording was tightened from legacy "production/default" wording to
  package-level and broad-production nonclaims.

## Evidence Contract

- Question: can the locked low-rank route be wired as the bounded
  default-certification route for the actual-SIR d18 GPU/TF32 LEDH-PFPF-OT
  validation lane without violating implementation, comparator, no-NumPy, API,
  or claim boundaries?
- Baseline/comparator: current streaming GPU/TF32 route remains explicitly
  selectable.
- Primary pass criterion: scoped changes pass focused tests, select the locked
  candidate by default in the validation/reporting surface, preserve explicit
  streaming and paired comparator modes, avoid NumPy in the active
  BayesFilter-owned implementation path, update stale metadata, and record exact
  changed-file provenance.
- Veto diagnostics: unscoped code change, public API/package/model/dependency
  change, NumPy implementation path, missing streaming comparator/fallback,
  failed tests, unsupported HMC/scientific/default-readiness claim.
- Explanatory diagnostics: focused tests, metadata scan, no-NumPy scan, and
  warning counts.
- Not concluded: posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, statistical superiority, public API readiness, package-level
  default readiness, broad production readiness, scientific validity, or formal
  memory scaling.

## Required Checks

- Syntax check:

```bash
python -m py_compile docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py
```

Result: passed.

- Focused tests:

```bash
python -m pytest tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q
```

Result: passed, `26 passed`.

Warnings: TensorFlow Probability/gast Python deprecation warnings only.

- Stale metadata scan over edited active surface:

```bash
rg -n "actual-sir-low-rank-validation-master-program-2026-06-21|actual-sir-low-rank-tuning-master-program-2026-06-22|no production/default readiness claim|no public API/default readiness claim" docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py
```

Result: passed, no hits.

- Active solver no-NumPy scan:

```bash
rg -n "import numpy|np\.|\.numpy\(" experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py
```

Result: passed, no hits.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P05 passes the bounded validation/reporting default-surface implementation gate |
| Primary criterion status | Passed: focused code changes lock the validation/reporting defaults to the P03/P04 candidate, preserve streaming and paired comparator routes, update plan metadata, and pass tests |
| Veto diagnostic status | No unscoped write, public API/package/model/dependency change, active-path NumPy, missing fallback, failed test, or unsupported HMC/scientific/broad-default claim was found |
| Main uncertainty | P05 is a scoped harness/runner default-certification surface change, not a package-level default switch or posterior/HMC/scientific proof |
| Next justified action | Write a skipped/nonclaim P06 result unless the user separately approves HMC/autodiff mechanics, then proceed to P07 closeout |
| What is not being concluded | No posterior correctness, HMC readiness, dense Sinkhorn equivalence, statistical superiority, public API readiness, package-level default readiness, broad production readiness, scientific validity, or formal memory scaling |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the scoped P05 implementation/test gate |
| Statistically supported ranking | None |
| Descriptive-only differences | P03/P04 timing remains descriptive only; P05 adds no new runtime comparison |
| Default-readiness | Bounded validation/reporting default-certification surface passes; package-level/public/broad default readiness remains nonclaimed |
| Next evidence needed | P06 skipped/nonclaim or separately approved HMC mechanics; P07 documentation-only final closeout review |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-subplan-2026-06-24.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-result-2026-06-24.md` |
| Commands | Syntax check; focused pytest; stale metadata scan; active solver no-NumPy scan |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, local repository environment |
| CPU/GPU status | Focused tests intentionally use CPU-hidden test setup where applicable; no new trusted GPU runtime was run in P05 |
| Data version | Synthetic actual-SIR d18 harness; no external data |
| Random seeds | Unit/smoke tests use existing small fixtures, including seed `81120`; no new benchmark seeds |
| Wall time | Focused pytest completed in about 23 seconds |
| Output artifact paths | This result, updated code/tests, refreshed P06/P07 subplans and ledgers |

## Post-Run Red-Team Note

The strongest alternative explanation is that P05 improves default-certification
metadata and CLI defaults for the validation lane, not the algorithm itself.
That is exactly the intended scope: algorithmic runtime evidence comes from
P03/P04, while P05 only wires the validated candidate into the owned
validation/reporting surface. The weakest part of the evidence remains that
P05 does not add posterior correctness, HMC readiness, dense equivalence, or a
statistical ranking.

## Next-Phase Handoff

P06 remains optional. Because P05 did not claim HMC/autodiff readiness and no
separate HMC approval has been granted, the next bounded action is to write a
P06 skipped/nonclaim result and refresh P07 for a documentation-only final
closeout.
