# Low-Rank LEDH/PFPF-OT Filter Integration Scale Master Program

Date: 2026-06-20

Status: `DRAFT_REVIEW_REQUIRED`

## Purpose

This program tests whether the tuned low-rank coupling solver route can survive
inside an actual LEDH/PFPF-OT filter-shaped TensorFlow loop at particle counts
that motivate the scalable-OT work.  The prior low-rank component lane only
validated the resampler on frozen particle clouds; it did not validate the
route inside the LEDH flow, log-density correction, ESS, and repeated
resampling loop.

Codex in this conversation is the supervisor and executor.  Claude is a
read-only reviewer only.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the tuned low-rank coupling route produce finite, nonmaterialized, factor-diagnostic-valid outputs when embedded in an LEDH/PFPF-OT filter-shaped loop at medium CPU scale and trusted GPU scale up to 50k particles, with a conditional 100k attempt? |
| Mechanism under test | `P = Q diag(1/g) R^T` lazy low-rank coupling solver-route resampling after LEDH flow and likelihood correction. |
| Baseline/comparator | The comparator for integration mechanics is the existing LEDH/PFPF-OT value recursion shape contract and LGSSM fixture. Dense Sinkhorn is not a scale comparator for 50k/100k. Component-lane tuned setting `rank=64`, `assignment_epsilon=0.015625` is a seed configuration, not a proof. |
| Promotion criterion | All required active-resampling phase rows prove that the low-rank solver route actually fired inside the filter loop and pass hard finite/nonnegative/factor-residual/log-weight/no-dense-materialization checks. |
| Promotion veto | Crash/OOM, nonfinite outputs, negative factors, nonpositive `g`, low-rank resampling invocation count missing or zero for active rows, invocation count not equal to the active fixed-resampling mask count, factor residual above the fixed threshold table below, induced row/column residual above the fixed threshold table below, missing required artifact, dense transport matrix materialized in scale phases, shared contract/public export edit, or unsupported claim. |
| Continuation veto | Broken harness invariant, missing route-execution evidence, missing required code artifact, inability to run CPU smoke, need for shared contract/public API/default change, network/package/POT/external solver requirement, or trusted GPU unavailable for GPU phase after the CPU phases have passed. |
| Repair trigger | Tuning-grid failure without harness invalidity triggers at most two focused tuning reruns; shape mismatch or artifact-schema failure triggers implementation repair; GPU-only resource failure triggers smaller trusted GPU preflight before scale. |
| Explanatory diagnostics | Runtime, memory, TF32 status, ESS, moment deltas, selected rank, and selected assignment epsilon. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or TF32-help claim. |

## Source And Implementation Boundaries

Owned files for this program:

- `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py`
- `tests/test_low_rank_ledh_pfpf_integration_smoke.py`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-*.json`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-*.md`
- `docs/benchmarks/logs/low-rank-ledh-pfpf-integration-*.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-*.md`

Read-only source anchors:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_lgssm_scale.py`
- `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py`

Forbidden edits:

- shared ledger or shared stop handoff;
- Phase 1 baseline or Phase 3 schema artifacts;
- Agent A Nystrom artifacts;
- positive-feature Sinkhorn lane intermediate artifacts;
- BayesFilter public exports/defaults/package metadata;
- low-rank component-lane closed result artifacts except as read-only source
  context.

## Fixed Diagnostic Thresholds

These thresholds are fixed before implementation and are the single source for
phase hard diagnostics.  They may not be widened after seeing results.

| Diagnostic | Threshold | Role |
| --- | ---: | --- |
| `low_rank_resampling_invocations` for active rows | `> 0` | hard veto if not met |
| `low_rank_resampling_invocations == active_resampling_mask_count` | exact equality | hard veto if not met |
| `max_factor_marginal_residual` | `<= 5.0e-3` | hard veto |
| `max_induced_row_residual` | `<= 5.0e-3` | hard veto |
| `max_induced_column_residual` | `<= 5.0e-3` | hard veto |
| `output_log_weight_normalization_residual` | `<= 1.0e-6` | hard veto |
| `tiny_materialized_apply_parity` | `<= 1.0e-10` | hard veto only for P01 tiny invariant rows |
| `finite_log_likelihood` | `true` | hard veto |
| `finite_filtered_means` | `true` | hard veto |
| `finite_filtered_variances` | `true` | hard veto |
| `finite_ess_by_time` | `true` | hard veto |
| `transport_matrix_shape` in scale rows | `[B, 0, 0]` | hard veto if dense matrix materialized |
| Runtime, memory, ESS values, moment deltas, TF32 status | not thresholded | explanatory only unless crash/OOM/nonfinite |

## Phase Index

| Phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| P00 | Governance, source intake, and plan review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p00-governance-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p00-governance-result-2026-06-20.md` |
| P01 | Harness implementation and small CPU invariants | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p01-harness-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p01-harness-result-2026-06-20.md` |
| P02 | CPU tuning grid and focused repair loop | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p02-tuning-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p02-tuning-result-2026-06-20.md` |
| P03 | Medium CPU filter-scale validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p03-medium-cpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p03-medium-cpu-result-2026-06-20.md` |
| P04 | Trusted GPU 50k/100k scale ladder | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p04-trusted-gpu-scale-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p04-trusted-gpu-scale-result-2026-06-20.md` |
| P05 | Final closeout and non-claim audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p05-closeout-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-result-2026-06-20.md` |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Lane-owned benchmark harness instead of public API edit | User lane rules and repo governance | Tests actual filter mechanics without changing defaults or shared contracts | Harness may drift from value recursion | Small no-resampling parity and source review | planned |
| Start from `rank=64`, `assignment_epsilon=0.015625` | Closed low-rank component lane | Seed tuning only; not accepted as filter-scale proof | Component tuning may not transfer to filter loop | P02 actual filter tuning grid | planned |
| Runtime/memory explanatory only | Evidence discipline | No fair speed comparison is in scope | Proxy metric becomes promotion criterion | Plan and result non-claim checks | planned |
| Dense Sinkhorn not attempted at 50k/100k | Scalable-OT objective and memory reality | Dense materialization is the failure mode being avoided | Missing comparator misread as superiority | Explicit comparator boundary | planned |
| Trusted GPU only for GPU evidence | AGENTS.md GPU policy | Sandbox GPU failures are not dispositive | False negative due sandbox | Escalated GPU phase or blocker | planned |

## Skeptical Plan Audit

Pre-execution audit target: `PENDING`.

Required audit checks before each phase:

- wrong baseline;
- proxy metrics treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If a material issue appears, the phase must be repaired before execution.

## Review Loop

Claude review is path-only and read-only.  Claude cannot authorize crossing
human, runtime, model-file, funding, product-capability, public API/default, or
scientific-claim boundaries.

For material plan or result defects:

1. patch the same artifact visibly;
2. rerun focused local checks;
3. request another path-only Claude review;
4. stop after five rounds for the same blocker and write a blocker result.

## Program Exit States

- `LOW_RANK_FILTER_INTEGRATION_SCALE_PASSED_DIAGNOSTIC_ONLY`
- `LOW_RANK_FILTER_INTEGRATION_SCALE_FAILED_TUNING_OR_VALIDITY`
- `LOW_RANK_FILTER_INTEGRATION_SCALE_BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`
- `LOW_RANK_FILTER_INTEGRATION_SCALE_BLOCKED_TRUSTED_GPU_UNAVAILABLE`
- `LOW_RANK_FILTER_INTEGRATION_SCALE_BLOCKED_REVIEW_NONCONVERGENCE`
