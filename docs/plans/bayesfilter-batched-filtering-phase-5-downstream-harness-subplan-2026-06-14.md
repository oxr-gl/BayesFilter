# Phase 5 Subplan: Downstream HMC/NeuTra Harness

Date: 2026-06-14

## Status

`DRAFT_FOR_LOCAL_AND_CLAUDE_REVIEW`

## Phase Objective

Validate that the experimental batched value+score path can be called from a
downstream target/harness boundary with the value and score semantics required
by HMC, NeuTra, and surrogate-training workloads.

This phase is an integration and contract phase.  It is not a sampler
convergence, posterior quality, production default, or scientific validity
phase.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed with reviewed inventory and boundary audit.
- Phase 1 passed with deterministic correctness tests for experimental batched
  Kalman and affine SVD sigma-point value+score.
- Phase 2 passed with nonlinear SVD sigma-point branch coverage.
- Phase 3 passed with a non-default experimental value+score interface
  candidate.
- Phase 4 passed with JIT-only GPU benchmark artifacts and capacity/
  infeasibility records.
- No public export/default change is authorized.
- CUT4 remains outside default-promotion scope.
- Existing unrelated dirty worktree changes must be preserved.
- Any NeuTra-related execution or interpretation must first audit and inherit
  the project's applicable Gate 1/2/3 status; stale or missing NeuTra gate
  status is a Phase 5 blocker, not a reason to infer downstream readiness.

## Required Artifacts

New or refreshed artifacts:

- `tests/test_experimental_batched_downstream_value_score_harness.py`
- Optional diagnostic script only if tests need a standalone runner:
  `docs/benchmarks/check_experimental_batched_downstream_value_score_harness.py`
- Phase 5 result:
  `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-result-2026-06-14.md`
- Phase 6 subplan:
  `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-subplan-2026-06-14.md`
- Claude review artifact:
  `docs/plans/bayesfilter-batched-filtering-phase-5-claude-review-round-01-2026-06-14.md`
- Phase 5 result section naming the exact existing downstream boundary
  exercised, or explicitly recording `PARTIAL_BLOCKED_SYNTHETIC_ONLY` if no
  existing boundary can be exercised without forbidden edits.

If downstream integration requires touching production adapter/default code,
stop and write a blocker result instead of editing those files.

## Required Checks, Tests, And Reviews

### Pre-execution local checks

1. Verify this subplan contains all required headings.
2. Verify Phase 4 result exists and records JIT-only GPU evidence.
3. Search current downstream value+score and HMC/NeuTra boundaries:
   - `rg -n "ValueScorePosteriorAdapter|latent_value_and_score|run_full_chain_tfp_hmc|NeuTra|neutra|value_and_score|experimental_batched" bayesfilter scripts tests docs/plans`
4. Verify public export files are not planned for editing:
   - `bayesfilter/__init__.py`
   - `bayesfilter/linear/__init__.py`
   - `bayesfilter/nonlinear/__init__.py`
5. Verify current HMC/NeuTra gate status from existing result notes before
   choosing any downstream harness.  The gate-status audit must name a specific
   local artifact and check that it is current-code relevant, not merely a
   historical/oracle-only note.  Candidate sources include:
   - `docs/plans/nonlinear-ssm-jit-hmc-phase-4-full-chain-tfp-hmc-jit-result-2026-06-08.md`
   - `docs/plans/nonlinear-ssm-jit-hmc-phase-5-runner-device-performance-result-2026-06-08.md`
   - `docs/plans/nonlinear-ssm-jit-hmc-phase-6-engineering-canary-result-2026-06-08.md`
   - `scripts/run_model_suite_hmc_qualification.py`
   - `tests/test_common_inference_runtime_contracts.py`
   If no current-code-relevant gate status can be found, Phase 5 may run only
   a narrow generic value+score harness test and must record
   `PARTIAL_BLOCKED_MISSING_DOWNSTREAM_GATE_STATUS`, not pass to Phase 6 as
   downstream evidence.

### Implementation

1. Add a narrow test harness around a named existing downstream boundary.  The
   preferred first target is an existing value+score consumer that can be
   exercised without long chains or default edits, such as
   `static_unroll_chain_value_and_score` or another current local
   HMC/value-score helper identified by the precheck search.
2. The downstream-boundary test must treat the Phase 3 experimental interface
   as a value+score provider and check:
   - `value.shape == [B]`;
   - `score.shape == [B, p]`;
   - output tensors are finite;
   - row order is preserved;
   - scalar fallback remains explicit;
   - metadata records experimental/non-default status;
   - no public export/default change is made.
3. A purely generic/synthetic value+score harness may be added as explanatory
   coverage, but it cannot satisfy the Phase 5 pass criterion by itself.
4. If no safe existing downstream boundary can consume batched value+score
   without default edits, write a partial/blocker result instead of counting
   the synthetic harness as downstream evidence.
4. Do not run long HMC chains, adaptation ladders, or NeuTra training in this
   phase unless a separate reviewed sampler-validity plan is created.
