# P37-M2.6c Claude Review Ledger

metadata_date: 2026-06-06
phase: P37-M2.6c short sequential SV TT value path

review_scope:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-subplan-2026-06-05.md`

governing_sources:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-overnight-gated-self-recovery-runbook-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-source-governance-charter-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-result-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-paper-code-crosswalk-ledger-2026-05-30.md`

## Iterations

### Plan Gate Iteration 1

worker: `highdim-p37-m2p6c-plan-review-iter1`

status: `BLOCKED_M2P6C_PLAN`

raw_response:

```text
BLOCKED_M2P6C_PLAN

1. The plan does not pin the exact M2.6c fixtures needed to rule out
   comparator drift.
2. The tolerance contract is explicitly placeholder text.
3. The plan does not sufficiently block promotion of the existing dense M2.5
   path as the TT path.
4. The comparator set is underspecified for retained statistics.
5. The plan does not pin per-step normalizer comparators concretely enough.
6. The implementation task list is too thin to be implementation-ready.
7. The plan does not pin the fitting fixture lineage strongly enough for
   sequential use.
8. The plan lacks an executable stop condition around horizon scope and
   non-claims.

Governance passes on anchors and clean-room boundary, but implementation
readiness and evidence-contract readiness do not pass.
```

accepted_fixes:

- Added an exact fixed-fixture section with M2.6a/M2.6b source fixture IDs,
  M2.6c fixture IDs, theta, observations, promoted horizon, coordinate map,
  basis, rank, fit config, quadrature orders, tau/floor contract, branch-seed
  policy, and dense comparator fixture.
- Replaced placeholder tolerances with executable tolerances and stated that
  failure does not authorize tolerance relaxation without reviewed amendment.
- Added hard vetoes against routing the promoted path through the current
  scalar dense value path, accepting `fit_config is None` and
  `product_basis is None`, missing TT artifacts, or using dense retained
  filters as promoted transition inputs.
- Defined the promoted TT normalizer route as
  `log(density.normalizer()) + target.log_scale_shift`.
- Defined the promoted retained-moment route as GL257 integration of
  `normalized_retained_density_values((0,), z)` mapped through the affine
  coordinate map.
- Defined the TT retained propagation route as a GL321 TT-generated retained
  grid with `storage_kind = scalar_tt_grid` and a required density hash.
- Added step-by-step implementation tasks for a new TT-only scalar sequential
  entry point, retained grid constructor, transition target support, branch
  manifests, focused tests, guardrails, result ledger, and traceability update.
- Pinned the promoted horizon to observations `(0.12, -0.08)` only.

### Plan Gate Iteration 2

worker: `highdim-p37-m2p6c-plan-review-iter2`

status: `PASS_M2P6C_PLAN`

raw_response:

```text
PASS_M2P6C_PLAN

Governance passes.  The subplan carries explicit P30 anchors, Zhao--Cui
anchors, MATLAB behavioral anchors, BayesFilter code/test anchors, an
explicit BayesFilter-extension deviation, and a clean-room statement.

The eight iteration-1 blockers are fixed:

1. Exact fixtures and values are pinned.
2. Tolerances are non-placeholder and executable.
3. TT-vs-dense hard vetoes are explicit, including blocking the current dense
   path.
4. The retained-statistic promotion route is concrete.
5. The per-step normalizer comparator route is concrete.
6. The implementation task list is implementation-ready.
7. Fitting lineage is pinned through M2.6a/M2.6b fixture IDs and fit config.
8. Exact horizon scope and non-claims are executable.

Implementation readiness also passes.  The plan correctly recognizes that the
current code has only the dense scalar nonlinear route and must add a TT-only
path.  Negative tests explicitly guard against silent fallback to the dense
path, and the dense comparator anchor is pinned.
```

### Local Implementation And Evidence

status: `LOCAL_EVIDENCE_PASS_PENDING_CLAUDE_CODE_GOVERNANCE_REVIEW`

implemented_files:

```text
bayesfilter/highdim/filtering.py
bayesfilter/highdim/__init__.py
tests/highdim/test_p30_sv_short_sequential_tt_value_path.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

local_repairs:

```text
1. Added missing _coordinate_map_for_config helper after first focused run
   exposed a NameError.
