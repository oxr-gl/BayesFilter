# Review Bundle: Minimal SSL-LSTM Zhao-Cui HMC Validity Gaps Phase 2

Date: 2026-07-06

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex is supervisor and executor. This is a substitute review because the
external Claude review gate was blocked by the escalation reviewer for private
repository context transfer risk.

## Review Scope

Review the compact Phase 2 implementation plan summary below for consistency,
correctness, feasibility, artifact coverage, and boundary safety.

Primary artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase1-scalar-oracle-design-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-subplan-2026-07-06.md`
- target under test: `bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py`

Context:

- The completed `hmc-next` program established internal adapter mechanics,
  CPU-hidden regression, GPU/XLA launch smoke, and a short GPU/XLA hard-veto
  diagnostic ladder.
- It did not establish posterior correctness, HMC convergence, R-hat/ESS,
  ranking, source-faithful parity, default readiness, production readiness,
  public API/package readiness, or LEDH evidence.
- Phase 1 found that the fixture is scalar in model dimensions but
  24-dimensional in parameter space, so a full 24D posterior quadrature oracle
  is out of scope.

## Phase 2 Proposal To Audit

Implement a CPU-hidden debug/reference harness:

- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py`

Add tests:

- `tests/test_minimal_ssl_lstm_zhaocui_hmc_oracle.py`

The harness should:

1. Import fixture data from
   `bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal`.
2. Use TensorFlow only to materialize frozen fixture tensors/noise arrays and
   evaluate the target under test.
3. Recompute fixed replay log likelihood plus Gaussian prior with plain NumPy
   reference helpers inside the harness.
4. Avoid calling `tf_ssl_lstm_zhaocui_fixed_score`,
   `MinimalZhaoCuiHMCTargetAdapter.log_prob_and_grad`, TensorFlow autodiff, or
   TensorFlow transition/observation helpers inside the NumPy reference replay.
5. Evaluate selected one-dimensional conditional parameter slices with all
   non-selected coordinates fixed at
   `initial_minimal_ssl_lstm_hmc_state(1.0e-3)`.

Selected coordinates:

- `0`: `lstm_input.input.0.0`
- `4`: `lstm_recurrent.input.0.0`
- `8`: `lstm_bias.input.0`
- `12`: `latent_mean_weight.0.0`
- `13`: `latent_mean_bias.0`
- `14`: `observation_weight.0.0`
- `15`: `observation_bias.0`
- `16`: `initial_mean.0`
- `19`: `initial_std_unconstrained.0`
- `22`: `process_std_unconstrained.0`
- `23`: `observation_std_unconstrained.0`

Hypothesis settings:

- grid half-widths: `0.5`, `1.0`, `2.0`, `5.0`, `10.0`, `20.0`;
- grid point count per coordinate/width: `401`;
- edge-mass hard-veto threshold: `1.0e-4`;
- target/reference value mismatch: absolute error `<= 1.0e-9` or relative
  error `<= 1.0e-12`;
- central finite-difference score step: `1.0e-5`;
- finite-difference score max absolute mismatch: `1.0e-3`;
- deterministic repeat max absolute delta: `1.0e-12`.

Repair note after first review: a pre-implementation skeptical audit found
that maximum half-width `2.0` is too narrow for prior-dominated directions
when `prior_scale = 5.0`. The repaired ladder expands to half-width `20.0` so
the edge-mass check tests domain adequacy rather than failing predictably
inside the prior bulk.

Execution repair note: reduced-grid implementation found absolute target/
reference error about `1.4e-9` on an extreme log-density near `-3.25e6`, with
relative error about `4e-16`. The repaired value gate preserves absolute
`1.0e-9` near normal magnitudes and admits relative error `<= 1.0e-12` for
wide-tail values.

## Evidence Contract To Audit

| Field | Contract |
| --- | --- |
| Question | Does an independent minimal reference artifact agree with the internal target on selected conditional one-dimensional slices and local score diagnostics? |
| Baseline/comparator | Phase 1 reviewed oracle design; current `MinimalZhaoCuiHMCTargetAdapter` only as target under test. |
| Primary pass criterion | Schema-valid JSON/Markdown with no hard vetoes: finite deterministic target/reference values, independent NumPy replay agreement within `1.0e-9`, finite-difference score subset agreement within `1.0e-3`, and selected slice edge mass at or below `1.0e-4` for at least one predeclared width per coordinate. |
| Veto diagnostics | Reference calls target implementation path, nonfinite target/reference value, target/reference value mismatch, finite-difference score mismatch, failed deterministic repeat, grid/domain edge-mass failure, invalid artifact, unreviewed HMC/GPU/long runtime, or unsupported posterior/convergence/ranking/readiness/source-faithful claim. |
| Explanatory diagnostics | Runtime, selected coordinate rows, conditional means/std/MAP points, normalization constants, edge masses, prior scale, grid width selected, and dirty-worktree summary. |
| Not concluded | Full posterior correctness, HMC convergence, R-hat/ESS, ranking/superiority, default readiness, production readiness, public API/package readiness, source-faithful Zhao-Cui parity, or LEDH result. |

## Boundary Checks

Phase 2 must not:

- run HMC;
- run GPU/XLA runtime;
- run long diagnostics;
- make source-faithful Zhao-Cui claims;
- change public API/default policy;
- edit model files;
- install packages or fetch network resources;
- claim full posterior correctness from conditional slices.

## Specific Review Questions

1. Is the plan honest that it is conditional-slice/reference evidence, not a
   full 24D posterior oracle?
2. Is the NumPy reference independence contract strong enough to avoid a
   circular target check?
3. Are the selected coordinates sufficient for a minimal first oracle, or is a
   required scalar-dimension parameter category missing?
4. Are the tolerance and edge-mass values clearly labeled as hypotheses rather
   than established validity thresholds?
5. Are the required artifacts and local checks sufficient for recovery and
   review?
6. Are stop conditions strong enough to prevent moving to longer HMC after a
   target/reference or score mismatch?
7. Does the plan avoid source-faithful, posterior correctness, convergence,
   readiness, ranking, and LEDH overclaims?

Findings first. End with exactly:

VERDICT: AGREE

or

VERDICT: REVISE
