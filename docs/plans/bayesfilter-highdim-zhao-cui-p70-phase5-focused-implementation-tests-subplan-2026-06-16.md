# P70 Phase 5 Subplan: Focused Implementation And Unit Tests

metadata_date: 2026-06-16
status: READY_AFTER_PHASE4_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement the Phase 4 fixed fitting design with narrow code edits and focused
unit tests.  The implementation must replace the P70 source-route fixed fit's
constant-path one-sweep behavior with a seeded-channel initialization,
alternating multi-sweep policy, row-adequacy gate, channel-activity predicate,
and recorded fitting thresholds.

Phase 5 does not run repaired P69/P70 diagnostics, validation ladders,
GPU/HMC commands, or long experiments.

## Entry Conditions Inherited From Phase 4

Phase 5 may begin only after Phase 4 produces:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase4-nondegenerate-fitting-design-result-2026-06-16.md`;
- Claude `VERDICT: AGREE` for the Phase 4 result and this subplan;
- initialization rule `fixed_hmc_seeded_channel_paths_v1`;
- \(\varepsilon_{\rm init}=10^{-6}\);
- canonical alternating sweep order `(0, 1, ..., D-1, D-1, ..., 0)`;
- `max_sweeps=4`;
- row thresholds
  \(n_{\rm hard}=\max\{4,\lceil D/4\rceil,(p+1)R^2\}\) and
  \(n_{\rm preferred}=\max\{D,2(p+1)R^2\}\);
- ridge and condition thresholds
  \(\rho=10^{-10}\), \(\kappa_{\rm warn}=10^{10}\),
  \(\kappa_{\rm veto}=10^{14}\);
- channel thresholds \(\epsilon_{\rm chan,abs}=10^{-12}\),
  \(\epsilon_{\rm chan,rel}=10^{-8}\), and
  \(b_{\min}=\max\{1,\lceil0.25(D-1)\rceil\}\);
- normalizer thresholds \(\epsilon_{\rm def}=10^{-14}\),
  \(\rho_{\rm fitmass}=10^{-6}\), and \(|F_t^B|\le10^6\);
- holdout/replay normalized residual veto \(10\);
- exact implementation and test surface list from Phase 4.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-result-2026-06-16.md`.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.
- Refreshed Phase 6 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-subplan-2026-06-16.md`.
- Implementation diff limited to the surfaces below.

## Authorized Implementation Surfaces

Phase 5 may edit only:

- `bayesfilter/highdim/source_route.py`;
- `bayesfilter/highdim/fitting.py` for repeated-axis update-schedule
  validation and manifest/diagnostic payload support;
- `bayesfilter/highdim/__init__.py` only if a new helper must be public;
- `tests/highdim/test_fixed_branch_fit.py`;
- a new focused P70 test file under `tests/highdim/`, if needed.

Any broader surface requires a blocker note and Claude review before editing.

## Required Checks/Tests/Reviews

Local pre-edit checks:

```bash
rg -n "_source_route_constant_path_initial_cores|FixedTTFitConfig|max_sweeps=1|sweep_order=tuple\\(range|P65_FIXED_BRANCH_INITIALIZATION_RULE" bayesfilter/highdim/source_route.py
rg -n "FixedTTFitter|holdout_residual_veto|condition_number_veto|branch_hash_changes|sweep_order" tests/highdim/test_fixed_branch_fit.py
rg -n "sorted\\(config\\.sweep_order\\)|sweep_order" bayesfilter/highdim/fitting.py
```

Focused tests after implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/fitting.py tests/highdim/test_fixed_branch_fit.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py
```

If a new P70 test file is added, include it in both commands.  CPU-only is
intentional for these unit tests and must be recorded in the result artifact.

Local formatting check:

```bash
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/fitting.py bayesfilter/highdim/__init__.py tests/highdim/test_fixed_branch_fit.py tests/highdim
```

Claude review:

- Review the focused implementation diff and Phase 5 result.
- Check that seeded-channel paths are actual core entries, not diagnostic-only
  labels.
- Check that the old constant-path one-sweep route is no longer the P70
  default.
- Check that tests cover row adequacy, channel activity, manifest/diagnostic
  thresholds, deterministic replay, and forbidden shortcuts.
- Check source-governance language: new seeded initialization is
  `fixed_hmc_adaptation`, not `source_faithful`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the code now implement the Phase 4 fixed fitting rule and expose focused unit-test evidence for nondegenerate channel paths, multi-sweep policy, and admissibility predicates? |
