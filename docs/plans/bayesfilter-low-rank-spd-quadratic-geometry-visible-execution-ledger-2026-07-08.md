# Low-Rank SPD Quadratic Geometry Visible Execution Ledger

Date: 2026-07-08
Status: `IN_PROGRESS`

## Ledger

### 2026-07-08 - Phase 0 - PRECHECK

Evidence contract:

- Question: Is the execution plan internally consistent, bounded, and aligned with BayesFilter evidence policy before code edits?
- Baseline/comparator: Existing Phase 5 minimal SSL-LSTM geometry path and 2026-07-07 geometry/tau-gate result.
- Primary criterion: Plan artifacts exist with research intent, evidence contract, skeptical audit, forbidden claims, review policy, and stop conditions.
- Veto diagnostics: Missing stop conditions, unsupported readiness/scientific claims, hidden source-faithfulness claim, hidden default-policy change, destructive dirty-worktree action.
- Non-claims: No implementation correctness, HMC readiness, posterior correctness, sampler convergence, or Zhao-Cui source-faithfulness.

Actions:

- Read local Claude-worker skill and review-gate guide.
- Inspected existing Phase 5 benchmark geometry path and mass-matrix helper.
- Created master program, Phase 0 subplan, Phase 1 subplan, visible runbook, and compact review bundle.

Artifacts:

- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase0-governance-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase1-utility-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-visible-gated-execution-runbook-2026-07-08.md`
- `docs/reviews/bayesfilter-low-rank-spd-quadratic-geometry-phase0-review-bundle-2026-07-08.md`

Gate status:

- `PASSED_WITH_CODEX_SUBSTITUTE_REVIEW`: Claude review gate rejected private-context transfer; substitute review returned `VERDICT: AGREE`.

Next action:

- Run `git diff --check`, then start Phase 1 utility implementation if it passes.

### 2026-07-08 - Phase 0 - REVIEW_GATE

Actions:

- Attempted material Claude review gate through `/home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh`.
- Escalation was rejected for private repository context transfer risk.
- Wrote Codex substitute review at `docs/reviews/bayesfilter-low-rank-spd-quadratic-geometry-phase0-codex-substitute-review-2026-07-08.md`.
- Wrote Phase 0 result at `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase0-governance-result-2026-07-08.md`.

Gate status:

- `PASSED_WITH_CODEX_SUBSTITUTE_REVIEW`.

Next action:

- Run Phase 0 `git diff --check`; if clean, advance to Phase 1.

### 2026-07-08 - Phase 1 - ASSESS_GATE

Evidence contract:

- Question: Does the utility enforce declared mechanical gates on controlled targets?
- Baseline/comparator: synthetic quadratic and adversarial under-sampled/nonfinite/bad-holdout cases.
- Primary criterion: focused utility tests pass and structured diagnostics are exposed.
- Veto diagnostics: accepted under-sampled fit, non-SPD precision, over-condition matrix, nonfinite silent accept, bad holdout accept, out-of-trust refined center accept.
- Non-claims: no MAP certification, HMC convergence, posterior correctness, default readiness, or source-faithful Zhao-Cui evidence.

Actions:

- Added `bayesfilter/inference/quadratic_geometry.py`.
- Exported the utility from `bayesfilter/inference/__init__.py`.
- Added `tests/test_quadratic_geometry.py`.
- Ran focused checks.

Artifacts:

- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase1-utility-result-2026-07-08.md`
- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase2-minimal-ssl-lstm-integration-subplan-2026-07-08.md`

Gate status:

- `PASSED`: compile passed; `pytest tests/test_quadratic_geometry.py -q` reported `8 passed, 4 warnings`; `git diff --check` passed.

Next action:

- Advance to Phase 2 minimal SSL-LSTM integration.

### 2026-07-08 - Phase 2 - ASSESS_GATE

Evidence contract:

- Question: Can the minimal diagnostic consume the reusable low-rank SPD geometry result without hiding failures or changing readiness claims?
- Baseline/comparator: existing `map_candidate_hessian` and `initial_covariance` strategies.
- Primary criterion: focused integration tests pass and geometry diagnostics preserve selected source, fallback status, utility payload, nonclaims, and position role.
- Veto diagnostics: silent default change, missing rejection status, hidden fallback, unsupported MAP/HMC-readiness/source-faithfulness claim.
- Non-claims: no posterior correctness, HMC convergence, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness.

Actions:

- Added optional `low_rank_spd_quadratic` strategy to the Phase 5 benchmark.
- Added CLI flags for strategy and low-rank sample count.
- Added focused tests for accepted precision transformation and rejected-attempt fallback provenance.

Artifacts:

- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase2-minimal-ssl-lstm-integration-result-2026-07-08.md`
- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase3-checks-diagnostic-subplan-2026-07-08.md`

Gate status:

- `PASSED`: focused integration suite reported `18 passed, 27 warnings`; `git diff --check` passed.

Next action:

- Advance to Phase 3 focused checks and bounded CPU-hidden diagnostic.

### 2026-07-08 - Phase 3 - ASSESS_GATE

Evidence contract:

- Question: Does the optional low-rank SPD geometry path produce a structured minimal-target diagnostic artifact or honest fallback without breaking focused HMC checks?
- Baseline/comparator: existing Phase 5 diagnostic and 2026-07-07 geometry/tau-gate result.
- Primary criterion: focused tests pass and diagnostic JSON/Markdown artifacts are written with CPU-hidden provenance and low-rank geometry diagnostics.
- Veto diagnostics: test failure, runtime exception, missing artifact, missing low-rank payload/fallback reason, unsupported convergence/default/source-faithfulness claim.
- Non-claims: no posterior correctness, HMC convergence, zero divergences, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness.

Actions:

- Ran focused checks.
- Ran bounded CPU-hidden diagnostic.
- First diagnostic exposed `UnboundLocalError`; repaired terminal Phase 7 slot initialization and `HMCKernelTuningConfig.payload()` indentation.
- Reran focused checks and bounded diagnostic.

Artifacts:

- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase3-checks-diagnostic-result-2026-07-08.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_cpu_hidden_2026-07-08.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_cpu_hidden_2026-07-08.md`

Gate status:

- `PASSED_VALID_NON_PROMOTING`: final rerun has no hard vetoes, low-rank geometry rejection/fallback is explicit, and tuning remains budget-exhausted with no viable joint pair.

Next action:

- Close out Phase 4.

### 2026-07-08 - Phase 4 - CLOSEOUT

Actions:

- Wrote closeout subplan and result.
- Recorded remaining gaps and next recommended repair options.

Artifacts:

- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase4-closeout-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase4-closeout-result-2026-07-08.md`

Gate status:

- `COMPLETE`.

Next action:

- Await human direction on whether to prioritize fixed-mass `L, epsilon` repair or low-rank quadratic fit repair.
