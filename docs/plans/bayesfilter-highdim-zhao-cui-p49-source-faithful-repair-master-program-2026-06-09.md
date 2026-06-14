# P49 Master Program: Source-Faithful Zhao--Cui Repair And Gradient-Lane Boundary

metadata_date: 2026-06-09
program: P49-source-faithful-repair
status: PLAN_REVIEW_CONVERGED
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Repair the eight serious issues identified by P48 by separating two legitimate
but different routes:

1. a clean-room, source-faithful filtering lane for Zhao--Cui-style filtering;
2. a deterministic gradient-bearing adaptation lane for HMC and score work.

The program must not treat the need for analytical gradients as permission to
invent an ad hoc route and call it source-faithful Zhao--Cui.

## Binding Source-Anchor Policy

For this lane, "source-faithful" is not a stylistic label.  It requires
paper/source grounding before implementation:

1. cite the relevant Zhao--Cui paper section/equation or reviewed paper note;
2. cite the author source file and line-level operation under
   `third_party/audit/zhao_cui_tensor_ssm_p10/source`;
3. classify the implementation choice as one of:
   - `source_faithful`: matches the cited paper/source operation;
   - `fixed_hmc_adaptation`: preserves the author's algorithmic route but
     freezes randomness, ranks, bases, schedules, or samples for HMC
     differentiability;
   - `extension_or_invention`: not present in the author paper/source and not
     allowed to close source-faithfulness gaps without explicit user approval.

Any plan, implementation, result, or review that claims source faithfulness
without both paper and source-code anchors must stop with
`BLOCK_SOURCE_UNGROUNDED`.  Claude review must verify the cited anchors, not
only internal consistency.

## Eight Repair Targets

| Target | Error to repair | Required outcome |
| --- | --- | --- |
| R1 | Fixed-branch evidence was at risk of being promoted as source-route equivalence. | Route-specific claim labels and pass tokens. |
| R2 | Current multistate route retains all axes on tensor-product grids. | Source-faithful retained object design using TT/SIRT density/transport objects and samples. |
| R3 | Current propagation uses pairwise grid-to-grid transition density. | Source-style sample propagation and reapproximation route. |
| R4 | ESS, resampling, enhanced sampling, and proposal correction are missing. | ESS and proposal-correction contracts with tests. |
| R5 | Source-style recentering, affine maps, determinant accounting, and coordinate maps are incomplete. | Weighted recentering/Jacobian contract and tests. |
| R6 | M5b predator-prey failure was from the fixed-design route, not evidence against source Zhao--Cui. | Preconditioned/residual route plan and ablation ladder. |
| R7 | Source-style smoothing/backward conditionals are not implemented. | Explicit smoothing boundary and, if implemented, separate tests. |
| R8 | Analytical-gradient need was not separated sharply enough from source fidelity. | Separate gradient-lane evidence contract and forbidden-claim guards. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter repair the Zhao--Cui implementation program so that source-faithful filtering claims, fixed-branch gradient claims, and blocked claims are no longer conflated? |
| Baseline/comparator | P48 discrepancy ledger; Zhao--Cui source snapshots under `third_party/audit`; current `bayesfilter/highdim/*`; exact Kalman/dense/CUT4 references where applicable. |
| Primary pass criterion | Every R1--R8 issue has a reviewed phase subplan, explicit pass/fail criteria, repair loop, result artifact path, and non-claims. |
| Veto diagnostics | Any plan that relabels a gradient adaptation as source-faithful; any fixed-grid proxy promoted as source-route evidence; any source-faithfulness claim without paper and source-code anchors; any code-copying from MATLAB; any phase without a stop condition; any production claim without matched target evidence. |
| Explanatory diagnostics | P30--P49 tests and artifacts, small smoke tests, line anchors, complexity preflights, likelihood/gradient calibration diagnostics. |
| Not concluded | No implementation is completed by this master plan alone; no paper-scale readiness; no HMC readiness; no S&P 500 reproduction; no adaptive-route differentiability. |
| Artifacts | This master program, phase subplans, visible execution runbook, visible execution ledger, phase result artifacts, Claude review ledger. |

## Skeptical Plan Audit

Status: REVIEWED.

- Wrong baseline risk: phase comparisons must use source snapshots or exact
  references, not P46/P47 fixed-grid artifacts as if they were source truth.
- Source-anchor risk: no phase may implement a new Zhao--Cui route before
  checking the paper and author source; missing anchors trigger
  `BLOCK_SOURCE_UNGROUNDED`.
- Proxy promotion risk: finite tiny tests and branch replay are explanatory
  unless the phase explicitly makes them primary criteria.
- Hidden assumption risk: a route can be good for gradients and bad for source
  fidelity, or good for source filtering and bad for gradients.
- Environment mismatch risk: MATLAB source is an audit reference unless a
  separate runtime approval exists; BayesFilter production code stays TF/TFP.
