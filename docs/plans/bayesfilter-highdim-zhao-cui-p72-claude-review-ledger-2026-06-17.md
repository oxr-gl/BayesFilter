# P72 Claude Review Ledger

metadata_date: 2026-06-17
status: PHASE5_BLOCKED_REAL_DIAGNOSTIC_CLAUDE_AGREE_PHASE6_ROOT_CAUSE_ONLY
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md

## Reviews

### Repair Note Review R1

Artifact:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.tex`

Claude verdict:

- `VERDICT: REVISE`

Accepted findings:

- The note needed to narrow "support-certified" to finite diagnostic
  certification.
- The fit-residual proposition should be read as an empirical residual claim,
  not a claim about the whole regularized objective.
- Guard targets needed a definition.
- Line-probe observables needed a precise finite definition.
- Weighted aggregate guard loss can hide spikes, so max/per-point gates were
  required.
- Conditioning gates needed explicit scaling and effective-rank conventions.

Codex repair:

- Retitled and reframed as finite-support-certified fixed fit.
- Added finite-diagnostic and non-continuum limitations.
- Defined guard targets as frozen-branch target evaluations unless a surrogate
  is separately reviewed.
- Defined finite line paths and observable classes.
- Added aggregate and maximum guard/audit gates.
- Required deterministic invertible column scaling and predeclared
  effective-rank convention.

### Repair Note Review R2

Artifact:

- repaired note above.

Claude verdict:

- `VERDICT: AGREE`

Summary:

- Claude accepted the repaired note as sufficient to govern implementation
  planning.
- Claude agreed source-governance anti-overclaim and downstream-validation
  nonclaims remain intact.

## Pending

### Master/Runbook Review R1

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md`

Claude verdict:

- `VERDICT: REVISE`

Accepted findings:

- Phase 5 decisive diagnostic needed a mandatory serious-run manifest.
- "Phase 7" naming was ambiguous between P72 administrative closeout and
  blocked downstream validation ladder.
- Runbook approvals needed to explicitly cover visible source-code edits on
  reviewed implementation surfaces only.

Codex repair:

- Added serious-run manifest as Phase 5 required output and Phase 6 input.
- Renamed Phase 6 to downstream validation-planning decision and Phase 7 to
  administrative closeout.
- Reworded forbidden actions to ban downstream validation ladder execution
  during P72.
- Added explicit source-code edit approval boundary for reviewed Phase 3/4
  surfaces.

## Pending

### Master/Runbook Review R2

Artifacts:

- repaired master program, runbook, and review ledger above.

Claude verdict:

- `VERDICT: AGREE`

Summary:

- Claude accepted the serious-run manifest requirement for Phase 5.
- Claude accepted the downstream-validation versus administrative-closeout
  separation.
- Claude accepted the explicit source-code edit boundary for reviewed
  implementation surfaces only.

## Pending

### Phase 0 Closeout And Phase 1 Subplan Review

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-subplan-2026-06-17.md`

Claude verdict:

- `VERDICT: AGREE`

Accepted findings:

- Phase 0 stays within documentation/governance closeout and does not
  overclaim repair, validation, HMC readiness, adaptive parity, original
  Zhao--Cui failure, or MathDevMCP proof.
- Phase 1 inherits the source-governance boundary: source-faithfulness claims
  require both Zhao--Cui paper anchors and local author-source file/line
  anchors, otherwise the plan blocks with source-ungrounded status.
- Phase 1 entry conditions are produced by Phase 0, and Phase 2 handoff
  conditions are restrictive enough.
- Required artifacts, checks, evidence contract, forbidden actions, and stop
  conditions are sufficient for the stated scope.

Codex action:

- Updated Phase 0 result, Phase 1 subplan, review ledger, and execution ledger
  statuses to reflect `VERDICT: AGREE`.

### Phase 1 Result And Phase 2 Subplan Review

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-subplan-2026-06-17.md`

Claude R1 verdict:

- `VERDICT: REVISE`

Accepted findings:

- Phase 1 classification coverage and limited source-faithful anchors were
  mostly sound, and guard/stability additions stayed outside source-faithful
  status.
- Stable weighted least-squares, Christoffel/leverage, and oversampling
  support remained correctly labeled as `SOURCE_GAP_BLOCKER` for theorem-level
  use.
- Phase 2 did not yet tightly require every borrowed P70/P71 diagnostic
  observable to be remapped through a Phase 1 classification row.
- Phase 2 did not yet explicitly quarantine optional shape penalties,
  derivative-energy penalties, line-growth objective penalties,
  Christoffel/leverage/oversampling ideas, and stable least-squares theorem
  claims from becoming mandatory without a separate reviewed derivation or
  literature audit.
