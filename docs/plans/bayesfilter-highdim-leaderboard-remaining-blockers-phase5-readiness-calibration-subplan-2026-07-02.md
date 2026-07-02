# Phase 5 Subplan: Batch/GPU/XLA Readiness And Score-At-True Calibration

Date: 2026-07-02

Status: `DRAFT_READY_AFTER_PHASE4_BLOCKERS`

## Phase Objective

Run readiness diagnostics for admitted rows without changing row admission:
batched parity where available, trusted GPU/XLA compile/timing only where
explicitly approved, and score-at-true calibration where simulator/truth
binding exists.

## Entry Conditions Inherited From Previous Phase

- Phase 1 admitted the Zhao-Cui predator-prey row-local value/manual-score
  artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-zhaocui-row-2026-07-02.json`.
- Phase 2 admitted the Zhao-Cui generalized-SV row-local value/manual-score
  artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-zhaocui-row-2026-07-02.json`.
- Phase 3 closed spatial SIR as a full-row theta-binding blocker:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-result-2026-07-02.md`.
- Phase 4 closed predator-prey/generalized-SV UKF as value-only blockers:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-score-cleanup-result-2026-07-02.md`.
- Phase 4 also produced the route-binding dependency used by Phase 5
  readiness classification:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-route-bindings-2026-07-02.json`.
- Phase 5 must not use readiness diagnostics to promote Phase 3 or Phase 4
  blockers into score rows.
- Any GPU/XLA command requires explicit trusted-context approval before
  execution.

## Required Artifacts

- Per-row readiness manifest:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-manifest-2026-07-02.json`.
- Batch parity result or blocker for admitted rows:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-batch-parity-2026-07-02.json`.
- Trusted GPU/XLA result or blocker if approved:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-gpu-xla-readiness-2026-07-02.json`.
- Score-at-true calibration result or precise not-applicable reason:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-score-at-true-2026-07-02.json`.
- Phase 5 result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-calibration-result-2026-07-02.md`
- Refreshed Phase 6 subplan:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-final-regeneration-subplan-2026-07-02.md`.

## Required Checks, Tests, Reviews

- CPU-only manifest/readiness classification check.
- CPU-only batch smoke where available and cheap.
- Trusted GPU probe before any GPU/XLA benchmark, only after explicit approval.
- Score-at-true multi-seed diagnostic under fixed true parameter where
  available.
- Claude read-only review of readiness interpretation.

## Exact Phase 5 Command Surface

CPU-only structural checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m json.tool docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-zhaocui-row-2026-07-02.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m json.tool docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-zhaocui-row-2026-07-02.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m json.tool docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-route-bindings-2026-07-02.json
```

CPU-only admitted-row inventory:

```bash
python -c "import json; paths=['docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-zhaocui-row-2026-07-02.json','docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-zhaocui-row-2026-07-02.json']; print(json.dumps([json.load(open(p)) for p in paths], indent=2, sort_keys=True))"
```

CPU-only readiness-harness discovery:

```bash
rg -n "batch|batched|score_at_true|score-at-true|multi-seed|multiseed|zhao_cui.*predator|zhao_cui.*generalized" bayesfilter docs/benchmarks tests/highdim tests/test_two_lane_highdim_leaderboard_analytical_scores.py
```

Operational classification constraints:

- The Phase 5 readiness manifest is keyed only by the admitted Phase 1 and
  Phase 2 Zhao-Cui row-local artifacts.
- The batch-parity and score-at-true artifacts must also be keyed by admitted
  row-local artifact, with each admitted row assigned exactly one row-level
  status from the closed enums below. Each artifact may include an explanatory
  `overall_summary` field, but no global status may hide a mixed row-level
  outcome.
- The Phase 4 route-binding artifact is used only as a negative-boundary
  cross-check: UKF entries closed as value-only/manual-route-missing blockers
  are non-admitted inputs and must not become Phase 5 readiness targets.
- Any discovered command whose route name, target, or derivative provenance
  cannot be matched to a Phase 1 or Phase 2 admitted row-local artifact must be
  classified as adjacent/wrong-target evidence, not executed for readiness.

Conditional batch-parity execution rule:

