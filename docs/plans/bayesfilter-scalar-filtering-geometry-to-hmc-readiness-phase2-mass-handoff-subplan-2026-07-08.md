# Phase 2 Subplan: Geometry-To-Mass Handoff

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Phase 1 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-result-2026-07-08.md`

## Phase Objective

Convert the accepted Phase 1 scalar filtering-likelihood geometry into an explicit HMC mass-matrix handoff artifact in the correct whitened coordinate system, with SPD regularization and coordinate-audit diagnostics.

This phase does not run HMC. It prepares and validates a mass candidate for the later mechanics canary.

## Entry Conditions Inherited From Phase 1

- Parent Phase 1 artifact exists: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json`.
- Phase 1 decision reports `geometry_sanity_passed: true` and no vetoes.
- Accepted precision is in whitened coordinates under `theta = center + scale * z`.
- Center role is `truth_free_initial_center`, not MAP.
- Center refinement was rejected outside the trust radius; do not use the refined point as a mass center.
- CPU-hidden non-XLA compiled wrapper was a debug/runtime repair, not production/GPU/XLA evidence.

## Required Artifacts

- Phase 2 subplan: this file.
- Phase 2 review bundle: `docs/reviews/scalar-filtering-geometry-hmc-phase2-mass-handoff-review-bundle-2026-07-08.md`
- Mass handoff script: `docs/benchmarks/prepare_scalar_ssl_lstm_filtering_mass_handoff_2026_07_08.py`
- Focused tests: `tests/test_scalar_ssl_lstm_filtering_mass_handoff.py`
- JSON artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json`
- Markdown artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.md`
- Phase 2 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-result-2026-07-08.md`
- Phase 3 subplan draft if Phase 2 passes: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-subplan-2026-07-08.md`

## Required Checks, Tests, Reviews

- Local Codex substitute review of this Phase 2 subplan because Claude review is policy-blocked for private repository context transfer.
- `python -m py_compile docs/benchmarks/prepare_scalar_ssl_lstm_filtering_mass_handoff_2026_07_08.py`
- `pytest tests/test_scalar_ssl_lstm_filtering_mass_handoff.py -q`
- CPU-hidden handoff command:

```bash
env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/prepare_scalar_ssl_lstm_filtering_mass_handoff_2026_07_08.py \
  --geometry-json docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json \
  --json-path docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json \
  --markdown-path docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.md
```

- `git diff --check`
- Review the Phase 2 result and Phase 3 subplan before any HMC mechanics canary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the accepted Phase 1 whitened precision/covariance be converted into a regularized SPD mass handoff artifact without coordinate mismatch or MAP claims? |
| Baseline/comparator | Phase 1 accepted low-rank geometry artifact. No sampler comparison is made. |
| Primary criterion | Artifact records center, scale, whitened precision, whitened covariance/mass candidate, SPD eigen summaries, condition number, regularization policy, coordinate convention, and no vetoes. |
| Veto diagnostics | Missing Phase 1 artifact, Phase 1 did not pass, coordinate convention mismatch, non-SPD precision/covariance/mass, over-condition matrix after regularization, use of rejected refined center as MAP, unsupported HMC/posterior/default claim. |
| Explanatory diagnostics | Eigenvalues, condition numbers, jitter/floor amount, center score norm, refinement rejection reason. |
| Not concluded | No HMC readiness, HMC convergence, posterior correctness, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness. |
| Preserving artifact | Phase 2 JSON/Markdown/result note and ledger entry. |

## Planned Handoff Design

- Treat Phase 1 precision as `K_z`, a precision matrix in whitened coordinates `z`.
- Treat the covariance/mass candidate as `M_z = inv(K_z)` after symmetry and SPD validation.
- Apply only explicit eigenvalue-floor regularization if needed, with before/after eigen summaries.
- Preserve the original-parameter mapping separately: `theta = center + scale * z`.
- Do not convert to original-coordinate mass in this phase unless the artifact labels it as explanatory and not the HMC handoff.
- Do not use the rejected refined center.

## Forbidden Claims And Actions

- Do not run HMC.
- Do not claim the mass is optimal, tuned, MAP-based, or posterior-correct.
- Do not claim default readiness, GPU/XLA readiness, convergence, sampler superiority, or Zhao-Cui source-faithfulness.
- Do not change the Phase 1 geometry artifact or pass/fail criteria.
- Do not install packages, fetch network resources, edit model files, or perform destructive git/filesystem actions.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- Phase 2 subplan review has no unresolved material blocker.
- Required checks pass.
- Phase 2 artifact records no vetoes.
- Whitened mass candidate is finite SPD and condition-bounded.
- Coordinate convention is explicit and matches Phase 1.
- Phase 2 result preserves non-claims.
- Phase 3 mechanics-canary subplan is drafted and reviewed.

If any veto fires, write a Phase 2 blocker/repair result and stop before HMC mechanics.

## Stop Conditions

- Phase 2 subplan review returns unresolved `REVISE`.
- Phase 1 artifact is missing, invalid, or not passing.
- Mass/precision/covariance is nonfinite, non-SPD, or coordinate-mismatched.
- Required tests fail and cannot be repaired within Phase 2 scope.
- Continuing would require HMC execution, package installation, network fetch, credentials, default-policy change, model-file edit, destructive git/filesystem action, or unsupported scientific/runtime claim.

## Skeptical Audit

- Wrong baseline: Phase 2 uses Phase 1 accepted geometry only, not posterior or sampler evidence.
- Proxy metric risk: SPD/condition passing is a mass-handoff gate, not HMC validation.
- Missing stop conditions: non-SPD, coordinate mismatch, missing Phase 1 pass, or MAP claim stops before HMC.
- Unfair comparison: no sampler or mass strategy ranking is attempted.
- Hidden assumptions: whitened mass may not be appropriate for actual HMC dynamics until Phase 3 canary tests it.
- Stale context: Phase 1 center refinement failed, so center and MAP language are guarded.
- Environment mismatch: CPU-hidden handoff artifact is not GPU/XLA evidence.
- Artifact adequacy: JSON/Markdown mass handoff answers coordinate and SPD validity only.

Audit result: `PASS_WITH_BOUNDARIES_PENDING_REVIEW`. Execute only after Phase 2 subplan review.
