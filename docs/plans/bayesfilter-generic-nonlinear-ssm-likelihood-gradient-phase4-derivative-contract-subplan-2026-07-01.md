# Phase 4 Subplan: Generic Analytical-Derivative Contract

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the generic analytical-derivative contract for the admitted lanes,
including same-branch signature rules, parameter-derivative backend taxonomy,
and the distinction between current-score objects and propagation-only objects.

## Entry Conditions Inherited From Previous Phase

- Phase 3 has reviewed the generic value-lane architecture.
- The target-and-authority contract and structural-admission categories are
  frozen.
- No derivative admission is authorized yet.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase4-derivative-contract-result-2026-07-01.md`
- refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-subplan-2026-07-01.md`
- derivative anchors:
  - `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
  - `bayesfilter/highdim/derivatives.py`
  - `bayesfilter/highdim/filtering.py`
  - `bayesfilter/highdim/models.py`
- visible execution ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-execution-ledger-2026-07-01.md`
- Claude review ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-claude-review-ledger-2026-07-01.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py
test -f bayesfilter/highdim/derivatives.py
test -f bayesfilter/highdim/filtering.py
test -f bayesfilter/highdim/models.py
rg -n "same_branch|same_scalar|derivative_method|branch_identity|d_transition_fn|d_observation_fn|parameter_score|GradientTape|replay" bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py bayesfilter/highdim/derivatives.py bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py
git diff --check -- docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient*.md
```

Required read-only Claude reviews:

- Phase 4 result,
- refreshed Phase 5 subplan.

No implementation, runtime, benchmark, HMC, GPU/CUDA, package/network,
release, CI, production, or default-policy command is authorized in Phase 4.

## Skeptical Plan Audit

| Risk Checked | Phase 4 Control |
| --- | --- |
| Wrong baseline | The derivative contract is anchored to the chapter-defined same-scalar and branch-validity obligations. |
| Proxy metric promoted | Reverse-mode availability or FD agreement alone is not analytical-gradient admission. |
| Missing stop condition | Any lane lacking branch-valid derivative obligations must remain blocked or fallback-only. |
| Unfair comparison | Current-score objects and propagation-only objects are separated so implementation does not overclaim what each derivative closes. |
| Hidden assumption | Phase 4 does not assume autodiff fallback and model-provided scores have the same authority. |
| Stale context | Derivative semantics are derived from current derivative code and chapter contracts. |
| Environment mismatch | Phase 4 is code/document inspection only. |
| Artifact-answer mismatch | Phase 4 must close with an explicit derivative contract result and refreshed Phase 5 subplan. |

Audit status: passed if derivative obligations are explicit and fail-closed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What analytical-derivative obligations must a generic nonlinear-SSM lane satisfy before value/score admission is allowed? |
| Baseline/comparator | Phase 3 lane architecture, chapter-defined branch-valid derivative contracts, and current derivative code seams. |
| Primary criterion | Phase 4 writes a reviewed derivative-contract artifact that fixes same-branch signature rules, backend taxonomy, and analytical-gradient admission boundaries without authorizing implementation or promotion. |
| Veto diagnostics | same-branch mismatch omitted, autodiff fallback silently treated as analytical admission, or score/path objects blurred so the derivative contract does not match the declared scalar. |
| Explanatory diagnostics | derivative-anchor inventory, backend taxonomy notes, and review observations. |
| Not concluded | No implementation pass, no gradient pass, no HMC readiness, and no top-level/production promotion. |
| Artifact | reviewed derivative-contract result and refreshed Phase 5 subplan. |

## Forbidden Claims/Actions

- Do not treat autodiff fallback as analytical-gradient admission by default.
- Do not claim derivative readiness before the value gate passes.
- Do not authorize implementation, runtime, benchmark, HMC, GPU/CUDA,
  package/network, release, CI, production, or default-policy work.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if:

- the Phase 4 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 5 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records same-branch derivative obligations and backend
  taxonomy explicitly.

## Stop Conditions

- The derivative contract cannot distinguish analytical, fallback, and blocked
  routes honestly.
- A same-scalar derivative claim would require silent branch drift.
- Local code/document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require implementation, runtime, benchmark, evaluator,
  GPU/HMC, package/network, release, CI, default-policy, destructive
  git/filesystem, or unrelated dirty worktree changes.

## End-Of-Phase Requirements

1. Run the required code/document inspection checks.
2. Write the Phase 4 derivative-contract result.
3. Refresh the Phase 5 subplan.
4. Review the Phase 4 result and refreshed Phase 5 subplan.
5. Update the execution ledger and Claude review ledger.
