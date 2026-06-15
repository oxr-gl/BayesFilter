# Fixed-SGQF Merge-Fix Plan

metadata_date: 2026-06-15
program_id: fixed-sgqf-merge-fix
status: EXECUTION_READY

## Purpose

This plan governs a narrow corrective follow-up after the fixed-SGQF
source-authority audit.  The audit found that higher-level cloud construction is
not source-faithful because distinct higher-level GHQ nodes can be merged into
one bucket by the current implementation.  The immediate purpose is to repair
that merge behavior, then rerun the exact higher-level probes that previously
looked suspicious.

## Governing references

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p49-fixed-sgqf-source-authority-audit-2026-06-15.md`
- `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`

## Skeptical plan audit

Status target: `PASS_TO_NARROW_FIX_AND_RERUN`

Risks to guard against:

1. **Symptom masking**
   - suppressing downstream failures without restoring the cloud would be the
     wrong fix.
2. **Level-2 regression**
   - current level-2 rows are strong and must remain green.
3. **Incorrect pruning order**
   - pruning before all signed contributions are merged would leave the cloud
     inconsistent even after the bug fix.
4. **Misreading branch-hash churn**
   - higher-level branch hashes should change after the fix because cloud payloads
     are part of branch identity.

## Evidence contract

Question:

Does a source-faithful merge fix restore higher-level SGQF clouds and change the
interpretation of the observed higher-level `carried_covariance` failures?

Primary pass criterion:

- 1D level-3 cloud no longer collapses to 3 nodes;
- higher-level cloud point sets and moments become more source-consistent;
- level-2 tests stay green;
- reruns show whether higher-level value/score failures persist after the cloud
  correction.

Veto diagnostics:

- level-2 regressions break;
- higher-level cloud still collapses distinct nodes;
- the rerun result claims more than the local evidence supports.

Explanatory-only diagnostics:

- point counts before/after fix,
- branch-hash changes,
- whether higher-level failures disappear, move, or persist.

## Code surfaces

Primary implementation surface:
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`

Primary test surfaces:
- `tests/test_fixed_sgqf_tf.py`
- `tests/test_fixed_sgqf_values_tf.py`
- `tests/test_fixed_sgqf_scores_tf.py`

Secondary rerun-only surfaces:
- `tests/test_fixed_sgqf_branch_contract_tf.py`
- `tests/test_fixed_sgqf_audit_tf.py`
- `tests/test_fixed_sgqf_testing_integration_tf.py`
- `tests/test_fixed_sgqf_verification_tf.py`

## Execution steps

1. Write this p50 plan artifact.
2. Replace the current bucket-based approximate merge in the fixed cloud builder
   with a source-faithful duplicate search using the declared sup-norm merge
   tolerance.
3. Ensure pruning happens only after all signed contributions are accumulated.
4. Add or adjust cloud-level regressions so higher-level cloud collapse is pinned
   directly.
5. Rerun cloud-only tests.
6. Rerun higher-level value and score tests.
7. Rerun the remaining SGQF contract/helper suite.
8. Re-run focused higher-level probes from the earlier P3/P4/P6 results.
9. Write the p51 result note.

## Verification ladder

1. `tests/test_fixed_sgqf_tf.py`
2. `tests/test_fixed_sgqf_values_tf.py`
3. `tests/test_fixed_sgqf_scores_tf.py`
4. remaining `tests/test_fixed_sgqf_*.py`
5. focused probe reruns for:
   - 1D level-3 / level-4 clouds,
   - 2D level-3 cloud,
   - 3D level-3 affine row,
   - previously observed higher-level `carried_covariance` rows.

## Deliverables

- Plan:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p50-fixed-sgqf-merge-fix-plan-2026-06-15.md`
- Result:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p51-fixed-sgqf-merge-fix-result-2026-06-15.md`