- Phase 2 entry conditions allowed "patched" findings without requiring a
  clean post-patch review, which was weaker than the review gate requires.

Codex repair:

- Patched the Phase 2 subplan to require a clean post-patch Claude review
  before Phase 2 begins.
- Added an imported-observable admission table requirement for every borrowed
  P70/P71 diagnostic term and repair-note candidate.
- Added veto, forbidden-action, handoff, and stop-condition language blocking
  unclassified observables and unaudited optional shape/stability candidates
  from becoming mandatory contract elements.

Status:

- Focused local checks passed and Claude R2 returned `VERDICT: AGREE`.

### Phase 1 Result And Phase 2 Subplan Review R2

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`

Claude verdict:

- `VERDICT: AGREE`

Summary:

- Claude agreed the repaired Phase 2 subplan requires every imported P70/P71
  diagnostic vocabulary item and repair-note candidate to map to a Phase 1
  classification row or be excluded from the mandatory contract.
- Claude agreed optional shape penalties, derivative-energy penalties,
  line-growth objective penalties, Christoffel/leverage/oversampling ideas,
  and stable least-squares theorem claims remain quarantined unless a separate
  reviewed derivation or literature audit closes the gap.
- Claude agreed Phase 2 entry now requires a clean post-patch review and does
  not treat attempted patches as sufficient.
- Claude found no new wrong baseline, proxy-metric promotion, unsupported
  source-faithful claim, artifact mismatch, or design-only boundary violation.

### Phase 2 Result And Phase 3 Subplan Review R1

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md`

Claude verdict:

- `VERDICT: REVISE`

Accepted findings:

- The Phase 2 result defined the main clouds, objective structure, thresholds,
  and pass/block semantics well, but the line-residual gate had an ambiguity:
  direct target evaluation needed to be mandatory for every line-probe point,
  not conditional on target availability.
- Normalizer gates needed to make required quantities mandatory; "when both
  are present" for fit mass fraction was too weak for an admission gate.
- The line absolute-value gate used `s_line = max(s_y, max_abs(h on Z_fit))`,
  which could loosen if fitted on-cloud predictions inflated.  The line gate
  needed a fixed target-scale ceiling and a separate pairwise endpoint-growth
  check.
- The effective-rank imported-observable row mixed inherited solver
  observables with invented admission gates and needed to be split.

Codex repair:

- Made direct frozen-branch target evaluation mandatory for every guard,
  audit, and line-probe point.
- Changed line absolute-value ceiling to `G_max = 1e3 * s_y` and added a
  pairwise endpoint-growth gate based on each selected line-start prediction.
- Made normalizer fit mass fraction block if either required normalizer term is
  absent.
- Split inherited scaled-solve condition observables from the P72
  condition/effective-rank admission gate.

Status:

- Awaiting focused local checks and Claude R2 review.

### Phase 5a Repair Subplan Review R2

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-skeptical-audit-blocker-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`

Claude verdict:

- `VERDICT: AGREE`

Summary:

- Claude agreed the repaired Phase 5a subplan could govern the runner repair
  after the schema-only blocker.
- Claude agreed Phase 5 could resume only after the implementation emitted a
  real non-schema diagnostic artifact and passed focused checks.

### Phase 5a Implementation Review R1

Artifacts:

- `scripts/p72_support_certified_lower_gate_diagnostic.py`
- `tests/highdim/test_p72_support_certified_lower_gate.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-runner-smoke-2026-06-17.json`

Claude verdict:

- `VERDICT: REVISE`

Accepted finding:

- Claude found that Phase 5a had added `--smoke-only`, but the default
  no-flag path still did not execute real bounded Phase 5 rows.  This meant
  Phase 5 would still not answer its evidence contract.

Codex repair:

- Patched the default path to run real bounded Phase 5 rows.
- Kept `--schema-only` and `--smoke-only` as explicit non-Phase-5 paths.
- Added fail-closed row handling for unexpected exceptions.
- After the real run exposed a known `NORMALIZER_FLOOR_EXCEEDED` row abort,
  patched the normalizer gate and row builder to record that failure as
  structured gate/skip evidence rather than a top-level exception row.

### Phase 5a/5 Repaired Execution Review R2

Artifacts:

- `scripts/p72_support_certified_lower_gate_diagnostic.py`
- `bayesfilter/highdim/source_route.py`
- `tests/highdim/test_p72_support_certified_lower_gate.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase6-downstream-validation-decision-subplan-2026-06-17.md`

Claude verdict:

- `VERDICT: AGREE`

Summary:

- Claude agreed this is a valid blocked diagnostic closeout, not a success
  closeout.
- Claude agreed the default path now matches the Phase 5 purpose and that
  schema/smoke sentinels no longer contaminate the artifact.
- Claude agreed the structured `NORMALIZER_FLOOR_EXCEEDED` evidence reports
  the mathematical blocker rather than hiding it.
- Claude agreed the step-2 skip after the step-1 normalizer block is correct
  fail-closed behavior because no admissible retained object exists.
- Claude agreed there is no basis for downstream validation, HMC readiness,
  scaling, rank/degree promotion, or a lower-gate pass claim.

Status:

- Phase 5 closeout review passed; Phase 6 must remain root-cause-only.

### Phase 5a Repair Subplan Review R2

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-skeptical-audit-blocker-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`