5. Do not claim sampler speedup from microbenchmarks alone.

### Required local test commands

Run CPU-only downstream harness tests:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_downstream_value_score_harness.py tests/test_experimental_batched_value_score_interface.py tests/test_experimental_batched_benchmark_harness.py
```

Run existing experimental correctness guard:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py
```

Run public API guard:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_v1_public_api.py -k public_api
```

Audit-only scans:

```bash
rg -n "experimental_batched_value_score|experimental_batched_kalman|experimental_batched_svd" bayesfilter/__init__.py bayesfilter/linear/__init__.py bayesfilter/nonlinear/__init__.py
```

The scan must remain empty.

### Review

- Claude Opus max effort must review this subplan read-only before execution.
- Claude must receive paths and bounded questions, not whole-file prompt
  contents.
- If Claude requests a fixable revision, patch this same subplan visibly and
  rerun focused plan checks.
- Stop after five rounds for the same material blocker.
- Claude is not an execution authority and cannot authorize default changes,
  sampler validity claims, model-file boundaries, product-capability claims,
  funding boundaries, or scientific claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the experimental batched value+score interface be consumed at a named existing downstream target/harness boundary while preserving HMC-style value/score shapes and explicit experimental metadata? |
| Baseline/comparator | Phase 3 interface contract, existing value+score adapter conventions, scalar fallback callback semantics, and Phase 1-3 correctness artifacts. Phase 4 timing is context only, not a downstream correctness comparator. |
| Primary criterion | Required tests pass against a named existing downstream boundary; the boundary receives `[B]` values and `[B, p]` scores; finite outputs and row order are preserved; no export/default edit occurs; NeuTra/HMC gate status is audited before any downstream claim. |
| Promotion veto diagnostics | Shape mismatch, nonfinite output, row-order failure, implicit scalar fallback, missing experimental metadata, public export/default edit, stale/missing HMC/NeuTra gate status used as readiness evidence. |
| Continuation veto diagnostics | Existing downstream harness cannot be exercised without production default edits, long sampler/training runs, package installation, network access, or modifying unrelated dirty files. |
| Explanatory diagnostics | Harness complexity, adapter mismatch, downstream gate status found/missing, Phase 4 timing context, and test runtime. |
| Not concluded | No sampler convergence, no posterior quality, no HMC/NeuTra production readiness, no default policy, no broad speedup claim. |
| Artifact preserving result | Phase 5 result file, test file, optional diagnostic script, and Claude review artifact. |

## Forbidden Claims And Actions

- Do not change production defaults or public exports.
- Do not run or claim NeuTra training readiness without auditing current Gate
  1/2/3 status and writing a separate sampler-validity plan if needed.
- Do not run long HMC chains or adaptation ladders in this phase.
- Do not claim posterior validity, sampler convergence, or scientific
  correctness from this harness.
- Do not use eager GPU timing as evidence.
- Do not include CUT4 in default-promotion scope.
- Do not overwrite unrelated dirty worktree changes.
- Do not install packages, fetch network resources, commit, push, or run
  destructive filesystem/git commands.
- Do not let Claude edit files or authorize execution.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if:

- Claude review of this subplan converges with `VERDICT: AGREE`.
- Required local tests pass.
- A named existing downstream boundary was exercised without forbidden edits.
- Phase 5 result records exact commands, outcomes, gate-status audit, and
  remaining downstream limitations.
- No public export/default edit occurred.
- Any missing NeuTra/HMC gate status is recorded as a blocker for readiness
  claims, not silently ignored.
- Phase 6 subplan exists and includes objective, inherited entry conditions,
  artifacts, checks/tests/reviews, evidence contract, forbidden claims/actions,
  handoff conditions, and stop conditions.

## Stop Conditions

Stop and write a blocker result if:

- Downstream harness integration requires production default/export edits.
- Only a generic/synthetic harness can be exercised safely; in that case write
  `PARTIAL_BLOCKED_SYNTHETIC_ONLY` and do not advance to Phase 6 as downstream
  evidence.
- Existing HMC/NeuTra gate status is missing or stale and the only possible
  Phase 5 path would require claiming readiness from it.
- Required tests fail and cannot be repaired within Phase 5 scope.
- Batched value/score output shape or row-order semantics do not match the
  downstream contract.
- Continuing would require package installation, network access, credentials,
  destructive git/filesystem action, long sampler/training runs, production
  default changes, or modifying unrelated dirty worktree changes.
- Claude review does not converge after five rounds for the same material
  blocker.

## End-Of-Phase Procedure

1. Run the required local checks.
2. Write the Phase 5 result / close record with a decision table and run
   manifest.
3. Draft or refresh the Phase 6 default-readiness subplan.
4. Review the Phase 6 subplan for consistency, correctness, evidence coverage,
   default-policy safety, and scientific-claim safety.
5. Send material Phase 6 subplan questions to Claude as read-only review before
   execution.
