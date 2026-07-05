# Phase 1 Subplan: Reset Memo And Authority-Order Freeze

Date: 2026-06-29

## Status

`REVIEWED_AUTHORITY_FREEZE_SUBPLAN_CLOSED`

## Phase Objective

Freeze the fresh-agent reset memo and authority order so future work cannot
start from the wrong model family, wrong row, or wrong truth/test point.

## Entry Conditions Inherited From Previous Phase

- Phase 0 launch package is reviewed closed.
- The restart memo, master program, target / truth / source-scope contract,
  runbook, execution ledger, and review ledger are the active launch package.
- The generalized-SV testing specification, prior-mean amendment result, and
  native generalized-SV dense-reference result remain the governing upstream
  anchors for inherited facts.
- No source-row evaluator admission, score admission, HMC readiness, or
  leaderboard promotion is authorized yet.

## Required Artifacts

- Restart memo:
  `docs/plans/bayesfilter-generalized-sv-governed-restart-reset-memo-2026-06-29.md`
- Master program:
  `docs/plans/bayesfilter-generalized-sv-governed-master-program-2026-06-29.md`
- Target / truth / source-scope contract:
  `docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md`
- Visible runbook:
  `docs/plans/bayesfilter-generalized-sv-visible-gated-execution-runbook-2026-06-29.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-generalized-sv-visible-execution-ledger-2026-06-29.md`
- Claude review ledger:
  `docs/plans/bayesfilter-generalized-sv-claude-review-ledger-2026-06-29.md`
- Generalized-SV testing specification:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md`
- Prior-mean amendment result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-generalized-sv-prior-mean-amendment-result-2026-06-12.md`
- Native dense-reference result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md`
- Phase 1 result:
  `docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-result-2026-06-29.md`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-generalized-sv-governed-restart-reset-memo-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-governed-master-program-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-visible-gated-execution-runbook-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-visible-execution-ledger-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-claude-review-ledger-2026-06-29.md
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-generalized-sv-prior-mean-amendment-result-2026-06-12.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md
test -f docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-result-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-subplan-2026-06-29.md
rg -n "authority order|actual-SV|KSC|native generalized-SV dense|source-row|prior-mean|not concluded|promotion oracle" docs/plans/bayesfilter-generalized-sv-*.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-generalized-sv-prior-mean-amendment-result-2026-06-12.md docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md
git diff --check -- docs/plans/bayesfilter-generalized-sv-governed-restart-reset-memo-2026-06-29.md docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-subplan-2026-06-29.md docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-result-2026-06-29.md docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-subplan-2026-06-29.md docs/plans/bayesfilter-generalized-sv-visible-gated-execution-runbook-2026-06-29.md docs/plans/bayesfilter-generalized-sv-visible-execution-ledger-2026-06-29.md docs/plans/bayesfilter-generalized-sv-claude-review-ledger-2026-06-29.md
```

Required read-only Claude reviews:

- restart memo,
- Phase 1 result,
- refreshed Phase 2 subplan.

No implementation, benchmark mutation, score/gradient work, HMC, GPU/CUDA,
leaderboard mutation, package/network, release, CI, or default-policy command
is authorized in Phase 1.

## Skeptical Plan Audit

| Risk Checked | Phase 1 Control |
| --- | --- |
| Wrong baseline | Phase 1 authority order explicitly ranks the restart memo, successor phase results, testing spec/contract, native dense reference, then older historical artifacts. |
| Proxy metric promoted | Historical blocker or dataset-readiness artifacts remain context only unless the new governed program explicitly promotes them. |
| Missing stop condition | Phase 1 stops on any conflict about row family, truth/test point, or source-scope status. |
| Unfair comparison | Actual-SV, KSC surrogate SV, native generalized-SV dense oracle, and Zhao-Cui source-row evaluator remain separate evidence families. |
| Hidden assumption | The existence of a native dense reference is not treated as proof that the source-row evaluator already exists or is admitted. |
| Stale context | Older P44/P45/P47/P50/P51 notes are preserved as historical context only. |
| Environment mismatch | Phase 1 is document/source-inventory only; no runtime evidence is created. |
| Artifact-answer mismatch | Phase 1 must freeze both the reset memo semantics and the authority order that later phases will inherit. |

Audit status: passed if the authority order remains explicit and every inherited
nonclaim is preserved.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 1 freeze an unambiguous reset memo and authority order for Generalized-SV so later phases cannot drift to the wrong family, row, truth/test point, or comparator? |
| Baseline/comparator | Phase 0 reviewed launch package, generalized-SV testing specification, prior-mean amendment result, native dense-reference result, and older generalized-SV historical artifacts. |
| Primary criterion | The reset memo and Phase 1 result record the correct authority order, inherited nonclaims, and identity separation without authorizing evaluation or promotion. |
| Veto diagnostics | actual-SV/generalized-SV confusion, KSC promoted as generalized-SV same-target evidence, native oracle/source-row blending, wrong truth/test point, missing prior-mean caveat, or lower-ranked artifacts overriding higher-ranked authority. |
| Explanatory diagnostics | exact path inventory, authority-order wording, and historical-context notes. |
| Not concluded | No source-row evaluator admission, no same-target SGQF pass, no score admission, no HMC readiness, no production readiness, and no leaderboard promotion. |
| Artifact | `docs/plans/bayesfilter-generalized-sv-governed-restart-reset-memo-2026-06-29.md`, `docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-result-2026-06-29.md`, and refreshed `docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-subplan-2026-06-29.md`. |

## Forbidden Claims/Actions

- Do not reinterpret historical generalized-SV blockers as current authority
  unless the new authority order explicitly says so.
- Do not let implementation surfaces, tests, registries, or leaderboards outrank
  the reviewed reset memo or contract.
- Do not authorize any evaluator execution or promotion.
- Do not run runtime, benchmark, GPU/CUDA, score/gradient, HMC,
  package/network, release, CI, or default-policy commands.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if:

- the restart memo receives Claude `VERDICT: AGREE` as the active fresh-agent
  authority;
- the Phase 1 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 2 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records Phase 1 as reviewed closed with preserved
  authority order and nonclaims.

## Stop Conditions

- The reset memo or Phase 1 result contradicts the reviewed testing
  specification.
- The authority order would let lower-ranked implementation surfaces silently
  override higher-ranked contracts.
- Local document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require runtime, benchmark, evaluator, GPU/CUDA,
  package/network, release, CI, default-policy, destructive git/filesystem, or
  unrelated dirty worktree changes.

## End-Of-Phase Requirements

1. Run the required local document/source-inventory checks.
2. Write the Phase 1 result.
3. Refresh the Phase 2 subplan.
4. Review the restart memo, Phase 1 result, and refreshed Phase 2 subplan.
5. Update the execution ledger and Claude review ledger.
