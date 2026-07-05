# Phase 2 Result: Primitive Parity And FD Validation

Date: 2026-07-04

Status: `CLOSED_REVIEWED`

## Phase Objective

Validate the candidate no-tape total VJP against the same finite streaming
transport scalar using raw TensorFlow tape and central finite differences on a
tiny float64 primitive fixture.

## Entry Conditions

- Phase 1 implemented and reviewed a no-tape candidate for the finite
  streaming transport total VJP.
- The Phase 1 review gate returned `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.
- `eps` and `scaling` remain constants for this primitive target.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the no-tape primitive compute the same total VJP as the finite transport scalar? |
| Baseline/comparator | Raw TensorFlow tape on `_filterflow_manual_streaming_finite_transport_value_total_vjp` and same-scalar central finite differences. |
| Primary criterion | Candidate VJP matches tape and FD within predeclared tiny-tensor tolerances for `scaled_x`, `particles`, `logw`, and `epsilon0`. |
| Veto diagnostics | Candidate matches stopped route but not total route; FD mismatch beyond tolerance; nonfinite cotangent; tape found in production helper; wrong scalar; tolerance changed after seeing failures. |
| Explanatory diagnostics | Per-input max absolute tape errors, directional FD errors, stopped-route gaps. |
| Not concluded | No P8p SIR regression admission, no LGSSM score admission, no GPU/XLA scalability, no HMC readiness. |

## Fixed Tolerances

These were set before running Phase 2 validation:

- tape parity absolute tolerance: `1.0e-8`;
- central FD directional absolute tolerance: `5.0e-5`;
- stopped-route negative-check minimum gap: `1.0e-6`;
- central FD step: `1.0e-5`.

## Checks Run

CPU-only checks intentionally set `CUDA_VISIBLE_DEVICES=-1`.

| Command | Result |
| --- | --- |
| `python -m py_compile tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py` | pass |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py` | pass: 2 passed |
| `PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py > docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json` | pass |
| `python -m json.tool docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json` | pass |
| `git diff --check -- tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json` | pass |

The first direct artifact attempt without `PYTHONPATH` failed with
`ModuleNotFoundError: No module named 'experiments'` because executing a test
file directly sets `sys.path[0]` to `tests/`.  The rerun with explicit
`PYTHONPATH=/home/chakwong/BayesFilter` succeeded.  That was an execution
wrapper issue, not a derivative validation failure.

## Numerical Result

Artifact:
`docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json`

Key values:

- same-scalar value gap: `0.0`;
- maximum tape parity error: `5.204170427930421e-18`;
- maximum FD directional error: `2.5253430770906966e-13`;
- maximum stopped-route gap versus total tape: `0.002199091916697652`;
- total `epsilon0` tape gradient: `4.113532015233492e-05`;
- no-tape custom `epsilon0` gradient: `4.113532015233463e-05`;
- stopped-route `epsilon0` gradient: `0.0`.

The stopped route fails the unstopped total derivative target.  In plain terms:
for this scalar, the stopped route omits a real derivative contribution.

## Decision Table

| Decision | Primary Criterion Status | Veto Status | Main Uncertainty | Next Justified Action | Not Concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 2 locally and request read-only review | pass | no Phase 2 veto found | The validation is tiny-primitive evidence, not downstream P8p/LGSSM score evidence | Phase 3 P8p SIR regression integration | Leaderboard score readiness, GPU/XLA scalability, HMC readiness |

## Skeptical Audit

- Wrong baseline risk: the comparator is the same finite scalar evaluated by
  raw TensorFlow tape, not the stopped partial derivative.
- Proxy metric risk: Phase 2 does not claim downstream score correctness from
  primitive parity.
- Missing stop condition risk: if the stopped route had also passed, Phase 2
  would have blocked as insensitive.  It did not pass.
- Environment risk: the run was CPU-only by design; no GPU/XLA claim is made.

## Nonclaims

- This does not prove the P8p SIR score route is repaired.
- This does not prove LGSSM score admission.
- This does not prove leaderboard readiness.
- This does not certify GPU/XLA compile or runtime behavior.

## Phase 3 Handoff

The read-only review gate accepted this result and the refreshed Phase 3
subplan:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- Summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-025648-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-phase3/status.json`

Phase 3 may start.  It must verify that the scoped P8p SIR same-scalar
total-derivative diagnostics pass while using the no-tape primitive route.
