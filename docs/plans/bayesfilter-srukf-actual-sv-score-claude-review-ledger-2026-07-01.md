# SR-UKF Actual-SV Analytical Score Claude Review Ledger

Date: 2026-07-01

Status: OPEN

## Protocol

Claude is read-only reviewer only. Prompts must use one bounded path and end
with `VERDICT: AGREE` or `VERDICT: REVISE`. Claude cannot authorize human,
runtime, model-file, funding, product-capability, default-policy, or scientific
claim boundaries.

## Reviews

### 2026-07-01 - Master Program - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-master-program-2026-07-01.md`

Question:

- Does the master program satisfy the requested two-part SR-UKF
  derivation/implementation governance, repair loop, Claude-read-only boundary,
  anticipated approvals, and stop-condition requirements without unsupported
  scientific or runtime claims?

Findings summary:

- Claude found no material governance gap.
- Claude noted one nonblocking tightening opportunity: mirror the five-round
  stop rule for unresolved MathDevMCP material failures.

Codex response:

- Patched the master program, Phase 2 subplan, and Phase 4 subplan to add a
  five-focused-repair-attempt MathDevMCP stop condition.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 8 Result - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase8-leaderboard-release-result-2026-07-01.md`

Question:

- Does this Phase 8 result satisfy the leaderboard admission/release subplan
  as a result artifact, including prior-gate dependency, admitted actual-SV
  SR-UKF provenance, regenerated leaderboard artifacts, exact four
  forbidden-route preservation, gamma-score caveat, and no
  exact-likelihood/HMC/GPU/superiority overclaim?

Findings summary:

- Claude agreed that the artifact covers the required release-admission
  elements.
- Claude confirmed prior-gate dependency, admitted actual-SV SR-UKF
  provenance, regenerated leaderboard artifacts, exact four forbidden-route
  preservation, gamma-score caveat, and non-overclaiming.
- Claude suggested explicit prior-result path traceability. Codex patched the
  Phase 8 result to name the Phase 6 and Phase 7 result paths.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 7 Result - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-result-2026-07-01.md`

Question:

- Does this Phase 7 result satisfy the test-ladder subplan as a result
  artifact, including local checks, score-at-true uncertainty handling,
  gamma-score caveat, exact four forbidden-route preservation, Phase 8 handoff,
  and no leaderboard/HMC/GPU/exact-likelihood overclaim?

Findings summary:

- Claude agreed that the result artifact satisfies the Phase 7 test-ladder
  requirements.
- Claude confirmed local checks, 10-dataset score-at-true uncertainty handling,
  gamma-score caveat, exact four forbidden-route preservation, Phase 8 handoff,
  and non-overclaiming.
- Claude noted that wording around leaderboard admission consideration and
  Phase 8 start is appropriately cautious rather than promotional.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 6 Result - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-result-2026-07-01.md`

Question:

- Does this Phase 6 result satisfy the actual-SV adapter implementation
  subplan, including audited-label mapping, focused CPU-only checks,
  same-scalar FD scope, exact four forbidden-route preservation, separate
  admitted module rationale, and no leaderboard/HMC/GPU/exact-likelihood
  overclaim?

Findings summary:

- Claude agreed that the result satisfies the Phase 6 subplan as a bounded
  result artifact.
- Claude confirmed audited-label mapping, CPU-only checks with explicit
  `CUDA_VISIBLE_DEVICES=-1`, same-scalar FD scope, exact four forbidden-route
  preservation, separate admitted-module rationale, and non-overclaiming.
- Claude noted only that the result claims analytical provenance rather than
  broader correctness, which is appropriately scoped for Phase 6.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Visible Runbook - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-visible-gated-execution-runbook-2026-07-01.md`

Question:

- Does the visible runbook preserve Codex supervisor/executor role, Claude
  read-only role, repair loop, no-invalid-stop behavior, and no detached/nested
  execution boundary?

Findings summary:

- Claude found the role contract, read-only boundary, repair loop, prompt
  fallback, and visible launch definition sufficient.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 0 Subplan - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase0-governance-inventory-subplan-2026-07-01.md`

Question:

- Does Phase 0 provide a sufficient governance/drift-inventory launch gate?

Findings summary:

- Claude found the Phase 0 scope boundary good but identified material gaps:
  drift inventory was not a required auditable artifact, two-product and
  forbidden-route checks were not operationalized, material launch-artifact
  convergence was ambiguous, and missing/stale drift evidence was not a stop
  condition.

Verdict:

- `VERDICT: REVISE`

Codex response:

- Patched Phase 0 to require a drift inventory section in the Phase 0 result,
  local checks for the two-product split, forbidden-route checks, explicit
  material-launch-artifact convergence definition, and a missing/stale drift
  evidence stop condition.

### 2026-07-01 - Phase 0 Subplan - Iteration 2

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase0-governance-inventory-subplan-2026-07-01.md`

