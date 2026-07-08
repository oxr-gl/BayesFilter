# P87 Phase 2 Subplan: Analytical Route Repair

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE2_REPAIR_OR_BLOCK_EXECUTION`

## Phase Objective

Repair or explicitly block the candidate SIR d18 filter score route so that
any future analytical-gradient claim is not backed by
JVP/`ForwardAccumulator`.

## Entry Conditions Inherited From Previous Phase

- Phase 1 produced derivative-component classification.
- `BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT` remains active.
- The exact JVP-backed backend is the filter-level
  `tensorflow_forward_accumulator_for_model_log_density` route, including
  `_scalar_target_log_derivative_by_forward_accumulator` and diagnostics in
  scalar/multistate fixed-design score paths.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase2-analytical-route-repair-result-2026-06-26.md`
- Focused implementation diff, if repair is attempted.
- Updated/added tests if repair is attempted; blocker-only outcome may instead
  preserve existing tests and document the active blocker.
- Updated Phase 3 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-subplan-2026-06-26.md`

## Allowed File Scope

Phase 2 may edit only these files unless a revised subplan is reviewed first:

- `bayesfilter/highdim/filtering.py`
- `bayesfilter/highdim/models.py`
- `tests/highdim/test_p81_analytical_sir_score.py`
- `tests/highdim/test_fixed_branch_derivatives.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase2-analytical-route-repair-result-2026-06-26.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-subplan-2026-06-26.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md`

Any broader file touch, route expansion, mathematical derivation change, or
default-policy change requires a refreshed reviewed subplan before execution.

## Required Checks/Tests/Reviews

Pre-repair inventory checks must include:

```bash
set -euo pipefail

rg -n "ForwardAccumulator|tensorflow_forward_accumulator_for_model_log_density" bayesfilter/highdim/filtering.py
```

Repair-attempt closeout checks must be fail-closed and include:

```bash
set -euo pipefail

python -m py_compile bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py tests/highdim/test_fixed_branch_derivatives.py
pytest -q tests/highdim/test_p81_analytical_sir_score.py
pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate or score"
if rg -n "ForwardAccumulator|tensorflow_forward_accumulator_for_model_log_density" bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py tests/highdim/test_fixed_branch_derivatives.py; then
  echo "BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT: JVP backend remains in Phase 2 repair scope" >&2
  exit 1
fi
git diff --check -- bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py tests/highdim/test_fixed_branch_derivatives.py docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Blocker-result closeout checks may retain the positive JVP inventory grep, but
the Phase 2 result must explicitly state that analytical-gradient promotion
remains blocked and Phase 3 is local-algebra-only.

Claude review:

- Required for implementation diff and Phase 2 result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the candidate filter score route be made JVP-free before any analytical-gradient promotion, or must analytical-gradient claims remain blocked? |
| Baseline/comparator | Phase 1 route audit result and local SIR analytical score/Jacobian methods. |
| Primary criterion | Candidate promotion route no longer uses JVP and passes repair-attempt closeout checks, or result records a blocker and downgraded claim class. |
| Veto diagnostics | Hidden or remaining JVP backend in repair-attempt scope, disconnected gradient, branch-hash drift, local score mismatch, broad unrelated refactor. |
| Explanatory diagnostics | FD rows, local `GradientTape` diagnostics, branch hashes. |
| Not concluded | Full d18 correctness, source-route correctness, HMC/production readiness. |
| Artifact | Phase 2 result and tests. |

## Forbidden Claims/Actions

- Do not use JVP as proof of analytical correctness.
- Do not describe the current route as promoted or analytical before repair.
- Do not broaden to LEDH, GPU, HMC, source-route validation, or training.
- Do not modify unrelated dirty files.

## Skeptical Pre-Execution Audit

Before any Phase 2 edit or test run, Codex must record in the execution ledger:

- Wrong baseline check: Phase 2 targets only the Phase 1-identified
  filter-level JVP backend, not local SIR algebra or source-route correctness.
- Proxy-promotion check: FD rows, local `GradientTape` diagnostics, and branch
  hashes may explain or veto, but cannot prove full filter correctness.
- Scope check: planned edits must stay inside the allowed file scope above.
- Environment check: Phase 2 must not run GPU, HMC, LEDH, source-route
  validation, training, or long benchmarks.
- Handoff check: Phase 3 path must be refreshed as either promotion-track
  local algebra certification or local-algebra-only after blocker confirmation.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if:

- Phase 2 passes with `PRIMARY_ROUTE_ANALYTICAL`, or
- Phase 2 blocks and Phase 3 is reframed as local algebra only, not filter
  analytical-gradient promotion.

The exact refreshed handoff artifact is
`docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-subplan-2026-06-26.md`.
The Phase 2 result must state whether that Phase 3 subplan is
promotion-track or local-algebra-only.

## Stop Conditions

- Repair requires unreviewed mathematical derivation.
- JVP cannot be removed without a larger design decision.
- Tests reveal a local analytical formula mismatch.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 2 result/close or blocker record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
