# P44-M2 Result: Cubic Additive-Gaussian Observation

metadata_date: 2026-06-08
phase: P44-M2
run_id: `p44-codex-supervised-20260608-013203`
Status: `PASS_P44_M2_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | M2 cubic additive-Gaussian phase passed final read-only Claude code/governance review. |
| Primary criterion status | Passed locally: dimensions 1, 2, and 3 have dense refinement, nested `a=0` Kalman tie-out for dense and CUT4 value/shared score coordinates, and bounded CUT4/Zhao--Cui value/score gaps against dense order-241 reference. |
| Veto diagnostic status | No dense-refinement, target-consistency, nonfinite, metadata, or compile veto fired. One tolerance/interpretation repair was reviewed by Claude. |
| Main uncertainty | CUT4 is a coarse same-target sigma-point approximation on this cubic target; the phase records explicit gaps and does not promote exact cubic correctness. |
| Next justified action | Run the P44-M2 executable phase gate, then proceed to P44-M3 if the gate passes. |
| Not concluded | No HMC readiness, no long-horizon stability, no paper-scale Zhao--Cui reproduction, no adaptive MATLAB TT-cross/SIRT reproduction, and no exact CUT4 nonlinear likelihood claim. |

## Evidence Contract

Question: for the cubic additive-Gaussian observation model
`x_t = rho x_{t-1} + eta_t`,
`y_t = x_t + a x_t^3 + epsilon_t`, do CUT4 and the
Zhao--Cui/fixed-design scalar TT lane produce bounded value and diagnostic
score errors against a refined dense quadrature reference in dimensions 1, 2,
and 3?

Baseline/comparator:

- Governing baseline: scalar dense quadrature reference, summed across
  independent product-panel coordinates.
- Reference validity check: dense order 161 versus dense order 241 refinement
  for value and deterministic directional score residuals.
- Nested sanity check: at `a=0`, dense value and the first four shared score
  coordinates tie to exact Kalman; CUT4 structural value and the first four
  shared score coordinates also tie to exact Kalman. The cubic-coordinate
  derivative is recorded as a nonclaim because the nested Kalman model has no
  cubic coefficient.
- CUT4 comparator: `tf_svd_cut4_filter` on the matched TensorFlow structural
  cubic target.
- Zhao--Cui comparator: `scalar_nonlinear_fixed_design_tt_value_path`, summed
  across product-panel coordinates.

Primary promotion criterion:

- Dims 1, 2, and 3 pass dense refinement;
- dims 1, 2, and 3 pass nested `a=0` Kalman value and shared-score checks;
- dims 1, 2, and 3 have finite CUT4 and Zhao--Cui values/scores;
- CUT4 gaps remain inside explicit same-target approximation bounds;
- Zhao--Cui gaps remain inside tighter fixed-design TT bounds;
- at least five deterministic directional score residuals are used in every
  dimension.

Veto diagnostics:

- dense reference has no refinement check;
- cubic transform or observation-noise target mismatch;
- nested linear check treats the cubic-coordinate derivative as Kalman-shared;
- CUT4 target metadata does not record same-target approximation status;
- active innovation floors or nonfinite value/score;
- tolerance or target change without reviewed repair amendment.

Explanatory-only diagnostics:

- TensorFlow warning logs, wall time, CUT4 point count, polynomial degree,
  fixed-design TT fit details, and approximation-gap magnitudes after passing
  the stated gate.

Nonclaims:

- no exact CUT4 nonlinear likelihood claim;
- no production analytic score API;
- no HMC readiness;
- no long-horizon stability;
- no paper-scale Zhao--Cui reproduction;
- no adaptive MATLAB TT-cross/SIRT reproduction.

Artifact preserving the result:

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-result-2026-06-07.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-evidence-manifest-p44-codex-supervised-20260608-013203.json`
- Command logs:
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M2-command0.log`
  and
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M2-command1.log`

