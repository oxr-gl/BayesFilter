# P44-M3 Result: Quadratic Observation Multimodality Stress

metadata_date: 2026-06-08
phase: P44-M3
run_id: `p44-codex-supervised-20260608-013203`
Status: `PASS_P44_M3_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | M3 quadratic observation stress phase passed final read-only Claude code/governance review. |
| Primary criterion status | Passed locally as a stress diagnostic: dense reference covers both symmetric modes and refines; Zhao--Cui/fixed-design TT matches dense tightly; CUT4 is finite and same-target but records a large bounded stress gap. |
| Veto diagnostic status | No dense-refinement, symmetric-mode, nonfinite, point-cap, or compile veto fired. The original small-gap CUT4 criterion was repaired and reviewed. |
| Main uncertainty | CUT4 is not accurate on this symmetric multimodal quadratic fixture; the evidence supports stress-gap detection, not CUT4 promotion. |
| Next justified action | Run the P44-M3 executable phase gate, then proceed to P44-M4 if the gate passes. |
| Not concluded | No HMC readiness, no long-horizon posterior recovery, no coupled multivariate TT claim, no exact CUT4 nonlinear likelihood claim, and no paper-scale Zhao--Cui reproduction. |

## Evidence Contract

Question: for the quadratic additive-Gaussian observation model
`x_t = rho x_{t-1} + eta_t`, `y_t = x_t^2 + epsilon_t`,
do dense quadrature, CUT4, and Zhao--Cui/fixed-design scalar TT expose the
expected multimodality stress in dimensions 1, 2, and 3?

Baseline/comparator:

- Governing baseline: scalar dense quadrature order 281 summed across
  independent product-panel coordinates.
- Reference validity checks: dense order 181 versus order 281 refinement for
  value and deterministic directional score residuals; explicit scalar
  symmetric-mode coverage before comparison.
- CUT4 comparator: `tf_svd_cut4_filter` on the matched TensorFlow structural
  quadratic observation target.
- Zhao--Cui comparator: `scalar_nonlinear_fixed_design_tt_value_path`, summed
  across product-panel coordinates.

Primary promotion criterion:

- Dims 1, 2, and 3 pass structural timing moment checks;
- scalar dense first-observation posterior mass has both negative and positive
  mode mass above `0.25` on every axis;
- dims 1, 2, and 3 pass dense refinement;
- Zhao--Cui value and score gaps remain tight against dense;
- CUT4 remains finite, same-target, and within the broad diagnostic stress-gap
  envelope, with the large gap reported rather than promoted as accuracy;
- at least five deterministic directional score residuals are used in every
  dimension.

Veto diagnostics:

- dense grid misses the symmetric mode;
- dense reference has no refinement check;
- one-mode approximation is promoted as full target correctness;
- score checks are performed near a symmetry-induced stationary point without
  absolute and directional tolerances;
- CUT4 point count exceeds the phase cap;
- CUT4 stress gap is hidden or described as small-error accuracy.

Explanatory-only diagnostics:

- TensorFlow warning logs, wall time, CUT4 point count, polynomial degree,
  fixed-design TT fit details, and approximation-gap magnitudes after passing
  the stated gate.

Nonclaims:

- no exact CUT4 nonlinear likelihood claim;
- no CUT4 accuracy promotion for symmetric multimodal quadratic observations;
- no production analytic score API;
- no HMC readiness;
- no long-horizon posterior recovery;
- no coupled multivariate TT claim;
- no paper-scale Zhao--Cui reproduction.

Artifact preserving the result:

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-result-2026-06-07.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-evidence-manifest-p44-codex-supervised-20260608-013203.json`
- Command logs:
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M3-command0.log`
  and
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M3-command1.log`

## Skeptical Audit

Status: `PASS_P44_M3_CODE_GOVERNANCE`.

- Wrong-baseline risk: dense order-281 remains the governing baseline after
  order-181 refinement passes at numerical-noise scale.
- One-mode risk: symmetric-mode mass is checked before comparisons are
  interpreted; all three axes have negative and positive masses around `0.42`.
- Proxy-metric risk: finite CUT4 values and point counts are not treated as
  accuracy evidence.
- Target-mismatch risk: the scalar dense/TT model and structural CUT4 model
  share the same parameter vector, observations, transition law, quadratic
  observation law, and observation variance; structural timing moments are
  checked.
- Tolerance-drift risk: the CUT4 reclassification is documented in a repair
  amendment and passed read-only Claude repair review.
- Fairness risk: dimensions 1--3 are independent product panels, not a coupled
  high-dimensional TT claim.

## Repair Notes

Repair amendment:

`docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-repair-amendment-2026-06-08.md`

Claude repair review Iteration 1 returned `PASS_P44_M3_REPAIR_REVIEW`.

Observed CUT4 gaps against dense order-281 reference:

| dim | value gap | max directional score gap | relative score error |
| --- | ---: | ---: | ---: |
| 1 | `7.099181e-02` | `2.418344e-01` | `2.579872e-01` |
| 2 | `1.751315e-01` | `5.681237e-01` | `3.527955e-01` |
| 3 | `3.607512e-01` | `1.102107e+00` | `4.637075e-01` |

Observed Zhao--Cui/fixed-design TT gaps against dense order-281 reference:

| dim | value gap | max directional score gap | relative score error |
| --- | ---: | ---: | ---: |
| 1 | `4.252455e-05` | `1.502594e-04` | `1.564833e-04` |
| 2 | `9.662974e-05` | `2.820354e-04` | `2.045106e-04` |
| 3 | `2.756965e-04` | `6.769339e-04` | `3.598171e-04` |

Dense order-181 versus order-281 refinement:

| dim | value gap | max directional score gap |
| --- | ---: | ---: |
| 1 | `3.330669e-15` | `1.468270e-14` |
| 2 | `7.327472e-15` | `1.987299e-14` |
| 3 | `2.220446e-14` | `3.033129e-13` |

Symmetric-mode coverage:

| axis | negative mass | positive mass |
| --- | ---: | ---: |
| 0 | `4.193900e-01` | `4.224101e-01` |
| 1 | `4.236593e-01` | `4.225527e-01` |
| 2 | `4.348730e-01` | `4.353366e-01` |

## Local Evidence

Commands:

1. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q -s tests/highdim/test_p44_quadratic_observation.py`
2. `python -m compileall -q bayesfilter/highdim tests/highdim/test_p44_quadratic_observation.py`

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
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-subplan-2026-06-07.md` |
| Repair amendment | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-repair-amendment-2026-06-08.md` |
| Test file | `tests/highdim/test_p44_quadratic_observation.py` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-result-2026-06-07.md` |

## Gate Markers

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_local_evidence_run: `COMPLETE`
p44_evidence_audit: `COMPLETE`
p44_result_note_substance: `COMPLETE`
p44_traceability_or_nonclaim: `COMPLETE`
p44_command_count: `2`
p44_long_run_used: `false`