Claude verdict:

- `VERDICT: AGREE`

Summary:

- Claude agreed the Phase 5a subplan now requires a bounded non-Phase-5
  `--smoke-only` invocation, non-schema JSON, structural JSON validation, and
  explicit sentinel-absence evidence.
- Claude agreed the Required Artifacts section and stale-status repairs are
  sufficient.
- Claude found no new wrong-baseline issue, proxy-promotion drift, boundary
  violation, or command ambiguity.

Status:

- Phase 5a implementation may begin.

### Phase 2 Result And Phase 3 Subplan Review R2

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`

Claude verdict:

- `VERDICT: REVISE`

Accepted findings:

- Claude agreed the R1 design blockers were fixed: line residuals now have
  mandatory direct target evaluation; normalizer gates require the necessary
  quantities; line absolute-value and growth gates cannot loosen through
  unrelated on-fit prediction inflation; and effective-rank classification is
  split between inherited fixed-solver observable and P72 admission gate.
- Claude found one remaining artifact issue: the top-level metadata status of
  this review ledger still claimed Phase 1 pending review.

Codex repair:

- Updated top-level review-ledger and execution-ledger status metadata to
  reflect the current Phase 2 R2 repair state.

Status:

- Focused local checks passed and Claude R3 returned `VERDICT: AGREE`.

### Phase 2 Result And Phase 3 Subplan Review R3

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md`

Claude verdict:

- `VERDICT: AGREE`

Summary:

- Claude agreed the stale top-level ledger status blocker was resolved.
- Claude found no new artifact mismatch or design-boundary regression.
- Phase 2 design is accepted for Phase 3 no-edit implementation-surface audit.

### Phase 3 Result And Phase 4 Subplan Review R1

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md`

Claude verdict:

- `VERDICT: REVISE`

Accepted findings:

- Phase 3 did not explicitly map support/clipping coverage diagnostics, full
  normalizer gate coverage, and branch/provenance/hash invariants to required
  Phase 4 helpers and tests.
- The authorized edit-surface list omitted required non-code artifacts under
  `docs/plans`, creating a mismatch with Phase 4 required artifacts.
- The conditional `fitting.py` permission and a Phase 3 sentence risked
  lowering the low-level solver veto to `1e10`, whereas Phase 2 freezes
  `1e10` as a P72 wrapper/admission gate and retains `1e14` as the hard
  solver-veto compatibility reference.

Codex repair:

- Added explicit support/clipping coverage helper and focused tests.
- Added explicit full-normalizer and provenance/hash/branch-invariance helper
  and test requirements.
- Authorized required non-code artifact writes under `docs/plans`.
- Tightened `fitting.py` permission: diagnostic exposure only, no objective,
  backend, solver-threshold, default-backend, or non-P72 behavior changes.
- Stated that P72 `kappa_max=1e10` is enforced at the wrapper/admission gate,
  not by lowering the low-level solver veto.

Status:

- Awaiting focused local checks and Claude R2 review.

### Phase 3 Result And Phase 4 Subplan Review R2

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`

Claude verdict:

- `VERDICT: REVISE`

Accepted findings:

- Claude agreed the R1 blockers were repaired: support/clipping coverage,
  full-normalizer coverage, provenance/hash requirements, `docs/plans`
  artifact authorization, diagnostic-only `fitting.py` permission, and the
  `1e14` solver-veto versus `1e10` P72 wrapper/admission distinction were
  covered.
- Claude found one remaining artifact issue: the top-level review-ledger
  metadata still claimed Phase 2 status even though the body had advanced to
  Phase 3 review.

Codex repair:

- Updated the review-ledger and execution-ledger status metadata to reflect the
  Phase 3 R2 metadata-repair state.

Status:

- Focused local checks passed and Claude R3 returned `VERDICT: REVISE` for a
  remaining execution-ledger body synchronization issue.

