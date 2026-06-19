# P70 Phase 5 Result: Focused Implementation And Unit Tests

metadata_date: 2026-06-16
status: PHASE5_PASSED_SPLIT_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 5 implemented the Phase 4 fixed fitting design on the authorized
surfaces and verified it with focused CPU-only unit tests.  No P69/P70 repaired
diagnostic, validation ladder, GPU command, HMC command, or p50 edit was run.

The implementation is not yet evidence that the original bug is fixed.  It is
evidence that the repaired fixed fitting machinery exists and is unit-tested
before Phase 6 diagnostic planning.

## Implementation Summary

Edited surfaces:

- `bayesfilter/highdim/fitting.py`;
- `bayesfilter/highdim/source_route.py`;
- `tests/highdim/test_fixed_branch_fit.py`.

No edit was needed in `bayesfilter/highdim/__init__.py`.

Implemented behavior:

- `FixedTTFitter.fit` now records the supplied initialization rule in the
  branch manifest and diagnostics.
- `FixedTTFitter` validation now accepts:
  - legacy permutation schedules of length \(D\);
  - the canonical P70 repeated-axis schedule
    `(0, 1, ..., D-1, D-1, ..., 0)`.
- Malformed repeated schedules remain invalid.
- The source-route fixed-TTSIRT helper now uses:
  - `fixed_hmc_seeded_channel_paths_v1`;
  - \(\varepsilon_{\rm init}=10^{-6}\);
  - canonical alternating update order;
  - `max_sweeps=4`;
  - ridge \(10^{-10}\);
  - condition warning \(10^{10}\);
  - condition veto \(10^{14}\);
  - hard/preferred row-adequacy diagnostics;
  - stored-gauge channel-activity diagnostics;
  - Phase 4 normalizer and holdout/replay threshold payloads.
- Legacy constant-path initialization remains available as an explicitly named
  helper and historical baseline.

## Source-Governance Classification

| Operation | Classification | Note |
| --- | --- | --- |
| Zhao--Cui adjacent target values passed to the fixed fit | `source_faithful` mathematical route component | Target semantics were not changed in Phase 5. |
| Seeded-channel initialization, canonical repeated-axis sweep, row adequacy, and channel-activity predicates | `fixed_hmc_adaptation` | These are BayesFilter fixed-branch safeguards from Phase 4, not Zhao--Cui adaptive parity. |
| Threshold payloads | `fixed_hmc_adaptation` engineering safeguards | The payload explicitly says thresholds are not source-faithful theory or validation evidence. |

## Test And Check Evidence

CPU-only was intentional for Phase 5 unit tests.

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/fitting.py tests/highdim/test_fixed_branch_fit.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/fitting.py bayesfilter/highdim/__init__.py tests/highdim/test_fixed_branch_fit.py tests/highdim
```

Results:

- compileall: passed;
- pytest: `24 passed, 2 warnings in 5.35s`;
- warnings: TensorFlow Probability `distutils` deprecation warnings only;
- `git diff --check`: passed.

Focused tests added or updated:

- seeded initializer preserves the positive constant path and creates nonzero
  extra-channel paths;
- initial extra-channel incident scores are nonzero;
- constant-path rank-2 cores fail the P70 channel-activity predicate;
- row adequacy has hard and preferred tiers;
- P70 policy payload records initialization rule, canonical sweep order,
  thresholds, row adequacy, channel activity, and nonclaims;
- canonical repeated-axis schedule is accepted and recorded;
- legacy permutation schedules remain valid;
- malformed repeated-axis schedules are rejected;
- test helper now preserves an explicitly supplied empty `sweep_order` so the
  empty-order validation path is actually tested.

## Decision Table

| Item | Status |
| --- | --- |
| Primary criterion | Passed locally: focused tests cover real seeded core entries, canonical sweep validation, row/channel predicates, and policy payloads. |
| Veto diagnostics | No repaired diagnostic run, no threshold change after output, no low/high closeness gate, no UKF target, no source-faithful overclaim, no broad unauthorized surface. |
| Main uncertainty | The repaired machinery has not yet been exercised on the P69/P70 diagnostic rows. |
| Next justified action | Review Phase 5 result and refreshed Phase 6 subplan with Claude; after agreement, ask for explicit Phase 6 diagnostic approval. |
| Not concluded | No d18 validation, no rank/degree promotion, no HMC readiness, no adaptive Zhao--Cui parity, no claim that the bug is fixed. |

## Phase 6 Handoff

Phase 6 may start only after Claude returns `VERDICT: AGREE` for this result
and the refreshed Phase 6 subplan.  The original full Phase 5 review prompts
stalled, but the review was successfully split into implementation, focused
test, and Phase 6 gating chunks.  Claude returned `VERDICT: AGREE` on the
implementation and focused-test chunks.  Claude first returned
`VERDICT: REVISE` on the Phase 6 gating chunk because the subplan needed a
terminal diagnostic stop rule and mandatory result-artifact fields; those
repairs were made in the Phase 6 subplan, and Claude returned
`VERDICT: AGREE` on the focused repair review.

Phase 6 diagnostic execution still requires explicit user approval under the
runbook's executable diagnostic gate.

Exact products handed off:

- implemented seeded-channel initialization;
- implemented canonical repeated-axis validation;
- implemented P70 row-adequacy and channel-activity diagnostics;
- implemented P70 threshold payloads;
- focused CPU-only test evidence;
- refreshed Phase 6 subplan.

## Not Concluded

- The P69 Phase 5c diagnostic was not rerun.
- No repaired P70 diagnostic was run.
- No validation ladder was run.
- No GPU/HMC command was run.
- No p50 document or PDF was edited.
- No claim is made that the repaired branch fixes the observed diagnostic bug.
