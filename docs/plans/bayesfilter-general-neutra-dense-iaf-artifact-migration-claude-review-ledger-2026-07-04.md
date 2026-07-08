# BayesFilter Dense-IAF Migration Claude Review Ledger

Date: 2026-07-04

Status: `CLAUDE_REVIEW_LEDGER_OPEN`

## Role Contract

Codex is supervisor and executor. Claude is a read-only reviewer only.

Claude review must use exact-path prompts and bounded questions. Do not paste
whole files, broad bundles, or repo-wide instructions into Claude. Claude cannot
authorize crossing human, runtime, model-file, funding, product-capability, or
scientific-claim boundaries.

## Review Rounds

### 2026-07-04 - Master Program Review - Round 1

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-master-program-2026-07-04.md`

Question:

- Does this master program satisfy the requested gated dense-IAF migration
  design, with Codex as supervisor/executor, Claude as read-only reviewer,
  phase-by-phase repair loop, evidence boundaries, anticipated approval
  boundaries, and no unsupported migration/HMC/posterior claims?

Outcome:

- Claude found the role split, phase repair loop, evidence boundaries,
  anticipated approval boundaries, and nonclaims explicit.

Verdict:

- `VERDICT: AGREE`

### 2026-07-04 - Phase 1 Subplan Review - Round 1

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-subplan-2026-07-04.md`

Question:

- Is this Phase 1 subplan consistent, correct, feasible, artifact-covered, and
  boundary-safe for read-only historical dense-IAF artifact taxonomy before
  schema/loader implementation?

Findings:

- The first draft could pass after selected subset inspection instead of every
  discovered candidate in scope.
- The baseline artifact was not named precisely enough.
- "Candidate cells" could imply notebooks while checks only covered `.py`,
  `.md`, and `.json`.
- Ambiguous candidates had no terminal fail-closed status.
- Unavailable Claude review did not have a separate blocker path.
- Result reproducibility fields were underspecified.

Verdict:

- `VERDICT: REVISE`

Repair:

- Patched the subplan to require classification of every discovered in-scope
  candidate, define the prior baseline artifact paths, define candidate cells
  as named evidence rows rather than notebooks, add
  `ambiguous_needs_manual_review` and
  `too_large_for_bounded_payload_inspection` statuses, add unavailable-review
  blocker handling, and require actual commands/environment/CPU-GPU status and
  infeasibility reasons.

### 2026-07-04 - Phase 1 Subplan Review - Round 2

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-subplan-2026-07-04.md`

Question:

- After patching the prior gaps, does the Phase 1 subplan now require every
  discovered in-scope candidate classification, define baseline artifacts,
  avoid notebook/candidate-cell ambiguity, include fail-closed ambiguity status,
  handle unavailable Claude review, and require reproducibility fields?

Outcome:

- Claude found no remaining material consistency, feasibility,
  artifact-coverage, or boundary-safety blocker.

Verdict:

- `VERDICT: AGREE`

### 2026-07-04 - Phase 2 Subplan Review - Round 1

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-subplan-2026-07-04.md`

Question:

- Is the Phase 2 dense-IAF schema subplan consistent, correct, feasible,
  artifact-covered, and boundary-safe given Phase 1 classified legacy dense-IAF
  payload candidates but no generic target signatures?

Findings:

- The draft required a `target_signature` field but did not require a canonical
  stable generic target-signature scheme.
- The required-field set omitted `topology_hash` despite the objective naming
  topology/tensor hashes.
- The baseline did not clearly separate observed Phase 1 evidence from legacy
  semantic inference and unresolved signature design.
- The subplan did not require a class-by-class mapping/rejection table.
- Approval boundaries and review-probe protocol were underspecified.
- Stop conditions did not cover unstable or process-local signature designs.

Verdict:

- `VERDICT: REVISE`

Repair:

- Patched the subplan to require canonical `SSMTargetContract` signature rules,
  `topology_hash`, `tensor_hash`, a class-by-class mapping/rejection table,
  separated observed evidence from legacy inference, explicit human approval
  boundaries, and unstable-signature stop conditions.

### 2026-07-04 - Phase 2 Subplan Review - Round 2

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-subplan-2026-07-04.md`

Question:

- After patching, does the subplan now require a canonical
  `SSMTargetContract` target-signature scheme, topology/tensor hash coverage,
  class-by-class mapping/rejection table, separated evidence/inference,
  explicit approval boundaries, and unstable-signature stop conditions?

Outcome:

- Claude found no remaining material blocker in the subplan text.

Verdict:

- `VERDICT: AGREE`

### 2026-07-04 - Phase 3 Subplan Review - Round 1

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-subplan-2026-07-04.md`

Findings:

- The `git diff --check` command used a placeholder instead of concrete paths.
- The fail-closed test matrix was underspecified for individual hash tamper,
  nonfinite tensor, process-local identity, component semantics, and historical
  reject-only behavior.
- Synthetic target-signature scope needed to be explicit.
- Result run-manifest and decision-table requirements were missing.
- Probe/stop handling needed definition.

Verdict:

- `VERDICT: REVISE`

Repair:

- Patched the subplan with exact paths, synthetic-only signature scope, concrete
  hash/rejection test requirements, result manifest/decision-table requirements,
  and probe/stop handling.

### 2026-07-04 - Phase 3 Subplan Review - Round 2

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-subplan-2026-07-04.md`

Findings:

- One material boundary remained: a historical-style schema/hash-shaped payload
  with noncanonical legacy target identity needed an explicit rejection test.

Verdict:

- `VERDICT: REVISE`

Repair:

- Added the historical-style noncanonical target identity rejection test and
  promoted it into the primary pass criterion.

### 2026-07-04 - Phase 3 Subplan Review - Round 3

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-subplan-2026-07-04.md`

Outcome:

- Claude found no material blocker before Phase 3 implementation.

Verdict:

- `VERDICT: AGREE`

### 2026-07-04 - Phase 4 Subplan Review - Round 1

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-subplan-2026-07-04.md`

Findings:

- The Phase 2 canonical signature rule was referenced but not bound to an exact
  artifact/check.
- Local checks used placeholders.
- Phase 5 review gate did not require `VERDICT: AGREE`.
- Reject-only bridge statuses were not fixed.
- Scope blurred all evidence cells with embedded-payload candidates.
- "Complete manifest payload" wording risked scope creep.
- Stop conditions lacked Phase 2 rule/schema mismatch and invented-field cases.

Verdict:

- `VERDICT: REVISE`

Repair:

- Patched exact Phase 2 artifact anchors, executable checks, fixed bridge
  statuses, embedded-payload scope, metadata-only bridge manifest wording,
  `VERDICT: AGREE` gate, probe protocol, and Phase2/invented-field stop
  conditions.

### 2026-07-04 - Phase 4 Subplan Review - Round 2

Path reviewed:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-subplan-2026-07-04.md`

Outcome:

- Claude found no remaining material blocker.

Verdict:

- `VERDICT: AGREE`
