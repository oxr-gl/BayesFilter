# BayesFilter Highdim Zhao--Cui P30 Remaining-Phases Gated Execution Master Plan

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

primary_governing_sources:
- P30 mathematical specification:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- source-governance charter:
  `docs/plans/bayesfilter-highdim-zhao-cui-source-governance-charter-2026-06-05.md`
- traceability ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md`
- MATLAB reference audit:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p34-zhao-cui-reference-implementation-audit-result-2026-06-03.md`
- P10 MATLAB code audit:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-code-audit-ledger-2026-05-30.md`

current_completed_checkpoint:
- M0 governance/schema: complete.
- M1 exact LGSSM references: complete.
- M2 dense P30 synthetic stochastic-volatility references: complete.
- M2.5 scalar dense nonlinear BayesFilter value path: complete and Claude-reviewed.

## Purpose

Execute the remaining P37/P30 Zhao--Cui implementation-test program one gated
block at a time.  The immediate next gate is M2.6a, a fixed-design functional
TT approximation gate for a small stochastic-volatility adjacent target.  Later
gates may not treat M2.6a as full Zhao--Cui sequential TT/SIRT evidence.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW`.

The largest risk is false promotion: M2.5 validates a scalar dense value path,
but the Zhao--Cui algorithm uses functional TT approximation, squared-density
normalization, retained marginalization, KR/SIRT transport, and replayable
sequential evidence.  Running SIR, predator-prey, stress ladders, or derivative
tables before the SV TT/SIRT value path exists would produce persuasive-looking
proxy artifacts while leaving the central algorithm unimplemented.

This plan therefore decomposes M2.6 into small gates:

- M2.6a tests only fixed-design functional TT approximation of an adjacent SV
  target against dense oracle values.
- M2.6b tests conversion from fitted square-root TT to squared density,
  normalizer, and retained marginalization.
- M2.6c tests a short sequential SV TT/SIRT-like value path against the dense
  M2/M2.5 oracle.
- M2.6d closes branch replay, governance, and traceability for the SV TT lane.

The plan explicitly blocks:

- treating fit residual as posterior accuracy;
- treating a scalar dense grid as TT evidence;
- treating one heldout target fit as a sequential filtering claim;
- treating stress or smoke metrics as correctness;
- moving to derivative/HMC/DSGE/GPU claims without direct downstream evidence;
- copying MATLAB code instead of deriving clean-room BayesFilter contracts from
  P30 and the paper.

No material flaw was found in executing M2.6a first.  The plan will be sent to
Claude before implementation.

## Shared Evidence Contract

Question: can BayesFilter advance from scalar dense nonlinear evidence to a
source-governed, fixed-branch TT/SIRT-style value path for the P30 model suite,
while preserving clean-room governance and claim discipline?

Baseline/comparator:

- M2/M2.5 dense SV references for scalar synthetic SV rows;
- exact Kalman references for LGSSM guardrails;
- P30 equations and validation rungs for model definitions;
- Zhao--Cui paper and audited MATLAB code as source/behavioral anchors only;
- independent BayesFilter tests for every implementation claim.

Primary promotion criterion:

- each phase produces executable tests and a result ledger whose claim boundary
  matches the traceability status in the governance ledger.

Veto diagnostics:

- missing P30 or paper anchor for a mathematical claim;
- missing MATLAB audit anchor for a behavioral reference claim;
- missing BayesFilter code/test anchor for an implementation claim;
- line-by-line MATLAB translation or copied implementation structure;
- nonfinite likelihood, target, normalizer, fit, residual, ESS, replay, or
  derivative diagnostic;
- exact-reference regression in LGSSM or M2/M2.5 SV references;
- rank/conditioning/resource failure without failure classification;
- branch or replay mismatch in fixed-branch phases;
- public API, HMC, DSGE, GPU-production, or large-scale claim without direct
  phase evidence.

Explanatory-only diagnostics:

