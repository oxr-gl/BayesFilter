# P82 Phase 1 Result: Route / Protocol / Harness Inventory

status: COMPLETE_PENDING_REVIEW
date: 2026-06-22
phase: P1

## Question

What exact local paths and gaps must P2/P3 address before LEDH gradient testing
can run?

## Decision

P1 may hand off to P2 for regression-FD harness protocol repair, but not to
gradient validation.  The current checkout has reusable batched-theta and
seed-averaging surfaces, yet the existing regression-FD harness still differs
from the corrected P82 protocol in two material ways:

- it accepts 7/9/15/17 offsets but not the required 13-point line protocol;
- it trims extreme offset abscissae, not the highest and lowest mean-over-seed
  objective values.

P1 also found a separate P3 route issue: the exported SIR multistate Zhao-Cui
score path still records a `tensorflow_forward_accumulator_for_model_log_density`
target derivative backend.  That route must not be treated as the analytical
comparator until P3 audits or repairs it.  Autodiff/JVP remains diagnostic-only.

## Skeptical Plan Audit

Pass with boundary warning.  The read-only inventory answered the P1 question
without code edits, GPU/CUDA work, or numerical validation.  The material
wrong-baseline risk is now explicit: a ForwardAccumulator/JVP-backed route is
present and cannot be silently promoted as the Zhao-Cui analytical comparator.
The P2 handoff is therefore limited to the FD harness protocol; P3 owns
comparator-route reconciliation.

## Commands Run

Read-only commands:

```bash
rg -n "multistate_nonlinear_fixed_design_tt_score_path|target_derivative_backend|ForwardAccumulator|analytic_gradient|ParameterizedZhaoCuiSIRSSM" bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p81-* docs/plans/bayesfilter-highdim-zhao-cui-p82-*
rg -n "batched-theta|regression-offsets|trim-extreme|slope_standard_error|seed_microbatch|num-particles|offset" docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
rg -n "experimental_batched_ledh_pfpf_ot|streaming_batched_ledh|transport_ad_mode|batch-seeds|num-particles|value_and_score|value_core" docs/benchmarks experiments/dpf_implementation/tf_tfp -g '*.py'
git status --short
```

## Route Inventory

| Surface | Anchor | P82 interpretation |
|---|---|---|
| Scalar fixed-branch score diagnostics | `bayesfilter/highdim/filtering.py:1130`, `bayesfilter/highdim/filtering.py:1369` | Uses `tensorflow_forward_accumulator_for_model_log_density`; diagnostic-only for P82 comparator purposes. |
| Multistate score function | `bayesfilter/highdim/filtering.py:1376` | Exported SIR-capable score surface exists. |
| Multistate multi-parameter wrapper | `bayesfilter/highdim/filtering.py:1412` to `bayesfilter/highdim/filtering.py:1456` | Concatenates single-parameter partial score results. |
| Multistate score diagnostics | `bayesfilter/highdim/filtering.py:1460` to `bayesfilter/highdim/filtering.py:1467`, `bayesfilter/highdim/filtering.py:1695` to `bayesfilter/highdim/filtering.py:1703` | Records `multistate_nonlinear_fixed_design_tt_score_path`, but target derivative backend is ForwardAccumulator/JVP. |
| JVP helper | `bayesfilter/highdim/filtering.py:4038` to `bayesfilter/highdim/filtering.py:4047` | Uses `tf.autodiff.ForwardAccumulator`; cannot be promoted as analytical comparator in P82. |
| Parameterized SIR wrapper | `bayesfilter/highdim/models.py:655`, `bayesfilter/highdim/models.py:825` | Local SIR parameterized model surface exists. |

P3 must either identify the already-implemented analytical derivative route
with exact anchors or patch/route the comparator so the Zhao-Cui analytical
derivative is used.  If P3 cannot prove that route, it must stop or classify
any new behavior honestly rather than claiming source-faithful analytical
comparison.

## Regression-FD Harness Inventory

| Surface | Anchor | Status |
|---|---|---|
| Default seeds | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:83` | Already defaults to five seeds. |
| Particle argument | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:85` | Present; P82 run commands must set `--num-particles 1000` for FD. |
| Offset parsing | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:57` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:65` | Rejects 13 points; P2 must allow exactly the P82 13-point grid. |
| Default offsets | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:104` | Currently 9 points; P2 should set or document the P82 13-point invocation explicitly. |
| Batched theta mode | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:114` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:126` | Present and reusable. |
| Slope SE | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:356` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:376` | OLS slope SE already computed. |
| Seed/offset mapping | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:560` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:645` | Batched theta repeats each seed over all offsets and averages over seeds by offset; P2 should preserve and expose this mapping. |
| Trimming | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:650` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:686` | Currently drops smallest/largest `x`, not highest/lowest mean value; P2 must patch value-outlier trimming. |
| Direction diagnostic output | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:700` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:755` | Already records raw line values and fit values; P2 should add dropped value/outlier metadata and protocol labels. |

## LEDH Surface Inventory

| Surface | Anchor | Status |
|---|---|---|
| SIR benchmark seeds and particles | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:100` to `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:102` | Present; P82 actual-gradient commands must set five seeds and `--num-particles 10000`. |
| Streaming value core | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:487` to `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:518` | Existing LEDH-PFPF-OT value surface. |
| Streaming module value core | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:256` | Existing streaming value implementation. |
| Streaming module value and score | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:616` | Existing value+score implementation. |
| Dense value core | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:821` | Existing non-streaming value implementation. |
| Dense value and score | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:968` | Existing non-streaming value+score implementation. |

## Dirty Worktree Constraint

`git status --short` shows many modified and untracked files predating this P82
continuation, including code under `bayesfilter/`, tests, generated docs, and
P81/P82 plan artifacts.  P2 must not revert unrelated changes.  If P2 edits a
dirty target file, it must preserve the surrounding user/current work and keep
the diff narrowly scoped to the reviewed harness protocol.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Hand off to P2 harness subplan | Passed | No P1 code/GPU work; harness gaps identified | Whether target harness has existing tests to extend | Draft and review P2 subplan before code edits | No numerical gradient validation |
| Defer comparator readiness to P3 | Passed with warning | JVP route found and not promoted | Location/status of user-mentioned analytical derivative route | P3 must audit or repair exact Zhao-Cui analytical route | No Zhao-Cui comparator certification |
| Preserve 2-SE caution | Passed | No oracle framing | SE assumptions must be stated in P7 | Keep triage-only wording in later artifacts | No correctness certification from `<=2 SE` |

## Required P2 Handoff

P2 must create or patch local tests for the regression-FD protocol and then
patch `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py` only
as needed to support:

- 13-point regression-offset parsing;
- P82 invocation with 13 offsets, five seeds, and `--fd-evaluation-mode batched-theta`;
- value-outlier trimming that drops the highest and lowest mean-over-seed line
  objective values, not extreme offsets;
- deterministic tie-breaking for tied highest/lowest mean objective values;
- raw per-offset mean values, fit values, dropped value metadata, and fit point
  count of 11;
- preservation of raw records, with only the fit subset changing;
- preservation of seed/offset mapping in batched-theta mode;
- slope standard error in the output artifact.

P2 must not claim comparator correctness, LEDH gradient validity, HMC readiness,
posterior correctness, or production/default readiness.
Regression FD remains a diagnostic construction, not an oracle and not a
replacement for the P3 Zhao-Cui analytical-route audit/repair.

## Next Subplan

Drafted:

`docs/plans/bayesfilter-highdim-zhao-cui-p82-phase2-regression-fd-harness-subplan-2026-06-22.md`
