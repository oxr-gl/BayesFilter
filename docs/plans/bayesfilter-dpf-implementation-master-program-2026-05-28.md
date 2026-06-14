# Master Program: BayesFilter Differentiable Particle Filter Implementation

## Date

2026-05-28

## Status

Draft for Claude Code Opus 4.7 max-effort review.

## Lane Boundary

This is a new BayesFilter-owned differentiable particle filter implementation
planning lane.  It is separate from the high-dimensional nonlinear filtering
monograph lane and must not use or edit that lane's master program, subplans, or
chapter artifacts.

This lane starts from the DPF monograph, cited literature, DPF monograph
evidence artifacts, and the closed student DPF experimental-baseline archive.
Student work is comparison-only and discrepancy-audit evidence; it is not
implementation authority and must not be copied into production.

## Purpose

Build an auditable path toward a BayesFilter-owned differentiable particle
filter implementation.  The program must separate:

1. classical particle-filter correctness;
2. particle-flow and PF-PF proposal/correction validity;
3. differentiable resampling and transport component behavior;
4. differentiable objective and gradient semantics;
5. validation harness evidence;
6. production/API readiness.

## Governing Inputs

- DPF monograph chapters:
  - `docs/chapters/ch19_particle_filters.tex`;
  - `docs/chapters/ch19b_dpf_literature_survey.tex`;
  - `docs/chapters/ch19c_dpf_implementation_literature.tex`;
  - `docs/chapters/ch19d_dpf_hmc_dsge_macrofinance_assessment.tex`;
  - `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`;
  - `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`;
  - `docs/chapters/ch32_diff_resampling_neural_ot.tex`.
- DPF monograph evidence under `experiments/dpf_monograph_evidence/`.
- Closed student DPF archive under `experiments/student_dpf_baselines/` and
  `experiments/controlled_dpf_baseline/`, used only as comparison/discrepancy
  evidence.
- Cited literature and source support from `docs/references.bib`,
  `docs/source_map.yml`, and local ResearchAssistant summaries when available.
