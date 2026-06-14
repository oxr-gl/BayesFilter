# P48 Result: Zhao--Cui Source-Code Discrepancy Audit And Rewrite Decision

metadata_date: 2026-06-09
program: P48-source-code-discrepancy-and-rewrite
status: EXECUTED_CLAUDE_RESULT_REVIEW_CONVERGED
supervisor: Codex
reviewer: Claude Code read-only

## Decision Table

| Field | Status |
| --- | --- |
| Decision | `REWRITE_REQUIRED_FOR_SOURCE_FAITHFUL_FILTERING_LANE`; `KEEP_FIXED_BRANCH_FOR_DETERMINISTIC_GRADIENT_LANE`; `DO_NOT_PROMOTE_M4B_M5B_FROM_CURRENT_ROUTE`. |
| Primary criterion status | Passed locally: discrepancy ledger, decision matrix, and scientific decision ladder created with source anchors, BayesFilter anchors, decisions, tests, and non-claims. |
| Veto diagnostic status | No claim is made that current BayesFilter reproduces adaptive MATLAB TT/SIRT. No fixed-design retained-grid test is treated as source-route equivalence. No code from LGPL/GPL MATLAB source is copied. No HMC readiness claim is made. The need for analytical gradients is not used to justify calling an ad hoc replacement source-faithful. |
| Main uncertainty | Exact performance of a clean-room source-faithful TF/TFP lane remains untested until P49+. |
| Next justified action | Create P49 to implement the clean-room source-faithful one-step/adaptive route and keep gradient/HMC fixed branch separate. |
| Not concluded | No completed BayesFilter rewrite, no paper-scale SIR or predator-prey production readiness, no S&P 500 reproduction, no adaptive-route differentiability. |

## Main Finding

The earlier P10/P34 audits were correct but narrower than the later execution
program implicitly needed.  They certify source understanding: the authors'
MATLAB repository contains the Zhao--Cui sequential TT/SIRT architecture,
including sample propagation, ESS, recentering, TT/SIRT construction,
normalizer updates, inverse Rosenblatt sampling, proposal correction,
preconditioning, and smoothing.

They do not certify that BayesFilter's current fixed-design route implements
the same adaptive source route.

The current BayesFilter highdim code is best understood as a deterministic
fixed-branch TT/SIRT-inspired lane.  It is valuable for branch replay,
TensorFlow gradients, and HMC-oriented experiments, but it is not the right
architecture for source-faithful high-dimensional filtering claims such as
paper-scale spatial SIR or predator-prey.

## Gradient Requirement Vs Source Fidelity

The need for analytical gradients is real and important.  For HMC and related
gradient-based inference, BayesFilter may need a deterministic, replayable,
differentiable likelihood lane that intentionally differs from the adaptive
source algorithm.

That engineering requirement does not license an unfaithful ad hoc invention.
If BayesFilter changes adaptive source mechanisms to obtain gradients, the new
route must be named as a gradient-bearing approximation or fixed-branch
adaptation, not as a source-faithful Zhao--Cui implementation.  It must carry
its own evidence contract, tests, baselines, and non-claims.

The rule is therefore:

1. Source-faithful filtering claims require source-faithful mechanisms or a
   reviewed derivation proving equivalence.
2. Analytical-gradient claims require differentiability and replay evidence.
3. A route can satisfy one of these without satisfying the other.
4. If a route is changed for gradients, the discrepancy must be documented and
   scientifically tested against the source-faithful lane or an exact
   reference before making accuracy claims.

## Why M4b Looked So Different From The Paper

The source SIR example uses `d=0`, `m=18`, `T=20`, `N=5e3`, random TT cross,
rank caps around 40, and a sample/ESS-driven `full_sol` route.  It does not
retain all state axes as a tensor-product grid and then evaluate all pairwise
transition densities.

The current BayesFilter multistate adapter retains all state axes on a grid.
P47 showed that this produces a route-architecture blocker:

| Candidate | Sites J | State Dim | Order | Grid Points | Pairwise Evaluations |
| --- | ---: | ---: | ---: | ---: | ---: |
| M4b-0 | 3 | 6 | 3 | 729 | 531441 |
| M4b-1 | 5 | 10 | 3 | 59049 | 3486784401 |
| M4b-2 | 9 | 18 | 3 | 387420489 | 150094635296999121 |

That explains the dramatic difference: BayesFilter was not executing the same
source-style route.

## Discrepancy Artifacts

Created:

- Discrepancy ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p48-source-code-discrepancy-ledger-2026-06-09.md`
- Machine-readable decision matrix:
  `docs/plans/bayesfilter-highdim-zhao-cui-p48-implementation-choice-decision-matrix-2026-06-09.json`
- Scientific decision test ladder:
  `docs/plans/bayesfilter-highdim-zhao-cui-p48-scientific-decision-test-ladder-2026-06-09.md`

## Rewrite Decision

### Source-Faithful Filtering Lane

Required before future paper-scale Zhao--Cui filtering claims:

1. Clean-room TensorFlow / TensorFlow Probability implementation.
2. Sample propagation through the model.
3. ESS and enhanced sampling logic.
4. Weighted recentering with affine `mu, L` maps and determinant accounting.
5. Adaptive TT/SIRT or source-faithful equivalent approximation.
6. Retained TT/SIRT transport/density objects rather than all-axes grids.
7. Proposal correction and log normalizer updates.
8. Preconditioned/residual lane for difficult nonlinear models.

### Deterministic Fixed-Branch Gradient Lane

Keep and label explicitly:

1. Fixed design and fixed rank.
2. Replayable branch manifests.
3. TensorFlow autodiff.
4. Scale-aware gradient and likelihood validation.
5. No adaptive/random route equivalence claim.
6. Explicit label as a gradient-bearing approximation when it departs from the
   source route.

## Scientific Tests Required

The P48 test ladder requires:

- analytic density and marginalization tests;
- source-faithful one-step filter tests;
- SV dim 1--3 value/gradient calibration against Kalman/mixture/CUT4 ladders
  where applicable;
- spatial SIR J=1/J=3 reference checks and J=5/J=9 preflight without
  pairwise-grid explosion;
- predator-prey full/preconditioned route ablation;
- fixed-branch gradient boundary tests.

## Local Validation

Planned commands:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p48-implementation-choice-decision-matrix-2026-06-09.json
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p48-*
```

Results:

```text
json.tool: passed
git diff --check: passed
```

## Claude Result Review

Iteration 1 returned the pass token
`PASS_P48_SOURCE_CODE_DISCREPANCY_REWRITE_RESULT` and one minor governance
note: normalize decision labels to the canonical master-plan vocabulary.  Codex
patched the ledger and JSON accordingly and requested a convergence review.

Iteration 2 returned:

```text
PASS_P48_RESULT_REVIEW_CONVERGED
```

Final review status: converged.
