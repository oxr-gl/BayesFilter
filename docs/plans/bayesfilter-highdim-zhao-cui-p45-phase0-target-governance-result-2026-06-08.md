# P45-M0 Result: Target Governance Registry

metadata_date: 2026-06-08
phase: P45-M0
run_id: `p45-codex-supervised-20260608-055034`
Status: `PASS_P45_M0_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | P45-M0 target registry created and made executable with focused tests. |
| Primary criterion status | Passed after read-only Claude code/governance review Iteration 2. |
| Veto diagnostic status | No equality claim is authorized for generalized SV, spatial SIR, or predator-prey in M0; unsupported rows are blocked or diagnostic-only. |
| Main uncertainty | P45-M1 must still decide whether a multistate/factorized Zhao--Cui route can be implemented or whether M2--M4 remain blocker/nonclaim phases. |
| Next justified action | Run the P45-M0 phase gate, then proceed to P45-M1 if the gate passes. |
| Not concluded | No value/gradient correctness, no HMC readiness, no production score API, no native generalized-SV/SIR/predator-prey equality claim. |

## Evidence Contract

Question: for each model family, what exact target is being compared, and is a
same-target CUT4--Zhao--Cui comparison authorized, blocked, or diagnostic-only?

Baseline/comparator:

- Target registry fields are checked against P45-M0 subplan requirements.
- Existing P44 generalized-SV, SIR, and predator-prey diagnostics are treated
  as source context, not as equality evidence.
- P45 phase gating validates the result note, Claude ledger, evidence
  manifest, and command logs.

Primary promotion criterion:

- Registry rows exist for generalized SV native, transformed-residual
  diagnostic, and Gaussian-mixture/moment-matched approximation routes.
- Registry rows exist for spatial SIR additive-Gaussian closure and
  native/non-Gaussian placeholder route.
- Registry rows exist for predator-prey additive-Gaussian RK4 closure and
  native/non-Gaussian placeholder route.
- Every row declares state law, observation law, parameterization,
  transformation/Jacobian terms, reference route, CUT4 route, Zhao--Cui route,
  panel convention, claim class, blocker class, route statuses, and nonclaims.

Veto diagnostics:

- no row may authorize same-target comparison unless reference, CUT4, and
  Zhao--Cui routes are all available;
- transformed generalized-SV residuals must not be represented as exact native
  generalized-SV likelihood;
- SIR and predator-prey additive-Gaussian closures must not be represented as
  native model correctness;
- generalized-SV panels, SIR `J=2,3`, and predator-prey replicated panels must
  be labeled factorized unless a coupled route is separately reviewed.

## Artifacts

- Target registry:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json`
- Focused tests:
  `tests/highdim/test_p45_target_registry.py`
- Phase gate:
  `scripts/p45_phase_gate.py`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase0-target-governance-claude-review-ledger-2026-06-08.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase0-target-governance-evidence-manifest-p45-codex-supervised-20260608-055034.json`

## Local Evidence

| Command | Result |
| --- | --- |
| `python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json` | passed |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_target_registry.py` | 5 passed |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p45_phase_gate.py tests/highdim/test_p45_target_registry.py` | passed |
| `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json tests/highdim/test_p45_target_registry.py scripts/p45_phase_gate.py` | passed |

## Claude Review

Iteration 1 returned `BLOCKED_P45_M0_CODE_GOVERNANCE` because the registry text
contained the required factorized/coupled panel boundaries, but tests enforced
that boundary only for SIR.

Repair:

- Added generalized-SV native, transformed-residual, and approximation panel
  assertions.
- Added predator-prey replicated/factorized panel assertion.

Iteration 2 returned `PASS_P45_M0_CODE_GOVERNANCE`. Claude found no remaining
M0 overclaim or unmet executable-governance condition.

## Gate Markers

p45_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase0-target-governance-evidence-manifest-p45-codex-supervised-20260608-055034.json`
p45_local_evidence_run: `COMPLETE`
p45_evidence_audit: `COMPLETE`
p45_result_note_substance: `COMPLETE`
p45_traceability_or_nonclaim: `COMPLETE`
p45_command_count: `4`
p45_long_run_used: `false`
