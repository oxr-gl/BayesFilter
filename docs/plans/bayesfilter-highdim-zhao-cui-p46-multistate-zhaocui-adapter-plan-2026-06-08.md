# P46 Plan: Multistate Zhao-Cui Fixed-Design TT Adapter

metadata_date: 2026-06-08
phase: P46
status: `DRAFT_FOR_CLAUDE_REVIEW`

## Purpose

Implement a bounded multistate extension of the current nonlinear
Zhao--Cui/fixed-design TT value path so tiny reviewed state-space targets with
`state_dim > 1` can be evaluated without routing through the scalar-only
adapter.  This is a repair follow-up to P45-M1, where generalized SV, spatial
SIR, and predator-prey comparison phases closed as blocker/nonclaim phases
because the nonlinear fixed-design TT route rejected multistate targets.

## Governing Sources

- P45 master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-generalized-sv-sir-predator-prey-comparison-master-program-2026-06-08.md`
- P45 overnight result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-overnight-gated-self-recovery-execution-result-2026-06-08.md`
- P45 target registry:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json`
- P42 validation rules:
  `docs/plans/bayesfilter-highdim-zhao-cui-p42-gradient-likelihood-validation-rules-2026-06-07.md`
- Current implementation anchors:
  `bayesfilter/highdim/filtering.py`,
  `bayesfilter/highdim/fitting.py`,
  `bayesfilter/highdim/squared_tt.py`,
  and `tests/highdim/test_p45_multistate_zhaocui_route.py`.

## Evidence Contract

Question:

- Can the scalar nonlinear fixed-design TT adapter be extended to a tiny
  multistate nonlinear filtering value path while preserving fixed branch
  replay, TensorFlow-only algorithmic implementation, target identity, and
  explicit nonclaims?
- After that repair, can the P45 overnight execution resume under Codex
  supervision without overstating generalized SV/SIR/predator-prey equality?

Baseline or comparator:

- Existing scalar path:
  `scalar_nonlinear_fixed_design_tt_value_path`.
- Independent dense tensor-product quadrature fixture in tests for small
  dimensions and short horizons.
- Existing P45 blocker tests, which must either remain historically valid for
  the scalar-only route or be supplemented by positive P46 adapter tests.

Primary promotion criteria:

- Add a clearly named multistate adapter that accepts `state_dim` equal to the
  configured product-basis dimension and evaluates at least two observations
  for tiny deterministic fixtures.
- The adapter must build initial and transition adjacent targets in
  reference-measure coordinates, fit fixed-design TT square-root targets, retain
  all state axes on a deterministic tensor-product grid, and propagate the
  retained filtering density through the model transition.
- Positive tests must show finite values, deterministic branch replay, retained
  mean/covariance shape correctness, and value agreement against an independent
  dense tensor-product quadrature reference on small dimensions.
- Gradient-bearing smoke tests may be added only as diagnostic P42-style
  evidence; they are not enough to claim HMC readiness or production analytic
  score correctness.
- The resumed overnight execution may promote only the adapter repair.  P45-M2
  through P45-M4 remain blocked unless they also get a reviewed dense/refined
  same-target reference and matched CUT4 target.

Veto diagnostics:

- The adapter silently falls back to a scalar route for `state_dim > 1`.
- Product-basis dimension, coordinate-map dimension, or retained axes do not
  match `model.state_dim()`.
- Reference-measure and physical-measure terms are mixed without the declared
  uniform reference density and coordinate Jacobian factors.
- Fit residual, finite value, or finite gradient is treated as correctness
  without a dense/reference comparator.
- Any artifact claims adaptive TT-cross/SIRT reproduction, paper-scale
  Zhao--Cui reproduction, stable public API, production score API, or HMC
  readiness.
- P45 historical results are overwritten instead of amended by a P46 follow-up.

Explanatory-only diagnostics:

- TT ranks, fit residuals, condition numbers, point counts, retained grid size,
  wall time, branch hashes, and finite value/gradient status.

What will not be concluded:

- no adaptive MATLAB TT-cross or SIRT reproduction;
- no paper-scale Zhao--Cui reproduction;
- no stable public API;
- no production analytic score API;
- no HMC readiness;
- no CUT4--Zhao--Cui equality for generalized SV, spatial SIR, or predator-prey
  unless their separate same-target reference gates pass.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_REVIEW_WITH_BOUND_SCOPE`.

- Wrong-baseline risk: CUT4 is not ground truth for nonlinear multistate
  targets.  P46 uses dense tensor-product quadrature as the adapter comparator.
- Proxy-metric risk: finite values, branch hashes, and TT fit residuals are
  necessary but not sufficient; dense value agreement is the promotion
  criterion for the tiny adapter fixture.
- Hidden-assumption risk: the adapter keeps all state axes retained.  It does
  not implement marginalization over integrated axes or a compressed retained
  posterior for large dimensions.
- Environment risk: local checks are CPU-only with `CUDA_VISIBLE_DEVICES=-1`;
  no GPU evidence is claimed.
- Resource risk: tensor-product quadrature scales exponentially.  P46 caps
  tests at state dimensions 2 and 3 with low quadrature orders and short
  horizons.
- Stale-context risk: P45 artifacts remain valid as historical blocker
  results.  P46 records a repair result instead of editing P45 closeout into a
  comparison result.

## Phase Plan

| Phase | Purpose | Gate |
| --- | --- | --- |
| P46-M0 | Plan and Claude read-only review loop. | `PASS_P46_PLAN_GOVERNANCE` |
| P46-M1 | Implement multistate adjacent target builders, retained-grid helpers, and fixed-design TT value path. | local tests pass |
| P46-M2 | Add positive adapter tests for two-state and three-state tiny nonlinear fixtures against dense tensor-product quadrature. | value/replay/shape tests pass |
| P46-M3 | Claude read-only code/governance review loop and repair until convergence or max 5. | `PASS_P46_CODE_GOVERNANCE` |
| P46-M4 | Record P46 result and resume P45 overnight execution as an amended follow-up: rerun focused P45/P46 gates, then classify remaining P45 blockers. | `PASS_P46_RESUME_GOVERNANCE` |

## Planned Implementation

- Add a new public highdim subpackage function:
  `multistate_nonlinear_fixed_design_tt_value_path`.
- Keep `scalar_nonlinear_fixed_design_tt_value_path` unchanged for scalar
  compatibility and historical P45 tests.
- Add multistate helper functions with explicit names rather than weakening
  scalar validations.
- Use TensorFlow/TensorFlow Probability only in BayesFilter-owned
  implementation code.
- Use NumPy nowhere in the implementation path.
- Keep dense tensor-product reference code inside tests as an independent
  comparator.

## Planned Local Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p46_multistate_zhaocui_adapter.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_multistate_zhaocui_route.py tests/highdim/test_p46_multistate_zhaocui_adapter.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p46_multistate_zhaocui_adapter.py
git diff --check -- bayesfilter/highdim/filtering.py bayesfilter/highdim/__init__.py tests/highdim/test_p46_multistate_zhaocui_adapter.py docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-plan-2026-06-08.md
```

## Claude Review Protocol

- Codex remains supervisor/executor.
- Claude is read-only reviewer only.
- Review loops until `PASS_P46_PLAN_GOVERNANCE` / `PASS_P46_CODE_GOVERNANCE`
  / `PASS_P46_RESUME_GOVERNANCE` or max 5 iterations.
- Claude commands must use non-interactive read-only mode and may not edit
  files or launch implementation commands.

## Result Artifact

P46 will record its result in:

`docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-result-2026-06-08.md`

