# P72 Phase 2 Subplan: Support-Certified Design Contract

metadata_date: 2026-06-17
status: READY_FOR_PHASE2_EXECUTION_CLAUDE_R2_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Write a design-only contract for the finite-support-certified fixed lower gate.
The contract must freeze, before implementation and before repaired diagnostic
outputs are seen:

- guard-cloud and audit-cloud construction rules;
- line-probe paths and observable statistics;
- finite target definitions for fit, guard, and audit points;
- aggregate and maximum residual gates;
- normalizer and defensive-mass gates;
- column scaling, singular-spectrum, condition-number, and effective-rank
  conventions;
- rank-direction activity diagnostics;
- classification labels for every design element.

This phase does not edit production code and does not run repaired diagnostics.

## Entry Conditions Inherited From Phase 1

Phase 2 may begin only if:

- Phase 1 result exists and includes the classification ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md`;
- Claude review of the Phase 1 result and this Phase 2 subplan returns
  `VERDICT: AGREE` after any material findings have been patched and
  re-reviewed; attempted patches without a clean post-patch review do not
  satisfy this entry condition;
- P70 Phase 6h remains the failed baseline;
- no production code edit or repaired diagnostic has occurred in P72;
- all support-certified additions are treated as `extension_or_invention` or
  `fixed_hmc_adaptation`, not as source-faithful Zhao--Cui behavior;
- downstream validation and d18 validation remain blocked.

## Required Artifacts

Phase 2 must produce:

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md`;
- finite design contract embedded in the Phase 2 result, including:
  guard/audit cloud definitions, line-probe definitions, residual metrics,
  normalizer metrics, condition/effective-rank metrics, activity metrics, and
  threshold provenance;
- classification table preserving Phase 1 labels for every design element;
- imported-observable admission table mapping every borrowed P70/P71
  diagnostic term and every repair-note candidate to a Phase 1 classification
  row, or else excluding it from the mandatory Phase 2 contract;
- explicit statement of thresholds that are frozen before Phase 4
  implementation and Phase 5 diagnostic execution;
- updated P72 execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`;
- updated P72 Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`;
- refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md`.

## Required Checks, Tests, And Reviews

Local read-only checks before writing the Phase 2 result:

```bash
test -f docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-result-2026-06-17.md
rg -n "H4 off-cloud|Row-B|line reaches|condition|raw holdout|replay" docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-result-2026-06-17.md
rg -n "guard|line-probe|maximum|conditioning|effective-rank|normalizer|rank-direction" docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.tex docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md
```

Local checks after writing the Phase 2 result and Phase 3 subplan:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md
rg -n "G_max|R_max|kappa|max residual|line-probe|guard cloud|audit cloud|effective-rank|extension_or_invention|fixed_hmc_adaptation|not concluded" docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md
```

Reviews:

- Codex skeptical plan audit before executing Phase 2.
- Claude read-only review of the Phase 2 result and refreshed Phase 3 subplan.
- If Claude returns `VERDICT: REVISE`, patch visibly and rerun focused checks.
  Stop after five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact finite guard/audit/line/conditioning contract should the fixed-variant repair implement and diagnose? |
| Baseline/comparator | P70 Phase 6h failed evidence, P72 repair note, Phase 1 classification ledger, and current P70/P71 diagnostic vocabulary only after each borrowed observable is remapped to a Phase 1 classification row. |
| Primary criterion | The Phase 2 result freezes finite cloud rules, observables, thresholds, scaling/effective-rank conventions, classification labels, and pass/block semantics before implementation or repaired diagnostic output. |
| Veto diagnostics | Thresholds left vague; fit residual used as sole pass criterion; low/high branch closeness introduced as a pass criterion; guard additions called source-faithful; downstream validation authorized; Phase 3 allowed to edit code without an implementation-surface map; any design depends on seeing Phase 5 outputs first; a P70/P71 observable is admitted without Phase 1 classification; shape penalties, derivative-energy penalties, line-growth objective penalties, Christoffel/leverage/oversampling, or stable least-squares candidates become mandatory without a separate reviewed derivation or literature audit. |
| Explanatory only | Literature candidate directions, rough implementation difficulty, expected runtime, optional shape or stability ideas that remain quarantined, and optional future continuum-support theory. |
| Not concluded | No implementation, no diagnostic pass, no continuum support theorem, no d18 validation, no HMC readiness, no source-faithfulness closure for guard/stability additions, no original Zhao--Cui failure claim. |
| Artifact preserving result | Phase 2 result, execution ledger, review ledger, and Phase 3 subplan. |

