# Fixed-SGQF Predator-Prey Comparison Plan

metadata_date: 2026-06-16
program_id: fixed-sgqf-predator-prey-comparison
status: EXECUTION_READY

## Purpose

This plan governs the first literature-backed non-affine family admission for
fixed SGQF beyond the affine / LGSSM anchor: predator-prey T20.

The goal is to add a same-target fixed-SGQF comparison row for the literature-
backed predator-prey family without changing the target semantics.

## Governing context

- broader fixed-SGQF source-paper scope contract
- current repaired fixed-SGQF lane
- existing predator-prey lower-rung same-target reference and deterministic
  comparator infrastructure

Primary evidence surfaces already exist in:
- `bayesfilter/highdim/models.py`
- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_p51_predator_prey_production_tuning.py`

## Skeptical plan audit

Status target: `PASS_TO_PREDATOR_PREY_IMPLEMENTATION`

Risks:
1. accidental target change in the adapter;
2. promoting local success beyond one family admission;
3. pulling gradient scope into the pass before value-path admission is stable;
4. reviving excluded P44 debugging logic in the literature-facing scope.

## Evidence contract

Question:

Can the repaired fixed-SGQF lane be admitted as a same-target comparison method
for the literature-backed predator-prey T20 family?

Primary pass criterion:
- predator-prey is adapted into the fixed-SGQF lane without changing target
  semantics,
- at least one same-target value-path comparison artifact is produced,
- the result states clearly what was admitted and what remains outside scope.

Veto diagnostics:
- the adapter changes target semantics,
- a non-same-target surrogate is used without explicit labeling,
- the result overclaims beyond one family admission.

## Likely files to modify

- `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`
- potentially `tests/highdim/test_p47_predator_prey_filtering.py`
- potentially broader comparison artifacts under `docs/plans/`

## Execution order

1. Write this plan artifact.
2. Inspect the predator-prey model and current comparison tests again with the
   fixed-SGQF lane in mind.
3. Implement a same-target predator-prey fixed-SGQF adapter.
4. Add focused tests for adapter correctness and value-path comparison.
5. Run the relevant predator-prey tests.
6. Write the result artifact.

## Verification

Minimum verification:
- adapter correctness test(s),
- value-path comparison test(s) on predator-prey,
- rerun of the relevant predator-prey highdim tests,
- confirm the result remains within the source-paper leaderboard scope.
