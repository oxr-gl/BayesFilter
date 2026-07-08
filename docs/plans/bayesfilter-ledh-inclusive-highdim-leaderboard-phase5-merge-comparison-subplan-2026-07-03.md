# Phase 5 Subplan: Merge And Cross-Algorithm Comparison

Date: 2026-07-03

Status: `DRAFT_READY_AFTER_PHASE4_VALUE_ONLY`

## Phase Objective

Merge LEDH row evidence into a new highdim leaderboard artifact and compare
LEDH to existing algorithms without changing the meaning of baseline rows.

Default comparator mode:
`frozen_non_ledh_baseline_plus_fresh_ledh`. In this mode, value and score status
may be compared by row target, but runtime cross-ranking between LEDH and
non-LEDH rows is forbidden because the non-LEDH rows were not rerun under the
same GPU/XLA/TF32 harness.

## Entry Conditions Inherited From Previous Phase

- Phase 4 raw LEDH value artifacts exist for all admitted rows.
- `benchmark_lgssm_exact_oracle_m3_T50` passed same-target value-only at
  `N=10000`; its score remains blocked.
- `zhao_cui_spatial_sir_austria_j9_T20` passed fixed-row value-only at
  `N=10000`; its score remains blocked.
- Parameterized SIR remains a scoped component row only.
- Actual SV, KSC SV, predator-prey, and generalized SV remain blocked until
  reviewed same-target LEDH adapters exist.
- Existing non-LEDH baseline artifact remains frozen.

## Required Artifacts

- Merged JSON:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`.
- Merged Markdown:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md`.
- Phase 5 result:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-result-2026-07-03.md`.
- Updated Phase 6 subplan.

## Required Checks, Tests, Reviews

- JSON schema/content check.
- Row count check: every model row has all intended algorithms or a direct
  blocked status.
- Compare row statuses, values, MCSE, score status, runtime, and device status.
- For LGSSM, merge the per-time average log likelihood from the same-target
  value artifact because the frozen baseline reports the per-time average.
- For SIR, merge the total log likelihood value from the fixed-row value
  artifact and mark the row value-only.
- Provenance check: frozen non-LEDH rows and fresh LEDH rows are labeled
  separately; runtime ranking is disabled unless all algorithms were rerun under
  one reviewed harness.
- Claude review of merged artifact claim boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the merged leaderboard compare LEDH with the other algorithms on every row while preserving target and score status? |
| Baseline/comparator | July 3 non-LEDH highdim leaderboard plus Phase 4 LEDH value artifacts. |
| Primary pass criterion | Merged artifact exists and has no hidden missing LEDH rows, no unsupported score rows, no baseline mutation, explicit frozen-vs-fresh provenance, and value-only rows labeled directly. |
| Veto diagnostics | Missing row; hidden blocked row; Contract E LGSSM fixture used as leaderboard score evidence; value-only row ranked as score-ready; scoped row ranked as full row; baseline row changed without recorded reason; runtime cross-ranking in frozen-baseline mode. |
| Explanatory diagnostics | Runtime and MCSE comparisons. |
| Not concluded | No posterior correctness, no HMC readiness, no broad superiority claim. |
| Artifact | Merged JSON/MD and Phase 5 result. |

## Forbidden Claims And Actions

- Do not overwrite the July 3 non-LEDH artifact.
- Do not rank rows whose targets differ.
- Do not runtime-rank frozen non-LEDH rows against fresh LEDH GPU/XLA rows.
- Do not call MCSE-stable value evidence score evidence.
- Do not merge the Contract E LGSSM route diagnostic as the
  `benchmark_lgssm_exact_oracle_m3_T50` score.
- Do not describe fixed SIR value evidence as exact nonlinear likelihood
  correctness.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if:

- merged artifact passes content checks;
- frozen-vs-fresh provenance is explicit;
- every requested row appears as full, scoped, or blocked;
- Claude review agrees or material issues are patched;
- all nonclaims are direct and plain.

## Stop Conditions

- Merged artifact cannot preserve row target distinctions.
- LEDH artifacts and baseline row IDs cannot be reconciled.
- Claude review finds a material unsupported claim after five repair rounds.
