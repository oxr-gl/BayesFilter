# Phase 1 Subplan: Target-And-Authority Contract Freeze

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the exact-target / declared approximate-scalar / same-scalar derivative
contract, the route taxonomy, and the API-scope authority boundaries so later
phases cannot drift into validating or promoting the wrong scalar.

## Entry Conditions Inherited From Previous Phase

- Phase 0 launch package is reviewed closed.
- The master program, runbook, and launch ledgers are the active authority
  package.
- Chapter anchors from ch33/ch34/ch35b/ch37/ch38 remain the governing upstream
  scientific basis.
- No implementation, value, gradient, HMC, or top-level API promotion is
  authorized yet.

## Required Artifacts

- target-and-authority contract:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-target-authority-contract-2026-07-01.md`
- Phase 1 result:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase1-target-authority-contract-result-2026-07-01.md`
- refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase2-structural-admission-subplan-2026-07-01.md`
- visible execution ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-execution-ledger-2026-07-01.md`
- Claude review ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-claude-review-ledger-2026-07-01.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-target-authority-contract-2026-07-01.md
test -f docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex
test -f docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex
test -f docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex
test -f docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex
test -f docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex
rg -n "Exact target|Declared approximate scalar|same-scalar|Gaussian-closure|Tests passed on the wrong scalar|subpackage|HMC readiness" docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-target-authority-contract-2026-07-01.md docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex
git diff --check -- docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient*.md
```

Required read-only Claude reviews:

- target-and-authority contract,
- Phase 1 result,
- refreshed Phase 2 subplan.

No implementation, runtime, benchmark, score, derivative, HMC, GPU/CUDA,
package/network, release, CI, production, or default-policy command is
authorized in Phase 1.

## Skeptical Plan Audit

| Risk Checked | Phase 1 Control |
| --- | --- |
| Wrong baseline | The contract is anchored directly to the chapter-defined exact-target and fixed-branch semantics. |
| Proxy metric promoted | The contract freezes value-before-gradient and exact-target versus surrogate distinctions before any runtime evidence exists. |
| Missing stop condition | The contract preserves explicit vetoes for wrong-target Gaussian closure, same-branch mismatch, missing structural-admission contract, and API-scope drift. |
| Unfair comparison | The route taxonomy keeps exact-target, Gaussian-projection, fixed-cloud, direct-likelihood, diagnostic-only, and blocked lanes separate. |
| Hidden assumption | Phase 1 does not assume that a structural route or SGQF route is already generic or exact-target. |
| Stale context | The contract is derived from reviewed chapter anchors, not from implementation convenience. |
| Environment mismatch | Phase 1 is document-only. No runtime evidence is created. |
| Artifact-answer mismatch | Phase 1 must close with a reviewed contract result and refreshed Phase 2 subplan; a contract file alone is insufficient. |

Audit status: passed if the contract remains explicit about the three-layer
object separation and prevents later user-choice drift.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 1 freeze an unambiguous target-and-authority contract so later phases cannot drift to the wrong scalar, wrong lane taxonomy, or wrong API scope? |
| Baseline/comparator | Phase 0 reviewed launch package and chapter anchors from ch33/ch34/ch35b/ch37/ch38. |
| Primary criterion | The contract and Phase 1 result preserve exact-target semantics, declared approximate-scalar semantics, same-scalar derivative semantics, route taxonomy, and scoped API authority without authorizing implementation or promotion. |
| Veto diagnostics | wrong-target Gaussian closure promoted as same-target evidence, same-scalar derivative contract omitted, route taxonomy ambiguity, or silent HMC/top-level/production overpromotion. |
| Explanatory diagnostics | chapter-anchor coverage, contract vocabulary, and review notes. |
| Not concluded | No structural admission, no generic value implementation, no generic analytical-gradient implementation, no HMC readiness, and no top-level/production promotion. |
| Artifact | reviewed contract closeout, Phase 1 result, refreshed Phase 2 subplan. |

## Forbidden Claims/Actions

- Do not claim any lane is implemented or admitted.
- Do not ask the user to choose mathematical conventions already fixed by the
  reviewed contract.
- Do not treat a convenience approximation as same-target evidence by default.
- Do not authorize runtime, benchmark, score, derivative, HMC, GPU/CUDA,
  package/network, release, CI, production, or default-policy work.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if:

- the target-and-authority contract receives Claude `VERDICT: AGREE`;
- the Phase 1 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 2 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records Phase 1 as reviewed closed with preserved route
  taxonomy and scoped API authority.

## Stop Conditions

- The contract conflicts with the chapter-defined exact-target or fixed-branch
  semantics.
- The contract blurs exact-target and surrogate-target status.
- The contract silently overpromotes subpackage support into HMC/top-level/
  production authority.
- Local document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require runtime, benchmark, evaluator, GPU/HMC,
  package/network, release, CI, default-policy, destructive git/filesystem, or
  unrelated dirty worktree changes.

## End-Of-Phase Requirements

1. Run the required document/source-inventory checks.
2. Write the Phase 1 result.
3. Refresh the Phase 2 subplan.
4. Review the contract, Phase 1 result, and refreshed Phase 2 subplan.
5. Update the execution ledger and Claude review ledger.
