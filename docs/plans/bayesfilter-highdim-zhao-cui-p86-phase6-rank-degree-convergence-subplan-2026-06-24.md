# P86 Phase 6 Subplan: Rank And Degree Convergence

Date: 2026-06-24

Status: `EXECUTED_BLOCK_P86_PHASE6_RANK_DEGREE_CONVERGENCE_NOT_ESTABLISHED_REVIEWED`

## Phase Objective

Close or block same-route convergence for the fixed-variant Zhao-Cui author
algebraic `Lagrangep` SIR candidate after the repaired Phase 5 training-base
fit admission.

The executable part of this phase is rank convergence on the hard-wired
`Lagrangep(4,8)` plus `AlgebraicMapping(1)` route. Degree convergence is a
separate branch: it may be planned only after a reviewed configurable-basis
execution path exists, or it must be recorded as blocked/out of scope for the
current P86 runner.

## Entry Conditions Inherited From Previous Phase

- Phase 5 produced an admissible full-budget CPU-hidden training-base fit
  artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json`
- The Phase 5 fit status is
  `P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE_COMPLETED`.
- The Phase 5 route is hard-wired author `Lagrangep(4,8)` plus
  `AlgebraicMapping(1)` with target dimension `36`, fit rank `4`,
  `P_theta=18216`, and training sample count `364320`.
- Phase 5 post-fit gates are acceptable: finite positive normalizers, active
  trainable component, finite fit/holdout residuals, no fallback route, no
  audit-cloud tuning, memory/runtime within envelope, and
  `training_backend=training_base_optimizer`.
- The historical ALS artifact is demoted to stale-route provenance only and
  must not be used as a Phase 6 lower rung or evidence against the
  training-base route.
- The refreshed Phase 5 result has passed Claude read-only bounded review:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-result-2026-06-24.md`
- No Phase 6 comparator fit command has been approved or run.

## Required Artifacts

- Claude-reviewed Phase 5 pass closeout:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-result-2026-06-24.md`
- Phase 6 comparator preflight package that freezes exact same-route rank
  comparator commands, sample floors, seeds/clouds, runtime and memory
  envelopes, output paths, and nonclaims before any runtime request:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-convergence-preflight-2026-06-24.json`
- Comparator fit manifests only after exact human approval of each fitting
  command. Reserved candidate path for the first stronger rank comparator:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank5-comparator-fit-2026-06-24.json`
- Convergence ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-ledger-2026-06-24.json`
- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-result-2026-06-24.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`
- Refreshed Phase 7 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase7-correctness-bridge-subplan-2026-06-24.md`

## Required Checks / Tests / Reviews

- Validate the Phase 5 artifact before using it as the lower rung:
  `training_backend=training_base_optimizer`, status completed, positive
  active normalizers, finite residuals, no fallback, no audit tuning, and
  memory/runtime within envelope.
- Confirm rank comparator artifacts use the same target, basis family, basis
  order/elements, domain map, measure convention, training backend, coordinate
  policy, and cloud-separation policy.
- Compute and record the comparator `P_theta` and required
  `max(20 * P_theta, 5000)` sample floor before any comparator fit approval.
- Run focused local checks for any new comparator/preflight logic.
- Claude read-only bounded review is required before interpreting convergence.
- Human exact-command approval is required before any Phase 6 fitting command.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are adjacent same-route rank rungs stable enough to pass the predeclared Phase 6 rank-convergence gate, and is degree convergence executable or explicitly blocked by current runner support? |
| Baseline/comparator | Lower rung: Phase 5 training-base rank-4 author Lagrangep(4,8) artifact. Comparator: predeclared same-route stronger rank artifact after exact approval and execution. |
| Primary criterion | Rank convergence passes only if predeclared validation/audit stability metrics pass without vetoes on same-route lower and stronger rank artifacts. Degree convergence passes only if a reviewed configurable-basis path exists and its predeclared degree comparator passes; otherwise degree convergence is blocked/out of scope. |
| Veto diagnostics | Historical ALS artifact used; mismatched route/basis/domain/measure/backend; under-budget comparator; missing comparator; cloud overlap; audit tuning; nonfinite diagnostics; inactive trainable normalizer; memory/runtime breach; unapproved command; treating fit residual alone as convergence. |
| Explanatory diagnostics | Rank deltas, residuals, normalizers, optimizer traces, runtime, memory, and any replay rows. |
| Not concluded | No posterior correctness without Phase 7 bridge; no KR closure, HMC readiness, LEDH comparison, scale, source-faithful author TT-cross training, or production readiness. |
| Artifact | Comparator manifests, convergence ledger, Phase 6 result. |

## Forbidden Claims / Actions

- Do not start from the historical blocked ALS artifact or bounded smoke.
- Do not claim rank convergence from the single Phase 5 lower-rung artifact.
- Do not execute degree convergence by changing basis order/elements unless a
  reviewed configurable-basis runner/subplan exists.
- Do not compare against weak, under-budget, or mismatched baselines.
- Do not use audit data for tuning.
- Do not run unapproved fitting commands.
- Do not run GPU, HMC, LEDH, or detached commands in this phase.
- Do not run long comparator fits without the frozen preflight package and
  exact human approval.
- Do not claim correctness or production readiness from rank/degree stability.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only if:

- Claude review agrees that the Phase 5 pass closeout is coherent, or any
  material revision has been patched and rechecked;
- Phase 6 either passes rank convergence with reviewed comparator evidence or
  writes a precise blocker/result explaining which comparator branch failed;
- degree convergence is either supported by a reviewed configurable-basis
  branch and resolved, or explicitly carried forward as a bounded gap;
- same-target correctness bridge scope and exact comparator/source anchors are
  drafted for Phase 7.

## Stop Conditions

Stop if:

- Phase 5 pass closeout review returns a material `VERDICT: REVISE` that
  cannot be patched within five loops;
- no exact same-route rank comparator command can be stated;
- exact command approval is unavailable;
- comparator budget, route identity, cloud separation, finite diagnostics,
  runtime, or memory gates fail;
- degree convergence is requested but no reviewed configurable-basis execution
  path exists;
- Claude and Codex do not converge after five review rounds for the same
  blocker.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 6 result / close record;
3. draft or refresh the Phase 7 subplan;
4. review the Phase 7 subplan for consistency, correctness, feasibility,
   artifact coverage, boundary safety, and stop conditions.

## Subplan Review History

Claude read-only bounded review converged after three iterations:

- Iteration 1 returned `VERDICT: REVISE` because the Phase 5 review state was
  stale and several Phase 6 artifacts lacked concrete paths.
- Iteration 2 returned `VERDICT: REVISE` because one forbidden-action line
  could be read as banning approved long comparator fits.
- Iteration 3 returned `VERDICT: AGREE` after those issues were patched.

Current reviewed gate:

```text
REVIEWED_READY_FOR_COMPARATOR_PREFLIGHT_BLOCKED_BEFORE_FIT_APPROVAL
```
