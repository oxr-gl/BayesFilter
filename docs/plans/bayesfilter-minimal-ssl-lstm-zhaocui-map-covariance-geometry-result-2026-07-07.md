# Minimal SSL-LSTM Zhao-Cui MAP-Candidate Covariance Geometry Result

Date: 2026-07-07

Status: `VALID_DIAGNOSTIC_ARTIFACT_GEOMETRY_AND_TAU_GATE_REPAIRED_NO_VIABLE_PAIR`

## Question

Can the minimal scalar SSL-LSTM `zhaocui_fixed` HMC tuning harness use a finite
SPD curvature-derived initial covariance instead of the blunt `0.01^2 I`
baseline when available, and prevent joint `L, epsilon` candidates outside the
declared trajectory window from being viable?

## Decision

Decision: `NON_PROMOTING_DIAGNOSTIC_REPAIR_RECORDED`.

The plan was created, reviewed locally after the external Claude gate was
rejected for private-context transfer risk, implemented, checked, and executed.
The fresh CPU-hidden diagnostic wrote a valid structured artifact.

The geometry initializer no longer silently relies on the blunt diagonal
covariance in this case. The MAP-candidate attempt was rejected because the
candidate score norm was far above the diagnostic tolerance, and the artifact
honestly fell back to a finite regularized negative Hessian at the initial
position:

- `map_candidate_status`: `map_candidate_gradient_norm_above_diagnostic_tolerance`
- `map_candidate_score_norm`: `2932.5086056315927`
- `position_role`: `initial_position`
- `covariance_source`: `regularized_negative_hessian_at_initial_position`
- initial mass summary: finite SPD, condition number about `94.50`, eigenvalue
  range about `0.2645` to `25.0`

The joint `L, epsilon` gate also worked. The only ladder-passed candidates had
trajectory lengths far below the target window and were marked non-viable:

| L | step size | L * step size | target ratio | relation | viable |
| --- | --- | --- | --- | --- | --- |
| `4` | `0.07810683530168723` | `0.3124273412067489` | `0.19889742284044926` | `below_trajectory_window` | `false` |
| `6` | `0.05062199346056618` | `0.3037319607633971` | `0.1933617717219531` | `below_trajectory_window` | `false` |

The remaining blocker is therefore a tuning-design blocker: no viable joint
`L, epsilon` pair was found after enforcing the trajectory window.

## Review

| Review item | Status |
| --- | --- |
| Plan skeptical audit | `PASS_WITH_BOUNDARIES` in the plan. |
| Claude review bundle | Written at `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-review-bundle-2026-07-07.md`. |
| Claude execution | `NOT_USED`: external review gate was rejected for private repository context transfer risk. No workaround was attempted. |
| Codex substitute review | `VERDICT: AGREE` at `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-codex-substitute-review-2026-07-07.md`. |

## Implementation Summary

- Added geometry provenance fields for position role and negative-Hessian
  source through the HMC tuning configuration path.
- Updated mass-matrix inversion to symmetrize dense covariance after inverse
  precision construction.
- Added benchmark-local MAP-candidate Hessian logic with a documented
  initial-position negative-Hessian fallback and prior-precision floor.
- Updated joint `L, epsilon` candidate payloads so `viable` requires
  `trajectory_window_relation == "inside_trajectory_window"`.
- Added tests for the initial curvature fallback and for rejecting
  out-of-window joint candidates.

## Runtime Command

```bash
PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_cpu_hidden_2026-07-07.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_cpu_hidden_2026-07-07.md --tuning-output-dir docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_public_artifacts_2026-07-07 --public-timeout-budget-s 300.0 --terminal-phase6-repair-extra-attempts 1
```

## Artifacts

