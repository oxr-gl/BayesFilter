# P87 Phase 5 Subplan: Tiny Full-History Exact Regression

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE5_EXECUTION`

## Phase Objective

Certify multi-row transition derivative propagation on tiny d2/d3 fixtures
where dense and streaming references are feasible, without promoting the
evidence to d18 full-history feasibility.

## Entry Conditions Inherited From Previous Phase

- Phase 4 passed horizon-0 SIR d18 value/gradient evidence with
  `BLOCK_HORIZON0_OVERCLAIM` preserved.
- Phase 4 did not claim d18 full-history feasibility.
- Phase 2 JVP-free repair sentinel remains active for the Phase 2 repair scope.
- Phase 5 is tiny-fixture full-history evidence only; it is not a d18 run.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-result-2026-06-26.md`
  - The result must record the CPU-only command manifest, including
    `CUDA_VISIBLE_DEVICES=-1` for Python/pytest commands.
- Focused tests in `tests/highdim/test_fixed_branch_derivatives.py`.
- Updated Phase 6 subplan.

## Required Checks/Tests/Reviews

Allowed edit scope:

- `tests/highdim/test_fixed_branch_derivatives.py`
- `bayesfilter/highdim/filtering.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-result-2026-06-26.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-subplan-2026-06-26.md`
- P87 execution/review ledgers

Allowed read/check scope:

- The allowed edit scope above.
- P87 plan files matched by `docs/plans/bayesfilter-highdim-zhao-cui-p87*.md`
  for diff hygiene only.

Any broader implementation edit, d18 full-history execution, source-route,
GPU, HMC, training, or default-policy change requires a refreshed reviewed
subplan.

Execution environment:

- Repository root: `/home/chakwong/BayesFilter`.
- Execution target: local CPU-only tiny-fixture gate; no GPU/CUDA command is
  required or allowed in Phase 5.
- CPU-only enforcement: every Python/pytest command below must be launched with
  `CUDA_VISIBLE_DEVICES=-1` before TensorFlow imports.
- Python environment: current active repository Python environment used by
  Phases 2-4 focused checks.
- Tensor dtype: float64.
- Network/model access: none during local checks; Claude is read-only review
  only.

```text
env CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py
env CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate and score"
git diff --check -- bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Claude review required for implementation/result changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does tiny full-history fixed-branch value/score propagation pass same-branch FD and dense/streaming transition derivative checks without promoting to d18? |
| Baseline/comparator | Tiny d2 multistate same-branch FD rows, dense-vs-streaming predictive parity, dense-vs-streaming derivative parity, and branch hashes. |
| Primary criterion | Tiny two-row multistate score test passes, dense/streaming derivative parity tests pass, branch hashes stay stable where asserted, and no d18 full-history claim is made. |
| Veto diagnostics | Transition derivative mismatch, branch drift, retained derivative shape error, all-pairs d18 promotion, CPU-only command not enforced. |
| Explanatory diagnostics | FD residuals, branch hashes, dense/streaming parity rows. |
| Not concluded | d18 full-history feasibility, source-route correctness, HMC/production readiness, GPU readiness. |
| Artifact | Phase 5 result and tests, with CPU-only command manifest recorded. |

## Forbidden Claims/Actions

- Do not promote tiny evidence to d18.
- Do not run d18 all-pairs.
- Do not alter pass/fail criteria after seeing results.
- Do not claim source-route correctness, HMC readiness, production readiness,
  GPU readiness, or default-policy readiness.
- Do not revive ALS training, training-base sweeps, or rank/degree claims.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only if:

- Phase 5 tiny full-history evidence passes with CPU-only manifest recorded;
- Phase 5 result explicitly says the evidence is tiny-fixture only and does
  not prove d18 full-history feasibility;
- Phase 6 subplan is refreshed as a d18 full-history feasibility/route gate,
  not an execution shortcut;
- Phase 6 subplan is reviewed.

## Stop Conditions

- Tiny dense reference mismatch.
- Route requires all-pairs d18 transition.
- CPU-only command enforcement is missing.
- Claude review nonconvergence after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 5 result/close record.
3. Draft or refresh Phase 6 subplan.
4. Review Phase 6 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