### Phase 3 Result And Phase 4 Subplan Review R3

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md`

Claude verdict:

- `VERDICT: REVISE`

Accepted findings:

- Claude agreed the review-ledger metadata no longer falsely claimed Phase 2.
- Claude found that the execution-ledger body had not recorded the Phase 3
  R2/R3 metadata repair sequence advertised by the headers.

Codex repair:

- Added an execution-ledger body entry documenting the Phase 3 R2/R3
  metadata-repair sequence.
- Updated both ledger headers to the current Phase 3 R3 body-repair state.

Status:

- Focused local checks passed and Claude R4 returned `VERDICT: REVISE` for a
  remaining review-ledger body synchronization issue.

### Phase 3 Result And Phase 4 Subplan Review R4

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md`

Claude verdict:

- `VERDICT: REVISE`

Accepted findings:

- Claude agreed the execution-ledger body now records the Phase 3 R2/R3
  metadata-repair sequence and that the headers no longer falsely present
  Phase 2 as current.
- Claude found that this review-ledger body still ended at "awaiting Claude
  R3 review" and therefore did not record the R2/R3/R4 sequence advertised by
  the header and execution ledger.

Codex repair:

- Rewrote the review-ledger tail from Phase 2 R1 onward into chronological
  order, preserving the accepted findings and removing duplicate/misordered
  headings.
- Updated both ledger headers to the current Phase 3 R4
  review-ledger-body-repair state.

Status:

- Awaiting focused local checks and Claude R5 review.

### Phase 3 Result And Phase 4 Subplan Review R5

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md`

Claude verdict:

- `VERDICT: AGREE`

Summary:

- Claude agreed the review-ledger tail is chronological and no longer
  duplicated or misordered.
- Claude agreed the review ledger and execution ledger both document the Phase
  3 R2/R3/R4 metadata/body synchronization sequence.
- Claude found no new artifact mismatch, stale metadata, boundary-safety
  regression, wrong-baseline/proxy-promotion drift, unsupported
  source-faithful claim, or solver-veto confusion.

Status:

- Phase 3 passed; Phase 4 may begin.

### Phase 4 Implementation Result And Phase 5 Subplan Review R1

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md`
- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `scripts/p72_support_certified_lower_gate_diagnostic.py`
- `tests/highdim/test_p72_support_certified_lower_gate.py`

Claude verdict:

- `VERDICT: AGREE`

Summary:

- Claude agreed the Phase 4 required surfaces are covered: frozen P72 policy,
  fit/guard batch construction with audit exclusion, support/clipping gates,
  line gates with direct target values, full normalizer gate, condition and
  effective-rank wrapper admission, provenance hashes, rank-activity
  propagation, P72 schema script, and focused tests.
- Claude agreed the low-level solver veto remains `1e14` and that `1e10` is
  only the P72 wrapper/admission threshold.
- Claude did not find audit clouds entering coefficient selection.
- Claude agreed the schema-only script is acceptable for Phase 4 because Phase
  5 explicitly stops if it remains schema-only.
- Claude did not find a material source-faithfulness overclaim,
  wrong-baseline issue, proxy-promotion drift, NumPy-backend violation, or
  unauthorized downstream execution claim.

Nonblocking caveat:

- The current script output is still a Phase 4 schema artifact, not a full
  Phase 5 diagnostic artifact.  It must not be interpreted as repaired
  diagnostic evidence.

Status:

- Phase 4 passed; Phase 5 may begin only after its skeptical plan audit.

### Phase 5 Blocker And Phase 5a Repair Subplan Review R1

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-skeptical-audit-blocker-result-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`

Claude verdict:

- `VERDICT: REVISE`

Accepted findings:

- Claude agreed that blocking Phase 5 execution was logically correct and
  required because the Phase 5 subplan stops when the script remains
  schema-only.
- Claude found that the Phase 5a subplan was directionally sound but needed a
  mandatory bounded default-path smoke invocation that emits a non-schema JSON
  artifact, validates JSON structurally, and proves the schema sentinel is not
  present.
- Claude found the Phase 5a subplan needed an explicit Required Artifacts
  section.
- Claude found stale metadata in the visible execution ledger and Phase 5
  subplan.

Codex repair:

- Added explicit Phase 5a required artifacts.
- Added the mandatory `--smoke-only` default-path invocation, JSON validation,
  and sentinel-absence check.
- Updated the Phase 5 subplan status and added a current-status note.
- Updated execution and review ledger headers to the Phase 5a R2-pending
  state.

Status:

- Awaiting focused local checks and Claude R2 review.
