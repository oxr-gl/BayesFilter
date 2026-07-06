# P02 Subplan: Repair Candidate Selection

Date: 2026-06-23

## Phase Objective

If P01 shows repeated paired drift with valid finite/residual artifacts, select
exactly one focused repair family for P03.

## Entry Conditions Inherited From Previous Phase

- P01 result exists.
- P01 classification is `REPRODUCED_AND_REPEATED_DRIFT`.
- Artifacts are valid and indicate paired drift rather than harness invalidity.

## Required Artifacts

- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p02-repair-selection-result-2026-06-23.md`
- Refreshed P03 subplan.

## Required Checks, Tests, And Reviews

- Review P01 diagnostics.
- Select one repair family only, using this predeclared routing:
  - If repeated-drift artifacts are finite/residual-valid and Nystrom
    diagnostics show low effective rank, poor landmark-core conditioning, or
    factor diagonal error as the most suspicious explanatory diagnostic,
    select a rank schedule candidate: `rank=64`.
  - Else if repeated-drift artifacts are finite/residual-valid and diagnostics
    show benign rank/conditioning but paired drift grows without numerical hard
    vetoes, select an epsilon schedule candidate: `epsilon=0.75`.
  - Else if repeated-drift artifacts show solver-sensitive factor diagnostics
    without nonfinite outputs, select core solver candidate:
    `svd_truncated,rcond=1e-6`.
  - Kernel projection is diagnostic-only and may not be selected as a
    promotion repair in this lane.
- If diagnostics do not clearly match one routing rule, stop for human
  direction rather than choosing a repair ad hoc.
- Claude read-only review required before P03 if the selected repair changes
  the fixed policy.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which single focused repair is justified by P01 repeated-drift evidence? |
| Baseline/comparator | P01 fixed-policy repeated-drift artifacts. |
| Primary pass criterion | One repair family is selected by the predeclared routing rules with rationale, artifact commands, and nonclaims. |
| Veto diagnostics | Selecting multiple repairs, selecting after-the-fact thresholds, unsupported default claim, repair not tied to P01 evidence, or diagnostics that do not match any routing rule. |
| Explanatory diagnostics | P01 paired deltas and Nystrom diagnostics. |
| Not concluded | No repair success until P03 runs. |
| Artifact | P02 result and refreshed P03 subplan. |

## Forbidden Claims/Actions

- Do not run repair benchmarks in P02.
- Do not select multiple repair families.
- Do not claim default readiness.

## Exact Next-Phase Handoff Conditions

Proceed to P03 only if P02 selects one repair and Claude review agrees when
required.

## Stop Conditions

- P01 did not classify `REPRODUCED_AND_REPEATED_DRIFT`.
- Repair selection cannot be justified without human direction.

## Skeptical Plan Audit

P02 prevents ad hoc tuning by requiring one predeclared repair family before
execution.
