# G4 Subplan: Nystrom-Specific Gradient Mechanics Gate

Date: 2026-06-24

Status: `READY_AFTER_FOCUSED_IMPLEMENTATION_CHECKS`

## Phase Objective

Run a bounded actual-SIR Nystrom-specific gradient mechanics smoke to verify
that the selected Nystrom route exposes a finite scalar and finite gradient
with respect to initial particles.

This is a hard-veto mechanics screen only.  It does not establish HMC readiness,
posterior correctness, target-shape HMC viability, or default readiness.

## Entry Conditions Inherited From Previous Phase

- G3 closed as `G3_HISTORY_MEMORY_PASS`.
- Focused G4 script exists:
  `docs/benchmarks/run_actual_sir_nystrom_gradient_mechanics_smoke.py`.
- Syntax check passed.
- Focused Nystrom/compiled-redo tests passed: `13 passed`.
- Fixed policy remains frozen:
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`.
- CPU-hidden execution is intentional for this tiny mechanics smoke.

## Required Artifacts

- G4 JSON:
  `docs/benchmarks/actual-sir-nystrom-g4-gradient-mechanics-cpu-2026-06-24.json`
- G4 Markdown:
  `docs/benchmarks/actual-sir-nystrom-g4-gradient-mechanics-cpu-2026-06-24.md`
- G4 log:
  `docs/plans/logs/actual-sir-nystrom-g4-gradient-mechanics-cpu-2026-06-24.log`
- G4 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g4-gradient-mechanics-result-2026-06-24.md`
- G5 evidence package or stop-handoff draft after G4.

## Required Checks, Tests, And Reviews

Pre-run checks:

- local skeptical plan audit;
- confirm CPU-hidden command uses `CUDA_VISIBLE_DEVICES=-1`;
- confirm route under test is `actual_sir_nystrom`;
- confirm fixed-policy metadata in command.

Run:

- `T=2`, `N=32`, one seed;
- `rank=32`, `epsilon=0.5`, raw kernel, scaling normalization `none`,
  Cholesky solver;
- differentiable scalar: sum of actual-SIR Nystrom route log likelihoods;
- gradient target: initial particles tensor;
- `dtype=float64`, TF32 disabled;
- CPU-hidden device scope.

Post-run JSON audit:

- `overall_passed is True`;
- `hard_veto_status == "passed"`;
- `route_under_test == "actual_sir_nystrom"`;
- CPU-hidden metadata matches;
- fixed-policy metadata recorded;
- Nystrom route invocation count positive;
- scalar is finite;
- gradient is not `None`;
- gradient is finite;
- gradient norm is finite;
- nonclaims include no HMC readiness/posterior/default claim.

Review:

- local review required;
- Claude read-only review recommended for G4 result/G5 boundary because this
  evidence is easy to overclaim.  Claude cannot authorize HMC readiness,
  posterior claims, or default promotion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the actual-SIR Nystrom route expose a finite differentiable scalar and finite gradient under a tiny mechanics smoke? |
| Baseline/comparator | No comparator; G4 is a hard-veto mechanics screen for Nystrom only. |
| Primary pass criterion | Syntax/focused checks already passed; smoke command exits 0 and JSON reports mechanics hard-veto pass with CPU-hidden metadata, positive route invocation count, finite scalar, non-`None` finite gradient, finite gradient norm, and fixed-policy metadata. |
| Veto diagnostics | Missing script/artifact, nonzero exit, CPU-hidden metadata mismatch, route invocation count zero, missing fixed-policy metadata, nonfinite scalar, missing/nonfinite gradient, unsupported HMC/posterior/default claim. |
| Explanatory diagnostics | Scalar value, gradient norm, tiny shape, runtime. |
| Not concluded | No HMC readiness, no posterior convergence, no sampler tuning adequacy, no target-shape HMC viability, no default readiness, no acceptance of seed `82921`. |
| Artifact | G4 JSON/Markdown/log/result. |

## Forbidden Claims/Actions

- Do not claim HMC readiness or posterior convergence.
- Do not use this tiny smoke as target-shape HMC viability.
- Do not claim default readiness or production promotion.
- Do not edit unrelated HMC or algorithm code in G4.
- Do not let Claude edit, execute, launch workers, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

- `G4_GRADIENT_MECHANICS_PASS`: write G4 result, review G5 boundary claims, and
  draft G5 evidence package/default-readiness review plan.
- `G4_GRADIENT_MECHANICS_FAIL`: write blocker/result; do not proceed to G5.
- `G4_ARTIFACT_BLOCKER`: stop if required artifact is missing or malformed.

## Stop Conditions

- Gradient mechanics command exits nonzero.
- Required artifact missing or malformed.
- Any hard-veto diagnostic fails.
- Result would require claiming HMC readiness, posterior convergence, or
  target-shape HMC viability.
- Fix would require unrelated HMC or algorithm code changes beyond a reviewed
  repair subplan.

## Skeptical Plan Audit

This gate can only reject obvious Nystrom gradient mechanics failures.  It
cannot validate posterior behavior, HMC readiness, default readiness, or broad
route robustness.  The plan preserves that boundary by making finite
Nystrom-scalar/gradient behavior the only primary criterion.

Audit status: `PASS_FOR_G4_LAUNCH`.
