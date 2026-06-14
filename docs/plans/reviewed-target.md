# Reviewed Target Fixture Evidence

Date: 2026-06-08

Scope: toy contract fixture only.

This file exists to make the `ReviewedTapeAdapter` evidence path used in
BayesFilter runtime-contract tests concrete and auditable.

The reviewed target is not a scientific model and is not promoted for real HMC
use. It is the two-dimensional toy target in
`tests/test_common_inference_runtime_contracts.py`:

- value: `-0.5 * theta @ theta`;
- score: `-theta`;
- target scope: `toy-target`.

The only claim supported by this artifact is that BayesFilter's
`reviewed_gradient_tape_xla_exception` metadata requires a scoped target and
that the HMC helper rejects mismatched scopes. This does not authorize an
unreviewed GradientTape fallback for nonlinear SSM, DSGE, MacroFinance, NeuTra,
score matching, full-chain TFP HMC, or any scientific baseline.

Nonclaims:

- no sampler convergence;
- no posterior validity;
- no filtering-equation claim;
- no GPU readiness;
- no performance claim;
- no default-policy change.
