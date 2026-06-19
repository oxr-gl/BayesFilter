# P71 Master Program: Full SIR d=18 Validation Ladder

metadata_date: 2026-06-16
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
executor: Codex in the current conversation
reviewer: Claude Opus max effort, read-only and bounded

## Objective

Create the gated program needed to fully test the Zhao-Cui spatial SIR d=18
route before any higher-dimensional, scaling, or HMC-readiness claim is made.

P71 is a validation lane, not a monograph rewrite and not an adaptive
Zhao-Cui reproduction lane.  It tests the fixed-HMC-adaptation route only after
the current P70 condition-number blocker is captured or repaired.  The program
must keep separate:

- execution-only readiness;
- finite numeric value/evaluator readiness;
- same-route rank and degree stability;
- d18 filtering accuracy against a reviewed reference/comparator;
- five-seed robustness and runtime/memory evidence;
- value-gradient and HMC diagnostic readiness.

## Starting State

Known local evidence at launch:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-status-2026-06-11.csv`
  records `P8-B6` as
  `PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED`, with numeric
  evaluator execution, accuracy, rank, and scaling still pending.
- `bayesfilter/highdim/source_route.py` records
  `P59_9E_D18_EXECUTION_ONLY_PASS_STATUS` and explicitly blocks higher tiers:
  `d18_same_route_rank_convergence`, `d18_correctness_candidate`, `d50`, and
  `d100`.
- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-result-2026-06-16.md`
  says the repaired fixed fitting machinery exists and passed focused
  CPU-only unit tests, but does not show that the original diagnostic bug is
  fixed.
- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-result-2026-06-16.md`
  records a first-row `CONDITION_NUMBER_VETO`.  Therefore a full d18
  validation run is not yet authorized.  That artifact was recorded at git
  commit `5fdd0819ce0eb2994fb0509e66d9e9cce5f2d47c` with a dirty worktree; P71
  Phase 0 must reconcile current code/worktree drift before treating the
  blocker as still applicable.

## Source-Governance Boundary

Every material phase must classify behavior as exactly one of:

- `source_faithful`: matches cited Zhao-Cui paper operations and cited author
  source operations;
- `fixed_hmc_adaptation`: preserves the author's broad sequential TT/SIRT
  route while freezing randomness, branches, ranks, samples, schedules,
  thresholds, and diagnostics so the branch defines a reproducible scalar;
- `extension_or_invention`: changes the route beyond the cited source route
  and the fixed adaptation.  It cannot close a source-faithfulness gap without
  explicit user approval.

Required author-source anchors include:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`
  and `:39-56` for the d18 SIR row, source route, basis/domain/rank controls,
  and `full_sol` launch;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`
  for sequential push, inverse-map sampling, proposal correction, and ESS;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:49-98`
  for ESS-triggered enrichment, `computeL`, weighted resampling, affine
  expansion, shifted target construction, and split fitting data;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:101-124`
  for TTSIRT construction and normalizer semantics;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47`
  for weighted mean/covariance, regularized Cholesky, and high-ESS quantile
  stretch;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:185-188`
  and `:238-248` for defensive mass and TT approximation/rounding;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:81-85`
  for squared approximation mass plus defensive mass.

Required local anchors include:

- `bayesfilter/highdim/source_route.py` for P59/P60/P66/P70 status constants,
  route helpers, nonclaims, and validation gates;
