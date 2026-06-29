# P87 Phase 5 Result: Tiny Full-History Exact Regression

Date: 2026-06-27

Status: `P87_PHASE5_TINY_FULL_HISTORY_PASS_REVIEWED_CLOSED`

## Decision

Phase 5 passed the tiny full-history fixed-branch regression gate under
CPU-hidden local execution.

The evidence supports only this claim:

> The repaired JVP-free fixed-design score route propagates value and score
> information through tiny d2 multistate full-history fixtures, preserves
> same-branch finite-difference rows, and matches dense versus streaming
> transition value/derivative references on the reviewed tiny fixtures.

`BLOCK_D18_ALL_PAIRS_DRIFT` and `BLOCK_HORIZON0_OVERCLAIM` remain active for
every SIR d18 full-history claim. This phase does not establish SIR d18
full-history feasibility, source-route correctness, HMC readiness, production
readiness, GPU readiness, LEDH comparison, training readiness, or a
default-policy change.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `97ad05d` |
| Repository root | `/home/chakwong/BayesFilter` |
| Execution target | CPU-only local tiny full-history gate |
| CPU-only enforcement | `CUDA_VISIBLE_DEVICES=-1` on Python/pytest commands |
| Tensor dtype | `tf.float64` in the tested fixtures |
| Network/model access | None for local checks; Claude review is external/read-only after this result |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-subplan-2026-06-26.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-result-2026-06-26.md` |

## Checks Run

```bash
env CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py
```

Result: passed.

```bash
env CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate and score"
```

Result: passed, `3 passed, 20 deselected, 2 warnings`.

Warnings were TensorFlow Probability deprecation warnings from
`distutils.version` checks; they are explanatory only and did not affect the
Phase 5 gate.

## Evidence Table

| Evidence item | Status | Notes |
| --- | --- | --- |
| Tiny two-row multistate score path | Passed | Targeted pytest includes `test_multistate_fixed_design_tt_score_path_matches_same_branch_fd_for_tiny_two_row_fixture`. |
| Same-branch FD rows | Passed | Test asserts plus/minus/base branch hashes stay equal for scored FD rows. |
| Dense versus streaming predictive parity | Passed | Targeted pytest includes streaming predictive parity checks selected by `multistate and score`. |
| Dense versus streaming derivative parity | Passed | Targeted pytest includes streaming derivative parity checks selected by `multistate and score`. |
| Streaming fallback route | Passed | Targeted pytest includes the score-path fallback selected by `multistate and score`. |
| CPU-only enforcement | Passed | Python/pytest commands used `CUDA_VISIBLE_DEVICES=-1` before TensorFlow imports. |
| d18 full-history limitation | Preserved | No d18 all-pairs or streamed all-pairs command was run or claimed. |

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Tiny full-history fixed-branch regression gate passes. |
| Primary criterion | Met for tiny d2 multistate fixtures only. |
| Veto diagnostics | No transition derivative mismatch in targeted tests; no branch drift in asserted FD rows; no retained derivative shape error; no d18 all-pairs promotion; CPU-only enforcement recorded. |
| Main uncertainty | SIR d18 full-history feasibility still requires a non-all-pairs route with explicit derivative semantics and memory/rank contract. |
| Next justified action | Review/refine Phase 6 as a d18 full-history feasibility route gate, not an execution shortcut. |
| What is not concluded | SIR d18 full-history correctness or feasibility, source-route correctness, HMC/production readiness, GPU readiness, LEDH/training/default readiness. |

## Phase 6 Handoff

Phase 6 may proceed because this result and the refreshed Phase 6 subplan
received read-only review. The Phase 6 handoff remains a route-feasibility
gate: it must select or block a non-all-pairs route with explicit derivative
semantics and bounded memory/rank contract before any d18 full-history
execution is attempted.

The refreshed handoff artifact is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-subplan-2026-06-26.md`
