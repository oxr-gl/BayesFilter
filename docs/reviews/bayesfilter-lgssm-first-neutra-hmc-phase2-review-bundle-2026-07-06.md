# BayesFilter LGSSM-First NeuTra/HMC Phase 2 Review Bundle

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

- `bayesfilter/testing/lgssm_generic_target_adapter_tf.py`
- `tests/test_lgssm_generic_target_adapter_tf.py`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase2-lgssm-target-adapter-result-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-subplan-2026-07-06.md`

Do not review the whole repository.

## Review Question

Does the Phase 2 implementation satisfy the reviewed LGSSM generic-adapter
boundary: stable generic SSM contract, rank-2 prior/likelihood value-score
functions, composed generic posterior adapter, focused CPU-only tests, explicit
nonclaims, and no hidden HMC, NeuTra training, GPU, package, git, transport,
DSGE/c603, default-policy, or scientific-claim crossing?

## Evidence To Check

| Field | Contract |
| --- | --- |
| Primary criterion | Adapter emits finite rank-2 posterior value/score, stable target signature, and focused gradient/reference checks pass. |
| Veto diagnostics | Process-local signature, shape ambiguity, nonfinite value/score, gradient/reference mismatch, hidden HMC/training/GPU, or DSGE/c603 dependency. |
| Required checks | Focused LGSSM adapter tests, generic target-builder regression tests, QR compact loglikelihood regression tests, `py_compile`, and `git diff --check`. |
| Not concluded | HMC convergence, posterior validation, NeuTra readiness, production readiness, default-policy change, sampler ranking, scientific validity. |

## Known Local Check Results

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_generic_target_adapter_tf.py -q`: 8 passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_target_builder.py tests/test_linear_qr_compact_loglik_tf.py -q`: 23 passed.
- `python -m py_compile bayesfilter/testing/lgssm_generic_target_adapter_tf.py tests/test_lgssm_generic_target_adapter_tf.py`: passed.
- `git diff --check` on Phase 2 code/test/planning artifacts: passed.

## Requested Output

Findings first. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
