# P04C0 Result: Harness Threshold-Control Repair

Date: 2026-06-26

Status: `P04C0_HARNESS_CONTROL_PASS_TO_P04C_PREFLIGHT`

## Phase Objective

Repair the local range-bearing benchmark harness so P04C scale extraction can
record paired normalized log-likelihood deltas without letting the historical
uncalibrated `0.05` threshold act as a hard P04C pass/fail gate.

This is a harness-control repair only. It is not P04C scale extraction, not a
threshold freeze, and not a nonlinear validation result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the benchmark explicitly separate paired-delta recording from paired-delta hard vetoing? |
| Baseline/comparator | Previous harness behavior, where the historical `0.05` paired threshold was always a hard veto. |
| Primary criterion | Default `gate` behavior remains backward-compatible, while explicit `--paired-threshold-mode record-only` suppresses only the paired-delta veto and records threshold-role metadata. |
| Veto diagnostics | Parser cannot express record-only mode, gate mode no longer emits paired veto, record-only mode still emits paired veto, missing threshold-role metadata, focused tests fail, or unsupported scientific/promotion claim. |
| Explanatory diagnostics | Tiny CPU-hidden smoke metadata, direct paired-veto unit checks, py_compile. |
| Not concluded | No calibrated nonlinear threshold, no P04C scale evidence, no P04D freeze authorization, no P05 eligibility, no default promotion, no posterior correctness, no HMC readiness, and no statistical superiority. |
| Artifact | This result plus the updated harness, focused test, P04C command shape, runbook/ledger/handoff updates. |

## Implementation Summary

- Added `--paired-threshold-mode {gate,record-only}` to
  `docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py`.
- Added `--paired-delta-threshold`, defaulting to the historical `0.05`, so
  the old threshold is explicit metadata rather than an implicit constant.
- Preserved default `gate` behavior: paired normalized-delta exceedance remains
  a hard veto unless record-only mode is requested.
- Added record-only behavior: paired deltas and threshold role are recorded,
  but `paired:paired_normalized_log_likelihood_delta` is not added to hard
  vetoes.
- Updated P04C command shape to include
  `--paired-threshold-mode record-only`.

## Required Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Focused range-bearing harness tests | PASS | `pytest -q tests/test_svd_nystrom_range_bearing_gate.py`: `6 passed` in `15.83s` |
| Syntax check | PASS | `python -m py_compile docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py tests/test_svd_nystrom_range_bearing_gate.py` |
| Default gate mode retained | PASS | Focused unit test confirms paired normalized-delta exceedance emits `paired_normalized_log_likelihood_delta` in `gate` mode. |
| Record-only mode suppresses paired hard veto | PASS | Focused unit test confirms paired normalized-delta exceedance emits no paired veto in `record-only` mode. |
| Metadata role recorded | PASS | Tiny smoke test checks `paired_threshold_mode=gate` and `normalized_abs_log_likelihood_delta_role=hard_veto`; harness records `record_only_descriptive_not_calibrated` in record-only mode. |
| P04C command shape repaired | PASS | P04C subplan now includes `--paired-threshold-mode record-only`. |

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P04C0_HARNESS_CONTROL_PASS_TO_P04C_PREFLIGHT` |
| Primary criterion status | PASS: the harness can now run P04C in record-only paired-threshold mode while preserving legacy/default hard-gate behavior. |
| Veto diagnostic status | PASS: no focused test failure, no syntax failure, no source-code disclosure to Claude, and no unsupported threshold/default/scientific claim. |
| Main uncertainty | GPU P04C rows have not been run yet; this repair only makes the row command valid for scale extraction. |
| Next justified action | Run P04C trusted GPU preflight, use GPU1 if suitable otherwise GPU0, then run calibration seeds `84100..84111` one at a time in record-only mode. |
| What is not concluded | No calibrated nonlinear threshold, no P04C pass/fail, no P04D threshold freeze, no P05 eligibility, no default promotion, no posterior correctness, no HMC readiness, and no statistical superiority. |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | PASS for the mechanical harness-control repair only |
| Statistically supported ranking | NO |
| Descriptive-only differences | None from this repair; focused tests are engineering checks |
| Default-readiness | NO |
| Next evidence needed | P04C GPU/TF32 scale-extraction rows and aggregate summary |

## Review Boundary

This repair was locally reviewed and tested. Claude was not asked to review
source code or tests because the standing Claude approval for this lane forbids
source-code disclosure. The updated P04C subplan remains eligible for
exact-path read-only document review if needed before P04D threshold freeze.

## Handoff

`P04C0_HARNESS_CONTROL_PASS_TO_P04C_PREFLIGHT`

P04C may proceed to trusted GPU preflight. P04C must still use record-only
paired-threshold mode and must not launch P05, freeze a threshold, validate the
candidate, or make promotion/default/scientific/HMC claims.
