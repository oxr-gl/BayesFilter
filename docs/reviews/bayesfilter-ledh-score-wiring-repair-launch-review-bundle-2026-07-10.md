# Claude Review Bundle: LEDH Score Wiring Repair Launch

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

## Objective

Review the launch plan for a Codex-supervised repair program that fixes LEDH
same-target score wiring across LGSSM, fixed-SIR, predator-prey, actual-SV,
generalized-SV, and KSC-SV.

Claude is read-only reviewer only. Codex remains supervisor and executor.

## Artifacts To Review

- Master program:
  `docs/plans/bayesfilter-ledh-score-wiring-repair-master-program-2026-07-10.md`
- Phase 0 subplan:
  `docs/plans/bayesfilter-ledh-score-wiring-repair-phase0-launch-inventory-subplan-2026-07-10.md`
- Phase 1 subplan:
  `docs/plans/bayesfilter-ledh-score-wiring-repair-phase1-shared-contract-subplan-2026-07-10.md`
- Visible runbook:
  `docs/plans/bayesfilter-ledh-score-wiring-repair-visible-gated-execution-runbook-2026-07-10.md`

## Current Inventory Summary

- LGSSM: compact default score route has been repaired; naming/timing residue
  remains.
- fixed-SIR: compact helper exists; historical memory-result normalizer remains.
- predator-prey: default diagnostic still uses memory-style reverse VJP.
- actual-SV: default diagnostic still uses memory-style reverse VJP.
- generalized-SV: compact route is wired, but default precision is float64/TF32
  disabled.
- KSC-SV: compact route is wired, but default precision is float64/TF32
  disabled.

## Binding Invariants

- Default LEDH score computation must physically use compact
  forward-sensitivity/no-time-history route.
- Historical `manual_total_vjp*` and `memory_style*` routes are diagnostic-only.
- Full score admission requires compact no-tape provenance.
- Production LEDH score execution uses TensorFlow `float32` tensors with TF32
  enabled.
- Same-scalar FD correctness must compare against a value-only scalar route,
  not the score/JVP route.
- Score-only memory diagnostics are not score correctness or full admission.

## Review Questions

Check for:

- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch;
- evasive scientific language;
- a plan path that relabels old memory-style evidence as compact computation.

Findings first. End with exactly:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
