# P7 Result: Final Audit And Handoff

Date: 2026-05-29

## Decision

`EXECUTED_WITH_P6_STRUCTURED_CALIBRATION_BLOCKER`

## Phase Status

| Phase | Status | Artifact |
| --- | --- | --- |
| P0 scope/criteria | accepted/executed | `bayesfilter-dpf-nonlinear-ssm-evidence-p0-scope-and-estimation-criteria-result-2026-05-29.md` |
| P1 LGSSM | passed | `dpf_nonlinear_ssm_lgssm_multiseed_2026-05-29.json` |
| P2 range-bearing | passed | `dpf_nonlinear_ssm_range_bearing_stress_2026-05-29.json` |
| P3 CUT4 | accepted/executed | TF/TFP CUT4 component |
| P4 stochastic volatility | passed smoke | `dpf_nonlinear_ssm_sv_gradient_mle_2026-05-29.json` |
| P5 structural AR(1) | residual/gradient smoke executed with estimation calibration warning | `dpf_nonlinear_ssm_structural_ar1_gradient_mle_2026-05-29.json` |
| P6 particle/seed ladder | structured blocker | particle-count calibration not run |

## Models Tested

- LGSSM with exact Kalman reference.
- Range-bearing Gaussian with UKF approximate reference, bootstrap PF, and
  bootstrap OT-DPF comparators.
- Stochastic volatility with differentiable TF/TFP CUT4 comparator.
- Structural AR(1) quadratic-completion toy model with differentiable TF/TFP
  CUT4 comparator and deterministic residual veto.

## Gradient And Estimation Status

SV same-scalar gradient smoke passed.  CUT4 and DPF coarse-grid MLEs for `mu`
both selected -1.0, with SE-scaled distance 0.0.

Structural same-scalar gradient smoke executed and deterministic residual was
0.0.  CUT4 selected `b=0.65`; DPF median selected `b=0.35`, with SE-scaled
distance 1.196399784219709.  This is not estimator equivalence.  It is the
reason P6 is recorded as a structured calibration blocker.

## Unresolved Risks

- CUT4 is a comparator, not ground truth.
- SV and structural MLEs use coarse bounded grids and smoke-scale particle
  counts.
- Structural DPF-vs-CUT4 gradient and MLE diagnostics differ visibly despite
  the residual veto passing.
- TensorFlow emits CUDA plugin/cuInit startup messages even on CPU-only runs;
  manifests record `CUDA_VISIBLE_DEVICES=-1`, `cpu_only=true`, and no visible
  GPUs.

## Verification

| Command | Result |
| --- | --- |
| `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp` | passed, no matches |
| `rg -n "^(from|import) .*?(student|vendored|highdim|DSGE|NAWM)|^(from|import) (student|vendored|highdim|DSGE|NAWM)" experiments/dpf_implementation/tf_tfp` | passed, no matches |
| `python -m py_compile` over touched Python files | passed |
| LGSSM runner, `--validate-only`, `--check-reproducibility` | passed |
| range-bearing runner, `--validate-only`, `--check-reproducibility` | passed |
| SV runner, `--validate-only`, `--check-reproducibility` | passed |
| structural runner, `--validate-only`, `--check-reproducibility` | passed |
| `python -m json.tool` over four new nonlinear-SSM JSON outputs | passed |
| lane-scoped trailing whitespace `rg` | passed, no matches |
| `git diff --check` | passed |
| `git status --short -- bayesfilter tests` | passed, no production/test changes |
| `git status --short --branch` | completed; worktree has many unrelated pre-existing dirty/untracked files |

The target CPU-only commands used `CUDA_VISIBLE_DEVICES=-1` before TensorFlow
imports.  TensorFlow emitted CUDA plugin/cuInit startup messages despite CPU
hiding, but manifests recorded `cpu_only=true`, pre-import CUDA visibility
`-1`, and no visible GPU devices.

## Caveats

No production/API readiness, HMC readiness, posterior correctness, DSGE/NAWM
validation, banking/model-risk claim, or monograph claim is concluded.

## Claude Result Review

- Iteration 1: `REJECT`.  Codex agreed with the material findings: P7 was not
  closed, P6 needed explicit structured-blocker status, and structural
  smoke-pass language could be mistaken for estimator-equivalence evidence.
  The artifacts were patched accordingly before resubmission.
- Iteration 2: `ACCEPT`.  Claude confirmed the prior rejection findings were
  fixed and accepted the lane as executed with a P6 structured particle-count
  calibration blocker, not as estimator-equivalence validation.
