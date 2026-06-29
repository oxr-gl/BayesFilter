# P91 Phase 4 Subplan: Score-Identity Validation

Date: 2026-06-29

Status: `EXECUTABLE_PENDING_REVIEW_AFTER_PHASE3_OWNER_ACCEPTANCE`

## Phase Objective

Run the first governed P91 score-identity validation for Zhao-Cui SIR d18 after
the Phase 3 limited-FD diagnostic was owner-accepted for continuation with
caveats. Phase 4 checks whether the implemented local parameterized SIR d18
component score has empirical zero-mean behavior at true parameters across
multiple regimes and simulated datasets.

This is a score-identity validation for the currently implemented complete-data
local SIR component score surface:

- initial parameter score;
- transition parameter score;
- observation parameter score;
- sum over a short simulated path.

It is not a full observed-data Zhao-Cui filtering score identity, not a full
source-route derivative claim, and not a waiver of previous-marginal or fixed
TTSIRT proposal/transport derivative blockers.

## Entry Conditions Inherited From Previous Phase

- Phase 3 limited-FD manifest status was
  `BLOCK_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY`, but the owner reviewed the
  threshold provenance and accepted the diagnostic for continuation with
  caveats in:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-result-2026-06-29.md`.
- Phase 2 batched API reviewed pass.
- Phase 1 score contract reviewed pass.
- This Phase 4 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Score-identity plan/manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json`
- New focused harness:
  `tests/highdim/test_p91_score_identity.py`
- Preserved local-check output:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-local-check-output-2026-06-29.md`
- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-result-2026-06-29.md`
- Refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

After Claude agrees on this executable subplan, implement the focused harness
and run only:

```bash
git diff --check -- tests/highdim/test_p91_score_identity.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape tests/highdim/test_p91_score_identity.py -q
```

After those commands, write:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-local-check-output-2026-06-29.md
```

Claude review is required for the Phase 4 result and refreshed Phase 5
subplan.

CPU-only intent is required because Phase 4 is a statistical score-identity
validation of the implemented local score surface, not a GPU/XLA gate. No
GPU/CUDA/XLA/HMC/benchmark/package/release/CI/default-policy command is
authorized.

## Runtime Design

The focused harness must use:

- model: `highdim.parameterized_zhao_cui_sir_austria_model()`;
- state dimension: `18`;
- parameter order:
  `log_kappa_scale`, `log_nu_scale`, `log_obs_noise_scale`;
- simulated path length: `final_time = 4`;
- seed set per regime: `9101` through `9110`;
- true-parameter regimes:
  - baseline/moderate: `(0.0, 0.0, 0.0)`;
  - low infection: `(-0.35, 0.15, 0.0)`;
  - high infection: `(0.25, -0.15, 0.1)`;
  - near-boundary stable: `(0.45, -0.35, 0.2)`.

For each regime and seed, generate a dataset from
`model.scaled_model(theta_0).simulate(final_time=4, seed=seed)`. Then compute
the implemented local complete-data score at the same `theta_0`:

```text
score(theta_0, x_0:T, y_0:T)
  = initial_log_density_parameter_score(theta_0, x_0)
    + sum_t transition_log_density_parameter_score(theta_0, x_{t-1}, x_t)
    + sum_t observation_log_density_parameter_score(theta_0, x_t, y_t)
```

The harness must emit the manifest path above with command, git commit, Python
executable, conda environment, CPU-only status, data generator, seeds, regimes,
path length, componentwise per-seed scores, means, sample standard deviations,
standard errors, advisory `abs(mean)/SE` z-scores, pass/fail booleans, and
nonclaims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the implemented local Zhao-Cui SIR d18 component score have empirical zero-mean behavior at true parameters across multiple simulated regimes/seeds? |
| Baseline/comparator | Data simulated from each `theta_0`; theoretical zero-mean score identity for the same local complete-data scalar components. |
| Primary criterion | For every regime and parameter component, `abs(mean score) <= 2 * sample_standard_deviation` across the 10 seeds. If sample standard deviation is numerically zero, require `abs(mean score) <= 1e-12`. All per-seed values must be finite. |
| Veto diagnostics | Score identity claimed as exact likelihood proof; full observed-data/filtering score identity claimed; previous-marginal or fixed TTSIRT derivative blockers hidden; strict `2 SE` treated as the owner-requested gate; too few seeds without caveat; NaN/Inf; branch/setup drift; audit/tuning cloud leakage; aggregate-only masking of component failures. |
| Explanatory diagnostics | Componentwise mean, sample standard deviation, standard error, advisory `abs(mean)/SE`, covariance/joint advisory statistic if present, seed table, runtime/memory. |
| Not concluded | No exact likelihood proof, root-solving validity, Hessian/information equality, HMC readiness, GPU speed superiority, package/release/CI readiness, default-policy authorization/change, or production readiness. |
| Artifact | Score-identity manifest, preserved local-check output, Phase 4 result, and refreshed Phase 5 subplan. |

## Skeptical Plan Audit

| Risk | Audit conclusion |
| --- | --- |
| Wrong baseline | The comparator is zero mean score for data simulated from the same true parameter under the same local component scalar, not FD or an external likelihood oracle. |
| Proxy metric promoted | Phase 4 validates local component-score identity only; it does not promote exact likelihood correctness, full filtering-score identity, GPU/XLA, HMC, or production readiness. |
| Missing stop condition | Nonfinite scores, hidden derivative blockers, aggregate-only pass, or unsupported broader claims stop the phase. |
| Unfair comparison | Each score is evaluated at the same theta used to simulate the dataset. |
| Hidden assumption | `2 SD` is the owner-requested finite-sample acceptance screen; stricter `2 SE` z-scores are advisory diagnostics and may motivate later replication, but are not this phase's pass criterion. |
| Stale context | Phase 3 FD remains a limited accepted diagnostic with caveats, not a full FD pass. |
| Environment mismatch | CPU-only execution hides GPU before TensorFlow import; GPU/XLA is deferred to Phase 5. |
| Artifact mismatch | The harness writes a manifest directly answering the score-identity question and the result must include the exact command/run manifest. |

Audit status: `PASS_P91_PHASE4_SCORE_IDENTITY_PLAN_AUDIT`

## Forbidden Claims/Actions

- Do not claim exact likelihood correctness.
- Do not claim full observed-data/filtering score identity.
- Do not claim previous-marginal or fixed TTSIRT derivative readiness.
- Do not claim the accepted Phase 3 diagnostic is a full FD pass or true
  gradient-oracle check.
- Do not solve `score(theta)=0` as a gate.
- Do not require Hessian/information equality as a gate.
- Do not run GPU/XLA/HMC/benchmarks unless explicitly reviewed for this phase.
- Do not authorize or interpret Phase 4 as enabling package/release/CI
  activity, default-policy changes, or any production-promotion step.
- Do not change theta regimes/tolerances after seeing results.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if:

- Phase 4 result receives Claude `VERDICT: AGREE`;
- Phase 5 subplan receives Claude `VERDICT: AGREE`;
- the local component-score identity gate passes or Phase 5 is converted to
  blocker-only closeout.

## Stop Conditions

- Score computation is unavailable for simulated datasets.
- Local component-score identity fails beyond reviewed diagnostic/repair scope.
- Local checks fail and cannot be repaired.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed GPU/HMC/default boundaries.

## End-Of-Phase Requirements

1. Run required local checks/tests authorized by this reviewed Phase 4 subplan.
2. Write Phase 4 result / close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 4 result and Phase 5 subplan.
