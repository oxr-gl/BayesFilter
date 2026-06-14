# P54 Source-Faithful Redrift Audit: Zhao--Cui Source Vs Current BayesFilter

metadata_date: 2026-06-10
program: P54-source-faithful-redrift-recovery
status: REVIEWED_AFTER_CLAUDE_LOOP
supervisor: Codex
reviewer: Claude Code read-only

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Excluding the legitimate need for a deterministic fixed-gradient variant, where does current BayesFilter still differ from the Zhao--Cui paper/source route? |
| Baseline/comparator | Zhao--Cui paper as captured in P30; author code under `third_party/audit/zhao_cui_tensor_ssm_p10/source`; P34 reference audit; P48 discrepancy ledger; P49 source-route contract and implementation. |
| Primary criterion | Every material source-route operation is classified as implemented, partial, blocked, or intentionally fixed-gradient-only, with source anchors and BayesFilter anchors. |
| Veto diagnostics | Any local-neighborhood, all-grid, or fixed-rank gradient adaptation is relabeled as source-faithful; any discrepancy omits a source anchor; any implementation fix copies MATLAB source instead of clean-room TF/TFP. |
| Explanatory diagnostics | Existing P49 tests, P53 blocker artifacts, code anchors in `source_route.py`, `transition_route.py`, `filtering.py`, and source files `full_sol.m`, `pre_sol.m`, `ssmodel.m`, `computeL.m`, `ESS.m`. |
| Not concluded | No paper-scale SIR reproduction, no adaptive TT/SIRT fit completion, no HMC readiness, no smoothing support, no claim that the fixed-gradient branch is source-faithful. |

## Skeptical Plan Audit

Status: PASS_FOR_AUDIT.

- Wrong baseline risk: use `full_sol.m` / `pre_sol.m` and P30/P48/P49, not P53
  local-neighborhood artifacts, as source-route baseline.
- Proxy metric risk: route labels, smoke tests, and lower-rung dense tie-outs
  are not source-faithfulness unless they exercise the source operation order.
- Hidden assumption risk: fixed branch necessity is real for HMC, but this audit
  intentionally excludes it from source-faithful promotion.
- Stale context risk: P49 already found and partially repaired the mismatch;
  P54 must not rediscover P49 and stop.
- Artifact adequacy risk: the audit must feed a repair plan and executable
  drift guards.

## Source Operation Coverage

| Operation | Source anchor | Current BayesFilter anchor | Status | Discrepancy |
| --- | --- | --- | --- | --- |
| Initialize samples | `full_sol.solve` lines 20--22; `pre_sol.solve` lines 14--15 | `SourceRouteSampleBatch` in `source_route.py`; P49 tests | partial | Batch object exists, but no full model-specific prior sampler integration. |
| Push samples | `ssmodel.push_samples` lines 35--47; `full_sol.solve` lines 22--25 | P54 adds `source_route_push_and_augment_samples` | partial after P54 patch | Clean-room helper now matches shape and log-weight update, but not wired into full sequential filter. |
| Augment current/previous state | `full_sol.solve` lines 23--25 | P54 helper and test | partial after P54 patch | Helper forms `[theta, x_t, x_{t-1}]`; model-suite integration remains pending. |
| ESS enhancement gate | `full_sol.reapprox` lines 48--63; `pre_sol.reapprox` lines 33--103; `ESS.m` | `source_route_needs_enhancement`, diagnostics | partial | ESS calculation and gate exist; doubling/enhanced resampling loop is not integrated into sequential filtering. |
| Weighted recentering / `computeL` | `computeL.m`; `full_sol.reapprox` lines 65--71 | P54 extends `source_route_recenter` | partial after P54 patch | Weighted covariance and high-ESS quantile scaling are now represented; sample pruning of NaN/Inf and model integration remain pending. |
| Prior or previous retained object / marginalization | `full_sol.reapprox` lines 73--83; `pre_sol.reapprox` lines 117--134; `TTSIRT.marginalise` | `SourceRouteRetainedObject` skeleton and P54 operation audit | blocked | This is a distinct source operation from shifted-target construction.  At `t=1` it uses the model prior; at `t>1` it uses the previous retained transport object and marginalization.  The operation is now explicit in audit coverage, but the executable marginalization route is still absent. |
| Shifted target construction | `full_sol.reapprox` lines 86--96; `pre_sol.reapprox` lines 218--227 | `source_route_shifted_negative_log_target` | partial | Shift identity exists; no full local-coordinate target object/function boundary yet. |
| TT/SIRT transport fit | `full_sol.reapprox` lines 102--121; `pre_sol.reapprox` lines 231--270; `TTFun.cross` | retained-object skeleton only | blocked | No clean-room adaptive TT/SIRT fit implementation. This is the largest remaining source-faithful gap. |
| Normalizer update | `full_sol.reapprox` line 124; `TTSIRT.marginalise` | `SourceRouteNormalizerContribution`, `source_route_log_normalizer_update` | partial | `log(z)-const` identity exists; not integrated with transport fit. |
| Retained sample generation | `full_sol.solve` lines 31--38; `pre_sol.reapprox` lines 272--286 | retained-object skeleton | blocked | No inverse-transport retained sample generation from fitted object. |
| Proposal correction | `full_sol.solve` lines 35--38; `pre_sol.reapprox` lines 288--294 | proposal log-weight helpers | partial | Correction math exists; not integrated into sequential source filter. |
| Preconditioned route | `pre_sol.reapprox` lines 136--294 | target identity and manifest scaffold | partial | Variant identity guard exists; no full preconditioned source route. |
| Smoothing | `full_sol.smooth`; `pre_sol.smooth` | explicit deferred boundary | intentionally blocked | Correctly not claimed for filtering likelihood completion. |

