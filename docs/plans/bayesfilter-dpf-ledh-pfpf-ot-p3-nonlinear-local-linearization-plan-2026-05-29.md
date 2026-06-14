# P3 Plan: Nonlinear Local Linearization

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: can the range-bearing fixture provide a TF/TFP local Jacobian contract
for LEDH without treating UKF or local linearization as ground truth?

Baseline/comparator: range-bearing observation function and TF/TFP UKF
approximate reference.

Pass criterion: result artifact records the analytic range-bearing Jacobian,
angle residual convention, finite checks, and the proxy-only status of nonlinear
diagnostics.

Veto diagnostics: undefined Jacobian near origin, missing angle wrapping, hidden
NumPy use, or exactness claimed for nonlinear local closure.

Not concluded: nonlinear filter correctness, UKF ground truth, production
readiness, NAWM-scale readiness.

## Inputs

- `experiments/dpf_implementation/tf_tfp/fixtures/range_bearing_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/ukf_tf.py`
- P1 math contract result.

## Outputs

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-result-2026-05-29.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`
- `experiments/dpf_implementation/tf_tfp/flows/`

## Forbidden Write Set

Production code, vendored code, monograph chapters, high-dimensional lane
artifacts, and student code.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop if the range-bearing Jacobian cannot be bounded on the fixture, if angle
residuals are not wrapped, or if local linearization is used as correctness
evidence rather than a proposal mechanism.

## Verification Commands

- targeted range-bearing runner once implementation exists;
- `rg -n "range-bearing|Jacobian|angle|UKF is approximate" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-*-2026-05-29.md`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No ground-truth UKF, production, HMC, posterior, NAWM-scale, or monograph claim.
