# BayesFilter Quadratic Initializer To Minimal HMC Readiness Master Program

Date: 2026-07-08

## Status

`DRAFT_MASTER_PROGRAM`

## Objective

Use the committed reusable quadratic MAP-covariance initializer as a candidate
mass source for the minimal scalar SSL-LSTM target, starting with a coordinate
and mass-convention audit before any HMC runtime.

This program must not claim HMC readiness, posterior correctness, sampler
convergence, default readiness, or Zhao-Cui source faithfulness unless later
predeclared HMC evidence gates pass.

## Starting Checkpoint

Initializer checkpoint:

- commit: `9220d90`
- subject: `Add quadratic map covariance initializer`

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the quadratic initializer produce an unambiguous original-coordinate mass artifact for the minimal scalar SSL-LSTM HMC mechanics path? |
| Mechanism under test | `estimate_quadratic_map_covariance` as a mass initializer; coordinate transform from quadratic whitened `z` space to original unconstrained theta space; existing HMC geometry initialization. |
| Expected failure mode | Coordinate mismatch, nonfinite initializer, rejected geometry, ill-conditioned covariance, mass artifact in the wrong space, or trajectory length far from intended diagnostic range. |
| Primary promotion criterion | For Phase 0/1 only: coordinate convention is explicitly audited and initializer artifact is finite/SPD with source and nonclaims recorded. |
| Promotion veto | Ambiguous state space, untransformed whitened precision passed as original-coordinate precision, nonfinite value/score, non-SPD mass, missing artifact, or unsupported HMC claim. |
| Continuation veto | Broken import/test path, inability to build the minimal target, rejected initializer without a repair path, or HMC runtime being required before coordinate audit passes. |
| Repair trigger | Any coordinate mismatch, missing provenance, condition-number concern, or trajectory-scale diagnostic inconsistency. |
| Explanatory diagnostics | Locator status, geometry status, covariance source, precision/covariance eigen summaries, map-candidate role, HMC geometry target trajectory, `L * step_size`, and relation to the 1.57 heuristic. |
| What must not be concluded | HMC readiness, posterior correctness, convergence, statistical superiority, default readiness, or Zhao-Cui source faithfulness. |

## Phase Index

| Phase | Name | Objective | Required artifacts |
| --- | --- | --- | --- |
| 0 | Coordinate and mass convention audit | Prove the state-space/mass coordinate mapping before runtime. | Phase 0 audit result and Phase 1 subplan. |
| 1 | Initializer artifact smoke | Run the reusable initializer on the minimal target and write a structured finite/SPD artifact. | JSON/Markdown artifact, result note, Phase 2 subplan. |
| 2 | HMC geometry initialization smoke | Feed the artifact to `initialize_hmc_kernel_geometry` only; compare computed trajectory target and `L * step_size` diagnostics without running HMC. | Geometry artifact and result note. |
| 3 | Bounded mechanics smoke | If Phase 2 passes, run the smallest fixed-kernel mechanics screen with predeclared vetoes. | Mechanics artifact and result note. |
| 4 | Closeout | State residual gaps and whether a short-chain plan is justified. | Closeout result. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we safely move from initializer artifact to HMC mechanics without a coordinate/mass mismatch? |
| Baseline/comparator | Existing minimal Phase 5 path plus committed reusable initializer. |
| Primary pass criterion | Phase-specific: audit clarity, finite/SPD initializer, geometry initialization consistency, then mechanics smoke if reached. |
| Veto diagnostics | Coordinate mismatch, nonfinite target/gradient, non-SPD mass, unsupported HMC readiness claim, HMC launch before audit gates pass, missing artifacts. |
| Explanatory diagnostics | Trajectory target formula, 1.57 heuristic relation, eigen summaries, condition number, source labels. |
| Not concluded | Posterior correctness, HMC convergence/readiness, default policy, method superiority, Zhao-Cui faithfulness. |

## Skeptical Plan Audit

| Risk | Audit finding |
| --- | --- |
| Wrong baseline | Baseline is the existing minimal Phase 5 coordinate path, not posterior/HMC success. |
| Proxy metric promoted | Initializer and geometry diagnostics are gates for mechanics launch only, not HMC readiness. |
| Missing stop conditions | Stop before HMC runtime if coordinates or mass artifact are ambiguous. |
| Unfair comparison | No method ranking occurs. |
| Hidden assumptions | The 1.57 target is diagnostic heuristic; implementation target trajectory is computed from curvature and must be reported separately. |
| Stale context | Audit cites current committed source at `9220d90`. |
| Environment mismatch | CPU-hidden debug/reference checks only unless a later reviewed GPU plan exists. |
| Artifact mismatch | Phase 0 artifact directly records coordinate mapping and runtime boundary. |

Audit status: `PASSED_FOR_PHASE_0_COORDINATE_AUDIT`.
