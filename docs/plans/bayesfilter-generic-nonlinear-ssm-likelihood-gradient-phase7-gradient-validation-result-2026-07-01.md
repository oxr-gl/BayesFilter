# Phase 7 Result: Gradient Validation And Scoped Score Admission

Date: 2026-07-01

Status: `GENERIC_NSSM_PHASE7_SCOPED_SCORE_ADMISSION_LOCAL_PASS_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 7 now passes for the reviewed scoped score-admission set. The affine structural exact-target lane, the model-C structural fixed-support approximate lane, and the SGQF fixture-only lane all clear the narrowed same-branch gradient gate at their reviewed claim levels after the value-side branch-alignment repair. |
| Primary criterion status | Met locally: branch-valid finite-difference support is now established for the reviewed scoped lane set, with lane-specific nonclaims preserved. |
| Veto diagnostic status | Passed locally: no same-branch mismatch remains in the reviewed narrowed set, no wrong-scalar FD tieout was used for admission, no fallback-only route was promoted as analytical, and model B remained excluded. |
| Main uncertainty | This does not promote HMC readiness, top-level API authority, production readiness, or generic direct-likelihood SGQF score support. |
| Next justified action | Execute Phase 8 and write the final scoped governed decision and stop handoff. |
| What is not being concluded | No HMC readiness, no top-level API promotion, no production/default claim, and no broad generic direct-likelihood SGQF gradient claim. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Do the candidate analytical-gradient lanes differentiate the same declared scalar on the same branch well enough to admit scoped score authority? |
| Baseline/comparator | reviewed value-passing lanes, same-branch FD ladders, branch-signature contracts, and the focused model-C branch-alignment repair. |
| Primary criterion | Passed locally for the reviewed scoped set: branch-valid FD ladders and same-scalar evidence support the claimed scoped score authority for the admitted lanes. |
| Veto diagnostics | Passed locally: no same-branch mismatch, no wrong-scalar FD tieout in the admitted lanes, no fallback-only route silently promoted as analytical, and no HMC/top-level/production scope promoted. |
| Explanatory diagnostics | focused pytest node outcomes, branch-signature checks, and repair-result notes. |
| Not concluded | No HMC readiness, no top-level API promotion, and no production/default claim. |
| Artifact | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-result-2026-07-01.md` and refreshed `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase8-final-decision-subplan-2026-07-01.md`. |

## Scoped Score Admission Summary

### Admitted at the reviewed claim level

1. **Affine structural exact-target lane**
   - admitted scope: exact-target structural value/score evidence for the
     reviewed affine SGQF adapter lane only
   - supporting evidence: same-scalar finite-difference and analytical-score
     checks passed

2. **Model-C structural fixed-support approximate lane**
   - admitted scope: declared Gaussian-projection approximate value/score
     evidence only
   - supporting evidence: same-scalar finite-difference pairing now passes after
     the value-side branch-alignment repair
   - preserved nonclaim: not exact-target gradient evidence

3. **Fixed-SGQF fixture-only lane**
   - admitted scope: lane-local same-branch SGQF scalar evidence only
   - supporting evidence: one-step / scalar SGQF same-branch checks passed

### Explicitly not admitted

4. **Model-B lane**
   - remains excluded because it did not pass the Phase 6 value gate and remains
     structurally ineligible

5. **Generic direct-likelihood SGQF gradient support**
   - remains not admitted; this phase does not promote the broader non-Gaussian
     SGQF runtime seam

## Local Checks

Commands actually run:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_fixed_sgqf_scores_tf.py::test_fixed_sgqf_p47_one_step_analytic_score_matches_oracle_and_fd \
  tests/test_fixed_sgqf_scores_tf.py::test_fixed_sgqf_score_rejects_expected_branch_mismatch \
  tests/test_fixed_sgqf_scores_tf.py::test_fixed_sgqf_same_branch_signature_tracks_failure_stage \
  tests/test_fixed_sgqf_scores_tf.py::test_fixed_sgqf_scalar_quadratic_multistep_score_matches_finite_difference_for_multiple_parameters \
  tests/test_fixed_sgqf_integration_tf.py::test_fixed_sgqf_score_api_is_deterministic_across_repeated_calls \
  tests/test_fixed_sgqf_integration_tf.py::test_fixed_sgqf_end_to_end_value_and_score_integration_on_p47_oracle \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_svd_sigma_point_analytic_score_matches_finite_difference \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_svd_cut4_analytic_score_matches_finite_difference_and_oracle_score \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_default_structural_fixed_support_score_matches_finite_difference
```

Outcome:

- Focused CPU-only pytest passed after the value-side repair: `15 passed, 2 warnings in 3.97s`.
- No reviewed node in the narrowed set failed after the repair.

## Bounded Claude Reviews

Reviewed artifacts and outcomes:

- Phase 7 executable refresh: `VERDICT: AGREE` after narrowing to exact node IDs and preserving claim boundaries
- Phase 7A repair subplan: `VERDICT: AGREE` after fixing execution logic and exact node-set specification
- Phase 7A repair result: prepared for review in the closeout packet
- Phase 7 result: prepared for review in the closeout packet

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: candidate lanes were tested only at the reviewed claim level. |
| Proxy metric promoted | Avoided: passing nodes support only scoped lane-local or lane-specific score admission, not HMC/API/production promotion. |
| Missing stop condition | Avoided: model B remained excluded and no broader SGQF direct-likelihood claim was inferred. |
| Unfair comparison | Avoided: affine exact-target, model-C approximate, and SGQF fixture-only lanes remained separately interpreted. |
| Hidden assumption | Avoided: the model-C score pass is attributed to explicit value-side branch alignment, not to a silent semantic rewrite. |
| Stale context | Avoided: Phase 7 remained constrained to Phase 6-passing lanes and the reviewed executable refresh. |
| Environment mismatch | Avoided: runtime was CPU-only with explicit GPU hiding. |
| Artifact-answer mismatch | Avoided: this result records scoped score admission only, not broader promotion. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Worktree status | Dirty pre-existing research/doc worktree; unrelated dirty changes preserved. |
| Execution target | Narrow same-branch gradient-validation gate. |
| CPU/GPU status | CPU-only TensorFlow test run with `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA command was run. |
| Commands | See Local Checks command above. |
| Data version | `N/A` (fixture/unit-test validation only) |
| Random seeds | `N/A` (deterministic fixture/unit-test focus) |
| Wall time | `N/A` (no dedicated benchmark timing artifact for Phase 7) |
| Plan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-subplan-2026-07-01.md` |
| Executable refresh | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-executable-refresh-2026-07-01.md` |
| Repair artifact | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7a-model-c-structural-fixed-support-repair-result-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-result-2026-07-01.md` |

## Phase 8 Handoff

Phase 8 may start only after the ledgers record that:

- the affine structural exact-target lane is admitted only for the reviewed
  affine SGQF adapter lane;
- the model-C structural fixed-support lane is admitted only as declared
  Gaussian-projection approximate value/score evidence;
- the SGQF fixture-only lane is admitted only as lane-local SGQF scalar
  evidence;
- model B remains blocked/excluded;
- the Phase 7 result is reviewed `AGREE`;
- the refreshed Phase 8 subplan is reviewed `AGREE`.

Phase 8 must write the final scoped governed decision only. It must not promote
HMC readiness, top-level API authority, production readiness, or default-policy
change.
