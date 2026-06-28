# P03 Subplan: Focused Repair Test

Date: 2026-06-23

## Phase Objective

Test the single P02-selected repair on the same `N=8192` replay/nearby seed set.

## Entry Conditions Inherited From Previous Phase

- P02 selected exactly one repair family.
- Repair commands and artifacts are written in the refreshed P03 subplan.
- Claude review converged if required.

## Required Artifacts

- P03 benchmark JSON/Markdown/logs, exact paths to be filled by P02.
- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p03-focused-repair-test-result-2026-06-23.md`
- Refreshed P04 subplan.

## Required Checks, Tests, And Reviews

- Trusted GPU preflight.
- Run the P02-selected repair on replay/nearby seeds.
- Audit artifacts for finite outputs, residuals, paired thresholds, repair
  metadata, GPU/TF32 evidence, and thresholds.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the selected repair remove repeated `N=8192` paired drift without introducing numerical hard vetoes? |
| Baseline/comparator | P01 fixed-policy repeated-drift artifacts and paired streaming comparator in each P03 artifact. |
| Primary pass criterion | Every launched P03 repair row passes aggregate hard-veto and paired-threshold screens. |
| Veto diagnostics | Missing artifact, metadata mismatch, nonfinite outputs, residual failure, paired failure, GPU/TF32 evidence missing, timeout. |
| Explanatory diagnostics | Runtime, residual magnitudes, paired deltas, factor/scaling diagnostics. |
| Not concluded | No default readiness, no broad robustness, no statistical superiority. |
| Artifact | P03 benchmark artifacts and result. |

## Forbidden Claims/Actions

- Do not change repair family mid-phase.
- Do not claim default readiness.
- Do not rank by runtime or descriptive deltas.

## Exact Next-Phase Handoff Conditions

Proceed to P04 after P03 writes a valid pass/fail result.

## Stop Conditions

- Trusted GPU unavailable.
- Required artifact missing or malformed.
- Repair would require code changes not covered by P02.

## Skeptical Plan Audit

P03 tests one predeclared repair and separates repair pass/fail from default
promotion.
