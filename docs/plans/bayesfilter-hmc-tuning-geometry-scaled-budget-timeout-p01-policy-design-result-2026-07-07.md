# Phase 1 Result: Central Geometry-Scaled Budget And Progress Policy Design

Date: 2026-07-07

Status: `PASSED_DESIGN_READY_FOR_IMPLEMENTATION`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Implement one BayesFilter-owned policy | Met: policy inputs, formulas, payloads, tests, and touch points are specified | No NUTS, no MacroFinance-local tuning, no public-private leak required | Exact constants are engineering defaults with provenance, not statistical truth | Draft and execute Phase 2 implementation subplan | No tuning readiness, posterior convergence, sampler superiority, production readiness, or CCMA success |

## Policy Name

Implement a single BayesFilter policy, tentatively:

`HMCGeometryScaledBudgetTimingPolicy`

This policy is the only promoted source for:

- bootstrap diagnostic sample counts;
- Phase 4 windowed-mass warmup counts;
- Phase 5 tune/screen counts;
- Phase 6 screen counts;
- final verification counts;
- attempt budget and extended-attempt eligibility;
- staged timing budgets and public watcher defaults.

## Public-Safe Geometry Inputs

Use existing `PrecomputedMassArtifact` metadata, not raw arrays in public
artifacts.

| Input | Source | Public-safe? | Use |
| --- | --- | --- | --- |
| `dimension` | `PrecomputedMassArtifact.dimension` | Yes | Model size scale |
| `condition_number` | metadata-only `eigen_summary.condition_number` | Yes | Geometry difficulty |
| `effective_dimension` | compute from metadata eigenvalues inside BayesFilter; publish scalar only | Yes | Anisotropy / concentration |
| `clipped_eigenvalue_count` | `regularization_report` | Yes | Regularization pressure |
| `raw_nonpositive_eigenvalue_count` | `regularization_report` | Yes | Geometry warning |
| `diagonal_fallback_used` | `regularization_report` | Yes | Heavy regularization warning |
| `shrinkage` | windowed mass config/result metadata where available | Yes | Mass update pressure |

Do not publish covariance arrays, factors, positions, raw samples, candidate
grids, step sizes, or leapfrog counts in public progress.

## Geometry Scores

For implementation, compute a public-safe geometry summary:

- `d = max(1, dimension)`;
- `kappa = max(1, finite condition number)`;
- `d_eff = (sum(lambda))^2 / sum(lambda^2)` when finite positive eigenvalues
  are available; otherwise `d_eff = d`;
- `anisotropy_pressure = clip(log(max(d / d_eff, 1)) / log(max(d, 2)), 0, 1)`;
- `condition_pressure = clip(log10(kappa) / 6, 0, 1)`;
- `regularization_pressure = clip((clipped + nonpositive) / d + diagonal_fallback, 0, 1)`;
- `geometry_multiplier = 1 + condition_pressure + anisotropy_pressure + regularization_pressure`.

This multiplier is a conservative evidence-budget inflator.  It is not a
posterior-convergence diagnostic and must not be described as proving geometry
quality.

## Sample Budget Formula

For serious/default tuning evidence:

- `base = ceil(dimension_factor * d * geometry_multiplier)`;
- `initial_budget = clamp(base, min_initial, max_initial)`;
- `attempt_budget_k = min(max_tune, initial_budget * 2**attempt_index)`.

Sub-budgets:

- Phase 4 warmup: `attempt_budget_k`;
- Phase 5 epsilon tuning ladder: `(ceil(b/4), ceil(b/2), b)`;
- Phase 5 screen: `max(screen_floor, ceil(b/4))`;
- Phase 6 screen: `max(screen_floor, ceil(b/4))`;
- final verification: `max(verification_floor, ceil(b/2))`;
- burn-in: `max(burnin_floor, ceil(results/4))`.

For smoke/diagnostic presets, route through the same policy but mark counts as
`contract`, `diagnostic`, or `observability` only.  They may be capped, but the
payload must say they cannot support tuning success, posterior convergence, or
default readiness.

