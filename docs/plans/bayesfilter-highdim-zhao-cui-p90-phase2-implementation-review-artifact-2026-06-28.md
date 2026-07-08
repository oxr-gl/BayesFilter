# P90 Phase 2 Implementation Review Artifact: Value Bridge Helper And Tests

Date: 2026-06-28

Status: `P90_PHASE2_IMPLEMENTATION_LOCAL_CHECKS_PASSED_PENDING_REVIEW`

## Scope

Phase 2 implemented a focused P90 value bridge surface and tests for the
reviewed contract:

- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p90_value_bridge_contract.py`
- `tests/highdim/test_p90_value_bridge_execution.py`

The worktree was already dirty. Unrelated pre-existing edits were preserved and
not reverted. The Phase 2 implementation is limited to the P90 bridge helper,
bindings, exports, and focused tests.

## Implemented Bridge Surfaces

- `SourceRouteValueBridgeBinding`
- `SourceRouteAuthorFormulaReplayResult`
- `source_route_author_formula_negative_log_physical_density`
- `source_route_coordinate_frame_hash`
- `source_route_callable_identity`
- P90 constants:
  - `P90_VALUE_BRIDGE_TARGET_ID`
  - `P90_VALUE_BRIDGE_COMPARATOR_LABEL`
  - `P90_VALUE_BRIDGE_TOLERANCE_VERSION`
  - `P90_VALUE_BRIDGE_PHYSICAL_ORDERING`

## Contract Controls

The bridge helper:

- computes the author formula separately from the production scalar;
- does not call `source_route_sequential_negative_log_physical_density`;
- does not call `source_route_previous_marginal_log_density`;
- binds target id, time index, physical shape/order, parameter/state dims,
  prior/previous branch, basis metadata, TT rank tuple, sample count, seed,
  transport branch hash, coordinate-frame hash, callable identities, comparator
  label, and tolerance version;
- rejects wrong target, ordering, retained hash, tolerance version, comparator
  label, transport branch hash, coordinate-frame hash, and callable identity;
- handles `t=1` via the prior log-density callable;
- handles `t>1` via an independent previous retained marginal replay:
  prefix physical points, previous affine prefix solve, marginal transport
  `eval_pdf`, and determinant correction.

## Focused Tests

Added:

```text
tests/highdim/test_p90_value_bridge_contract.py
```

The tests use the real Zhao-Cui parameterized SIR dimensions:

- `parameter_dim = 3`;
- `state_dim = 18`;
- physical ordering `[theta, x_t, x_{t-1}]`;
- a deterministic contract-double transport, not a fitted production TTSIRT.

Coverage:

- `t=1` prior / transition / likelihood component replay;
- `t=2` previous retained marginal replay;
- monkeypatch guard that fails if the bridge calls the production scalar or
  production previous-marginal helper;
- wrong physical ordering fail-closed;
- wrong previous retained hash fail-closed;
- changed tolerance version fail-closed;
- proxy comparator label fail-closed;
- wrong target id fail-closed;
- transport branch, coordinate-frame, and callable identity mismatches
  fail-closed.

The source-scalar-vs-replay comparison required by Phase 3 is not collected by
the Phase 2 test command. It is exposed as a helper plus a separate Phase
3-only test file:

```text
tests/highdim/test_p90_value_bridge_execution.py
```

## Local Checks

Commands run:

```bash
env CUDA_VISIBLE_DEVICES=-1 pytest tests/highdim/test_p90_value_bridge_contract.py --maxfail=1
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Results:

- First focused pytest run failed because the deterministic `t=2` previous
  affine frame was unit-scale while SIR physical states were hundreds-scale,
  making the Gaussian contract-double marginal underflow to zero.
- The fixture was repaired by resizing the previous affine frame scale so the
  deterministic marginal is finite.
- Rerun passed after separating the Phase 3 wrapper:
  `4 passed, 2 warnings`.
- Warnings were TensorFlow Probability deprecation warnings only.
- P90 docs diff hygiene passed.

## Skeptical Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided. The helper replays the reviewed author formula for the same source-route scalar; it does not use UKF, LEDH, rank/degree, holdout, FD, or validation-loss proxies. |
| Proxy metrics promoted | Avoided. Tests are implementation guards only and do not claim value correctness. |
| Missing stop conditions | Avoided. Identity, tolerance, target, branch, retained-object, and callable drift all fail closed. |
| Unfair comparison | Avoided at implementation level by binding same target/branch/setup metadata before Phase 3 execution. |
| Hidden assumptions | Exposed. The tests use deterministic contract-double transports; Phase 3 must compare against the production source-route scalar before any value-correctness nomination. |
| Stale context | P89 blockers remain open until Phase 3 executes the same-scalar value bridge. |
| Environment mismatch | Focused test was run CPU-only with `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA, HMC, FD, package, release, or production command was run. |
| Artifact usefulness | The implementation artifact directly answers Phase 2: bridge surfaces and fail-closed tests exist and pass. |

## Nonclaims

Phase 2 does not claim:

- value correctness;
- `D18_CORRECTNESS_CANDIDATE`;
- source-route correctness;
- analytical-gradient correctness;
- FD validation;
- HMC readiness;
- GPU/XLA readiness;
- runtime, memory, cost, or performance properties;
- production readiness;
- packaging, CI, release, or default-policy readiness.

Phase 3 must still execute the same-target value bridge comparison against
`source_route_sequential_negative_log_physical_density`.
