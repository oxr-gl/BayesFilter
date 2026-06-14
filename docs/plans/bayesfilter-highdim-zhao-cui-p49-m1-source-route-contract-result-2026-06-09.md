# P49-M1 Result: Source Route Contract

metadata_date: 2026-06-09
phase: P49-M1
status: PASS
supervisor: Codex
reviewer: Claude Code read-only

PASS_P49_M1_SOURCE_ROUTE_CONTRACT

## Decision Table

| Field | Result |
| --- | --- |
| Decision | PASS |
| Primary criterion status | PASS: a clean-room source-route specification exists with operation order, data structures, shape contracts, normalizer accounting, function boundaries, reference tests, and non-claims. |
| Veto diagnostic status | PASS: the contract rejects all-axes pairwise grids as the paper-scale source route, forbids copied MATLAB code, and makes determinant/proposal-correction accounting explicit. |
| Main uncertainty | The contract is not yet an implementation. M2--M5 must convert the retained object, ESS/proposal, recentering, and preconditioned-route pieces into code/tests or narrower blockers. |
| Next justified action | Submit M1 to Claude read-only review, then advance to P49-M2 only if Claude returns `VERDICT: AGREE`. |
| What is not concluded | No numerical accuracy, source-faithful implementation completion, paper-scale readiness, smoothing support, HMC readiness, or differentiability of the source route. |

## Evidence Contract Result

Question: What exact clean-room algorithm must BayesFilter implement to be
source-faithful enough for filtering claims?

Answer: the required clean-room route is specified in:

- `docs/plans/bayesfilter-highdim-zhao-cui-p49-clean-room-source-route-contract-2026-06-09.md`

## Source Anchors Used

| Source surface | Use in M1 |
| --- | --- |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m` | Full source route: augmented samples, sample propagation, ESS/enhancement, recentering, shifted target, TT/SIRT fit, normalizer update, proposal correction, smoothing boundary. |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m` | Preconditioned/residual route variants, map composition, preconditioner target and posterior target split. |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTFun/cross.m` | Adaptive/random TT fitting behavior that the existing fixed branch does not reproduce. |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m` | Marginalization and normalizer metadata requirements. |
| P48 discrepancy ledger | Confirms the required source-route components and the split from the gradient-bearing fixed branch. |

No source MATLAB code was copied into BayesFilter production code.

## Contract Summary

The M1 contract requires the source-faithful filtering lane to include:

- augmented state/sample shape `[d+2m, N]`;
- source-style sample propagation;
- ESS and enhanced-sampling diagnostics;
- weighted affine recentering with `mu`, `L`, and determinant policy;
- shifted target construction with an explicit shift constant;
- retained TT/SIRT density/transport object, not all-grid retention;
- normalizer update using transport normalizer and shift accounting;
- retained sample generation;
- proposal-correction log weights and final ESS;
- separate preconditioned/residual route variants;
- separate smoothing boundary.

## Implementation Boundary

Existing BayesFilter fixed-branch code remains classified as
`gradient_bearing_adaptation`.  It can be reused for diagnostics or exact
comparators only when artifacts keep that route label.  It is not the M1
source-faithful route.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d`; worktree is dirty with unrelated existing files. |
| Commands | `sed` reads of P49 M1 subplan, P48 ledger, source snapshots, and current highdim implementation surfaces. |
| Environment | Local shell, static/design phase only. |
| CPU/GPU status | CPU-only by scope; no GPU command run. |
| Random seeds | N/A. |
| Output artifacts | This result file; clean-room source-route contract. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m1-source-route-contract-subplan-2026-06-09.md` |

## Post-Run Red-Team Note

Strongest alternative explanation: the contract could still be too high-level
to catch a future implementation that has the right nouns but the wrong
normalizer/proposal math.  M2--M4 mitigate this by requiring shape/object,
ESS/proposal, and affine-normalizer tests before production claims.

What would overturn this M1 pass: a Claude or Codex finding that the contract
omits one of the material source-route mechanisms from P48 D01--D08, or that it
permits all-grid pairwise propagation as the paper-scale route.

Weakest part of the evidence: M1 is a design artifact, not executable
source-route filtering.
