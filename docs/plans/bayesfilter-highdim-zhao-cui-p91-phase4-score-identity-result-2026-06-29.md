# P91 Phase 4 Result: Local Component Score Identity

Date: 2026-06-29

Status: `PASS_P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 4 ran the reviewed CPU-only score-identity harness and passed for the implemented local complete-data Zhao-Cui SIR d18 component score. |
| Primary criterion status | Passed: all four regimes and all three parameter components satisfy `abs(mean score) <= 2 * sample_standard_deviation` across ten seeds. |
| Veto diagnostic status | Passed: scores are finite; component failures are not masked; Phase 3 is not claimed as a full FD pass; no exact-likelihood, full filtering-score, GPU/XLA, HMC, package/release/CI, default-policy, or production claim is made. |
| Main uncertainty | This validates the local complete-data component score identity, not the full observed-data/filtering score through previous marginal and fixed TTSIRT transport/proposal derivatives. Advisory `abs(mean)/SE` z-scores exceed 2 for some components, so more seeds would be appropriate before making a stronger statistical precision claim. |
| Next justified action | Review this Phase 4 result and refreshed Phase 5 GPU/XLA JIT subplan. |
| What is not being concluded | No exact likelihood proof, full observed-data/filtering score identity, previous-marginal derivative readiness, fixed TTSIRT proposal/transport derivative readiness, HMC readiness, GPU/XLA readiness, benchmark result, package/release/CI readiness, default-policy authorization/change, or production readiness. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the implemented local Zhao-Cui SIR d18 component score have empirical zero-mean behavior at true parameters across multiple simulated regimes/seeds? |
| Baseline/comparator | Data simulated from each `theta_0`; theoretical zero-mean score identity for the same local complete-data scalar components. |
| Primary criterion | Passed: every regime/component satisfies the reviewed `2 sample SD` finite-sample screen. |
| Veto diagnostics | Passed: no nonfinite score, no full filtering-score overclaim, no hidden previous-marginal/fixed-TTSIRT derivative readiness claim, no strict `2 SE` gate substitution, and no aggregate-only masking. |
| Explanatory diagnostics | Componentwise mean, sample standard deviation, standard error, advisory `abs(mean)/SE`, per-seed score table, theta regimes, and seed table are in the manifest. |
| Not concluded | No exact likelihood proof, root-solving validity, Hessian/information equality, HMC readiness, GPU speed superiority, package/release/CI readiness, default-policy authorization/change, or production readiness. |
| Artifact | Score-identity manifest, preserved local-check output, this result, and refreshed Phase 5 subplan. |

## Manifest Summary

Manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json`

Manifest status:

```text
PASS_P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY
```

Primary criterion:

```text
for every regime and parameter component, abs(mean_score) <= 2 * sample_standard_deviation across 10 seeds
```

| Regime | Theta | Pass | Mean score | Sample SD | Advisory abs(mean)/SE |
| --- | --- | --- | --- | --- | --- |
| baseline_moderate | `(0.0, 0.0, 0.0)` | true | `[-75.2299, 74.4176, 10.3922]` | `[180.9463, 64.1452, 10.8707]` | `[1.3147, 3.6687, 3.0231]` |
| low_infection | `(-0.35, 0.15, 0.0)` | true | `[-11.9234, 29.8328, 10.3922]` | `[52.4840, 25.6554, 10.8707]` | `[0.7184, 3.6772, 3.0231]` |
| high_infection | `(0.25, -0.15, 0.1)` | true | `[-99.5646, 134.4976, 10.3922]` | `[383.1206, 113.3349, 10.8707]` | `[0.8218, 3.7528, 3.0231]` |
| near_boundary_stable | `(0.45, -0.35, 0.2)` | true | `[57.4507, 174.3811, 10.3922]` | `[501.5722, 140.6286, 10.8707]` | `[0.3622, 3.9213, 3.0231]` |

Interpretation:

- The reviewed `2 sample SD` score-identity screen passes for all regimes and
  components.
- The advisory standard-error z-scores are above 2 for some components. Under
  the reviewed Phase 4 plan, these are not veto diagnostics; they indicate that
  a future stronger statistical precision claim should use more seeds or a
  separate replication plan.
- The third parameter component has identical mean/SD/advisory-z across
  regimes because this local component score depends on observation-noise
  scaling and the same seed/observation dimension protocol was used in each
  regime.

## Local Checks

Commands:

```bash
git diff --check -- tests/highdim/test_p91_score_identity.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape tests/highdim/test_p91_score_identity.py -q
```

Outcome:

- `git diff --check`: passed.
- Focused pytest: `2 passed, 2 warnings in 14.60s`.
- Warnings were TensorFlow Probability `distutils` deprecation warnings from
  environment imports; they were not Phase 4 harness failures.
- The pytest command intentionally set `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA,
  XLA, HMC, benchmark, package/network, release, CI, production, or
  default-policy command was run.

Preserved output:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-local-check-output-2026-06-29.md`

## Blockers Preserved

The manifest preserves:

- `full_observed_data_filtering_score_identity = NOT_CLAIMED`;
- `BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED`.

Phase 4 did not claim full observed-data/filtering score identity.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty research worktree; unrelated dirty changes preserved. |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Conda environment | `tf-gpu` |
| Execution target | CPU-only local complete-data component score-identity harness. |
| CPU/GPU status | CPU-only; `CUDA_VISIBLE_DEVICES=-1` intentionally set for pytest. |
| Commands | `git diff --check -- tests/highdim/test_p91_score_identity.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md`; `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape tests/highdim/test_p91_score_identity.py -q` |
| Data version | `N/A`; simulated datasets generated by `model.scaled_model(theta_0).simulate(final_time=4, seed=seed)`. |
| Random seeds | `9101` through `9110` for each of four regimes. |
| Wall time | Pytest reported `14.60s`; diff check completed with exit code 0 and no output. |
| Phase 3 accepted diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-result-2026-06-29.md` |
| Phase 4 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-subplan-2026-06-29.md` |
| Harness | `tests/highdim/test_p91_score_identity.py` |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json` |
| Local check output | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-local-check-output-2026-06-29.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-result-2026-06-29.md` |
| Refreshed Phase 5 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-subplan-2026-06-29.md` |

## Phase 5 Handoff

Phase 5 may proceed only after Claude review agrees on this Phase 4 result and
the refreshed Phase 5 GPU/XLA JIT subplan. Phase 5 must use trusted/escalated
GPU execution and must preserve that Phase 4 validates only the local
complete-data component score identity.
