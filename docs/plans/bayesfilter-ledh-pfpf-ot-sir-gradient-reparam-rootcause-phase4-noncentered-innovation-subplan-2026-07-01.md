# Phase 4 Subplan: Non-Centered Innovation Diagnostic

Date: 2026-07-01

Status: `SUPERSEDED_BY_PHASE4_TRANSPORT_ADJOINT_AFTER_PHASE3`

Supersession note: Phase 3 passed the transition-only RHS/RK4 VJP audit, so
the next smallest justified diagnostic is the transport-adjoint /
stopped-scale-key boundary.  This non-centered innovation plan remains a
possible later diagnostic but is not the active Phase 4 gate.

## Phase Objective

Test whether a fixed-innovation representation of process randomness changes
or explains the kappa/nu score behavior.

## Entry Conditions Inherited From Previous Phase

- Phase 3 did not fully explain the mismatch, or explicitly left centered
  process-noise representation as a plausible confound.
- Process covariance dependence on kappa/nu has been checked.

## Required Artifacts

- Non-centered diagnostic:
  `docs/benchmarks/diagnose_p8p_sir_noncentered_innovation_route.py`
- Unit/smoke tests:
  `tests/test_p8p_sir_noncentered_innovation_route.py`
- Material wrapper, only if target-preserving implementation is available:
  `scripts/run_sir_gradient_reparam_rootcause_phase4_noncentered_budget10.sh`
- Non-centered diagnostic design/result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-noncentered-innovation-result-2026-07-01.md`
- Optional JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-noncentered-innovation-2026-07-01.json`

## Required Checks, Tests, Reviews

- Code-path check for whether process covariance depends on kappa/nu.
- If implemented, local equality check that centered and non-centered values
  match for fixed innovations.
- Material GPU/XLA/TF32 diagnostic only if the non-centered path preserves the
  target and baseline route.
- Claude read-only review before interpreting a non-centered result as a root
  cause signal.

Exact local command templates:

```bash
rg -n "process_covariance|transition_covariance|process_noise|initial_particles|fixed.*seed|standard_normal|random" docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py experiments/dpf_implementation/tf_tfp
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/diagnose_p8p_sir_noncentered_innovation_route.py
pytest -q tests/test_p8p_sir_noncentered_innovation_route.py
bash -n scripts/run_sir_gradient_reparam_rootcause_phase4_noncentered_budget10.sh
```

Exact optional material command, run only if target-preserving implementation
is available:

```bash
bash scripts/run_sir_gradient_reparam_rootcause_phase4_noncentered_budget10.sh
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does fixing standard-normal innovations separate stochastic-state representation effects from deterministic SIR transition sensitivity? |
| Baseline/comparator | Centered fixed-seed SIR budget-10 route and Phase 3 transition audit. |
| Primary pass criterion | Non-centered route must be classified as `target_preserving_score_delta`, `target_preserving_no_material_delta`, `not_target_preserving`, or `not_implemented`. Covariance-independence alone is explanatory only and cannot by itself rule out representation effects. |
| Veto diagnostics | Changed target distribution, changed random seeds without exact mapping, CPU material route, missing centered-vs-non-centered value equality. |
| Explanatory diagnostics | Value deltas, score deltas, innovation mapping, covariance dependence check. |
| Not concluded | General stochastic PF gradient correctness or HMC readiness. |

## Forbidden Claims And Actions

- Do not claim non-centered is superior without full target-preserving evidence.
- Do not change model covariance policy as a hidden repair.
- Do not run a CPU-only material comparison.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 if:

- Phase 4 either rules out non-centering as relevant or produces a documented
  score-delta signal by the classification rule above.
- All unresolved blockers are listed with artifacts.

## Stop Conditions

- Non-centered representation would change the target rather than re-express
  the same fixed-noise computation.
- Required fixed-innovation mapping is not available without broad rewrites.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write Phase 4 result / close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
