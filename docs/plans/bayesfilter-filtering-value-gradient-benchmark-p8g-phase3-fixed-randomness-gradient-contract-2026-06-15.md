# P8g-G3 Fixed-Randomness Gradient Contract

Date: 2026-06-15

Status: `ACTIVE_G3_CONTRACT`

## Scope

This contract covers only:

- row: `zhao_cui_sv_actual_nongaussian_T1000`;
- route variant: `p8g_sv_scalar_graph`;
- resampling route: `none`;
- coordinate: `canonical_unconstrained`;
- theta: `(Phi^{-1}(gamma), log(beta))`;
- fixed sigma: `1.0`;
- flow observation: `log(y_t^2 + 1e-6) - 2 log(beta)`;
- target correction: raw zero-mean SV normal density.

## Randomness Contract

For each seed and horizon prefix:

- initial standard normals use stateless seed salt `110`;
- transition standard normals at time `t` use stateless seed salt `1110 + t`;
- random normal draws are precomputed outside XLA and treated as fixed inputs
  to the graph objective;
- no resampling randomness is used.

## Gradient Kernel Contract

G2b value profiles use the XLA value route for speed evidence. G3 gradient
checks use a non-XLA TensorFlow graph variant of the same scalar equations
because reverse-mode differentiation through XLA `tf.while_loop` currently
raises TensorList boundary errors in this environment.

This split is an implementation detail for gradient validation. It does not
authorize a generic Algorithm 1 gradient claim, a stochastic PF marginal
gradient claim, or HMC readiness.

## Promotion Rules

Gradient evidence may pass G3 only if:

- values and gradients are finite;
- repeated evaluation with the same fixed random draws is identical within
  recorded tolerance;
- finite-difference directional checks are recorded;
- CPU/GPU gradient outputs are compared in the same coordinate;
- artifacts preserve the nonclaims above.
