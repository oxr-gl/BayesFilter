# G2 Subplan: Scope/Fallback Decision After Sparse N8192 Drift

Date: 2026-06-24

Status: `READY_FOR_LOCAL_AND_OPTIONAL_REVIEW`

## Phase Objective

Decide the next evidence path after G1 classified the broader `N=8192` panel as
sparse drift: no repair selection now, no default promotion, and continuation
only as a restricted diagnostic fixed-policy path with the known hard seed
preserved.

## Entry Conditions Inherited From Previous Phase

- G1 result exists:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-result-2026-06-24.md`.
- G1 classification is `G1_SPARSE_N8192_DRIFT`.
- New seeds `82924..82931` passed, but known seed `82921` remains a valid prior
  paired mean threshold failure.
- Current fixed policy remains frozen:
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`.
- G2 may choose a diagnostic continuation path, but may not accept a hard seed
  for default promotion or change product/default policy.

## Required Artifacts

- G2 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g2-scope-fallback-decision-result-2026-06-24.md`
- Refreshed G3 subplan if continuing:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g3-history-memory-subplan-2026-06-24.md`
- Execution ledger update:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-visible-execution-ledger-2026-06-24.md`

## Required Checks, Tests, And Reviews

- Local artifact check:
  - G1 result exists and records `G1_SPARSE_N8192_DRIFT`;
  - G1 summary JSON exists and records `paired_threshold_failures == 0`;
  - known seed `82921` failure is still cited as unresolved;
  - no repair/tuning/default claim is introduced.
- Local claim-boundary scan for default, HMC, posterior, ranking, and failure
  probability overclaims.
- Claude read-only review is recommended if G2 makes a material repair/scope
  decision.  Claude cannot authorize default promotion or product acceptance.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Given sparse new-panel drift and one known hard seed, what is the next safe evidence path? |
| Baseline/comparator | G1 artifacts and prior `82921` replay artifact; future paired rows still use same-artifact compiled streaming comparator. |
| Primary decision criterion | Choose one of: no repair and continue diagnostic G3 with hard-seed caveat; open repair only if G1 showed repeated drift or numeric veto; stop for human decision if accepting `82921` as default-compatible would be required. |
| Veto diagnostics | Unsupported default promotion, hard-seed erasure, repair/tuning without trigger, threshold relaxation, treating G1 as statistical failure-probability evidence. |
| Explanatory only | G1 pass count, observed paired delta margins, runtime. |
| Not concluded | No default readiness, no acceptance of known hard seed for production default, no HMC readiness, no posterior correctness, no ranking. |
| Artifact | G2 result and refreshed G3 subplan or blocker. |

## Forbidden Claims/Actions

- Do not claim `N=8192` is broadly solved.
- Do not claim seed `82921` is acceptable for a default route.
- Do not change thresholds, rank, epsilon, solver, chunks, or seed policy.
- Do not launch repair after G1 sparse drift.
- Do not proceed to final default review before history/memory and gradient
  mechanics gates.

## Exact Next-Phase Handoff Conditions

- `G2_DIAGNOSTIC_CONTINUE_TO_G3`: choose no repair now; preserve the `82921`
  hard-case caveat; continue only to fixed-policy history/memory diagnostics.
- `G2_STOP_FOR_HUMAN_SCOPE_DECISION`: stop if the next step would require
  accepting a known hard seed as compatible with default production scope.
- `G2_REPAIR_SELECTED`: not allowed under current G1 result unless a new
  artifact invalidates G1 or shows repeated drift/numeric veto.
- `G2_HARNESS_OR_ARTIFACT_BLOCKER`: stop if G1 artifacts are inconsistent or
  malformed.

## Stop Conditions

- G1 result or summary artifact missing/malformed.
- Local claim-boundary scan finds unsupported default/HMC/posterior/ranking
  claims.
- Proceeding would require human acceptance of unresolved seed `82921` for
  default scope.
- Review finds a material unpatched flaw.

## Skeptical Plan Audit

Wrong baseline is controlled by using G1 artifacts and the known same-artifact
paired replay for seed `82921`.  Proxy metrics are not promotion criteria.
Sparse drift does not erase the known hard seed.  G2 can permit only a
diagnostic continuation to G3 or stop for human/default-scope decision; it
cannot promote the route.

Audit status: `PASS_FOR_LOCAL_G2_DECISION_AFTER_CHECKS`.
