# Phase 2 Subplan: BayesFilter Central Policy Implementation

Date: 2026-07-07

Status: `DRAFT_PHASE_SUBPLAN`

## Phase Objective

Implement the Phase 1 central BayesFilter HMC budget/timing policy and route
active BayesFilter tuning through it without changing the fixed-trajectory HMC
algorithm.

## Entry Conditions

- Phase 1 result is `PASSED_DESIGN_READY_FOR_IMPLEMENTATION`.
- No active NUTS path is authorized.
- MacroFinance remains integration-only.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p02-implementation-result-2026-07-07.md`
- Code diff in:
  `bayesfilter/inference/hmc_kernel_tuning.py`
- Export diff in:
  `bayesfilter/inference/__init__.py`
- Focused tests under existing HMC tuning test files or a new focused test.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does BayesFilter expose and use one central geometry-scaled budget/timing policy? |
| Baseline/comparator | Phase 0 current split policies and Phase 1 design. |
| Primary pass criterion | Focused tests prove budgets scale with dimension/condition/regularization, diagnostic counts are non-promoting, public policy payload is redacted, and active policy payloads carry numeric provenance. |
| Veto diagnostics | NUTS introduced; MacroFinance tuning logic added; public payload leaks private mechanics; active defaults still use unexplained stage timeout/sample constants; existing focused tests fail. |
| Explanatory diagnostics | Exact numeric budget values for toy dimensions/geometries, policy payloads, and remaining compatibility constants. |
| Not concluded | No tuned CCMA result, posterior convergence, sampler superiority, GPU readiness, or production readiness. |

## Implementation Scope

Allowed:

- add dataclasses/helpers in `hmc_kernel_tuning.py`;
- thread policy through existing budget factories;
- update tests for payload and scaling behavior;
- export the new policy class.

Forbidden:

- rewrite HMC transition logic;
- add NUTS or dynamic trajectory sampler;
- move tuning mechanics into MacroFinance;
- remove privacy/redaction guards;
- run long HMC.

## Required Checks

Run focused BayesFilter tests after implementation:

```bash
pytest tests/test_hmc_kernel_tuning_public_api.py tests/test_hmc_kernel_tuning_outer_loop.py tests/test_hmc_kernel_tuning_bootstrap.py tests/test_hmc_budget_ladder.py -q
```

If that is too slow or fails outside the changed scope, run a narrower focused
selection and record the limitation.

## Skeptical Plan Audit

- Wrong baseline: compare against Phase 0 active files only.
- Proxy metric risk: tests must not claim posterior validity.
- Missing stop conditions: no-progress and emergency-cap roles must appear in
  policy payload.
- Hidden assumption: condition number alone is insufficient; tests must cover
  regularization pressure too.
- Environment mismatch: BayesFilter writes have succeeded in this session; if
  they fail, stop for approval.

## Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- BayesFilter tests for the new policy pass;
- no active NUTS use appears;
- public payload redaction tests pass;
- Phase 2 result names any MacroFinance integration edits still required.

## Stop Conditions

Stop if implementation requires changing sampler semantics, if policy cannot be
threaded without breaking public redaction, if tests reveal existing unrelated
dirty work that would be overwritten, or if focused tests cannot be run and no
smaller check can verify the policy.