2. Added chunked retained-density evaluation after the reviewed GL257/GL321
   retained grids exceeded the existing fitted-TT per-call complexity budget.
   The reviewed grids, tolerances, fixtures, baselines, and promoted objects
   were unchanged.
```

focused_evidence:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_stochastic_volatility.py

17 passed, 2 warnings in 10.39s
```

broad_guardrail:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_bases.py \
  tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py \
  tests/highdim/test_transport.py \
  tests/highdim/test_fixed_branch_fit.py \
  tests/highdim/test_failure_exits.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_public_api_highdim.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_lgssm_exact_reference.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py

143 passed, 2 warnings in 12.61s
```

### Code/Governance Review Iteration 1

worker: `highdim-p37-m2p6c-code-governance-review-iter1`

status: `BLOCKED_M2P6C_CODE_GOVERNANCE`

raw_response:

```text
BLOCKED_M2P6C_CODE_GOVERNANCE

1. The promoted t=1 transition path still reuses the dense retained-grid
   propagation routine instead of a distinct TT-retained propagation path.

The TT entry point requires scalar_tt_grid, but the transition builder accepts
either scalar_dense_grid or scalar_tt_grid and computes predictive density
through _scalar_dense_predictive_log_density_from_retained(...).  That helper
consumes generic dense-grid fields.  For scalar_tt_grid the code only checks
that a density_hash exists, but it does not use the hash to enforce a
TT-specific propagation contract.

Required fix:

1. Split the transition propagation contract so the promoted M2.6c path uses a
   TT-specific propagation routine for scalar_tt_grid, with explicit
   validation that the retained input is the TT-generated object and that the
   density hash is part of the enforced replay contract rather than
   metadata-only.
2. Add a focused negative test that would fail if scalar_tt_grid transition
   propagation silently routes through the dense retained helper.
3. Update result ledger wording if the implementation remains
   grid-replay-equivalent by design.

Governance anchors, clean-room boundary, per-step normalizer formula,
retained-moment reference-measure route, chunking, top-level API non-leak, and
non-claims otherwise pass.
```

accepted_fix_plan:

```text
Blocker classification: fixable implementation/governance issue with
unchanged scientific contract.  Repair will split scalar_tt_grid propagation
from scalar_dense_grid propagation, require density object/hash replay, and
add a negative test that monkeypatches the dense helper to fail if TT
propagation uses it.
```

accepted_fix_implementation:

```text
Implemented _scalar_tt_predictive_log_density_from_retained for scalar_tt_grid
propagation.  The helper validates storage_kind, retained SquaredTTDensity
object, and density_hash replay before using the retained grid fields.  The
dense helper remains separate.  Added a monkeypatch negative test that raises
from the dense helper and verifies the promoted TT path still runs.
```

repair_evidence:

```text
Focused M2.6c repair evidence:
18 passed, 2 warnings in 10.73s.

Broad highdim guardrail:
144 passed, 2 warnings in 12.87s.
```

### Code/Governance Review Iteration 2

worker: `highdim-p37-m2p6c-code-governance-review-iter2`

status: `PASS_M2P6C_CODE_GOVERNANCE`

raw_response:

```text
PASS_M2P6C_CODE_GOVERNANCE

Governance passes first, then implementation/evidence.

Source-governance and clean-room pass.  The M2.6c subplan carries explicit
P30, Zhao--Cui, MATLAB-audit, and BayesFilter code/test anchors plus an
explicit BayesFilter-extension deviation and clean-room boundary.  The result
ledger and traceability row keep the same non-claims and extension status.

The prior blocker is fixed.  scalar_tt_grid transition propagation now goes
through the TT-specific helper, not the dense helper.  That helper enforces
storage_kind == scalar_tt_grid, requires a SquaredTTDensity object, and checks
density_hash replay before using retained-grid fields.  The focused
monkeypatch test would fail if dense fallback were used.

The promoted path stays TT-only.  The promoted entry point requires fit_config
and product_basis and is pinned to exactly two observations.  The old nonlinear
FixedBranchSquaredTTFilter.log_likelihood still routes to the dense path and
rejects TT-artifact requests.

The per-step normalizer, retained-moment route, chunking, top-level API
non-leak, and evidence contract pass for the scoped M2.6c claim.

No remaining governance, math, implementation, or evidence-contract blocker
was found in the reviewed M2.6c scope.
```

## Current Status

`PASS_M2P6C_CODE_GOVERNANCE`.