- Stop-condition risk: every phase must define pass, repair, and human-required
  stop conditions.
- Artifact adequacy risk: every phase has a required result artifact before it
  can pass.

## Phase Index

| Phase | Name | Repair targets | Subplan | Required result artifact | Required pass/block token |
| --- | --- | --- | --- | --- | --- |
| P49-M0 | Route-Claim Governance | R1, R8 | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m0-route-claim-governance-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m0-route-claim-governance-result-2026-06-09.md` | `PASS_P49_M0_ROUTE_CLAIM_GOVERNANCE` or `BLOCK_P49_M0_ROUTE_CLAIM_GOVERNANCE` |
| P49-M1 | Source Route Contract | R2, R3, R4, R5 | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m1-source-route-contract-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m1-source-route-contract-result-2026-06-09.md` | `PASS_P49_M1_SOURCE_ROUTE_CONTRACT` or `BLOCK_P49_M1_SOURCE_ROUTE_CONTRACT` |
| P49-M2 | Retained TT/SIRT Object Skeleton | R2 | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m2-retained-transport-object-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m2-retained-transport-object-result-2026-06-09.md` | `PASS_P49_M2_RETAINED_TRANSPORT_OBJECT` or `BLOCK_P49_M2_RETAINED_TRANSPORT_OBJECT` |
| P49-M3 | Sample Propagation, ESS, And Proposal Correction | R3, R4 | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m3-sample-ess-proposal-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m3-sample-ess-proposal-result-2026-06-09.md` | `PASS_P49_M3_SAMPLE_ESS_PROPOSAL` or `BLOCK_P49_M3_SAMPLE_ESS_PROPOSAL` |
| P49-M4 | Recentring, Jacobian, And Normalizer Accounting | R5 | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m4-recentering-normalizer-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m4-recentering-normalizer-result-2026-06-09.md` | `PASS_P49_M4_RECENTERING_NORMALIZER` or `BLOCK_P49_M4_RECENTERING_NORMALIZER` |
| P49-M5 | Preconditioned Predator-Prey Repair | R6 | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m5-preconditioned-predator-prey-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m5-preconditioned-predator-prey-result-2026-06-09.md` | `PASS_P49_M5_PRECONDITIONED_PREDATOR_PREY` or `BLOCK_P49_M5_PRECONDITIONED_PREDATOR_PREY` |
| P49-M6 | Smoothing Boundary And Backward Conditionals | R7 | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m6-smoothing-boundary-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m6-smoothing-boundary-result-2026-06-09.md` | `PASS_P49_M6_SMOOTHING_BOUNDARY` or `BLOCK_P49_M6_SMOOTHING_BOUNDARY` |
| P49-M7 | Deterministic Gradient-Lane Contract | R8 | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m7-gradient-lane-boundary-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m7-gradient-lane-boundary-result-2026-06-09.md` | `PASS_P49_M7_GRADIENT_LANE_BOUNDARY` or `BLOCK_P49_M7_GRADIENT_LANE_BOUNDARY` |
| P49-M8 | Integration Closeout | R1--R8 | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m8-integration-closeout-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m8-integration-closeout-result-2026-06-09.md` | `PASS_P49_M8_INTEGRATION_CLOSEOUT` or `BLOCK_P49_M8_INTEGRATION_CLOSEOUT` |

## Repair Loop Rule

For each phase, Codex must continue through fixable issues instead of stopping
for no valid reason.

Fixable issues include:

- failed local tests with a clear code or artifact repair path;
- Claude `REVISE` findings that name specific fixable flaws;
- missing result metadata;
- stale labels or unsupported claims;
- local command errors caused by wrong command scope, import path, or test
  selection.

Human-required blockers include:

- package installation, network fetch, credentials, or external runtime setup;
- destructive git/filesystem changes;
- modifying unrelated dirty user work;
- changing pass/fail criteria after seeing results;
- changing backend/default policy;
- GPU/special hardware claims without trusted-context approval;
- Codex/Claude non-convergence after five review rounds for the same blocker.

## Claude Review Loop

Claude is read-only reviewer only.  Use up to five iterations.  Stop early on:

```text
VERDICT: AGREE
```

If Claude returns `VERDICT: REVISE`, Codex patches the plan or runbook and
resubmits, unless the finding is a human-required blocker.  At iteration 5,
accept only if there is no major blocker; otherwise record
`BLOCKED_P49_PLAN_REVIEW_MAJOR_ISSUE`.

## Approval Needs For Execution

The visible runbook anticipates asking the user to approve:

1. direct escalated `claude -p` read-only review prompts for every material
   phase, blocker plan, and closeout review;
2. CPU-only Python validation commands such as `python -m json.tool`,
   `python -m compileall`, and focused `pytest`;
3. TensorFlow/TFP CPU-only tests with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`;
4. no network fetch, no package installation, no GPU run, no detached supervisor,
   and no destructive git operation unless separately approved.
