# Phase 0 Subplan: Launch And Inherited-Boundary Freeze

Date: 2026-06-29

## Status

`REVIEWED_LAUNCH_SUBPLAN_CLOSED`

## Phase Objective

Launch the Generalized-SV fresh-agent governed package, freeze the inherited
authority set, and verify that the launch package is coherent before any
implementation or promotion work begins.

## Entry Conditions Inherited From Previous Phase

- The restart memo exists and is the first-read authority for fresh agents:
  `docs/plans/bayesfilter-generalized-sv-governed-restart-reset-memo-2026-06-29.md`.
- The governed master program exists:
  `docs/plans/bayesfilter-generalized-sv-governed-master-program-2026-06-29.md`.
- The target / truth / source-scope contract exists:
  `docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md`.
- The visible runbook, execution ledger, Claude review ledger, and stop handoff
  template exist.
- First-wave phase subplans through Phase 4 exist.
- No implementation, benchmark mutation, source-row promotion, score
  admission, HMC admission, or leaderboard-status upgrade is authorized yet.

## Required Artifacts

Launch package inputs:

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
- Stop handoff:
  `docs/plans/bayesfilter-generalized-sv-visible-stop-handoff-2026-06-29.md`
- Phase 1 subplan:
  `docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-subplan-2026-06-29.md`
- Phase 2 subplan:
  `docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-subplan-2026-06-29.md`
- Phase 3 subplan:
  `docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-subplan-2026-06-29.md`
- Phase 4 subplan:
  `docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-subplan-2026-06-29.md`
- Generalized-SV testing specification:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md`
- Native dense-reference result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md`
- Prior-mean amendment result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-generalized-sv-prior-mean-amendment-result-2026-06-12.md`

Phase 0 closeout outputs:

- Phase 0 result:
  `docs/plans/bayesfilter-generalized-sv-phase0-launch-boundary-freeze-result-2026-06-29.md`
- Refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-generalized-sv-governed-restart-reset-memo-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-governed-master-program-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-visible-gated-execution-runbook-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-visible-execution-ledger-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-claude-review-ledger-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-visible-stop-handoff-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-subplan-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-subplan-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-subplan-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-subplan-2026-06-29.md
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-generalized-sv-prior-mean-amendment-result-2026-06-12.md
rg -n "zhao_cui_generalized_sv_synthetic_from_estimated_values|native generalized-SV dense|prior-mean|precursor|same-target|oracle|source-scope" docs/plans/bayesfilter-generalized-sv*.md
git diff --check -- docs/plans/bayesfilter-generalized-sv*.md
```

Required read-only Claude reviews:

Core review-gated launch authorities:

- restart memo,
- master program,
- target / truth / source-scope contract,
- visible runbook,
- this Phase 0 subplan,
- then Phase 0 result and refreshed Phase 1 subplan.

Supporting inputs that must exist and be cross-checked locally, but are not
separately Phase-0 review-gated unless an inconsistency is later found:

- input Phase 1 subplan before refresh,
- execution ledger,
- Claude review ledger,
- stop handoff,
- Phase 2 subplan,
- Phase 3 subplan,
- Phase 4 subplan,
- generalized-SV testing specification,
- native dense-reference result,
- prior-mean amendment result.

The execution ledger and Claude review ledger are bookkeeping artifacts in Phase
0: they must be updated as part of closeout, but they do not require separate
one-path review unless a later bounded review finds an inconsistency in them.

No runtime, TensorFlow, GPU/CUDA, benchmark, leaderboard, score, derivative,
HMC, package/network, release, CI, or default-policy command is authorized in
Phase 0.

## Skeptical Plan Audit

