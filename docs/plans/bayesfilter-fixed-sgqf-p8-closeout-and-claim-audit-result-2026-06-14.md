# Phase Result: Fixed-SGQF Closeout and Claim Audit

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p8-closeout-and-claim-audit-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`

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
| final SGQF suite status | `38 passed, 2 warnings` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p8-closeout-and-claim-audit-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p8-closeout-and-claim-audit-result-2026-06-14.md` |

## Result summary
The overnight fixed-SGQF program completed all planned phases P0-P8 without a
hard stop.  Several gaps were fully closed at local tested scope, and several
higher-level or broader-scope questions were converted into explicit limits
rather than hidden assumptions.

One implementation fix was required during execution:
- `bayesfilter/nonlinear/fixed_sgqf_tf.py` now uses
  `tf.linalg.matrix_transpose(...)` inside `_symmetrize(...)` so derivative-path
  batched covariance tensors are symmetrized rank-safely.

The fixed-SGQF suite now passes locally with expanded coverage:
- `38 passed, 2 warnings`.

## Required closure matrix
| Gap | Status | Supporting phase(s) | Evidence class | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|---|
| G1 multistep nonlinear dense-reference | `closed` | P1 | `dense_numerical_reference` | only one selected 1D nonlinear fixture | add harder nonlinear fixtures if needed | no general nonlinear exactness claim |
| G2 higher-dimensional accepted-path validation | `partially_closed` | P2, P4 | `exact_reference`, `contract_failure` | nonlinear higher-dimensional accepted paths remain thinner than affine ones | add additional nonlinear accepted-path fixtures if needed | no blanket higher-dimensional pass claim |
| G3 cloud exactness beyond current small cases | `partially_closed` | P3 | `contract_failure` / tested-moment evidence | higher-level behavior is not uniformly stronger | extend tested-moment ladder cautiously | no all-moment or all-level exactness claim |
| G4 later-time and later-stage failure coverage | `partially_closed` | P2, P5 | `contract_failure` | deterministic `time_index > 0` failure row still missing | keep explicit blocker; search broader fixtures only if needed | no claim that all stage/time combinations are covered |
| G5 broader score/FD coverage | `closed` | P5 | `dense_numerical_reference` + same-branch score evidence | broader higher-dimensional and stochastic-score rows remain open | add more fixtures only if a consumer needs them | no stochastic-score or HMC readiness claim |
| G6 multidimensional affine exact-vs-Kalman parity | `closed` | P4 | `exact_reference` | higher sparse levels can still block | use level-2 affine rows as exact anchors | no claim that all higher levels inherit parity |
| G7 same-target baseline comparison ladder | `closed` | P7 | `baseline_only` | only one selected fixture panel was run; CUT4 not eligible there | add broader same-target panels if needed | no universal ranking claim |
| G8 sparse-level ladder vs dense | `closed` | P6 | `dense_numerical_reference` | ladder is local and non-monotone beyond level 2 | keep level-2 as stable anchor and record higher-level limits | no general convergence or monotonic-improvement claim |

## Supported claims
1. **Exact-reference affine support is broader than before.**
   Fixed-SGQF level 2 now matches exact Kalman value-path outputs on tested 1D,
   2D, and 3D affine Gaussian rows.
2. **The local dense-reference ladder is stronger than before.**
   On the selected scalar quadratic fixture, fixed-SGQF level 2 matches a
   recursive dense numerical reference through three observations.
3. **The branch/failure contract is broader than before.**
   The lane now explicitly covers `carried_covariance` failures on both value and
   score paths, with preserved stage labels and branch signatures.
4. **Score evidence is broader than before.**
   The analytic fixed-branch score now has one multistep, four-parameter,
   accepted-branch FD parity row.
5. **A selected-fixture baseline panel now exists.**
   On the scalar quadratic same-target panel, SGQF level 2 is closer to the
   dense reference than UKF or cubature.

## Unsupported or not-yet-supported claims
- No universal SGQF superiority claim.
- No general sparse-level convergence claim.
- No production-default recommendation.
- No paper-scale high-dimensional readiness claim.
- No stochastic-score correctness claim.
- No HMC readiness claim.
- No claim that all later-time failure modes are now covered.
- No claim that higher sparse levels are always safe or always better.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| final SGQF pass count | 38 | expanded local test coverage passes |
| fully closed gaps | 5 | G1, G5, G6, G7, G8 |
| partially closed gaps | 3 | G2, G3, G4 |
| hard-blocked gaps | 0 | no phase had to stop the program entirely |
| implementation fixes applied | 1 | rank-safe `_symmetrize(...)` repair |

## Engineering observations
- The fixed-SGQF lane was mature enough for overnight execution, but only after
  preserving strict label discipline.
- The only production-surface change was small but important: rank-safe
  symmetrization for derivative-path tensors.
- The remaining uncertainties are mostly about scope expansion, not basic lane
  viability.

## Empirical evidence
- The expanded SGQF suite passes locally.
- New evidence rows close most of the originally identified gaps at local tested
  scope.
- Several limits were informative rather than merely negative:
  - affine level-3 blocking,
  - sparse-level blocking beyond level 2,
  - 2D level-3 cloud covariance mismatch,
  - missing deterministic later-time failure row.

## Mathematical claims
- No new general theorem.
- Supported mathematical claims remain local to the tested exact-reference rows
  and named dense-reference/moment rows.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| close program as pass with explicit nonclaims | satisfied | no hidden-baseline, hidden-label, or overclaiming veto triggered | partially closed gaps remain local-scope limits | keep current lane as a well-tested local implementation surface; expand only for specific consumers | no broad scientific or production policy claim |

## Next step
1. **Implementation-hardening**
   - keep the `_symmetrize(...)` rank-safe fix;
   - if a consumer needs stronger later-time failure coverage, design a broader
     deterministic fixture search rather than forcing a weak row.
2. **Research-comparison**
   - extend the baseline panel to additional same-target rows only if there is a
     real model-selection consumer;
   - treat higher sparse levels as a hypothesis to test, not a default upgrade.
3. **Documentation/API**
   - summarize the tested scope of fixed-SGQF in a reset memo or developer note;
   - document that current strong support is level-2 affine and selected 1D
     nonlinear ladders, not a general SGQF certification.
