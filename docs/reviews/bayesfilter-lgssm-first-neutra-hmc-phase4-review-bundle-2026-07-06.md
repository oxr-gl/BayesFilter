# BayesFilter LGSSM-First NeuTra/HMC Phase 4 Review Bundle

Date: 2026-07-06

## Role Contract

Read-only review only. Do not edit files, run experiments, launch agents, or
change state. Codex remains supervisor and executor.

Claude review was previously policy-rejected as an external-service
data-exfiltration risk for this program. Unless the user explicitly approves
that external review boundary, this bundle is intended for a fresh Codex
read-only substitute review.

## Exact Review Scope

Review these artifacts for consistency, correctness, feasibility, artifact
coverage, and boundary safety:

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-result-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-2026-07-06.json`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase5-frozen-transport-binding-subplan-2026-07-06.md`

Do not review the whole repository.

## Review Question

Does the Phase 4 result correctly report deterministic LGSSM target/reference
validation only, with fixed tolerances and no HMC sampling/posterior claim, and
does the refreshed Phase 5 subplan safely move to fixed identity/affine
transport mechanics without hidden NeuTra training, GPU, long HMC, package, git,
DSGE/c603, default-policy, or scientific-claim crossings?

## Evidence To Check

| Field | Contract |
| --- | --- |
| Phase 4 primary criterion | All grid values finite, value residual below `1e-9`, selected finite-difference score residual below `1e-4`. |
| Phase 4 veto diagnostics | Nonfinite grid value/score, residual failure, hidden HMC sampling, GPU use, or posterior claims beyond deterministic target validation. |
| Phase 5 boundary | Fixed identity/affine transport mechanics only; no training, no DSGE/c603 import, no HMC readiness claim. |
| Not concluded | HMC convergence, stochastic posterior validation, generic nonlinear SSM validity, NeuTra readiness, production readiness, default-policy change, scientific validity. |

## Known Local Check Results

- Phase 4 deterministic reference JSON exists.
- JSON readback: `pass=true`, `all_values_finite=true`, value residual `0.0`,
  score residual `4.7978010453419984e-11`, grid point count `625`.
- Bounded log tail includes TensorFlow CUDA/cuInit warnings under
  `CUDA_VISIBLE_DEVICES=-1`; recorded as CPU-only environment noise, not GPU
  evidence.

## Requested Output

Findings first. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
