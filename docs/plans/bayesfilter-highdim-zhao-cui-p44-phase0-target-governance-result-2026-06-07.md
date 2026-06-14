# P44-M0 Result: Target Governance Matrix

metadata_date: 2026-06-08
phase: P44-M0
run_id: `p44-codex-supervised-20260608-013203`
Status: `PASS_P44_M0_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | M0 target-governance matrix drafted for all P44 phases. |
| Primary criterion status | Passed read-only Claude review at code/governance Iteration 4. |
| Veto diagnostic status | No target-equality promotion is made in M0; later phases remain gated by their labels. |
| Main uncertainty | Later implementation phases must still freeze exact parameter vectors, data fixtures, and references. |
| Next justified action | Run M0 phase gate, then proceed to P44-M1 if the gate passes. |
| Not concluded | No numerical value/gradient correctness, no HMC readiness, no paper-scale Zhao--Cui reproduction. |

## Evidence Contract

Question: for each planned P44 model family, are CUT4,
Zhao--Cui/fixed-design TT, and the reference route evaluating the same
likelihood and score target?

Baseline/comparator:

- P44-M1 uses exact Kalman as governing baseline.
- P44-M2--M4 use dense/refined references on tiny same-target nonlinear
  additive-Gaussian fixtures.
- P44-M5--M6 are diagnostic-only closures unless a matched closure target is
  later declared.
- P44-M7 is blocked for same-target equality until its target-definition table
  passes review.
- P44-M8 is closeout and introduces no new numerical target.

Primary promotion criterion:

- Every P44 phase receives one of the required M0 labels and carries
  parameterization, dimension, panel-structure, target-identity, and reference
  route metadata.

Veto diagnostics:

- missing parameterization;
- missing observation/noise contract;
- missing horizon/dimension convention;
- comparing transformed and native targets without Jacobian accounting;
- using diagnostic closures as native-model evidence.

## Target-Governance Matrix

Machine-readable matrix:

`docs/plans/bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-matrix-p44-codex-supervised-20260608-013203.json`

Summary:

| Phase | Target identity | Reference route | Panel structure | Promotion status |
| --- | --- | --- | --- | --- |
| P44-M0 | governance only | document-grounded subplan audit | not applicable | `DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM` |
| P44-M1 | exact LGSSM likelihood/score | exact Kalman | `factorized_product` | `SAME_TARGET_EXACT_OR_DENSE_REFERENCE` |
| P44-M2 | cubic additive-Gaussian observation | dense quadrature refinement | `factorized_product` | `SAME_TARGET_APPROXIMATION_WITH_EXPLICIT_REFERENCE_GAP` |
| P44-M3 | quadratic additive-Gaussian observation | dense quadrature with symmetric-mode coverage | `factorized_product` | `SAME_TARGET_APPROXIMATION_WITH_EXPLICIT_REFERENCE_GAP` |
| P44-M4 | nonlinear additive-Gaussian transition | dense/sequential quadrature refinement | `factorized_product` | `SAME_TARGET_APPROXIMATION_WITH_EXPLICIT_REFERENCE_GAP` |
| P44-M5 | spatial SIR diagnostic closure | model-contract and finite closure diagnostics | not applicable | `DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM` |
| P44-M6 | predator-prey diagnostic closure | model-contract and finite closure diagnostics | not applicable | `DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM` |
| P44-M7 | generalized SV target unresolved | blocked pending target-definition table | not applicable | `BLOCKED_TARGET_UNSPECIFIED` |
| P44-M8 | integration closeout | traceability audit | not applicable | `DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM` |

## Phase Governance Consequences

- P44-M1 may claim exact same-target Tier-1 local correctness only after
  Kalman value and score checks pass in dimensions 1, 2, and 3.
- P44-M2--M4 may compare CUT4 and Zhao--Cui only against the same declared
  nonlinear additive-Gaussian target and must record approximation gaps against
  the dense/refined reference.
- P44-M5--M6 may run finite closure diagnostics but must not claim native SIR
  or native predator-prey likelihood correctness.
- P44-M7 cannot run a generalized-SV same-target equality test until its target
  table is complete and reviewed.
- P44-M8 is a synthesis phase and cannot add new numerical claims.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `N/A - dirty worktree preserved; command manifest captures current files` |
| Command environment | CPU-only/document validation; no GPU used |
| Data version | deterministic documentation/subplan inputs |
| Random seeds | `N/A` |
| Wall time | tiny local validation only |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-subplan-2026-06-07.md` |
| Matrix file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-matrix-p44-codex-supervised-20260608-013203.json` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-result-2026-06-07.md` |

## Gate Markers

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_local_evidence_run: `COMPLETE`
p44_evidence_audit: `COMPLETE`
p44_result_note_substance: `COMPLETE`
p44_traceability_or_nonclaim: `COMPLETE`
p44_command_count: `2`
p44_long_run_used: `false`