Question:

- Did the revised Phase 0 subplan fix the prior drift-inventory launch-gate
  gaps without unsupported claims?

Findings summary:

- Claude agreed the revised subplan fixed the auditability, operational checks,
  convergence definition, and stop-condition gaps.
- Claude gave one nonblocking wording note about keeping the strict-SPD route
  label identical across sections.

Codex response:

- Patched wording to use "strict-SPD principal-root derivative" consistently.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 1 Generic Derivation - Iteration 1

Path reviewed:

- `docs/chapters/ch17_square_root_sigma_point.tex`

Question:

- In the section `Factor-Propagating SR-UKF Score Contract`, does the derivation
  define a generic factor-propagating SR-UKF analytical score backend that does
  not rely on strict-SPD principal-square-root derivatives, historical
  SVD/eigenderivative score, or autodiff tape fallback; and are branch/failure
  conditions, factor reconstruction, likelihood score, filtered-state handoff,
  and forbidden claims sufficiently stated for Phase 1?

Findings summary:

- Claude found the construction genuinely factor-propagating, with declared
  factor placement, fixed-branch derivatives, explicit branch/failure stops,
  factor reconstruction equations, solve-form likelihood/score, filtered-state
  handoff, and forbidden provenance.
- Claude noted a nonblocking limitation: the section is a contract/specification
  and defers detailed QR/update primitive proofs to `ch12`, which is acceptable
  for Phase 1 but must be audited in Phase 2.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 2 Generic Derivation Audit - Iteration 1

Path reviewed:

- `docs/chapters/ch17_square_root_sigma_point.tex`

Question:

- After the audit-assumption patch, does the generic derivation adequately state
  a factor-propagating SR-UKF analytical score route that avoids historical
  SVD/eigenderivative, strict-SPD principal-square-root derivative, and autodiff
  tape fallback routes; and are the local branch, dimension, solve/logdet,
  score, gain, factor reconstruction, state handoff, and admission boundaries
  sufficient to proceed from Phase 2 to the Actual-SV augmented-noise adapter
  derivation, with remaining MathDevMCP proof-backend limitations treated as
  nonblocking implementation diagnostics?

Findings summary:

- Claude agreed the patched section is sufficient as a generic Phase 2 contract.
- Claude specifically confirmed route exclusion, fixed-branch assumptions,
  shape declarations, factor reconstruction, solve/logdet score route, gain and
  filtered-factor handoff, and admission boundary.
- Claude classified the remaining primitive QR/Cholesky/update-branch proof
  details as nonblocking for Phase 2 and suitable for later implementation
  diagnostics.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 3 Subplan - Iteration 3

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-augmented-adapter-derivation-subplan-2026-07-01.md`

Question:

- After adding the required bounded Claude review to the next-phase handoff and
  local checks over touched LaTeX and `docs/plans` files, is the Phase 3
  subplan consistent, feasible, artifact-complete, and boundary-safe for
  deriving the actual-SV augmented-noise adapter, with the three-coordinate
  default augmented variable, strict-SPD principal-root derivative
  nonadmission, historical SVD and `GradientTape` nonadmission, and no exact or
  same-target actual-SV claim leakage?

Findings summary:

- Claude agreed that the Phase 3 subplan is materially consistent, feasible,
  artifact-complete, and boundary-safe.
- Claude confirmed the three-coordinate pre-observation variable, the
  two-coordinate specialization fence, the historical SVD, `GradientTape`, and
  strict-SPD principal-root derivative nonadmission boundaries, and the no
  exact/same-target actual-SV claim boundary.
- Claude noted only a nonmaterial editorial looseness in the phrase "likely
  cross-linked" for chapter placement.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 3 Adapter Derivation - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-adapter-derivation-review-excerpt-2026-07-01.md`

Question:

- Is the Phase 3 actual-SV augmented-noise adapter derivation excerpt
  internally consistent, mathematically correct for the declared raw
  Gaussian-closure surrogate, and boundary-safe for handoff to Phase 4 audit?
  Check especially the three-coordinate augmented variable
  `(H_{t-1}, U_t, E_t)`, fixed-sigma
  `theta=(theta_gamma, theta_beta)`, transition and observation derivatives,
  stationary initial derivatives, score handoff, collapsed-route fence, and
  absence of exact/same-target actual-SV, `GradientTape`, historical SVD, or
  strict-SPD principal-root admission.

Findings summary:

- Claude agreed the excerpt is internally consistent, mathematically correct
  for the declared raw-observation Gaussian-closure surrogate, and
  boundary-safe for Phase 4.
- Claude specifically confirmed the three-coordinate augmentation, transition
  and observation maps, pointwise derivatives, stationary initial variance
  derivative, score handoff, collapsed-route fence, and nonadmission
  boundaries.
