# P59 Master Program: Phase 9 Preparation And Validation Boundary Repair

metadata_date: 2026-06-11
status: PLAN_DRAFT_FOR_CLAUDE_REVIEW

## Supervisor Contract

Codex is the visible supervisor and execution agent.

Claude Code Opus max-effort is a read-only reviewer only.  Claude must not edit
files, run experiments, launch agents, or mutate the workspace.

If Claude does not respond, Codex must first run the minimal read-only probe
`READ-ONLY PROBE. Reply with exactly: PROBE_OK`.  If the probe succeeds, Codex
must reduce or redesign the review prompt instead of treating Claude as
unavailable.

## Planning Bug Being Repaired

P57-M9 asked for a spatial SIR validation ladder before the author-SIR source
route had been assembled.  P58 correctly added a fail-closed readiness guard,
but it did not close the real launch blockers B1-B5.

P59 rewrites Phase 9 into preparation phases followed by validation:

- P59-9a: author-SIR adjacent target and bounded fixed TT/SIRT fit artifacts;
- P59-9c: full-route versus preconditioned-route decision gate;
- P59-9b: source-route step-spec assembly for the route selected by 9c;
- P59-9d: M9 runner and manifest path;
- P59-9e: validation ladder only after 9a-9d pass.

This is not a governance-only lane.  The first executable target is a bounded
P59-9a artifact that exercises the author-SIR source-route adjacent target in
the correct dimension.

## Binding Source-Faithfulness Rule

Every implementation decision in this lane must cite the Zhao-Cui paper/source
operation it follows.  Agent-created choices are allowed only for the fixed-HMC
variant boundary: ranks, draws, bases, shifts, schedules, ESS gates, and
resampling choices may be frozen for differentiability, but the route must
still follow the author's source-route operations.

Non-goals and noise:

- adaptive Zhao-Cui parity;
- S&P 500 reproduction;
- smoothing;
- old local/operator/all-grid routes;
- UKF, memory budget, finite values, or contract doubles promoted as
  correctness evidence.

## Critical Dimension Contract

For the author Austria SIR row, the model has parameter dimension `d = 0`,
state dimension `m = 18`, observation dimension `n = 9`, and horizon `T = 20`.

The source-route reapproximation target dimension is not 18.  It is

```text
d + 2m = 0 + 2 * 18 = 36,
```

because `full_sol` carries `[theta, x_t, x_{t-1}]` in each reapproximation
target.  Any Phase 9 preparation artifact that fits or validates the
source-route target must preserve this 36-dimensional target contract.

## Source Anchors

- Author SIR row:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m`
  declares `d=0`, `m=18`, `T=20`, `N=5e3`, `tau=10`, `sqr=1`,
  `poly2 = ApproxBases(..., d + 2*m)`, max rank 40, init rank 20, and
  `full_sol(..., N, 4)`.
- Full source route:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m`
  initializes `[theta, x_0]`, pushes samples, augments `[theta, x_t,
  x_{t-1}]`, computes weighted recentering, constructs `fun_into_sirt`, fits
  `TTSIRT`, inverse-maps retained samples, and corrects by
  `exp(-fun_post(r)) / eval_pdf(sirt,r)`.
- Previous marginal:
  `full_sol.m` marginalizes the previous retained SIRT over the
  `[theta, x_{t-1}]` prefix for `t > 1`.
