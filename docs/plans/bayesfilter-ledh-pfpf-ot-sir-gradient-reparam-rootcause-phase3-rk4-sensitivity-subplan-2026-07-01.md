# Phase 3 Subplan: RK4 Sensitivity Audit

Date: 2026-07-01

Status: `REFRESHED_AFTER_PHASE2_PENDING_REVIEW`

## Phase Objective

Audit the SIR RK4 transition derivative with explicit sensitivity equations or
an independent local autodiff comparator before transport/resampling terms are
involved.

## Entry Conditions Inherited From Previous Phase

- Phase 2 indicates the dominant mismatch is the regional
  infection-vs-recovery contrast (`rho`) with secondary common-rate (`tau`)
  discrepancy.
- Current manual VJP code anchors for `_sir_rhs_vjp_tf` and
  `_sir_transition_mean_vjp_tf` are known.
- Phase 3 is transition-only.  It must not run LEDH transport, resampling, or
  full filter scoring unless the subplan is revised and reviewed.
- Phase 3 is a narrowing step, not evidence that transition is the leading
  remaining culprit.  Transport-adjoint and stopped-scale-key routes remain
  live alternatives if transition algebra passes.

## Required Artifacts

- Focused RK4 sensitivity diagnostic:
  `docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py`
- Unit/smoke tests:
  `tests/test_p8p_sir_rk4_sensitivity_vjp.py`
- Phase 3 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-result-2026-07-01.md`
- Optional JSON if a numerical diagnostic is run:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-2026-07-01.json`

## Required Checks, Tests, Reviews

- Compare manual VJP against local autodiff/sensitivity equations on tiny
  fixed tensors for kappa and nu.
- Verify regional score chain-rule through RK4 transition alone.
- Syntax/compile checks for touched files.
- Run the diagnostic locally on CPU unless a GPU is explicitly needed; record
  CPU-only status as transition-only algebra, not material LEDH evidence.
- Claude read-only review for any derivation/result that changes the root-cause
  target.

Exact local command templates:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py
pytest -q tests/test_p8p_sir_rk4_sensitivity_vjp.py
```

Exact diagnostic command:

```bash
python docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-2026-07-01.json
```

Phase 3 local RK4 checks may be CPU-only if they do not initialize or evaluate
LEDH transport and are explicitly recorded as transition-only algebra checks.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the manual RK4 transition derivative for kappa/nu correct before LEDH transport terms enter? |
| Baseline/comparator | Independent TensorFlow autodiff comparator on identical fixed tensors in float64 CPU transition-only algebra. |
| Primary pass criterion | For each checked tensor family (`bar_state`, `bar_kappa`, `bar_nu`, regional log-kappa contractions, regional log-nu contractions), the manual VJP vs autodiff comparator must satisfy both max absolute residual `<= 1.0e-8` and relative L2 residual `<= 1.0e-7`, with denominator `max(norm(comparator), 1.0)`. If this fails, the result must localize the mismatch to RHS, RK4 step, or multi-substep scan. |
| Veto diagnostics | Comparator uses different state/parameter semantics, missing regional chain-rule check, unsupported claim about full filter score from transition-only test. |
| Explanatory diagnostics | Stage-wise residuals, per-region derivatives, state/cotangent shapes. |
| Not concluded | Full filter score correctness, transport adjoint correctness, HMC readiness. |

## Forbidden Claims And Actions

- Do not infer full filter correctness from transition-only agreement.
- Do not introduce NumPy into gradient-bearing implementation paths.
- Do not change production transition semantics.
- Do not treat CPU transition-only checks as evidence for GPU LEDH runtime
  behavior.
- Do not introduce the non-centered/process-noise representation hypothesis in
  the Phase 3 exit unless the Phase 3 result gives explicit transition evidence
  that makes it the next smallest discriminating diagnostic.

## Exact Next-Phase Handoff Conditions

Advance to the next phase only if:

- RK4 transition derivative passes the float64 CPU transition-only audit and
  the result explicitly preserves transport-adjoint/stopped-scale-key routes as
  live alternatives; then draft the next subplan for the smallest remaining
  discriminating diagnostic.
- RK4 transition derivative fails the local audit but the failure is localized
  to a named RHS/RK4/scan term; then draft a repair subplan rather than
  advancing.
- Any next subplan must state exact evidence that justifies its target; Phase 3
  alone does not pre-authorize non-centered/process-noise diagnostics.

## Stop Conditions

- Transition VJP mismatch is found and a local repair is clearly required.
- Independent comparator cannot be made semantically identical.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write Phase 3 result / close record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
