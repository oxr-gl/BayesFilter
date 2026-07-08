# Phase 3 Subplan: Bounded Mechanics Smoke

Date: 2026-07-08

## Status

`DRAFT_SUBPLAN_NOT_EXECUTED`

## Phase Objective

Run the smallest bounded fixed-kernel mechanics smoke using the Phase 2
geometry artifact, only to check that a tiny HMC runtime can execute with
finite target/log-acceptance diagnostics and no immediate hard-veto mechanics
failure.

This phase is not HMC readiness, not convergence evidence, and not posterior
correctness evidence.

## Entry Conditions

- Phase 2 geometry artifact exists:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.json`
- Phase 2 decision has `geometry_initialization_passed=true` and empty vetoes.
- Phase 2 artifact records:
  - `selected_hint=negative_hessian`;
  - `fallback_used=false`;
  - finite positive `initial_step_size`;
  - positive `initial_num_leapfrog_steps`;
  - `hmc_runtime_invoked=false`.

## Required Artifacts

- Phase 3 script or harness patch, to be created before execution.
- JSON artifact:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_mechanics_cpu_hidden_2026-07-08.json`
- Markdown artifact:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_mechanics_cpu_hidden_2026-07-08.md`
- Phase 3 result note:
  `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase3-bounded-mechanics-result-2026-07-08.md`

## Required Checks And Reviews

- Local Codex self-review before execution for HMC boundary safety and
  unsupported claims.
- Required local checks, to be finalized in the Phase 3 implementation patch:
  - compile/import check for the Phase 3 harness;
  - CPU-hidden execution of the tiny mechanics smoke;
  - focused HMC-kernel tests relevant to the harness touched;
  - `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Phase 2 fixed geometry execute the smallest bounded HMC mechanics smoke without immediate finite-value, divergence, or artifact failures? |
| Baseline/comparator | Phase 2 geometry artifact; no ranking or alternative sampler comparison. |
| Primary pass criterion | Tiny mechanics artifact exists, records finite target values/log accept ratios, no runtime exception, no missing divergence/acceptance telemetry, and no hard-veto diagnostics. |
| Veto diagnostics | Runtime exception, nonfinite target/log accept, divergence telemetry unavailable when required by the harness, unexpected fallback/reinitialization, missing artifact, or unsupported readiness/posterior claim. |
| Explanatory diagnostics | Acceptance fraction, log-acceptance summaries, energy/proposed-state finite checks, runtime, and any target-status telemetry. |
| What will not be concluded | HMC convergence, posterior correctness, acceptable long-run behavior, sampler superiority, production/default readiness, or Zhao-Cui source-faithfulness. |
| Artifact preserving result | Phase 3 JSON/Markdown artifacts and result note listed above. |

## Forbidden Claims And Actions

- Do not run long chains, tuning ladders, adaptive HMC, or GPU/default-policy
  evidence in Phase 3.
- Do not claim HMC readiness or posterior correctness from a tiny mechanics
  smoke.
- Do not change the Phase 2 mass or formula settings after seeing mechanics
  results unless recording a blocker/repair result and drafting a new subplan.

## Exact Next-Phase Handoff Conditions

If Phase 3 passes, Phase 4 may draft a short-chain validation plan only if:

- all Phase 3 hard vetoes are clear;
- artifact records finite mechanics telemetry;
- result note states that the result is mechanics-only and non-promoting.

If Phase 3 fails, write a blocker/repair result and do not proceed to
short-chain validation until the failure is classified as implementation,
tuning/geometry, target, or artifact failure.

## Stop Conditions

- Phase 2 artifact missing or not passed.
- Phase 3 harness cannot be made to preserve Phase 2 fixed geometry.
- Runtime would exceed the intended tiny mechanics scope.
- Required telemetry cannot be recorded.
- Continuing would require package installation, network access, external
  Claude review, GPU/default-policy evidence, or unsupported scientific claims.

## Skeptical Plan Audit

| Risk | Phase 3 audit |
| --- | --- |
| Wrong baseline | Uses only Phase 2 fixed geometry; no sampler ranking. |
| Proxy metric promoted | Acceptance and finite telemetry are mechanics smoke diagnostics only. |
| Missing stop conditions | Stop conditions block long chains, tuning ladders, and missing telemetry. |
| Unfair comparison | No comparison. |
| Hidden assumptions | Harness must preserve Phase 2 fixed geometry and not silently retune. |
| Stale context | Must re-read Phase 2 artifact before execution. |
| Environment mismatch | CPU-hidden debug/reference status must be recorded. |
| Artifact mismatch | Result artifact must answer mechanics execution only, not convergence. |

Audit status: `DRAFT_ONLY_NOT_EXECUTED`.

