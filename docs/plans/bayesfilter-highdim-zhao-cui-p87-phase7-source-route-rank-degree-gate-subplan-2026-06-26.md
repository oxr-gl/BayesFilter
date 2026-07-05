# P87 Phase 7 Subplan: Source-Route Rank/Degree Gate

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE7_EXECUTION`

## Phase Objective

Audit whether prior source-route execution-only evidence can upgrade to a
same-route rank/degree-stable source-route label under P86 training-base/L1
discipline, without running new fits or promoting correctness.

## Entry Conditions Inherited From Previous Phase

- Phase 6 selected the source-route rank/degree lane as the only admissible
  non-all-pairs handoff route.
- Phase 6 did not establish SIR d18 correctness, source-route correctness, or
  full-history analytical-gradient correctness.
- Dense all-pairs, streamed all-pairs, local/operator source-faithful
  overclaims, and proxy promotion remain blocked.
- Execution-only is not correctness.

## Required Artifacts

- Phase 7 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase7-source-route-rank-degree-gate-result-2026-06-26.md`
- Rank/degree artifact inventory.
- Decision table and run/check manifest.
- Explicit mapping from P86 rank/degree artifacts to P87 allowed final labels.
- Updated Phase 8 subplan.

## Required Checks/Tests/Reviews

Allowed edit scope:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase7-source-route-rank-degree-gate-result-2026-06-26.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase8-correctness-candidate-bridge-subplan-2026-06-26.md`
- P87 execution/review ledgers

Allowed read/check scope:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83*.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p86*.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87*.md`
- `scripts/p86_author_lagrangep_phase5_budget_fit.py`
- `tests/highdim/test_p86_phase5_budget_preflight.py`

Execution environment:

- Repository root: `/home/chakwong/BayesFilter`.
- Execution target: local artifact audit only.
- No TensorFlow numerical command, new fit, GPU/CUDA command, HMC, LEDH, or
  production benchmark is required or allowed in Phase 7.
- If a Python/TensorFlow check becomes necessary during a repair loop, the
  subplan must be visibly patched first and the command must use
  `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
- Network/model access: none during local checks; Claude is read-only review
  only.

Planning checks:

```bash
set -euo pipefail
rg -n "P86_PHASE6|L1|training-base|ALS|holdout|audit|rank|degree|extension_or_invention|source-faithful" docs/plans/bayesfilter-highdim-zhao-cui-p86*.md scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
rg -n "P86_PHASE6W_RANK_CONVERGENCE_PASSED_DEGREE_BLOCKED_REVIEWED|P86_PHASE6Y_DEGREE_ORDER3_RANK4_FIT_COMPLETED_REVIEWED|degree convergence|Phase 7 remains blocked|L1 tuning remains" docs/plans/bayesfilter-highdim-zhao-cui-p86*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Claude review required for the Phase 7 subplan and any Phase 7 result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can source-route evidence upgrade from execution-only to same-route rank/degree stability? |
| Baseline/comparator | P83 execution-only/result-tier discipline; P86 Lagrangep author-basis rank, L1, configurable-basis, and degree-comparator artifacts. |
| Primary criterion | A stable label may pass only if rank and degree evidence are both reviewed, same-policy or explicitly classified, use training-base/L1 tuning discipline, preserve validation/holdout/audit separation, avoid ALS, avoid source-faithful overclaims for non-default basis choices, and do not rely on fit residuals as correctness proof. Otherwise Phase 7 must block or emit a weaker source-route label. |
| Veto diagnostics | ALS revival, zero-L1 silently promoted as default, audit tuning, missing degree comparator, unresolved degree gate, non-default basis called source-faithful, fit residual promoted to correctness, new fit/GPU/HMC/LEDH/default-policy drift. |
| Explanatory diagnostics | Fit/holdout residuals, validation events, normalizers, parameter/sample budgets, L1 margin decisions, rank/degree comparator classification. |
| Not concluded | Exact correctness, analytical-gradient correctness, HMC, production, GPU, LEDH, d50/d100 scaling. |
| Artifact | Phase 7 result, rank/degree inventory, decision table, run/check manifest. |

## Forbidden Claims/Actions

- Do not claim correctness from rank/degree stability alone.
- Do not run new fits in Phase 7.
- Do not use audit data for tuning.
- Do not treat `l1_weight=0.0` selection as a universal scalar default; L1
  tuning remains the Zhao-Cui default procedure.
- Do not call the non-default `Lagrangep(3,8)` degree comparator
  source-faithful.
- Do not reopen Phase 7/production/HMC/source-route correctness from favorable
  degree-comparator evidence alone.

## Exact Next-Phase Handoff Conditions

Phase 8 may start only if Phase 7 passes or explicitly blocks with the missing
rank/degree artifact. Phase 8 must require a source-backed same-target
reference or bridge.

## Stop Conditions

- Missing budget-compliant comparator.
- Missing L1 tuning/validation discipline.
- Degree evidence remains explicitly blocked or too weak for rank/degree-stable
  upgrade.
- Phase 7 would need a new fit, GPU command, HMC, LEDH, or criterion change.
- Claude review nonconvergence.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 7 result/close or blocker record.
3. Draft or refresh Phase 8 subplan.
4. Review Phase 8 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
