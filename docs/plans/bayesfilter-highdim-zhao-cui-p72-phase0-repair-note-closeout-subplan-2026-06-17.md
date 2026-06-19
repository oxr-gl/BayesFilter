# P72 Phase 0 Subplan: Repair-Note Closeout And Governance Reset

metadata_date: 2026-06-17
status: READY_FOR_VISIBLE_LAUNCH_AFTER_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Close out the P72 mathematical repair note as the governing document for the
support-certified fixed-fit implementation plan.  Record local checks,
MathDevMCP diagnostic status, Claude convergence, PDF production, and the
nonclaim/source-governance boundary.  Draft the Phase 1 source/literature
boundary subplan.

## Entry Conditions Inherited From Previous Work

Phase 0 may begin only after:

- P70 Phase 6h result exists and keeps Phase 7 blocked;
- P72 repair note exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.tex`;
- the note has been reviewed by Claude until convergence or a blocker;
- no implementation code has been changed for P72.

## Required Artifacts

- this Phase 0 subplan;
- P72 repair note and PDF:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.tex`,
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.pdf`;
- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-result-2026-06-17.md`;
- P72 Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`;
- P72 execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`;
- refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-subplan-2026-06-17.md`.

## Required Checks, Tests, And Reviews

Local checks:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.tex
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.tex
rg -n "Overfull|undefined references|Fatal error" bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.log
```

MathDevMCP checks:

- `audit_derivation_v2_label` for `prop:p72-fit-not-support`;
- `audit_derivation_v2_label` for `prop:p72-guard-control`;
- `audit_derivation_v2_label` for `prop:p72-admission-excludes-phase6h`.

These are diagnostic-only unless the tool returns a verified proof
certificate.  Inconclusive parser/backend results must be recorded as
inconclusive, not as proof.

Claude review:

- bounded read-only review of the repair note;
- if Claude returns `VERDICT: REVISE`, patch the note visibly, rerun focused
  local checks, and request focused re-review;
- stop after five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the P72 mathematical repair note good enough to govern implementation planning for the Phase 6h off-cloud/conditioning blocker? |
| Baseline/comparator | P70 Phase 6h failed evidence, P72 note, MathDevMCP diagnostic output, Claude note review. |
| Primary criterion | Phase 0 result records a successful PDF build, no overfull/unresolved-reference warnings after repair, `git diff --check` pass, MathDevMCP status honestly recorded, and Claude `VERDICT: AGREE` for the repaired note. |
| Veto diagnostics | Note overclaims continuum support, source-faithfulness, original Zhao--Cui failure, Phase 7 readiness, or validation; missing guard target definition; missing line-probe observable; missing conditioning scaling convention; PDF build failure. |
| Explanatory only | Underfull table warnings, MathDevMCP parser/backend inconclusive results, literature directions not yet audited. |
| Not concluded | No implementation, no diagnostic repair, no Phase 7 authorization, no d18 accuracy, no HMC readiness, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 0 result and P72 ledgers. |

## Forbidden Claims And Actions

- Do not edit production code.
- Do not run repaired diagnostics.
- Do not run Phase 7 or d18 validation.
- Do not claim MathDevMCP proof if the tool is inconclusive.
- Do not claim literature support beyond locally inspected or explicitly
  caveated sources.
- Do not claim the original Zhao--Cui adaptive method fails.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- Phase 0 result exists;
- Claude agrees the repaired note is sufficient for planning;
- the Phase 1 subplan exists and inherits the source-governance boundary;
- Phase 0 states that no code/diagnostic work has yet been launched.

## Stop Conditions

Stop and write a blocker if:

- LaTeX build fails;
- Claude finds a material note flaw that cannot be patched within five rounds;
- the note cannot avoid overclaiming source-faithfulness or validation;
- the user redirects the lane.

## Skeptical Plan Audit

This phase is safe to execute because it closes documentation and governance
before implementation.  It does not use fit residuals, diagnostic commands, or
implementation outputs as promotion evidence.  The main risk is treating the
mathematical note as stronger than it is; the evidence contract therefore
requires recording finite-diagnostic scope and nonclaims.
