# BayesFilter LGSSM-First NeuTra/HMC Phase 5 Review Bundle

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

- `tests/test_lgssm_fixed_transport_mechanics_tf.py`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase5-frozen-transport-binding-result-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-subplan-2026-07-06.md`

Do not review the whole repository.

## Review Question

Does Phase 5 satisfy fixed identity/affine transport mechanics only, using the
validated LGSSM target signature, chain-rule checks, mismatch rejection, and
focused CPU-only tests, while avoiding hidden NeuTra training, GPU, HMC
readiness/convergence claims, package/git/default-policy changes, DSGE/c603
imports, or scientific-claim crossings? Does Phase 6 correctly stop at an
approval/request gate before any training?

## Evidence To Check

| Field | Contract |
| --- | --- |
| Phase 5 primary criterion | Transported value/score matches base chain rule on probes and rejects mismatched signatures. |
| Phase 5 veto diagnostics | Signature mismatch accepted, nonfinite transformed values/scores, fallback authority promoted, HMC/training hidden, GPU use, or DSGE/c603 transport import. |
| Phase 6 boundary | No training without explicit approval and reviewed execution subplan. |
| Not concluded | Learned NeuTra quality, HMC convergence, posterior correctness, production readiness, default-policy change, scientific validity. |

## Known Local Check Results

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_fixed_transport_mechanics_tf.py -q`: 4 passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_neutra_artifact_loader.py tests/test_fixed_transport_hmc_binding.py -q`: 12 passed.
- `python -m py_compile tests/test_lgssm_fixed_transport_mechanics_tf.py`: passed.
- `git diff --check` on Phase 5 code/planning artifacts: passed.

## Requested Output

Findings first. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
