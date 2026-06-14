# P8 Blocker Closure Master Plan

metadata_date: 2026-06-11
status: CODEX_DRAFT_PENDING_2026_06_12_NUMERIC_EXECUTION_UPDATE

## Role Contract

| Role | Agent |
| --- | --- |
| Supervisor and executor | Codex in this dialogue |
| Read-only critical reviewer | Claude Code, opus, max effort |
| Detached Codex agent | Not allowed |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can Phase 8 move from P8a contract/preflight status to the actual P8b reviewed numeric value/score/curvature benchmark for the promoted source-paper filtering rows? |
| Baseline/comparator | Current P8 synthetic-truth contract, source-paper scope contract, generalized-SV specification, P57/P58 spatial-SIR source-route blocker ledgers, and focused tests for the benchmark emitters. |
| Primary promotion criterion | Every promoted source-paper row has accepted truth values, generated synthetic datasets, reviewed evaluator outputs, value and score tables, curvature status, stochastic uncertainty where required, and an explicit pass/block status with no silent holes. |
| Veto diagnostics | P44 diagnostic rows re-enter promoted tables; old LEDH-PFPF-OT results are used as current evidence; old SIR local/operator/all-grid route is promoted as source-route evidence; generalized-SV author defaults or SP500 returns are substituted for the amended synthetic-from-estimates row; DPF filters are ranked before Monte Carlo uncertainty is quantified; score/Hessian coordinate transforms are omitted or mislabeled; preflight/smoke values are treated as performance results. |
| Explanatory-only diagnostics | Runtime, finite-value smoke checks, fixture-level adapters, UKF scout values, lower-rung SIR rows, and single-seed DPF outputs. |
| Not concluded even if this plan passes | Bayesian-estimation readiness, exact nonlinear likelihood correctness, universal DPF gradient validity, or superiority of a filter outside the promoted benchmark ladder. |
| Result artifact | Existing 2026-06-11 blocker artifacts plus a required 2026-06-12 numeric-execution update before launch; P8b must emit JSON/CSV/Markdown benchmark artifacts and a reviewed result note. |

## Skeptical Plan Audit

Initial audit status: `CODEX_P8_BLOCKER_CLOSURE_PLAN_AUDIT_PASS_PENDING_CLAUDE`.

The plan explicitly rejects the failure modes that caused prior confusion:

- Wrong baseline: source-paper rows supersede BayesFilter-only P44 diagnostic rows.
- Proxy promotion: preflight, smoke, UKF scout, lower-rung SIR, and old local/operator/all-grid routes cannot retire numeric blockers.
- Missing stop conditions: each phase has a pass token and a block token; only source-grounding gaps, missing estimated values, failed validators, failed Claude review, or unavailable runtime resources may stop a phase.
- Unfair comparison: all filters are attempted on the same generated datasets when the target contract permits it; Kalman is exact only for LGSSM and otherwise must be labeled structured not-applicable or declared surrogate.
- Hidden assumptions: score and Hessian results must state coordinate system and provenance.
- Stale context: this 2026-06-11 draft predates later P59-9b through P59-9e SIR execution-only evidence and the generalized-SV prior-mean amendment.  Before launch, P8b must refresh the active P8 manifests so stale source-row blocks cannot mask the true remaining numeric-run blocker.
- Artifact adequacy: a phase does not pass unless it writes machine-readable artifacts and focused tests/validation output.

## Blocker Inventory

