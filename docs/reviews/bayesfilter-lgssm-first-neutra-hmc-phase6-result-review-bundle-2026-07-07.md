# BayesFilter LGSSM-First NeuTra/HMC Phase 6 Result Review Bundle

Date: 2026-07-07

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

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-execution-result-2026-07-07.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-simple-nonlinear-ssm-subplan-2026-07-06.md`
- `bayesfilter/testing/lgssm_neutra_training_tf.py`
- `tests/test_lgssm_neutra_training_tf.py`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-validation-2026-07-07.json`

Do not review the whole repository.

## Review Question

Does Phase 6 satisfy the approved CPU-only tiny learned affine LGSSM
NeuTra-style training gate, with frozen payload write/reload, target-signature
binding, finite mechanics/reference checks, required local tests, and clear
nonclaims, while avoiding hidden GPU, dense IAF, long HMC, DSGE/c603 import,
package/git/default-policy changes, posterior correctness claims,
production-readiness claims, or scientific-validity claims? Does the refreshed
Phase 7 subplan inherit the Phase 6 result safely and preserve the non-DSGE
simple nonlinear SSM boundary?

## Evidence To Check

| Field | Contract |
| --- | --- |
| Phase 6 primary criterion | Frozen learned affine payload is written, reloads with the LGSSM target signature, transformed mechanics are finite, and deterministic reference residual checks pass. |
| Phase 6 veto diagnostics | Nonfinite loss, missing artifact, signature mismatch, load failure, nonfinite mechanics, reference residual failure, GPU use, dense IAF training, long HMC, or training loss promoted to correctness. |
| Phase 7 handoff | Phase 7 starts only after bounded review and targets a simple nonlinear non-DSGE SSM with explicit filter semantics. |
| Not concluded | Dense IAF quality, HMC convergence, posterior correctness, sampler superiority, generic nonlinear SSM validity, production readiness, default-policy change, scientific validity. |

## Known Local Check Results

- Phase 6 execution subplan substitute review: `VERDICT: AGREE`.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_neutra_training_tf.py -q`:
  3 passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_fixed_transport_mechanics_tf.py tests/test_lgssm_generic_target_adapter_tf.py -q`:
  12 passed.
- `python -m py_compile bayesfilter/testing/lgssm_neutra_training_tf.py tests/test_lgssm_neutra_training_tf.py`:
  passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m bayesfilter.testing.lgssm_neutra_training_tf | tee docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-validation-2026-07-07.log`:
  passed and wrote validation JSON with `passed: true`.
- `git diff --check` on Phase 6 code/docs/artifacts and refreshed handoff:
  passed.

## Requested Output

Findings first. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
