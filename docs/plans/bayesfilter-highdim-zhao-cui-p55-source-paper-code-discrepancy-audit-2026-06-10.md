# P55 Discrepancy Audit: Zhao--Cui Paper/Source Vs Current BayesFilter

metadata_date: 2026-06-10
program: P55-zhao-cui-paper-source-code-conformance
status: REVIEWED_AFTER_CLAUDE_LOOP
supervisor: Codex
reviewer: Claude Code read-only

## Task Decomposition

This artifact covers task 1 of the requested workflow:

1. audit current BayesFilter code against the Zhao--Cui paper/source;
2. write every material discrepancy found under `docs/plans`;
3. exclude noncompliance that exists solely because BayesFilter requires a
   fixed/fixed-gradient variant for HMC;
4. submit the audit to Claude Code read-only review until convergence or a
   maximum of five rounds.

This artifact does not execute repairs.  The repair plan and execution result
are separate artifacts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Besides the legitimate fixed-variant requirement, where does current BayesFilter still disagree with the Zhao--Cui paper/source behavior? |
| Baseline/comparator | Zhao--Cui paper as captured in P30/P40 notes; local author source under `third_party/audit/zhao_cui_tensor_ssm_p10/source`; P10/P34/P48/P49/P54 source-audit artifacts. |
| Current implementation inspected | `bayesfilter/highdim/source_route.py`, `filtering.py`, `fitting.py`, `squared_tt.py`, `transport.py`, `models.py`, `transition_route.py`, `rank_budget.py`, `ukf_scout.py`, and highdim tests P30--P54. |
| Primary criterion | Every material discrepancy is classified with source anchor, BayesFilter anchor, severity, fixed-variant carveout status, and repair/test action. |
| Veto diagnostics | Counting the existence of the fixed branch itself as an error; omitting source anchors; treating governance helpers as full execution; treating fixed-design substitutes as paper/source conformance; proposing MATLAB code copying. |
| Not concluded | No full source-route implementation, no paper-scale SIR/predator-prey readiness, no HMC readiness from the source route, no smoothing support, no S&P 500 reproduction. |

## Fixed-Variant Carveout

The deterministic fixed/fixed-gradient branch is legitimate and required for
HMC-style work.  The following are not counted as source noncompliance by
themselves:

- fixed-rank deterministic fitting for a separately labeled gradient lane;
- replayable branch manifests and deterministic seeds;
- TensorFlow/TFP implementation choices needed for differentiability;
- CPU/GPU/backend choices required by BayesFilter governance.

However, it remains noncompliant to label a fixed-gradient adaptation as
reproduction of the author's adaptive TT/SIRT route.  Adaptive Zhao--Cui
requirements are excluded from future missing-gap lists unless explicitly
requested as a separate historical reproduction study.

## Source Operation Baseline

| Source operation | Source anchor |
| --- | --- |
| Initialize `[theta, x_0]` samples | `full_sol.m` line 22; `pre_sol.m` line 17 |
| Push samples and update weights by likelihood | `ssmodel.m` lines 45--59; `full_sol.m` lines 23--26 |
| Augment target state as `[theta, x_t, x_{t-1}]` | `full_sol.m` lines 23--26; `pre_sol.m` lines 19--21 |
| ESS and enhanced sample loop | `full_sol.m` lines 49--63; `pre_sol.m` lines 35--103 |
| Weighted recentering with pruning and quantile scaling | `computeL.m` lines 14--47 |
| Prior or previous retained object / marginalization | `full_sol.m` lines 72--81; `pre_sol.m` lines 110--127 |
| Shifted local-coordinate target | `full_sol.m` lines 84--98; `pre_sol.m` lines 187--239 |
| TTIRT/TTSIRT fit/update | `full_sol.m` lines 101--129; `pre_sol.m` lines 204--244 |
| Normalizer update | `full_sol.m` line 124; `TTSIRT.marginalise` per P48/P49 |
| Retained sample generation by inverse transport | `full_sol.m` lines 33--38; `pre_sol.m` lines 245--256 |
| Proposal correction and ESS | `full_sol.m` lines 35--42; `pre_sol.m` lines 251--256 |
| Preconditioned route variants | `pre_sol.m` lines 131--182, 187--260 |
| Smoothing/backward conditionals | `full_sol.m` lines 139--205; `pre_sol.m` lines 270--340 |

## Discrepancy Ledger

