# P91 Phase 2 Implementation Artifact: Batched Value/Score API

Date: 2026-06-29

Status: `P91_PHASE2_IMPLEMENTATION_DESIGN_PENDING_REVIEW`

## Scope

This artifact specifies the Phase 2 code/test change before execution. It is
not a result record. It does not authorize FD, score identity, GPU/XLA, HMC,
benchmarks, package/release/CI, default policy, or production-readiness claims.

## Phase Objective

Add a narrow stable subpackage batched value/score API contract beside the
existing single-call highdim score API. The batched contract must:

- evaluate a fixed one-dimensional `theta` against a batch of deterministic
  scalar value functions;
- return per-item scalar values and per-item scores;
- preserve existing single API behavior;
- expose setup identity through diagnostics and branch manifests;
- fail closed when batched setup identity metadata is missing, ambiguous, or
  inconsistent with the selected identity mode;
- prove deterministic batched outputs match looped single API outputs in local
  tests.

## Entry Conditions Inherited From Previous Phase

- Phase 1 score contract: `VERDICT: AGREE`.
- Phase 1 result: `VERDICT: AGREE`.
- Phase 2 subplan: `VERDICT: AGREE`.
- This implementation artifact must receive Claude `VERDICT: AGREE` before
  code edits or pytest commands.

## Required Artifacts

- Code edit:
  `bayesfilter/highdim/score_api.py`
- Subpackage export edit:
  `bayesfilter/highdim/__init__.py`
- Focused test:
  `tests/highdim/test_p91_batched_score_api.py`
- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md`
- Refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-subplan-2026-06-29.md`

## Proposed Code Changes

### `bayesfilter/highdim/score_api.py`

Add:

- `HighDimBatchedScoreAPIResult`
- `evaluate_batched_highdim_score_api`

The result contract will require:

- `theta.shape.rank == 1`;
- `log_likelihoods.shape.rank == 1`;
- `score.shape == (batch_size, theta_dim)`;
- one `BranchIdentity` per batch item;
- finite theta/value/score tensors;
- diagnostics declare `api_scope == "bayesfilter.highdim"`;
- diagnostics declare `stable_subpackage_api is True`;
- diagnostics declare `stable_top_level_api is False`;
- diagnostics declare `hmc_readiness == "not_claimed"`;
- diagnostics declare `setup_identity_channel == "diagnostics_and_branch_manifest"`;
- diagnostics declare `batch_identity_mode` as either
  `shared_setup_identity` or `per_item_setup_identity`.

The batched evaluator will accept:

```text
target_id
evidence_class
route_label
parameterization
theta
value_fns
diagnostics=None
shared_setup_identity=None
per_item_setup_identities=None
```

The evaluator must reject:

- matrix or scalar `theta`;
- empty or non-callable `value_fns`;
- non-scalar value-function outputs;
- disconnected score outputs;
- simultaneous `shared_setup_identity` and `per_item_setup_identities`;
- missing setup identity metadata;
- empty setup identity mappings;
- per-item setup identity length mismatch.

For shared setup identity, each per-item branch manifest records the same setup
identity plus batch index and batch size. For per-item setup identity, each
manifest records the corresponding item identity. The diagnostics payload also
records the identity mode and per-item branch hashes.

Existing `evaluate_highdim_score_api` remains backward compatible. It may gain
an optional `setup_identity` keyword to allow the looped single comparator to
record the same setup metadata, but existing callers and tests must continue to
work without the keyword.

### `bayesfilter/highdim/__init__.py`

Export the new batched result and evaluator from `bayesfilter.highdim` only:

- `HighDimBatchedScoreAPIResult`
- `evaluate_batched_highdim_score_api`

Do not add root-level `bayesfilter` exports.

### `tests/highdim/test_p91_batched_score_api.py`

Add deterministic CPU-safe tests:

1. Subpackage-only export test:
   - new symbols exist in `bayesfilter.highdim.__all__`;
   - new symbols are absent from root `bayesfilter.__all__`.

