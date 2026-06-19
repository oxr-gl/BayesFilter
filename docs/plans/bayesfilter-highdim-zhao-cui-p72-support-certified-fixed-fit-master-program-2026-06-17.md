# P72 Master Program: Support-Certified Fixed-Fit Repair

metadata_date: 2026-06-17
status: READY_FOR_USER_LAUNCH_APPROVAL_CLAUDE_AGREE
executor: Codex in the current conversation
reviewer: Claude Opus max effort, read-only and bounded
governing_note: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.tex

## Objective

Repair the P70 Phase 6h fixed-variant blocker by implementing a
finite-support-certified fixed square-root TT fit.  The repair must target:

- H4 off-cloud square-root TT growth: tiny fit residuals but explosive
  holdout/replay/line-probe values;
- H8/H3 row-B conditioning failure: a rank-three local ALS system with
  near-null singular directions and condition-number veto.

This program is not a Zhao--Cui adaptive reproduction lane.  It is a
fixed-HMC adaptation and stabilization lane.  Guard objective terms, explicit
off-cloud gates, max residual gates, and stable-sampling ideas are
`extension_or_invention` unless a later phase proves paper and author-source
anchors.  Downstream validation-ladder planning remains blocked until the
repaired lower gate passes under a reviewed evidence contract.

## Starting Evidence

The governing evidence is:

