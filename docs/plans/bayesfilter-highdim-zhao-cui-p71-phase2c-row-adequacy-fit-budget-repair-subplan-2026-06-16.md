# P71 Phase 2c Subplan: Row-Adequacy Fit-Budget Repair

metadata_date: 2026-06-16
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 2c

## Phase Objective

Repair the Phase 2 execution-only harness and focused tests so they respect
the already-reviewed P70 row-adequacy rule:

```text
n_hard = max(4, ceil(D/4), (degree + 1) * rank * rank)
```

For the d18 source-route target, `D=36`, `degree=0`, and `rank=1`, so the hard
minimum is `9` rows.  The repair must make this budget visible in the Phase 2
artifacts and must not weaken the row-adequacy veto.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed current-evidence/source-anchor reset.
- Phase 1 passed condition-veto diagnostic capture and Claude review.
- Phase 2 direct execution-only reproduction failed first on
  `diagnostic_data_all_local_entries_clipped`.
- Phase 2b made all-clipped post-fit diagnostic channels nonfatal and
  unavailable for validation, then focused pytest failed on
  `branch_fit_row_adequacy_failed`.
- No d18 accuracy, rank convergence, scaling, or HMC claim has been made.

## Required Artifacts

- Phase 2c result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2c-row-adequacy-fit-budget-repair-result-2026-06-16.md`.
- Focused code/test patch limited to Phase 2 execution-only row-budget
  handling and manifest observability, including the direct P59-9d runner
  manifest API and script surface.
- Updated Phase 2 result note after the rerun, if the rerun passes.
- Machine-readable Phase 2 JSON manifest if the rerun passes.
- Updated P71 visible execution ledger and stop handoff.

## Skeptical Audit Before Execution

The Phase 2b failure is not a reason to lower the P70 hard row threshold.  The
wrong baseline is the stale two-row smoke fixture.  The phase artifact that
answers the question is an execution-only rerun using a predeclared admissible
row budget, plus focused tests that prove the old two-row budget fails closed
or is no longer used as a pass fixture.

This plan does not change rank, degree, ridge, condition thresholds, sweep
policy, source-route density callbacks, or validation pass criteria after
seeing output.  The row count `9` follows from the prior P70 formula and was
confirmed before any accuracy, rank, scaling, or HMC run.  The helper/constant
introduced in this phase is for default fixture selection and manifest
reporting only; it must not silently rewrite a caller-supplied
`fit_sample_count=2` into `9`.

## Required Checks/Tests/Reviews

Before code edits:

```bash
rg -n "branch_fit_row_adequacy_failed|fit_sample_count=2|fit_sample_count: int = 2|p59_author_sir_validation_ladder|p59_author_sir_runner_manifest_path|p60_author_sir_same_route_rank_comparator" bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py tests/highdim/test_p59_author_sir_runner_manifest.py tests/highdim/test_p60_author_sir_rank_comparator.py scripts/p59_author_sir_m9_runner_manifest.py
```

After code edits:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py tests/highdim/test_p59_author_sir_runner_manifest.py tests/highdim/test_p60_author_sir_rank_comparator.py scripts/p59_author_sir_m9_runner_manifest.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_validation_ladder.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_runner_manifest.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p60_author_sir_rank_comparator.py
git diff --check -- bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py tests/highdim/test_p59_author_sir_runner_manifest.py tests/highdim/test_p60_author_sir_rank_comparator.py scripts/p59_author_sir_m9_runner_manifest.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2c-row-adequacy-fit-budget-repair-subplan-2026-06-16.md
```

Then rerun the Phase 2 execution-only command with CPU-only CUDA hiding and
write the JSON manifest.

Claude read-only review is required before implementation and again if the
implementation changes the Phase 2 evidence contract.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the d18 execution-only Phase 2 harness run with a row budget admissible under the frozen P70 hard row-adequacy rule? |
| Baseline/comparator | Phase 2b blocker: old `fit_sample_count=2` fixture raises `branch_fit_row_adequacy_failed`; P70 hard minimum for D=36, degree 0, rank 1 is 9. |
| Primary criterion | Focused tests pass with the admissible row budget; direct P59-9d runner manifest tests pass; the Phase 2 execution-only rerun writes a JSON manifest with finite log marginal likelihood, finite normalizer increments, ESS by step, branch hashes, row-adequacy metadata, and nonclaims. |
| Veto diagnostics | Lowering or bypassing row adequacy; changing rank/degree/ridge/sweeps/thresholds/seeds after output; hiding the old two-row failure; promoting execution-only evidence to accuracy/rank/scaling/HMC claims; using missing holdout/replay diagnostics as validation evidence. |
| Explanatory diagnostics | Row count, `n_hard`, `n_preferred`, fit-quality diagnostics, holdout/replay availability, ESS, normalizer increments, correction-weight ranges, branch hashes. |
| Not concluded | No d18 filtering accuracy, no same-route rank convergence, no correctness, no d50/d100 scaling, no HMC readiness. |
| Artifact | Phase 2c result note, focused test output, and Phase 2 JSON manifest if the rerun passes. |

## Proposed Repair Shape

- Introduce a small helper or constant for the d18 execution-only admissible
  fit row budget derived from `_p70_row_adequacy_diagnostics`.  The helper is
  for defaults and reporting only, not for auto-clamping explicit user input.
- Update the P59 runner/validation defaults and focused P59/P60 tests from the
  stale two-row fixture to the admissible row budget.
- Preserve fail-closed behavior for explicitly under-rowed calls by adding or
  retaining a test that `fit_sample_count=2` raises or blocks with
  `branch_fit_row_adequacy_failed`.
- Update direct P59-9d runner manifest tests and
  `scripts/p59_author_sir_m9_runner_manifest.py` coverage if its default or
  manifest output changes.
- Add manifest fields exposing the execution-only `fit_sample_count` and
  row-adequacy metadata so future artifacts show why 9 rows were used.  The
  Phase 2 JSON manifest itself must carry machine-readable fields such as
  effective `fit_sample_count` and per-step `row_adequacy` with `status`,
  `row_count`, `n_hard`, `n_preferred`, `max_core_columns`, threshold role, and
  nonclaim text; nested P59-9b assembly diagnostics alone are insufficient.
- Keep Phase 2 execution-only as execution-only: no accuracy, rank
  convergence, d50/d100, GPU, or HMC run.

## Forbidden Claims/Actions

- Do not lower, bypass, or retune P70 row adequacy.
- Do not change the SIR model, observations, density callbacks, transport
  target, rank, degree, ridge, sweep count/order, condition thresholds, or
  seeds.
- Do not use Phase 2 as an accuracy, rank-convergence, scaling, or HMC gate.
- Do not proceed to Phase 3 until Phase 2 rerun passes and is recorded.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- Phase 2c focused checks pass;
- Claude review does not identify a material blocker;
- Phase 2 execution-only rerun passes and writes the JSON manifest;
- Phase 2 result records row-adequacy metadata and explicit nonclaims.

If these conditions are not met, write a Phase 2c blocker result and stop.

## Stop Conditions

Stop and write a blocker if:

- an admissible row budget still fails with condition-number veto or another
  fitter failure;
- the only available repair would weaken P70 row adequacy;
- focused tests cannot distinguish an under-rowed fixture from an admissible
  execution-only fixture;
- Claude and Codex do not converge after five material review rounds.