- Preconditioned route:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m` and
  `models/tensordot/precond.m`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter repair Phase 9 so that launch preparation happens before validation, and can it produce bounded author-SIR source-route preparation evidence without drifting into old proxy routes? |
| Baseline/comparator | P58 blocker ledger; P57 M1-M8 source-route components; Zhao-Cui author SIR source and `full_sol`; current BayesFilter source-route APIs. |
| Primary promotion criterion | P59-9a through P59-9d must produce real assembly artifacts before P59-9e validation may run.  P59-9e may claim only the declared tier: `d18_execution_only`, `d18_same_route_rank_convergence`, or `d18_correctness_candidate`. |
| Veto diagnostics | 18-dimensional target used for TT/SIRT reapproximation instead of 36; old local/operator/all-grid route; contract-double transport treated as author-SIR evidence; UKF/memory proxy promoted; missing P59-9a..9d artifact hidden while claiming validation readiness. |
| Explanatory diagnostics | Bounded rank-1 or low-rank 36D fit, finite target values, shape/provenance manifests, source searches, focused CPU tests, and Claude read-only reviews. |
| Not concluded | Bounded 9a evidence does not prove d=18 filtering accuracy, d=50/d=100 scaling, HMC production readiness, adaptive parity, or paper reproduction. |
| Artifact trail | P59 master, 9a-9e subplans, Claude plan review ledger, code/tests, 9a result, later phase results, and final readiness manifest under `docs/plans`. |

## Skeptical Plan Audit

Status before Claude review: `PASS_TO_REVIEW_WITH_EXECUTION_BOUNDARY`.

- Wrong-baseline risk: the plan rejects P51/P53 local/operator/all-grid routes
  and P57-M6 contract doubles as validation evidence.
- Proxy-risk: UKF and memory are diagnostic/veto inputs only.
- Missing-stop risk: if 9a-9d are not passed, 9e must not run.
- Dimension-risk: 9a is explicitly gated on the `d + 2m = 36` source target.
- Environment mismatch: CPU-only focused tests are acceptable for 9a shape and
  bounded-fit evidence.  GPU use, if later needed, must be escalated.
- Artifact-risk: every phase has a named result artifact and stop token.

## Phase Matrix

| Phase | Name | Subplan | Result | Pass token | Block token |
| --- | --- | --- | --- | --- | --- |
| P59-9a | Author-SIR 36D Target And Bounded Fit Prep | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9a-author-sir-36d-target-fit-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9a-author-sir-36d-target-fit-result-2026-06-11.md` | `PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP` | `BLOCK_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP` |
| P59-9c | Preconditioned Route Integration | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9c-preconditioned-route-integration-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9c-preconditioned-route-integration-result-2026-06-11.md` | `PASS_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION` | `BLOCK_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION` |
| P59-9b | Source-Route Step-Spec Assembly | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9b-source-route-step-spec-assembly-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9b-source-route-step-spec-assembly-result-2026-06-11.md` | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | `BLOCK_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` |
| P59-9d | Runner And Manifest Path | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9d-runner-manifest-path-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9d-runner-manifest-path-result-2026-06-11.md` | `PASS_P59_9D_RUNNER_MANIFEST_PATH` | `BLOCK_P59_9D_RUNNER_MANIFEST_PATH` |
| P59-9e | Validation Ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9e-validation-ladder-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9e-validation-ladder-result-2026-06-11.md` | tier-specific pass token | `BLOCK_P59_9E_VALIDATION_LADDER` |

P59-9c is ordered before P59-9b even though the phase id is `9c`, because a
route decision must exist before step-spec assembly.  For the author Austria SIR
row, the expected route is the `full_sol` route used by
`eg3_sir/mainscript.m`.  If P59-9c ever concludes that a preconditioned route
is required, P59-9b and P59-9d must block until they are rewritten against
`pre_sol` anchors and P57-M8 wiring.

## Review Loop

Claude review must loop until `VERDICT: AGREE` or max five iterations.  The
fifth review may be accepted only if there is no major source-faithfulness,
implementation-order, 36D-target, or claim-boundary blocker.

Every review prompt must ask:

1. Does the plan force source/paper checks before implementation?
2. Does 9a correctly use the 36D `[theta, x_t, x_{t-1}]` target?
3. Are 9a-9d real prerequisites rather than results of validation?
4. Does 9e refuse to launch until 9a-9d pass?
5. Are UKF, memory, old routes, and contract doubles prevented from becoming
   correctness evidence?

## Initial Token

`PLAN_P59_M9_PREPARATION_AND_VALIDATION_BOUNDARY_REPAIR`
