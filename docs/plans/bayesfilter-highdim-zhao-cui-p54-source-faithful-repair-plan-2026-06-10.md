# P54 Plan: Source-Faithful Redrift Repair

metadata_date: 2026-06-10
program: P54-source-faithful-redrift-recovery
status: REVIEWED_AFTER_CLAUDE_LOOP
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Repair the source-route drift found after P53 while preserving the legitimate
deterministic fixed-gradient branch as a separate route.  The repair must move
BayesFilter back toward the Zhao--Cui paper/source operation order and prevent
local-neighborhood or all-grid routes from being treated as source-faithful
progress.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we patch the current implementation so future source-faithful Zhao--Cui work is guarded against P53-style drift and covers the first missing executable source-route operations? |
| Baseline/comparator | P54 redrift audit; P49 source-route contract; source files `ssmodel.m`, `full_sol.m`, `pre_sol.m`, `computeL.m`, `ESS.m`. |
| Primary criterion | Tests pass for source push/augmentation, drift audit coverage, recentering with `computeL` quantile scaling, existing P49 route guards, and public exports. |
| Veto diagnostics | Any patch copies MATLAB code; any patch relabels fixed-gradient or P53 local-neighborhood route as source-faithful; any patch claims adaptive TT/SIRT or paper-scale SIR completion. |
| Explanatory diagnostics | Focused pytest and compile checks; Claude read-only audit and execution review. |
| Not concluded | No full source sequential filter, no adaptive TT/SIRT fit, no SIR d=18 readiness, no predator-prey production readiness, no HMC readiness. |
| Artifact | This plan, audit artifact, implementation diff, result artifact, Claude review notes. |

## Skeptical Plan Audit

Status: PASS_FOR_EXECUTION_AFTER_CLAUDE_REVIEW.

- Wrong baseline risk: plan is anchored to source route and P49, not P53 local
  neighborhood route.
- Proxy metric risk: helper tests only certify helper behavior; result artifact
  must say full source filter remains incomplete.
- Hidden assumption risk: quantile scaling is included as source-style
  behavior, but exact numerical equality with MATLAB is not claimed.
- Environment mismatch risk: no MATLAB execution or code copying is required.
- Stop condition risk: if tests fail due to implementation mistakes, repair
  locally; if adaptive TT/SIRT is required for pass, block and plan next phase.

## Phase Plan

| Phase | Scope | Files | Pass criterion | Non-claims |
| --- | --- | --- | --- | --- |
| P54-M0 | Discrepancy audit and drift classification | P54 audit doc | Claude agrees or only minor revisions remain | No implementation completion |
| P54-M1 | Source-route operation drift guards | `source_route.py`, new tests | Audit object blocks missing/partial/drift markers, keeps previous retained object / marginalization explicit, and passes complete source coverage only when every required operation is present | No source filter |
| P54-M2 | Author-style push and augmentation helper | `source_route.py`, sample/proposal tests | Helper updates log weights by likelihood and emits `[theta,x_t,x_{t-1}]` augmented batch | No model-suite integration |
| P54-M3 | `computeL` recentering correction | `source_route.py`, recenter tests | Weighted Cholesky and high-ESS quantile stretch are both tested | No exact MATLAB bitwise equality |
| P54-M4 | Validation and result review | result artifact, focused tests | Focused pytest/compile pass and Claude execution review agrees no drift | No adaptive TT/SIRT fit |

## Implementation Details

### P54-M1 Drift Guards

Add:

- `SOURCE_ROUTE_REQUIRED_OPERATION_IDS`;
- `SOURCE_ROUTE_FORBIDDEN_DRIFT_MARKERS`;
- `SourceRouteOperationRecord`;
- `SourceRouteImplementationAudit`.

The audit must emit `BLOCK_SOURCE_ROUTE_DRIFT` when markers such as
`pairwise_grid_transition`, `all_grid_pairwise_transition`,
`multistate_grid_pairwise_transition`, `local_neighborhood_rank_multiplier`,
`q_power_dependency_width`, `all_grid_retained_storage`, or
`retained_grid_only_route` appear.

The required operation list must include
`previous_retained_object_marginalization` as a separate operation between
`weighted_recenter_computeL` and `shifted_target_construction`.  Folding this
operation into shifted-target construction is a source-route drift because the
source code uses the model prior at `t=1` and the previous retained TT/SIRT
object plus marginalization at later time steps.

### P54-M2 Push/Augment Helper

Add a clean-room helper:

```text
source_route_push_and_augment_samples(
    previous_batch=[theta,x_{t-1}],
    transition_fn,
    log_likelihood_fn,
    parameter_dim=d,
    state_dim=m,
    time_index=t,
)
```

It must return:

- propagated `[theta,x_t]` samples;
- augmented `[theta,x_t,x_{t-1}]` samples;
- normalized log weights proportional to previous weight times likelihood;
- ESS diagnostics.

### P54-M3 Recenter Correction

Extend `source_route_recenter` so it keeps the existing covariance path but also
supports source-style high-ESS quantile scaling:

```text
L = chol(weighted_covariance + jitter I)
standardized = L^{-1}(samples - mu)
scale_jj = -(q99_j - q01_j) / (2 norminv(q))
L <- L diag(scale)
L <- epd L
```

The quantile branch is optional and tested separately.

## Claude Review Loop

Use Claude Opus read-only review up to five iterations.

Accept early only on:

```text
VERDICT: AGREE
```

If Claude returns `VERDICT: REVISE`, patch audit/plan/code/tests unless the
finding requires human approval or a new phase.  At iteration 5, accept only if
there is no major source-drift blocker.

P54 may not close if Claude or Codex finds either of these blockers still
present:

- previous retained object / marginalization is absent from required operation
  coverage;
- pairwise-grid, all-grid, or retained-grid-only routes can still satisfy the
  source-faithful audit vocabulary.

## Execution Commands

CPU-only focused validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p54_source_route_drift_audit.py \
  tests/highdim/test_p49_source_route_sample_proposal.py \
  tests/highdim/test_p49_source_route_recenter_normalizer.py \
  tests/highdim/test_p49_source_route_retained_object.py \
  tests/highdim/test_p49_source_route_preconditioned_predator_prey.py \
  tests/highdim/test_p49_source_route_smoothing_boundary.py \
  tests/highdim/test_p49_gradient_lane_boundary.py \
  tests/highdim/test_public_api_highdim.py
```

Compile check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p54_source_route_drift_audit.py \
  tests/highdim/test_p49_source_route_sample_proposal.py \
  tests/highdim/test_p49_source_route_recenter_normalizer.py
```

Static check:

```bash
git diff --check -- \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p54_source_route_drift_audit.py \
  tests/highdim/test_p49_source_route_sample_proposal.py \
  tests/highdim/test_p49_source_route_recenter_normalizer.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p54-source-faithful-redrift-audit-2026-06-10.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p54-source-faithful-repair-plan-2026-06-10.md
```

## Next Phase If P54 Passes

Start P55 for clean-room source transport fitting and one-step source
reapproximation:

1. define transport-fit interface;
2. add analytic/dense one-step target references;
3. fit minimal deterministic clean-room transport object;
4. integrate retained sample generation and proposal correction;
5. only then retry spatial SIR source filtering ladders.
