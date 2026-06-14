# P6 Plan: Particle-Count And Seed Ladder

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Evidence Contract

Question: how much of the CUT4-vs-DPF difference is explained by DPF
Monte Carlo variability and particle-count sensitivity?

Comparator: P4/P5 CUT4 values and P4/P5 DPF seed/particle rows.

Pass criterion: result summarizes seed variability, particle-count trend, and
calibration implications for future acceptance bands.  This phase may be a
structured blocker if P4/P5 only support a minimal smoke ladder.

Veto diagnostics: treating one-seed results as final equivalence, hiding
Monte Carlo variability, or setting universal thresholds without calibration.

## Inputs

- P4 and P5 result JSONs.

## Outputs

- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p6-particle-count-seed-ladder-result-2026-05-29.md`

## Allowed Write Set

DPF nonlinear-SSM plan/result artifacts and existing JSON/report outputs if
the reviewed implementation supports them.

## Forbidden Write Set

Production code, tests, monograph chapters, vendored code, high-dimensional
lane, DSGE/NAWM files.

## Skeptical Audit Checklist

Use the master checklist.  Pay special attention to threshold calibration.

## Stop Conditions

Write a structured blocker if P4/P5 do not generate enough seed/particle rows
to support calibrated acceptance bands.

## Verification Commands

- `python -m json.tool` over P4/P5 JSON outputs.
- `rg -n "calibration|seed|particle|structured blocker" docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p6-*-2026-05-29.md`

## Claude Review Protocol

Use exact Claude command and loop.

## What Must Not Be Concluded

No final universal thresholds, production readiness, posterior correctness,
DSGE/NAWM validation, or monograph claim.