- `tests/highdim/test_p59_author_sir_validation_ladder.py`;
- `tests/highdim/test_p60_author_sir_rank_comparator.py`;
- `tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py`;
- `scripts/p67_author_sir_adjacent_ladder_diagnostics.py`;
- `scripts/p69_phase5c_rank_activity_degree_normalizer_diagnostic.py`;
- `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`;
- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-result-2026-06-16.md`.

Veto rule: any artifact that says "faithful", "source-faithful",
"paper-scale Zhao-Cui", "adaptive parity", or equivalent without paper/source
anchors and local code anchors is blocked with `BLOCK_SOURCE_UNGROUNDED`.

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does the fixed Zhao-Cui SIR d=18 route produce finite, stable, source-anchored filtering values and accuracy evidence across a predeclared validation ladder? |
| Baseline/comparator | Current P59/P60/P66/P70 fixed route, the P70 condition-veto blocker, the Zhao-Cui author source anchors, and a Phase 5-reviewed reference/comparator chosen before accuracy execution. |
| Primary program pass criterion | All phases pass their predeclared gates in order, ending with a closeout artifact that explicitly states which d18 claims are supported and which remain forbidden. |
| Veto diagnostics | Missing source anchors, unresolved P70 condition-number veto, nonfinite values, branch identity drift, source-route invariant drift, rank-channel collapse, defensive-only fitted transport, accuracy threshold chosen after seeing outputs, one-seed promotion, GPU sandbox evidence treated as trusted, HMC smoke promoted to production readiness. |
| Explanatory diagnostics | Fit residuals, holdout/replay residuals, condition numbers, core/channel norms, ESS, normalizer increments, correction weight ranges, runtime, memory, per-seed summaries, reference deviations, gradient finite-difference checks. |
| Not concluded | No d50/d100 scaling, no adaptive Zhao-Cui parity, no author-code failure claim, no HMC production readiness, and no default-policy change unless a later reviewed plan asks for that explicitly. |
| Artifacts | This master program, phase subplans, phase results, machine-readable JSON/CSV run artifacts, Claude review ledger, and final closeout/claim-boundary record. |

## Skeptical Plan Audit

This is a planning artifact, not execution evidence.  The plan survives the
pre-execution skeptical audit only under these constraints:

- P59 execution-only success is not used as an accuracy, rank, or scaling
  baseline.
- P70 Phase 6's condition-number veto is a blocker, not a nuisance failure.
- Fit residuals, local smoke tests, ESS, and short HMC runs are explanatory or
  veto diagnostics unless a phase explicitly makes them part of a stricter
  primary criterion.
- Five fixed seeds are required for robustness; the average is meaningful only
  if every seed passes veto diagnostics and seed spread is reported.
- GPU diagnostics must run in trusted/escalated context, while deliberate
  CPU-only runs must hide CUDA before framework import and say so in the
  artifact.
- No phase may change thresholds after seeing outputs.
- No phase may launch d50/d100, HMC production, or adaptive-parity work.
- Phase 0 must verify cited source anchors by reading the local files and
  recording existence/route-match evidence, not by token search alone.
- A same-route replay or reference bridge is a consistency diagnostic only; it
  cannot serve as the primary accuracy reference in Phase 5.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and current-evidence reset | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase0-governance-current-evidence-reset-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase0-governance-current-evidence-reset-result-2026-06-16.md` |
| 1 | Condition-veto capture and repair gate | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase1-condition-veto-capture-repair-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase1-condition-veto-capture-repair-result-2026-06-16.md` |
| 2 | d18 execution-only reproduction | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-result-2026-06-16.md` |
| 3 | Numeric evaluator and value-finite gate | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-result-2026-06-16.md` |
| 4 | Same-route rank and degree ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-result-2026-06-16.md` |
| 5 | Filtering accuracy and reference gate | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase5-filtering-accuracy-reference-gate-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase5-filtering-accuracy-reference-gate-result-2026-06-16.md` |
| 6 | Five-seed robustness and performance | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase6-five-seed-robustness-and-performance-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase6-five-seed-robustness-and-performance-result-2026-06-16.md` |
| 7 | Value-gradient and HMC diagnostic readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase7-value-gradient-hmc-readiness-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase7-value-gradient-hmc-readiness-result-2026-06-16.md` |
| 8 | Closeout and scaling-decision boundary | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase8-closeout-claim-boundary-scaling-decision-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase8-closeout-claim-boundary-scaling-decision-result-2026-06-16.md` |

## Phase Gate Summary

Phase 0 validates the baseline and source anchors, including current-worktree
drift relative to the P70 blocker artifact.  Phase 1 must capture or repair
the P70 condition-number veto before any full d18 run can proceed.
Phase 2 re-establishes execution-only d18 evidence after the repair.  Phase 3
proves the numeric evaluator/value path is finite.  Phase 4 tests same-route
rank/degree stability.  Phase 5 defines and executes the first d18 accuracy
gate against a reviewed reference/comparator.  Phase 6 repeats the admitted
configuration on five fixed seeds and records runtime/memory.  Phase 7 checks
value-gradient and HMC diagnostic readiness without production-readiness
claims.  Phase 8 writes the final claim boundary and decides whether a separate
d50/d100 scaling program is justified.

## Review Loop

Claude may review this master program and the phase subplans as read-only
artifacts.  Claude cannot authorize crossing human, runtime, model-file,
funding, product-capability, or scientific-claim boundaries.  If review finds
a fixable problem, patch the same planning packet visibly, rerun focused local
checks, and rerun Claude review.  Stop after five Claude review rounds for the
same blocker.
