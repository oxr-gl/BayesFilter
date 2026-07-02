# Phase 2 Subplan: Structural Admission Contract

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Define what a generic nonlinear SSM must expose to be eligible for the generic
likelihood / analytical-gradient lanes, and classify routes as exact eligible,
approximate eligible, or ineligible with explicit reasons.

## Entry Conditions Inherited From Previous Phase

- Phase 1 has reviewed and frozen the target-and-authority contract.
- Structural target semantics, route taxonomy, and API-scope boundaries are
  fixed.
- No implementation or runtime admission is authorized yet.

## Required Artifacts

- structural-admission result:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase2-structural-admission-result-2026-07-01.md`
- refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase3-value-lane-architecture-subplan-2026-07-01.md`
- structural and adapter anchors:
  - `bayesfilter/structural.py`
  - `bayesfilter/structural_tf.py`
  - `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`
  - `bayesfilter/highdim/models.py`
- posterior/score authority anchors:
  - `bayesfilter/inference/posterior_adapter.py`
  - `bayesfilter/highdim/score_api.py`
- visible execution ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-execution-ledger-2026-07-01.md`
- Claude review ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-claude-review-ledger-2026-07-01.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f bayesfilter/structural.py
test -f bayesfilter/structural_tf.py
test -f bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py
test -f bayesfilter/highdim/models.py
test -f bayesfilter/inference/posterior_adapter.py
test -f bayesfilter/highdim/score_api.py
rg -n "StatePartition|StructuralFilterConfig|TFStructuralStateSpace|tf_structural_to_fixed_sgqf_model|NonlinearSSMAdapterContract|ValueScoreCapability|TARGET|same_scalar|xla_hmc_ready" bayesfilter/structural.py bayesfilter/structural_tf.py bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py bayesfilter/inference/posterior_adapter.py bayesfilter/highdim/models.py bayesfilter/highdim/score_api.py
git diff --check -- docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient*.md
```

Required read-only Claude reviews:

- Phase 2 result,
- refreshed Phase 3 subplan.

No implementation, runtime, benchmark, score, derivative, HMC, GPU/CUDA,
package/network, release, CI, production, or default-policy command is
authorized in Phase 2.

## Skeptical Plan Audit

| Risk Checked | Phase 2 Control |
| --- | --- |
| Wrong baseline | Admission criteria are anchored to the structural and posterior contracts already present in the codebase. |
| Proxy metric promoted | A model being runnable is not the same as being exact eligible, same-scalar eligible, or HMC/API-ready. |
| Missing stop condition | Ineligible models and fixture-specific adapters must be classified explicitly rather than left implied. |
| Unfair comparison | Exact-eligible, approximate-eligible, and ineligible routes are separate statuses, not a continuum hidden inside implementation details. |
| Hidden assumption | Phase 2 does not assume the current structural adapter is generic; it must state exact eligibility limits. |
| Stale context | Admission semantics are derived from current code seams, not project memory alone. |
| Environment mismatch | Phase 2 is code/document inspection only. |
| Artifact-answer mismatch | Phase 2 must close with an explicit admission matrix and refreshed Phase 3 subplan. |

Audit status: passed if structural admission is explicit and fail-closed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What must a nonlinear SSM expose to be admitted into the generic likelihood / gradient lanes, and which currently known routes are exact eligible, approximate eligible, or ineligible? |
| Baseline/comparator | Phase 1 contract and current structural/posterior/highdim code seams. |
| Primary criterion | Phase 2 writes a reviewed structural-admission artifact that names exact eligibility, approximate eligibility, ineligibility, and required metadata/semantics without authorizing implementation or promotion. |
| Veto diagnostics | fixture-specific adapters mislabeled as generic support, missing ineligibility reasons, silent HMC/API overpromotion, or structural contracts that fail to distinguish exact from approximate eligibility. |
| Explanatory diagnostics | code-anchor inventory, metadata contract notes, and review observations. |
| Not concluded | No value-path implementation, no derivative implementation, no HMC readiness, and no top-level/production promotion. |
| Artifact | reviewed structural-admission result and refreshed Phase 3 subplan. |

## Forbidden Claims/Actions

- Do not treat the current structural adapter as already generic unless the
  reviewed artifact explicitly says so.
- Do not promote a structurally ineligible model as generic support.
- Do not authorize implementation, runtime, benchmark, derivative, HMC,
  package/network, release, CI, production, or default-policy work.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if:

- the Phase 2 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 3 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records reviewed exact-eligible, approximate-eligible,
  and ineligible structural categories.

## Stop Conditions

- The structural-admission result cannot classify current seams honestly without
  rewriting target/authority contracts.
- A route would need silent fallback or hidden model-specific semantics to be
  labeled generic.
- Local document/source checks fail and cannot be repaired within document
  scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require implementation, runtime, benchmark, evaluator,
  GPU/HMC, package/network, release, CI, default-policy, destructive
  git/filesystem, or unrelated dirty worktree changes.

## End-Of-Phase Requirements

1. Run the required code/document inspection checks.
2. Write the structural-admission result.
3. Refresh the Phase 3 subplan.
4. Review the Phase 2 result and refreshed Phase 3 subplan.
5. Update the execution ledger and Claude review ledger.
