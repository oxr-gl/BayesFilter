# BayesFilter LGSSM-First NeuTra/HMC Phase 3 Review Bundle

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

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-result-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-2026-07-06.json`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-subplan-2026-07-06.md`

Do not review the whole repository.

## Review Question

Does the Phase 3 result correctly report only a tiny CPU-only HMC mechanics
smoke against the Phase 2 generic LGSSM adapter, and does the refreshed Phase 4
subplan safely move to deterministic LGSSM target/reference validation without
hidden long HMC, NeuTra training, GPU, package, git, transport, DSGE/c603,
default-policy, or scientific-claim crossings?

## Evidence To Check

| Field | Contract |
| --- | --- |
| Phase 3 primary criterion | Tiny smoke completes with finite target evaluations and no crash. |
| Phase 3 veto diagnostics | Nonfinite target, crash, hidden long chain, GPU use, retuning beyond plan, or smoke promoted to convergence. |
| Phase 4 primary criterion | Deterministic target/reference residuals pass with no HMC sampling. |
| Not concluded | HMC convergence, posterior correctness, sampler ranking, NeuTra readiness, production readiness, default-policy change, scientific validity. |

## Known Local Check Results

- Phase 3 smoke JSON exists.
- JSON readback: finite sample count `8`, nonfinite sample count `0`, sample
  shape `[8, 1, 2]`, acceptance rate `1.0`.
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
