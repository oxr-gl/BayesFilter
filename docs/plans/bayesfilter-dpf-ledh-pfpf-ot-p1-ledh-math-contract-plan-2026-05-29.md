# P1 Plan: LEDH Math Contract

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: can the lane state a finite-step TF/TFP LEDH flow contract with
explicit local linearization, affine map, invertibility, and log determinant?

Baseline/comparator: DPF3 PF-PF object contract and LGSSM/range-bearing fixture
interfaces.

Pass criterion: result artifact defines the local Gaussian closure, map
`x1 = m_post + L_post L_prior^{-1}(x0 - m_prior)`, the forward log determinant,
and diagnostics needed before implementation.

Veto diagnostics: missing local Jacobian semantics, singular covariance without
blocker, unclear forward/inverse convention, or exactness claimed outside the
linear-Gaussian case.

Not concluded: continuous-time EDH ODE exactness, nonlinear correctness,
production readiness, or monograph validation.

## Inputs

- `docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md`
- `experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/fixtures/range_bearing_tf.py`

## Outputs

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-result-2026-05-29.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`

## Forbidden Write Set

Production code, vendored code, monograph chapters, high-dimensional lane
artifacts, and implementation modules.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop if the affine map/log-det convention cannot be stated, if local
linearization for range-bearing is not defined, or if the contract would
overstate nonlinear exactness.

## Verification Commands

- `rg -n "x1 =|log determinant|linear-Gaussian|not exact" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-*-2026-05-29.md`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No production, HMC, posterior, NAWM-scale, monograph, or nonlinear exactness
claim.