| Blocker ID | Current evidence | Repair objective | Pass token | Block token |
| --- | --- | --- | --- | --- |
| P8-B1 truth values | Source-paper scope contract has LGSSM, SV, KSC, SIR, predator-prey values; generalized SV is amended to the Zhao-Cui S&P prior-center synthetic row. | Refresh manifests so the old generalized-SV estimated-values blocker is retired and source values/test points are recorded with provenance. | `PASS_P8_B1_SOURCE_TRUTH_MANIFEST` | `BLOCK_P8_B1_SOURCE_TRUTH_MANIFEST` |
| P8-B2 data generation | P8 dataset manifest reports generated datasets for the promoted rows, including generalized SV prior-mean. | Verify generated dataset hashes and row coverage before P8b launch. | `PASS_P8_B2_SYNTHETIC_DATASETS` | `BLOCK_P8_B2_DATA_GENERATOR_VALIDATION` |
| P8-B3 horizon calibration | T/R ladder exists but is pending. | Run or emit reviewed calibration protocol using source-paper horizons plus optional long-horizon stability ladder. | `PASS_P8_B3_HORIZON_CALIBRATION` | `BLOCK_P8_B3_HORIZON_CALIBRATION` |
| P8-B4 stochastic seed calibration | DPF seed ladder exists but is pending. | Quantify DPF Monte Carlo uncertainty and require `MC_SE <= 0.25 * data_SE` before ranking small differences. | `PASS_P8_B4_STOCHASTIC_SEED_CALIBRATION` | `BLOCK_P8_B4_STOCHASTIC_SEED_CALIBRATION` |
| P8-B5 source evaluators/adapters | 25 adapter-required cells; many value-only or unexposed gradient cells. | Implement target/evaluator adapters and label score/Hessian provenance honestly. | `PASS_P8_B5_EVALUATOR_ADAPTERS` | `BLOCK_P8_B5_EVALUATOR_ADAPTERS` |
| P8-B6 spatial SIR d=18 source route | Later P59-9b, P59-9c, P59-9d, and P59-9e artifacts pass at execution-only tier; active P8 manifests are stale if they still say only P59-9a passed. | Retire the stale row-level hard block in P8 manifests and carry the honest status `PASS_P59_9E_D18_EXECUTION_ONLY` with nonclaims: no accuracy, rank convergence, same-target correctness, d=50/d=100 scaling, HMC readiness, adaptive parity, or UKF correctness. | `PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED` | `BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE` |
| P8-B7 numeric benchmark runner | Reviewed evaluator outputs absent. | Run promoted rows across all algorithms, preserving failures, N/A-by-target, value, componentwise score, curvature, and uncertainty tables. | `PASS_P8_B7_NUMERIC_BENCHMARK_RUNNER` | `BLOCK_P8_B7_NUMERIC_BENCHMARK_RUNNER` |
| P8-B8 closeout review | No numeric execution review yet. | Claude read-only review loop until convergence or five iterations; revise until pass or record real blocker. | `PASS_P8_B8_REVIEWED_CLOSEOUT` | `BLOCK_P8_B8_REVIEWED_CLOSEOUT` |

## Execution Phases

### Phase P8-B1: Source Truth And Generalized-SV Gate

1. Emit a source-truth manifest for LGSSM, SV actual, SV KSC surrogate, spatial SIR J=9 d=18, and predator-prey from checked Zhao--Cui source-paper/code values.
2. For generalized SV, search local paper/code/artifacts for checked estimated values.
3. If values are found, materialize both physical and transformed coordinates with source anchors.
4. If values are not found, keep only the generalized-SV row blocked and allow other rows to proceed.

### Phase P8-B2: Synthetic Data Generators

1. Implement or bind TensorFlow/TFP generators for source-paper rows.
2. Generate reproducible synthetic data from the accepted truth values.
3. Record seeds, horizon, model row ID, data replicate ID, and artifact path.
4. Do not use SP500 returns as generalized-SV benchmark data.

### Phase P8-B3: Horizon Calibration

1. For each model family, report source-paper horizon results and optional long-horizon stability diagnostics.
2. Estimate long-run variance for average likelihood and score using HAC/Newey-West or batch means where applicable.
3. Do not require nonlinear exact likelihood references.

### Phase P8-B4: Stochastic Filter Calibration

1. Run DPF seed ladders `S in {4, 8, 16, 32}`.
2. Report data standard error, particle Monte Carlo standard error, ESS, resampling count, and degeneracy flags.
3. Prevent ranking of small differences when Monte Carlo uncertainty dominates.

