# P0 Plan: Scope And Estimation Criteria

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Evidence Contract

Question: does the ladder define a principled estimation/gradient evidence
contract for general nonlinear SSMs without claiming production, posterior,
DSGE, or NAWM validation?

Comparator: current LEDH-PF-PF-OT handoff and ch18b structural warning.

Pass criterion: result records estimation-scale comparison, same-scalar
gradient requirements, calibrated-threshold policy, lane boundaries, and caveats.

Veto diagnostics: arbitrary final thresholds, value-only promotion, missing
same-scalar requirement, DSGE/NAWM drift, or production write need.

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `docs/chapters/ch18b_structural_deterministic_dynamics.tex`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-result-2026-05-29.md`

## Outputs

- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p0-scope-and-estimation-criteria-result-2026-05-29.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-*-2026-05-29.md`

## Forbidden Write Set

Production `bayesfilter/`, `tests/`, monograph chapters, vendored code,
high-dimensional lane, DSGE/NAWM implementation files.

## Skeptical Audit Checklist

Check stale context, wrong comparator, value-only evidence overclaimed as
gradient evidence, arbitrary thresholds, missing stop conditions, hidden
production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, DSGE/NAWM drift, and artifact fitness.

## Stop Conditions

Stop if final thresholds are asserted without calibration, if CUT4 is called
ground truth, or if the plan would require forbidden edits.

## Verification Commands

- `rg -n "standard-error|same-scalar|CUT4 is a differentiable comparator|No DSGE" docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-*-2026-05-29.md`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No production/API readiness, HMC readiness, posterior correctness, DSGE/NAWM
validation, banking/model-risk claim, or monograph claim.
