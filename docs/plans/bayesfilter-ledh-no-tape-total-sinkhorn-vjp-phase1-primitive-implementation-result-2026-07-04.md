# Phase 1 Result: Primitive No-Tape VJP Implementation

Date: 2026-07-04

Status: `CLOSED_REVIEWED`

## Phase Objective

Implement a candidate no-`GradientTape`, no-`ForwardAccumulator` manual total
VJP for the finite streaming Sinkhorn transport primitive.

## Entry Conditions

- Phase 0 froze the scalar target as the finite streaming transport value
  computed by `_filterflow_manual_streaming_finite_transport_value_total_vjp`.
- Differentiated inputs for this primitive are `scaled_x`, `particles`,
  `logw`, and `epsilon0`.
- `eps` and `scaling` remain constants for this primitive target.  If a later
  model row makes either one parameter-dependent, that row is not admitted as a
  score until those derivatives are added or the row explicitly freezes them.

## Implementation Artifacts

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - `_filterflow_streaming_softmin_vjp` now has an optional no-tape epsilon
    cotangent return.
  - `_match_epsilon_cotangent_shape` maps per-batch temperature cotangents back
    to scalar, vector, or higher-rank epsilon input shape.
  - `_filterflow_streaming_finite_sinkhorn_potentials_vjp_total` is a new
    no-tape reverse recursion for the unstopped finite streaming Sinkhorn
    potential map.
  - `_filterflow_manual_streaming_finite_transport_total_vjp` no longer opens a
    local tape in its custom-gradient body; it calls the transport VJP and the
    new total potential VJP.
- `tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py`
  - static no-tape source checks;
  - explicit `epsilon0` cotangent path check;
  - tiny finite cotangent smoke for the potential VJP;
  - tiny finite cotangent smoke for the full custom-gradient transport helper.
- `tests/test_audit_ledh_clean_xla.py`
  - updated the stale expectation that the total-helper tape warning must
    still be present.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the repository contain a candidate no-tape total transport VJP implementation? |
| Baseline/comparator | Phase 0 target brief and the previous tape-backed total helper. |
| Primary criterion | Candidate implementation compiles, has no tape/forward-accumulator in the production helper, returns finite primitive cotangents on tiny tensors, and includes an explicit total cotangent path for `epsilon0`. |
| Veto diagnostics | Tape remains in production helper; stopped-key VJP reused as total VJP; missing `epsilon0` cotangent path; finite smoke fails; helper changes forward scalar; broad unrelated edits. |
| Explanatory diagnostics | Static source checks, tensor shapes, tiny cotangent finiteness, static clean-XLA warning status. |
| Not concluded | No tape/FD parity, no downstream P8p or LGSSM score admission, no GPU scalability, no HMC readiness. |

## Checks Run

CPU-only checks intentionally set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow
import.

| Command | Result |
| --- | --- |
| `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py tests/test_audit_ledh_clean_xla.py` | pass |
| AST/source check for `_filterflow_manual_streaming_finite_transport_total_vjp` and `_filterflow_streaming_finite_sinkhorn_potentials_vjp_total` forbidding `GradientTape`, `ForwardAccumulator`, `.gradient(` | pass |
| `git diff --check` | pass |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py tests/test_audit_ledh_clean_xla.py::test_default_clean_xla_audit_reports_current_route_unclean_with_line_anchors tests/test_audit_ledh_clean_xla.py::test_phase5_sinkhorn_target_helpers_have_no_python_step_loop_or_state_list` | pass: 6 passed |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "streaming_softmin_vjp or streaming_transport_from_potentials_vjp"` | pass: 5 passed |
| `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py` | expected `FAIL_CURRENT_ROUTE` remains only for stopped-key current vetoes; total-helper tape warning absent |

## Decision Table

| Decision | Primary Criterion Status | Veto Status | Main Uncertainty | Next Justified Action | Not Concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 1 locally and request read-only review | pass | no Phase 1 veto found | The no-tape implementation has not yet been checked against tape or finite differences | Phase 2 primitive parity and same-scalar FD validation | Score correctness, leaderboard readiness, GPU/XLA readiness, HMC readiness |

## Skeptical Audit

- Wrong baseline risk: Phase 1 is not using stopped-key helpers as a correctness
  baseline.  It only checks that a candidate no-tape total path exists.
- Proxy metric risk: finite tiny cotangents are not treated as correctness.
  They are only an implementation smoke.
- Hidden assumption: `eps` and `scaling` are constant for this primitive target.
  The result states that explicitly.
- Artifact-answer fit: the checks answer Phase 1's implementation-existence
  question, not Phase 2's correctness question.

## Nonclaims

- This does not prove the derivative is numerically correct.
- This does not prove P8p SIR or LGSSM score admission.
- This does not make stopped-key partial derivatives valid scores.
- This does not certify XLA/GPU behavior.

## Phase 2 Handoff

The read-only review gate accepted this close record and the refreshed Phase 2
validation subplan:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- Summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-024329-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-phase2/status.json`

Phase 2 may start.  It must compare the candidate no-tape total VJP against the
same finite scalar using tape and finite differences on tiny tensors.
