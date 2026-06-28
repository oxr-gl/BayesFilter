# P07 Closeout And Recommendation Subplan

Date: 2026-06-24

Status: `DRAFT_PENDING_P06`

## Phase Objective

Write the final scoped calibration verdict, update ledgers and stop handoff,
and state exactly what residual/value/gradient rule is justified, if any.

P07 is a documentation and review phase. It does not run new benchmarks unless
a required local artifact validator is missing and can be run without changing
evidence.

## Entry Conditions Inherited From Previous Phase

- P06 result or blocker result exists and has review convergence.
- P01-P06 results are available or clearly classified as blocked/skipped with
  nonclaims.
- P07 subplan has been refreshed with actual evidence state.
- No approval is inherited for HMC runtime, package/API/default changes,
  package installs, network fetches, model-file edits, or scientific claims.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-result-2026-06-24.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-execution-ledger-2026-06-24.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-claude-review-ledger-2026-06-24.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-stop-handoff-2026-06-24.md`

## Required Checks, Tests, And Reviews

- Local artifact inventory for P00-P06 results and structured benchmark paths.
- Final claim-boundary scan:
  - threshold recommendation scope;
  - posterior correctness nonclaim;
  - HMC readiness nonclaim;
  - default/public API nonclaim;
  - statistical-superiority nonclaim unless uncertainty evidence supports more.
- Final decision table and inference-status table.
- Run manifest summarizing git commit, environment, GPU status, seeds, commands,
  and artifact paths.
- Post-run red-team note.
- Claude Opus/max read-only review of final result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What scoped rule or blocker is justified by the residual posterior-gradient calibration program? |
| Baseline/comparator | P01-P06 results, LGSSM exact reference where available, streaming engineering comparator, and frozen rule manifest. |
| Primary pass criterion | Final result accurately reflects evidence, separates calibration from holdout and target-family probes, preserves nonclaims, and passes local/Claude review. |
| Veto diagnostics | Unsupported claim, missing required result artifact, contradictory threshold status, ignored hard veto, missing uncertainty statement, or review nonconvergence. |
| Explanatory diagnostics | All per-phase diagnostics, residual/value/gradient association, actual-SIR paired deltas, and runtime notes. |
| Not concluded | No package default change, no public API readiness, no HMC readiness, no broad posterior correctness, no scientific validity unless separately proven. |
| Artifact | Final result, updated ledgers, updated stop handoff, and Claude review ledger. |

## Forbidden Claims And Actions

- Do not claim more than P01-P06 evidence supports.
- Do not make default-policy, public API, package release, HMC readiness,
  funding, product, or scientific claims.
- Do not retroactively change P04 frozen rule.
- Do not run new material experiments in closeout.
- Do not use Claude as execution authority.

## Exact Next-Phase Handoff Conditions

P07 is the final phase. It completes the program only if:

- final result exists and includes decision and inference-status tables;
- ledgers and stop handoff are updated;
- local boundary scan passes;
- Claude final review returns `VERDICT: AGREE`.

If final review does not converge, write a blocker stop handoff and ask for
human direction.

## Stop Conditions

- Required phase result artifacts are missing and cannot be recovered.
- The final verdict would require a human product/default/scientific decision
  not authorized by this program.
- Claude/Codex review does not converge within five rounds for the same
  blocker.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write final result or blocker result.
3. Update ledgers and stop handoff.
4. Run final Claude read-only review.
5. Report final status to the user.
