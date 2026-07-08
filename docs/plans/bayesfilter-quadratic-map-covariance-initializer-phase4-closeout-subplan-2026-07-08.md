# Phase 4 Subplan: Closeout And Handoff

Date: 2026-07-08

## Status

`DRAFT_SUBPLAN`

## Phase Objective

Close the quadratic MAP-covariance initializer runbook by running final focused
checks, recording the implemented artifacts, and stating residual gaps before
any HMC-readiness or posterior-correctness claim.

## Entry Conditions Inherited From Previous Phase

- Phase 3 status: `PASSED_BOUNDED_BENCHMARK_SMOKE`.
- Benchmark-facing oracle smoke passed with `12 passed`.
- No HMC/GPU/long benchmark/default-policy boundary was crossed.

## Required Artifacts

- Final closeout result:
  - `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase4-closeout-result-2026-07-08.md`
- Updated visible execution ledger.
- Final worktree summary.

## Required Checks, Tests, Reviews

- Local checks:
  - `pytest tests/test_quadratic_map_covariance.py tests/test_identifiable_ssl_lstm_oracle_geometry.py tests/test_v1_public_api.py -q`
  - `python -m py_compile bayesfilter/inference/quadratic_map_covariance.py bayesfilter/inference/__init__.py bayesfilter/__init__.py`
  - `git diff --check`
  - `git status --short`
- Review:
  - Codex closeout self-review for unsupported claims, missing artifacts, and
    dirty-worktree awareness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the runbook complete for the reusable initializer implementation and bounded validation? |
| Baseline/comparator | Phase 1-3 result records and final focused checks. |
| Primary pass criterion | Final focused checks pass, artifacts are present, and closeout states exact residual gaps before HMC. |
| Veto diagnostics | Failing focused checks, missing result artifacts, unsupported HMC/MAP/posterior/default claim, or unreported dirty worktree changes. |
| Explanatory diagnostics | Test counts, warning classes, changed files, residual gaps. |
| Not concluded | No global MAP, posterior covariance correctness, HMC readiness, sampler convergence, statistical superiority, default readiness, or Zhao-Cui source faithfulness. |
| Artifact preserving result | Phase 4 closeout result and ledger. |

## Forbidden Claims And Actions

- Do not claim HMC readiness, posterior correctness, global MAP, default
  readiness, sampler convergence, or Zhao-Cui source faithfulness.
- Do not commit, push, launch HMC/GPU/long runs, install packages, or alter
  default policy.

## Exact Final Handoff Conditions

The runbook may close when:

- final checks pass or any failure is recorded with a blocker;
- closeout result is written;
- user-facing final answer reports implemented files, checks, and residual gaps.

## Stop Conditions

- Final focused checks fail and cannot be repaired within scope.
- Worktree contains unexpected unrelated changes that block safe summary.
- Closing would require a claim or boundary not supported by the artifacts.

## Skeptical Plan Audit

| Risk | Phase 4 audit |
| --- | --- |
| Wrong baseline | Baseline is the completed runbook evidence, not HMC output. |
| Proxy metric promoted | Tests support implementation/smoke behavior only. |
| Missing stop conditions | Stop conditions are explicit above. |
| Unfair comparison | No method ranking occurs. |
| Hidden assumptions | Residual gaps must state what remains unproved. |
| Stale context | Final worktree/status checks are required. |
| Environment mismatch | CPU-safe tests only; no GPU/HMC evidence. |
| Artifact mismatch | Closeout result directly records what was implemented and not concluded. |

Audit status: `PASSED_FOR_CLOSEOUT`.
