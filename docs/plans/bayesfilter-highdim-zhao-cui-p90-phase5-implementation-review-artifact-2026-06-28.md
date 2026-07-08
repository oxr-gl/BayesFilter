# P90 Phase 5 Implementation Review Artifact: Deterministic Derivative Carry

Date: 2026-06-28

Status: `P90_PHASE5_IMPLEMENTATION_LOCAL_CHECKS_PASSED_PENDING_REVIEW`

## Scope

Phase 5 implemented the reviewed deterministic derivative-carry surface for
the P90 same-scalar value bridge. It does not implement fixed TTSIRT
proposal/transport derivatives and does not claim source-route
analytical-gradient readiness.

Touched Phase 5 files:

- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p90_derivative_carry_contract.py`

The worktree was already dirty. Unrelated pre-existing edits were preserved and
not reverted.

## Implemented Surfaces

- `SourceRouteDerivativeBinding`
- `SourceRouteComponentDerivativeCarry`
- `SourceRoutePreviousMarginalDerivativeCarry`
- `source_route_negative_log_assembly_derivative_carry`

These surfaces bind to the existing `SourceRouteValueBridgeBinding` and require
the exact Phase 3 value-bridge binding hash.

## Contract Controls

The implementation:

- preserves the P90 value-bridge target id and binding hash;
- requires derivative parameter indices to be explicit and in range;
- keeps fixed TTSIRT transport derivative status as `BLOCK_*`;
- stores component values and parameter scores with shape/finite checks;
- requires previous-marginal retained hash, keep axes, and input axes to match
  the value-bridge binding;
- keeps previous-marginal derivative owner status as `BLOCK_*`;
- assembles the negative-log derivative as the negative sum of component
  log-density scores;
- rejects derivative-binding drift before tensor arithmetic.

## Focused Tests

Added:

```text
tests/highdim/test_p90_derivative_carry_contract.py
```

Coverage:

- derivative binding preserves value-bridge hash and fixed TTSIRT blocker;
- transition and likelihood score carry match TensorFlow tape on the
  deterministic SIR d18 fixture;
- negative-log assembly carries correct signs and value;
- previous-marginal carry keeps retained-hash identity and blocker status;
- component shape drift and derivative-binding drift fail closed.

## Local Checks

Commands:

```bash
env CUDA_VISIBLE_DEVICES=-1 pytest tests/highdim/test_p90_derivative_carry_contract.py --maxfail=1
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Outcomes:

- First pytest attempt found a fail-closed bug: assembly checked only the
  value-bridge hash, so a derivative binding with different parameter-index
  shape reached TensorFlow shape arithmetic.
- Patched assembly to require the exact same `SourceRouteDerivativeBinding`
  across components before computing the score.
- Final pytest outcome: `5 passed, 2 warnings`.
- Warnings were TensorFlow Probability deprecation warnings.
- P90 docs diff hygiene passed.

## Skeptical Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided. Implementation binds to the Phase 3 value-bridge binding hash and deterministic derivative manifest. |
| Proxy metrics promoted | Avoided. Tests are implementation checks, not FD validation or HMC evidence. |
| Missing stop conditions | Avoided. Fixed TTSIRT proposal/transport and previous-marginal derivative readiness remain explicit blockers. |
| Unfair comparison | Avoided. Drift-veto checks preserve same target, branch, retained object, and derivative parameter indices. |
| Hidden assumptions | Exposed. Transition/likelihood scores use local parameterized SIR analytical score surfaces; fixed TTSIRT transport derivatives remain unimplemented. |
| Environment mismatch | Tests ran CPU-only with `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA, FD, HMC, production, package, CI, release, or default-policy command was run. |
| Artifact usefulness | The artifact answers Phase 5 implementation scope and hands off to either limited FD or blocker closeout in Phase 6. |

## Nonclaims

Phase 5 does not claim:

- full source-route analytical-gradient readiness;
- fixed TTSIRT proposal/transport derivative readiness;
- FD validation;
- HMC readiness;
- GPU/XLA readiness;
- runtime/performance/memory/cost result;
- production readiness;
- packaging, CI, release, or default-policy readiness.