- Production readiness constraints from
  `docs/chapters/ch32_production_checklist.tex`.

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-implementation-*`;
- later experimental implementation files under `experiments/dpf_implementation/`
  if authorized by a reviewed phase plan;
- later focused tests under `tests/` only if authorized by DPF5 or DPF6;
- production `bayesfilter/` files only after DPF6 explicitly passes and a
  separate production patch plan is accepted.

## Forbidden Write Set

- high-dimensional nonlinear filtering plans or chapters;
- vendored student code under `experiments/student_dpf_baselines/vendor/`;
- production `bayesfilter/` code before DPF6 acceptance;
- monograph chapter edits during DPF0-A, except recommended patch registers;
- broad experiment outputs not authorized by a phase-specific evidence contract;
- unrelated V1, nonlinear-performance, or monograph lanes.

## Evidence Ledgers

Every phase must keep separate ledgers for:

1. mathematical claim status;
2. source/literature support;
3. engineering correctness;
4. numerical validity;
5. gradient/differentiability validity;
6. sampler/HMC validity;
7. performance evidence;
8. production/API readiness.

No phase may promote evidence from one ledger into another without an explicit
promotion criterion and a result note saying the criterion passed.

## Review Loop

For the master program and every subplan:

1. Codex drafts the artifact.
2. Claude Code reviews read-only using exact reviewer settings:
   `--model claude-opus-4-7 --effort max`.
3. Claude must output `ACCEPT` or `REJECT` with findings.
4. Codex audits Claude's findings.
5. If rejected and Codex agrees, Codex patches and resubmits.
6. Loop until `ACCEPT` or until 5 review iterations.
7. On the 5th version, accept only for user inspection and record unresolved
   reviewer objections as unresolved risks.  This is not scientific validation.

If the exact Claude model or max effort is unavailable, stop rather than
substituting another reviewer.

## Phase Order

| Phase | Subplan | Exit Label |
| --- | --- | --- |
| DPF0-A | `docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-plan-2026-05-28.md` | `DPF0A_DOCS_CONSISTENT`, `DPF0A_DOC_PATCH_REQUIRED`, `DPF0A_STUDENT_CLAIMS_QUARANTINED`, or blocker |
| DPF0 | `docs/plans/bayesfilter-dpf-implementation-dpf0-claim-extraction-plan-2026-05-28.md` | `DPF0_CLAIM_LEDGER_ACCEPTED` or blocker |
| DPF1 | `docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-baseline-plan-2026-05-28.md` | `DPF1_CLASSICAL_BASELINE_READY` or blocker |
| DPF2 | `docs/plans/bayesfilter-dpf-implementation-dpf2-differentiable-resampling-plan-2026-05-28.md` | `DPF2_COMPONENT_SPEC_READY` or blocker |
| DPF3 | `docs/plans/bayesfilter-dpf-implementation-dpf3-particle-flow-pfpf-plan-2026-05-28.md` | `DPF3_FLOW_PFPF_SPEC_READY` or blocker |
| DPF4 | `docs/plans/bayesfilter-dpf-implementation-dpf4-differentiable-objective-gradient-contract-plan-2026-05-28.md` | `DPF4_GRADIENT_CONTRACT_READY` or blocker |
| DPF5 | `docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-benchmark-ladder-plan-2026-05-28.md` | `DPF5_HARNESS_READY` or blocker |
| DPF6 | `docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-api-review-plan-2026-05-28.md` | `DPF6_PRODUCTION_BOUNDARY_ACCEPTED` or blocker |
| DPF7 | `docs/plans/bayesfilter-dpf-implementation-dpf7-final-audit-implementation-handoff-plan-2026-05-28.md` | `DPF7_HANDOFF_ACCEPTED` or blocker |

## Phase Summaries

### DPF0-A: Student-Document Crosswalk And Discrepancy Adjudication

Compare the DPF monograph against student reports/documents and controlled
baseline artifacts.  Classify discrepancies as:

- `consistent`;
- `assumption_mismatch`;
- `student_claim_wrong`;
- `our_doc_wrong_or_incomplete`;
- `unsupported_student_claim`;
- `implementation_only`;
- `blocked_needs_source_review`.

No monograph chapter edits are allowed in DPF0-A; record patch recommendations.

### DPF0: Monograph/Literature Claim Extraction

Extract implementation obligations from the DPF monograph and cited literature.
Each obligation must have source support, claim status, assumptions, expected
test evidence, and non-implications.

### DPF1: Classical Bootstrap/SIR Particle Filter Baseline

Plan the BayesFilter-owned classical PF foundation first: log weights, ESS,
resampling, likelihood-estimator semantics, seeds, dtypes, and LGSSM reference
recovery.  This is the correctness base for later differentiable variants.

### DPF2: Differentiable Resampling Components

Specify soft, Sinkhorn/OT, and related relaxed resampling components as optional
components.  Require finite outputs/gradients and bias/proxy labels.  Do not
claim exact likelihood, unbiased resampling, posterior validity, or HMC target
validity from gradient finiteness.

### DPF3: Particle-Flow / PF-PF Proposal And Correction

Specify particle-flow and PF-PF proposal correction obligations: proposal
density, Jacobian correction, corrected log weights, affine closed-form parity,
and nonlinear range-bearing controlled fixtures.

### DPF4: Differentiable Objective And Gradient Contract

Define what objective is differentiated and what the gradient means.  Separate
filtering proxy loss, surrogate likelihood, transport residuals, and
posterior/HMC targets.

### DPF5: Validation Harness And Benchmark Ladder

Design the validation ladder: LGSSM Kalman recovery, affine-flow parity,
range-bearing controlled fixture, student controlled-baseline qualitative
comparison, and component stress tests.  Rankings remain research diagnostics
unless downstream criteria pass.

### DPF6: Production Boundary/API Review

Decide whether anything is ready to leave experiments.  Review public API,
dependency, dtype, shape, seed, device, serialization, and documentation
contracts.  No default-policy change without a separate production evidence
contract.

### DPF7: Final Audit And Implementation Handoff

Audit all ledgers, unresolved risks, review iterations, and artifact paths.
Produce a handoff for implementation or a structured blocker.

## Global Stop Rules

Stop or record a structured blocker if:

- exact Claude Opus 4.7 max-effort review is unavailable;
- DPF0-A finds a monograph/student discrepancy that blocks claim extraction;
- a phase requires editing the high-dimensional nonlinear filtering lane;
- a phase requires copying or patching vendored student code;
- student agreement is used as correctness evidence;
- gradient finiteness is used as posterior, likelihood, or HMC validity;
- a run would be broad, expensive, or GPU-dependent without a phase-specific
  evidence contract and the required trusted GPU permissions;
- production code edits are required before DPF6;
- any result cannot state what is not concluded.

## Final Acceptance Criteria

DPF7 may pass only if:

- every phase has a reviewed result or structured blocker;
- DPF0-A discrepancy adjudication is complete enough to avoid implementing from
  disputed claims;
- implementation obligations trace to monograph equations, literature support,
  or explicitly labeled engineering choices;
- every numerical/gradient claim has an appropriate validation artifact;
- no HMC, posterior, production, monograph, model-risk, or banking claim is made
  without its own accepted evidence contract;
- `git diff --check` passes;
- final status and next action are unambiguous.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `ACCEPT`.
- Codex audit: accepted Claude's findings; no patch required.
- Final review status: reviewed master program accepted for execution planning.
