# Phase 0 Result: Launch Boundary Freeze

Date: 2026-07-03

Status: `PASS_PHASE0_BASELINE_FREEZE`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 0 passes. The current baseline is frozen before runner edits. |
| Primary criterion status | Passed: retained-grid demotion markers, current SIR leaderboard status, and P91 fixed-variant evidence paths were recorded. |
| Veto diagnostic status | Passed: no retained-grid production admission was found; P91 evidence is scoped local complete-data/component evidence; no full observed-data/filtering claim is admitted. |
| Main uncertainty | The current leaderboard still reports the Zhao-Cui SIR main cell as blocked/status-only. Phase 1/2 must decide exactly which fixed-variant scoped quantity can be wired without overclaiming. |
| Next justified action | Start Phase 1 fixed-variant entrypoint inventory. |
| What is not being concluded | No runner implementation correctness, no regenerated leaderboard, no exact likelihood proof, no posterior correctness, no full observed-data/filtering score identity, and no new GPU readiness claim. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What is the current baseline before fixed-variant leaderboard wiring begins? |
| Baseline/comparator | Current route-boundary code/docs, July 2 highdim leaderboard artifacts, and P91 fixed-variant SIR artifacts. |
| Primary criterion | Passed: this result records route/admission status, affected row ids, and P91 evidence paths. |
| Veto diagnostics | Passed: retained-grid demotion is present, P91 evidence exists, the stale current row is noticed, and no unreviewed full-filtering production claim is made. |
| Explanatory diagnostics | Dirty worktree context, current blocked leaderboard status, and P91 scoped evidence status. |
| Not concluded | No implementation correctness, regenerated leaderboard, full filtering readiness, or GPU readiness. |
| Artifact | This Phase 0 result and the visible execution ledger. |

## Frozen Baseline

Route boundary:

- `AGENTS.md` records that the generic all-axes multistate retained-grid route
  is diagnostic/historical only for Zhao-Cui leaderboard and production work.
- `bayesfilter/highdim/filtering.py` defines
  `MULTISTATE_RETAINED_GRID_ROUTE_ROLE =
  "diagnostic_historical_retained_grid"`.
- `bayesfilter/highdim/filtering.py` defines
  `MULTISTATE_RETAINED_GRID_LEADERBOARD_ADMISSION =
  "not_admitted_for_production_leaderboard_use_fixed_variant_zhao_cui"`.
- `bayesfilter/highdim/filtering.py` defines
  `FIXED_VARIANT_ZHAO_CUI_PRODUCTION_ROUTE =
  "fixed_variant_zhao_cui_source_route"`.

Current leaderboard baseline:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md`
  reports `zhao_cui_spatial_sir_austria_j9_T20` /
  `zhao_cui_scalar_or_multistate` as `blocked_or_status_only`.
- The current reason says P91 closes only scoped local complete-data SIR d18
  component evidence while the full observed-data/filtering evaluator remains
  blocked by preserved source-route derivative/evaluator gaps.
- The July 2 JSON includes P91 sidecar evidence under
  `scope = local_complete_data_zhao_cui_sir_d18_component` and preserves
  `not full observed-data/filtering score identity`.

P91 evidence present:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`

P91 final decision:

- Status is `P91_SCOPED_PRODUCTION_READY_CLOSED`.
- Promoted scope is the highdim API and local complete-data component route
  conditioned on fixed latent state and observation paths.
- Preserved nonclaims include no exact likelihood correctness, no posterior
  correctness, no full observed-data/filtering score identity, and no
  universal GPU superiority.

## Local Checks

Commands:

```bash
git diff --check -- docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-*.md AGENTS.md bayesfilter/highdim/filtering.py tests/test_highdim_zhao_cui_leaderboard_phase1.py
rg -n "zhao_cui|Zhao|sir|austria|retained|fixed_variant|score" docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md
ls docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-result-2026-06-29.md docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-result-2026-06-29.md docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-result-2026-06-29.md docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md
rg --files tests | rg "phase3_spatial_sir|highdim_zhao_cui|p91|two_lane_highdim"
rg -n "retained-grid|retained_grid|diagnostic/historical|diagnostic_historical|fixed_variant_zhao_cui|production route|leaderboard" AGENTS.md bayesfilter/highdim/filtering.py tests/test_highdim_zhao_cui_leaderboard_phase1.py tests/highdim/test_p91_score_identity.py tests/highdim/test_p91_gpu_xla_local_target.py
rg -n "Status:|PASS_|SCOPED|full_observed|local complete|GPU/XLA|HMC|benchmark" docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-result-2026-06-29.md docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-result-2026-06-29.md docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json
```

Outcome:

- `git diff --check`: passed with no output.
- Leaderboard `rg`: passed and found the current SIR blocked/status-only row.
- P91 artifact `ls`: passed; all named artifacts exist.
- Test-file discovery: passed and found current P91 and highdim leaderboard
  tests.
- Route-marker `rg`: passed and found the demotion constants and governance
  text.
- P91 status `rg`: passed and found the scoped production decision plus Phase
  5/6/7 status markers.
- JSON manifest formatting check: passed.

Corrected stale check:

- A first-pass `rg` command included the stale path
  `tests/highdim/test_phase3_spatial_sir`; it failed with exit code 2.
- The command was corrected to discover real test paths first and then check
  `tests/test_highdim_zhao_cui_leaderboard_phase1.py`,
  `tests/highdim/test_p91_score_identity.py`, and
  `tests/highdim/test_p91_gpu_xla_local_target.py`.
- This was a stale local-check path issue, not an algorithmic blocker.

## Phase 1 Handoff

Phase 1 may start because:

- retained-grid demotion markers are present;
- current leaderboard SIR Zhao-Cui row status is recorded;
- P91 evidence paths are present;
- the scoped/nonclaim boundary is explicit;
- no material baseline ambiguity requires human direction.

Phase 1 must classify the fixed-variant callable quantity before any
leaderboard row admission decision is made.
