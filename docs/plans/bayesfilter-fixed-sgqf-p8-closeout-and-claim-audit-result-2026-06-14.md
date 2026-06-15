# Phase Result: Fixed-SGQF Closeout and Claim Audit

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p8-closeout-and-claim-audit-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`
- superseding cloud-construction update:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p51-fixed-sgqf-merge-fix-result-2026-06-15.md`

## Status
- Outcome token: `PASS_P8_FIXED_SGQF_CLOSEOUT_COMPLETE`
- Decision class: `pass_with_explicit_nonclaims`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_verification_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| environment | `anaconda3/envs/tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| original-program suite status at first closeout | `38 passed, 2 warnings` |
| current repaired-lane suite status | `41 passed, 2 warnings` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p8-closeout-and-claim-audit-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p8-closeout-and-claim-audit-result-2026-06-14.md` |
| governing update | `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p51-fixed-sgqf-merge-fix-result-2026-06-15.md` |

## Result summary
The original fixed-SGQF program still closes as a pass, but this closeout is now
explicitly reconciled with the post-fix merge-fix rerun.

The earlier pre-fix interpretation that higher-level cloud behavior itself was a
local SGQF limitation on the tested scalar and affine rows is superseded. The
source-authority audit and the p51 merge-fix result showed that the higher-level
merge bug was real, and once repaired:
- higher-level clouds become source-consistent on the tested rows,
- 2D level-3 cloud covariance mismatch disappears,
- scalar level-3/4/5 `carried_covariance` failures disappear on the tested row,
- 3D affine level-3 also matches exact Kalman.

Two implementation fixes now govern the current lane:
1. rank-safe `_symmetrize(...)` for derivative-path tensors;
2. source-faithful higher-level cloud merge repair.

The current fixed-SGQF suite passes locally with the repaired lane:
- `41 passed, 2 warnings`.

## Required closure matrix
| Gap | Status | Supporting phase(s) | Evidence class | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|---|
| G1 multistep nonlinear dense-reference | `closed` | P1 | `dense_numerical_reference` | only one selected 1D nonlinear fixture | add harder nonlinear fixtures if needed | no general nonlinear exactness claim |
| G2 higher-dimensional accepted-path validation | `partially_closed` | P2, P4 | `exact_reference`, `contract_failure` | nonlinear higher-dimensional accepted paths remain thinner than affine ones | add additional nonlinear accepted-path fixtures if needed | no blanket higher-dimensional pass claim |
| G3 cloud exactness beyond current small cases | `closed` | P3 plus p51 | `contract_failure` / tested-moment evidence | broader higher-level clouds beyond tested rows still need case-specific evidence | extend cautiously only if a consumer needs it | no all-moment or all-level exactness claim |
| G4 later-time and later-stage failure coverage | `partially_closed` | P2, P5 | `contract_failure` | deterministic `time_index > 0` failure row still missing | keep explicit blocker; search broader fixtures only if needed | no claim that all stage/time combinations are covered |
| G5 broader score/FD coverage | `closed` | P5 | `dense_numerical_reference` + same-branch score evidence | broader higher-dimensional and stochastic-score rows remain open | add more fixtures only if a consumer needs them | no stochastic-score or HMC readiness claim |
| G6 multidimensional affine exact-vs-Kalman parity | `closed` | P4 plus p51 | `exact_reference` | still local to tested rows | use these rows as exact anchors | no claim that every future higher-level row automatically inherits parity |
| G7 same-target baseline comparison ladder | `closed` | P7 | `baseline_only` | only one selected fixture panel was run; CUT4 not eligible there | add broader same-target panels if needed | no universal ranking claim |
| G8 sparse-level ladder vs dense | `closed` | P6 plus p51 | `dense_numerical_reference` | ladder is still local to the tested scalar row | keep the repaired level ladder as current evidence | no general convergence or monotonic-improvement claim |

## Supported claims
1. **Exact-reference affine support is broader than before.**
   Fixed-SGQF now matches exact Kalman value-path outputs on tested 1D, 2D, and
   3D affine Gaussian rows, including the repaired 3D level-3 row.
2. **The local dense-reference ladder is stronger than before.**
   On the selected scalar quadratic fixture, fixed-SGQF matches a recursive dense
   numerical reference through three observations, and higher sparse levels no
   longer fail on that tested row after the cloud repair.
3. **The branch/failure contract is broader than before.**
   The lane explicitly covers branch identity, stage labels, carried-covariance
   logic, and same-branch score/value interpretation, while also preserving that
   some later-time failure coverage remains open.
4. **Score evidence is broader than before.**
   The analytic fixed-branch score has a multistep, four-parameter,
   accepted-branch FD parity row in the repaired lane.
5. **A selected-fixture baseline panel exists for the repaired lane.**
   On the scalar quadratic same-target panel, fixed-SGQF is closer to the dense
   reference than UKF or cubature on the tested row.
6. **The higher-level failure story on the tested scalar and affine rows was revised.**
   The previously reported level-3 cloud/value failures on those rows were caused
   by a higher-level merge bug and are superseded by the repaired rerun.

## Unsupported or not-yet-supported claims
- No universal SGQF superiority claim.
- No general sparse-level convergence claim.
- No production-default recommendation.
- No paper-scale high-dimensional readiness claim.
- No stochastic-score correctness claim.
- No HMC readiness claim.
- No claim that all later-time failure modes are now covered.
- No claim that every future higher-level nonlinear row will pass.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| current SGQF pass count | 41 | repaired local test coverage passes |
| fully closed gaps | 6 | G1, G3, G5, G6, G7, G8 |
| partially closed gaps | 2 | G2, G4 |
| hard-blocked gaps | 0 | no phase had to stop the program entirely |
| implementation fixes applied | 2 | rank-safe `_symmetrize(...)` and higher-level cloud merge repair |

## Engineering observations
- The fixed-SGQF lane was mature enough for overnight execution, but the repaired
  post-fix interpretation is more trustworthy than the original pre-fix one.
- The higher-level merge bug was structurally important because it affected the
  cloud itself rather than merely a downstream summary.
- The remaining uncertainties are now mostly about scope expansion, not about the
  correctness of the tested repaired lane.

## Empirical evidence
- The repaired SGQF suite passes locally with `41 passed, 2 warnings`.
- New post-fix evidence closes more of the originally identified gaps than the
  first closeout did.
- The earlier higher-level limitation story for the tested scalar and affine rows
  is superseded by the merge-fix rerun.

## Mathematical claims
- No new general theorem.
- Supported mathematical claims remain local to the tested exact-reference rows,
  named dense-reference rows, and named cloud-construction rows.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| close program as pass with explicit nonclaims and repaired-lane reconciliation | satisfied | no hidden-baseline, hidden-label, or overclaiming veto triggered | partially closed gaps remain local-scope limits | treat the current lane as the repaired fixed-SGQF implementation surface; expand only for specific consumers | no broad scientific or production policy claim |

## Next step
1. **Implementation-hardening**
   - keep both implementation fixes: rank-safe symmetrization and repaired cloud
     merge behavior;
   - if a consumer needs stronger later-time failure coverage, design a broader
     deterministic fixture search rather than forcing a weak row.
2. **Research-comparison**
   - extend the baseline panel to additional same-target rows only if there is a
     real model-selection consumer;
   - treat future higher-level rows as hypotheses to test, not as automatic
     extensions of the repaired evidence.
3. **Documentation/API**
   - summarize the tested scope of the repaired fixed-SGQF lane in a reset memo or
     developer note;
   - note explicitly that the pre-fix higher-level failure story on the tested
     scalar and affine rows has been superseded.
