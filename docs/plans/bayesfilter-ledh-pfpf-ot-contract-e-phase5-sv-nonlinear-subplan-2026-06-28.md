# Phase 5 Subplan: Contract E SV and nonlinear extension diagnostic

Date: 2026-06-28

Status: `DRAFT_PENDING_PHASE4`

## Phase Objective

Run one scoped SV-like or nonlinear target diagnostic to check whether Contract
E behavior generalizes beyond LGSSM and SIR without claiming broad model-suite
coverage.

## Entry Conditions Inherited From Previous Phase

- Phase 4 SIR same-scalar FD gate has passed, either directly or after a
  reviewed same-phase repair and focused rerun.
- Contract E route and FD protocol remain fixed.

## Required Artifacts

- SV/nonlinear diagnostic script/update.
- JSON/Markdown diagnostic artifacts.
- Phase 5 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase5-sv-nonlinear-result-2026-06-28.md`
- Refreshed Phase 6 GPU/XLA stress subplan.

## Required Checks, Tests, And Reviews

- Compile/check changed files.
- Tiny smoke if implementation changed.
- Trusted GPU/XLA/TF32 material run if GPU evidence is claimed.
- Bounded Claude review of result and Phase 6 subplan.

Default uncertainty gate, unless Phase 4 result justifies a reviewed narrower
target-specific gate before execution:

- same-scalar 13-point FD regression;
- highest and lowest objective values dropped;
- at least five seeds when runtime permits, otherwise a reviewed blocker/repair
  must narrow the scope before execution;
- manual/reverse gradient agrees with FD slope within two combined SE for the
  targeted parameter subset.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does Contract E avoid obvious same-scalar gradient or value pathologies on one additional nonlinear target? |
| Baseline/comparator | Same-scalar FD regression is the only pass/fail comparator.  Existing no-OT and old-OT arms are explanatory-only diagnostics when already available. |
| Primary pass criterion | No veto diagnostics, and the targeted same-scalar gradient diagnostic passes the default two-combined-SE FD regression gate or a reviewed target-specific gate frozen before execution. |
| Veto diagnostics | Wrong comparator, missing FD SE, nonfinite values, missing conditioning diagnostics, untrusted GPU evidence, or old reset mislabeled Contract E. |
| Explanatory diagnostics | Runtime, memory, central FD sanity, covariance residuals, condition spectra, per-seed scatter. |
| Not concluded | No broad nonlinear certification, no HMC readiness, no production readiness. |
| Artifact | SV/nonlinear diagnostic JSON/Markdown plus Phase 5 result. |

## Forbidden Claims And Actions

- Do not claim model-suite validity.
- Do not introduce a new learned/neural component.
- Do not change Contract E parameters to fit this target without a blocker note.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if:

- at least one nonlinear diagnostic artifact exists;
- Contract E passes the Phase 5 primary nonlinear diagnostic gate, or a
  reviewed repair closes Phase 5 as passed after focused reruns;
- Phase 6 names exact particle counts, chunks, device, dtype, and time budget.

If the nonlinear diagnostic gate fails and is not repaired inside Phase 5,
classify the failure in the Phase 5 result and stop rather than advancing to
Phase 6.

## Stop Conditions

Stop if nonlinear diagnostics are uninterpretable, require a new implementation
route, or exceed bounded runtime without producing evidence.

## End-Of-Phase Protocol

Run checks, write result, refresh Phase 6, review Phase 6, repair findings, and
advance or stop.
