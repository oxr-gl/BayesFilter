# P82 Phase 1 Subplan: Route / Protocol / Harness Inventory

status: DRAFT_PENDING_PHASE0
date: 2026-06-22

## Phase Objective

Inventory the current checkout for the exact Zhao-Cui analytical comparator
route, the LEDH-PFPF-OT harness surfaces, and the regression-FD harness gaps
before any code patch or GPU run.

## Entry Conditions Inherited From Previous Phase

- P0 governance bootstrap passed.
- Master program and runbook are reviewed or accepted.
- P81 corrections are preserved:
  - Zhao-Cui approximate comparator, not oracle;
  - analytical derivative route intended;
  - autodiff/JVP diagnostic-only;
  - regression FD with 13 points, five seeds, N=1000, value-outlier trim;
  - LEDH actual estimate N=10000, five seeds.

## Required Artifacts

- P1 result markdown with inventory output and route classification.
- Updated execution ledger.
- Draft P2 harness subplan.
- Claude review note if material ambiguity remains.

## Required Checks / Tests / Reviews

Run read-only commands:

```bash
rg -n "multistate_nonlinear_fixed_design_tt_score_path|target_derivative_backend|ForwardAccumulator|analytic_gradient|ParameterizedZhaoCuiSIRSSM" bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p81-* docs/plans/bayesfilter-highdim-zhao-cui-p82-*
rg -n "batched-theta|regression-offsets|trim-extreme|slope_standard_error|seed_microbatch|num-particles" docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
rg -n "experimental_batched_ledh_pfpf_ot|streaming_batched_ledh|transport_ad_mode|batch-seeds|num-particles" docs/benchmarks experiments/dpf_implementation/tf_tfp -g '*.py'
git status --short
```

Review P1 result with Claude if the route classification is not trivial.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What exact local paths and gaps must P2/P3 address before LEDH gradient testing can run? |
| Baseline/comparator | Current checkout inventory, not stale conversation. |
| Primary criterion | P1 records comparator route, autodiff/JVP occurrences, harness support/gaps, LEDH surfaces, dirty-worktree constraints, and exact P2 handoff. |
| Veto diagnostics | Treating JVP as primary comparator; missing harness gap; missing dirty-worktree warning; stale P81 claims used as evidence; no exact P2 handoff. |
| Explanatory diagnostics | Search hits and file/path anchors. |
| Not concluded | No route correctness, no code repair, no GPU viability, no gradient validation. |
| Artifact preserving result | P1 result under `docs/plans`. |

## Forbidden Claims / Actions

- Do not edit code in P1.
- Do not run GPU/CUDA commands.
- Do not claim the analytical SIR route is ready unless inventory proves it.
- Do not call Zhao-Cui an oracle.
- Do not use central finite difference as promotion evidence.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- P1 identifies the exact harness changes needed for 13 offsets and
  value-outlier trimming;
- P1 records whether the existing batched-theta and seed microbatch logic can
  be reused;
- P2 subplan exists and names target files/tests;
- any route ambiguity is sent to P3 rather than hidden.

## Stop Conditions

Stop if:

- current checkout lacks the expected benchmark harness or LEDH surfaces;
- inventory shows that the intended comparator route cannot be classified
  without human direction;
- P2 would require broad refactors or unrelated dirty-file rewrites.
