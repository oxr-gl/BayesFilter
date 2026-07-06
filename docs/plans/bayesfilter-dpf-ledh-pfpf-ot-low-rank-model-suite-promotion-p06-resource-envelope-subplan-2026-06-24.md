# P06 Large-N And Long-T Resource Envelope Subplan

Date: 2026-06-24

Status: `PROVISIONAL_PENDING_P05_RESULT_AND_REFRESH`

## Phase Objective

After quality gates, test large-particle and long-horizon resource envelope for
locked low-rank LEDH-PFPF-OT without turning unpaired large-N rows into
superiority claims.

## Entry Conditions Inherited From Previous Phase

- P01 through P05 results exist and do not fire a continuation veto.
- Candidate lock remains unchanged.
- Streaming comparator remains available for feasible paired rows.
- Trusted GPU runtime requires explicit approval.

## Required Artifacts

- P06 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p06-resource-envelope-result-2026-06-24.md`
- P07 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p07-hmc-autodiff-subplan-2026-06-24.md`
- Resource-envelope JSON/Markdown artifacts under `docs/benchmarks`.
- Logs under `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/`.

## Required Checks, Tests, And Reviews

- Refresh N/T ladders after prior phase results.
- Syntax and focused tests for selected harness.
- Trusted GPU precheck.
- Paired streaming/low-rank rows for feasible N/T values.
- Low-rank-only envelope rows only after comparator infeasibility is recorded
  under a predeclared timeout/resource boundary.
- Validators for finite outputs, route-fired evidence, nonmaterialization,
  GPU/TF32/XLA provenance, timeout sidecars, and paired comparability.
- Claude read-only review of P06 result and P07 subplan if material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does low-rank extend the executable resource envelope after passing quality gates? |
| Baseline/comparator | Streaming GPU/TF32 route for feasible paired rows; timeout/resource sidecars for boundary rows. |
| Primary pass criterion | Feasible paired rows pass hard screens; any low-rank-only envelope rows are explicitly unpaired and pass nonmaterialization/provenance screens. |
| Veto diagnostics | Nonfinite output, route mismatch, missing timeout sidecar for comparator infeasibility, dense materialization, active-path NumPy, missing GPU/TF32/XLA provenance, or unsupported speedup claim. |
| Explanatory diagnostics | Runtime, memory, warm ratios, timeouts, compile time, ESS, and storage estimates. |
| Not concluded | No statistical superiority, unpaired speed superiority, posterior correctness, HMC readiness, dense equivalence, or package/public default readiness. |
| Artifact | P06 result, benchmark artifacts, logs, ledgers. |

## Forbidden Claims And Actions

- Do not claim speed superiority at unpaired large-N/long-T rows.
- Do not claim memory improvement unless a declared memory screen passes.
- Do not change candidate settings after seeing results.
- Do not run HMC/autodiff runtime.
- Do not change default policy, public API, package metadata, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P06 hands off to P07 only if P06 passes or writes a reviewed blocker that does
not invalidate the candidate and P07 is either explicitly approved for
HMC/autodiff runtime or refreshed as a skip/nonclaim branch.

## Stop Conditions

- Resource harness cannot preserve comparator semantics.
- Valid resource gate reveals candidate nonfinite output or dense
  materialization.
- Trusted GPU runtime is unavailable or unapproved.
- Review does not converge within five rounds for the same blocker.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write P06 result or blocker result.
3. Draft or refresh P07 subplan.
4. Review P07 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
