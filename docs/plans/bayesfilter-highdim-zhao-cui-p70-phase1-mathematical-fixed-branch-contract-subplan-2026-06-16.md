# P70 Phase 1 Subplan: Mathematical Fixed-Branch Contract Audit

metadata_date: 2026-06-16
status: READY_AFTER_PHASE0_LOCAL_RESULT_PENDING_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded; MathDevMCP for derivation checks

## Phase Objective

Write the mathematical contract for the intended UKF-guided fixed branch before
implementation.  The output should be proposition/proof style, human-readable,
and precise enough that later code can be audited against it.

The phase must explain:

- the adaptive Zhao--Cui route and why it uses propagated samples, local
  coordinates, adaptive fitting, and defensive density;
- the fixed-HMC adaptation and why branch choices must be frozen before
  differentiating a likelihood;
- how UKF scout output may choose \(\mu_t\), \(L_t\), \(\Omega_t\), and a
  design measure \(\mathcal D_t\) without becoming a correctness oracle;
- what it means for the fitted tensor train to use declared rank channels;
- what normalizer, holdout, and replay gates are required before validation.
- why the p50 constant-path initialization proposition remains a nonzero
  starting-branch result but is not, by itself, a rank-channel activation
  guarantee for the P70 repair.

## Entry Conditions Inherited From Phase 0

Phase 1 may begin only after Phase 0 produces:

- the Phase 0 source-anchor reset result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase0-governance-source-anchor-reset-result-2026-06-16.md`;
- an anchor inventory with p50, code, and author-source line anchors;
- a bug/gap classification for current rank-channel inactivity and
  degree-normalizer instability;
- a claim-boundary table distinguishing `source_faithful`,
  `fixed_hmc_adaptation`, and `extension_or_invention`;
- a threshold-provenance placeholder naming where later threshold values must
  be frozen before repaired diagnostics are observed;
- paper-anchor quarantine language stating that no new `source_faithful` claim
  is allowed until Phase 1 adds or cites Zhao--Cui paper anchors.

Phase 1 may be launched only after this Phase 1 subplan and the Phase 0 result
receive Claude `VERDICT: AGREE`.  That review approval is a launch gate, not a
Phase 0 output.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase1-mathematical-fixed-branch-contract-result-2026-06-16.md`.
- Threshold-provenance register, either inside the Phase 1 result or as a
  linked artifact, stating which quantities are mathematical admissibility
  predicates and which later phase must freeze their numerical tolerances
  before any repaired diagnostic is run.
- If p50 is edited, a focused p50 patch and a rebuilt/checkable PDF artifact
  or an explicit reason PDF build is deferred.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase2-current-code-gap-audit-subplan-2026-06-16.md`.

## Required Checks/Tests/Reviews

Local document checks:

```bash
rg -n "computeL-style|const-style|source shift|machine|executable source route" docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex
rg -n "UKF|fixed branch|Zhao--Cui|defensive|normalizer|rank channel" docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex
```

MathDevMCP checks:

- Audit the labeled fixed-branch normalizer and any new propositions.
- Audit the UKF-guided branch-builder derivation if a new label is added.
- Audit code/document correspondence only after Phase 2 or later creates a code
  target.

Claude review:

- Review for mathematical correctness, source-anchor discipline, and human
  readability.
- Reject machine-facing phrases such as "computeL-style mean" or
  "const-style source shift" in monograph prose.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact fixed mathematical scalar should the UKF-guided fixed-branch implementation evaluate and differentiate? |
| Baseline/comparator | Phase 0 anchor ledger, p50 fixed-branch section, p50 UKF-scout section, Zhao--Cui paper/source anchors, and P69 Phase 5c bug diagnosis. |
| Primary criterion | A proposition/proof-style contract defines \(B_t\), \(\mu_t,L_t,\Omega_t,\mathcal D_t,c_t,\phi_t,\tau_t,\lambda_t,\zeta_t^B\), channel-activity and normalizer admissibility predicates, threshold-provenance responsibilities, and clear source/fixed-adaptation classifications. |
| Veto diagnostics | UKF called truth; adaptive route differentiated; machine-facing prose in monograph text; missing citations/anchors; low/high closeness gate; in-sample residual as correctness; source-faithful claim without anchors. |
| Explanatory diagnostics | MathDevMCP derivation checks, Claude readability review, source-anchor table, exact nonclaim list. |
| Not concluded | No code repair, no validation, no HMC readiness, no adaptive parity. |
| Artifact preserving result | Phase 1 result and any p50 patch/PDF artifact if edited. |

## Forbidden Claims/Actions

- Do not implement code in Phase 1.
- Do not claim the current code satisfies the new contract.
- Do not claim UKF validates the branch.
- Do not claim degree 2 is accepted or rejected generally.
- Do not use source-code helper names as mathematical terms in p50 prose.
- Do not edit unrelated monograph chapters.
- Do not freeze numerical thresholds after observing repaired diagnostic
  results.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if Phase 1 produces:

- a mathematical fixed-branch contract with labeled objects and propositions;
- a source/fixed-adaptation classification for UKF-guided branch construction;
- a reconciliation note explaining that constant-path initialization guarantees
  nonzero fitted mass at initialization but does not guarantee activation of
  declared higher-rank channels after a one-sweep fixed fit;
- Zhao--Cui paper-anchor additions for any operation claimed as
  `source_faithful`;
- a threshold-provenance register assigning numerical threshold freezing to
  Phase 3, Phase 4, Phase 6, or Phase 7 before any corresponding diagnostic is
  run;
- an executable-diagnostic approval note stating that Phase 0/1 authorize only
  further audit/design and that Phase 6/7 require separate reviewed evidence
  contracts and explicit user approval before execution;
- an explicit list of implementation surfaces to audit;
- local document checks completed;
- MathDevMCP evidence for new or modified derivations where applicable;
- Claude `VERDICT: AGREE`;
- a refreshed Phase 2 subplan.

## Stop Conditions

Stop and write a blocker if:

- the mathematical contract cannot be made consistent with p50 or source
  anchors;
- a needed claim lacks a derivation or citation;
- MathDevMCP flags an unresolved derivation issue;
- Claude and Codex do not converge after five material review rounds;
- the phase needs implementation evidence before the contract can be stated.

## Skeptical Plan Audit

Known risk: writing implementation jargon into a monograph chapter.  Phase 1
must write mathematical objects first and reserve machine status labels for
ledgers, manifests, and result files.