2. Shared-identity parity test:
   - create a full P91-style setup identity fixture with target id, time index,
     dimensions, physical ordering, basis/rank/sample/seed, transport hash,
     coordinate-frame hash, callable ids, and tolerance version;
   - define two deterministic scalar value functions using the same `theta`
     but different fixed offsets;
   - compute looped single `evaluate_highdim_score_api` results using the same
     setup identity;
   - compute one batched `evaluate_batched_highdim_score_api` result with
     `shared_setup_identity`;
   - assert values and scores match the looped single results;
   - assert diagnostics expose setup identity channel, batch identity mode, and
     per-item branch hashes.

3. Per-item identity test:
   - provide two explicit per-item setup identities;
   - assert result diagnostics use `per_item_setup_identity`;
   - assert per-item branch hashes are distinct when identity metadata differs.

4. Fail-closed tests:
   - reject missing setup identity;
   - reject both shared and per-item setup identities together;
   - reject per-item identity length mismatch;
   - reject matrix `theta`;
   - reject non-scalar batch item value.

## Required Local Checks/Tests

After Claude agrees on this artifact and after code edits:

```bash
git diff --check -- bayesfilter/highdim/score_api.py bayesfilter/highdim/__init__.py tests/highdim/test_p91_batched_score_api.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p51_stable_score_api.py tests/highdim/test_p91_batched_score_api.py -q
```

CPU-only intent must be recorded in the Phase 2 result. These tests are local
semantic/API checks only and cannot be used as FD, score-identity, GPU/XLA,
HMC, benchmark, package, release, CI, default-policy, or production evidence.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the highdim subpackage expose a batched value/score API whose outputs match looped single calls and whose setup identity metadata fails closed? |
| Baseline/comparator | Existing `evaluate_highdim_score_api` looped over deterministic scalar value functions under the same theta and setup identity. |
| Primary criterion | Batched values and scores equal looped single values and scores within TensorFlow default `assert_near` tolerance, with stable shape/dtype, branch identities, and explicit setup identity metadata. |
| Veto diagnostics | Batch/single mismatch, missing setup identity channel, ambiguous/mixed identity without per-item metadata, root-level export, NaN/Inf, shape/dtype drift, disconnected scores, or any broader validation/readiness claim. |
| Explanatory diagnostics | Per-item branch hashes, identity mode, batch size, fixture setup identity. |
| Not concluded | FD consistency, score identity, GPU/XLA readiness, HMC readiness, CPU/GPU performance, packaging/release/CI readiness, default-policy readiness, production readiness, exact likelihood correctness, posterior correctness, or universal GPU superiority. |
| Artifact | Code/test diff, test output, Phase 2 result, refreshed Phase 3 subplan. |

## Skeptical Plan Audit

| Risk | Audit conclusion |
| --- | --- |
| Wrong baseline | Baseline is the existing reviewed single API, not a new batched implementation compared against itself. |
| Proxy metric promoted | No speed, JIT, FD, or validation metric is promoted; parity is only an API semantic gate. |
| Missing stop condition | Any parity, metadata, shape, dtype, export, or local test failure stops Phase 2 unless repaired within scope. |
| Unfair comparison | Batched and single calls use the same theta, value functions, route labels, diagnostics, and setup identity fixture. |
| Hidden assumption | The artifact names that this is a semantic wrapper and not the final GPU/XLA/HMC target. |
| Stale context | Inventory used current `score_api.py`, `highdim/__init__.py`, existing P51 score API tests, and fixed-branch manifest helpers. |
| Artifact mismatch | Required edits and tests are named exactly; Phase 2 result must record command output and CPU-only status. |

Audit status: `PASS_P91_PHASE2_IMPLEMENTATION_PLAN_AUDIT`

## Forbidden Claims/Actions

- Do not claim batched speed or GPU/XLA readiness.
- Do not run GPU/CUDA, XLA, HMC, FD, score identity, benchmarks, package,
  release, CI, production, or default-policy commands.
- Do not add root-level `bayesfilter` exports.
- Do not revive ALS.
- Do not hide setup identity in local variables only.

## Phase 2 Handoff After Execution

Phase 2 can close only if:

- required local checks/tests pass, or an explicit API blocker result is
  written;
- Phase 2 result is written and reviewed;
- refreshed Phase 3 FD subplan is written and reviewed.
