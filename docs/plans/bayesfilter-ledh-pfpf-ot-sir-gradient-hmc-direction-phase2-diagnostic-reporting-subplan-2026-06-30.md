# Phase 2 Subplan: Diagnostic Reporting And Test Hooks

Date: 2026-06-30

Status: `DRAFT_PENDING_PHASE1`

## Phase Objective

Implement or refresh SIR diagnostic reporting so the Phase 1 HMC-direction gate
is machine-readable and locally tested before any material GPU run.

## Entry Conditions Inherited From Previous Phase

- Phase 1 gate contract passed Claude review.
- Required fields are known: route metadata, compiler metadata, score route,
  FD slope, FD slope SE, per-seed MCSE, `combined_se`, `direction_scale`,
  `precision_pass`, row residual, sign status, supportive labels, pass or veto
  reason, and nonclaims.

## Required Artifacts

- Phase result: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase2-diagnostic-reporting-result-2026-06-30.md`
- Code diff if required, likely limited to:
  - `docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py`
  - focused tests under `tests/`
- Updated Phase 3 subplan.

## Required Checks, Tests, And Reviews

Local checks, adjusted to the final diff:

```bash
python -m py_compile docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
python -m pytest tests/test_ledh_pfpf_ot_p7_manual_score.py -q
```

If a new focused non-GPU test is added, include it in the pytest command.

Review:

- Claude read-only review is required for material implementation diffs.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the diagnostic emit the fields needed to apply the SIR HMC-direction gate without manual reinterpretation? |
| Baseline/comparator | Phase 1 gate contract and existing P8p diagnostic schema. |
| Primary criterion | Local checks pass and the diagnostic schema records route, numerical gate, `combined_se`, `precision_pass`, pass/veto reason, supportive labels, and nonclaims. |
| Veto diagnostics | Missing route fields; missing pass/veto reason; missing `combined_se` or `precision_pass`; missing nonclaims; test-only logic diverges from script logic; material code touches outside reviewed scope. |
| Explanatory diagnostics | Existing JSON structure, markdown table readability, test fixture coverage. |
| Not concluded | No GPU performance, no material SIR gradient result, no HMC readiness. |

## Forbidden Claims And Actions

- Do not run material GPU diagnostics in Phase 2 except a tiny smoke if Phase 3
  is explicitly entered.
- Do not modify unrelated benchmark or monograph files.
- Do not silently change thresholds from Phase 1.
- Do not use NumPy in BayesFilter-owned gradient implementation paths.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- local checks pass;
- any code diff is reviewed by Claude or is documented as non-material;
- Phase 3 command can validate GPU/XLA/TF32 route and report the new fields.

## Stop Conditions

- Required fields cannot be added without rewriting the diagnostic architecture.
- Local tests reveal a manual-score route defect.
- Claude flags a material implementation problem that does not converge within
  five rounds.

## End-Of-Phase Close Protocol

1. Run required local checks.
2. Write the Phase 2 result.
3. Refresh Phase 3 subplan.
4. Review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
