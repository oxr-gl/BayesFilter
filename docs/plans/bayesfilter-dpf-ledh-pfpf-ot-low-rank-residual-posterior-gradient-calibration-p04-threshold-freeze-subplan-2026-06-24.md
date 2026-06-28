# P04 Threshold Freeze And Rule Selection Subplan

Date: 2026-06-24

Status: `DRAFT_PENDING_P03`

## Phase Objective

Select and freeze one candidate gate or rule before any holdout validation is
run. The rule may be:

- retain `factor_marginal_residual <= 0.005`;
- raise or otherwise adjust the residual threshold;
- demote factor residual to a repair trigger while using direct
  value/gradient/peak screens as the primary gate;
- replace factor residual with another predeclared residual or gradient-aware
  diagnostic.

P04 is a decision-freeze phase. It does not run holdout validation.

## Entry Conditions Inherited From Previous Phase

- P03 result exists with complete calibration artifacts and review convergence.
- P03 did not invalidate the harness or calibration/holdout split.
- P04 has access only to calibration rows for rule selection.
- No holdout outcomes have been run or inspected for this program.
- No approval is inherited for HMC runtime, package/API/default changes,
  package installs, network fetches, model-file edits, or scientific claims.

## Required Artifacts

- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p04-threshold-freeze-result-2026-06-24.md`
- Frozen rule manifest JSON:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p04-frozen-rule-2026-06-24.json`
- Frozen rule Markdown:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p04-frozen-rule-2026-06-24.md`
- Refreshed P05 subplan with the frozen rule embedded by value, not by
  reference to mutable text.

## Required Checks, Tests, And Reviews

- Local skeptical audit of rule selection:
  - wrong baseline;
  - proxy promoted without value/gradient support;
  - threshold chosen to rescue a known row without holdout protection;
  - missing uncertainty statement;
  - missing hard validity vetoes.
- Structured manifest validation that the frozen rule contains:
  - rule name and version;
  - calibration artifact paths;
  - exact candidate settings;
  - value/gradient/peak pass screens;
  - residual role: hard gate, repair trigger, explanatory, or replaced;
  - hard validity vetoes;
  - nonclaims;
  - holdout rows excluded from selection.
- Claude Opus/max read-only review of P04 result and P05 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What rule should be frozen before holdout to relate low-rank residual diagnostics to posterior value/gradient/peak behavior? |
| Baseline/comparator | P03 calibration rows only, LGSSM exact value/gradient oracle, and declared hard validity vetoes. |
| Primary pass criterion | A single frozen rule is recorded before holdout with clear residual role, value/gradient/peak screens, hard vetoes, artifact paths, and nonclaims. |
| Veto diagnostics | Holdout leakage, post-hoc threshold change, unsupported proxy promotion, missing value/gradient screens, missing hard validity vetoes, missing manifest, or Claude review nonconvergence. |
| Explanatory diagnostics | Calibration descriptive tables, uncertainty limits, residual distributions, and rule-selection rationale. |
| Not concluded | No holdout pass, no calibrated threshold validity, no statistical superiority, no posterior correctness, no HMC readiness, no default readiness. |
| Artifact | P04 result, frozen rule JSON/Markdown, review ledger, and refreshed P05 subplan. |

## Forbidden Claims And Actions

- Do not run holdout validation in P04.
- Do not use future P05 or P06 outcomes to choose the rule.
- Do not claim the frozen rule is validated until P05 passes.
- Do not change the candidate or comparator unless the result explicitly
  downgrades the program to repair-only and stops before holdout.
- Do not run HMC.
- Do not change public API, package metadata, default policy, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P04 hands off to P05 only if:

- P04 result exists with decision and inference-status tables;
- frozen rule JSON/Markdown exists and passes manifest validation;
- P05 subplan embeds the frozen rule and names holdout rows;
- Claude review returns `VERDICT: AGREE`;
- stop handoff remains `NOT_STOPPED`.

If no defensible rule can be frozen from P03, write a blocker result and stop
for human direction or a repair plan.

## Stop Conditions

- P03 evidence is too incomplete or invalid to freeze any rule.
- Calibration/holdout split is contaminated.
- Claude identifies unsupported proxy promotion that cannot be repaired within
  five rounds.
- Continuing would require changing pass/fail criteria after seeing holdout
  results.

## End-Of-Subplan Procedure

1. Run required local checks and manifest validation.
2. Write P04 result or blocker result.
3. Draft or refresh P05 subplan with the frozen rule.
4. Review P05 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
5. Send material result/subplan to Claude read-only review and record verdict.
