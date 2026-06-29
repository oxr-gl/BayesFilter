# Generalized-SV Governed Master Program

Date: 2026-06-29

## Status

`DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Program Objective

Establish a fresh, anti-drift governed program for Generalized SV that freezes
row identity, target identity, truth/test-point identity, and precursor-versus-
promotion boundaries before any implementation or benchmark promotion work
begins.

This launch does **not** authorize same-target SGQF admission, analytical-score
admission, HMC readiness, production readiness, or default-policy change for the
Generalized-SV source-row benchmark.

## Inherited State

The inherited Generalized-SV record is now:

- a low-dimensional native generalized-SV dense same-target raw-y reference
  exists and passed its reviewed reference phase;
- the promoted source-paper benchmark row is
  `zhao_cui_generalized_sv_synthetic_from_estimated_values`, governed by the
  reviewed testing specification and source-scope contract;
- the current generalized-SV SGQF path is still a source-scope unlock / precursor
  question, not an admitted same-target source-row evaluator;
- older generalized-SV blocker/equality/ladder artifacts preserve important
  nonclaims and must be treated as historical context rather than automatic
  authority.

## Governing Authority Order

When artifacts disagree, use the following authority order for Generalized-SV
identity and promotion semantics:

1. newest reviewed Generalized-SV reset memo or target/truth/source-scope
   contract produced by this program;
2. newest reviewed Generalized-SV phase result produced by this program;
3. the Generalized-SV testing specification and source-scope contract;
4. the native generalized-SV dense-reference result;
5. older P44/P45/P47/P50/P51 generalized-SV artifacts as historical context only;
6. implementation surfaces, tests, registries, and leaderboard rows.

No lower-ranked artifact may silently override a higher-ranked target statement.

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the Generalized-SV source-row work be advanced under a governed, anti-drift program that freezes the correct row identity and target first, then determines whether any SGQF route can be admitted as a same-target/source-scope evaluator? |
| Baseline/comparator | reviewed reset memo, testing specification, source-scope contract, native dense reference result, and older blocker/equality/ladder artifacts. |
| Primary pass criterion | Each phase writes the required artifact, preserves the target/truth/source-scope contract, passes its veto checks, and advances only after reviewed handoff. |
| Promotion veto diagnostics | wrong target identity, actual-SV and generalized-SV confusion, KSC surrogate promoted as generalized-SV, native reference and source-row evaluator blended, precursor evidence promoted as admission, wrong truth/test point, missing source-scope evaluator, phase advance without review. |
| Explanatory diagnostics | refinement behavior, finite-value checks, runtime/point-count notes, row-status emissions, and review disagreement notes. |
| Not concluded at launch | No same-target SGQF source-row admission, no score admission, no HMC readiness, no production generalized-SV readiness, no leaderboard/source-row promotion. |
| Required artifacts | reset memo, master program, contract, runbook, ledgers, stop handoff, phase subplans/results, and final decision artifact. |

## Anti-Drift Hard Gates And Vetoes

### Hard gates

1. **Target-before-implementation gate**
   - No implementation, test mutation, benchmark mutation, or source-row
     promotion work may begin until the target/truth/source-scope contract phase
     passes.

2. **Same-target-before-promotion gate**
   - No row may move from blocked/precursor to admitted/executed same-target
     status unless a reviewed phase result shows same-target agreement at the
     relevant claim level.

3. **Value-before-score gate**
   - No analytical-score, FD, HMC, or derivative-admission work may begin before
     the same-target value gate passes for the same row/target.

4. **Precursor-is-not-promotion gate**
   - A precursor SGQF route may support engineering unlock work but may not by
     itself promote the source-row SGQF evaluator.

5. **Source-scope-evaluator gate**
   - The native dense reference may serve as the promotion oracle, but it does not
     by itself authorize the source-row evaluator to execute or promote.

6. **Review-before-advance gate**
   - No phase may advance without a reviewed subplan, reviewed result/blocker, and
     refreshed next-phase subplan.

7. **Status-preservation gate**
   - Historical blocked/diagnostic statuses may not be silently upgraded by code,
     tests, registries, or emitted tables.

### Explicit veto tokens

- `WRONG_TARGET_IDENTITY`
- `ACTUAL_SV_AND_GENERALIZED_SV_CONFUSED`
- `KSC_SURROGATE_PROMOTED_AS_GENERALIZED_SV`
- `NATIVE_REFERENCE_AND_ZHAO_CUI_SOURCE_ROW_BLENDED`
- `PRECURSOR_EVIDENCE_PROMOTED_AS_ADMISSION`
- `WRONG_TRUTH_OR_TEST_POINT`
- `SOURCE_SCOPE_EVALUATOR_MISSING`
- `RESET_MEMO_REQUIRED_BEFORE_CONTINUING`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch and inherited-boundary freeze | `docs/plans/bayesfilter-generalized-sv-phase0-launch-boundary-freeze-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase0-launch-boundary-freeze-result-2026-06-29.md` |
| 1 | Reset memo and authority-order freeze | `docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase1-reset-authority-freeze-result-2026-06-29.md` |
| 2 | Target/truth/source-scope contract freeze | `docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-result-2026-06-29.md` |
| 3 | Precursor-route design and classification | `docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-result-2026-06-29.md` |
| 4 | Short-prefix same-target value gate | `docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-result-2026-06-29.md` |
| 5 | Source-row evaluator wiring gate | `docs/plans/bayesfilter-generalized-sv-phase5-source-row-evaluator-wiring-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase5-source-row-evaluator-wiring-result-2026-06-29.md` |
| 6 | Analytical-score / derivative admission gate | `docs/plans/bayesfilter-generalized-sv-phase6-score-derivative-admission-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase6-score-derivative-admission-result-2026-06-29.md` |
| 7 | Benchmark / leaderboard integration gate | `docs/plans/bayesfilter-generalized-sv-phase7-benchmark-leaderboard-integration-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase7-benchmark-leaderboard-integration-result-2026-06-29.md` |
| 8 | Documentation/manuscript reconciliation | `docs/plans/bayesfilter-generalized-sv-phase8-documentation-reconciliation-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase8-documentation-reconciliation-result-2026-06-29.md` |
| 9 | Final decision and stop handoff | `docs/plans/bayesfilter-generalized-sv-phase9-final-decision-stop-handoff-subplan-2026-06-29.md` | `docs/plans/bayesfilter-generalized-sv-phase9-final-decision-stop-handoff-result-2026-06-29.md` |

## Sequential Gate Rule

No phase may execute as promotional work unless all prior promotional gates have
reviewed pass artifacts. If an upstream gate is blocked, downstream phases may
write no-runtime blocker closeouts or a final blocked decision only.

## Claude Review Protocol

Claude is read-only reviewer only. Every Claude prompt must be one-path bounded
by default:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

## Final Handoff Requirement

The final handoff must state:
- exact row status,
- what target was actually admitted or still blocked,
- which comparator family was used,
- what was not concluded,
- and the exact next safe reviewed action.
