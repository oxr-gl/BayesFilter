# Phase 3 Subplan: Generic Value-Lane Architecture

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the reusable generic value-path split between the structural
Gaussian-projection SGQF lane and the direct-likelihood / pointwise
reweighting lane, and state which declared scalar each lane computes.

## Entry Conditions Inherited From Previous Phase

- Phase 2 has reviewed structural admission categories.
- The target-and-authority contract and route taxonomy are frozen.
- No derivative admission is authorized yet.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase3-value-lane-architecture-result-2026-07-01.md`
- refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase4-derivative-contract-subplan-2026-07-01.md`
- value-path anchors:
  - `bayesfilter/nonlinear/fixed_sgqf_tf.py`
  - `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`
  - `bayesfilter/highdim/filtering.py`
  - `bayesfilter/highdim/models.py`
  - `bayesfilter/structural_tf.py`
- visible execution ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-execution-ledger-2026-07-01.md`
- Claude review ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-claude-review-ledger-2026-07-01.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f bayesfilter/nonlinear/fixed_sgqf_tf.py
test -f bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py
test -f bayesfilter/highdim/filtering.py
test -f bayesfilter/highdim/models.py
test -f bayesfilter/structural_tf.py
rg -n "TFFixedSGQFNonlinearModel|TFFixedSGQFNonGaussianModel|tf_fixed_sgqf_filter|observation_log_density|Gaussian|same-scalar|fixed branch|transition_log_density|observation_log_density" bayesfilter/nonlinear/fixed_sgqf_tf.py bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py bayesfilter/structural_tf.py
git diff --check -- docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient*.md
```

Required read-only Claude reviews:

- Phase 3 result,
- refreshed Phase 4 subplan.

No implementation, runtime, benchmark, derivative, HMC, GPU/CUDA,
package/network, release, CI, production, or default-policy command is
authorized in Phase 3.

## Skeptical Plan Audit

| Risk Checked | Phase 3 Control |
| --- | --- |
| Wrong baseline | Lane classification is anchored to actual value-path code and chapter-defined scalar distinctions. |
| Proxy metric promoted | A reusable interface declaration does not imply exact-target or derivative admission. |
| Missing stop condition | If a lane cannot state what scalar it computes, it must be blocked or labeled diagnostic-only. |
| Unfair comparison | Structural Gaussian-projection and direct-likelihood reweighting lanes are separate architectural families. |
| Hidden assumption | Phase 3 does not assume the declared non-Gaussian interface is already fully wired through the SGQF runtime. |
| Stale context | Lane semantics are derived from current code and chapter contracts, not memory. |
| Environment mismatch | Phase 3 is code/document inspection only. |
| Artifact-answer mismatch | Phase 3 must close with an explicit lane architecture result and refreshed Phase 4 subplan. |

Audit status: passed if each lane's declared scalar and authority boundary are
stated explicitly.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What reusable generic value-path lanes exist or should exist, and what declared scalar does each lane compute? |
| Baseline/comparator | Phase 2 structural-admission result, chapter-defined value-path contracts, and current SGQF/highdim value-path code. |
| Primary criterion | Phase 3 writes a reviewed lane-architecture artifact that distinguishes structural Gaussian-projection and direct-likelihood reweighting lanes, states what scalar each computes, and records any still-unwired generic seam as blocked or diagnostic-only. |
| Veto diagnostics | claiming two lanes compute the same scalar when they do not, silent surrogate promotion, or hiding an unwired generic seam behind a model-specific route. |
| Explanatory diagnostics | code-anchor inventory, chapter-language mapping, and review notes. |
| Not concluded | No derivative admission, no HMC readiness, and no top-level/production promotion. |
| Artifact | reviewed Phase 3 lane-architecture result and refreshed Phase 4 subplan. |

## Forbidden Claims/Actions

- Do not claim the current SGQF runtime already gives generic direct-likelihood
  support unless the reviewed artifact shows the code path explicitly.
- Do not merge Gaussian-projection and direct-likelihood lanes into one
  overgeneralized “generic likelihood” label.
- Do not authorize implementation, runtime, benchmark, derivative, HMC,
  package/network, release, CI, production, or default-policy work.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if:

- the Phase 3 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 4 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records the reviewed generic value-lane taxonomy and any
  blocked/unwired seams explicitly.

## Stop Conditions

- The current code cannot state the scalar/target relation of a lane honestly.
- A lane would need silent semantic drift to look generic.
- Local code/document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require implementation, runtime, benchmark, evaluator,
  GPU/HMC, package/network, release, CI, default-policy, destructive
  git/filesystem, or unrelated dirty worktree changes.

## End-Of-Phase Requirements

1. Run the required code/document inspection checks.
2. Write the Phase 3 lane-architecture result.
3. Refresh the Phase 4 subplan.
4. Review the Phase 3 result and refreshed Phase 4 subplan.
5. Update the execution ledger and Claude review ledger.
