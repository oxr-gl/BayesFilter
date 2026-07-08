# P91 Phase 4 Local Check Output

Date: 2026-06-29

Status: `PASS_P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY_CHECKS`

## Commands

```bash
git diff --check -- tests/highdim/test_p91_score_identity.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape tests/highdim/test_p91_score_identity.py -q
```

## Outcomes

- `git diff --check`: exit status 0, no output.
- Focused pytest: exit status 0.

Pytest summary:

```text
2 passed, 2 warnings in 14.60s
```

Warnings:

- TensorFlow Probability `distutils` deprecation warnings from environment
  imports. These were not Phase 4 harness failures.

## Runtime Context

| Field | Value |
| --- | --- |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Conda environment | `tf-gpu` |
| CPU/GPU status | CPU-only; `CUDA_VISIBLE_DEVICES=-1` intentionally set before pytest. |
| Data status | Simulated datasets from `model.scaled_model(theta_0).simulate(final_time=4, seed=seed)`. |
| Seeds | `9101` through `9110` for each of four theta regimes. |
| Manifest path | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json` |

## Nonclaims

These outputs do not establish exact likelihood correctness, full
observed-data/filtering score identity, previous-marginal derivative readiness,
fixed TTSIRT proposal/transport derivative readiness, GPU/XLA readiness, HMC
readiness, benchmark readiness, package/release/CI readiness, default-policy
authorization/change, or production readiness.
