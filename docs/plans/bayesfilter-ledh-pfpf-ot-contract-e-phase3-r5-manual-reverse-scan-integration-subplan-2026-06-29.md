# Phase R5 Subplan: Manual Reverse-Scan Integration Handoff

Date: 2026-06-29

Status: `DRAFT_HANDOFF_FROM_R4`

## Phase Objective

Integrate the R4 fixed-ridge Cholesky reset VJP into the Contract E manual
likelihood reverse-scan route, without using generic autodiff as the material
gradient path.

R5 is an integration-planning and first-wiring phase.  It may create a local
manual reverse-scan prototype, but it must not run material Phase 3 until the
prototype passes its own reviewed local checks.

## Entry Conditions Inherited From R4

- R4 local reset-map VJP parity passed.
- R4 fixed-chart tests asserted identical center/`+h`/`-h` realized ridge and
  ridge-attempt counts.
- Static tests block hidden generic autodiff/eigh in the reset helper family.
- The material blocker remains:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Required Artifacts

- Inventory of the existing Phase 3 gradient route and all reset inputs needed
  by the reverse scan.
- Integration design showing where cotangents from the next particles enter
  `contract_e_cholesky_ridge_reset_fixed_ridge_vjp`.
- Explicit policy for the realized ridge in the integrated route:
  - fixed realized ridge is recorded and replayed for local VJP checks; or
  - branch changes stop the gate.
- A local one-step or tiny-loop reverse-scan fixture before any full LGSSM
  material run.
- R5 result / close record.
- R6 handoff only if local integrated reverse-scan parity passes.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before implementation.
- Bounded Claude read-only review of this R5 subplan before execution.
- Static audit that the integrated material route still does not use generic
  autodiff or `transport_ad_mode=full`.
- Local same-scalar parity test for the integrated one-step or tiny-loop route.
- `py_compile`, focused pytest, and `git diff --check` on touched paths.
- Bounded Claude implementation review before advancing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the local reset VJP be composed into the manual likelihood reverse scan without reopening hidden autodiff? |
| Baseline/comparator | Same-scalar local finite differences on a one-step or tiny-loop integrated fixture. |
| Primary pass criterion | Integrated manual cotangents match same-scalar finite differences within frozen tolerances, with no hidden generic autodiff/eigh/full-transport autodiff and no ridge branch changes. |
| Veto diagnostics | Nonfinite cotangents, branch changes, hidden autodiff, mismatch with value route, missing reset auxiliary state, or weakened material blocker. |
| Explanatory diagnostics | Reset VJP contribution norms, transport VJP contribution norms, value residuals, covariance residuals, ridge values, and attempt counts. |
| Not concluded | Material LGSSM gradient correctness, SIR/SV correctness, HMC readiness, production readiness, or GPU/XLA readiness. |
| Artifact preserving result | R5 result note and local parity artifacts. |

## Forbidden Claims And Actions

- Do not remove or weaken the material blocker during R5 first wiring.
- Do not run material Phase 3, full LGSSM FD, SIR, SV, GPU, or XLA jobs until
  R5 local integration checks pass and a later reviewed phase authorizes them.
- Do not claim full filter gradient correctness from one-step or tiny-loop
  parity.
- Do not differentiate through ridge branch selection.
- Do not use TensorFlow `GradientTape`, Jacobian, `ForwardAccumulator`,
  `tf.gradients`, or `tf.compat.v1.gradients` as the material implementation.

## Exact Next-Phase Handoff Conditions

Advance to R6 only if:

- local integrated reverse-scan parity passes;
- static hidden-autodiff/full-transport audit passes;
- realized ridge and attempt counts are recorded and stable on parity probes;
- R5 result is written;
- bounded Claude implementation review converges; and
- the material blocker remains in place unless R6 is specifically reviewed to
  replace it with a narrower material gate.

## Stop Conditions

Stop and write an R5 blocker result if:

- reset auxiliary state cannot be replayed without hidden autodiff;
- local integrated parity fails after one focused repair attempt;
- ridge branch changes appear on parity probes;
- the material route requires generic autodiff to pass; or
- Claude review does not converge after five rounds for the same blocker.
