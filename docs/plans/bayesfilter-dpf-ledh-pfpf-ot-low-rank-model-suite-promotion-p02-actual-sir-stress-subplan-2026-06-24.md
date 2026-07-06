# P02 Actual-SIR Stress Extension Subplan

Date: 2026-06-24

Status: `PROVISIONAL_PENDING_P01_RESULT_AND_REFRESH`

## Phase Objective

Extend actual-SIR evidence beyond the already-completed d18 validation/reporting
lane by testing additional seeds and stress regimes while preserving streaming
as comparator and avoiding any claim that actual-SIR alone proves broad
promotion.

## Entry Conditions Inherited From Previous Phase

- P01 result exists and either passes LGSSM exact-Kalman gate or records a
  reviewed non-candidate blocker that permits continuation.
- Candidate remains locked to `r16_eps0p25_alpha1em08_it120`.
- P01 did not reveal active-path NumPy, route mismatch, dense materialization,
  or exact-reference quality failure that vetoes promotion.
- Explicit approval is required before trusted GPU actual-SIR stress runtime.

## Required Artifacts

- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p02-actual-sir-stress-result-2026-06-24.md`
- P03 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p03-nonlinear-gaussian-subplan-2026-06-24.md`
- Actual-SIR stress JSON/Markdown artifacts under `docs/benchmarks`.
- Command log under
  `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/`.

## Required Checks, Tests, And Reviews

- Refresh stress matrix after P01.
- Syntax and focused tests for actual-SIR low-rank harness.
- Trusted GPU precheck.
- Paired streaming/low-rank stress rows with fixed seeds, GPU/TF32/XLA
  provenance, route-fired evidence, and hard-veto validation.
- Validators for actual-SIR semantics, paired comparability, low-rank
  nonmaterialization, candidate lock, and no unsupported claims.
- Claude read-only review of P02 result and P03 subplan if material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does locked low-rank remain valid on actual-SIR stress cases beyond the completed d18 lane? |
| Baseline/comparator | Streaming GPU/TF32 actual-SIR route with paired seeds and settings. |
| Primary pass criterion | All declared stress rows pass hard validity, provenance, route-fired, nonmaterialization, and paired-comparability screens. |
| Veto diagnostics | Nonfinite output, route mismatch, missing actual-SIR semantics, failed comparability, missing provenance, dense materialization, active-path NumPy, or unsupported claim. |
| Explanatory diagnostics | Runtime, memory, ESS, warm ratios, tail metrics, and seed variation. |
| Not concluded | No statistical superiority, posterior correctness, dense equivalence, HMC readiness, broad promotion, or package/public default switch. |
| Artifact | P02 result, benchmark JSON/Markdown artifacts, logs, ledgers. |

## Forbidden Claims And Actions

- Do not use actual-SIR stress timing alone as promotion evidence.
- Do not change candidate settings after seeing results.
- Do not run HMC/autodiff runtime.
- Do not change default policy, public API, package metadata, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P02 hands off to P03 only if P02 result passes or records a reviewed blocker
that does not invalidate candidate quality, P03 subplan is refreshed, and
Claude/local review converges where material.

## Stop Conditions

- Candidate fails a valid actual-SIR hard screen.
- Stress harness cannot preserve paired comparator semantics.
- Trusted GPU runtime is unavailable or unapproved.
- Review does not converge within five rounds for the same blocker.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write P02 result or blocker result.
3. Draft or refresh P03 subplan.
4. Review P03 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
