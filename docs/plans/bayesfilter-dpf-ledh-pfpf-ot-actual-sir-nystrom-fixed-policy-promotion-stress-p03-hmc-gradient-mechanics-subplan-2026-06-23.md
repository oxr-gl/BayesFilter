# P03 Subplan: Nystrom-Specific Gradient Mechanics Gate

Date: 2026-06-23

## Phase Objective

Run a bounded Nystrom-specific gradient mechanics screen after P01/P02 pass,
without claiming posterior convergence, HMC readiness, or target-shape HMC
viability.

## Entry Conditions Inherited From Previous Phase

- P01 replicated high-N gate passed.
- P02 full-history/memory gate passed.
- Fixed policy remains frozen for actual-SIR Nystrom evidence.
- P03 must exercise the actual-SIR Nystrom route. A generic HMC mechanics
  fixture is not sufficient evidence for this lane.

## Required Artifacts

- Nystrom gradient mechanics script, if it does not already exist:
  `docs/benchmarks/run_actual_sir_nystrom_gradient_mechanics_smoke.py`
- Nystrom gradient mechanics JSON:
  `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p03-nystrom-gradient-mechanics-cpu-2026-06-23.json`
- Nystrom gradient mechanics Markdown:
  `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p03-nystrom-gradient-mechanics-cpu-2026-06-23.md`
- Nystrom gradient mechanics log:
  `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p03-nystrom-gradient-mechanics-cpu-2026-06-23.log`
- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p03-hmc-gradient-mechanics-result-2026-06-23.md`
- Refreshed P04 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-subplan-2026-06-23.md`

## Required Checks, Tests, And Reviews

- If the Nystrom gradient mechanics script does not exist, create it in a
  focused implementation step before running P03. The script must use
  TensorFlow, reuse the actual-SIR Nystrom compiled-redo callbacks/core route,
  and write JSON/Markdown artifacts.
- Syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_nystrom_gradient_mechanics_smoke.py`
- Run CPU-hidden tiny actual-SIR Nystrom gradient mechanics smoke with:
  - `T=2`, `N=32`, one seed;
  - `rank=32`, `epsilon=0.5`, raw kernel, scaling normalization `none`,
    cholesky solver;
  - differentiable scalar equal to the sum of Nystrom route log likelihoods;
  - gradient target equal to the initial particles tensor;
  - `CUDA_VISIBLE_DEVICES=-1`, device scope CPU, `float64`, TF32 disabled.
- JSON audit:
  - `overall_passed is True`;
  - `hard_veto_status == "passed"`;
  - CPU-hidden metadata matches;
  - route under test is `actual_sir_nystrom`;
  - fixed-policy metadata is recorded;
  - Nystrom route invocation count is positive;
  - scalar value is finite;
  - gradient exists, is not `None`, and is finite;
  - gradient norm is finite;
  - nonclaims include no HMC readiness/posterior claim.
- Claude Opus max-effort read-only review is required before final P04
  synthesis because gradient mechanics evidence is easy to overclaim.
- Write P03 result with decision table, inference-status table, run manifest,
  post-run red-team note, and nonclaims.
- Refresh and locally review P04 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the actual-SIR Nystrom route expose a finite differentiable scalar and finite gradient under a tiny mechanics smoke? |
| Baseline/comparator | No comparator; P03 is a hard-veto mechanics screen for the Nystrom route only. |
| Primary pass criterion | Syntax check passes; smoke command exits 0 and writes JSON/Markdown; JSON reports mechanics hard-veto pass with CPU-hidden metadata, positive Nystrom route invocation count, finite scalar, non-`None` finite gradient, finite gradient norm, and fixed-policy metadata. |
| Veto diagnostics | Missing script/artifact, nonzero command exit, CPU-hidden metadata mismatch, route invocation count zero, missing fixed-policy metadata, nonfinite scalar, missing/`None`/nonfinite gradient, unsupported HMC readiness/posterior claim. |
| Explanatory diagnostics | Scalar value, gradient norm, tiny shape, selected gradient target, runtime. |
| Not concluded | No HMC readiness, no posterior convergence, no sampler tuning adequacy, no target-shape HMC viability, no GPU HMC claim, no Nystrom-specific HMC readiness. |
| Artifact | P03 JSON/Markdown/log and P03 result. |

## Forbidden Claims/Actions

- Do not claim HMC readiness or posterior convergence.
- Do not use the generic tiny HMC mechanics fixture as a substitute for the
  Nystrom-specific gradient mechanics artifact.
- Do not run target-shape HMC without a separate reviewed subplan.
- Do not edit unrelated HMC or algorithm code in P03 unless a separate repair
  subplan is written and reviewed first.
- Do not let Claude edit, execute, launch workers, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

Proceed to P04 only if:

- P03 checks and smoke pass;
- P03 result exists and preserves Nystrom-specific mechanics boundaries;
- Claude read-only review converges for P03/P04 boundary claims;
- P04 subplan exists and has been locally reviewed.

## Stop Conditions

- Nystrom gradient mechanics command exits nonzero.
- Required artifact missing or malformed.
- Any hard-veto diagnostic fails.
- Result would require claiming HMC readiness, posterior convergence, or
  target-shape HMC viability.
- Fix would require unrelated HMC or algorithm code changes beyond a reviewed
  repair subplan.

## Skeptical Plan Audit

This gate can only reject obvious Nystrom gradient mechanics failures; it
cannot validate posterior behavior or HMC readiness. The plan preserves that
boundary by making finite Nystrom scalar/gradient behavior the only primary
criterion and requiring Claude review before final synthesis.

Audit status: `READY_AFTER_P02_PASS`.