## Acceptance Uncertainty

Each screen should report:

- number of transitions used for acceptance;
- estimated acceptance;
- uncertainty method, preferably Wilson interval;
- whether the interval lies wholly inside, wholly outside, or overlaps the
  pass/repair band.

If uncertainty overlaps a decision boundary and the stage is not smoke-only,
the next attempt should either:

- increase the relevant sample budget by the normal attempt-doubling rule; or
- report `insufficient_acceptance_evidence` instead of pretending the noisy
  estimate is decisive.

## Attempt Policy

Serious/default tuning:

- minimum serious attempt envelope: 5 attempts;
- maximum attempt cap: 10;
- attempts 6 through 10 are allowed only if the previous attempt made
  meaningful repair progress.

Meaningful repair progress means at least one public/private-safe state change
occurred:

- new mass artifact signature;
- changed selected step hash;
- changed selected trajectory hash;
- repaired or shifted L-grid/edge relation;
- acceptance moved from one decision relation to another;
- new verification repair handoff;
- additional completed batch that changes the evidence classification.

If none of these happens, close with
`phase7_extended_attempt_stalled_no_meaningful_progress`.

## Timing Policy

Separate three clocks:

- sample/evidence budget: chosen by the sample policy;
- stall detection: stage-aware no-progress window;
- emergency cap: generous machine protection only.

Policy payload should include:

- `progress_poll_s`;
- `no_progress_timeout_s`;
- `emergency_safety_timeout_s`;
- `public_timeout_budget_s`;
- staged timing budget/rationale;
- role labels: `stall_detection_not_tuning_evidence`,
  `emergency_cap_machine_protection_only`.

The current implementation can keep explicit external watcher timeouts, but
their defaults must be emitted by this BayesFilter policy rather than copied as
MacroFinance-local numbers.  A slow run that continues emitting progress events
must not be stopped by the no-progress rule.

## Implementation Touch Points

Modify BayesFilter:

- add `HMCGeometryScaledBudgetTimingPolicy`;
- add public-safe geometry summary helper;
- extend `_HMCAttemptBudgetPolicy.payload()` with geometry/rationale fields;
- replace `_default_attempt_budget_policy` and `_public_budget_policy_factory`
  formulas with calls into the central policy;
- replace `_public_bootstrap_config` hard-coded counts with central policy
  output;
- replace `HMCStagedTimeoutPolicy` default stage budgets with central policy
  timing output or explicit compatibility adapter;
- export the new policy from `bayesfilter.inference`.

Modify MacroFinance only as integration:

- remove local CCMA staged timeout table;
- request the BayesFilter policy by name or instantiate the BayesFilter policy;
- keep watcher as a monitor, but get default safety/no-progress/public timeout
  values from BayesFilter policy payload;
- keep public redaction tests.

## Required Tests

BayesFilter tests:

- high dimension increases serious attempt budgets;
- high condition number increases budgets;
- low effective dimension / anisotropy increases budgets;
- heavy regularization increases budgets;
- smoke/diagnostic counts are labeled non-promoting;
- acceptance uncertainty overlap is labeled or drives more draws;
- public policy payload omits mass arrays, samples, step sizes, leapfrog counts,
  and candidate grids;
- staged timing payload has no bare `900` default and labels emergency cap as
  machine protection.

MacroFinance tests:

- CCMA launcher uses BayesFilter policy defaults;
- progress-aware supervisor no longer hard-codes `900`;
- watcher still stops no-progress runs and does not stop progress updates;
- public summary does not leak private HMC mechanics.

## Phase 2 Handoff

Phase 2 may implement the central policy and tests.  The implementation should
be surgical: do not rewrite the HMC algorithm, do not add NUTS, do not move
generic docs into MacroFinance, and preserve existing public-private redaction
guards.

## Review Status

Claude review is unavailable because the approval system rejected external
review.  Phase 2 should use a fresh Codex substitute review for material design
or implementation gates.
