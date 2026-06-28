# LR-TF32-0 Subplan: Governance, Evidence, And Review Gate

Date: 2026-06-20
Owner: peer agent

## Status

`P00_PASSED`

## Phase Objective

Lock the algorithm, scale motivation, evidence contract, thresholds, ownership
boundaries, approval gates, and repair loop before implementation or scale
execution.

## Entry Conditions Inherited From Previous Phase

- User requested a detailed master program for testing whether low-rank
  coupling can scale LEDH-PFPF-OT batched TF32 to 50k-100k particles.
- The active independent-lane clarification says the peer agent owns low-rank
  coupling solver-route work and does not wait on positive-feature artifacts.
- Existing low-rank solver-route implementation and Wave 2/Wave 3 context are
  available.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-master-program-2026-06-20.md`
- Visible gated execution runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-visible-gated-execution-plan-2026-06-20.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-visible-execution-ledger-2026-06-20.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-visible-stop-handoff-2026-06-20.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-claude-review-ledger-2026-06-20.md`
- P00 result/close record.

## Required Checks, Tests, And Reviews

- Local scan that the master/runbook/subplans include required evidence
  contracts, stop conditions, non-claims, phase artifacts, fixture scales,
  embedded run-manifest schema, and approval gates.
- Local scan that no positive-feature artifact is treated as evidence.
- Claude Opus path-only read-only review of the material plan artifacts until
  `VERDICT: AGREE` or max five rounds for the same blocker.  Claude review
  commands must use trusted/elevated wrapper execution; non-elevated Claude
  failures are sandbox-only evidence until a trusted probe is rerun.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the low-rank TF32 scale-smoke program sufficiently bounded and evidence-bearing to launch without confusing tiny validation with 50k/100k scale feasibility? |
| Baseline/comparator | Independent-lane clarification, Wave 2/Wave 3 low-rank context, and TF32 closeout context. |
| Primary pass criterion | Required governance artifacts exist, include phase subplans with evidence contracts and stop conditions, predeclare thresholds, freeze fixture scales/run sizes, define the embedded run-manifest schema, separate CPU checks from trusted GPU scale evidence, and preserve all non-claims. Claude path-only review converges under trusted/elevated wrapper execution. |
| Veto diagnostics | Missing phase subplan, missing threshold, missing fixed fixture scale/run size, missing embedded manifest schema, missing approval gate, positive-feature comparison dependency, runtime/memory promoted to speedup, missing GPU/Claude trust boundary, missing dense-materialization veto, or unsupported readiness/default/ranking claim. |
| Explanatory diagnostics | Claude review round count, local scan hits, dirty-worktree notes for unrelated files. |
| Not concluded | No implementation validity, 50k/100k feasibility, TF32 help, speedup, ranking, dense equivalence, posterior correctness, HMC readiness, public/default readiness, or coordinator merge. |

## Forbidden Claims And Actions

- Do not implement before the governance review gate passes.
- Do not send full file bodies to Claude; use paths and bounded questions
  through trusted/elevated wrapper execution.
- Do not claim TF32 helps or that low-rank is faster/better.
- Do not use GPU evidence without trusted/escalated execution.
- Do not edit positive-feature, public export/default, schema, package, or
  coordinator merge files.

## Exact Next-Phase Handoff Conditions

Advance to LR-TF32-1 only if:

- P00 local checks pass;
- Claude path-only review returns `VERDICT: AGREE`;
- no approval/resource/shared-contract blocker remains;
- P01 subplan is refreshed and reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.

## Stop Conditions

Stop if Claude and Codex fail to converge after five rounds on the same
material planning blocker; if a shared contract/public/default/API edit is
required; if GPU/package/network/destructive permissions are required before
the relevant approved phase; or if the scale question cannot be answered by the
planned artifacts.
