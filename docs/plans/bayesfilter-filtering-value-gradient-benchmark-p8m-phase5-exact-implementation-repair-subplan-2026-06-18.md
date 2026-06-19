# P8m Phase 5 Subplan: Exact Implementation Repair

metadata_date: 2026-06-18
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 5

## Phase Objective

Implement the reviewed exact transport-core repair from Phase 4 and verify it
does not change matched exact outputs.

## Entry Conditions Inherited From Previous Phase

- Phase 4 identifies an implement-now exact repair.
- Focused tests and artifact paths are specified.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase5-exact-implementation-repair-result-2026-06-18.md`
- Code diffs and focused test artifacts.

## Required Checks/Tests/Reviews

Minimum checks, refined by Phase 4:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest <focused-transport-tests> -q
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py <tests-or-benchmarks> docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-*
```

Trusted GPU performance check only after CPU correctness checks pass.

Claude review is required for the implementation diff and result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the exact implementation repair preserve outputs and improve or simplify generic transport behavior? |
| Baseline/comparator | Pre-repair exact transport route under matched synthetic benchmark settings. |
| Primary criterion | Focused correctness checks pass and any performance claim is backed by trusted-GPU artifacts. |
| Veto diagnostics | Value mismatch under exact settings, gradient breakage if relevant, CPU fallback, nonfinite output, SIR-specific code, default change. |
| Explanatory diagnostics | Runtime, compile time, memory, residuals, diff summary. |
| Not concluded | No lower-iteration acceptance, no production default, no scientific adequacy. |

## Forbidden Claims/Actions

- Do not change Sinkhorn iterations or epsilon as part of exact repair.
- Do not claim speedup without trusted GPU evidence.
- Do not touch unrelated model code.

## Exact Next-Phase Handoff Conditions

Phase 6 may proceed if exact implementation state is closed and any remaining
iteration/epsilon question is explicitly separated as validation.

## Stop Conditions

Stop if exact output equality fails, focused tests fail, or the repair expands
beyond reviewed scope.
