# Phase 3 Subplan: Production Interface Candidate

Date: 2026-06-14

## Status

`READY_FOR_LOCAL_CHECK_AND_REVIEW`

## Phase Objective

Design and implement a non-default production-facing interface candidate for
batched filtering value+score.  The interface must expose deliberate,
opt-in batch-over-parameters evaluation while preserving scalar fallback
semantics and avoiding any production default change or public export change
without human approval.

The candidate intentionally follows the repo's established
`ValueScorePosteriorAdapter`-style value+score contract at the shape level:
`value` is a rank-1 batch tensor and `score` is a rank-2 batch-by-parameter
tensor.  It is not a posterior adapter and does not claim sampler readiness.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed with reviewed boundaries and validated baseline artifacts.
- Phase 1 passed with small deterministic batched Kalman and affine SVD
  correctness tests.
- Phase 2 passed with tiny non-affine Model B batched SVD-UKF/cubature parity
  and fail-closed branch diagnostics.
- Existing experimental modules remain unexported:
  - `bayesfilter/linear/experimental_batched_kalman_tf.py`
  - `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py`
- Existing unrelated dirty worktree changes must be preserved.
- No production default change is authorized.
- No public package export change is authorized in this phase unless explicitly
  approved by the user before implementation.

## Required Artifacts

- New non-default interface candidate module, proposed path:
  `bayesfilter/experimental_batched_value_score.py`
- New tests:
  `tests/test_experimental_batched_value_score_interface.py`
- Phase 3 result:
  `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-result-2026-06-14.md`
- Phase 4 subplan draft:
  `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-subplan-2026-06-14.md`
- Claude review artifact:
  `docs/plans/bayesfilter-batched-filtering-phase-3-claude-review-round-01-2026-06-14.md`

## Required Checks, Tests, And Reviews

Pre-execution local checks:

1. Verify this subplan contains all required headings.
2. Verify no public export files are planned for editing:
   `bayesfilter/__init__.py`, `bayesfilter/linear/__init__.py`,
   `bayesfilter/nonlinear/__init__.py`.
3. Verify Phase 1-2 tests still pass:
   `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`.

Implementation:

1. Add a new non-default module `bayesfilter/experimental_batched_value_score.py`.
   This is an intentional experimental public import path but must not be
   re-exported from `bayesfilter.__init__`, `bayesfilter.linear`, or
   `bayesfilter.nonlinear`.
2. Define a small dataclass-based result/metadata contract that records:
   - backend name;
   - batch size;
   - whether the path is experimental;
   - scalar fallback status;
   - nonclaims including no production default readiness.
3. Provide thin opt-in wrappers around the existing experimental Kalman and
   SVD sigma-point value+score functions.  The wrappers may be convenience
   contracts only; they must not change the experimental kernels.
4. Provide scalar fallback utility semantics only when the caller supplies an
   explicit scalar callback; do not infer model-specific scalar fallback from
   opaque model objects.
5. Do not edit public exports or make the candidate default.
6. Add tests that verify:
   - metadata/nonclaims are present;
   - unsupported backend fails closed;
   - wrapper output exactly matches the underlying experimental Kalman kernel
     for one existing Phase 1 linear fixture;
   - wrapper output exactly matches the underlying experimental SVD nonlinear
     kernel for one existing Phase 2 Model B fixture;
   - wrapper outputs have `value.shape == [B]` and `score.shape == [B, p]`;
   - scalar fallback callback is called row-by-row and preserves order;
   - scalar fallback stacked value/score outputs equal the callback authority
     values and have expected shapes;
   - no public export is added;
   - existing experimental value+score tests still pass.

Required test commands:

1. `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_value_score_interface.py tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`
2. `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_v1_public_api.py -k "public_api"`

Audit-only command:

1. `rg -n "experimental_batched_value_score|production default|__all__|tf_batched|fallback|nonclaims" bayesfilter/experimental_batched_value_score.py tests/test_experimental_batched_value_score_interface.py`

Review:

- Claude Opus max effort must review this subplan read-only before execution.
- If Claude requests revision and the issue is fixable, patch this subplan
  visibly and rerun focused subplan checks.
- Stop after five review rounds for the same material blocker.
- Claude is not an execution authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we expose a non-default, opt-in interface candidate for batched value+score without changing public defaults or weakening scalar authority semantics? |
| Baseline/comparator | Existing experimental kernels, Phase 1-2 tests, public API tests, established value+score shape semantics, and explicit scalar fallback callback behavior. |
| Primary pass criterion | Required tests pass; interface candidate records experimental metadata/nonclaims; wrapper outputs match underlying kernels for representative linear and nonlinear fixtures; scalar fallback stacks callback values/scores correctly; unsupported paths fail closed; public exports/defaults remain unchanged. |
| Veto diagnostics | Public export/default edited without approval; wrapper output mismatch vs underlying kernels; scalar fallback silently inferred or stacks wrong values/shapes; unsupported backend accepted; metadata omits experimental/nonclaim status; existing Phase 1-2 tests regress. |
| Explanatory diagnostics | Wrapper complexity, test runtime, and source audit output. |
| Not concluded | No production readiness, no default policy, no GPU performance claim, no HMC/NeuTra integration claim. |
| Artifact preserving result | Phase 3 result file plus candidate module and tests. |

## Forbidden Claims And Actions

- Do not modify public exports or defaults without explicit user approval.
- Do not move experimental kernels into production modules.
- Do not claim the top-level experimental import path is a stable public API.
- Do not benchmark GPU or use eager GPU timing.
- Do not infer scalar fallback from opaque model objects.
- Do not add CUT4 to default-promotion scope.
- Do not overwrite unrelated dirty files.
- Do not use Claude to edit or approve execution.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- Claude review of this subplan converges with `VERDICT: AGREE`;
- the required Phase 3 tests pass;
- the Phase 3 result file records exact commands, outcomes, and remaining API
  limitations;
- Phase 4 subplan exists and includes objective, inherited entry conditions,
  artifacts, checks/reviews, evidence contract, forbidden claims/actions,
  handoff conditions, and stop conditions;
- Phase 4 subplan has been reviewed for benchmark fairness, GPU trusted
  execution, JIT-only GPU comparison, artifact coverage, and boundary safety.

## Stop Conditions

Stop and write a blocker result if:

- a useful interface candidate cannot be expressed without public export/default
  edits;
- wrapper metadata/result contract cannot be added without changing
  experimental kernel return values;
- the candidate would require inventing semantics incompatible with established
  value+score shape conventions;
- existing Phase 1-2 tests regress;
- public API tests show an accidental export/default change;
- scalar fallback semantics require unsafe inference;
- Claude review does not converge after five rounds for the same material
  blocker;
- continuing would require package installation, network access, GPU trusted
  execution, destructive git/filesystem action, production default changes, or
  modifying unrelated dirty worktree changes.

## End-Of-Phase Procedure

1. Run the required local checks.
2. Write the Phase 3 result / close record.
3. Draft or refresh the Phase 4 benchmark subplan.
4. Review the Phase 4 subplan for consistency, correctness, benchmark fairness,
   artifact coverage, and boundary safety.
5. Send material Phase 4 subplan questions to Claude as read-only review before
   execution.
