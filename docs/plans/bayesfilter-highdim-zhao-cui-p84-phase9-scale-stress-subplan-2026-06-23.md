# P84 Phase 9 Subplan: d50/d100 Scale Stress And Uncertainty Accounting

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE8_AND_APPROVAL`

## Phase Objective

Run or block d=50/d=100 scale/stress after stronger d=18 evidence, and certify
multi-seed/uncertainty accounting for any scale/stress claim in scope.

## Entry Conditions Inherited From Previous Phase

- Phase 8 and stronger d=18 gates justify scale/stress, or the phase is labeled
  stress-only with no correctness implication.
- Exact GPU/CPU commands, seeds, dimensions, runtime posture, and artifacts are
  frozen.
- Phase 0 has assigned the multi-seed/uncertainty accounting obligation to this
  phase for any d=50/d=100 claim.
- Explicit human approval is required before any scale/stress command.

## Required Artifacts

- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase9-scale-stress-result-2026-06-23.md`
- Scale/stress manifests.
- Multi-seed/uncertainty accounting manifest, or blocker explaining why it
  cannot be certified.
- Updated execution ledger and Phase 10 subplan.

## Required Checks / Tests / Reviews

Before execution, exact commands must be added.  Design checks:

```bash
rg -n "d50|d100|scale|stress|memory|runtime|GPU|stress-only|correctness" \
  docs/plans \
  bayesfilter/highdim \
  experiments -S
```

Claude review and explicit human approval are required before scale/stress.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the candidate survive declared d=50/d=100 stress with valid multi-seed/uncertainty accounting, without overclaiming correctness? |
| Baseline/comparator | Prior phase result documenting d=18 stronger-tier evidence, plus the stress-only protocol when used. |
| Primary criterion | Finite diagnostics, bounded runtime/memory, declared uncertainty accounting, and no vetoes under declared scope. |
| Veto diagnostics | d=18 stronger evidence missing, OOM, nonfinite diagnostics, missing uncertainty accounting, stress-only promoted to correctness. |
| Explanatory diagnostics | Runtime, memory, ESS, normalizers, correction ranges. |
| Not concluded | No correctness unless correctness bridge also scales. |
| Artifact | Scale/stress result. |

## Forbidden Claims / Actions

- Do not run d=50/d=100 without exact approval.
- Do not claim correctness from stress survival.
- Do not hide one-seed or short-run uncertainty limits.

## Exact Next-Phase Handoff Conditions

Phase 10 may begin only if every mandatory production gate is pass or explicitly
out of scope with owner acceptance, and multi-seed/uncertainty accounting is
certified or blocked.

## Stop Conditions

Stop if scale/stress prerequisites or uncertainty-accounting prerequisites are
missing.
