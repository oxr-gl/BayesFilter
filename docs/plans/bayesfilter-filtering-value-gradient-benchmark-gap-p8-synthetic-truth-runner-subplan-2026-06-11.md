# P8a Subplan: Synthetic-Truth Benchmark Contract Preflight

metadata_date: 2026-06-11
phase: FILTER_BENCH_P8A_CONTRACT_PREFLIGHT
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only
supersedes: docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-subplan-2026-06-10.md

## Objective

Rewrite the Phase 8 preflight around the reviewed synthetic-truth
likelihood-geometry benchmark instead of the obsolete "oracle error matrix
everywhere" benchmark.  This subplan is P8a, not the numeric Phase 8 run.  P8a
must produce an executable benchmark contract artifact for the frozen P7 roster
and must prevent status, smoke, or preflight fixtures from being promoted into
performance evidence.

The revised P8 does not claim that nonlinear exact likelihood oracles exist.
It turns P8a into the gate that freezes the synthetic-truth measurement design,
tuple-level capability crosswalk, derivative provenance requirements,
stochastic uncertainty requirements, and performance table schemas needed
before the P8b full numeric benchmark run can be trusted.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P8a convert the frozen P7 all-filter/all-model roster into a synthetic-truth benchmark contract with no silent holes and no oracle-overclaim? |
| Baseline/comparator | `docs/plans/bayesfilter-synthetic-truth-filter-benchmark-methodology-proposal-2026-06-11.md`, the P7 preflight roster, P6 gradient semantics, and the old P8 blocked result. |
| Primary criterion | P8a emits a structured synthetic-truth benchmark artifact that preserves all 7 x 12 current cells, supplies the required row/algorithm capability crosswalk and derivative provenance fields, declares truth-prior/data/horizon/MC calibration requirements, and labels numeric performance as pending unless measured by a reviewed evaluator. |
| Veto diagnostics | Old `LEDH-PFPF-OT` used as current evidence; smoke/preflight values used as performance evidence; nonlinear exact references invented; missing canonical `phi` coordinate policy; missing score/Hessian provenance fields; DPF Monte Carlo uncertainty omitted; curvature based only on eigenvalues of an averaged Hessian; changing thresholds after seeing results. |
| Explanatory diagnostics | P7 coverage states, current adapter gaps, future horizon calibration fields, future stochastic seed-ladder fields, and exact LGSSM reference hooks. |
| Not concluded | P8a contract emission does not rank filters, does not complete the full numeric benchmark, does not certify DPF gradients, and does not establish Bayesian-estimation readiness. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json` plus CSV/Markdown summary tables and a P8 result note. |

## Skeptical Plan Audit

Status: PASSED_FOR_CONTRACT_IMPLEMENTATION.

- Wrong baseline risk: exact Kalman remains an LGSSM row property only.
  Nonlinear rows use synthetic-truth likelihood geometry, not fake exact
  likelihood errors.
- Proxy promotion risk: the script must carry P7 and smoke information only as
  engineering diagnostics.  Any performance field must be null or explicitly
  `pending_numeric_execution` unless a reviewed evaluator produced it.
- Missing stop-condition risk: P8 blocks numeric closeout if accepted truth
  draws, synthetic datasets, horizon calibration, or stochastic seed
  calibration are missing.  This is a deliberate P8a stop condition; it is not
  a P8 closeout pass.
- Unfair-comparison risk: all future algorithms must share the same truth draw
  ids, synthetic dataset ids, horizons, parameter coordinates, and sign
  conventions.
- Hidden-assumption risk: every tuple must state score coordinate system,
  score derivative provenance, Hessian coordinate/provenance or reason, and
  diagnostic-only or not-available reason.
- Stale-context risk: old `LEDH-PFPF-OT` remains historical-only and old P8
  value/gradient error matrices remain superseded status artifacts.
- Environment-mismatch risk: this P8 contract run is CPU-only metadata/schema
  validation.  GPU or full TensorFlow benchmark runs require a later trusted
  manifest.
- Artifact-answer risk: the output must answer whether the benchmark design is
  ready for numeric execution; it must not masquerade as the P8b numeric
  benchmark result.

## Required Implementation

1. Add `scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py`.
   The script reads the P1 registry, P6 gradient semantics, P7 preflight
   matrix, and reviewed synthetic-truth methodology proposal.

2. Emit
   `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json`
   with schema version `filter_bench.synthetic_truth_p8.v1`.

3. Preserve the frozen P7 roster:
   seven current algorithm ids by twelve model columns, with
   `ledh_pfpf_ot_historical` excluded from current evidence.

4. Emit a design-level capability crosswalk for every current
   `(algorithm_id, model_row_id)` pair.  Each cell must contain:

   ```text
   capability_status
   score_coordinate_system
   score_derivative_provenance
   hessian_coordinate_system_or_reason
   hessian_derivative_provenance_or_gap
   diagnostic_only_reason
   not_available_reason
   current_performance_status
   ```

   The crosswalk must also freeze the future accepted-draw tuple manifest
   schema.  Once accepted truth draws exist, every
   `(model_row_id, truth_draw_id, algorithm_id)` tuple must include the same
   fields above plus `truth_prior_lane`, `accepted_draw_status`,
   `truth_coordinate_system`, `data_replicate_ids`, `filter_seed_ids`,
   `branch_veto_status`, `failure_status`, and
   `performance_table_admission_status`.  When no accepted truth draws have
   been generated yet, P8a must explicitly mark tuple-level emission as
   `pending_accepted_truth_draws` and forbid treating design-level cells as
   performance evidence.

5. Enforce canonical benchmark-coordinate derivative semantics.  The main
   score and Hessian tables are in canonical unconstrained `phi` coordinates.
   If an evaluator produces physical-coordinate derivatives, the score is
   admissible only after the chain-rule conversion
   `g_phi = J_tau(phi)^T g_theta`.  Hessian cells are admissible only when the
   full transform is reviewed:

   ```text
   H_phi = J_tau^T H_theta J_tau
           + sum_k g_theta,k Hessian_phi tau_k.
   ```

   Partial Hessian transforms such as `J_tau^T H_theta J_tau` without the
   second transform term are diagnostic-only.  Missing or unreviewed transform
   terms must be reported as `not_available_transform_gap`, not as failed
   curvature and not as a valid Hessian.

   Allowed score provenance/status values:

   ```text
   native_phi_autodiff
   native_phi_analytic
   physical_theta_chain_rule_converted_to_phi
   fixed_branch_diagnostic_only
   physical_theta_unconverted_diagnostic_only
   algorithm_gradient_not_exposed
   adapter_required_pending
   unsupported_by_target
   blocked_value_route
   no_theta_gradient_dim0
   not_available_transform_gap
   ```

   Allowed Hessian provenance/status values:

   ```text
   native_phi_hessian_autodiff
   native_phi_hessian_analytic
   full_chain_rule_hessian_transform
   partial_transform_diagnostic_only
   hessian_not_exposed
   adapter_required_pending
   unsupported_by_target
   blocked_value_route
   no_theta_gradient_dim0
   not_available_transform_gap
   ```

6. Emit benchmark table schemas for:

   - value: mean average log likelihood, SE, failure rate;
   - score: mean score norm, max/min component, max standardized component;
   - componentwise score: signed mean score, SE, confidence interval,
     standardized mean, coordinate name, and coordinate provenance;
   - curvature: replicate-level `lambda_min(-H)`, positive-definite fraction,
     and sign convention;
   - stochastic filters: data SE, particle MC SE, seed ladder status, ESS and
     resampling diagnostics;
   - LGSSM exact reference: exact value, score, and Hessian errors where
     reviewed evaluators exist.

   The componentwise score artifact is mandatory.  Aggregate score norm and
   extrema tables cannot substitute for it, because they can hide
   coordinate-specific signed bias.

7. Emit CSV and Markdown summary tables whose cells are status/provenance
   fields, not numeric performance claims.

8. Add focused tests validating:

   - schema and status;
   - no silent 7 x 12 holes;
   - canonical `phi` coordinate and derivative-provenance fields;
   - chain-rule score and full Hessian-transform statuses are enforced,
     including `not_available_transform_gap`;
   - componentwise score artifact schema is present;
   - old `LEDH-PFPF-OT` is historical-only;
   - smoke/preflight values are not promoted;
   - DPF rows require MC uncertainty before ranking;
   - full numeric benchmark remains pending unless accepted truth draws and
     reviewed evaluator outputs exist.

9. Write/update a P8a result artifact with a decision table and run manifest.

10. Ask Claude for execution review.  Stop early on `VERDICT: AGREE` or after
   five iterations.  If Claude identifies a material flaw, repair and resubmit.

## Pass And Block Tokens

P8a may pass the revised contract gate with:

```text
PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT
```

only if the synthetic-truth runner contract is emitted, validated, and reviewed
with no silent holes or proxy performance claims.

P8a must block the full numeric benchmark and downstream filtering closeout
with:

```text
BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING
```

if accepted truth draws, synthetic datasets, horizon calibration, stochastic
seed calibration, or reviewed evaluator outputs are still missing.  This block
does not invalidate the contract artifact; it prevents treating the contract as
the completed performance benchmark.  Phase 8 remains open until P8b executes
the reviewed numeric value, componentwise score, curvature/status, failure, and
stochastic uncertainty tables.

## Validation Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json >/dev/null
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py
git diff --check -- scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-subplan-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-result-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.md
```

## Claude Review Rule

Claude reviews are read-only and must return:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
MAJOR:
- ...
MINOR:
- ...
```

If Claude does not respond, run a small probe.  If the probe responds, shorten
or split the prompt and retry.
