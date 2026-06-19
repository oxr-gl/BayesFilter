# P77 Phase 3 Result: Implementation Surface For Budgeted Training

metadata_date: 2026-06-19
status: PHASE3_CLAUDE_AGREE_READY_FOR_PHASE4_MECHANICS_SMOKE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Summary

Phase 3 implemented the scoped P77 runner/test surface authorized by the
reviewed P77 governance patch.  The implementation is limited to:

- `scripts/p77_budgeted_corrected_metric_training.py`;
- `tests/highdim/test_p77_budgeted_corrected_metric_training.py`.

Phase 3 did not run a training-evidence command.  It did not run the
`1024 x 40` proper budget, use GPU/CUDA, use network, install packages, change
defaults, launch detached agents, or take destructive git/filesystem actions.

## Governance Patch

The user directed that implementation-code edits should not require separate
human approval when the runbook and Claude review already govern the scoped
phase.  P77 was patched accordingly:

- scoped code edits are allowed when named in a Claude-reviewed subplan;
- edits must stay within the named files and behavior surface;
- Codex must execute visibly in this session;
- focused local checks must be run and recorded;
- training-evidence runs, including `1024 x 40`, still require a separate
  reviewed subplan and explicit approval;
- GPU/CUDA, network/package operations, default changes, destructive actions,
  detached agents, large diagnostics, and post-result criterion changes remain
  human-required stops.

Claude reviewed this governance patch in
`p77-governance-phase3-readiness-r1` and returned `VERDICT: AGREE`.

## Implementation Surface

The P77 runner is an opt-in surface with CPU-only defaults:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p77_budgeted_corrected_metric_training.py ...
```

It reuses the P76 UKF-frame context and corrected-metric surfaces, while adding
P77-specific manifests and gates:

- \(P_\theta\) parameter count manifest, including rank, degree, basis counts,
  trainable mask, and recompute rule;
- runtime trainable-variable count when a trainer is constructed;
- \(20P_\theta\) hard evidence gate and budget arithmetic;
- `N_train`, `N_train_over_P_theta`, and minimum-batch arithmetic, including
  \(P_\theta=1656\), minimum 33120, and preferred first proper budget 40960;
- predeclared learning rate candidates \(\{10^{-4},3\cdot10^{-4},10^{-3}\}\);
- batch count fields for mechanics smokes and later proper diagnostics;
- corrected validation CE for the untrained UKF baseline and trained
  candidate;
- replay corrected CE for both candidates;
- audit exclusion and validation-only selection fields;
- failed historical route fence for random, calibrated-constant, and
  source-prefit routes;
- nonclaims for source-faithfulness, lower-gate repair, HMC readiness,
  scaling, and default policy.

The runner exposes an `--evidence-run` flag.  If `--evidence-run` is supplied
and \(N_{\rm train}<20P_\theta\), the runner fails closed before context
construction, optimizer construction, or training.  Without `--evidence-run`,
under-budget commands are labelled as non-evidence mechanics smokes.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Can P77 expose a scoped runner/test surface that enforces the Phase 2 budget/tuning contract before any evidence run? |
| Exact baseline/comparator | UKF-initialized untrained TT candidate evaluated with corrected validation/replay CE under the same roles as trained candidates. |
| Primary criterion | Passed locally pending Claude review: the implementation records \(P_\theta\), budget gates, fresh-sample counts, learning-rate protocol, corrected validation/replay metrics, untrained UKF baseline, failed-route fences, and nonclaims. |
| Veto diagnostics | No code edits outside the scoped P77 runner/test surface; no training-evidence command; no default change; under-budget evidence requests fail closed; audit tuning is excluded; failed routes are fenced; focused tests pass. |
| Explanatory only | Mechanics-smoke command shape, runtime estimates, P76 runner reuse details, and TensorFlow Probability deprecation warnings during test import. |
| What will not be concluded | No training improvement, no proper evidence run, no final hyperparameter selection, no lower-gate repair, no validation/HMC readiness, no scaling. |
| Artifact preserving result | This Phase 3 result, scoped runner/test diff, and Phase 4 mechanics-smoke subplan. |

## Local Checks

Governance/readiness review:

- `p77-governance-phase3-readiness-r1`: `VERDICT: AGREE`.

Focused implementation checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p77_budgeted_corrected_metric_training.py
```

Results:

- compileall passed;
- pytest passed: `7 passed, 2 warnings`;
- warnings were TensorFlow Probability `distutils` deprecation warnings, not
  P77 failures.

Source/documentation checks:

```bash
rg -n "PHASE2|P_theta|1656|33120|40960|learning-rate|validation-only|audit exclusion|failed historical routes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md
rg -n "bounded_ukf_minibatch_pilot_payload|generated_corrected_metric_diagnostic_payload|P76CorrectedHeldoutMetricBatch|corrected_heldout_density_metric|train_step|make_adam_optimizer" scripts/p76_bounded_ukf_minibatch_pilot.py scripts/p76_generated_corrected_metric_diagnostic.py bayesfilter/highdim/stochastic_density_training.py
rg -n "P_theta|parameter_count|rank|degree|basis|trainable_mask|recompute|1656|33120|40960|20P|budget|evidence|non_evidence|mechanics" scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
rg -n "learning_rate|batch_count|batches|validation|selection_protocol|audit_exclusion|replay|untrained_ukf|comparator|corrected_validation|random_initialization|calibrated_constant|source_route_prefit" scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
rg -n "P75_INIT_MODES|compare_init_modes|source_guided_prefit|source-guided-prefit|\"random\"" scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
git diff --check -- scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
```

Results:

- Phase 2/Phase 3 prerequisite coverage checks passed.
- P76 surface-symbol checks passed.
- P77 runner/test manifest and tuning coverage checks passed.
- Failed-route live-name grep returned no matches after cleaning up the test
  literals.
- `git diff --check` passed for the scoped implementation files.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 3 pending Claude review | Local implementation checks pass | No Phase 3 veto triggered | The runner has not been exercised against the real target context in this phase | Claude review Phase 3 result/diff and Phase 4 non-evidence smoke subplan | No training improvement, no proper evidence run, no lower-gate repair, no validation/HMC readiness |

## Phase 4 Handoff

Phase 4 should run a tiny CPU-only mechanics smoke using the new P77 runner
without `--evidence-run`, with under-budget output explicitly labelled
non-evidence.  Phase 4 must not run `1024 x 40`, must not use GPU/CUDA, and
must not use the smoke to tune, select, promote, or claim training success.

Claude execution review:

- `p77-phase3-execution-review-r1`: `VERDICT: AGREE`.
- Claude agreed Phase 3 may close and Phase 4 may proceed under the reviewed
  tiny CPU-only non-evidence smoke subplan.