## Drift Findings

| ID | Finding | Severity | Why it matters | Required correction |
| --- | --- | --- | --- | --- |
| P54-D01 | P53 local-neighborhood route drifted from P48/P49 source-route baseline. | critical | It made a source-feasible SIR example fail through `R_eff=q^w`, which is not the paper/source compression route. | Add source-route drift guard and forbid local-neighborhood rank multiplier from source-faithful progress tokens. |
| P54-D02 | Current source route is still mostly helper/skeleton code, not an executable source filter. | critical | Passing helper tests can be misread as implementation completion. | Repair plan must target one-step source reapproximation before any SIR production retry. |
| P54-D03 | Author `push_samples` and augmentation shape were not encoded as a first-class source-route helper. | high | Shape `[d+2m,N]` and log-likelihood weight update are core route mechanics. | Add clean-room push-and-augment helper and tests. |
| P54-D04 | `computeL` quantile scaling was simplified to Cholesky recentering. | medium-high | For high ESS, author code stretches coordinates by weighted quantiles after whitening. | Add optional source-style quantile scale branch and tests. |
| P54-D05 | Adaptive TT/SIRT fit remains absent. | critical | Without this, spatial SIR/predator-prey source-faithful filtering cannot be claimed. | Create next-phase implementation plan for clean-room transport fit boundary and one-step reapproximation. |
| P54-D06 | Proposal correction exists only as a standalone identity. | high | The paper/source route relies on correction after retained sample generation. | Integrate correction into a source-route one-step result object. |
| P54-D07 | Preconditioned route is only a target identity, not source behavior. | high | Predator-prey source performance depends on preconditioned/residual maps. | Defer production predator-prey claims until preconditioned route is executable. |
| P54-D08 | P54 initially omitted the previous-retained-object/marginalization operation from required coverage. | critical | This would let an implementation skip the `t>1` retained-object density carried by the source route while still passing the coverage audit. | Add `previous_retained_object_marginalization` to required operation IDs and keep it blocked until executable marginalization exists. |
| P54-D09 | P54 drift markers were too narrow for pairwise-grid, all-grid, or retained-grid-only route drift. | critical | P48-D02/D10 show that all-grid retained payloads and pairwise grid propagation are a separate non-source route, not a source-faithful high-dimensional solution. | Add explicit pairwise-grid propagation, all-grid storage, retained-grid-only, and multistate-grid storage drift markers to the P54 guard vocabulary and tests. |

## Fixed Variant Boundary

The deterministic fixed-gradient branch remains legitimate and necessary for
HMC-style work, but it is a separate route.  P54 does not require removing that
branch.  It requires that fixed/local/grid routes cannot satisfy
`source_faithful_filtering` operation coverage unless a reviewed derivation
proves equivalence to the source route.

## Immediate Patch Scope

P54 patches only safe, source-contract-level discrepancies:

1. add a clean-room `push_samples` / augmentation helper;
2. add source-operation drift audit objects;
3. add `computeL` quantile scaling to recentering;
4. add tests that fail on local-neighborhood, pairwise-grid, all-grid, or
   retained-grid-only source-route drift;
5. make previous retained object / marginalization a required operation rather
   than folding it into shifted-target construction.

P54 does not attempt the adaptive TT/SIRT transport fit in the same step,
because that requires a separate implementation plan and lower-rung references.

## Required Claude Review Prompt

Claude should review this artifact read-only and answer:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

Review for source drift specifically: whether the audit uses the right
baseline, whether the fixed-gradient exception is properly separated, whether
any discrepancy is missing, and whether the immediate patch scope is too narrow
or too broad.
