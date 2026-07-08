# SIR Gradient HMC-Direction Master Program

Date: 2026-06-30

Status: `DRAFT_PENDING_LOCAL_CHECK_AND_CLAUDE_REVIEW`

## Objective

Debug and validate the P8p parameterized SIR d18 LEDH-PFPF-OT gradient lane
under the repository default GPU/XLA/TF32 production route, using a visible
gated repair loop.  The program asks whether the current manual reverse score
is wired correctly and whether remaining discrepancies are finite-particle,
finite-Sinkhorn-budget, finite-difference-window, or implementation defects.

Codex is the supervisor and executor.  Claude Opus max effort is a bounded
read-only reviewer only.

## Governing Artifacts

- Runbook: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-gated-overnight-execution-runbook-2026-06-30.md`
- Execution ledger: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-execution-ledger-2026-06-30.md`
- Claude review ledger: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`
- Stop handoff: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-stop-handoff-2026-06-30.md`

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | SIR route inventory and governance freeze | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-result-2026-06-30.md` |
| 1 | SIR gradient evidence contract | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-result-2026-06-30.md` |
| 2 | Diagnostic reporting and test hooks | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase2-diagnostic-reporting-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase2-diagnostic-reporting-result-2026-06-30.md` |
| 3 | GPU/XLA/TF32 route smoke | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-result-2026-06-30.md` |
| 4 | Material SIR gradient diagnostic | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-result-2026-06-30.md` |
| 5 | Repair loop and discriminating ladders | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-result-2026-06-30.md` |
| 6 | Closeout and next handoff | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase6-closeout-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase6-closeout-result-2026-06-30.md` |

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the current SIR d18 manual reverse LEDH-PFPF-OT gradient lane produce a route-valid, numerically useful HMC-direction score, and if not, which mechanism is the smallest supported root-cause class? |
| Baseline/comparator | Same fixed-randomness SIR target, same theta, same seeds, same observations, same particles, same resampling masks, same streaming finite transport route.  Gradient comparator is local regression finite difference on the same fixed-randomness objective, not an exact nonlinear oracle. |
| Primary pass criterion | By closeout, either a reviewed SIR HMC-direction diagnostic passes its predeclared route and numerical gate, or the program produces a reviewed blocker/root-cause classification with the smallest next discriminating action. |
| Veto diagnostics | CPU route used as material LEDH evidence; GPU evidence without trusted/escalated execution; non-XLA manual reverse route for material runs; TF32 disabled for material production-route runs; hidden dense/full transport autodiff; nonfinite objective/score; missing FD slope SE; missing seed-gradient MCSE; Sinkhorn row residual above the phase threshold when used as evidence; unsupported exact-gradient/HMC/posterior claims. |
| Explanatory diagnostics | Runtime, memory, row residuals, FD regression R2, FD plateau summaries, per-seed gradient covariance/MCSE, manual score decomposition, N ladder, Sinkhorn budget ladder, no-resampling isolation, active-odd isolation. |
| Not concluded | No exact SIR likelihood-gradient proof, no posterior correctness, no NUTS/HMC readiness, no production default change, no Zhao-Cui paper/source-faithfulness claim, no claim that regression FD is an exact oracle. |
| Artifacts | This master program, runbook, per-phase subplans/results, execution ledger, Claude review ledger, JSON/Markdown diagnostic outputs, stop handoff. |

## Skeptical Plan Audit

Audit status: `PASS_WITH_CONSTRAINTS`.

- Wrong-baseline risk: SIR has no exact Kalman comparator.  This program uses
  fixed-randomness regression FD only as a local derivative comparator and
  records that limitation in every material phase.
- Proxy-promotion risk: FD slope SE, MCSE, row residual, and relative error are
  not individually promoted to scientific correctness.  They are route and
  HMC-direction diagnostics under a predeclared gate.
- Environment mismatch risk: material LEDH runs must be escalated GPU/XLA/TF32
  runs.  CPU-hidden unit tests are allowed only for syntax and tiny wiring.
- Stale-context risk: Phase 0 refreshes route inventory before any numerical
  conclusion.
- Artifact-risk check: every phase has a result artifact and the next subplan
  must be refreshed or reviewed before advancing.
- Hidden-action risk: no detached execution is authorized by this visible
  runbook.  Detached overnight execution would require a separate human
  approval and a separate detached-supervisor plan.

## Repair Loop Policy

1. Each phase starts from its dedicated subplan and a skeptical audit entry.
2. If a phase fails for a fixable implementation or planning problem, Codex
   writes the blocker in the phase result, patches the same subplan or affected
   code visibly, runs focused checks, and requests Claude read-only review when
   material.
3. Claude may recommend revisions but cannot authorize boundary changes.
4. Stop after five Claude review rounds for the same blocker and write a
   blocker handoff.
5. Do not change pass/fail criteria after seeing material results unless a new
   human direction explicitly authorizes the criterion change.

## Approval And Escalation Plan

- Claude bounded read-only review has owner approval for this repo, but Claude
  commands still use escalated/trusted execution per policy.
- GPU/CUDA/TensorFlow-XLA commands require escalated execution per `AGENTS.md`.
- Local file edits remain under `docs/plans` unless a reviewed phase authorizes
  code/test changes.
- Detached overnight launch is not authorized by this plan.  This is a visible,
  recoverable execution program.