### Phase P8-B5: Evaluator And Adapter Closure

1. Implement value adapters first for all algorithm/model cells that are target-compatible.
2. Implement score adapters only when coordinate provenance can be certified.
3. Mark gradient/Hessian cells as value-only, diagnostic-only, or blocked with reason when certification is missing.
4. Add focused tests that the status matrix has no silent holes.

### Phase P8-B6: Spatial SIR d=18 Source Route Recognition

This phase consumes the later P58/P59 evidence rather than rerunning stale
source-route work:

- P59-9b step-spec assembly: `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY`;
- P59-9c route decision: `PASS_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION`;
- P59-9d runner/manifest path: `PASS_P59_9D_RUNNER_MANIFEST_PATH`;
- P59-9e validation ladder: `PASS_P59_9E_D18_EXECUTION_ONLY`.

The P8 manifest must recognize this as execution-only readiness and must not
convert it into accuracy, rank-convergence, correctness, scaling, HMC, adaptive
parity, or UKF-correctness evidence.  The old local/operator/all-grid route is
still forbidden as performance evidence.

### Phase P8-B7: Numeric Runner And Tables

1. Run the promoted source-paper benchmark ladder.
2. Emit value tables with average log likelihood and uncertainty.
3. Emit score tables with norm, max component, min component, and componentwise standardized means.
4. Emit curvature tables where full Hessian provenance is available; otherwise preserve status.
5. Emit failure and not-applicable tables.

### Phase P8-B8: Read-Only Review And Closeout

1. Ask Claude opus max effort to review the execution artifacts.
2. Iterate repairs until Claude says pass/converged or five review loops have run.
3. Close with a result file that states what passed, what remains blocked, and what cannot be concluded.

## Claude Review Loop Protocol

For both plan review and execution review:

1. Send bounded prompt with artifact paths and exact review questions.
2. If Claude does not respond, run a small probe.
3. If the probe responds, redesign the prompt and retry.
4. If Claude identifies material blockers, revise artifacts or code and rerun focused validations.
5. Stop after convergence or five iterations, recording each iteration in the result file.

## Commands And Validation Surface

Initial focused validations:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_generalized_sv_spec.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_generalized_sv_spec.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py tests/highdim/test_p58_m9_source_route_pipeline_readiness.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py scripts/filtering_value_gradient_benchmark_emit_generalized_sv_spec.py scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-master-plan-2026-06-11.md scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py scripts/filtering_value_gradient_benchmark_emit_generalized_sv_spec.py scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_generalized_sv_spec.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py tests/highdim/test_p58_m9_source_route_pipeline_readiness.py
```

## Approval Assumptions

- Claude Code usage is required for read-only review and must run with escalated/trusted permissions.
- CPU-only schema/tests hide CUDA intentionally with `CUDA_VISIBLE_DEVICES=-1`.
- Any future GPU benchmark or TensorFlow GPU probe must request escalated/trusted permissions.

## Nonclaims

- This plan is not itself a numeric benchmark result.
- P8a contract/preflight completion is not Phase 8 completion.
- This plan does not rank filters.
- This plan does not certify DPF gradients.
- This plan does not claim SIR d=18 source-route accuracy; the current recognized target is execution-only readiness.
- This plan does not claim generalized-SV numeric performance; the current recognized target is prior-center synthetic-row readiness.

## 2026-06-12 Patch Required Before Launch

Before executing P8b, patch and regenerate the active P8 gate/status artifacts
so they reflect the latest source-row state:

1. Retire stale `BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE` when the P59-9b
   through P59-9e pass artifacts are present.
2. Preserve `PASS_P59_9E_D18_EXECUTION_ONLY` and its nonclaims in the P8 row
   status instead of treating SIR as a performance result.
3. Preserve generalized-SV prior-center readiness and dataset hashes.
4. Keep `BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN` and
   `BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING` until P8b
   actually emits reviewed value, componentwise score, curvature/status,
   failure, and stochastic uncertainty tables.
