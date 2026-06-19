# P71 Phase 0 Result: Governance And Current-Evidence Reset

metadata_date: 2026-06-16
status: PHASE0_PASSED_PHASE1_CONDITION_VETO_CAPTURE_READY
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 0
git_head: 94069066a70df6f1f0f2b53d32b9d452bd67f891
p70_blocker_commit: 5fdd0819ce0eb2994fb0509e66d9e9cce5f2d47c

## Decision

Phase 0 has launched and completed the P71 pre-validation evidence reset.

The current SIR d=18 state is not validation-ready.  The active handoff is
Phase 1 condition-veto capture and repair, because the P70 Phase 6 first row
still blocks on `CONDITION_NUMBER_VETO` and current code still raises on a
non-OK fixed fit before preserving a complete failed-fit diagnostic payload.

No P71 d18 validation command was run in Phase 0.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What is the exact pre-validation state of SIR d=18? |
| Baseline/comparator | P59/P8-B6 execution-only evidence, P70 Phase 5 focused tests, and P70 Phase 6 condition-number veto. |
| Primary criterion | Passed: current evidence, blockers, source/local anchors, nonclaims, and P70 drift state are recorded without promoting execution-only evidence. |
| Veto diagnostics | No missing source anchor was found in the read-level checks.  No evidence resolves the P70 condition-number blocker. |
| Explanatory diagnostics | Source-anchor table, local-code table, P70 blocker reconciliation, dirty-worktree note, and next-phase handoff. |
| Not concluded | No d18 accuracy, no same-route rank convergence, no d50/d100 scaling, no HMC readiness, no adaptive Zhao-Cui parity, no author-code failure claim. |
| Artifact | This Phase 0 result note plus the P71 visible execution ledger. |

## Skeptical Audit

The Phase 0 plan survived only as a governance/current-evidence phase.  The
main risks were wrong baseline promotion, stale P70 blocker state, token-only
source-anchor verification, and treating same-route diagnostics as accuracy.
Those risks are controlled here by recording read-level anchors, preserving the
P70 blocker, and routing Phase 1 to observability repair rather than d18
validation.

## Author Source Anchor Read Table

