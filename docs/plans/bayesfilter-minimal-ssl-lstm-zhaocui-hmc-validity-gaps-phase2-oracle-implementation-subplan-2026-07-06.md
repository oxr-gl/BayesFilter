# Phase 2 Subplan: Minimal Oracle Implementation And Checks

Date: 2026-07-06

Status: `PASSED`

## Phase Objective

Implement the reviewed minimal reference oracle for the scalar-dimension
`zhaocui_fixed` HMC target and run the smallest CPU-hidden checks needed to
classify target/reference and conditional-slice agreement without HMC
convergence or full posterior claims.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result exists and passed:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-governance-result-2026-07-06.md`.
- Phase 1 design result exists and passed:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase1-scalar-oracle-design-result-2026-07-06.md`.
- The minimal fixture remains scalar in model dimensions and 24-dimensional in
  parameter space.
- No posterior correctness, HMC convergence, ranking, readiness,
  source-faithful parity, or LEDH claim has been made.

## Required Artifacts

- Harness:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py`
- Tests:
  `tests/test_minimal_ssl_lstm_zhaocui_hmc_oracle.py`
- JSON artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.json`
- Markdown artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.md`
- Quiet log:
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase2_oracle_cpu_hidden_2026-07-06.log`
- Phase 2 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-result-2026-07-06.md`
- Refreshed Phase 3 longer-HMC diagnostics subplan.

## Required Checks, Tests, Reviews

Pre-implementation:

- Skeptical plan audit.
- Material read-only review of this subplan using Claude when allowed, else a
  documented fresh visible Codex substitute review.

Implementation/local checks:

- `python -m py_compile docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_oracle.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest -q tests/test_minimal_ssl_lstm_zhaocui_hmc_oracle.py`
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.md`
- `git diff --check`
- Claim-boundary scan over new Phase 2 files.

Result review:

- Review the JSON/Markdown artifact and Phase 2 result before Phase 3.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does an independent minimal reference artifact agree with the internal target on selected conditional one-dimensional slices and local score diagnostics? |
| Baseline/comparator | Phase 1 reviewed oracle design; current `MinimalZhaoCuiHMCTargetAdapter` only as target under test. |
| Primary pass criterion | The Phase 2 harness writes schema-valid JSON/Markdown with no hard vetoes: finite deterministic target/reference values, independent NumPy replay agreement with absolute error `<= 1.0e-9` or relative error `<= 1.0e-12`, finite-difference score subset agreement within `1.0e-3`, and selected slice edge mass at or below `1.0e-4` for at least one predeclared width per coordinate. |
| Veto diagnostics | Reference calls target implementation path, nonfinite target/reference value, target/reference value mismatch, finite-difference score mismatch, failed deterministic repeat, grid/domain edge-mass failure, invalid artifact, unreviewed HMC/GPU/long runtime, or unsupported posterior/convergence/ranking/readiness/source-faithful claim. |
| Explanatory diagnostics | Runtime, selected coordinate rows, conditional means/std/MAP points, normalization constants, edge masses, prior scale, grid width selected, and dirty-worktree summary. |
| Not concluded | Full posterior correctness, HMC convergence, R-hat/ESS, ranking/superiority, default readiness, production readiness, public API/package readiness, source-faithful Zhao-Cui parity, or LEDH result. |

## Reference Method

Implement a CPU-hidden debug/reference harness that:

1. Imports the frozen fixture from
   `bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal`.
2. Imports TensorFlow only for fixture tensors, deterministic stateless noise
   materialization, and target-under-test evaluation.
3. Recomputes the fixed replay log likelihood and Gaussian prior in plain
   NumPy helper functions inside the harness.
4. Does not call `tf_ssl_lstm_zhaocui_fixed_score`,
   `MinimalZhaoCuiHMCTargetAdapter.log_prob_and_grad`, TensorFlow autodiff, or
   TensorFlow transition/observation helpers inside the NumPy reference replay.
5. Evaluates target/reference values over selected conditional one-dimensional
   grids with all non-selected parameters fixed at
   `initial_minimal_ssl_lstm_hmc_state(1.0e-3)`.

The selected coordinates are:

| Index | Name | Role |
| --- | --- | --- |
| 0 | `lstm_input.input.0.0` | LSTM input gate weight |
| 4 | `lstm_recurrent.input.0.0` | recurrent gate weight |
| 8 | `lstm_bias.input.0` | gate bias |
| 12 | `latent_mean_weight.0.0` | transition mean scale |
| 13 | `latent_mean_bias.0` | transition mean bias |
| 14 | `observation_weight.0.0` | observation loading |
| 15 | `observation_bias.0` | observation intercept |
| 16 | `initial_mean.0` | latent initial mean |
| 19 | `initial_std_unconstrained.0` | latent initial scale transform |
| 22 | `process_std_unconstrained.0` | process scale transform |
| 23 | `observation_std_unconstrained.0` | observation scale transform |

Grid/domain hypothesis:

- widths: `0.5`, `1.0`, `2.0`, `5.0`, `10.0`, `20.0`;
- points per width: `401`;
- edge-mass hard-veto threshold: `1.0e-4`;
- selected row per coordinate: narrowest width passing the edge-mass threshold.

Repair note: the initial width ladder stopped at `2.0`, which is too narrow
for prior-dominated directions under `prior_scale = 5.0`. The expanded ladder
keeps the same mass check but avoids turning a foreseeable domain-design flaw
into a false target/reference veto.

Tolerance hypotheses:

- target/reference value mismatch: absolute error `<= 1.0e-9` or relative
  error `<= 1.0e-12`;
- central finite-difference step: `1.0e-5`;
- finite-difference score max absolute mismatch: `1.0e-3`;
- deterministic repeat max absolute delta: `1.0e-12`.

Execution repair note: a reduced-grid implementation check found
machine-epsilon relative agreement at extreme negative log-density values on
the observation-scale slice, with absolute error about `1.4e-9` on a value near
`-3.25e6`. The value gate now keeps the reviewed strict absolute tolerance and
adds a relative tolerance so wide-tail roundoff does not become a false veto.

## Expected Artifact Schema

The JSON artifact must include:

- `schema_version`;
- `status`;
- `artifact_role`;
- `target_quantity`;
- `reference_independence_contract`;
- `fixture`;
- `selected_coordinates`;
- `grid_settings`;
- `tolerances`;
- `target_reference_value_check`;
- `finite_difference_score_check`;
- `conditional_slice_rows`;
- `hard_vetoes`;
- `diagnostic_roles`;
- `decision_table`;
- `run_manifest`;
- `nonclaims`.

## Forbidden Claims And Actions

Do not run HMC, GPU/XLA runtime, long diagnostics, source-faithful work,
package installation, network fetch, public API/default-policy changes, or
model-file edits in Phase 2.

Do not claim full posterior correctness from conditional slices. Do not claim
HMC convergence, ranking, readiness, source-faithful parity, or LEDH evidence.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only if:

- Phase 2 local checks pass;
- the JSON artifact status is `passed`;
- Phase 2 result records the decision table and nonclaims;
- result review converges;
- Phase 3 longer-HMC diagnostics subplan is refreshed with the Phase 2 artifact
  as a comparator and with explicit runtime approval requirements.

If Phase 2 fails with a target/reference or score mismatch, the next phase must
be a localization/repair subplan, not longer HMC.

## Stop Conditions

Stop if the independent reference cannot be implemented without circular calls,
if any hard veto fires, if grid/domain mass checks fail, if review does not
converge after five rounds for the same blocker, or if continuing would require
unreviewed HMC/GPU/long runtime or another human-required boundary.
