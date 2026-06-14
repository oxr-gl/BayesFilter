# P44-M4 Result: Nonlinear Additive-Gaussian Transition

metadata_date: 2026-06-08
phase: P44-M4
run_id: `p44-codex-supervised-20260608-013203`
Status: `PASS_P44_M4_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | M4 nonlinear transition phase passed final read-only Claude code/governance review. |
| Primary criterion status | Local evidence passed under the repaired scope: dense refinement, nested linear Kalman tie-out, T=2 dense/CUT4/Zhao--Cui value and score checks for dims 1--3, and T=4 dense/CUT4 accumulation diagnostics for dims 1--3. |
| Veto diagnostic status | No nested-linear, dense-refinement, nonfinite, point-cap, branch/floor, or compile veto fired. |
| Main uncertainty | The current Zhao--Cui scalar helper is pinned to two observations, so there is no Zhao--Cui T=4 accumulation claim in M4. |
| Next justified action | Run the P44-M4 executable phase gate, then proceed to P44-M5 if the gate passes. |
| Not concluded | No Zhao--Cui T=4 accumulation result, no HMC readiness, no long-horizon posterior recovery, no coupled multivariate TT claim, no exact CUT4 nonlinear likelihood claim, and no paper-scale Zhao--Cui reproduction. |

## Evidence Contract

Question: for the nonlinear additive-Gaussian transition model
`x_t = rho x_{t-1} + c tanh(x_{t-1}) + eta_t`, `y_t = x_t + epsilon_t`,
do dense quadrature, CUT4, and Zhao--Cui/fixed-design scalar TT produce
consistent same-target value and diagnostic score evidence in dimensions 1, 2,
and 3?

Baseline/comparator:

- Governing baseline: scalar dense quadrature order 241 summed across
  independent product-panel coordinates after order-181 refinement.
- Nested linear check: the `c=0` fixture must tie dense and CUT4 to exact
  Kalman value and score for shared parameters at horizons `T=2` and `T=4`.
- CUT4 comparator: `tf_svd_cut4_filter` on the matched TensorFlow structural
  nonlinear transition target.
- Zhao--Cui comparator: `scalar_nonlinear_fixed_design_tt_value_path`, summed
  across product-panel coordinates, only for the governed two-observation lane.

Primary promotion criterion:

- Dims 1, 2, and 3 pass nested `c=0` dense/CUT4 tie-out to exact Kalman at
  `T=2` and `T=4`;
- dims 1, 2, and 3 pass dense order-181 versus order-241 refinement at `T=2`
  and `T=4`;
- dims 1, 2, and 3 pass `T=2` CUT4 and Zhao--Cui value and at least five
  deterministic directional score residual checks against dense;
- dims 1, 2, and 3 pass `T=4` CUT4 accumulation checks against dense;
- the current Zhao--Cui `T=4` nonclaim is enforced by an executable helper
  boundary check.

Veto diagnostics:

- transition, observation, or initial-law targets differ across methods;
- nested `c=0` timing fails against exact Kalman;
- dense reference lacks refinement;
- horizon growth hides accumulated score error;
- a Zhao--Cui T=4 claim is made without a separately reviewed helper;
- CUT4 augmented dimension, point count, polynomial degree, or innovation-floor
  diagnostics exceed the phase boundary;
- nonfinite value or score appears.

Explanatory-only diagnostics:

- TensorFlow warning logs, wall time, CUT4 point count, polynomial degree,
  fixed-design TT fit details, and approximation-gap magnitudes after passing
  the stated gate.

Nonclaims:

- no Zhao--Cui T=4 accumulation result;
- no exact CUT4 nonlinear likelihood claim;
- no production analytic score API;
- no HMC readiness;
- no long-horizon posterior recovery;
- no coupled multivariate TT claim;
- no paper-scale Zhao--Cui reproduction.

Artifact preserving the result:

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-result-2026-06-07.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-evidence-manifest-p44-codex-supervised-20260608-013203.json`
- Command logs:
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M4-command0.log`
  and
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M4-command1.log`

## Skeptical Audit

Status: `PASS_P44_M4_CODE_GOVERNANCE`.

- Wrong-baseline risk: dense order-241 is used only after order-181 refinement
  passes at numerical-noise scale for every dimension and horizon.
