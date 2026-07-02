# Phase 4 Subplan: Short-Prefix Same-Target Value Gate

Date: 2026-06-29

## Status

`REVIEWED_BLOCKER_ONLY_SUBPLAN_CLOSED`

## Phase Objective

Use the native generalized-SV dense reference as the promotion oracle for a
short-prefix same-target value gate, deciding whether any Generalized-SV SGQF
route remains blocked, precursor-only, or value-admitted on a reviewed scope.

## Entry Conditions Inherited From Previous Phase

- Phase 3 has reviewed and classified the current SGQF source-row route.
- The active benchmark row remains
  `zhao_cui_generalized_sv_synthetic_from_estimated_values`.
- The native generalized-SV dense raw-y reference remains the promotion oracle,
  not the source-row evaluator.
- Phase 4 is executable only if Phase 3 identifies a reviewed precursor or
  candidate route that can be compared against the oracle on a short-prefix
  same-target scope without changing target identity.
- If Phase 3 closes as `BLOCKED_PENDING_SOURCE_SCOPE_EVALUATOR` with no reviewed
  precursor route suitable for short-prefix oracle agreement, Phase 4 must write
  a blocker-only result and must not run a same-target value gate.

## Required Artifacts

Executable-path artifacts if Phase 3 unlocks a reviewed precursor route:

- Phase 4 result:
  `docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-result-2026-06-29.md`
- Refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-generalized-sv-phase5-source-row-evaluator-wiring-subplan-2026-06-29.md`
- Native dense-reference implementation/result:
  `bayesfilter/highdim/native_generalized_sv.py`
  `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md`
- Reviewed precursor-route evidence from Phase 3.

Blocker-path artifacts if Phase 3 leaves the route blocked:

- Phase 4 blocker result:
  `docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-result-2026-06-29.md`
- Stop handoff update or final blocked closeout handoff if Phase 4 cannot safely
  refresh an executable Phase 5.

## Required Checks/Tests/Reviews

Allowed Phase 4 actions depend on the Phase 3 result.

If Phase 3 leaves no reviewed precursor route, allowed local checks are
blocker-only document checks:

```bash
test -f docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-result-2026-06-29.md
git diff --check -- docs/plans/bayesfilter-generalized-sv*.md
```

If Phase 3 unlocks a reviewed precursor route, Phase 4 must be refreshed with
an exact runtime plan, evidence contract, and authorized checks before any
runtime may begin.

Required read-only Claude reviews:

- Phase 4 result or blocker result,
- refreshed Phase 5 subplan or stop handoff, depending on the Phase 4 outcome.

No runtime, benchmark, leaderboard mutation, score, derivative, HMC, GPU/CUDA,
package/network, release, CI, or default-policy command is authorized from this
draft subplan alone.

## Skeptical Plan Audit

| Risk Checked | Phase 4 Control |
| --- | --- |
| Wrong baseline | Phase 4 uses the native dense raw-y reference as oracle only after Phase 3 identifies a reviewed candidate route suitable for comparison. |
| Proxy metric promoted | Finite execution or availability of a precursor route is not admission; Phase 4 must still preserve route-class and scope-limited conclusions. |
| Missing stop condition | If no reviewed precursor route exists, Phase 4 closes blocker-only rather than pretending an oracle-agreement gate occurred. |
| Unfair comparison | No transformed, KSC, or augmented-noise route may be compared against the native oracle and called same-target unless Phase 3 explicitly justifies that identity claim. |
| Hidden assumption | Phase 4 does not assume the source-row evaluator exists merely because the oracle exists. |
| Stale context | Phase 4 inherits the reviewed Phase 3 classification and may not widen scope without a refreshed reviewed subplan. |
| Environment mismatch | This draft authorizes no runtime. Any executable Phase 4 must be refreshed first. |
| Artifact-answer mismatch | A blocker-only outcome is valid if the prerequisite reviewed precursor route is missing. |

Audit status: passed if Phase 4 either stays blocker-only honestly or is
refreshed into an exact reviewed executable gate before any runtime.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a reviewed precursor or candidate route that can legitimately enter a short-prefix same-target value gate against the native dense oracle, or does the governed program remain blocked at this stage? |
| Baseline/comparator | reviewed Phase 3 route classification and the native generalized-SV dense oracle. |
| Primary criterion | Phase 4 either records a blocker-only closeout because no executable reviewed precursor route exists, or refreshes into a narrower executable gate with exact runtime authority before any value comparison is attempted. |
| Veto diagnostics | treating a missing source-row evaluator as present, promoting precursor existence as admission, blending oracle and evaluator, or widening into runtime without a refreshed reviewed subplan. |
| Explanatory diagnostics | Phase 3 route-class notes, oracle references, and blocker rationale. |
| Not concluded | No same-target value pass from this draft alone, no source-row evaluator admission, no score admission, no HMC readiness, no production readiness, and no leaderboard promotion. |
| Artifact | reviewed Phase 4 result/blocker result and refreshed Phase 5 subplan or stop handoff. |

## Forbidden Claims/Actions

- Do not claim a Phase 4 same-target value pass unless an executable reviewed
  Phase 4 subplan is first written and approved.
- Do not treat a blocked Phase 3 route as if it had passed into executable Phase
  4.
- Do not run runtime, benchmark, evaluator, score, derivative, HMC, GPU/CUDA,
  package/network, release, CI, or default-policy commands from this draft.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if:

- Phase 4 writes a truthful reviewed result or blocker result;
- Claude reviews the Phase 4 outcome artifact with `VERDICT: AGREE`;
- if executable, the refreshed Phase 5 subplan receives Claude
  `VERDICT: AGREE`;
- if blocked, the reviewed stop handoff or final blocked closeout is updated
  instead of forcing a Phase 5 advance.

## Stop Conditions

- Phase 3 leaves no reviewed precursor route suitable for short-prefix
  oracle-agreement work.
- Any purported candidate route changes target identity or comparator family.
- Local document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require runtime or implementation authority not yet reviewed.

## End-Of-Phase Requirements

1. Read the reviewed Phase 3 classification result.
2. Decide whether Phase 4 is blocker-only or requires an executable refreshed
   subplan.
3. Write the Phase 4 result/blocker result.
4. Refresh Phase 5 or the stop handoff, depending on the outcome.
5. Review the Phase 4 outcome artifact and the next reviewed handoff artifact.
6. Update the execution ledger and Claude review ledger.
