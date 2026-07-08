# Phase 5 Subplan: Synthesis And Handoff

Date: 2026-07-01

Status: `REFRESHED_AFTER_PHASE4_PENDING_REVIEW`

## Phase Objective

Synthesize the regional, orthogonal, sensitivity, and transport-adjoint
diagnostics into a root-cause classification and the smallest justified next
action.

## Entry Conditions Inherited From Previous Phase

- Phase 1 completed and ruled out scalar-to-regional kappa aggregation failure.
- Phase 2 completed and localized the largest discrepancy to
  infection-vs-recovery contrast (`rho`) with secondary common-rate (`tau`)
  mismatch.
- Phase 3 completed and cleared local RHS/RK4 transition VJP algebra.
- Phase 4 completed and cleared local stopped-scale-key transport wrapper VJP
  algebra.
- Full-filter score correctness remains unresolved.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase5-synthesis-result-2026-07-01.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-visible-stop-handoff-2026-07-01.md`

## Required Checks, Tests, Reviews

- Verify every phase has a result or blocker artifact.
- Verify all material claims cite exact artifacts.
- Verify the synthesis preserves full-filter score uncertainty after Phase 3/4
  local passes.
- Claude read-only final review of synthesis and nonclaims.

Exact local commands:

```bash
rg -n "Status:|Decision|BLOCK|No SIR gradient correctness|No HMC readiness|not concluded|Nonclaims" docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase*-result-2026-07-01.md docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-visible-stop-handoff-2026-07-01.md
python - <<'PY'
from pathlib import Path
for phase in range(0, 5):
    hits = list(Path('docs/plans').glob(f'bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase{phase}-*result-2026-07-01.md'))
    print(phase, [str(p) for p in hits])
PY
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the best-supported current root-cause classification and next action? |
| Baseline/comparator | All completed artifacts from Phases 0-4 plus raw/physics/whitened entry evidence. |
| Primary pass criterion | Synthesis separates implementation bug, numerical/tuning failure, parametrization issue, and unresolved uncertainty with exact evidence. |
| Veto diagnostics | Overclaiming HMC readiness, unsupported root-cause certainty, treating local VJP passes as full-filter correctness, missing phase blocker, or changing thresholds after seeing results. |
| Explanatory diagnostics | Decision table, artifact map, strongest alternative explanation, next discriminating test. |
| Not concluded | Posterior correctness, production readiness, general nonlinear-model result. |

## Forbidden Claims And Actions

- Do not declare the score correct unless all stated gates support that claim.
- Do not bury negative results.
- Do not promote a default reparameterization from diagnostic-only evidence.
- Do not claim local transition/transport VJP passes resolve material
  GPU/TF32 full-route score behavior.

## Exact Next-Phase Handoff Conditions

No next phase is required by this master program.  If new work is justified,
write a new plan or a Phase 5 handoff with exact next diagnostic.

## Stop Conditions

- Missing artifacts prevent a fair synthesis.
- Claude final review identifies material unsupported claims that cannot be
  fixed in-place.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write Phase 5 result / close record.
3. Refresh visible stop handoff.
4. Review final artifacts for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
