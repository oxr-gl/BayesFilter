# P60 Master Program: Rank Convergence And Correctness Bridge For Author-SIR d=18

metadata_date: 2026-06-12
status: PLAN_CREATED_NOT_EXECUTED

## Purpose

P59 closed Phase 9 at the honest execution-only tier:

```text
PASS_P59_9E_D18_EXECUTION_ONLY
```

P60 is the next evidence lane.  It must not repeat the P59 planning mistake of
using launch preparation as validation evidence.  P60 has two separate goals:

1. build same-route higher-rank evidence for d=18 rank convergence;
2. build a same-target reference or bridge before calling the d=18 result a
   correctness candidate.

These are different claims.  Same-route rank convergence can show stability of
the implemented source-route approximation.  It does not by itself prove
correctness against the filtering target.

## Real Blocker Audit

Status: `NO_CONCEPTUAL_BLOCKER_FOR_PLANNING`.

No source or mathematical reason currently blocks creating this plan.  The real
constraints are procedural and evidentiary:

- the current P59-9e run used tiny bounded settings, so it is execution
  evidence only;
- same-route rank convergence requires a stricter, feasible higher-rank
  comparator on the same Zhao-Cui `full_sol` route;
- correctness-candidate status requires a separate same-target reference or a
  documented lower-rung-to-d18 bridge;
- d=50/d=100 must stay blocked until d=18 reaches at least same-route rank
  convergence;
- UKF, memory budget, finite values, and old local/operator/all-grid routes are
  not correctness evidence.

The largest practical risks are runtime, memory, and tolerance selection.  Those
are planning and implementation issues, not fundamental blockers.

## Binding Source-Faithfulness Rule

Every implementation choice must first identify the corresponding Zhao-Cui
paper/source operation.  Agent-created choices are allowed only where the fixed
HMC variant requires frozen ranks, draws, bases, shifts, schedules, ESS gates,
or deterministic diagnostics.  Such choices must be labeled as fixed-variant
choices and may not be represented as author-code behavior.

Author anchors:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m`
  uses `d=0`, `m=18`, `T=20`, `N=5e3`, `tau=10`, `sqr=1`, and
  `full_sol(...)`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m`
  defines the generic route over `[theta, x_t, x_{t-1}]`, previous retained
  marginals, proposal correction, ESS/recentering, and TTIRT/TTSIRT fitting.
  For the author SIR row `d = 0`, the theta block is empty, so the realized
  36D target is `[x_t, x_{t-1}]`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the d=18 author-SIR source-route implementation move from execution-only to rank-stable, and then to correctness-candidate, without drifting from Zhao-Cui `full_sol`? |
| Baseline/comparator | P59-9e execution-only artifact, Zhao-Cui author SIR `full_sol`, and a strictly stronger same-route fixed-TT/SIRT comparator. |
| Primary promotion criterion | P60 may first promote to `PASS_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` only after same-route higher-rank evidence passes declared tolerances.  It may promote to `PASS_P60_D18_CORRECTNESS_CANDIDATE` only after the same-target reference/bridge gate passes. |
| Veto diagnostics | Source-route drift, 18D target instead of realized 36D `[x_t, x_{t-1}]` target for the `d=0` author row, old all-grid/local route, UKF promoted as correctness comparator, synthetic/contract-double transport promoted as evidence, missing rank comparator, missing reference/bridge, nonfinite log marginal likelihood, failed replay/proposal-correction checks, unbounded memory forecast, or post-hoc tolerance relaxation after seeing comparator/reference results. |
| Explanatory diagnostics | Runtime, memory, ESS, correction-log-weight ranges, normalizer increments, probe-density deltas, lower-rung dense residuals, UKF scout summaries, and wall time. |
| Not concluded | Rank convergence does not prove exact correctness; correctness-candidate status does not prove d=50/d=100 scaling or HMC production readiness. |
| Artifact trail | P60 master, P60-1 through P60-4 subplans, result files, manifests, tests, and optional Claude read-only review ledgers under `docs/plans`. |

## Skeptical Plan Audit

Status: `PASS_TO_REVIEW_BEFORE_EXECUTION`.

- Wrong-baseline risk: blocked by requiring the Zhao-Cui `full_sol` route and
  P59-9e as the baseline.
- Proxy-risk: UKF, memory, finite values, and wall time are explanatory or veto
  diagnostics only.
- Missing-stop risk: stronger claims remain blocked unless the exact evidence
  artifact exists.
- Unfair-comparison risk: same-route rank comparisons must use the same target,
  observations, frozen draws/probes where applicable, and route ordering.
- Hidden-assumption risk: any fixed-variant choices must be labeled and
  separated from author-code facts.
- Environment risk: GPU/CUDA runs, if any, require escalation.  CPU-only runs
  must hide GPU devices and record that choice.
- Artifact-risk: every phase has a result file and pass/block token.

## Phase Matrix

| Phase | Name | Subplan | Result | Pass token | Block token |
| --- | --- | --- | --- | --- | --- |
| P60-1 | Source Rank Knobs And Comparator Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p60-1-source-rank-knobs-and-comparator-contract-subplan-2026-06-12.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p60-1-source-rank-knobs-and-comparator-contract-result-2026-06-12.md` | `PASS_P60_1_SOURCE_RANK_COMPARATOR_CONTRACT` | `BLOCK_P60_1_SOURCE_RANK_COMPARATOR_CONTRACT` |
| P60-2 | Same-Route Higher-Rank Comparator | `docs/plans/bayesfilter-highdim-zhao-cui-p60-2-same-route-higher-rank-comparator-subplan-2026-06-12.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p60-2-same-route-higher-rank-comparator-result-2026-06-12.md` | `PASS_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` | `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` |
| P60-3 | Same-Target Reference Or Bridge | `docs/plans/bayesfilter-highdim-zhao-cui-p60-3-same-target-reference-bridge-subplan-2026-06-12.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p60-3-same-target-reference-bridge-result-2026-06-12.md` | `PASS_P60_D18_CORRECTNESS_BRIDGE` | `BLOCK_P60_D18_CORRECTNESS_BRIDGE` |
| P60-4 | Validation Ladder Promotion Integration | `docs/plans/bayesfilter-highdim-zhao-cui-p60-4-validation-ladder-promotion-integration-subplan-2026-06-12.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p60-4-validation-ladder-promotion-integration-result-2026-06-12.md` | `PASS_P60_D18_CORRECTNESS_CANDIDATE` | `BLOCK_P60_D18_CORRECTNESS_CANDIDATE` |

## Execution Order

1. Execute P60-1 before changing code.
2. Execute P60-2 only after P60-1 passes.
3. Execute P60-3 after P60-1, and preferably after P60-2 so the bridge is not
   used to excuse rank instability.
4. Execute P60-4 only after P60-2 and P60-3 pass.

## Claim Ladder

| Claim | Required evidence |
| --- | --- |
| d=18 execution-only | Already passed in P59-9e. |
| d=18 same-route rank convergence | P60-2 pass: strictly stronger same-route comparator, same target and route, declared tolerances met, no veto. |
| d=18 correctness candidate | P60-2 plus P60-3 plus P60-4: rank stability and same-target reference/bridge evidence. |
| d=50/d=100 launch | Not in P60 except as future gated work after d=18 same-route rank convergence. |

## Initial Token

`PLAN_P60_RANK_CONVERGENCE_AND_CORRECTNESS_BRIDGE`
