# P84 Zhao-Cui Production Promotion Master Program

Date: 2026-06-23

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Objective

Promote the Zhao-Cui fixed-TTSIRT source-route SIR lane from the P83
execution-only closeout toward production readiness, or stop with a precise
blocker whenever the evidence is insufficient.

This program starts from P83:

```text
Zhao-Cui SIR d=18 source-route execution works as a bounded diagnostic.
It is not yet validated as a correct, scalable, or production SIR filter.
```

P84 must not use the P83 `d18_execution_only` pass as correctness, fit-quality,
rank-convergence, HMC, LEDH, scaling, or production evidence.

## Governing Inputs

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-final-reset-memo-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-result-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase8-scale-stress-closeout-result-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md`
- Zhao-Cui author source under
  `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

## Role Contract

Codex is the visible supervisor and executor.

Claude Opus max effort may be used only as a read-only reviewer of compact,
bounded prompts.  Claude is not an execution authority and cannot authorize
crossing human, runtime, GPU, model-file, funding, product-capability,
default-policy, or scientific-claim boundaries.

## Whole-Program Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the Zhao-Cui fixed-TTSIRT source-route SIR lane be promoted from execution-only diagnostic status to a reviewed production-ready target, or can each remaining production gap be closed or blocked with evidence? |
| Baseline/comparator | P83 execution-only closeout, Phase 6 fitting budget contract, author Zhao-Cui source anchors, and BayesFilter TensorFlow/TFP source-route implementation. |
| Primary pass criterion | Every production gap has a phase result with either a passing artifact and review trail or a precise blocker.  Production promotion requires all mandatory gates to pass and owner approval. |
| Veto diagnostics | P83 execution-only pass promoted to correctness; under-budget fit promoted to evidence; local all-grid/operator route used as source-faithful; UKF/FD/JVP/ForwardAccumulator promoted beyond diagnostic role; production KR closure claimed while metadata says false; GPU/LEDH/HMC/long commands run without exact approval. |
| Explanatory diagnostics | Code/source inventories, fit residuals, holdout/replay rows, ESS, rank/degree stability, reference-bridge residuals, derivative diagnostics, HMC diagnostics, LEDH comparison summaries, scale/stress telemetry. |
| Not concluded | No production readiness, default-policy change, posterior correctness, broad source-faithfulness, HMC readiness, LEDH superiority, or d=50/d=100 scaling until the corresponding phase gates pass. |
| Artifacts | This master program, visible runbook, execution ledger, Claude review ledger, phase subplans/results, JSON manifests, stop handoff, and final reset memo. |

## Skeptical Plan Audit

Pre-execution audit result:

- Wrong baseline risk is high.  P83 passed only execution-only, so P84 must
  start from gap closure rather than scale/stress.
- Proxy-promotion risk is high.  Fit loss, finite execution, ESS, replay,
  holdout, validation CE, FD/JVP, and short chains can explain or veto only
  under their phase contracts.
- Missing stop-condition risk is controlled by per-phase stop conditions and
  human-required approval gates.
- Environment risk is deferred into exact-command approvals.  GPU/CUDA/LEDH/HMC
  commands require escalated/trusted execution and explicit approval.
- Artifact risk is controlled by requiring a result or blocker at each phase.

P84 may begin with Phase 0 because it is a planning/governance phase and does
not run fitting, GPU, LEDH, HMC, MCMC, d=50/d=100, or long commands.

Phase 0 must explicitly freeze the production-claim scope before any later
phase executes:

- whether gradients/HMC are in scope for the production claim;
- whether LEDH comparison is part of the production claim;
- whether any d=50/d=100 scale claim is in scope;
- where multi-seed/uncertainty accounting will be certified.

## Phase Ladder

| Phase | Name | Subplan | Required result |
|---|---|---|---|
| P84-0 | Production target freeze | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase0-production-target-freeze-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase0-production-target-freeze-result-2026-06-23.md` |
| P84-1 | Author basis/domain parity | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase1-author-basis-domain-parity-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase1-author-basis-domain-parity-result-2026-06-23.md` |
| P84-2 | Budget-compliant fitting | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase2-budget-compliant-fitting-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase2-budget-compliant-fitting-result-2026-06-23.md` |
| P84-3 | Same-route rank/degree convergence | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase3-same-route-rank-convergence-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase3-same-route-rank-convergence-result-2026-06-23.md` |
| P84-4 | Correctness bridge | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase4-correctness-bridge-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase4-correctness-bridge-result-2026-06-23.md` |
| P84-5 | Production KR closure | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase5-production-kr-closure-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase5-production-kr-closure-result-2026-06-23.md` |
| P84-6 | Analytical derivative repair | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase6-analytical-derivative-repair-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase6-analytical-derivative-repair-result-2026-06-23.md` |
| P84-7 | HMC readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase7-hmc-readiness-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase7-hmc-readiness-result-2026-06-23.md` |
| P84-8 | LEDH comparator | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase8-ledh-comparator-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase8-ledh-comparator-result-2026-06-23.md` |
| P84-9 | d50/d100 scale stress and uncertainty accounting | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase9-scale-stress-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase9-scale-stress-result-2026-06-23.md` |
| P84-10 | Production promotion decision | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase10-production-promotion-decision-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase10-production-promotion-decision-result-2026-06-23.md` |

## Approval Gates To Anticipate

Already anticipated for smooth execution:

- Claude read-only review through the trusted wrapper requires escalated
  permissions.
- Any GPU/CUDA/NVIDIA probe or run requires escalated permissions.
- Any fitting run expected to exceed a short smoke, any d=18 validation beyond
  execution-only, LEDH comparison, HMC/MCMC, d=50/d=100, or long command
  requires exact-command human approval.
- Any default-policy or production-promotion decision requires explicit owner
  approval.

## Per-Phase Protocol

Every phase must use its dedicated subplan.  At the end of each phase:

1. run required local checks;
2. write a phase result or blocker;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, boundary safety, stop conditions, and approval needs;
5. use Claude read-only review for material subplans or material blockers;
6. repair visibly and rerun focused checks when fixable;
7. stop after five Claude review rounds for the same blocker.

## Final Promotion Rule

`PASS_P84_PRODUCTION_PROMOTION` is allowed only if all mandatory gates pass:

- author-basis/domain parity or reviewed fixed adaptation;
- budget-compliant fitting;
- same-route rank/degree convergence;
- correctness bridge;
- production KR closure;
- derivative readiness when HMC/gradient use is in scope;
- HMC readiness when HMC is in scope;
- LEDH comparison if used for the production claim;
- scale/stress evidence for any d=50/d=100 claim;
- multi-seed/uncertainty accounting, certified in Phase 9 for scale/stress
  claims and audited again in Phase 10 for the final approved scope;
- explicit owner approval for default/policy change.
