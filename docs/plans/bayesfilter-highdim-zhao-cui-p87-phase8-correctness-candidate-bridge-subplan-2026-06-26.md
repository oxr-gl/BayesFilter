# P87 Phase 8 Subplan: Correctness-Candidate Bridge Gate

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE8_EXECUTION`

## Phase Objective

Decide whether source-route evidence can become a correctness candidate by
using a same-target source-backed reference or bridge, while preserving the
Phase 7 block on rank/degree-stable status.

The Phase 8 same-target identity is the bounded fixed-TTSIRT source-route
SIR d=18 implementation evaluated by the P83/P59 runner/readiness and
execution-only ladder artifacts. The bridge inventory/result must restate this
target identity and cite the artifact anchor that claims
`missing_same_target_reference_or_bridge` remains active for stronger tiers.

## Entry Conditions Inherited From Previous Phase

- Phase 7 provided an explicit blocker for `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`
  because degree convergence remains unresolved.
- P83 source-route evidence remains execution-only.
- No correctness, source-route correctness, or full-history analytical-gradient
  claim has been made.
- Proxy promotion remains blocked.

## Required Artifacts

- Phase 8 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase8-correctness-candidate-bridge-result-2026-06-26.md`
- Same-target reference/bridge inventory embedded in the Phase 8 result.
- Decision table and run/check manifest embedded in the Phase 8 result.
- Explicit mapping to `D18_CORRECTNESS_CANDIDATE` pass/block status.
- Updated Phase 9 subplan.

## Required Checks/Tests/Reviews

Allowed edit scope:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase8-correctness-candidate-bridge-result-2026-06-26.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase9-final-claim-gate-subplan-2026-06-26.md`
- P87 execution/review ledgers

Allowed read/check scope:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83*.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p86*.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87*.md`
- `bayesfilter/highdim`
- `tests/highdim`

Execution environment:

- Repository root: `/home/chakwong/BayesFilter`.
- Execution target: local artifact audit only.
- No TensorFlow numerical command, new fit, GPU/CUDA command, HMC, LEDH, or
  production benchmark is required or allowed in Phase 8.
- If a Python/TensorFlow check becomes necessary during a repair loop, the
  subplan must be visibly patched first and the command must use
  `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
- Network/model access: none during local checks; Claude is read-only review
  only.

```bash
set -euo pipefail
rg -n "same-target reference|reference bridge|correctness_candidate|d18_correctness_candidate|source-backed comparator|no d18 correctness|missing_same_target_reference_or_bridge|fixed-TTSIRT source-route SIR d=18|P59_AUTHOR_SIR_TARGET_ID|P58_M9_AUTHOR_SIR_TARGET_ID" docs/plans/bayesfilter-highdim-zhao-cui-p83*.md docs/plans/bayesfilter-highdim-zhao-cui-p86*.md docs/plans/bayesfilter-highdim-zhao-cui-p87*.md bayesfilter/highdim tests/highdim -g '*.md' -g '*.py'
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

The `rg` command is a discovery aid and anchor finder, not a proof of absence.
The Phase 8 result must state whether any candidate bridge found by the search
is same-target, source-backed, tolerance-pinned, and separable from proxy
execution/rank/degree evidence.

Claude review required.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a same-target source-backed reference or bridge sufficient for a correctness-candidate claim for the bounded fixed-TTSIRT source-route SIR d=18 target? |
| Baseline/comparator | P83/P59 correctness-candidate blocker, P86 rank/degree blocker status, and any available same-target source-backed reference. |
| Primary criterion | A bridge exists with scope, tolerances, source anchors, and vetoes, or result blocks. |
| Veto diagnostics | Proxy correctness, non-source-backed bridge, wrong target, stale comparator, missing tolerances, rank/degree-stable blocker silently bypassed. |
| Explanatory diagnostics | Reference provenance and scope. |
| Not concluded | Production, posterior correctness, source-route correctness, or full-history analytical-gradient correctness unless separately gated. |
| Artifact | Phase 8 result, bridge inventory, decision table, run/check manifest. |

## Forbidden Claims/Actions

- Do not create a correctness claim from execution-only or rank stability.
- Do not create a correctness claim from favorable degree-comparator evidence.
- Do not use LEDH/UKF/local diagnostic routes as source-route correctness
  without reviewed bridge status.
- Do not bypass the Phase 7 rank/degree-stable blocker.

## Exact Next-Phase Handoff Conditions

Phase 9 may start after Phase 8 either passes a bridge gate or records an
explicit Phase 8 blocker, including `BLOCK_SOURCE_ROUTE_REFERENCE_BRIDGE_MISSING`,
`BLOCK_WRONG_TARGET_BRIDGE`, `BLOCK_PROXY_CORRECTNESS_BRIDGE`,
`BLOCK_BRIDGE_TOLERANCE_MISSING`, or `BLOCK_PHASE8_REVIEW_NOT_CONVERGED`.

## Stop Conditions

- No same-target reference/bridge.
- Bridge depends on forbidden proxy metric.
- A candidate bridge cannot be separated from execution-only/rank/degree proxy
  evidence.
- Candidate bridge target identity, source anchors, or tolerances cannot be
  pinned in the Phase 8 result.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 8 result/close or blocker record.
3. Draft or refresh Phase 9 subplan.
4. Review Phase 9 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