- Timing risk: the nested `c=0` model checks dense and CUT4 against exact
  Kalman at `T=2` and `T=4`.
- Proxy-metric risk: finite CUT4 values and metadata are not treated as
  correctness by themselves; value and directional score residuals are checked
  against dense.
- Target-mismatch risk: scalar dense/TT and structural CUT4 use the same
  parameter vector, observations, transition law, observation law, and noise
  variances.
- Horizon-scope risk: the Zhao--Cui helper is explicitly not promoted beyond
  its governed two-observation path; the `T=4` boundary is executable.
- Fairness risk: dimensions 1--3 are independent product panels, not a coupled
  high-dimensional TT claim.

## Repair Notes

Repair amendment:

`docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-repair-amendment-2026-06-08.md`

Claude repair review Iteration 1 returned `PASS_P44_M4_REPAIR_REVIEW`.

The reviewed repair preserves:

- Zhao--Cui evidence at `T=2`, dims 1--3, for value and TensorFlow autodiff
  score;
- CUT4 accumulation diagnostics at `T=2` and `T=4`, dims 1--3;
- an explicit nonclaim for Zhao--Cui `T=4` until a separately reviewed helper
  exists.

## Observed Gaps

Dense order-181 versus order-241 refinement:

| horizon | dim | value gap | max directional score gap |
| ---: | ---: | ---: | ---: |
| 2 | 1 | `2.264855e-14` | `1.204592e-14` |
| 2 | 2 | `4.130030e-14` | `2.242651e-14` |
| 2 | 3 | `6.217249e-14` | `3.486100e-14` |
| 4 | 1 | `4.485301e-14` | `2.453593e-14` |
| 4 | 2 | `8.126833e-14` | `4.507505e-14` |
| 4 | 3 | `1.212364e-13` | `7.016610e-14` |

Observed `T=2` gaps against dense order-241 reference:

| dim | CUT4 value gap | CUT4 max directional score gap | CUT4 relative score error | Zhao--Cui value gap | Zhao--Cui max directional score gap | Zhao--Cui relative score error |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `1.864004e-04` | `7.699782e-04` | `9.301666e-04` | `5.142597e-04` | `2.026995e-03` | `2.578170e-03` |
| 2 | `4.204723e-04` | `1.713398e-03` | `1.469702e-03` | `6.321448e-04` | `2.589532e-03` | `2.338865e-03` |
| 3 | `6.552222e-04` | `2.649590e-03` | `1.515370e-03` | `9.175742e-04` | `4.034557e-03` | `2.295156e-03` |

Observed `T=4` CUT4 accumulation gaps against dense order-241 reference:

| dim | CUT4 value gap | CUT4 max directional score gap | CUT4 relative score error |
| ---: | ---: | ---: | ---: |
| 1 | `1.878893e-04` | `7.760044e-04` | `6.680158e-04` |
| 2 | `4.237858e-04` | `1.726542e-03` | `7.379129e-04` |
| 3 | `6.594262e-04` | `2.665903e-03` | `7.594646e-04` |

## Local Evidence

Commands:

1. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q -s tests/highdim/test_p44_nonlinear_transition.py`
2. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p44_nonlinear_transition.py`

Observed result:

- Focused pytest: `6 passed`, exit code 0.
- Compile check: exit code 0.
- CPU-only mode was deliberate; no GPU evidence is claimed. TensorFlow emitted
  CUDA initialization warnings despite `CUDA_VISIBLE_DEVICES=-1`; these are
  treated as explanatory-only because the phase is CPU-only.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `N/A - dirty worktree preserved; command manifest captures current files` |
| Command environment | CPU-only via `CUDA_VISIBLE_DEVICES=-1` and `MPLCONFIGDIR=/tmp` |
| Data version | deterministic in-test observations |
| Random seeds | deterministic branch seeds embedded in fixture config |
| Wall time | tiny local validation only |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-subplan-2026-06-07.md` |
| Repair amendment | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-repair-amendment-2026-06-08.md` |
| Test file | `tests/highdim/test_p44_nonlinear_transition.py` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-result-2026-06-07.md` |

## Gate Markers

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_local_evidence_run: `COMPLETE`
p44_evidence_audit: `COMPLETE`
p44_result_note_substance: `COMPLETE`
p44_traceability_or_nonclaim: `COMPLETE`
p44_command_count: `2`
p44_long_run_used: `false`
