# Phase Result: Fixed-SGQF Inventory and Evidence Contract

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p0-inventory-and-evidence-contract-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`

## Status
- Outcome token: `PASS_P0_FIXED_SGQF_INVENTORY_READY_FOR_EXECUTION_PHASES`
- Decision class: `pass`

## Command actually run
```bash
rg -n "FixedBranchSquaredTTFilter|fixed_sgqf|SGQF|dense_projection_first_step|tf_svd_sigma_point_filter|tf_svd_cut4_filter|tf_svd_ukf_score|tf_svd_cut4_score|tf_svd_cubature_score" bayesfilter tests docs experiments
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_verification_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| environment | `anaconda3/envs/tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p0-inventory-and-evidence-contract-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p0-inventory-and-evidence-contract-result-2026-06-14.md` |
| baseline suite status | `27 passed before expansion` |
| expanded suite status at closeout time | `38 passed` |

## Result summary
P0 passed. I froze the fixed-SGQF lane into four evidence classes and mapped the
known gaps G1-G8 onto the later execution phases.

### Coverage / ownership matrix
| Gap | Current evidence at execution start | Evidence label | Owning phase | Notes |
|---|---|---|---|---|
| G1 multistep nonlinear dense-reference | one-step scalar quadratic vs dense projection | `dense_numerical_reference` | P1 | needed recursive multistep extension |
| G2 higher-dimensional accepted-path validation | 1D accepted paths; 2D hard-interaction limit note | `contract_failure` + local value evidence | P2 | needed explicit higher-dimensional accepted-path rows |
| G3 cloud exactness beyond current small cases | 1D rules, 3D level-2 preview | `contract_failure` / construction evidence | P3 | needed broader `(dim, sparse_level)` ladder |
| G4 later-time / later-stage failure coverage | previous/predictive/innovation/cloud failures | `contract_failure` | P2 | needed carried-covariance and later-time coverage |
| G5 broader score/FD coverage | one-step scalar beta score | `dense_numerical_reference` + same-branch contract | P5 | needed multi-parameter and multistep rows |
| G6 multidimensional affine exact-vs-Kalman | 1D affine exactness only | `exact_reference` | P4 | needed 2D/3D exact rows |
| G7 same-target baseline comparison ladder | no fixed-SGQF-vs-baseline panel | `baseline_only` planned | P7 | same-target eligibility required |
| G8 sparse-level ladder vs dense | no explicit level ladder | `dense_numerical_reference` planned | P6 | needed level-by-level comparison |

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| baseline SGQF suite pass count | 27 | starting evidence base was real, not empty |
| current SGQF evidence families | 4 | exact-reference, dense-reference, baseline-only, contract/failure |
| identified gaps | 8 | all gaps mapped to later phases |
| orphan gaps after inventory | 0 | phase ownership complete |

## Engineering observations
- The fixed-SGQF lane was already coherent enough to support an overnight-style
  execution ladder.
- Existing helper surfaces were sufficient to start execution:
  `dense_projection_first_step`, affine Kalman conversion, and sigma-point
  backends already existed.
- The main risk was not missing scaffolding; it was overclaiming from local
  fixtures.

## Empirical evidence
- The pre-expansion SGQF suite passed locally.
- The inventory confirmed that later phases could reuse current SGQF tests
  rather than invent new lane definitions.

## Mathematical claims
- No new mathematical claim.  P0 is a governance and classification phase.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P0 and continue | satisfied | no label-mismatch veto triggered | later phases may still hit genuine reference-scope blockers | run P4 exact affine ladder first | no new numerical claim from inventory alone |

## Next step
- Continue to P4 using exact affine/Kalman rows as the first low-ambiguity
  expansion rung.
