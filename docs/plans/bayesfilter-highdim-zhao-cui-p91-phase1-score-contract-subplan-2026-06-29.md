# P91 Phase 1 Subplan: Score Contract Freeze

Date: 2026-06-29

Status: `PHASE0_REVIEW_PENDING_SCORE_CONTRACT_READY`

## Phase Objective

Freeze the released Zhao-Cui score contract: sign convention, parameterization,
fixed basis/rank/setup policy, training-base/no-ALS policy, branch/retained
identity, transport/proposal derivative policy, single and batched API
semantics, and release-note caveats.

## Entry Conditions Inherited From Previous Phase

- Phase 0 production contract reviewed pass.
- Production contract:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-production-contract-2026-06-29.md`
- Score identity is primary scientific gate.
- FD is necessary but not sufficient.
- GPU/XLA capability and batched APIs are required for HMC-facing production.
- This Phase 1 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Score contract:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-contract-2026-06-29.md`
- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-result-2026-06-29.md`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
rg -n "SourceRoute|score|basis|rank|ALS|training|batched|batch|derivative|proposal|transport" bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p9*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

Claude review is required for Phase 1 result and Phase 2 subplan. No algorithmic
code edit or runtime command is authorized unless the reviewed Phase 1 result
identifies a document-only contract patch.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P91 freeze an unambiguous Zhao-Cui score contract suitable for batched API, FD, score identity, GPU/XLA, HMC, and release notes? |
| Baseline/comparator | Reviewed P91 production contract and existing highdim source-route surfaces. |
| Primary criterion | Score contract names exact semantics, non-claims, and blockers/diagnostics without authorizing runtime promotion. |
| Veto diagnostics | Ambiguous sign, missing branch identity, ALS revival, hidden derivative omission, score identity as exact likelihood proof, or batched API mismatch left unspecified. |
| Explanatory diagnostics | Local source/API grep inventory. |
| Not concluded | No implementation correctness, FD pass, score identity pass, GPU/XLA readiness, HMC readiness, benchmark result, or production readiness. |
| Artifact | Score contract, Phase 1 result, refreshed Phase 2 subplan. |

## Forbidden Claims/Actions

- Do not claim the score is exact likelihood score.
- Do not claim omitted/frozen derivative policy is scientifically harmless
  without validation.
- Do not run FD, HMC, GPU/XLA, benchmarks, package/release/CI, or default
  commands.
- Do not change defaults.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if:

- Phase 1 result receives Claude `VERDICT: AGREE`;
- Phase 2 subplan receives Claude `VERDICT: AGREE`;
- single and batched API semantics are pinned or Phase 2 explicitly blocks on
  missing semantics.

## Stop Conditions

- Score sign/convention cannot be determined from local code/docs.
- Contract would hide derivative omissions/frozen terms.
- Local checks fail and cannot be repaired in document scope.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed code/runtime/default changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 1 result / close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 1 result and Phase 2 subplan.