- Claude raised one Phase 4 handoff caveat: the audit should clarify whether
  downstream implementation consumes the stationary initial variance law or the
  scalar square-root factor and its derivative.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 4 Adapter Audit Result - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase4-adapter-audit-result-2026-07-01.md`

Question:

- Does this Phase 4 adapter audit result satisfy the Phase 4 audit subplan for
  target law, dimensions, derivative checks, variance-vs-factor handoff,
  artifact coverage, and boundary safety, without overclaiming implementation,
  numerical accuracy, HMC readiness, leaderboard admission, exact actual-SV
  likelihood, or same-target transformed-likelihood?

Findings summary:

- Claude agreed the Phase 4 result satisfies the audit subplan within the
  bounded file-only scope.
- Claude specifically confirmed target-law boundary, three-coordinate state
  layout, derivative evidence with parser limitation disclosed, variance versus
  scalar-factor handoff coverage, artifact coverage, and non-overclaiming.
- Claude noted that not every displayed equation was formalized in MathDevMCP,
  but the result correctly records this as uncertainty rather than a false pass.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 5 Subplan - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-subplan-2026-07-01.md`

Question:

- Is the Phase 5 generic backend implementation subplan consistent, feasible,
  artifact-complete, and boundary-safe after Phase 4, especially generic-only
  scope, exact forbidden-route guards for `GradientTape`,
  `tf_svd_sigma_point_filter`, historical SVD, strict-SPD principal-root
  derivatives, evidence contract, skeptical audit, tests, stop conditions, and
  Phase 6 handoff?

Findings summary:

- Claude found the subplan mostly solid but requested revision.
- Material issues: `tf_svd_sigma_point_filter` was not repeated in required
  checks and forbidden actions; negative guard tests were not explicitly
  required; the evidence-contract artifact row omitted the refreshed Phase 6
  subplan.

Codex response:

- Patched required checks to include `tf_svd_sigma_point_filter`.
- Added negative route-guard tests for each forbidden route family.
- Patched forbidden actions to ban importing or calling
  `tf_svd_sigma_point_filter`.
- Patched the evidence-contract artifact row to include the refreshed Phase 6
  subplan.

Verdict:

- `VERDICT: REVISE`

### 2026-07-01 - Phase 5 Subplan - Iteration 2

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-subplan-2026-07-01.md`

Question:

- After patching the prior issues, does the Phase 5 subplan consistently carry
  the full forbidden-route set through required artifacts, required checks,
  negative guard tests, forbidden actions, and artifact handoff, without new
  boundary leaks or feasibility problems?

Findings summary:

- Claude agreed the core Phase 5 enforcement machinery now names all four
  forbidden route families in required artifacts, required checks, negative
  guard tests, and forbidden actions.
- Claude requested revision because the Phase 5 result and refreshed Phase 6
  subplan were not explicitly required to restate/preserve the same four-route
  forbidden set.

Codex response:

- Patched required artifacts, next-phase handoff conditions, and end-of-phase
  review procedure to require the Phase 5 result and refreshed Phase 6 subplan
  to preserve the exact four-route forbidden set: `GradientTape`,
  `tf_svd_sigma_point_filter`, historical SVD/eigenderivative derivatives, and
  strict-SPD principal-root derivative helpers.

Verdict:

- `VERDICT: REVISE`

### 2026-07-01 - Phase 5 Subplan - Iteration 3

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-subplan-2026-07-01.md`

Question:

- After adding exact forbidden-route preservation to required artifacts,
  handoff conditions, and end-of-phase review, does this resolve the prior
  handoff leak without new boundary or feasibility problems?

Findings summary:

- Claude agreed the prior handoff leak is closed.
- Claude confirmed that required downstream artifacts, the Phase 6 advance
  gate, and the end-of-phase review now preserve the exact four-route
  forbidden set.
- Claude found no new boundary or feasibility problem.  It noted a nonblocking
  wording caution that static guard implementation should not be token-only;
  the subplan's route-family language covers this at the planning level.

Verdict:

- `VERDICT: AGREE`

### 2026-07-01 - Phase 5 Result - Iteration 1

Path reviewed:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-result-2026-07-01.md`

Question:

- Does this Phase 5 generic backend implementation result satisfy the converged
  Phase 5 subplan, including generic-only scope, focused tests, static
  admitted-backend guard, negative forbidden-route tests, exact four-route
  forbidden-set preservation into Phase 6, CPU-only test disclosure, and no
  actual-SV/leaderboard/HMC/exact-likelihood overclaim?

Findings summary:

- Claude agreed the result note satisfies the requested Phase 5 checklist
  within the bounded result-file scope.
- Claude confirmed generic-only scope, focused tests, static admitted-backend
  guard, negative forbidden-route tests, exact four-route forbidden-set
  preservation into Phase 6, CPU-only test disclosure, and non-overclaiming.
- Claude noted it did not compare the separate subplan directly because the
  review was bounded to the result path.

Verdict:

- `VERDICT: AGREE`
