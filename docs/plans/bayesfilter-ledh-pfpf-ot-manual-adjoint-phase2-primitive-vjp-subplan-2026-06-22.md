# Manual Adjoint Phase 2 Subplan: Primitive Dense VJP Parity

status: DRAFT_BLOCKED_UNTIL_M1_COMPLETE
date: 2026-06-22
phase: M2-PRIMITIVE-VJP

## Phase Objective

Implement private, dense, tiny-problem primitive checks for the
LEDH-PFPF-OT manual-adjoint route.  The goal is to verify the local VJP/JVP
building blocks before any filter-loop or public integration work.

## Entry Conditions

- M1 derivation contract is complete and reviewed when material.
- The finite scalar, tensor shapes, stopped/frozen quantities, and unsupported
  modes are explicitly listed in:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-derivation-contract-2026-06-22.md`.
- M1 result authorizes only primitive dense tests, not public integration.

## Required Artifacts

- Test file or private diagnostic file, to be selected by M2 before editing.
- Primitive parity JSON or markdown result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-result-2026-06-22.md`
- Updated M3 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase3-dense-custom-gradient-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

- Unit tests for:
  - barycentric projection VJP;
  - dense log-domain softmin VJP;
  - dense transport-from-potentials VJP;
  - finite Sinkhorn loop VJP/JVP on tiny dense cases;
  - scalar directional finite-difference spot checks.
- `python -m py_compile` for any edited Python files.
- `git diff --check` on touched files.
- Claude read-only review if primitive parity tolerances, scalar definition, or
  stopped/frozen policy changed from M1.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Do the primitive dense manual-adjoint pieces match tiny TensorFlow autodiff and finite-difference references within predeclared tolerances? |
| Baseline/comparator | TensorFlow autodiff on tiny dense finite Sinkhorn computations, plus scalar finite-difference spot checks. |
| Primary criterion | All primitive tests pass with finite values, shape checks, and recorded absolute/relative error tolerances. |
| Veto diagnostics | Nonfinite adjoints; shape mismatch; parity failure; hidden use of full N10000 AD; tests that compare a different scalar than M1; unsupported mode accidentally treated as supported. |
| Explanatory diagnostics | Error tables, tested seeds, dtype, finite-difference step ladder, and per-primitive max errors. |
| Not concluded | No filter-loop correctness, streaming memory improvement, SIR d18 readiness, P82 validation, HMC/default/posterior readiness. |

## M1-Derived Test Contract

Use the route named:

```text
manual_dense_finite_sinkhorn_stopped_scale_keys
```

Required primitive fixtures:

- `B=1, N=3, D=1`;
- `B=1, N=4, D=2`;
- `B=2, N=3, D=2`.

Required `float64` tolerances unless M2 explicitly changes them before running:

- value equality: `1e-10` absolute;
- VJP max absolute error: `1e-8`;
- JVP/VJP directional agreement: `1e-8`;
- finite-difference residual: explanatory step-ladder diagnostic only.

M2 must keep `eps`, `scaling`, `threshold`, and `max_iterations` constant for
primitive gradient checks.  Streaming, warmstarts, gradients through `eps`, and
governed N10000 validation remain unsupported.

The oracle comparator is tiny dense full-graph TensorFlow autodiff/JVP/VJP of
the same fixed finite program.  This is allowed only at tiny fixture scale and
must not be described as evidence that raw full AD works for governed N10000.

M2 is CPU/float64 oracle-style validation unless this subplan is patched before
execution.  It provides no GPU/TF32 performance, stability, memory, or
production-readiness evidence.

## Advancement Rule

M2 may advance to M3 only if:

- every named primitive passes on every required fixture within tolerance;
- finite Sinkhorn loop VJP/JVP passes against the tiny autodiff/JVP/VJP oracle;
- unsupported-route rejection passes;
- values and adjoints are finite;
- the result artifact records dtype, fixtures, tolerances, oracle comparator,
  and observed max errors.

Any primitive parity failure blocks integration or scale-up work.  FD
mismatches are explanatory unless they coincide with autodiff/JVP/VJP
disagreement or expose a scalar/fixture bug.

Failure of any named advancement condition stops M2 promotion and does not
unblock M3 integration, M7 handoff, or P82 validation.

Memory discipline is not established in M2.  M2 can establish only local
derivative consistency for dense tiny finite kernels; memory-ledger and
streaming/chunked claims remain M4/M6 gates.

## Forbidden Claims / Actions

- Do not expose a public API.
- Do not modify BayesFilter defaults.
- Do not run GPU or N10000 diagnostics.
- Do not claim correctness beyond tiny dense primitive parity.
- Do not use this phase to promote `transport_ad_mode=full`.

## Next-Phase Handoff Conditions

M3 may proceed only if M2 records:

- exact primitives tested;
- exact tolerances and observed max errors;
- no unresolved parity failure;
- unsupported modes still blocked;
- dense custom-gradient prototype target for M3.
- explicit nonclaim that M2 does not unblock P82.

## Stop Conditions

Stop and write a blocker if any primitive fails parity, if the tested scalar
does not match M1, if finite-difference diagnostics are unstable enough to
invalidate the comparison, or if the implementation requires public/default
changes before private parity is complete.
