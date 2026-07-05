# Manual Adjoint Phase 6 Result: Streaming/Chunked Memory Route

Date: 2026-06-22

Status: PASSED_AFTER_CLAUDE_R3_ONE_PATH_AGREE

## Evidence Contract

| Field | Result |
|---|---|
| Question | Does a streaming/chunked manual-adjoint route preserve small-case parity while materially reducing dense transport-matrix exposure enough to justify P82 handoff preparation? |
| Baseline/comparator | M5 opt-in dense finite route on the same tiny fixed finite programs; dense-vs-streaming transported-particle and gradient parity; returned transport-matrix shape/size evidence. |
| Primary criterion | Passed after local tiny CPU/float64 checks and Claude R3 one-path review: streaming values and gradients match the dense opt-in route within tolerance, unsupported combinations reject, and the streaming route returns an empty `(B,0,0)` transport matrix. |
| Veto diagnostics | No parity failure; no nonfinite tiny value/score smoke; no unsupported dense/warmstart/full/vector-epsilon route accepted; no raw full-AD N10000 or P82 run launched. |
| Explanatory diagnostics | Per-fixture value/gradient maxima, returned transport-matrix size, local commands, and implementation anchors below. |
| Not concluded | No N10000 feasibility, no P82 FD agreement, no GPU/TF32 evidence, no HMC/default/posterior readiness, no exact likelihood claim, and no production readiness. |

## Implementation

M6 adds a second explicit opt-in route:

```text
manual_streaming_finite_sinkhorn_stopped_scale_keys
```

Implementation anchors:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  defines `_filterflow_manual_streaming_finite_transport_stopped_scale_keys`,
  which computes transported particles through the streaming finite
  stopped-scale/key route and recomputes the streaming value under
  `GradientTape` in the custom-gradient backward pass.
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  accepts the route only when `transport_plan_mode="streaming"`,
  `transport_ad_mode="stabilized"`, no warmstart is supplied, scalar epsilon is
  used, and static positive finite Sinkhorn steps are available.
- The streaming branch returns transported particles and row residuals, then
  records `transport_matrix = tf.zeros([batch_size, 0, 0], dtype=DTYPE)`.

This route avoids returning or blending a dense `[B,N,N]` transport matrix from
the experimental batched core.  The backward pass is still a recompute-on-
backward TensorFlow route through the streaming helper; M6 evidence therefore
supports only the tested tiny memory-shape/parity claim, not a general large-N
memory bound.

## Tests Added

Focused tests in:

- `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`

cover:

- dense-vs-streaming transported-particle parity on tiny fixtures;
- dense-vs-streaming gradients with respect to particles and log weights;
- returned streaming `transport_matrix.shape == (B,0,0)`;
- returned streaming `tf.size(transport_matrix) == 0`;
- rejection of dense plan mode, warmstart, `transport_ad_mode="full"`, and
  vector epsilon for the manual streaming route.

Tiny value/score smoke in:

- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`

covers finite log likelihood and finite score for the opt-in streaming route,
plus eager/graph parity on the tiny fixed-branch LEDH mechanics fixture.

## Local Checks

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md
PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_m6_manual_streaming_value_and_score_tiny_opt_in_smoke tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_m5_manual_dense_value_and_score_tiny_opt_in_smoke tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_phase4_value_and_score_source_has_no_numpy_rng_or_runtime_ess_branch tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_phase3_value_core_source_has_no_numpy_rng_or_runtime_ess_branch -q
```

Observed results:

- `py_compile`: passed;
- `git diff --check`: passed;
- diagnostics script: passed and printed JSON diagnostics;
- focused pytest bundle: `23 passed in 46.28s`.

These are deliberate CPU-only checks with `CUDA_VISIBLE_DEVICES=-1`.  They are
not GPU/TF32 evidence.

## Diagnostics

M6 tolerance contract:

- transported particle value max absolute error: `1e-10`;
- particle/log-weight gradient max absolute error: `1e-8`;
- streaming returned transport matrix size: exactly `0`;
- tiny value/score graph/eager parity: `1e-10`;
- finite value/score/gradient: required.

M6 dense-vs-streaming per-fixture diagnostics:

| Fixture | Particle value error | Particle/log-weight gradient error | Returned transport-matrix size |
|---|---:|---:|---:|
| `B=1,N=3,D=1` | 5.551115123125783e-17 | 2.0816681711721685e-17 | 0.0 |
| `B=1,N=4,D=2` | 1.1102230246251565e-16 | 3.8163916471489756e-17 | 0.0 |
| `B=2,N=3,D=2` | 1.1102230246251565e-16 | 4.163336342344337e-17 | 0.0 |

Overall M6 maxima:

- particle value error: `1.1102230246251565e-16`;
- particle/log-weight gradient error: `4.163336342344337e-17`;
- returned transport-matrix size: `0.0`.

## Memory/Runtime Interpretation

The M6 route has materially different returned-state behavior from M5:

- M5 returns and blends a dense `[B,N,N]` transport matrix.
- M6 returns `transport_matrix.shape == (B,0,0)` from the experimental batched
  core for streaming mode.

This is sufficient to prepare an M7 P82 handoff plan that asks for a bounded
N10000 actual-gradient gate using the streaming route.  It is not sufficient to
claim N10000 feasibility yet because M6 did not run a large-N memory ladder, a
trusted GPU memory measurement, or the full P82 SIR d18 validation.

## Source-Faithfulness Boundary

The repo-root `memory.md` Zhao-Cui source-faithfulness rule was checked during
bounded local review.  M6 is a BayesFilter manual-adjoint engineering gate for
the LEDH-PFPF-OT transport-gradient route.  It does not claim Zhao-Cui
source-faithfulness, does not cite Zhao-Cui paper/source anchors, and does not
close any Zhao-Cui source-route gap.

Any later P82/P83 artifact that claims a Zhao-Cui source-faithful route must
re-enter the `memory.md` rule with paper/math anchors and local author source
file/line anchors.  M6 cannot be used as a substitute for that source-anchor
review.

## Review Attempts

Claude read-only review required three attempts:

- first as a compact fact-packet review; rejected by external-disclosure
  approval policy;
- second as a bounded path/range-only review after reading `memory.md`, with no
  pasted code chunks; also rejected because it would still allow an external
  model service to inspect private workspace paths;
- third as a one-path bounded review of this result file only, with no code
  chunks and no artifact packet.  Claude returned `VERDICT: AGREE`.

Claude R3 found no new technical parity or memory-shape blocker in this result
file.  Claude noted that the only blocker visible in the prior text was the
unresolved review gate itself.  This R3 one-path review resolves that procedural
gate for M6.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Accept M6 local streaming route evidence | Local checks passed; Claude R3 one-path review agreed | No local or R3 review veto observed | Whether recompute-on-backward streaming remains feasible at N10000/P82 scale | Advance to M7 handoff preparation only; do not run P82 from M6 | No P82 FD agreement, N10000 feasibility, GPU/TF32 evidence, HMC/default/posterior readiness, or production readiness |

## Handoff

M7 may proceed.  M7 must prepare a return-to-P82 validation handoff with exact
commands and stop conditions.  M7 must not run P82 validation unless a refreshed
P82 subplan explicitly authorizes that downstream phase.