- P70 Phase 6h result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-result-2026-06-17.md`.
- P70 master and ledgers:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md`,
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-execution-ledger-2026-06-16.md`,
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-claude-review-ledger-2026-06-16.md`.
- Mathematical repair note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.tex`.

Phase 6h classifies the mechanisms as follows:

| Mechanism | Status | Consequence |
| --- | --- | --- |
| Off-cloud square-root TT growth | supported | Repair must add finite guard/line/max diagnostics, not just fit residual improvement. |
| Row-B design conditioning | supported | Repair must record scaling, singular spectra, effective-rank convention, and condition gates. |
| Normalized-metric amplification | weakened | Raw residuals are already enormous, so changing normalization is not a repair. |
| Target/shift/frame mismatch | weakened | Repair should not chase target bookkeeping as the main mechanism. |
| Support/effective-support mismatch | unresolved | Repair design must include support-coverage diagnostics without claiming this was fully proven. |

## Source-Governance Boundary

Every material design, implementation, result, and review statement must
classify new behavior as exactly one of:

- `source_faithful`: matches cited Zhao--Cui paper and cited author-source
  operation;
- `fixed_hmc_adaptation`: preserves the author's broad sequential TT/SIRT
  route but freezes choices to define a differentiable same scalar;
- `extension_or_invention`: changes the route beyond author paper/source and
  fixed-branch freezing.

Veto rule: any artifact that says "faithful", "source-faithful",
"paper-scale Zhao--Cui", "adaptive parity", or equivalent without paper
anchors and author-source file/line anchors blocks with
`BLOCK_SOURCE_UNGROUNDED`.

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a finite-support-certified fixed fit remove the observed off-cloud growth and conditioning blockers on the bounded P70 diagnostic scale without overclaiming source-faithfulness or validation? |
| Baseline/comparator | P70 Phase 6h failed evidence, unchanged model/row intent, P70 fixed-branch implementation surfaces, and the P72 mathematical repair note. |
| Primary program pass criterion | Every phase produces its required artifact and exact next-phase entry conditions, or writes a blocker.  The repaired diagnostic can advance only if predeclared finite guard, holdout/replay, line-probe, normalizer, rank-activity, and conditioning gates pass. |
| Veto diagnostics | Fit residual used as sole pass criterion; guard/line/audit thresholds chosen after seeing outputs; guard terms called source-faithful without anchors; downstream validation ladder launched before lower gate pass; UKF used as truth; low/high branch closeness used as promotion criterion; nonfinite normalizer or residuals; missing scaling/effective-rank convention. |
| Explanatory diagnostics | Fit residuals, guard residuals, max residuals, line-probe values/growth, singular spectra, condition numbers, effective ranks, rank-direction activity, normalizer components, support distances, clipping fractions, branch hashes. |
| Not concluded | No original Zhao--Cui failure claim, no adaptive parity, no d18 accuracy, no d50/d100 scaling, no HMC readiness, no source-faithfulness closure for guard/stability additions unless separately anchored. |
| Artifacts | P72 note/PDF, master program, runbook, execution ledger, review ledger, phase subplans/results, bounded diagnostic JSONs, implementation diffs when launched, stop handoff. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Mathematical repair-note closeout and governance reset | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-result-2026-06-17.md` |
| 1 | Source and literature boundary audit | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md` |
| 2 | Guard-cloud, line-probe, and conditioning design contract | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md` |
| 3 | Implementation surface audit and focused test plan | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md` |
| 4 | Focused implementation and unit tests | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-result-2026-06-17.md` |
| 5 | Bounded repaired lower-gate diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md` |
| 6 | Result review and downstream validation-planning decision | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase6-downstream-validation-decision-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase6-downstream-validation-decision-result-2026-06-17.md` |
| 7 | Administrative closeout, ledgers, and stop handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase7-administrative-closeout-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase7-administrative-closeout-result-2026-06-17.md` |

Only Phase 0 subplan is created before launch.  Every later phase subplan must
be drafted or refreshed at the close of the immediately previous phase.

## Dependency Matrix

| Phase | Must consume | Must produce for next phase |
| --- | --- | --- |
| 0 | P72 note, PDF, local checks, MathDevMCP diagnostic status, Claude note review | Repair-note closeout, nonclaim ledger, reviewed Phase 1 subplan |
| 1 | Phase 0 result, Zhao--Cui anchors, local bibliography, P70/P72 source-governance boundary | Classification ledger for each proposed repair operation, literature support/gap ledger, reviewed Phase 2 subplan |
| 2 | Phase 1 classification ledger and P72 note | Exact finite guard/audit/line/conditioning/rank-activity design contract, frozen observables and threshold provenance, reviewed Phase 3 subplan |
| 3 | Phase 2 design contract and current code | Implementation surface map, tests required before execution, risk controls, reviewed Phase 4 implementation subplan |
| 4 | Phase 3 surface map and tests | Code/tests implementing only reviewed surfaces, local check evidence, reviewed Phase 5 diagnostic subplan |
| 5 | Phase 4 implementation and reviewed evidence contract | Bounded repaired lower-gate diagnostic JSON, serious-run manifest, result note, explicit pass/block decision, reviewed Phase 6 decision subplan |
| 6 | Phase 5 result, serious-run manifest, and Claude execution review | Decision whether downstream validation planning remains blocked or a separate validation-ladder plan may be drafted; reviewed administrative closeout subplan |
| 7 | All prior artifacts | Final ledger, stop handoff, claim boundary, next justified action |

A phase may repair the blocker handed to it.  A phase must not require the
repair to have already succeeded before it begins.

## Phase Boundaries

### Phase 0: Mathematical repair-note closeout and governance reset

Close out the mathematical note as the governing design document.  Record
local checks, PDF production, MathDevMCP diagnostic-only status, and Claude
review convergence.  This phase creates no production code and runs no
diagnostic.

### Phase 1: Source and literature boundary audit

Classify each proposed repair operation before code.  Source-faithful claims
must cite Zhao--Cui paper and author-source anchors.  Literature directions for
stable least squares, Christoffel/leverage sampling, or TT-cross may be listed
as candidate support, but they remain source gaps until technical sections are
audited.

### Phase 2: Guard-cloud, line-probe, and conditioning design contract

Define the finite guard cloud, audit cloud, line-probe paths/statistics,
targets, weights, scaling convention, effective-rank convention, singular
spectrum gate, rank-direction activity gate, and normalizer gate.  Thresholds
must be frozen before implementation and before diagnostic outputs are seen.

### Phase 3: Implementation surface audit and focused test plan

Map the Phase 2 contract to current TensorFlow/TensorFlow Probability
implementation surfaces.  Identify exact functions and tests to change.  Do
not edit code in this phase except plan/result artifacts.

### Phase 4: Focused implementation and unit tests

Implement only the Phase 3-authorized surfaces.  New BayesFilter-owned
algorithmic code must use TensorFlow/TensorFlow Probability.  NumPy is allowed
only for references, fixtures, reporting, and explicitly reviewed exceptions.

### Phase 5: Bounded repaired lower-gate diagnostic

Run a bounded P70 Phase 6h-style diagnostic on the repaired path.  The primary
criterion is not fit residual improvement; the repaired path must pass
predeclared finite guard, holdout/replay, line-probe, normalizer,
rank-activity, and conditioning gates.

Phase 5 must also write a serious-run manifest before it can close.  The
manifest must record git commit or dirty-state summary, exact command,
environment or conda environment, CPU/GPU status, data/model/row specification,
random seeds, wall time, output artifact paths, governing subplan, result
file, and nonclaims.  Use `N/A` only when the field genuinely does not apply.

### Phase 6: Result review and downstream validation-planning decision

Review whether Phase 5 actually repairs the lower gate.  If any veto fails,
downstream validation planning remains blocked and the next action is repair or
blocker escalation.  If all gates pass, this phase may authorize drafting a
separate validation-ladder plan; it does not itself run that ladder.

### Phase 7: Administrative closeout, ledgers, and stop handoff

Refresh ledgers and write the final stop handoff.  Preserve nonclaims and list
the next justified human decision.

## Global Forbidden Actions

- Do not launch a detached process, nested agent, or copied-workspace runner.
- Do not execute the runbook before user launch approval.
- Do not run any downstream validation ladder or d18 validation during this
  P72 program.
- Do not use fit residual alone as a promotion criterion.
- Do not move thresholds after seeing outputs.
- Do not claim original Zhao--Cui failure.
- Do not claim source-faithfulness for guard/stability additions without paper
  and author-source anchors.
- Do not treat UKF as truth or low/high branch closeness as a promotion gate.

## Skeptical Plan Audit

This master program survives the initial skeptical audit because it uses the
actual Phase 6h failed evidence as baseline, makes the mathematical repair
note the first governing artifact, forbids downstream validation-ladder
execution during P72, and separates finite diagnostic certificates from
continuum, validation, and source-faithfulness claims.  P72 Phase 7 is
administrative closeout only.  The main remaining risks are threshold
overfitting, guard-cloud self-consistency without real support coverage,
missing run provenance, and source-governance overclaim.  These are assigned
to Phases 1--2 and Phase 5 before any validation-planning decision.
