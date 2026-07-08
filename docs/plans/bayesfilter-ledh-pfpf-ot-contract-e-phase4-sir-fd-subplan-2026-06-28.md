# Phase 4 Subplan: Contract E SIR same-scalar FD diagnostic

Date: 2026-06-28

Status: `DRAFT_PENDING_PHASE3`

## Phase Objective

Test Contract E on the parameterized SIR target using same-scalar finite
differences only, with no Zhao-Cui oracle and no central-difference promotion.

## Entry Conditions Inherited From Previous Phase

- Phase 3 LGSSM gradient gate has passed, either directly or after a reviewed
  same-phase repair and focused rerun.
- Contract E reset route, random residual policy, and conditioning gates are
  fixed from earlier phases.

## Required Artifacts

- SIR Contract E diagnostic script/update.
- JSON/Markdown SIR FD diagnostic artifacts.
- Phase 4 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase4-sir-fd-result-2026-06-28.md`
- Refreshed Phase 5 SV/nonlinear subplan.

## Required Checks, Tests, And Reviews

- Compile/check changed files.
- Tiny CPU-hidden smoke if useful for wiring.
- Trusted GPU/XLA/TF32 run for material SIR evidence.
- Bounded Claude review of result and Phase 5 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the SIR Contract E gradient route agree with same-scalar FD regression within uncertainty on targeted parameters? |
| Baseline/comparator | Same-scalar 13-point FD regression with fixed randomness, 5 or more seeds where feasible, highest/lowest objective dropped, regression over remaining points, and explicit SE. |
| Primary pass criterion | Manual/reverse gradient agrees with FD slope within two combined SE for predeclared targeted parameters. |
| Veto diagnostics | Zhao-Cui comparator used as oracle, central FD as primary evidence, missing SE, nonfinite values, `transport_ad_mode=full`, missing residual/conditioning diagnostics, or untrusted GPU evidence. |
| Explanatory diagnostics | Sinkhorn residuals, FD R2, per-seed scatter, central FD sanity, runtime, memory. |
| Not concluded | No exact SIR gradient correctness, no posterior correctness, no HMC readiness, no production readiness. |
| Artifact | SIR FD JSON/Markdown plus Phase 4 result. |

## Forbidden Claims And Actions

- Do not claim SIR truth from FD alone; this is a same-scalar consistency
  diagnostic.
- Do not use Zhao-Cui as an oracle.
- Do not change FD protocol after seeing results.
- Do not run larger N ladders before the small targeted diagnostic is
  interpretable.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- SIR result records FD slopes, SE, z-scores, and diagnostics;
- Contract E passes the Phase 4 primary same-scalar FD gate, or a reviewed
  repair closes Phase 4 as passed after focused reruns;
- Phase 5 target and comparator are explicitly scoped.

If the SIR same-scalar FD gate fails and is not repaired inside Phase 4,
classify the failure in the Phase 4 result and stop rather than advancing to
Phase 5.

## Stop Conditions

Stop on missing same-scalar guarantee, FD protocol violation, unbounded runtime,
documented MCSE/conditioning veto that blocks interpretation, or evidence that
Contract E nonlinear path needs a separate implementation repair program.

## End-Of-Phase Protocol

Run checks, write result, refresh Phase 5, review Phase 5, repair findings, and
advance or stop.