| Risk Checked | Phase 0 Control |
| --- | --- |
| Wrong baseline | Phase 0 requires the restart memo, testing specification, prior-mean amendment result, and native dense-reference result to exist before any launch closeout is written. |
| Proxy metric promoted | Artifact existence and document coherence are launch criteria only; they do not admit any evaluator, value gate, score gate, or leaderboard promotion. |
| Missing stop condition | Wrong target identity, actual-SV/generalized-SV confusion, KSC promotion drift, native-oracle/source-row blending, wrong truth/test point, and missing source-scope evaluator are all explicit blockers in the governing package. |
| Unfair comparison | Phase 0 preserves separation among actual-SV, KSC surrogate SV, native generalized-SV dense oracle, and Zhao-Cui generalized-SV source-row SGQF routes. |
| Hidden assumption | SP500 remains source-estimation input only; it is not benchmark observation data for the governed row. |
| Stale context | The 2026-06-29 restart memo and successor master/contract artifacts outrank older P44/P45/P47/P50/P51 historical notes. |
| Environment mismatch | Phase 0 is document-only. No GPU, TensorFlow, benchmark, or evaluator execution is allowed. |
| Artifact-answer mismatch | Phase 0 must close with reviewed launch artifacts plus a refreshed Phase 1 subplan; a partial package is insufficient. |

Audit status: passed for launch preparation if the launch-package inputs exist,
local document checks pass, the Phase 0 result and refreshed Phase 1 subplan
are written, and the bounded Claude reviews converge.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Generalized-SV governed program safely launch a fresh-agent anti-drift package that freezes inherited authority and target boundaries before any implementation or promotion work begins? |
| Baseline/comparator | restart memo, generalized-SV testing specification, prior-mean amendment result, native dense reference result, and the new governed package artifacts. |
| Primary criterion | The launch package is coherent, locally checked, reviewed, and explicit about row identity, target identity, truth/test-point identity, oracle/evaluator separation, and precursor-versus-promotion boundaries. |
| Veto diagnostics | wrong target identity, actual-SV/generalized-SV confusion, KSC surrogate promoted as generalized-SV, native reference and source-row evaluator blended, wrong truth/test point, missing source-scope evaluator while claiming promotion, or phase advance without review. |
| Explanatory diagnostics | artifact existence, keyword/anchor coverage, authority-order wording, and review disagreement notes. |
| Not concluded | No same-target SGQF admission, no source-row evaluator execution authority, no score admission, no HMC readiness, no production generalized-SV readiness, and no leaderboard/source-row promotion. |
| Artifact | reviewed launch package, Phase 0 result, and refreshed Phase 1 subplan. |

## Forbidden Claims/Actions

- Do not claim the source-row SGQF evaluator is already admitted.
- Do not claim the native dense reference itself executes the benchmark row.
- Do not treat KSC or actual-SV evidence as generalized-SV same-target
  evidence.
- Do not change the truth/test-point convention.
- Do not run implementation, runtime, benchmark, leaderboard, score, gradient,
  HMC, GPU/CUDA, package/network, release, CI, or default-policy commands.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if:

- the restart memo receives Claude `VERDICT: AGREE`;
- the master program receives Claude `VERDICT: AGREE`;
- the target / truth / source-scope contract receives Claude `VERDICT: AGREE`;
- the visible runbook receives Claude `VERDICT: AGREE`;
- this Phase 0 subplan receives Claude `VERDICT: AGREE`;
- the Phase 0 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 1 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger and Claude review ledger are updated for Phase 0 closeout;
- the execution ledger records Phase 0 as reviewed closed rather than merely
  locally prepared.

## Stop Conditions

- Any launch artifact contradicts the row identity or truth/test-point contract.
- A launch artifact blends the native dense oracle with the source-row
  evaluator.
- A launch artifact silently upgrades precursor evidence into admission
  evidence.
- Local document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require runtime, benchmark, GPU/CUDA, package/network,
  release, CI, default-policy, destructive git/filesystem, or unrelated dirty
  worktree changes.

## End-Of-Phase Requirements

1. Run the required local document checks.
2. Review the launch package with bounded read-only Claude prompts.
3. Write the Phase 0 result.
4. Refresh the Phase 1 subplan.
5. Record launch and Phase 0 review outcomes in the execution ledger and Claude
   review ledger.