| Anchor | Read-level route evidence | Classification |
| --- | --- | --- |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17` | Defines `d = 0`, `m = 18`, `n = m/2`, and `T = 20`, establishing the d18 SIR row. | `source_faithful` target anchor |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:39-56` | Defines `N = 5e3`, `sqr = 1`, bounded/algebraic basis choices, TT options, and launches `full_sol(..., N, 4)` under `rng(2)`. | `source_faithful` target anchor |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43` | Sequentially pushes samples, stores state/history, reapproximates, samples through inverse SIRT, applies proposal correction weights, and records ESS. | `source_faithful` route anchor |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:49-98` | ESS-triggered enrichment, `computeL`, weighted resampling, affine expansion, shifted target construction, and split fitting data are present. | `source_faithful` route anchor |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:101-124` | Builds `TTSIRT` when `sqr == 1` and adds `log(sirt.z) - const` to the log marginal likelihood. | `source_faithful` route anchor |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47` | Computes weighted mean/covariance, Cholesky regularization, and high-ESS quantile stretch. | `source_faithful` route anchor |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:185-188` | Defines `defaultTau = 1E-8` and default TTSIRT settings. | `source_faithful` defensive-mass anchor |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:238-248` | TTSIRT construction calls the SIRT parent route and `TTFun`, with optional rounding. | `source_faithful` approximation anchor |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:81-85` | Marginalized mass is squared-core mass plus `tau`. | `source_faithful` normalizer anchor |

## Local Anchor Read Table

| Anchor | Read-level evidence | Current interpretation |
| --- | --- | --- |
| `bayesfilter/highdim/source_route.py:100-170` | Defines P59/P60/P66/P70 status constants, P70 condition thresholds, seeded-channel initializer token, and fixed-HMC adaptation class. | Local source-route governance exists; P70 veto threshold remains `1e14`. |
| `bayesfilter/highdim/source_route.py:1840-1870` | `P59AuthorSIRValidationLadderResult` permits a pass only for `d18_execution_only` with a P59-9d pass. | Execution-only evidence cannot promote higher tiers. |
| `bayesfilter/highdim/source_route.py:5329-5455` | `p59_author_sir_validation_ladder` blocks higher tiers and records nonclaims including no d18 accuracy, no d50/d100, no HMC readiness, and no adaptive parity. | P59/P8-B6 remains execution-only. |
| `tests/highdim/test_p59_author_sir_validation_ladder.py:10-77` | Tests execution-only pass, finite log marginal, ESS presence, nonclaims, and blocking of rank/correctness tiers. | Existing tests preserve the execution-only boundary. |
| `tests/highdim/test_p60_author_sir_rank_comparator.py:31-135` | Tests same-route rank comparator structure, fixed-branch adaptation tokens, nonclaims, and incoherent pass rejection. | Rank comparator tests are governance/diagnostic evidence, not accuracy evidence. |
| `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py:1-216` | Script is a CPU-only terminal diagnostic wrapper with fixed rows, predeclared command, nonclaims, P70 thresholds, and run manifest. | The failed Phase 6 command was a bounded diagnostic, not a validation run. |
| `bayesfilter/highdim/source_route.py:3197-3285` | `_p59_fixed_ttsirt_transport_from_values` builds fit quality diagnostics, then raises on non-OK fit status before constructing transport/holdout diagnostics. | The P70 condition-veto observability blocker remains active in current code. |

## Current Evidence Ledger

| Ledger | Current evidence | Boundary |
| --- | --- | --- |
| Execution-only | P59/P8-B6 and tests recognize d18 execution-only with finite local outputs and ESS fields under tiny local counts. | Not accuracy, not rank convergence, not scaling. |
| Numeric value/evaluator | P59 records finite execution-only log marginal in the tiny local route. | Does not prove full d18 numeric evaluator validity under the P70 repaired diagnostic. |
| Rank/degree | P60/P66/P70 artifacts define same-route rank/degree diagnostics and blockers. | No same-route rank convergence claim. |
| Accuracy/reference | P71 Phase 5 requires a reviewed independent same-target comparator before any accuracy claim. | Same-route replay/reference bridge is consistency-only. |
| Robustness/performance | P71 Phase 6 freezes seeds `7101` through `7105` for a future robustness gate. | No five-seed evidence exists yet. |
| Gradient/HMC | P71 Phase 7 is diagnostic-only and requires trusted GPU context if GPU evidence is interpreted. | No HMC production-readiness claim. |
| Blocker | P70 Phase 6 first row failed with `fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO`. | Phase 1 must preserve failed-fit diagnostics without weakening the veto. |

## P70 Blocker And Drift Reconciliation

The P70 Phase 6 blocker artifact was recorded at commit
`5fdd0819ce0eb2994fb0509e66d9e9cce5f2d47c` with a dirty worktree.  A raw diff
from that commit to current HEAD shows modified `bayesfilter/highdim/source_route.py`,
`bayesfilter/highdim/fitting.py`, and `tests/highdim/test_fixed_branch_fit.py`
because the P70 blocker itself came from uncommitted implementation artifacts.

The relevant current behavior still matches the blocker: current
`_p59_fixed_ttsirt_transport_from_values` computes fit and policy diagnostics,
but raises `ValueError(f"fixed_ttsirt_fit_status_{fit_result.status.value}")`
when the fit status is not `HighDimStatus.OK`.  Therefore the P70 blocker is
not stale and not resolved.

The P70 Phase 6b subplan already states the narrow repair scope: preserve
condition-veto failed-fit diagnostics without rerunning the four-row diagnostic,
without changing thresholds, and without treating a failed fit as admissible.
P71 Phase 1 should use that same boundary.

## Phase 1 Handoff

Phase 1 may begin under
`docs/plans/bayesfilter-highdim-zhao-cui-p71-phase1-condition-veto-capture-repair-subplan-2026-06-16.md`.

Required handoff conditions are:

- no full d18 validation command has run under P71;
- P70 `CONDITION_NUMBER_VETO` remains active;
- the next patch, if any, is limited to diagnostic-safe fit-status capture or
  failure-payload preservation;
- no threshold, row, rank, degree, sweep, ridge, initializer, source-route, or
  pass/fail criterion is changed after observing P70 output;
- focused tests must prove failed condition-veto fits preserve fit status,
  condition records when available, design dimensions, P70 policy payload, and
  nonclaims;
- Claude must review material implementation changes as read-only reviewer
  before Phase 2 handoff.

## Stop-Rule Compliance

Phase 0 did not:

- run d18 validation;
- patch implementation code;
- change thresholds or pass/fail criteria;
- use token presence as source-anchor verification;
- use Claude as execution authority;
- claim d18 accuracy, robustness, scaling, or HMC readiness.

