# Phase 2 Result: Predator-Prey T20 SGQF Row Completion

Date: 2026-07-01

Status: `SGQF_LEADERBOARD_PHASE2_LOCAL_PASS_PENDING_REVIEW`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | The predator-prey T20 SGQF row is no longer blocked at the row-contract / focused-evidence level. Existing reviewed SGQF predator-prey value and analytical-manual score evidence already covers a same-row T20 source-scope route, so the row can advance from `blocked` to a reviewed candidate `executed_value_score` state pending final score-gate and leaderboard regeneration phases. |
| Primary criterion status | Met locally: the reviewed T20 row contract, the existing SGQF predator-prey value route, and the analytical-manual score evidence are aligned at the same row/target level. |
| Veto diagnostic status | Passed locally: lower-rung evidence was not silently substituted for the T20 row, autodiff was not admitted as analytical provenance, and no wrong-target scalar promotion was made. |
| Main uncertainty | Final leaderboard admission still depends on the cross-row SGQF analytical score gate and final regeneration phase. |
| Next justified action | Advance to Phase 3 and freeze the generalized-SV SGQF source-row contract while preserving the predator-prey row as a locally passed SGQF candidate. |
| What is not being concluded | No HMC readiness, no production/default claim, and no broad SGQF exactness claim beyond the reviewed predator-prey T20 row. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the predator-prey T20 SGQF row be tied to a reviewed same-row value/analytical-score evaluator, or must it remain blocked with a precise target/evaluator/derivative gap? |
| Baseline/comparator | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`, `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`, `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`, `docs/plans/bayesfilter-source-scope-sgqf-admission-ledger-2026-06-24.md`, `docs/plans/bayesfilter-source-scope-sgqf-analytical-gradient-ledger-2026-06-24.md`, and `tests/highdim/test_p47_predator_prey_filtering.py`. |
| Primary criterion | Passed locally: the row has a reviewed T20 source-row identity, a finite SGQF value path, and analytical/manual score evidence tied to the same declared scalar. |
| Veto diagnostics | Passed locally: lower-rung evidence was not promoted as the T20 row by itself, autodiff was not admitted as analytical, no wrong-target scalar/score promotion occurred, and the same-row score evidence is present. |
| Explanatory diagnostics | Value magnitude, score norm, same-branch FD checks, and score-gap diagnostics are available in the predator-prey SGQF test family. |
| Not concluded | No HMC readiness, no production/default claim, and no broad SGQF claim beyond the reviewed T20 row. |
| Artifact | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-result-2026-07-01.md` and refreshed `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase3-generalized-sv-subplan-2026-07-01.md`. |

## Reviewed Row Contract Summary

Current reviewed row identity:

```text
zhao_cui_predator_prey_T20
```

Current reviewed SGQF row basis:

- source-scope predator-prey T20 row identity is fixed by the source-scope
  artifact and current leaderboard artifacts;
- the SGQF evaluator route exists through
  `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py` and is exercised
  in `tests/highdim/test_p47_predator_prey_filtering.py`;
- the existing SGQF predator-prey tests already include:
  - same-target value comparison versus dense reference,
  - single-parameter same-branch FD score check,
  - multi-parameter FD score check,
  - same-branch FD ladder checks,
  - score-gap-to-dense and score-gap-to-UKF finiteness checks.

Reviewed row-contract conclusion:

- the SGQF predator-prey row is a same-row T20 source-scope candidate with
  analytical/manual score evidence already present;
- it should no longer remain blocked solely on the old `blocked_target_alignment`
  status.

## Local Checks

Commands actually run:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p47_predator_prey_filtering.py
```

```bash
python -m compileall -q bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py tests/highdim/test_p47_predator_prey_filtering.py
```

```bash
git diff --check -- bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py tests/highdim/test_p47_predator_prey_filtering.py docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-*.md
```

Outcome:

- Focused CPU-only predator-prey SGQF pytest passed: `19 passed, 2 warnings in 148.28s`.
- `compileall` passed.
- Diff hygiene passed.
- The only code repair needed was restoring the import of `TFFixedSGQFDerivatives`
  in `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py` so the already-
  reviewed predator-prey analytical score route remained runnable after the
  generic structural-admission refresh.

## Key Supporting Evidence

Most relevant existing predator-prey SGQF checks from
`tests/highdim/test_p47_predator_prey_filtering.py`:

- same-target value row check versus dense reference
- single-parameter same-branch FD analytical score check
- multi-parameter same-branch FD analytical score check
- same-branch FD ladder preservation checks
- SGQF score gap to dense score is finite
- SGQF score gap to UKF score is finite

This is sufficient local evidence to move the row from blocked alignment status
into the cross-row analytical score gate.

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: the row is anchored to the T20 source-scope identity, not just lower-rung evidence. |
| Proxy metric promoted | Avoided: passing the predator-prey family tests is recorded as row-level SGQF candidate evidence only; final leaderboard promotion still waits for the cross-row score gate. |
| Missing stop condition | Avoided: if the tests had failed or the row contract had been inconsistent, the row would have remained blocked. |
| Unfair comparison | Avoided: lower-rung evidence is treated as support only insofar as it demonstrably covers the same T20 row/value-score route, not as a different target. |
| Hidden assumption | Avoided: the row is not promoted to exactness; approximate-but-explained policy remains intact. |
| Stale context | Avoided: the authoritative July 1 leaderboard and source-scope artifacts remain the baseline. |
| Environment mismatch | Avoided: checks were CPU-only with explicit GPU hiding. |
| Artifact-answer mismatch | Avoided: the result records the exact local route and exact tests run rather than narrating a generic “likely works” story. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Worktree status | Dirty pre-existing research/doc worktree; unrelated dirty changes preserved. |
| Execution target | Focused predator-prey T20 SGQF row completion phase. |
| CPU/GPU status | CPU-only TensorFlow test run with `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA command was run. |
| Commands | See Local Checks commands above. |
| Data version | `N/A` (existing fixture/unit-test evidence only) |
| Random seeds | `N/A` (existing fixture/unit-test evidence only) |
| Wall time | `N/A` (no dedicated benchmark timing artifact for Phase 2) |
| Plan | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-subplan-2026-07-01.md` |
| Row contract | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-row-contract-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-result-2026-07-01.md` |
| Refreshed Phase 3 subplan | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase3-generalized-sv-subplan-2026-07-01.md` |

## Phase 3 Handoff

Phase 3 may start only after the ledgers record that:

- the predator-prey T20 SGQF row is now a reviewed same-row candidate rather
  than a stale `blocked_target_alignment` cell;
- the Phase 2 result is reviewed `AGREE`;
- the refreshed Phase 3 subplan is reviewed `AGREE`;
- and the row still carries approximate-but-explained and no-HMC/no-production
  nonclaims until the later cross-row score gate and final regeneration closeout.

Phase 3 must now freeze the generalized-SV SGQF source-row contract and either
implement or block that row honestly.
