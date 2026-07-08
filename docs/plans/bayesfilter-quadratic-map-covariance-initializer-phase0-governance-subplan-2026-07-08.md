# Phase 0 Subplan: Governance And API Boundary

Date: 2026-07-08

## Status

`DRAFT_SUBPLAN`

## Phase Objective

Converge the master program, role boundaries, evidence contract, implementation
surface, and current-code inventory before editing BayesFilter source code for
the quadratic MAP-covariance initializer.

## Entry Conditions Inherited From Previous Phase

This is the entry phase. The repository worktree was checked with
`git status --short` before writing this subplan and was clean at that time.

## Required Artifacts

- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase0-governance-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-visible-gated-execution-runbook-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-visible-execution-ledger-2026-07-08.md`
- `docs/reviews/bayesfilter-quadratic-map-covariance-initializer-phase0-review-bundle-2026-07-08.md`
- Phase 0 close/result record.
- Draft Phase 1 implementation subplan.

## Required Checks, Tests, Reviews

- Local checks:
  - `git status --short`
  - `python -m py_compile bayesfilter/inference/quadratic_geometry.py bayesfilter/inference/mass_matrix.py bayesfilter/inference/__init__.py`
- Read-only review:
  - Claude review gate on the master program, Phase 0 subplan, runbook, and review bundle.
  - If Claude review returns `REVISE`, patch the same planning artifacts visibly and retry, with a maximum of five rounds for the same blocker.
  - If Claude is unavailable, use the review gate fallback or a fresh Codex review only as a clearly labeled weaker review signal.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the plan, runbook, and Phase 0 boundary sufficient to start implementation of a reusable initializer without smuggling unsupported MAP/HMC claims? |
| Baseline/comparator | Current code surfaces: `bayesfilter/inference/quadratic_geometry.py`, `bayesfilter/inference/mass_matrix.py`, current `bayesfilter/inference/__init__.py`, and benchmark-local MAP helpers. |
| Primary pass criterion | Planning artifacts explicitly encode BFGS as locator only, constrained SPD quadratic as covariance authority, sample-budget guard, fail-closed behavior, focused tests, review/repair loop, and nonclaims. |
| Veto diagnostics | Missing stop condition, optimizer curvature treated as covariance authority, unsupported HMC/MAP claim, missing artifact contract, missing review record, or py_compile failure in inventoried source files. |
| Explanatory diagnostics | Current helper names, export locations, test names, and benchmark-local helper references. |
| Not concluded | No implementation correctness, no covariance quality on SSL-LSTM, no global MAP, no HMC readiness, no posterior correctness. |
| Artifact preserving result | Phase 0 result note under `docs/plans`. |

## Forbidden Claims And Actions

- Do not claim a certified MAP, posterior covariance, HMC readiness, sampler
  convergence, default readiness, or Zhao-Cui source faithfulness.
- Do not edit model files, benchmarks, or inference source during Phase 0 except
  for planning/review artifacts.
- Do not use BFGS inverse Hessian as a covariance source.
- Do not launch HMC, GPU benchmarks, package installs, network fetches, commits,
  pushes, or detached supervisors.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- Phase 0 local checks pass;
- Claude review gate returns `AGREE` or a clearly recorded weaker fallback
  agreement that Codex accepts after fresh local review;
- Phase 0 result is written;
- Phase 1 implementation subplan is drafted and reviewed for consistency,
  correctness, feasibility, artifact coverage, and boundary safety.

## Stop Conditions

- Local checks fail and cannot be repaired within Phase 0 scope.
- Review returns `REVISE` for a material blocker that cannot be fixed within five
  rounds.
- Continuing would require package installation, network fetches outside Claude
  review, model-file edits, default-policy changes, HMC runtime, destructive git
  actions, or a human product/scientific boundary decision.

## Skeptical Plan Audit

| Risk | Phase 0 audit |
| --- | --- |
| Wrong baseline | Baseline is current reusable geometry/mass-matrix code and benchmark-local helper pattern, not HMC performance. |
| Proxy metric promoted | Phase 0 promotes only plan readiness; no numeric fit or HMC diagnostic can promote. |
| Missing stop conditions | Stop conditions are explicit above. |
| Unfair comparison | No method ranking occurs. |
| Hidden assumptions | Default/numeric provenance is captured in the master program. |
| Stale context | Source inventory and py_compile are required before Phase 1. |
| Environment mismatch | CPU-safe py_compile only; GPU/HMC excluded. |
| Artifact mismatch | Required artifacts directly answer whether implementation may start. |

Audit status: `PASSED_FOR_REVIEW_GATE`.