| Baseline/comparator | Current P59/P69 one-sweep constant-path source-route fit and generic `FixedTTFitter` support for sweeps, manifests, holdout, and condition vetoes. |
| Primary criterion | Focused tests pass and implementation diff shows real seeded-channel initial cores, canonical alternating sweeps, row-adequacy gate, channel-activity predicate, and threshold recording on the authorized surfaces. |
| Veto diagnostics | Diagnostic-only channel labels; thresholds changed from Phase 4; low/high closeness gate; UKF used as target; source-faithful overclaim; broad unrelated edits; repaired diagnostic run launched. |
| Explanatory diagnostics | Unit-test branch hashes, channel scores, fit status, condition summaries, manifest payloads, row-adequacy blockers. |
| Not concluded | No repaired diagnostic pass, no d18 validation, no rank/degree promotion, no HMC readiness, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 5 result, code diff, test output, and refreshed Phase 6 subplan. |

## Required Implementation Content

Phase 5 must implement:

- seeded-channel initializer for source-route fixed TT cores;
- P70 fit policy constants or local configuration values matching Phase 4;
- row-adequacy predicate before fitting;
- canonical alternating sweep order and `max_sweeps=4` for the P70 fixed route;
- generic fitter validation that permits exactly the canonical P70
  repeated-axis update schedule and all legacy permutation schedules, while
  rejecting malformed repeated schedules;
- channel-activity score helper and branch diagnostic payload;
- normalizer/admissibility threshold payloads needed by Phase 6 diagnostics;
- branch identity or manifest fields for initialization rule, sweep policy,
  row thresholds, ridge, condition thresholds, and channel thresholds.

Phase 5 may preserve legacy constant-path helpers for historical tests or
non-P70 routes, but the P70 source-route path must not silently keep
`fixed_hmc_constant_path_weighted_mean` with `max_sweeps=1`.

## Required Focused Tests

Tests must cover:

- seeded initializer preserves the positive constant path and creates nonzero
  extra-channel paths for \(R>1\);
- initial extra-channel incident scores are nonzero;
- P70 fit configuration records canonical alternating sweep order and
  `max_sweeps=4`;
- generic fitter accepts the canonical repeated-axis schedule;
- generic fitter continues to accept legacy permutation schedules;
- generic fitter rejects malformed repeated schedules, including schedules
  with arbitrary extra repeats, missing axes, out-of-range axes, empty order,
  or a repeated-axis pattern different from the canonical P70 pattern;
- manifest payloads and branch hashes preserve the full canonical repeated-axis
  schedule;
- row-adequacy failure blocks below \(n_{\rm hard}\);
- all-constant-path rank-2 cores fail the channel-activity predicate;
- normalizer predicate rejects defensive-only or nonfinite summaries if the
  predicate is implemented in Phase 5;
- deterministic replay preserves branch hash for same fixed inputs and changes
  branch hash when initialization rule or sweep order changes;
- old one-sweep constant-path behavior is explicitly legacy or historical, not
  the P70 default.

## Forbidden Claims/Actions

- Do not run P69 Phase 5c or any repaired diagnostic.
- Do not run Phase 6/7 ladders.
- Do not run GPU/HMC commands.
- Do not edit p50.
- Do not broaden implementation surfaces without a blocker and review.
- Do not change Phase 4 thresholds after seeing test or diagnostic output.
- Do not claim the bug is fixed until Phase 6 evidence exists.
- Do not claim source-faithful implementation for seeded-channel initialization
  or UKF-guided branch construction.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only if Phase 5 produces:

- focused implementation result with test output;
- code diff limited to authorized surfaces or a reviewed expansion note;
- branch manifests/diagnostics exposing the Phase 4 thresholds;
- no repaired diagnostic or ladder run in Phase 5;
- refreshed Phase 6 diagnostic subplan with explicit evidence contract and
  user approval requirement before execution;
- Claude `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- the seeded initializer cannot be implemented without broad code movement;
- the P70 source-route path cannot be isolated from legacy constant-path
  behavior;
- focused tests require the long P69 diagnostic or d18 validation to pass;
- row-adequacy or channel-activity predicates require thresholds not frozen in
  Phase 4;
- TensorFlow unit tests fail for reasons not repairable within the authorized
  surfaces;
- Claude and Codex do not converge after five material review rounds.

## Skeptical Plan Audit

The main Phase 5 risk is accidentally changing only labels or diagnostics while
the actual fitted core tuple remains constant-path and one-sweep.  The tests
must inspect the initialized cores and the realized configuration directly.
The second risk is overcorrecting into broad algorithmic rewrites.  Phase 5 is
therefore limited to source-route fitting helpers, manifest/diagnostic support
only if needed, and focused tests.