| ID | Classification | Topic | Source/paper anchor | Current BayesFilter anchor | Difference | Severity | Fixed-variant carveout? | Repair/test action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P55-D01 | missing implementation | Full executable source-route filter loop | `full_sol.solve` lines 21--43; `pre_sol.solve` lines 16--30 | `source_route.py` helper contracts; `filtering.py` fixed-design value paths | Source route has a time loop that propagates samples, reapproximates, samples from fitted transport, corrects proposal weights, and stores retained objects. BayesFilter has pieces and guards but no executable source-route filter loop. | critical | no | Create a source reapproximation boundary with transport fit first, then a short sequential loop after lower-rung tests pass. |
| P55-D02 | missing implementation | Previous retained-object marginalization/evaluation | `full_sol.m` lines 72--81; `pre_sol.m` lines 113--127; P49 contract step 5 | `SourceRouteRetainedObject` skeleton; P54 required operation audit | The operation is now named, but there is no callable retained-density marginalization/evaluation path for `t>1`.  This is not required for a pure `t=1` one-step target, but it is required before any two-step or sequential source filter claim. | critical for sequential filtering | no | Add a clean-room retained density interface and low-dimensional marginalization tests before multi-step filtering claims. |
| P55-D03 | excluded author-route difference | Adaptive TTIRT/TTSIRT transport fit | `full_sol.m` lines 101--121; `pre_sol.m` lines 204--244; `TTFun.cross` per P48 | `fitting.py` fixed-rank ALS; `source_route.py` retained-object skeleton | BayesFilter fixed branch is deterministic and useful for gradients but is not the adaptive/random TTIRT/TTSIRT fit used by the author's MATLAB route. Under the fixed/HMC-compatible requirement, adaptive parity is a historical difference, not a required missing gap. | not a required repair target | yes, excluded by fixed-gradient requirement | Do not list adaptive TT/SIRT parity as a future gap.  Keep a label guard so fixed-branch results are not claimed as reproduction of the author's adaptive route. |
| P55-D04 | partial implementation | ESS enhanced sampling loop | `full_sol.m` lines 49--63; `pre_sol.m` lines 35--103 | `source_route_needs_enhancement`; `SourceRouteSampleDiagnostics` | ESS calculation exists, but the source doubling/enhanced sampling loop is not integrated with prior/retained-object sampling or source reapproximation. | high | no | Implement an enhancement policy object and tests for t=1 prior resampling and t>1 retained-object resampling. |
| P55-D05 | partial implementation | `computeL` pruning and quantile scaling | `computeL.m` lines 14--47 | `source_route_recenter` and P54 tests | Weighted covariance and quantile scaling are represented; NaN/Inf sample pruning and integration into the source filter loop are incomplete. | medium-high | no | Add finite-sample pruning semantics and tests against source behavior on contaminated sample batches. |
| P55-D06 | partial implementation | Shift constant and affine determinant accounting | `full_sol.m` lines 84--93; `pre_sol.m` lines 187--195, 222--232 | `source_route_shifted_negative_log_target`; `SourceRouteNormalizerContribution` | BayesFilter has identities, but no first-class source-route target object combining prior/marginal density, transition, likelihood, shift constant, and determinant policy. | high | no | Add `SourceRouteTarget` contract/helper with analytic Gaussian and nonlinear dense equality tests. |
| P55-D07 | missing implementation | Retained sample generation from fitted transport | `full_sol.m` lines 33--38; `pre_sol.m` lines 245--249 | `SourceRouteRetainedObject.samples`; no sampler from transport | BayesFilter stores samples in the retained skeleton but cannot sample through a fitted source transport object. | critical | no | Add transport object protocol for inverse transport sampling and proposal log density. |
| P55-D08 | partial implementation | Proposal correction inside source route | `full_sol.m` lines 35--42; `pre_sol.m` lines 251--256 | proposal log-weight helper functions | Correction algebra exists, but it is not integrated with retained sample generation, true target evaluation, ESS recording, or normalizer evidence. | high | no | Add one-step proposal-correction result object and dense one-step recovery tests. |
| P55-D09 | missing implementation | Source preconditioned route variants | `pre_sol.m` lines 131--182, 187--260; predator-prey script lines 55--79 | `SourceRoutePreconditionerContract`; P49 preconditioner tests | Variant metadata and identity checks exist, but the two-stage preconditioner/residual construction and map composition are not executable. | critical for predator-prey | no | Defer production predator-prey claims; plan a later preconditioned-route phase after unpreconditioned one-step route passes. |
| P55-D10 | claim/documentation drift risk | P47 fixed-design route labels | P48 D01--D03; source `full_sol` / `pre_sol` | P47 registry/tests label “documented-deviation fixed-design substitute” | P47 tests correctly preserve deviation labels, but downstream summaries can still be misread as source implementation success unless P55 closeout repeats the boundary. | medium | yes for the fixed route existence; no for overclaim | Keep fixed-variant carveout and add source-conformance plan language that no fixed-design row closes source-route discrepancies. |
| P55-D11 | ad hoc invention / blocked route | P53 local-neighborhood/rank-scaling route | P48 D10; P54 D01/D09 | `transition_route.py`; P53 tests/artifacts | Local-neighborhood/rank-scaling is an exploratory workaround, not source behavior. P54 guards block it as source-faithful drift, but it still exists as a separate route. | high for claim drift | no if labeled exploratory; noncompliant if source-faithful | Keep route quarantined from source-faithful pass tokens; do not build P55 repair on it. |
| P55-D12 | missing implementation | Model-specific source transforms for generalized SV | `svmodels/true2ftt.m`, `ftt2true.m`, `like.m` | `native_generalized_sv.py`; `sv_mixture_cut4.py`; P44/P47 tests | BayesFilter has generalized/native SV diagnostics and transformed SV mixture lanes, but no audited source-route parameter transform and Student/Box-Cox likelihood path matching `svmodels`. | medium-high | no | Add target-equality audit/tests for `true2ftt`/`ftt2true` semantics before source-route generalized SV claims. |
| P55-D13 | missing/scoped implementation | Spatial SIR paper-scale route under the fixed protocol | `eg3_sir/mainscript.m` lines 14--55 | `SpatialSIRSSM`; P47/P52/P53 SIR diagnostics | Source uses `d=0,m=18,T=20,N=5e3,max_rank=40` with adaptive/random TTSIRT on augmented dimension 36. BayesFilter’s fixed or rank-budget routes still need a faithful fixed/HMC-compatible route for this model scale; adaptive parity itself is excluded. | critical for SIR fixed-route claims | yes for adaptive parity only | Do not retry d=18 as a fixed-route success claim until one-step fixed/source-contract filtering and transport integration pass lower rungs. |
| P55-D14 | missing/scoped implementation | Predator-prey source route | `eg4_predatorprey/mainscript.m` lines 14--79 | `PredatorPreySSM`; P47/P49 predator-prey diagnostics | Source uses bounded full and preconditioned TTSIRT with `pifg`; BayesFilter has fixtures and fixed-design diagnostics but no source preconditioned execution. | critical for predator-prey claims | no | Put predator-prey after unpreconditioned route and preconditioner phase gates. |
| P55-D15 | intentionally out of scope | Smoothing/backward conditionals | `full_sol.smooth`; `pre_sol.smooth` | `SourceRouteSmoothingBoundary`; P49/P50 smoothing boundary tests | Smoothing is correctly not claimed, but source smoothing is not implemented. | medium unless claimed | no | Keep as explicit out-of-scope blocker; no filtering repair should imply smoothing. |
| P55-D16 | governance/backend | MATLAB source reuse and backend | Source license files and MATLAB code; AGENTS.md | BayesFilter TF/TFP policy | Any repair must be clean-room TF/TFP and cannot copy MATLAB code. | critical | yes, backend choice is legitimate | Make every implementation phase record clean-room translation and no-copy status. |

