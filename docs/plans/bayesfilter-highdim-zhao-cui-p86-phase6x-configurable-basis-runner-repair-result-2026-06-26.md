# P86 Phase 6X Result: Configurable-Basis Runner Repair

Date: 2026-06-26

Status: `P86_PHASE6X_CONFIGURABLE_BASIS_RUNNER_REPAIR_REVIEWED_PASS`

## Scope

Phase 6X repaired the P86 runner path that kept degree convergence blocked
after Phase 6W rank convergence passed. The repair makes the Lagrangep basis
order and element count explicit setup parameters in the preflight/fit runner
instead of hard-wiring only `Lagrangep(4,8)`.

This is a setup and guard repair only. No degree-comparator fit, GPU run,
Phase 7 bridge, HMC run, or production-promotion command was executed.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P86 represent non-default Lagrangep basis setup choices in runner preflights and exact-fit guards without reviving ALS or claiming degree convergence? |
| Baseline/comparator | Existing author-default `Lagrangep(4,8)` algebraic route and a non-default static setup comparator such as `Lagrangep(3,8)`. |
| Primary criterion | Default `Lagrangep(4,8)` remains source-faithful; non-default order/elements are classified as `extension_or_invention`; preflight budgets use the configured basis dimension; exact guards reject basis drift; focused tests pass. |
| Veto diagnostics | Command-string drift, preflight/fit basis mismatch, parameter-count drift, source-faithfulness overclaim for non-default bases, ALS revival, audit tuning, Phase 7 reopening, or failed local checks. |
| Explanatory diagnostics | Basis dimension, TT parameter count, sample floor, command fidelity, and configured classification/subtype. |
| Not concluded | No degree convergence, no posterior correctness, no KR closure, no HMC readiness, no LEDH comparison, no GPU performance, no production readiness, and no source-faithful claim for non-default degree comparators. |
| Artifact | This result, focused tests, refreshed handoff, and the next degree-comparator subplan. |

## Skeptical Plan Audit

Potential flaws checked before execution:

- Wrong baseline: the repair must preserve `Lagrangep(4,8)` as the only
  source-faithful author default while marking non-default degree comparators
  as extensions.
- Proxy-promotion: passing preflight tests cannot become a degree-convergence
  or production criterion.
- Missing stop conditions: no degree-comparator fit may run until a reviewed
  subplan freezes exact commands and approval boundaries.
- Unfair comparisons: the configurable path records basis order/elements in
  the route manifest and exact guard so later degree comparisons cannot drift
  silently.
- Environment mismatch: all checks are CPU-hidden local diagnostics, not GPU
  evidence.
- Artifact mismatch: the result must preserve Phase 6W rank-passed /
  degree-blocked status and update the next handoff.

Audit result: repair the configurable-basis setup path and focused tests only;
do not run degree fits.

## Implementation Summary

Changed files:

- `bayesfilter/highdim/bases.py`
- `bayesfilter/highdim/__init__.py`
- `scripts/p86_author_lagrangep_phase5_budget_fit.py`
- `tests/highdim/test_p85_configurable_basis_domain.py`
- `tests/highdim/test_p86_phase5_budget_preflight.py`
- `bayesfilter/highdim/sv_mixture_cut4.py`

Runner/basis changes:

- Added default basis constants:
  `P85_AUTHOR_SIR_LAGRANGEP_ORDER=4` and
  `P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS=8`.
- Added degree-comparator classification constants:
  `extension_or_invention` /
  `setup_static_degree_comparator_config`.
- Extended `p85_author_sir_lagrangep_algebraic_product_basis_spec(...)` to
  accept `order` and `num_elems`.
- Preserved `Lagrangep(4,8)` as `source_faithful` / `sir_config`.
- Classified non-default order/elements as `extension_or_invention`.
- Added runner CLI fields `--basis-order` and `--basis-num-elems`.
- Added basis config to preflight payloads and exact-fit expectations.
- Updated exact guards to reject `basis_order` and `basis_num_elems` drift.
- Updated training-base initial cores to use the product-basis dimension
  instead of a hard-coded `33`.
- Added a generic degree-comparator preflight helper that can validate an
  explicit non-default basis preflight command without treating it as one of
  the historical fixed preflight commands.
- Fixed non-default basis command-string spacing so `--basis-num-elems` cannot
  concatenate with the next CLI flag.
- Repaired an import-blocking syntax break in `sv_mixture_cut4.py` by restoring
  the missing `def exact_transformed_sv_independent_panel_zhaocui_tt_filter(`
  header. That file-level fix was necessary because `bayesfilter.highdim`
  imports failed before the focused basis tests could collect.

