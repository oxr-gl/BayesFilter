# P70 Phase 0 Result: Governance And Source-Anchor Reset

metadata_date: 2026-06-16
status: PHASE0_PASSED_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 0
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 0 passed the local governance and source-anchor checks and Claude
read-only review.  The P70 runbook may proceed to the Phase 1 precheck under
the refreshed Phase 1 subplan.

The current failure is classified as a fixed-branch implementation/design gap:
the P69 Phase 5c result shows that the current constant-path, one-sweep fixed
fit realizes only rank channel 0 and therefore cannot support a rank-capacity
or d18-validation claim.  This is not a claim that the Zhao--Cui paper or
author code fails.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are the P70 source anchors, bug classification, and claim boundaries sufficient to begin a mathematical fixed-branch contract audit? |
| Baseline/comparator | p50 fixed-branch/UKF sections, P57/P61/P69 results, current code anchors, and author source anchors listed below. |
| Primary criterion | Satisfied locally: Phase 0 produced an anchor inventory, bug/gap classification, claim-boundary table, threshold-provenance placeholder, and refreshed Phase 1 handoff without launching repair code. |
| Veto diagnostics | No missing source anchor found in local checks; no UKF-as-truth claim; no adaptive parity claim; no low/high closeness gate; no code repair; no detached execution. |
| Explanatory diagnostics | File existence checks and targeted `rg` scans over p70 artifacts, current BayesFilter code, and Zhao--Cui author source. |
| Not concluded | No implementation repair, diagnostic rerun, d18 validation, scaling, HMC readiness, adaptive Zhao--Cui parity, or author-code failure claim. |
| Artifact preserving result | This Phase 0 result, the P70 execution ledger, and the refreshed Phase 1 subplan. |

## Anchor Inventory

### Mathematical document anchors

| Object | Anchor | Role |
| --- | --- | --- |
| Fixed-branch definition and normalizer | `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex:4131-4305` | Defines \(B_t\), shifted square-root density, defensive mass, and fixed-versus-adaptive distinction. |
| Frozen-choice consequences and constant-path initialization | `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex:4441-4585` | Explains why fixed branches need admissibility rules and why constant-path initialization gives a nonzero starting branch, not a rank-channel guarantee. |
| UKF scout role | `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex:9311-9378` | Allows UKF centers/scales/covariance as scout evidence while forbidding correctness/HMC-readiness promotion. |

### Current code anchors

| Object | Anchor | Phase 0 interpretation |
| --- | --- | --- |
| Current fixed fit uses one sweep | `bayesfilter/highdim/source_route.py:3212-3248` | Current implementation baseline for the P69 rank-channel collapse. |
| Constant-path initial cores | `bayesfilter/highdim/source_route.py:3606-3628` | Initializes only the first rank channel path. |
| ALS sweep loop | `bayesfilter/highdim/fitting.py:223-236` | The current sweep count controls how much opportunity the fixed fit has to activate channels. |
| UKF scout nonclaims | `bayesfilter/highdim/ukf_scout.py:13-22` | UKF is `scout_not_truth`. |
| UKF rank-policy limit | `bayesfilter/highdim/rank_budget.py:330-365` | UKF is diagnostic only and cannot certify rank/correctness. |

### Zhao--Cui author-source anchors

| Object | Anchor | Phase 0 interpretation |
| --- | --- | --- |
| SIR row and rank controls | `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`, `:39-56` | Author d18 SIR row has \(d=0,m=18,T=20\), squared route, author basis/domain choice, and random TT options. |
| Sequential route | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43` | Push samples, reapproximate, sample from inverse SIRT, apply proposal correction, and record ESS. |
| Local coordinates and fitting data | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:49-98` | ESS enrichment, `computeL`, weighted resampling, affine expansion, shifted target, and split fitting data. |
| TTSIRT construction and log normalizer | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:101-124` | Constructs TTSIRT and updates `log(sirt.z)-const`. |
| Weighted coordinate construction | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47` | Weighted mean/covariance, regularized Cholesky, high-ESS quantile stretch. |
| TTSIRT default mass and TT approximation | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:185-188`, `:238-248` | Executable default defensive mass and TT approximation/rounding route. |
| Squared mass plus defensive mass | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:81-85` | Sets `obj.z = obj.fun_z + obj.tau`. |

