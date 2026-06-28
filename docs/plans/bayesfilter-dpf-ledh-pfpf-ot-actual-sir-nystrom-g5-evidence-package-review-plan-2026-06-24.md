# G5 Plan: Evidence Package And Default-Readiness Review

Date: 2026-06-24

Status: `SUPERSEDED_BY_STATISTICAL_TESTING_AMENDMENT`

Supersession note, 2026-06-24: stochastic paired-delta exceedances must be
interpreted through
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-statistical-testing-amendment-2026-06-24.md`.
This G5 plan remains a historical review packet, but its future default or
rejection implications are replaced by the statistical testing amendment.

## Phase Objective

Assemble the G1-G4 evidence package and define the boundary for any future
human/default-scope review.

G5 is not an experiment launch.  It is a claim-boundary and decision-packet
phase.

## Entry Conditions Inherited From Previous Phase

- G1 closed as `G1_SPARSE_N8192_DRIFT`.
- G2 closed as `G2_DIAGNOSTIC_CONTINUE_TO_G3`.
- G3 closed as `G3_HISTORY_MEMORY_PASS`.
- G4 closed as `G4_GRADIENT_MECHANICS_PASS`.
- Seed `82921` remains a valid stochastic paired-delta exceedance under the
  old engineering threshold.
- No statistical test has established that this exceedance is significant
  breakage or default-incompatibility.

## Required Artifacts

- This G5 plan.
- G5 result/evidence package:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g5-evidence-package-review-result-2026-06-24.md`
- Optional Claude read-only review log if requested or if a material default
  boundary is being crossed.

## Required Checks, Tests, And Reviews

- Local artifact-existence check for G1-G4 result files and summary JSON.
- Claim-boundary scan for unsupported default/HMC/posterior/ranking claims.
- Explicit inference-status table.
- Human approval required for any default-policy change.
- Claude read-only review recommended before any later default-readiness packet
  is presented as promotion-relevant.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What decision is justified by G1-G4 evidence? |
| Baseline/comparator | G1/G3 paired streaming comparator artifacts and G4 Nystrom-only mechanics artifact. |
| Primary decision criterion | Recommend optional/restricted continuation, repair, stop, or human default-scope review based on closed gates and unresolved vetoes. |
| Veto diagnostics | Deterministic validity vetoes only: nonfinite outputs, malformed artifacts, wrong route/policy metadata, residual failure, comparator failure, or missing trusted GPU/TF32 evidence.  Seed `82921` is stochastic paired-delta evidence requiring the statistical testing amendment; no posterior correctness evidence; no HMC readiness evidence; no statistical ranking or failure-probability model. |
| Explanatory only | Runtime, warm ratios, ESS, gradient norm, scalar value, residual magnitudes below thresholds. |
| Not concluded | No default readiness, no HMC readiness, no posterior correctness, no statistical superiority, no statistical rejection from seed `82921`, and no acceptance criterion for default scope. |
| Artifact | G5 result/evidence package. |

## Forbidden Claims/Actions

- Do not change default policy by agent-only decision.
- Do not claim HMC readiness from G4.
- Do not claim posterior correctness from paired comparability.
- Do not claim statistical failure probability from one-seed panels.
- Do not call seed `82921` statistically significant breakage without a
  predeclared statistical test.

## Exact Next-Phase Handoff Conditions

- `RECOMMEND_STATISTICAL_VALIDATION_BEFORE_DEFAULT`: if deterministic validity
  evidence remains favorable but paired-delta stochastic evidence is not yet
  statistically calibrated.
- `RECOMMEND_REPAIR_BEFORE_PROMOTION`: only if deterministic validity fails or
  a predeclared statistical test rejects the acceptable paired-error model.
- `STOP_FOR_HUMAN_DEFAULT_SCOPE_DECISION`: if the next action would accept
  default scope without statistical validation or change product policy.

## Stop Conditions

- Required G1-G4 artifact missing or malformed.
- Claim-boundary scan finds unsupported default/HMC/posterior/ranking claim.
- Default-policy change would be made without human approval.

## Skeptical Plan Audit

G5 must not let a sequence of passed diagnostic gates silently become a default
decision.  The strongest evidence now is restricted fixed-policy viability and
mechanics-screen passage.  The strongest remaining gap for default promotion is
the absence of a predeclared statistical paired-delta validation rule, plus
absent HMC/posterior evidence.  Seed `82921` is evidence about the tail of a
stochastic diagnostic, not deterministic proof of breakage.

Audit status: `SUPERSEDED_FOR_FUTURE_DECISIONS`.
