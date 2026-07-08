# Generic Nonlinear-SSM Likelihood And Analytical-Gradient Visible Execution Ledger

Date: 2026-07-01

## Status

`GENERIC_NSSM_SCOPED_VALUE_AND_SCORE_SUPPORT_CLOSED`

## Ledger

### 2026-07-01 - Phase 0 - PREPLAN

Evidence contract:

- Question: Can BayesFilter launch a governed program for generic nonlinear-SSM
  likelihood and analytical-gradient support without drifting target semantics,
  branch semantics, or API-scope authority?
- Baseline/comparator: exact-target chapter contracts, SGQF/fixed-branch chapter
  contracts, current structural/posterior/highdim code seams, and prior
  governed-program patterns.
- Primary criterion: master program, runbook, ledgers, stop handoff, and phase
  subplans exist with explicit anti-drift gates and no-choice execution
  discipline.
- Veto diagnostics: wrong-target Gaussian closure, silent API overpromotion,
  structural-admission ambiguity, phase advance without review, user-choice
  prompts for scientific matters.
- Non-claims: no implementation success, no value pass, no gradient pass, no
  HMC readiness, no production/default claim.

Skeptical audit result:

- Wrong baseline: exact target, declared approximate scalar, and same-scalar
  derivative must be separated before implementation.
- Proxy metric risk: API success, FD, and performance are not promotion
  criteria by themselves.
- Missing stop condition: target drift, branch mismatch, and API-scope drift are
  explicit blockers.
- Unfair comparison: exact-target, Gaussian-projection, fixed-cloud, and
  direct-likelihood lanes are separate families.
- Hidden assumption: the current structural adapter is not yet generic and must
  be governed explicitly.
- Stale context: chapter and code-anchor inventory is frozen in the master.
- Environment mismatch: launch is document-only.
- Artifact adequacy: full governance package plus first-wave subplans required.

Actions:

- Created the generic nonlinear-SSM master package and first-wave subplans.
- Bounded reviews closed for:
  - master program (`VERDICT: AGREE` after semantic-family and blocked-closeout repairs)
  - target-and-authority contract (`VERDICT: AGREE` after route/scalar/branch/admission clarifications)
  - visible runbook (`VERDICT: AGREE`)
  - Phase 0 subplan (`VERDICT: AGREE` after launch-freeze repairs)

Artifacts:

- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-master-program-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-target-authority-contract-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-gated-execution-runbook-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase0-launch-subplan-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase0-launch-result-2026-07-01.md`

Gate status:

- `GENERIC_NSSM_PHASE0_REVIEWED_CLOSED`

Next action:

- Execute the document-only contract and architecture phases before implementation.

### 2026-07-01 - Phases 1 Through 4 Document Contracts Closed

Actions:

- Wrote and closed the target-and-authority contract result.
- Wrote and closed the structural-admission contract result.
- Wrote and closed the generic value-lane architecture result.
- Wrote and closed the generic analytical-derivative contract result.
- Preserved no-choice execution discipline and route-level (`model × lane × claim`) admission.

Artifacts:

- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase1-target-authority-contract-result-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase2-structural-admission-result-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase3-value-lane-architecture-result-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase4-derivative-contract-result-2026-07-01.md`

Gate status:

- `GENERIC_NSSM_PHASE1_REVIEWED_CLOSED`
- `GENERIC_NSSM_PHASE2_REVIEWED_CLOSED`
- `GENERIC_NSSM_PHASE3_REVIEWED_CLOSED`
- `GENERIC_NSSM_PHASE4_REVIEWED_CLOSED`

Next action:

- Execute the narrow structural-adapter implementation refresh.

### 2026-07-01 - Phase 5 Structural-Adapter Refresh Implemented

Evidence contract:

- Question: Can the reviewed contracts be implemented across the structural/
  nonlinear seam without silent semantic fallback?
- Baseline/comparator: reviewed contracts from Phases 1-4 and the current
  implementation seams.
- Primary criterion: implement the structural adapter refresh without widening
  semantics or claims.
- Veto diagnostics: silent fallback, hidden target drift, API overpromotion, or
  hidden direct-likelihood SGQF claim.
- Non-claims: no value-gate pass, no gradient admission, no HMC readiness, no
  top-level/production promotion.

Actions:

- Implemented explicit admission metadata in
  `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`.