## Skeptical Audit

Status: `PASS_P44_M2_CODE_GOVERNANCE`.

- Wrong-baseline risk: dense order-241 reference remains the governing
  comparator after order-161 refinement passes at about `1e-14` scale.
- Proxy-metric risk: finite values, compile success, and point counts are not
  promotion criteria by themselves.
- Target-mismatch risk: the scalar dense/TT model and structural CUT4 model
  share the same parameter vector, observations, transition law, cubic
  observation law, and observation variance. The repaired test now directly
  ties CUT4 structural `a=0` timing to exact Kalman in dims 1, 2, and 3.
- Nested-linear risk: the `a=0` check validates value and shared parameters;
  it does not claim the cubic-coordinate score equals Kalman because Kalman has
  no cubic coefficient.
- Tolerance-drift risk: the CUT4 tolerance repair is documented in a repair
  amendment and received read-only Claude repair review before final phase
  review.
- Fairness risk: dimensions 1--3 are independent product panels, not a coupled
  high-dimensional TT claim.

## Repair Notes

Repair amendment:

`docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-repair-amendment-2026-06-08.md`

Claude repair review Iteration 2 returned `PASS_P44_M2_REPAIR_REVIEW`.
Iteration 1 was an operational timeout with no substantive review output.

Observed CUT4 gaps against dense order-241 reference:

| dim | value gap | max directional score gap | relative score error |
| --- | ---: | ---: | ---: |
| 1 | `3.198174e-03` | `8.470451e-03` | `1.074936e-02` |
| 2 | `6.693418e-03` | `1.770687e-02` | `1.589103e-02` |
| 3 | `1.541071e-02` | `4.073841e-02` | `2.326626e-02` |

Observed Zhao--Cui/fixed-design TT gaps against dense order-241 reference:

| dim | value gap | max directional score gap | relative score error |
| --- | ---: | ---: | ---: |
| 1 | `1.931912e-04` | `8.914410e-04` | `1.115007e-03` |
| 2 | `2.224265e-04` | `1.059130e-03` | `9.395700e-04` |
| 3 | `3.496295e-04` | `1.818532e-03` | `9.991846e-04` |

Dense order-161 versus order-241 refinement:

| dim | value gap | max directional score gap |
| --- | ---: | ---: |
| 1 | `6.217249e-15` | `3.692153e-15` |
| 2 | `1.332268e-14` | `5.426714e-15` |
| 3 | `2.153833e-14` | `7.861249e-15` |

## Local Evidence

Commands:

1. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q -s tests/highdim/test_p44_cubic_additive_gaussian.py`
2. `python -m compileall -q bayesfilter/highdim tests/highdim/test_p44_cubic_additive_gaussian.py`

Observed result:

- Focused pytest: `5 passed`, exit code 0.
- Compile check: exit code 0.
- CPU-only mode was deliberate; no GPU evidence is claimed. TensorFlow emitted
  CUDA initialization warnings despite `CUDA_VISIBLE_DEVICES=-1`; these are
  treated as explanatory-only because the phase is CPU-only.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `N/A - dirty worktree preserved; command manifest captures current files` |
| Command environment | CPU-only for pytest via `CUDA_VISIBLE_DEVICES=-1`; compile check CPU-only |
| Data version | deterministic in-test observations |
| Random seeds | deterministic branch seeds embedded in fixture config |
| Wall time | tiny local validation only |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-subplan-2026-06-07.md` |
| Repair amendment | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-repair-amendment-2026-06-08.md` |
| Test file | `tests/highdim/test_p44_cubic_additive_gaussian.py` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-result-2026-06-07.md` |

## Gate Markers

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_local_evidence_run: `COMPLETE`
p44_evidence_audit: `COMPLETE`
p44_result_note_substance: `COMPLETE`
p44_traceability_or_nonclaim: `COMPLETE`
p44_command_count: `2`
p44_long_run_used: `false`
