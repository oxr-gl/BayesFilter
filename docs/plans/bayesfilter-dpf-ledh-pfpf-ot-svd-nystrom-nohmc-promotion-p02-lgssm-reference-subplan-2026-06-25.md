# P02 Subplan: LGSSM Exact-Reference Gate

Date: 2026-06-25

Status: `DRAFT_AFTER_P01`

## Phase Objective

Test fixed SVD-Nystrom value-route behavior on an LGSSM case with exact Kalman
reference, so basic filtering-quality failures are caught before nonlinear and
resource stress.

## Entry Conditions Inherited From Previous Phase

- P01 inventory confirms relevant SVD-Nystrom harness/tests are present.
- Focused local tests passed.
- Candidate policy remains locked.

## Required Artifacts

- Per-run JSON/Markdown/log artifacts under:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-*.json`,
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-*.md`, and
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/`.
- Aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-lgssm-reference-summary-2026-06-25.json`
- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02-lgssm-reference-result-2026-06-25.md`
- P03 refreshed subplan.

## Required Checks, Tests, And Reviews

- Trusted `nvidia-smi` preflight; use GPU1 if suitable, else GPU0.
- Use an exact-Kalman LGSSM reference harness or write a blocker if only
  low-rank-specific LGSSM harness exists and SVD-Nystrom cannot be fairly run.
- Verify finite outputs, exact-reference errors, route/policy metadata,
  GPU/TF32 provenance, no active-path NumPy, and no dense materialization.
- Claude read-only review required if a new/modified LGSSM SVD-Nystrom harness
  is needed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does fixed SVD-Nystrom pass an LGSSM exact-reference quality gate? |
| Baseline/comparator | Exact Kalman reference for the declared LGSSM; streaming route may be explanatory. |
| Primary criterion | Deterministic validity and predeclared exact-reference error thresholds pass for all included rows. |
| Veto diagnostics | Exact-reference failure, nonfinite outputs, wrong route/policy metadata, GPU/TF32 mismatch, dense materialization, missing SVD metadata, or malformed artifacts. |
| Explanatory diagnostics | Runtime, memory, ESS, residuals, factor/core diagnostics, streaming deltas. |
| Not concluded | No nonlinear validity, no promotion, no statistical superiority, no HMC readiness. |
| Artifact | P02 aggregate summary and result. |

## Forbidden Claims And Actions

- Do not use LGSSM success as broad model-suite promotion.
- Do not tune candidate settings.
- Do not run HMC/autodiff.
- Do not compare against a weak baseline when exact Kalman is available.

## Exact Next-Phase Handoff Conditions

- `P02_PASS_TO_P03_ACTUAL_SIR_STRESS`: exact-reference gate passes and P03
  subplan reviewed.
- `P02_FAIL_OPTIONAL_OR_REPAIR`: deterministic validity passes but exact
  quality fails.
- `P02_DETERMINISTIC_BLOCKER`: artifact/GPU/metadata/numerical validity fails.
- `P02_BLOCKED`: no fair executable SVD-Nystrom LGSSM harness exists.

## Stop Conditions

- Exact-reference failure.
- Missing fair comparator/reference.
- Trusted GPU unavailable for GPU claim.
- Required harness work exceeds bounded docs/benchmark/test edits.

## Local Self-Review Of Next Subplan

P03 extends the already validated actual-SIR family with fresh stress seeds and
does not reuse P06 validation rows as new promotion evidence.