- Added affine structural exact-eligible adaptation.
- Reclassified model C as approximate-eligible only.
- Kept model B explicitly ineligible / fail-closed.
- Updated focused tests in:
  - `tests/test_nonlinear_benchmark_models_tf.py`
  - `tests/test_fixed_sgqf_values_tf.py`
- Focused CPU-only checks passed:
  - `23 passed, 2 warnings in 3.80s`

Artifacts:

- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-executable-refresh-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-result-2026-07-01.md`
- `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`
- `tests/test_nonlinear_benchmark_models_tf.py`
- `tests/test_fixed_sgqf_values_tf.py`

Gate status:

- `GENERIC_NSSM_PHASE5_LOCAL_PASS_PENDING_REVIEW`

Next action:

- Execute the narrow structural value gate.

### 2026-07-01 - Phase 6 Structural Value Gate Passed

Evidence contract:

- Question: Do the implemented value paths reproduce the exact or declared
  scalar they are authorized to compute at the intended claim level?
- Baseline/comparator: reviewed Phase 5 implementation and the exact/declared
  comparators frozen in earlier phases.
- Primary criterion: affine exact lane, model-C approximate lane, and model-B
  fail-closed status must validate at their reviewed claim levels.
- Veto diagnostics: wrong-scalar tieout, surrogate promoted as exact-target,
  affine recovery failure, fixed-cloud oracle failure, or branch-invalid
  comparison.
- Non-claims: no gradient admission, no HMC readiness, no top-level/production
  promotion.

Actions:

- Ran the reviewed CPU-only value-gate checks.
- Confirmed:
  - affine structural lane passes exact Kalman recovery,
  - model C passes only the declared Gaussian-projection approximate value gate,
  - model B remains blocked/ineligible.
- Focused CPU-only checks passed:
  - `23 passed, 2 warnings in 6.41s`

Artifacts:

- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-executable-refresh-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-result-2026-07-01.md`

Gate status:

- `GENERIC_NSSM_PHASE6_VALUE_GATE_LOCAL_PASS_PENDING_REVIEW`

Next action:

- Execute the narrowed same-branch gradient gate.

### 2026-07-01 - Phase 7 Blocked, Then Repaired, Then Scoped Score Gate Passed

Evidence contract:

- Question: Do the candidate analytical-gradient lanes differentiate the same
  declared scalar on the same branch well enough to admit scoped score
  authority?
- Baseline/comparator: reviewed value-passing lanes, same-branch FD ladders,
  branch-signature contracts, and the model-C structural fixed-support
  value/score pairing.
- Primary criterion: branch-valid FD support for the reviewed narrowed lane set,
  with no HMC/top-level/production promotion.
- Veto diagnostics: same-branch mismatch, wrong-scalar FD tieout, fallback-only
  promotion, or model-B promotion after failing the value gate.
- Non-claims: no HMC readiness, no top-level API promotion, no production claim.

Actions:

- Wrote and reviewed the narrowed Phase 7 executable refresh.
- Initial narrowed gradient run blocked on the model-C structural fixed-support
  value/score alignment issue.
- Wrote the focused repair subplan and repair result.
- Repaired `tests/test_nonlinear_sigma_point_scores_tf.py` so the value-side
  comparator threads the requested backend through the model-C structural
  fixed-support helper.
- Re-ran the focused repair nodes; `15 passed, 2 warnings in 3.97s`.
- Reopened and re-ran the narrowed Phase 7 gradient gate successfully for the
  reviewed scoped lane set.

Artifacts:

- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-executable-refresh-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-result-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7a-model-c-structural-fixed-support-repair-subplan-2026-07-01.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7a-model-c-structural-fixed-support-repair-result-2026-07-01.md`
- `tests/test_nonlinear_sigma_point_scores_tf.py`

Gate status:

- `GENERIC_NSSM_PHASE7_SCOPED_SCORE_ADMISSION_LOCAL_PASS_PENDING_REVIEW`

Admitted scoped lanes:

- affine structural exact-target value/score lane
- model-C structural fixed-support approximate value/score lane
- SGQF fixture-only same-branch scalar lane

Still not admitted:

- model B lane
- generic direct-likelihood SGQF runtime/score support
- HMC readiness
- top-level API promotion
- production/default-policy promotion

Next action:

- Write the final scoped governed decision and stop handoff.
