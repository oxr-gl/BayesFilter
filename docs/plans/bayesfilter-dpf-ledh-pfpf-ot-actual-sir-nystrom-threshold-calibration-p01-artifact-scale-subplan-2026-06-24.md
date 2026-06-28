# P01 Subplan: Existing-Artifact Scale Extraction

Date: 2026-06-24

Status: `PENDING_P0_HANDOFF`

## Phase Objective

Extract normalized paired log-likelihood error scales from existing unique
`N=8192`, `rank=32`, `epsilon=0.5` artifacts without running new GPU
benchmarks.  P1 quantifies the legacy `5.0` threshold on total, per-time, and
per-observed-component scales and prepares a P2 threshold-freeze subplan.

## Entry Conditions Inherited From Previous Phase

- P0 closes as `P0_PASS_TO_P1`.
- Master program and visible runbook are reviewed.
- Legacy `5.0` is not treated as principled.
- No new threshold is frozen.
- No validation seed outcomes are interpreted for pass/fail.

## Required Artifacts

- P1 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p01-artifact-scale-result-2026-06-24.md`
- Optional machine-readable summary:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p01-artifact-scale-2026-06-24.json`
- Refreshed P2 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p02-threshold-freeze-subplan-2026-06-24.md`
- Execution ledger update.

## Required Checks, Tests, And Reviews

Local checks:

- locate existing fixed-policy `N=8192`, `rank=32`, `epsilon=0.5` JSON
  artifacts;
- count each seed once, preferring replay artifact for duplicate seed `82921`;
- verify at least 12 unique seed artifacts are available; the expected current
  seed panel is `82920..82931`;
- verify each included artifact has route `both`, fixed-policy metadata,
  `T=20`, `N=8192`, `float32`, TF32 enabled, and paired log-likelihood deltas;
- verify each included artifact records actual-SIR shape `state_dim=18` and
  `obs_dim=9` either in `shape` or `sir_semantics`; do not infer `M=9` from
  memory alone;
- compute signed and absolute paired deltas;
- compute per-time and per-observed-component deltas using `T=20`, `M=9`;
- compute streaming comparator spread and Nystrom-minus-streaming spread across
  the included seed panel;
- classify all numbers as descriptive only.

Review:

- local review required;
- Claude read-only review required for the P2 threshold-freeze subplan because
  threshold selection is a material boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What scale do existing artifacts imply for paired deltas and for the legacy `5.0` threshold? |
| Baseline/comparator | Existing same-artifact compiled streaming TF32 actual-SIR route. |
| Primary pass criterion | P1 result reports deduplicated seed set, normalized deltas, comparator noise proxies, caveats, and no pass/fail threshold choice. |
| Veto diagnostics | Missing/malformed artifact, duplicate seed mishandled, wrong policy included, missing paired deltas, treating descriptive statistics as calibration or validation. |
| Explanatory diagnostics | Means, SDs, quantiles, per-component scaling, legacy-threshold conversion, runtime if already present. |
| Not concluded | No calibrated threshold, no statistical validation, no default readiness, no rejection, no HMC/posterior claim. |
| Artifact | P1 result and optional JSON summary. |

## Forbidden Claims And Actions

- Do not run GPU benchmarks in P1.
- Do not freeze `tau_component` in P1.
- Do not claim legacy `5.0` is principled.
- Do not use P1 descriptive SD alone as promotion or rejection evidence.
- Do not choose thresholds after looking at future validation seeds.

## Exact Next-Phase Handoff Conditions

- `P1_PASS_TO_P2`: artifact checks pass, descriptive scale result is written,
  P2 threshold-freeze subplan is drafted/refreshed, and material review
  converges.
- `P1_REPAIR_LOOP`: a fixable artifact inclusion, deduplication, or reporting
  issue is found.
- `P1_BLOCKED`: fewer than 12 unique fixed-policy artifacts are verified,
  required artifacts are missing/malformed enough that scale extraction cannot
  be trusted, `obs_dim=9` cannot be verified, or P2 review fails to converge
  after five rounds.

## Stop Conditions

- Fewer than 12 required existing unique artifacts can be verified.
- Any included artifact lacks verifiable `T=20`, `N=8192`, `state_dim=18`, or
  `obs_dim=9`.
- Included artifacts disagree on model shape or fixed policy.
- The summary script/report cannot distinguish descriptive statistics from
  threshold calibration.
- Continuing would require choosing `tau_component` without P2 review.

## Skeptical Plan Audit

| Risk | P1 Audit |
| --- | --- |
| Wrong baseline | Existing paired artifacts use same-artifact streaming comparator; P1 states it is not truth. |
| Proxy metric | Descriptive SDs and quantiles cannot promote/reject. |
| Missing stop conditions | Artifact validity and threshold-freeze boundaries are explicit. |
| Unfair comparison | P1 uses fixed-policy N8192 artifacts only. |
| Hidden assumption | `M=9` is taken from actual-SIR semantics and must be verified in artifacts or harness metadata. |
| Stale context | Legacy `5.0` is reported only as historical scale. |
| Environment mismatch | P1 is artifact-only. |
| Artifact mismatch | Deduplication and fixed-policy checks are mandatory. |

P3 split requirement: validation seeds must be disjoint from the P1 seed panel
unless a later reviewed subplan explicitly labels the result
`RESUBSTITUTION_ONLY_NO_VALIDATION_CLAIM`.

Audit status: `PENDING_P0_HANDOFF`.