| Artifact | Path |
| --- | --- |
| Plan | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-plan-2026-07-07.md` |
| Claude review bundle | `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-review-bundle-2026-07-07.md` |
| Codex substitute review | `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-codex-substitute-review-2026-07-07.md` |
| Result note | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-result-2026-07-07.md` |
| JSON diagnostic | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_cpu_hidden_2026-07-07.json` |
| Markdown diagnostic | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_cpu_hidden_2026-07-07.md` |
| Public tuning result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_public_artifacts_2026-07-07/hmc_kernel_tuning_result.json` |
| Public progress result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_public_artifacts_2026-07-07/hmc_kernel_tuning_progress.json` |
| Private tuning events | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_public_artifacts_2026-07-07/private_diagnostics/hmc_tuning_events.jsonl` |
| Initial mass artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_public_artifacts_2026-07-07/private_diagnostics/mass_geometry_initial_14b2fba127e244a8.npz` |
| Windowed mass artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_public_artifacts_2026-07-07/private_diagnostics/mass_windowed_attempt_0_8b267ab232523aa3.npz` |

## Checks

| Check | Status |
| --- | --- |
| `py_compile` for touched implementation, harness, and focused tests | passed |
| `pytest tests/test_hmc_kernel_tuning_geometry.py tests/test_hmc_kernel_tuning_fixed_mass_step.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py -q` | passed: `34 passed, 27 warnings` |
| `git diff --check` | passed |
| Runtime diagnostic | exited successfully and wrote structured JSON/Markdown/public/private artifacts |
| Artifact hard-veto screen | no hard vetoes in wrapper or public tuner |

## Runtime Artifact Summary

| Diagnostic | Result | Role |
| --- | --- | --- |
| Wrapper status | `passed` | structured artifact validity |
| Phase decision | `structured_non_promoting_tuning_result_recorded` | non-promoting diagnostic |
| Public tuner status | `budget_exhausted` | active tuning blocker |
| Public tuner diagnostic role | `budget_exhausted_non_promoting` | non-promoting blocker |
| Hard vetoes | `[]` | no hard-veto invalidity |
| Windowed mass stage | `passed` | handoff stage |
| Fixed-mass step stage | `repair_or_retry` | active blocker |
| Frozen-step trajectory stage | not reached | blocked before trajectory handoff |
| Selected joint pair | absent | no viable pair |
| Runtime | `41.17925936600659` seconds | explanatory only |
| Random seed | `[20260706, 6501]` | manifest |
| Environment | TensorFlow `2.20.0`, TFP `0.25.0`, `CUDA_VISIBLE_DEVICES=-1` | CPU-hidden diagnostic |
| Git commit | `b1c97c9424907e177f8a95ab98657f07b064a081` | manifest |

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `NON_PROMOTING_DIAGNOSTIC_REPAIR_RECORDED` |
| Primary criterion status | `PASSED`: focused tests pass, geometry provenance is finite and explicit, and out-of-window joint candidates are not viable. |
| Veto diagnostic status | No hard vetoes; no non-finite mass artifact; no outside-window candidate selected; no unsupported readiness claim. |
| Main uncertainty | The fixed-mass tuning ladder still selects steps that are too small for the declared trajectory window, so no viable joint pair is available. |
| Next justified action | Create a reviewed tuning-design repair subplan for step-size bootstrap/windowed handoff or a tau-targeted ladder so candidates can reach the trajectory window. |
| What is not being concluded | No posterior correctness, convergence, zero divergences, source-faithful Zhao-Cui parity, statistical ranking, sampler superiority, default readiness, production readiness, GPU/XLA readiness, public API readiness, or package readiness. |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | `PASSED_NO_HARD_VETO` |
| Geometry initialization | `USABLE_INITIAL_POSITION_CURVATURE_FALLBACK`; not a MAP covariance |
| Tau-window viability repair | `PASSED`: out-of-window candidates are non-viable |
| Statistically supported ranking | `NOT_APPLICABLE` |
| Descriptive-only differences | acceptance, runtime, candidate counts, tau distances, Hessian condition, and stage statuses |
| Default readiness | `NOT_CHECKED` |
| Next evidence needed | A separate reviewed repair of the fixed-mass step/trajectory handoff that can produce at least one in-window viable joint pair before any frozen-trajectory or final-kernel validation. |

## Post-Run Red-Team Note

| Field | Note |
| --- | --- |
| Strongest alternative explanation | The current step-size adaptation is optimizing acceptance at steps that are too small relative to the desired trajectory length, so tau-window enforcement correctly blocks selection. |
| Result that would overturn this result | A rerun showing an out-of-window candidate marked viable, missing geometry provenance, non-SPD mass artifact, or unsupported convergence/readiness claim. |
| Weakest part of evidence | This is a one-seed CPU-hidden smoke diagnostic and the MAP candidate was rejected; it only validates the repair mechanics and blocker localization. |

## Boundary Classification

| Boundary | Status |
| --- | --- |
| CPU-hidden bounded diagnostic | `EXECUTED` |
| Trusted GPU/XLA runtime | `NOT_RUN` |
| Long HMC/convergence run | `NOT_RUN` |
| Public API/default-policy change | `NOT_INTRODUCED` |
| Model-file edit | `NOT_INTRODUCED` |
| Source-faithful Zhao-Cui parity claim | `NOT_CLAIMED` |
| Zero-divergence claim | `NOT_CLAIMED` |
| HMC convergence/posterior correctness claim | `NOT_CLAIMED` |
| Ranking/superiority claim | `NOT_CLAIMED` |

## Handoff

Do not promote this as tuned-kernel readiness. The next runbook should repair
the fixed-mass step/trajectory handoff so the joint grid can search or tune
toward the declared target trajectory window instead of repeatedly selecting
acceptance-compatible but tau-too-small candidates.