- fit residual, holdout residual, condition numbers, rank, basis degree,
  ALS sweeps, wall time, memory, target evaluations, branch hashes, plots,
  resource trends, and smoke-test timing.

What will not be concluded even if this plan completes:

- no guarantee that adaptive Zhao--Cui TT-cross behavior is reproduced;
- no stable top-level public API;
- no DSGE or HMC readiness unless a separate downstream plan passes;
- no GPU production readiness unless escalated GPU tests pass;
- no claim that all high-dimensional nonlinear filters have low TT rank;
- no permission to copy MATLAB code into BayesFilter.

Artifact preserving the result:

- this master plan;
- one subplan, result ledger, and Claude review ledger per subphase;
- updated traceability ledger rows where status changes.

## Phase Decomposition

| Phase | Gate | Primary comparator | Promotion boundary |
|---|---|---|---|
| M2.6a | fixed-design functional TT fitting for scalar SV adjacent targets | dense oracle values on train/holdout grids | functional TT target approximation only |
| M2.6b | squared-density normalizer and retained marginalization for fitted adjacent target | dense quadrature normalizer/moments | one fitted target density normalizer/marginal only |
| M2.6c | short sequential SV TT/SIRT-like value path | M2/M2.5 dense sequential oracle | short-horizon SV TT value path only |
| M2.6d | branch/replay/governance closeout for SV TT lane | deterministic replay and traceability ledger | SV TT lane ready to feed later model-suite phases |
| M3 | spatial SIR model fixtures and small filtering rows | RK4 transition references and synthetic truth | SIR evidence only for tested `J` rows |
| M4 | predator-prey preconditioning gate | matched linear vs nonlinear preconditioning budgets | preconditioning comparison only under matched controls |
| M5 | stress ladders | lower-phase guardrails plus one-axis ladders | resource/failure manifests, not correctness proof |
| M6 | fixed-branch gradient | central finite differences of compatible scalar replay | derivative evidence only for value-validated scalar rows |
| M7 | integration closeout | all passed ledgers and traceability rows | final claim ledger and blocker list |

## M2.6 Subphase Dependency

```text
M2.6a -> M2.6b -> M2.6c -> M2.6d -> M3 -> M4 -> M5 -> M6 -> M7
```

M2.6b may not start until M2.6a passes Claude plan and implementation review.
M2.6c may not start until M2.6b demonstrates finite squared-density
normalizer and retained marginal diagnostics.  M6 may not promote any
derivative for a model whose value path has not passed.

## Per-Block Review Loop

For every block:

1. Write or update the subplan with evidence contract and skeptical audit.
2. Run Claude plan review using the trusted Claude worker wrapper.
3. Revise until explicit `PASS`; if max 5 review rounds are exhausted without
   `PASS`, write a stop note and do not implement the block.
4. Implement only the reviewed block.
5. Run focused tests, relevant broad guardrails, `compileall`, and
   `git diff --check`.
6. Write a result ledger with run manifest and decision table.
7. Run Claude governance/code review.
8. Fix material findings until explicit `PASS`; if max 5 review rounds are
   exhausted without `PASS`, write a stop note and do not promote or proceed.
9. Update the traceability ledger only for claims supported by the block.

## Initial Execution Scope

Historical note: the first revision of this artifact authorized only M2.6a
plan review and implementation.  M2.6a has now passed plan, fixture-revision,
and code/governance review as recorded in:

- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-result-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-claude-review-ledger-2026-06-05.md`

After `PASS_M2P6A`, this master plan authorizes the overnight gated
self-recovery runbook below to govern execution from M2.6b onward, but only
after that runbook receives substantive Claude plan review to
`PASS_OVERNIGHT_RUNBOOK`:

- `docs/plans/bayesfilter-highdim-zhao-cui-p30-overnight-gated-self-recovery-runbook-2026-06-05.md`

The later phases remain gated work.  The runbook may repair fixable blockers
under its reviewed recovery loop, but it may not relax evidence contracts,
change scientific baselines, reuse tuned holdouts as promotion evidence, or
promote a phase that still has an unresolved veto.