## Required Design Contents

The Phase 2 result must specify at least:

- `Z_fit`: the fitting cloud inherited from the fixed branch;
- `Z_guard`: deterministic guard points generated before fitting;
- `Z_audit`: holdout/replay/audit points not used for coefficient selection;
- an imported-observable admission table: each P70/P71 term, repair-note
  term, and diagnostic statistic used by the contract must point to one Phase
  1 classification row and one admitted role;
- line-probe pairs and finite fractions \(S\subset[0,1]\);
- target evaluation rule for every fit/guard/audit point;
- aggregate weighted residuals and maximum pointwise residuals;
- line-probe absolute value, residual, and growth statistics;
- squared-density normalizer and defensive-mass checks;
- column scaling rule and scale-floor convention;
- singular-value, condition-number, and effective-rank thresholds;
- rank-direction activity observable and threshold;
- exact pass/block table for Phase 5;
- exact nonclaims and source-governance labels.

## Forbidden Claims And Actions

- Do not edit production code.
- Do not run repaired diagnostics, Phase 7 validation, d18 validation, HMC, or
  GPU diagnostics.
- Do not use fit residual alone as a promotion criterion.
- Do not introduce low/high branch closeness as a success criterion.
- Do not call guard clouds, line probes, max gates, or activity gates
  source-faithful.
- Do not admit a P70/P71 diagnostic observable merely because it appeared in
  earlier artifacts; Phase 2 must classify it through the Phase 1 ledger before
  it can enter the contract.
- Do not make shape penalties, derivative-energy penalties, line-growth
  objective penalties, Christoffel/leverage/oversampling ideas, or stable
  least-squares theorem claims mandatory unless a separate reviewed derivation
  or literature audit closes the Phase 1 source gap.
- Do not change thresholds after seeing repaired diagnostic outputs.
- Do not authorize Phase 4 implementation; Phase 3 must first map surfaces and
  tests.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- Phase 2 result exists and contains the required design contract;
- every design element has a Phase 1-compatible classification label;
- every imported P70/P71 observable or repair-note candidate used in the
  contract is mapped to a Phase 1 classification row;
- thresholds and observables are frozen before implementation;
- Phase 3 subplan exists and maps the design to implementation surfaces
  without editing code;
- local checks pass;
- Claude returns `VERDICT: AGREE` for Phase 2 result and Phase 3 subplan.

## Stop Conditions

Stop and write a blocker if:

- a needed threshold cannot be set without seeing repaired diagnostic outputs;
- the design would require unapproved source-faithfulness claims;
- the design requires a P70/P71 observable that cannot be mapped to a Phase 1
  classification row;
- the design would require mandatory shape-penalty, Christoffel/leverage,
  oversampling, or stable least-squares support before a separate reviewed
  derivation or literature audit is available;
- Phase 2 cannot define guard/audit clouds without using implementation
  details that require code edits first;
- Phase 3 would need to implement unclassified behavior;
- Claude and Codex do not converge after five review rounds for the same
  blocker;
- the user redirects the lane.

## Skeptical Plan Audit

This phase is appropriate only after Phase 1 review because it consumes the
classification ledger.  Its main risk is threshold gaming or proxy promotion.
The phase controls that risk by freezing observables and pass/block semantics
before implementation and by making fit residual an explanatory input rather
than a success criterion.  It also controls source-boundary leakage by
requiring each borrowed P70/P71 diagnostic vocabulary item and each optional
repair-note candidate to pass through the Phase 1 classification ledger before
becoming part of the mandatory design contract.