## Additional Findings Beyond P48/P54

1. P55-D03 is retained only as a label-control/historical-source boundary:
   adaptive TT/SIRT parity is not a required future gap for the fixed/HMC
   branch.
2. P55-D05 is more specific than P54: `computeL` also prunes NaN/Inf samples
   before weighting, not only quantile-scales high-ESS batches.
3. P55-D12 adds the generalized-SV source transform/likelihood gap.  Earlier
   work tested useful SV approximations, but not the author `svmodels` transform
   path as a source-route implementation.
4. P55-D06 separates target construction from standalone shift/determinant
   identities.  A source-route implementation needs a first-class target object
   before fitting or sampling.
5. P55-D10 records that fixed-design existence is not an error, but fixed-design
   results cannot close source-route discrepancy rows.

## Proposed Repair Priority

| Priority | Discrepancies | Why |
| --- | --- | --- |
| A0 | P55-D06 | A true fixed/source-contract reapproximation boundary needs a first-class source target before retained sampling or proposal correction can be meaningful. |
| A1 | P55-D07, D08 | Retained sample generation and proposal correction depend on the fitted transport object from A0. |
| A2 | P55-D01, D02 | The executable loop and previous-retained-object marginalization are sequential `t>1` obligations after one-step reapproximation exists. |
| B | P55-D04, D05 | ESS enhancement and finite-sample pruning make the path closer to source behavior and prevent silent finite/nonfinite weighting errors. |
| C | P55-D09, D13, D14 | Preconditioned predator-prey and SIR should wait until the unpreconditioned source path works. |
| D | P55-D12 | Generalized SV source transforms should be audited with target-equality tests before source-route claims. |
| Deferred | P55-D15 | Smoothing remains out of filtering-likelihood scope unless explicitly requested. |
| Excluded | P55-D03 | Author-adaptive TT/SIRT parity is not a future missing gap under the fixed/HMC-compatible requirement. |

## What This Audit Does Not Conclude

- It does not say the fixed-gradient branch should be removed.
- It does not claim the author source is production-quality Python.
- It does not make adaptive TT/SIRT parity a required future gap.
- It does not certify paper-scale model readiness.

## Claude Review Request

Claude should review this audit read-only and return:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

Review specifically for missed discrepancies, wrong source anchors,
fixed-variant carveout mistakes, overclaims, and whether the repair priority
would still let an implementation drift away from the author code/paper.
