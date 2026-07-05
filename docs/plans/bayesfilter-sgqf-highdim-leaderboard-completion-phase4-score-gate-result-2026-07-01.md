# Phase 4 Result: Cross-Row SGQF Analytical Score Gate

Date: 2026-07-01

Status: `SGQF_LEADERBOARD_PHASE4_PARTIAL_PASS_PENDING_FINAL_REGENERATION`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Phase 4 passes for the rows that are newly executable and carry analytical/manual SGQF score provenance, and preserves blocked rows honestly. The predator-prey T20 SGQF row clears the analytical score gate at the reviewed claim level; the SIR and generalized-SV rows remain blocked and are not promoted into score evidence. |
| Primary criterion status | Met locally: every newly executed SGQF row is either value+score admitted with analytical/manual provenance or preserved as blocked/value-only with precise reasons. |
| Veto diagnostic status | Passed locally: no autodiff was admitted as analytical, no value-only row was promoted as gradient evidence, no wrong-target score route was promoted, and no blocked row was silently upgraded. |
| Main uncertainty | Final leaderboard admission still depends on Phase 5 regeneration, which must rewrite the authoritative artifacts consistently. |
| Next justified action | Execute Phase 5 and regenerate the authoritative highdim leaderboard artifacts from the reviewed SGQF row states. |
| What is not being concluded | No HMC readiness, no top-level API promotion, and no production/default claim. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Do the newly executed SGQF rows carry analytical/manual score provenance and same-scalar support well enough to be admitted as value+score leaderboard cells? |
| Baseline/comparator | reviewed row contracts and value-passing SGQF rows from Phases 1-3. |
| Primary criterion | Passed locally for the rows that are executable in the current program scope: predator-prey T20 passes the SGQF analytical score gate, while SIR and generalized-SV remain blocked with precise reasons that the final leaderboard can represent without ambiguity. |
| Veto diagnostics | Passed locally: no autodiff admitted as analytical, no value-only row promoted as gradient evidence, no wrong-target score route promoted, and no unexplained approximation gap used as admission evidence. |
| Explanatory diagnostics | same-branch FD checks, score norms, runtime, branch/failure labels, and row-specific nonclaims. |
| Not concluded | No HMC readiness, no top-level API promotion, and no production/default claim. |
| Artifact | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase4-score-gate-result-2026-07-01.md` and refreshed `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase5-final-regeneration-subplan-2026-07-01.md`. |

## Cross-Row Score Gate Summary

### Admitted through the SGQF analytical score gate in this completion program

1. **Predator-prey T20 SGQF row**
   - status: value+score admitted at the reviewed row scope
   - score provenance class: analytical/manual fixed-branch SGQF score route
   - preserved policy: approximate-but-explained remains allowed; this does not imply HMC, production, or default-policy readiness

### Preserved blocked rows

2. **Spatial SIR SGQF row**
   - remains blocked because no full observed-data SGQF evaluator and no row-level admitted analytical/manual score route exist
   - not promoted as value-only or score evidence

3. **Generalized-SV SGQF source row**
   - remains blocked because no reviewed same-row SGQF evaluator and no admitted analytical/manual score route exist
   - native-oracle, precursor, and auxiliary evidence remain debugging-only

### Preserved baseline rows (already complete before this program)

4. **Affine LGSSM SGQF row**
   - preserved baseline `executed_value_score`

5. **Actual SV SGQF row**
   - preserved baseline `executed_value_score`

6. **KSC surrogate SV SGQF row**
   - preserved baseline `executed_value_score`

## Local Checks

Commands actually run:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_predator_prey_filtering.py::test_p47_m5_fixed_sgqf_predator_prey_single_parameter_score_matches_fd_same_branch \
  tests/highdim/test_p47_predator_prey_filtering.py::test_p47_m5_fixed_sgqf_predator_prey_multistep_score_matches_fd_for_all_parameters \
  tests/highdim/test_p47_predator_prey_filtering.py::test_p47_m5_fixed_sgqf_predator_prey_fd_ladder_preserves_same_branch_contract \
  tests/highdim/test_p47_predator_prey_filtering.py::test_p47_m5_fixed_sgqf_score_gap_to_dense_score_is_finite \
  tests/highdim/test_p47_predator_prey_filtering.py::test_p47_m5_fixed_sgqf_vs_ukf_score_gap_is_finite
```

Outcome:

- Focused predator-prey SGQF score-gate tests passed: `5 passed, 2 warnings in 68.56s`.
- No SGQF SIR or generalized-SV score route was run because those rows remain blocked by reviewed row contracts.

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: the gate was applied only to rows with reviewed row contracts and reviewed SGQF value support. |
| Proxy metric promoted | Avoided: score-gate passage is scoped row evidence only, not HMC or production evidence. |
| Missing stop condition | Avoided: blocked rows remained blocked and were not coerced into partial score admission. |
| Unfair comparison | Avoided: predator-prey same-row analytical/manual score evidence was evaluated separately from SIR/generalized-SV blocked states. |
| Hidden assumption | Avoided: existing SGQF baseline rows were preserved rather than re-adjudicated. |
| Stale context | Avoided: row states remain anchored to the reviewed July 1 leaderboard artifact plus this program's row-specific results. |
| Environment mismatch | Avoided: the score-gate runtime was CPU-only with explicit GPU hiding. |
| Artifact-answer mismatch | Avoided: the result records a partial pass with blocked rows preserved, not a false “everything passed” closeout. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Worktree status | Dirty pre-existing research/doc worktree; unrelated dirty changes preserved. |
| Execution target | Cross-row SGQF analytical score gate for newly executable rows. |
| CPU/GPU status | CPU-only TensorFlow test run with `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA command was run. |
| Commands | See Local Checks command above. |
| Data version | `N/A` (existing fixture/unit-test evidence only) |
| Random seeds | `N/A` (existing fixture/unit-test evidence only) |
| Wall time | `N/A` (no dedicated benchmark timing artifact for Phase 4) |
| Plan | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase4-score-gate-subplan-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase4-score-gate-result-2026-07-01.md` |
| Refreshed Phase 5 subplan | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase5-final-regeneration-subplan-2026-07-01.md` |

## Phase 5 Handoff

Phase 5 may start only after the ledgers record that:

- predator-prey T20 SGQF row is value+score admitted at the reviewed row scope;
- SIR SGQF row remains blocked;
- generalized-SV SGQF row remains blocked;
- the already-complete SGQF baseline rows remain preserved;
- the Phase 4 result is reviewed `AGREE`;
- the refreshed Phase 5 subplan is reviewed `AGREE`.

Phase 5 must now regenerate the authoritative highdim leaderboard artifacts and
close the SGQF completion program without silently upgrading any blocked row.
