# P00 Subplan: Governance, Runbook, And Review Lock

Date: 2026-06-20

## Phase Objective

Create and review the master program, visible gated execution runbook,
execution ledger, stop handoff, Claude review ledger, and P01 subplan before
running any scientific/engineering benchmark in the LEDH default impact ladder.

## Entry Conditions Inherited From Previous Phase

- GPU-oriented LEDH-PFPF-OT TF32 is the DPF transport default by owner
  directive.
- Fresh default GPU smoke passed and is preserved under `docs/benchmarks`.
- Peer low-rank artifacts are unrelated and must not be edited in this lane.
- Local dirty HMC files exist and must be treated as ambient state, not reverted.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-master-program-2026-06-20.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-gated-execution-runbook-2026-06-20.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-execution-ledger-2026-06-20.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-stop-handoff-2026-06-20.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-claude-review-ledger-2026-06-20.md`
- P01 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p01-correctness-subplan-2026-06-20.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p00-governance-result-2026-06-20.md`

## Required Checks, Tests, And Reviews

- `git diff --check` for newly edited planning artifacts.
- `rg` checks that the master/runbook/subplans contain required phase fields,
  stop conditions, evidence contracts, and forbidden claims/actions.
- Claude Opus max-effort read-only review of the artifact paths and compact
  summary, not whole-file prompt text.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the execution structure safe and complete enough to launch P01? |
| Baseline/comparator | Visible runbook template, repo governance, default promotion result, and existing LEDH benchmark harnesses. |
| Primary pass criterion | Required governance artifacts exist, local checks pass, and after any visible repairs Claude returns `VERDICT: AGREE` within five rounds for the same blocker. |
| Veto diagnostics | Missing phase subplan/result path; missing evidence contract; missing stop conditions; Claude-as-executor language; unsupported posterior/HMC/speed claim; unrelated dirty work touched. |
| Explanatory diagnostics | File path inventory and review comments. |
| Not concluded | No correctness, precision, GPU target-shape, performance, HMC, posterior, or statistical result. |
| Artifact | P00 result note plus review ledger. |

## Forbidden Claims/Actions

- Do not run LEDH benchmarks in P00.
- Do not touch peer low-rank files or unrelated HMC dirty files.
- Do not claim the route helps accuracy, performance, posterior inference, or
  HMC.
- Do not let Claude edit, execute, launch workers, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

Proceed to P01 only if:

- P00 required artifacts exist;
- local checks pass;
- Claude review converges with `VERDICT: AGREE`;
- P01 subplan exists and is reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.

## Stop Conditions

- Required artifact cannot be written.
- Local checks fail and the fix is unclear.
- Claude does not respond to a small probe or review prompt after prompt repair.
- Claude/Codex do not converge after five rounds for the same blocker.
- Any action would require changing default policy, touching unrelated dirty
  work, or making unsupported scientific claims.
