# P75 Phase 3 Subplan: Opt-In Implementation And Unit Tests

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE3
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement the reviewed opt-in P75 stochastic density-training surfaces and
verify them with focused CPU-only tests and smoke commands.  Phase 3 proves
implementation mechanics only; it does not run the target pilot and does not
make lower-gate or validation claims.

## Entry Conditions Inherited From Phase 2

Phase 3 may begin only if:

- Phase 2 result exists;
- Phase 2 names exact implementation files, test files, and runner commands;
- Phase 2 distinguishes implementation mechanics from fresh-audit evidence;
- Phase 2 local checks pass;
- Claude returns `VERDICT: AGREE` for Phase 2 result and this subplan.

## Required Artifacts

Phase 3 must produce:

- new module:
  `bayesfilter/highdim/stochastic_density_training.py`;
- new tests:
  `tests/highdim/test_p75_stochastic_density_training.py`;
- new runner:
  `scripts/p75_stochastic_density_training_pilot.py`;
- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-result-2026-06-17.md`;
- Phase 4 bounded-pilot subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-subplan-2026-06-17.md`;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --schema-only --output /tmp/p75-schema.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --smoke-only --output /tmp/p75-smoke.json
rg -n "P75|TrainableFunctionalTT|tf.Variable|GradientTape|weighted_empirical_cross_entropy|normalizer|audit|nonclaims" bayesfilter/highdim/stochastic_density_training.py tests/highdim/test_p75_stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py
git diff --check -- bayesfilter/highdim/stochastic_density_training.py tests/highdim/test_p75_stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md
```

Review:

- Claude read-only review of implementation diffs, test results, Phase 3
  result, and Phase 4 subplan;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does the opt-in P75 implementation correctly expose finite differentiable stochastic density-training mechanics? |
| Exact baseline/comparator | Phase 2 surface map, immutable `SquaredTTDensity` normalizer and density evaluation, and current P73-B blocked evaluator. |
| Primary pass/fail criterion | Phase 3 passes if focused CPU-only tests and smoke commands pass, implementation remains opt-in, exact normalizer and `rho_theta` match snapshot density on tiny cases, gradients are finite, audit records are rejected, P72/P73 regression checks pass, and Phase 4 subplan is drafted. |
| Diagnostics that can veto | Nonfinite loss/grad/log-normalizer, missing gradients, normalizer mismatch, `rho_theta` mismatch, audit leakage, default P72/P73 behavior change, TensorFlow backend violation, runner missing CPU-only/nonclaim manifest, smoke exceeding synthetic/tiny bounds. |
| Explanatory only | Smoke loss values, one-step parameter delta, runtime, parameter count. |
| What will not be concluded | No target-pilot success, no lower-gate repair, no validation readiness, no HMC readiness, no scaling claim, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 3 result, tests, smoke JSONs, ledgers. |

## Implementation Requirements

Implement:

- `P75TrainableTTConfig`;
- `P75ObjectiveBatch`;
- `P75ObjectiveTerms`;
- `TrainableFunctionalTT`;
- weighted empirical target weights
  \(\alpha_i\propto w_i(g_i^2+\tau q_0(z_i))\);
- exact differentiable squared-TT normalizer;
- trainable `rho_theta(points)` and normalized log-density equality with
  immutable `SquaredTTDensity` after snapshot;
- finite objective and finite-gradient checks;
- audit-record and audit-hash rejection;
- snapshot conversion into immutable `FunctionalTT` and `SquaredTTDensity`;
- CPU-only schema and smoke runner manifests.

Phase 3 smoke is limited to a synthetic fixture with dimension at most 2,
degree at most 2, rank at most 2, batch size at most 8, and at most 2
optimizer steps.  It must not generate Zhao--Cui target fresh batches and must
record `smoke_only_not_pilot_evidence`.

Phase 3 must include explicit P72/P73 regression checks:

- `p73_density_aware_optimizer_status()["status"]` remains
  `P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED`;
- P72 and P73 diagnostic runner import paths still load;
- default P72/P73 code paths do not import or execute P75 code.

Keep the route opt-in:

- no top-level `bayesfilter` export;
- no default behavior changes in P72/P73;
- no target-pilot execution in Phase 3.

## Forbidden Claims/Actions

- Do not run the degree 2/rank 4/1024/500 target pilot.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not alter P72/P73 thresholds or default behavior.
- Do not modify P72/P73 entrypoints to call P75.
- Do not use audit holdout, replay, or audit-line samples for training or
  model selection.
- Do not claim source-faithful Zhao--Cui.
- Do not claim lower-gate repair from smoke tests.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- Phase 3 result exists and passes local checks;
- implementation and tests are present;
- CPU-only smoke output exists and records nonclaims;
- Phase 4 subplan exists and defines the bounded target-pilot command,
  wall-clock cap, seeds, pass/block/nonclaim criteria, and review steps;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- exact normalizer differentiation cannot be implemented without `.numpy()` in
  the trainable path;
- tests expose audit leakage or P73 default behavior drift;
- trainable `rho_theta` or normalized log-density mismatches immutable
  snapshot density on tiny fixtures;
- smoke would require Zhao--Cui target fresh batches, more than 2 optimizer
  steps, or a batch larger than 8;
- Phase 3 needs to thread P75 through default P72/P73 entrypoints;
- TensorFlow imports fail in CPU-only mode;
- smoke command cannot produce a manifest;
- implementation would require package install, network access, GPU,
  destructive action, or outside-repo writes;
- Claude and Codex do not converge after five review rounds for the same
  blocker.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit if Phase 2 passes review:
it limits code edits to opt-in P75 surfaces, uses immutable
`SquaredTTDensity` as a normalizer comparator, requires CPU-only tests before
any pilot, and blocks proxy-metric promotion.
