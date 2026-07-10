# Review Bundle: Deterministic LGSSM HMC Tuning Phase 4 Result / Phase 5 Subplan

Date: 2026-07-09

## Role Contract

Claude is read-only reviewer only. Codex remains supervisor and executor.
Claude must not edit files, run commands, launch agents, or review the whole
repository.

## Review Question

Does the Phase 4 result support advancing only to deterministic geometry/mass
initialization, while preserving the no-HMC-run, XLA-only, no-runtime-autodiff,
and no-scientific-claim boundaries?

## Exact Paths

- Phase 4 result:
  `docs/plans/bayesfilter-deterministic-lgssm-hmc-tuning-phase4-xla-score-gate-result-2026-07-09.md`
- Phase 5 subplan:
  `docs/plans/bayesfilter-deterministic-lgssm-hmc-tuning-phase5-geometry-mass-subplan-2026-07-09.md`
- Runbook:
  `docs/plans/bayesfilter-deterministic-lgssm-hmc-tuning-visible-gated-execution-runbook-2026-07-09.md`

## Evidence Summary

- Focused tests: `5 passed, 2 warnings`.
- XLA score command: passed under `CUDA_VISIBLE_DEVICES=-1`.
- XLA artifact:
  `docs/benchmarks/artifacts/multidim_lgssm_serious_hmc_tuning_2026_07_09/xla_compile_gate.json`
- Artifact hash:
  `sha256:f945e98ad2aac75cb2998e51855a717e9b9894384f254c29861e4911d35593a9`
- `jit_compile`: `true`
- `jit_compile_false_runtime_executed`: `false`
- `runtime_autodiff_tape_executed`: `false`
- finite value/score: `true`
- score shape: `[18]`
- concrete function count: `1`
- HLO byte count: `3427939`
- vetoes: `[]`

## Pass Criteria For Review

- Phase 4 does not overclaim beyond XLA value/score admissibility.
- Phase 5 subplan inherits the Phase 4 gate and stays deterministic.
- Phase 5 uses existing BayesFilter geometry/mass tools rather than manual
  agent tuning.
- Phase 5 does not run serious HMC or posterior sampling.
- Boundaries requiring human approval remain intact.

## Block Criteria For Review

- Any HMC convergence, posterior recovery, production, GPU, or scientific claim
  is supported by Phase 4 compile evidence alone.
- Phase 5 allows manual mass editing, manual tuning decisions, or serious HMC.
- The handoff misses a required veto or stop condition.

## Required Verdict

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
