# Phase 1 Subplan: Reusable Initializer Implementation

Date: 2026-07-08

## Status

`DRAFT_SUBPLAN`

## Phase Objective

Add a reusable BayesFilter inference API that uses a local optimizer only as a
finite neighborhood locator, fits constrained SPD quadratic geometry around the
locator, and returns an explicitly diagnostic MAP-candidate/covariance result
whose accepted covariance is produced through `covariance_from_precision`.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result status: `PASSED_WITH_CODEX_FALLBACK_REVIEW`.
- Claude external review was blocked by managed approval policy; fresh Codex
  read-only fallback review returned `VERDICT: AGREE`.
- Binding residual risk from review: do not rely on direct inversion inside
  `fit_low_rank_spd_quadratic_geometry` for the new initializer covariance
  provenance; route accepted precision through `covariance_from_precision`.

## Required Artifacts

- New or modified source implementing the initializer, expected write set:
  - `bayesfilter/inference/quadratic_map_covariance.py`
  - `bayesfilter/inference/__init__.py`
  - `bayesfilter/__init__.py` only if consistent with current lazy public API.
- Tests drafted or updated, expected write set:
  - `tests/test_quadratic_map_covariance.py`
  - `tests/test_v1_public_api.py` only if a public API assertion is needed.
- Phase 1 result record.
- Draft Phase 2 validation subplan.

## Required Checks, Tests, Reviews

- Local checks:
  - `python -m py_compile bayesfilter/inference/quadratic_map_covariance.py bayesfilter/inference/__init__.py bayesfilter/__init__.py`
  - Focused import smoke for the new symbols.
  - `git diff --check`
- Review:
  - Codex self-review of the implementation diff against the evidence contract.
  - Claude review is not retried in Phase 1 unless the user explicitly approves
    external transfer after the prior rejection risk; if not available, use
    fresh Codex review only for material boundary concerns.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the source diff provide a reusable initializer API with the correct authority split and fail-closed result structure? |
| Baseline/comparator | Existing `fit_low_rank_spd_quadratic_geometry`, `covariance_from_precision`, benchmark-local `estimate_map_center`/`map_candidate_negative_hessian` patterns. |
| Primary pass criterion | Source compiles and exposes a result/config API where optimizer output is a locator only, accepted covariance comes from `covariance_from_precision`, rejected cases are explicit, and nonclaims are preserved. |
| Veto diagnostics | BFGS inverse Hessian used as covariance, accepted nonfinite covariance, accepted non-SPD precision, missing nonclaims, missing fallback path, direct-HMC launch, broad benchmark refactor, or source compile failure. |
| Explanatory diagnostics | Locator status, center/source role, geometry status, mass-matrix regularization report, eigen summaries, trust-region refinement status. |
| Not concluded | No implementation correctness beyond compile/import until Phase 2 tests; no global MAP, posterior covariance correctness, HMC readiness, convergence, default readiness, or Zhao-Cui source faithfulness. |
| Artifact preserving result | Phase 1 result note plus source diff. |

## Implementation Requirements

- Define explicit nonclaims, for example:
  - diagnostic initializer only;
  - not a certified global MAP;
  - not posterior covariance correctness evidence;
  - not HMC convergence/readiness evidence;
  - not default-readiness evidence;
  - not source-faithful Zhao-Cui evidence.
- Provide a locator config for `tfp.optimizer.lbfgs_minimize` with finite
  fallback to the initial position when the optimizer fails or degrades the
  log-probability.
- Use TensorFlow/TFP for target value/score and optimizer interactions.
- Reuse `fit_low_rank_spd_quadratic_geometry` for constrained SPD precision.
- Convert accepted precision to covariance with `covariance_from_precision`.
- Preserve geometry diagnostics separately from mass-matrix diagnostics.
- Label the mode as `quadratic_surrogate_map_candidate` or
  `locator_position` rather than certified MAP.
- Keep benchmark adoption out of Phase 1 except for import references.

## Forbidden Claims And Actions

- Do not claim certified/global MAP, posterior covariance correctness, HMC
  readiness, sampler convergence, default readiness, or Zhao-Cui source
  faithfulness.
- Do not launch HMC, GPU runs, long benchmarks, package installs, commits,
  pushes, or detached supervisors.
- Do not change pass/fail criteria after seeing test results.
- Do not edit unrelated user changes.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 source compile/import checks pass or failures are recorded with a
  focused repair plan;
- Phase 1 result record is written;
- Phase 2 validation subplan is drafted with exact pytest commands and expected
  pass/fail criteria;
- no veto diagnostic remains unresolved.

## Stop Conditions

- Source compile/import failure that cannot be fixed within the intended write
  set.
- Discovery that `fit_low_rank_spd_quadratic_geometry` cannot support the
  required authority split without a larger redesign.
- Need to alter default public API policy, launch HMC/GPU, install packages, or
  use external Claude review despite approval rejection.

## Skeptical Plan Audit

| Risk | Phase 1 audit |
| --- | --- |
| Wrong baseline | Baseline is current reusable geometry and mass-matrix helpers, not HMC performance. |
| Proxy metric promoted | Compile/import only gates source readiness; correctness is deferred to Phase 2 tests. |
| Missing stop conditions | Stop conditions are explicit above. |
| Unfair comparison | No method ranking occurs. |
| Hidden assumptions | Locator numeric defaults are implementation defaults only and must be reported in payload/config. |
| Stale context | Phase 0 inventory inspected current files; Phase 1 will re-read touched files before editing. |
| Environment mismatch | CPU-safe compile/import only; no GPU/HMC evidence. |
| Artifact mismatch | Source diff and result record directly answer the implementation-surface question. |

Audit status: `PASSED_FOR_PHASE_1_IMPLEMENTATION`.
