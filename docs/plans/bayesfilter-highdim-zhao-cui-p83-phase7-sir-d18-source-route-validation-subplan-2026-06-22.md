# P83 Phase 7 Subplan: SIR d=18 Source-Route Validation

Date: 2026-06-22

Status: `DRAFT_BLOCKED_PENDING_HUMAN_APPROVAL_AND_EXECUTION_REFRESH`

## Phase Objective

Validate the actual fixed-TTSIRT source-route SIR d=18 pipeline only after the
Phase 6 fitting budget design has passed review and the required fit artifacts
exist.

This subplan is a handoff draft.  It does not authorize execution.  Any d=18,
GPU, fitting, LEDH, HMC, MCMC, or long validation command requires a refreshed
reviewed subplan and explicit human approval.

## Entry Conditions Inherited From Phase 6

Phase 7 may begin execution only if:

- Phase 6 result status is `PASS_P83_PHASE6_FITTING_BUDGET_DESIGN`;
- Phase 6 local checks passed;
- Claude read-only review agreed the Phase 6 design and this Phase 7 handoff;
- the fitting budget manifest records `P_theta`, `minimum_training_samples`,
  realized rank tuple, basis dimensions, source fit-data mode, defensive tau,
  and disjoint training/holdout/replay/validation/audit cloud roles;
- source-route fit artifacts exist and are named in the Phase 7 command
  manifest, or the refreshed Phase 7 plan is explicitly a fitting/build phase
  rather than validation;
- `production_kr_closure=False` remains recorded unless a later reviewed
  source-backed KR replacement passes;
- Phase 4 derivative readiness remains blocked and out of validation scope, or
  a separate reviewed derivative repair has passed;
- the user explicitly approves the exact command(s).

Inherited nonclaims:

- Phase 5 was mechanics-only;
- Phase 6 was design-only;
- current grid-CDF transport is a diagnostic approximation, not production KR
  closure;
- FD/JVP/ForwardAccumulator evidence is diagnostic-only;
- UKF, generated-sample CE, validation CE, replay, finite values, and fit loss
  cannot by themselves prove source-route correctness.

## Required Artifacts

- Phase 7 result or blocker:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-result-2026-06-22.md`
- Phase 7 command/evidence manifest, to be frozen before execution:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-2026-06-22.json`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md`

## Required Checks / Tests / Reviews

Before any execution command is allowed, refresh this subplan with exact files,
commands, seeds, runtime posture, GPU/CPU decision, and expected artifacts.

Minimum pre-execution checks:

```bash
rg -n "PASS_P83_PHASE6_FITTING_BUDGET_DESIGN|P_theta|minimum_training_samples|training|holdout|validation|audit|approval|BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md -S

rg -n "P58_M9_AUTHOR_SIR_TARGET_ID|p58_m9_source_route_pipeline_readiness|p59_author_sir_runner_manifest_path|p59_author_sir_validation_ladder|has_fixed_ttsirt_fit_artifacts|d18_execution_only|d18_correctness_candidate" \
  bayesfilter/highdim/source_route.py \
  tests/highdim/test_p58_m9_source_route_pipeline_readiness.py -S

git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md
```

Review:

- Claude read-only review is required for any refreshed execution version of
  this subplan.
- Claude may not authorize crossing human, runtime, GPU, funding,
  product-capability, default-policy, or scientific-claim boundaries.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the reviewed fixed-TTSIRT source-route SIR d=18 pipeline pass the declared validation tier using source-route fit artifacts and disjoint evidence clouds? |
| Baseline/comparator | Phase 6 budget contract, P58/P59 launch readiness guard, P66 ladder discipline, source-route mechanics from P83-5, and a declared comparator tier. |
| Primary criterion | To be frozen before execution.  At minimum: ready source-route manifest, completed budgeted fit artifacts, finite source-route execution diagnostics, no launch-readiness blockers, and tier-specific pass criteria. |
| Veto diagnostics | Missing fit artifacts; under-budget training; source drift; proxy comparator; nonfinite target/transport/proposal/weights; failed readiness guard; heldout/audit role contamination; derivative readiness assumed while Phase 4 remains blocked; unapproved GPU/long/d=18/LEDH/HMC command. |
| Explanatory diagnostics | Fit residual, holdout residual, replay diagnostics, ESS, normalizer increments, correction ranges, runtime, memory, and finite-value summaries. |
| Not concluded | No posterior correctness, no exact likelihood correctness, no HMC readiness, no production KR closure, no LEDH superiority, no d=50/d=100 scaling. |
| Artifact preserving result | Phase 7 result and JSON manifest. |

## Comparator Tiers

Phase 7 must choose exactly one tier before execution:

| Tier | Allowed interpretation | Extra requirements |
|---|---|---|
| `d18_execution_only` | finite source-route execution diagnostics only | no accuracy/correctness/rank-convergence claim |
| `d18_same_route_rank_convergence` | adjacent rank/degree stability diagnostic | budgeted stronger same-route comparator, same source invariants, disjoint clouds |
| `d18_correctness_candidate` | candidate evidence toward d=18 correctness | source-backed comparator/reference bridge and stricter audit contract |

If Phase 4 derivative readiness is still blocked, Phase 7 cannot be a gradient,
HMC, or value-gradient validation phase.

## Forbidden Claims / Actions

- Do not execute this draft subplan.
- Do not run d=18 validation, fitting, GPU, LEDH, HMC, MCMC, or long jobs
  without explicit human approval of exact commands.
- Do not promote UKF, generated-sample CE, validation CE, FD, JVP,
  ForwardAccumulator, replay, finite values, ESS, or training loss into
  correctness evidence outside the declared tier.
- Do not claim production KR closure while current transport metadata says
  `production_kr_closure=False`.
- Do not claim derivative readiness while
  `BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS` remains active.
- Do not change default project policy.

## Exact Next-Phase Handoff Conditions

P83-8 scale/stress closeout may be drafted only if Phase 7 writes a result
that states:

- selected comparator tier;
- exact command(s) actually run;
- fit artifact and evidence manifest paths;
- pass/fail status for primary criterion;
- veto diagnostic status;
- uncertainty and nonclaims;
- whether d=50/d=100 stress is justified, blocked, or out of scope.

## Stop Conditions

Stop with a Phase 7 blocker result if:

- fit artifacts are missing or under budget;
- the readiness guard reports blockers;
- source-route invariants drift;
- training/holdout/validation/audit roles overlap;
- Phase 4 derivative readiness is needed but still blocked;
- current grid-CDF diagnostic approximation would need to be promoted into
  production KR closure;
- exact commands, seeds, artifacts, or runtime posture cannot be frozen before
  execution;
- human approval is not available for any d=18, GPU, LEDH, fitting, HMC, MCMC,
  or long command.

## Consistency Review

Local Codex review result:

- Boundary safety: PASS.  The draft blocks execution and requires explicit
  approval for validation or long/hardware work.
- Artifact coverage: PASS.  Required result, JSON, ledgers, and stop handoff
  are named.
- Feasibility: BLOCKED for execution until fit artifacts and exact commands are
  frozen.
- Scientific-claim safety: PASS.  Execution-only diagnostics, rank convergence,
  and correctness-candidate tiers are separated.
- Phase 4 derivative blocker: preserved.
