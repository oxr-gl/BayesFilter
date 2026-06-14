# P7 Plan: Final Audit And Handoff

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Evidence Contract

Question: is the nonlinear-SSM DPF evidence ladder ready for handoff with clear
models tested, comparators, gradient/MLE status, structural residuals, caveats,
and unresolved risks?

Comparator: P0-P6 outputs.

Pass criterion: final result summarizes phase status, Claude review iterations,
files changed, models tested, comparators, MLE/SE status or blockers, gradient
status, structural residual status, verification, caveats, and next action.

Veto diagnostics: missing phase result, failed verification that invalidates
evidence, unauthorized edits, or overclaim.

## Inputs

- P0-P6 result artifacts and model report JSONs.

## Outputs

- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p7-final-audit-handoff-result-2026-05-29.md`

## Allowed Write Set

DPF nonlinear-SSM plan/result artifacts.

## Forbidden Write Set

Production code, tests, monograph chapters, vendored code, high-dimensional
lane, DSGE/NAWM files.

## Skeptical Audit Checklist

Use the master checklist.

## Stop Conditions

Stop or write structured blocker if required verification fails, if CUT4/DPF
same-scalar evidence is missing, or if deterministic structural residuals are
not recorded.

## Verification Commands

- NumPy import gate over `experiments/dpf_implementation/tf_tfp`.
- import-boundary search for student/vendored/highdim/DSGE/NAWM imports.
- `python -m py_compile` over touched Python files.
- targeted runners and validate/repro checks.
- JSON parse checks.
- `git diff --check`.
- `git status --short --branch`.
- `git status --short -- bayesfilter tests`.

## Claude Review Protocol

Use exact Claude command and loop.

## What Must Not Be Concluded

No production/API readiness, HMC readiness, posterior correctness, DSGE/NAWM
validation, banking/model-risk claim, or monograph claim.
