# P05 LGSSM Heldout Validation Subplan

Date: 2026-06-24

Status: `DRAFT_PENDING_P04`

## Phase Objective

Validate the P04 frozen rule on heldout LGSSM exact-reference rows that were
not used to select the rule. P05 is the first phase that may support a
calibrated residual or direct value/gradient gate, within LGSSM scope only.

## Entry Conditions Inherited From Previous Phase

- P04 result exists and freezes a single candidate rule before holdout.
- P05 subplan embeds the frozen rule by value.
- Heldout rows were not used to choose the rule.
- Trusted GPU runtime approval is available.
- No approval is inherited for HMC runtime, package/API/default changes,
  package installs, network fetches, model-file edits, or scientific claims.

## Required Artifacts

- P05 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p05-holdout-validation-result-2026-06-24.md`
- Structured aggregate JSON:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p05-holdout-2026-06-24.json`
- Aggregate Markdown:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p05-holdout-2026-06-24.md`
- Logs under:
  `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/`
- Refreshed P06 subplan.

## Required Checks, Tests, And Reviews

- Trusted GPU precheck.
- Quiet visible execution and structured artifact validation.
- Run heldout LGSSM rows. Initial intended holdout set:
  - `lgssm_medium_exact_ref`, seeds `91011,91012,91013`;
  - `lgssm_informative_obs_stress`, seeds `91021,91022,91023`;
  - routes `streaming` and `low_rank`;
  - same fixed probe schedule as P04 frozen rule.
- Apply the P04 frozen rule exactly. Do not tune thresholds during P05.
- Record hard validity vetoes, value/gradient/peak screens, residual role, and
  uncertainty limitations.
- Claude read-only review of P05 result and P06 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the P04 frozen rule pass heldout LGSSM value/gradient/peak diagnostics under exact Kalman reference? |
| Baseline/comparator | Exact Kalman value/gradient oracle for heldout LGSSM rows and streaming finite-particle route as comparator. |
| Primary pass criterion | Frozen rule passes all heldout rows without hard validity vetoes, missing metrics, or unsupported claims. |
| Veto diagnostics | Any frozen-rule hard failure, nonfinite value/gradient, invalid factors, active-path NumPy, dense materialization, missing exact reference, missing GPU/XLA provenance, holdout leakage, or corrupt artifact. |
| Explanatory diagnostics | Residual distribution, gradient component differences, peak-neighborhood summaries, timing, memory, ESS, and seed variation. |
| Not concluded | No broad posterior correctness, no statistical superiority unless separately supported, no HMC readiness, no package default readiness, no actual-SIR validation. |
| Artifact | P05 result, aggregate JSON/Markdown, row logs, review ledger, and refreshed P06 subplan. |

## Forbidden Claims And Actions

- Do not change the frozen rule after seeing heldout outcomes.
- Do not continue to P06 as if P05 passed if a hard frozen-rule veto fires.
- Do not claim actual-SIR readiness from LGSSM heldout validation.
- Do not run HMC.
- Do not change public API, package metadata, default policy, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P05 hands off to P06 only if:

- P05 result and structured artifacts exist;
- local validator confirms the frozen rule was applied unchanged;
- heldout pass/fail status is recorded;
- if P05 fails, the result classifies whether this invalidates the rule, the
  harness, or only the candidate threshold;
- Claude review returns `VERDICT: AGREE`;
- P06 subplan is refreshed to respect P05 scope.

If P05 fails the frozen rule due to value/gradient/peak harm, stop before P06
unless the result classifies the failure as harness invalidity with a reviewed
repair path.

## Stop Conditions

- Trusted GPU runtime is unavailable or unapproved.
- Frozen rule manifest is missing or mutable/ambiguous.
- Holdout leakage is discovered.
- Required heldout artifacts are missing or corrupt.
- Claude/Codex review does not converge within five rounds for the same
  blocker.

## End-Of-Subplan Procedure

1. Run required local checks and runtime validators.
2. Write P05 result or blocker result.
3. Draft or refresh P06 subplan.
4. Review P06 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
5. Send material result/subplan to Claude read-only review and record verdict.