## Bug/Gap Classification

| Finding | Classification | Explanation |
| --- | --- | --- |
| P69 observed inactive higher-rank channels under rank 2 and rank 3. | `fixed_hmc_adaptation` implementation/design gap | The fixed branch declares rank but the realized current fit uses only channel 0.  This blocks rank-capacity evidence. |
| P69 observed degree-2 normalizer, holdout, and replay instability. | `fixed_hmc_adaptation` design/admissibility gap | Degree 2 improved in-sample fit residuals in the bounded diagnostic but destabilized normalizer and out-of-sample diagnostics.  This blocks degree promotion and validation until Phase 1/3/4/6 define and test admissibility gates. |
| Current path uses constant-path initialization and one sweep. | `fixed_hmc_adaptation` baseline behavior | This is part of the current fixed branch, not a source-faithful adaptive Zhao--Cui claim. |
| UKF output exists as scout/rank-policy metadata. | `fixed_hmc_adaptation` / scout evidence | UKF may guide branch objects later, but current UKF artifacts do not implement the full fixed branch and do not certify correctness. |
| Zhao--Cui author route uses propagated samples, local coordinates, TTSIRT, defensive mass, and sequential recursion. | `source_faithful` source anchor for route components only | These anchors define what must be preserved or explicitly adapted; they do not prove the current BayesFilter fixed branch is source-faithful. |
| A UKF-guided branch builder for \(\mu_t,L_t,\Omega_t,\mathcal D_t,c_t\). | planned `fixed_hmc_adaptation` unless later proven otherwise | This is the intended P70 repair route, but it must be mathematically specified and code-audited before implementation. |

## Paper-Anchor Quarantine

Phase 0 verified p50, current-code, and author-source anchors.  It did not
construct a fresh Zhao--Cui paper section/equation ledger.  Therefore Phase 0
does not authorize any new `source_faithful` claim beyond the source-route
component anchors listed here.  Phase 1 must add or cite paper anchors before
any operation is promoted to `source_faithful`; otherwise the operation remains
`fixed_hmc_adaptation` or `extension_or_invention`.

## Claim-Boundary Table

| Claim class | Allowed in P70 | Required evidence | Forbidden use |
| --- | --- | --- | --- |
| `source_faithful` | Only for a specific operation matching Zhao--Cui paper/source anchors. | Paper anchor plus author source file/line anchor and code/doc audit. | Do not apply to the whole UKF-guided fixed branch by default. |
| `fixed_hmc_adaptation` | Default class for frozen branch choices, deterministic samples/seeds, fixed ranks, fixed fitting schedules, and UKF-guided branch design. | p50 fixed-branch derivation plus source-route component anchors. | Do not call it adaptive parity or paper-scale Zhao--Cui. |
| `extension_or_invention` | Allowed only as a separately approved route. | Explicit user approval and a plan saying it no longer closes a source-faithfulness gap. | Do not use it to close Zhao--Cui source gaps silently. |
| `scout_not_truth` | Required UKF role unless a later phase proves a narrower anchored role. | p50 UKF section, `ukf_scout.py`, and `rank_budget.py` nonclaims. | Do not use UKF as correctness, rank, HMC, or validation oracle. |

## Threshold-Provenance Placeholder

Phase 0 does not set numerical thresholds.  It assigns where thresholds must be
frozen before any corresponding diagnostic can be run:

| Quantity | Must be frozen no later than | Notes |
| --- | --- | --- |
| Branch-builder coverage and scale admissibility | Phase 3 subplan/result | Must be fixed before implementation and before observing repaired branch diagnostics. |
| Channel-activity tolerance | Phase 4 subplan/result | Must be fixed before Phase 5 implementation and Phase 6 diagnostic rerun. |
| Fitting, normalizer, holdout, and replay tolerances | Phase 6 subplan before execution | Must trace to Phase 1 provenance and Phase 3/4 design artifacts; missing values block Phase 6. |
| Rank/degree ladder thresholds | Phase 7 subplan before execution | Phase 7 may run only after Phase 6 explicitly authorizes a ladder. |

## Local Checks Run

The Phase 0 file-existence checks passed for:

- all seven P70 planning artifacts;
- P69 Phase 5c result;
- p50 fixed-branch document;
- Zhao--Cui author `mainscript.m`, `full_sol.m`, `computeL.m`, `TTSIRT.m`,
  and `marginalise.m`.

The targeted source scans found the expected anchor terms:

- `scout_not_truth`, `UKF is diagnostic only`, `max_sweeps=1`, and
  `_source_route_constant_path_initial_cores` in BayesFilter code;
- `d = 0`, `m = 18`, `max_rank`, and `full_sol` in the author SIR script;
- `push_samples`, `computeL`, `TTSIRT`, `log(sirt.z)`, and `fun_into_sirt` in
  `full_sol.m`;
- weighted normalization, Cholesky, `scaleL`, and `ESS` in `computeL.m`;
- `defaultTau`, `TTFun`, and `round(approx)` in `TTSIRT.m`;
- `fun_z` and `obj.z = obj.fun_z + obj.tau` in `marginalise.m`.

The forbidden-claim scan found only guardrail/nonclaim/veto occurrences in the
P70 planning artifacts.  It did not identify an affirmative Phase 0 claim of
adaptive parity, d18 correctness, low/high closeness promotion, or HMC
readiness.

## Skeptical Audit Result

Phase 0 survived the skeptical audit:

- wrong baseline: no; the baseline is the current P59/P69 fixed path plus p50
  and author anchors;
- proxy metrics promoted: no; no numerical diagnostics were run or promoted;
- missing stop conditions: no; Phase 0 stop conditions remain active;
- unfair comparisons: no numerical comparison is made;
- hidden assumptions: threshold provenance is assigned to later phases rather
  than set after results;
- stale context: local checks verified the current files and anchors;
- environment mismatch: no GPU/CUDA/HMC command was run;
- artifact mismatch: checks and result artifacts answer the Phase 0 question.

## Refreshed Phase 1 Handoff

Phase 1 may start because Claude review agreed, provided it consumes this
result as the source-anchor and claim-boundary reset.  Its first deliverables
are:

- mathematical fixed-branch contract in proposition/proof style;
- constant-path reconciliation;
- UKF-guided branch-design classification;
- Zhao--Cui paper-anchor additions for any operation claimed as
  `source_faithful`;
- threshold-provenance register;
- executable-diagnostic approval note;
- refreshed Phase 2 current-code gap audit subplan.

## Not Concluded

- No algorithmic code was changed.
- p50 was not edited.
- No P69 Phase 5c diagnostic was rerun.
- No fixed-branch repair has been implemented.
- No d18 validation, d50/d100 scaling, HMC readiness, adaptive Zhao--Cui
  parity, or author-code failure claim has been made.

## Claude Review

R1 returned `VERDICT: REVISE` and required:

- a separate degree-normalizer instability classification;
- relocation of the executable-diagnostic approval note to Phase 1
  deliverables;
- rewording of Phase 1 Claude approval as a launch gate rather than a Phase 0
  output;
- paper-anchor quarantine before any new `source_faithful` claim.

Those repairs were applied.  R2 stalled, a probe returned `PROBE_OK`, and the
shortened R2b review returned `VERDICT: AGREE`.