- For each admitted row-local artifact independently, if discovery finds an
  exact admitted row-local Zhao-Cui batch-parity harness and the harness is
  cheap/reviewed enough for this phase, Phase 5 must add the exact command to
  this subplan before running it, run it CPU-only unless separately approved
  for GPU, and preserve the row-level output in
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-batch-parity-2026-07-02.json`.
- For each admitted row-local artifact independently, if discovery finds an
  exact admitted row-local batch-parity harness that is not cheap/reviewed
  enough for this phase, Phase 5 must write the row-level status
  `deferred_exact_harness_not_cheap_or_not_reviewed` and name the harness and
  reason it was not run.
- For each admitted row-local artifact independently, if discovery finds only
  adjacent or wrong-target harnesses, Phase 5 must write the row-level status
  `deferred_exact_harness_missing` and name the mismatch.
- For each admitted row-local artifact independently, if discovery finds no
  batch-parity harness at all, Phase 5 must write the row-level status
  `deferred_no_batch_harness_found`.
- Closed batch-parity row-level status enum:
  `executed_pass`, `executed_fail`,
  `deferred_exact_harness_not_cheap_or_not_reviewed`,
  `deferred_exact_harness_missing`, `deferred_no_batch_harness_found`.

Conditional score-at-true execution rule:

- For each admitted row-local artifact independently, if discovery finds an
  exact admitted row-local simulator/truth binding and multi-seed
  score-at-true harness, and the harness is cheap/reviewed enough for this
  phase, Phase 5 must add the exact command to this subplan before running it,
  run it CPU-only unless separately approved for GPU, and preserve mean,
  standard deviation, standard error, seed list, and true parameter in
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-score-at-true-2026-07-02.json`.
- For each admitted row-local artifact independently, if discovery finds an
  exact admitted row-local simulator/truth binding and exact multi-seed
  score-at-true harness that is not cheap/reviewed enough for this phase,
  Phase 5 must write the row-level status
  `deferred_exact_harness_not_cheap_or_not_reviewed` and name the harness and
  reason it was not run.
- For each admitted row-local artifact independently, if discovery finds an
  exact admitted row-local simulator/truth binding but no exact multi-seed
  score-at-true harness, Phase 5 must write the row-level status
  `deferred_exact_multiseed_harness_missing` and name the binding and missing
  harness.
- For each admitted row-local artifact independently, if discovery finds only
  adjacent or wrong-target score-at-true harnesses, Phase 5 must write the
  row-level status `deferred_exact_harness_missing` and name the mismatch.
- For each admitted row-local artifact independently, if discovery finds no
  exact admitted row-local simulator/truth binding, Phase 5 must write the
  row-level status `skipped_binding_unavailable`.
- Closed score-at-true row-level status enum:
  `executed_pass`, `executed_fail`,
  `deferred_exact_harness_not_cheap_or_not_reviewed`,
  `deferred_exact_multiseed_harness_missing`,
  `deferred_exact_harness_missing`, `skipped_binding_unavailable`.

Phase 5 may write not-applicable/blocker readiness manifests without running
new numerical experiments if no cheap reviewed batch/score-at-true harness is
available for the exact admitted row-local routes.

GPU/XLA commands are not preauthorized by this subplan. If Phase 5 needs GPU,
Codex must stop and ask for explicit approval with exact commands, expected
runtime, artifacts, and device-readiness precheck.

## Phase 5 Skeptical Audit / Pre-Mortem

Material risks before execution:

- Readiness promotion drift: timing, batch parity, or score-at-true diagnostics
  could be misread as value/score admission. Phase 5 forbids admission changes.
- Wrong population: Phase 5 must not run readiness on Phase 4 UKF blockers as
  if they were score rows.
- GPU trust mismatch: non-escalated GPU failures are sandbox evidence only, and
  trusted GPU commands require explicit approval.
- Overclaiming score-at-true: score-at-true consistency can support sanity
  wording but cannot prove exact likelihood correctness.
- Hidden runtime: row-local TT routes can be expensive; Phase 5 should prefer
  manifest classification unless a cheap reviewed harness exists.

Audit status for launch: `PASSED_AFTER_CLAUDE_REVIEW_ITERATION_5`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which admitted rows have batch/GPU/XLA readiness and score-at-true consistency evidence, and which readiness checks are not applicable or deferred? |
| Baseline/comparator | Admitted Zhao-Cui row-local artifacts from Phases 1-2; blockers from Phases 3-4 as non-admitted rows. |
| Primary criterion | Readiness evidence or precise not-applicable/blocker status is recorded separately from row admission and does not promote unsupported scientific claims. |
| Veto diagnostics | Untrusted GPU claim; score-at-true treated as exact likelihood proof; failed batch parity hidden; Phase 3/4 blockers promoted by readiness. |
| Explanatory diagnostics | Runtime, compile status, device status, score mean/standard deviation/standard error. |
| Not concluded | Universal GPU superiority, HMC convergence, posterior correctness, release readiness. |
| Artifact | Phase 5 result and readiness/batch/GPU/score-at-true manifests. |

## Forbidden Claims And Actions

- Do not run GPU/XLA without trusted escalation/approval.
- Do not change value/score admission criteria based on readiness results.
- Do not claim score-at-true proves exact likelihood correctness.
- Do not include Phase 4 UKF value-only blockers in score-readiness
  diagnostics.
- Do not rerun full leaderboard regeneration in Phase 5.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 if readiness diagnostics are recorded or precisely
classified as blocked/not-applicable/deferred without altering row-admission
criteria.

## Stop Conditions

Stop if GPU/XLA approval is needed and unavailable, if readiness diagnostics
would require changing criteria after seeing results, or if no exact admitted
row-local route can be matched to the proposed readiness command.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 5 result / close record.
3. Draft or refresh Phase 6 subplan.
4. Review Phase 6 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
