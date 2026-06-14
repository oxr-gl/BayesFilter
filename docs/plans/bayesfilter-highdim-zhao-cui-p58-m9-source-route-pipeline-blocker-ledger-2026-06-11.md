# P58-M9 Source-Route Pipeline Blocker Ledger

metadata_date: 2026-06-11
status: BLOCKER_AUDIT_DRAFT_FOR_CLAUDE_REVIEW

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | What concrete blockers prevent launching Phase 9's source-route spatial SIR ladder? |
| Baseline/comparator | P56 source-anchor audit; P57 M1-M8 pass artifacts; P57-M9 block; Zhao-Cui author SIR/source route; current BayesFilter code/tests. |
| Primary criterion | Identify the blocker set without promoting old routes, contract doubles, UKF, or memory preflight into M9 evidence. |
| Veto diagnostics | Old all-grid/local/operator route used as launch path; M6 contract doubles treated as author SIR; UKF/rank/memory diagnostics treated as d=18 source-route result; missing assembly hidden as future work while claiming readiness. |
| Not concluded | No d=18 source-route success, no d=50/d=100 scaling, no HMC readiness, no adaptive parity, no S&P reproduction. |

## Source Anchors Reopened

| Source operation | Anchor | Audit implication |
| --- | --- | --- |
| Author SIR settings | `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-56` | Paper-scale row is `d=0`, `m=18`, `T=20`, `N=5e3`, `tau=10`, squared TTSIRT, author basis/options, and rank controls. |
| Full source loop | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43` | A launchable route must initialize, push samples, augment current/previous state, reapproximate, inverse-map retained samples, and correct by `eval_pdf`. |
| Previous retained marginal | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:72-81` | For `t>1`, the previous retained SIRT is marginalized and evaluated in the previous affine frame. |
| TTSIRT construction | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:101-124` and `deep-tensor.dev/src/SIRT.m:50-86` | The target is fit into TTIRT/TTSIRT and converted into a density/CDF transport, not an all-grid transition operator. |
| Proposal correction | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:33-38` | Retained weights use `exp(-fun_post(r)) / eval_pdf(sirt,r)` after inverse transport. |
| Preconditioned route surface | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m:187-255` | P57-M8 implemented the algebraic surface, but M9 still needs any required integration into the actual SIR fitting pipeline. |

## Audit Searches

Findings from code/doc/test searches:

- `zhao_cui_sir_austria_model()` exists and is covered by P57-M1.
- `FixedTTSIRTTransport` exists and is covered by P57-M4/M5.
- `source_route_run_sequential_fixed_hmc(...)` exists and is covered by P57-M6, but its tests use analytic contract doubles and supplied/frozen specs.
- P57-M7 implements a rank/UKF policy, but it is a policy gate and diagnostic scaffold, not a d=18 M9 result.
- P57-M8 implements linear-preconditioner and preconditioned proposal-correction source surfaces, but not a d=18 SIR fitting run.
- Searches did not find an assembled author-SIR d=18 fixed TT/SIRT source-route fitting pipeline or M9 comparator-tier manifest.
- P51/P53 spatial-SIR artifacts are explicitly old local/operator/all-grid or lower-rung routes with nonclaims; they remain wrong-route evidence for M9.

## Blocker Classification

### B0: No Codified Phase-9 Launch-Readiness Guard

classification: `local_repairable_blocker`

The P57 run stopped correctly, but the codebase still lacks a small executable
guard that refuses Phase 9 launch when the available artifacts are only:
contract doubles, old local/operator/all-grid routes, rank/UKF preflight, or
unassembled source surfaces.

Fix: add a focused P58 readiness audit helper and tests.  The helper must
require author-SIR metadata, fixed TTSIRT transport evidence, frozen reference
samples, rank-policy status, previous-marginal evidence for `t>1`, and
preconditioned-route status when required.  It must emit a block token if any
piece is missing.

### B1: No Assembled Author-SIR d=18 Fixed TT/SIRT Fit Artifacts

classification: `real_m9_launch_blocker`

P57 has `FixedTTFitter`, `SquaredTTDensity`, and `FixedTTSIRTTransport`, but no
artifact or builder was found that applies them to the author SIR adjacent
targets for the d=18 row and records per-time fit manifests.

Required fix before M9 launch: build the author-SIR adjacent target rows,
perform fixed/frozen TT/SIRT fits, wrap each fitted density in
`FixedTTSIRTTransport`, and record fit statuses, ranks, bases, samples, shifts,
normalizers, and branch identities.

### B2: No Author-SIR Source-Route Step-Spec Assembly

classification: `real_m9_launch_blocker`

P57-M6 proves `source_route_run_sequential_fixed_hmc(...)` can carry supplied
retained objects through two steps.  It does not build the author SIR
`SourceRouteSequentialStepSpec` sequence from `zhao_cui_sir_austria_model()`,
observations, frozen samples, fitted transports, and previous retained
marginal axes.

Required fix before M9 launch: create a builder that turns the fitted author-SIR
transport/fitting artifacts into consecutive source-route step specs and a
manifest preserving the author current/previous-state ordering.

### B3: No M9 Comparator-Tier Manifest For d=18

classification: `real_m9_launch_blocker`

P57-M7 defines the rank policy and allowed comparator types, but no d=18 M9 row
was found with a declared tier such as `d18_execution_only`,
`d18_same_route_rank_convergence`, or `d18_correctness_candidate`.

Required fix before M9 launch: once the assembled pipeline exists, write the M9
manifest with rank, comparator tier, replay diagnostics, ESS, normalizer,
value/gradient diagnostics where applicable, memory, wall time, and nonclaims.

### B4: Preconditioned Algorithm-5 Surface Is Not Integrated Into M9

classification: `real_m9_launch_blocker_if_preconditioned_route_required`

P57-M8 passed the preconditioned source surface.  The M9 launch path still needs
to declare whether the author-SIR row uses the full or preconditioned route and
must wire the corresponding surface into the assembled step specs if required.

Required fix before M9 launch: preserve a `PASS_P57_M8_PRECONDITIONED_ALGORITHM5`
or row-specific preconditioned-route evidence token when Phase 9 requires it.

### B5: No Phase-9 Runner/Manifest Path

classification: `real_m9_launch_blocker_after_B1_B2`

No runnable M9 command or manifest path was found that consumes the assembled
author-SIR source-route specs and emits the Phase 9 result token.

Required fix before M9 launch: after B1/B2/B4 are closed, add the bounded M9
runner or documented command path and result manifest writer.

## Already Closed By P57

| Item | Status |
| --- | --- |
| Author SIR callback target | `PASS_P57_M1_AUTHOR_MODEL_CALLBACK_PARITY` |
| Fixed TTSIRT transport protocol/surface | `PASS_P57_M2_FIXED_TTSIRT_TRANSPORT_CONTRACT`, `PASS_P57_M4_SOURCE_KR_CDF_MAPS`, `PASS_P57_M5_PROPOSAL_DENSITY_RETAINED_SAMPLING` |
| Sequential retained-object carry skeleton | `PASS_P57_M6_SEQUENTIAL_FIXED_HMC_SOURCE_LOOP` |
| UKF/rank governance | `PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION` |
| Preconditioned Algorithm-5 algebraic surface | `PASS_P57_M8_PRECONDITIONED_ALGORITHM5` |

## Proxy Or Non-Launch Evidence

| Artifact family | Classification |
| --- | --- |
| P51/P53 old spatial-SIR local/operator/all-grid route | `proxy_not_launch_evidence`; useful as historical blocker evidence only. |
| M6 contract-double source loop tests | `proxy_not_launch_evidence`; proves skeleton, not author-SIR fitting. |
| UKF scout and memory budget | `proxy_not_launch_evidence`; diagnostic or veto only. |
| Fixed uniform `FixedTTSIRTTransport` tests | `proxy_not_launch_evidence`; proves map contracts, not fitted author-SIR d=18. |

## Repair Decision

Proceed to Phase B with B0 as the local repair target.

B1-B5 require a larger author-SIR fitting and runner implementation.  This P58
lane must not pretend those are closed unless code and artifacts actually
assemble and run the fixed TT/SIRT source-route pipeline.

## Token

`BLOCKERS_P58_M9_SOURCE_ROUTE_PIPELINE_IDENTIFIED`
