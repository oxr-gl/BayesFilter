# Fixed-SGQF Predator-Prey Budget Ladder Plan

metadata_date: 2026-06-17
program_id: fixed-sgqf-predator-prey-budget-ladder
status: EXECUTION_READY

## Purpose

This plan governs **Track B first** for the literature-backed predator-prey
model: a fixed-SGQF budget/tuning ladder study focused only on predator-prey,
so we can understand SGQF behavior thoroughly on this one model before moving to
other families.

The main question is whether increasing SGQF budget improves approximation
quality on this fixed target when compared against the same-target dense lower-
rung reference, for both value and score.

## Governing references

- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_p51_predator_prey_production_tuning.py`
- `tests/test_fixed_sgqf_values_tf.py`
- `tests/test_fixed_sgqf_scores_tf.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `tests/highdim/test_fixed_branch_derivatives.py`
- `tests/highdim/test_p30_fixed_branch_gradient_tables.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`

## SGQF budget knobs

### Primary budget knob
- `sparse_level`

This is the main SGQF budget axis to vary.

### Knobs to hold fixed for this study
- `predictive_epsilon = 1e-10`
- `innovation_epsilon = 1e-10`
- `merge_tolerance = 1e-12`
- `zero_weight_tolerance = 1e-14`
- observations
- theta
- dense reference order
- branch contract

These should stay fixed so the study measures quadrature richness rather than
branch-policy or merge-policy drift.

## Skeptical plan audit

Status target: `PASS_TO_PREDATOR_PREY_BUDGET_LADDER`

Risks:
1. confusing approximation quality with branch-admission tuning by changing
   epsilon settings;
2. reading any local monotone improvement as a general SGQF theorem;
3. treating UKF as the oracle instead of dense same-target reference;
4. silently dropping unstable/blocked higher-budget rows instead of recording
   them.

## Evidence contract

Question:

For the fixed predator-prey lower-rung same target, does increasing SGQF budget
(sparse level) improve value and score agreement against the same-target dense
reference?

### Primary value comparator
- `_dense_reference(order=7)` in `tests/highdim/test_p47_predator_prey_filtering.py`

### Primary score comparator
- `_dense_value_and_score(theta, order=7)` in the same file

### Promotion conditions
- same target,
- same observations,
- same theta,
- same branch config,
- same dense comparator,
- all gaps explicitly reported,
- no branch-valid score comparison unless accepted same-branch signatures match.

### Veto / block conditions
- branch identity changes under FD checks,
- a higher-budget row is silently omitted after failure,
- thresholds are loosened after inspecting outcomes,
- any claim implies global monotonicity or production/HMC readiness.

### What will not be concluded
- no universal SGQF monotonicity claim,
- no production predator-prey SGQF claim,
- no HMC readiness claim,
- no broader family admission claim.

## Test plan

### Phase A — value ladder in `tests/highdim/test_p47_predator_prey_filtering.py`
Add a sparse-level ladder over predeclared levels, e.g. 1 / 2 / 3 / 4 where
tractable.

For each level record:
- `cloud.point_count`
- branch hash / branch acceptance
- total log-likelihood gap vs dense
- per-step log-normalizer gaps vs dense
- filtered mean/covariance path gaps vs dense

Primary assertion style:
- all rows finite,
- all gaps recorded,
- level 2 should not be worse than level 1 on primary value metrics,
- level 3/4 are observational rows unless clearly stable and improved.

### Phase B — score ladder in `tests/highdim/test_p47_predator_prey_filtering.py`
For the same sparse-level ladder:
- compute SGQF score with `with_derivatives=True`
- compare to the dense same-target score
- keep score comparison only where the SGQF accepted-branch contract holds

Record:
- componentwise score gaps
- score L2 / L∞ gaps
- branch signature status

### Phase C — UKF baseline row
For the same predator-prey target:
- keep UKF as a fixed same-target baseline row against the dense value and dense
  score reference.
- report SGQF-vs-UKF only as explanatory comparison after both are anchored to
  dense.

## Execution order

1. Write this budget-ladder plan artifact.
2. Add a predeclared SGQF sparse-level ladder helper in the predator-prey test
   file.
3. Add value-gap ladder checks against the dense reference.
4. Add score-gap ladder checks against the dense score oracle.
5. Keep UKF as a fixed baseline comparator on the same target.
6. Run the focused predator-prey test suite.
7. Write the result artifact with a compact numerical table.

## Verification

Minimum verification:
- rerun `tests/highdim/test_p47_predator_prey_filtering.py`
- rerun `tests/highdim/test_p44_predator_prey_diagnostic.py` if touched
- rerun `tests/highdim/test_p51_predator_prey_production_tuning.py`

## Expected outcome

After implementation, the repo should have a compact SGQF budget-ladder study on
predator-prey that shows how value and score gaps to the dense same-target
reference behave as SGQF budget increases, while preserving the repo’s branch,
same-scalar, and non-overclaiming discipline.
