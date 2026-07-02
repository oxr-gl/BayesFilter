# Manual Adjoint Phase 3 Subplan: Dense Custom-Gradient Prototype

status: DRAFT_READY_AFTER_M2_REVIEW
date: 2026-06-22
phase: M3-DENSE-CUSTOM-GRADIENT

## Phase Objective

Build an opt-in private dense custom-gradient prototype for the stabilized
finite Sinkhorn/transport primitive, using only the primitive adjoints verified
in M2.

This phase proves nothing about streaming memory or SIR d18.  It only asks
whether the dense opt-in prototype can reproduce the tiny dense scalar
gradients checked in M2 while preserving finite values and shape contracts.

## Entry Conditions

- M2 primitive parity result is complete with no unresolved blocker and has
  passed the read-only review gate.
- M2 identified the exact private helper/module/test harness to edit:
  `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py` for primitive parity,
  and a private implementation helper to be selected before production edits.
- M1/M2 still forbid governed N10000 raw full AD as the target route.

## Required Artifacts

- Private dense custom-gradient implementation diff.
- Focused tests for the private dense route.
- Phase 3 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase3-dense-custom-gradient-result-2026-06-22.md`
- Refreshed M4 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase4-loop-adjoint-integration-design-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

- Run the M2 primitive tests against both direct primitive helpers and the
  dense custom-gradient wrapper.
- Add shape/finite-value tests for batched tiny dense cases.
- `python -m py_compile` for edited Python files.
- `git diff --check` for touched code/tests/docs.
- Claude read-only review of the implementation boundary and tests, because
  this is the first code-producing phase.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can an opt-in private dense custom-gradient wrapper reproduce the verified primitive gradients on tiny dense cases? |
| Baseline/comparator | M2 primitive parity tests and TensorFlow autodiff on tiny dense cases where raw AD is cheap. |
| Primary criterion | Tests pass for objective value equality, gradient parity, finite values, batched shapes, and unsupported-mode rejection. |
| Veto diagnostics | Public/default exposure; parity regression; nonfinite gradients; memory growth inconsistent with dense tiny route; unsupported transport modes accepted; missing tests. |
| Explanatory diagnostics | Runtime, dtype, batch/particle dimensions, gradient max errors, and unsupported-mode error messages. |
| Not concluded | No streaming/chunked memory claim, no filter-loop integration, no SIR d18 readiness, no P82 validation, no HMC/default readiness. |

## Forbidden Claims / Actions

- Do not wire the prototype into production/default code paths.
- Do not claim memory improvement.
- Do not run N10000 GPU tests.
- Do not change external API semantics.
- Do not accept `full`, `diff-keys`, `diff-scale`, or `diff-potentials` unless
  M1/M2 explicitly derived and tested them.

## Next-Phase Handoff Conditions

M4 may proceed only if M3 records:

- private dense route path and function names;
- supported mode(s);
- tests and tolerances;
- known unsupported modes;
- exact retained/replay information needed for filter-loop integration design.

## Stop Conditions

Stop if private custom-gradient parity fails, if public integration is needed
to test the primitive, if unsupported modes cannot be blocked cleanly, or if
the dense prototype is too fragile to serve as an integration target.