Test additions:

- Default Phase 5/P86 preflight asserts `basis_config` remains
  `order=4`, `num_elems=8`, dim `33`, author-default true.
- Exact fit guards include default basis fields and reject basis drift.
- P85 non-default `Lagrangep(3,8)` manifest test asserts dim `25` and
  `extension_or_invention` classification.
- P86 degree-comparator helper test asserts non-default order-3 preflight
  payloads are classified as static setup comparators and compute budget from
  basis dim `25`.

## Corrected Budget Note

The order-3/rank-4 degree-comparator helper budget is:

```text
basis_dim = 8 * 3 + 1 = 25
ranks = (1, 4, ..., 4, 1)
P_theta = 1*25*4 + 34*(4*25*4) + 4*25*1
        = 100 + 13600 + 100
        = 13800
minimum_training_samples = 20 * 13800 = 276000
```

This corrects a stale handoff arithmetic note that listed `54600`.

## Local Checks

Commands run:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile bayesfilter/highdim/bases.py bayesfilter/highdim/__init__.py bayesfilter/highdim/sv_mixture_cut4.py scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p86_phase5_budget_preflight.py
git diff --check -- bayesfilter/highdim/bases.py bayesfilter/highdim/__init__.py bayesfilter/highdim/sv_mixture_cut4.py scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p86_phase5_budget_preflight.py
rg -n "[[:blank:]]+$" bayesfilter/highdim/bases.py bayesfilter/highdim/__init__.py bayesfilter/highdim/sv_mixture_cut4.py scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p86_phase5_budget_preflight.py
```

Results:

```text
py_compile passed
48 passed, 2 warnings
git diff --check passed
trailing-whitespace scan found no matches
```

The pytest warning source was TensorFlow Probability deprecation warnings.
TensorFlow also emitted CUDA/cuInit startup noise despite
`CUDA_VISIBLE_DEVICES=-1`; these were CPU-hidden local checks and are not GPU
evidence.

## Decision Table

| Field | Status |
|---|---|
| Decision | Configurable-basis runner repair passed focused local checks. |
| Primary criterion status | Passed locally: default basis remains source-faithful, non-default basis is classified as extension, budgets follow configured basis dimension, and exact guards include basis drift checks. |
| Veto diagnostic status | Passed locally: no ALS revival, no fit execution, no audit tuning, no degree/Phase 7/production claim, no focused check failure. |
| Main uncertainty | Degree convergence itself is still unresolved because no reviewed degree-comparator preflight/fits have run. |
| Next justified action | Review this result and the next degree-comparator preflight subplan, then implement a no-fit degree preflight only if review agrees. |
| What is not being concluded | No degree convergence, no Phase 7 readiness, no posterior correctness, no KR closure, no HMC readiness, no GPU performance, no production readiness, and no source-faithful author claim for non-default bases. |

## Boundary Notes

- Phase 6W rank convergence remains passed under the reviewed same-policy
  rank rule.
- Degree convergence remains blocked until the next reviewed degree-comparator
  preflight phase freezes exact commands and boundaries.
- Non-default basis settings are setup parameters for comparator experiments;
  they are not source-faithful author defaults.
- L1 tuning remains the default Zhao-Cui training-base procedure.
- ALS training remains historical, buggy/stale, and not allowed for fixed
  variant Zhao-Cui training.

## Next Handoff

Drafted next subplan:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-subplan-2026-06-26.md`

The next phase may implement a no-fit degree-comparator preflight. It must not
run degree fits until exact commands, artifacts, criteria, and approval
boundaries are reviewed and frozen.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6x-configurable-basis-runner-repair-result-2026-06-26.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6X result correctly record the configurable-basis runner repair after Phase 6W rank convergence, preserve default Lagrangep(4,8) as source-faithful while classifying non-default basis choices as extension_or_invention, correctly state the order-3/rank-4 parameter budget as P_theta=13800 with sample floor 276000, preserve that no degree fit or Phase 7/production/HMC/source-faithful non-default claim has been made, and hand off safely to a no-fit Phase 6Y degree-comparator preflight? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed the Phase 6W rank-passed / degree-blocked context is
  preserved.
- Claude agreed default `Lagrangep(4,8)` remains source-faithful while
  non-default basis settings are classified as extensions.
- Claude agreed the order-3/rank-4 budget is `P_theta=13800` with sample
  floor `276000`.
- Claude agreed no degree-fit, Phase 7, production, HMC, GPU, or
  source-faithful non-default claim is made.
- Claude agreed the handoff to the no-fit Phase 6Y preflight is safe.

Verdict:

```text
VERDICT: AGREE
```
