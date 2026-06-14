# P0 Result: Scope And Estimation Criteria

Date: 2026-05-29

## Decision

`ACCEPTED_EXECUTED`

## Evidence Contract Result

The nonlinear-SSM evidence ladder is scoped to BayesFilter-owned experimental
TF/TFP DPF evidence under `experiments/dpf_implementation/tf_tfp/`.  It does
not edit production `bayesfilter/`, vendored student code, monograph chapters,
the high-dimensional nonlinear filtering lane, or DSGE/NAWM implementations.

## Estimation Criteria

The primary evidence target is differentiable parameter-estimation behavior:
same named scalar, `tf.GradientTape` gradient, bounded one-parameter MLE smoke,
and standard-error scaled distance when the comparator Hessian is finite.
Filtered-state RMSE remains diagnostic only.

Acceptance bands are not universal constants.  They are calibration outputs
from comparator self-consistency, DPF multi-seed variability, particle-count
sensitivity, and likelihood curvature.

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| stale context | pass | Read AGENTS/CLAUDE, ch18b, LEDH-PF-PF-OT handoff, and current DPF reports. |
| wrong comparator | pass | Kalman/UKF/CUT4 roles are separated by model and caveat. |
| value-only overclaim | pass | Same-scalar gradient/MLE evidence is central for SV and structural phases. |
| arbitrary thresholds | pass | Thresholds are calibration records, not final promotion gates. |
| hidden production drift | pass | Production writes remain forbidden. |
| monograph drift | pass | ch18b was read-only context. |
| vendored/highdim contamination | pass | No student/vendored/highdim source is used as authority. |
| DSGE/NAWM drift | pass | Structural model is a toy non-DSGE split fixture. |

## Claude Review

Plan review iteration 1: `ACCEPT`.  Claude noted a non-blocking weakness that
P0's grep verification was lighter than P7's final checks.  Codex audited this
as non-material because P7 carries the stronger verification gate.

## Caveats

No production/API readiness, HMC readiness, posterior correctness, DSGE/NAWM
validation, banking/model-risk claim, or monograph claim is concluded.
