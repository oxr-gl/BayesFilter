# Phase 0 Subplan: Program Launch And Inherited-Boundary Freeze

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Launch the generic nonlinear-SSM governed program, freeze inherited chapter and
code anchors, and verify that the launch package is coherent before any
implementation or promotion work begins.

## Entry Conditions Inherited From Previous Phase

- The scientific need for generic nonlinear-SSM likelihood / analytical-gradient
  support has been identified.
- The chapter foundations and current code seams have been inventoried at plan
  time.
- No implementation, benchmark, HMC, top-level API, or production promotion
  authority exists yet.

## Required Artifacts

- master program:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-master-program-2026-07-01.md`
- runbook:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-gated-execution-runbook-2026-07-01.md`
- execution ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-execution-ledger-2026-07-01.md`
- Claude review ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-claude-review-ledger-2026-07-01.md`
- stop handoff:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-stop-handoff-2026-07-01.md`
- target-and-authority contract:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-target-authority-contract-2026-07-01.md`
- Phase 0 result:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase0-launch-result-2026-07-01.md`
- refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase1-target-authority-contract-subplan-2026-07-01.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-master-program-2026-07-01.md
test -f docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-gated-execution-runbook-2026-07-01.md
test -f docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-execution-ledger-2026-07-01.md
test -f docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-claude-review-ledger-2026-07-01.md
test -f docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-stop-handoff-2026-07-01.md
test -f docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-target-authority-contract-2026-07-01.md
test -f docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex
test -f docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex
test -f docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex
test -f docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex
test -f docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex
rg -n "bayesfilter/structural.py|bayesfilter/structural_tf.py|bayesfilter/inference/posterior_adapter.py|bayesfilter/nonlinear/fixed_sgqf_tf.py|bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py|bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py|bayesfilter/highdim/models.py|bayesfilter/highdim/filtering.py|bayesfilter/highdim/derivatives.py|bayesfilter/highdim/score_api.py" docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-master-program-2026-07-01.md docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase0-launch-subplan-2026-07-01.md
rg -n "target-and-authority|wrong-target Gaussian|value-before-gradient|same-branch|subpackage|no lower-ranked artifact" docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient*.md
git diff --check -- docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient*.md
```

Required read-only Claude reviews:

Core review-gated launch authorities:

- master program,
- target-and-authority contract,
- visible runbook,
- this Phase 0 subplan,
- then Phase 0 result and refreshed Phase 1 subplan.

Supporting inputs that must exist and be cross-checked locally, but do not
require separate one-path review unless an inconsistency is later found:

- visible execution ledger,
- Claude review ledger,
- stop handoff,
- chapter anchors,
- inherited code-seam inventory named in the master package.

The execution ledger, Claude review ledger, and stop handoff are bookkeeping or
state-tracking artifacts in Phase 0: they must be updated as part of closeout,
but they do not require separate one-path review unless a later bounded review
finds an inconsistency in them.

No implementation, runtime, benchmark, score, derivative, HMC, GPU/CUDA,
package/network, release, CI, production, or default-policy command is
authorized in Phase 0.

## Skeptical Plan Audit

| Risk Checked | Phase 0 Control |
| --- | --- |
| Wrong baseline | Phase 0 requires chapter anchors, the master program, and the target-and-authority contract to exist before closeout. |
| Proxy metric promoted | Artifact existence and review closure are launch criteria only; they do not admit any lane, value path, or gradient lane. |
| Missing stop condition | Wrong target identity, wrong-scalar Gaussian closure, same-branch mismatch, missing structural-admission contract, and API-scope drift are all explicit blockers in the launch package. |
| Unfair comparison | Exact-target, Gaussian-projection, fixed-cloud, direct-likelihood, diagnostic, and blocked lanes are kept separate from launch. |
| Hidden assumption | Phase 0 does not assume the current structural adapter or SGQF lane is already generic. |
| Stale context | The master package explicitly anchors the chapter and code seams future phases must obey. |
| Environment mismatch | Phase 0 is document-only. No runtime evidence is created. |
| Artifact-answer mismatch | Phase 0 must close with reviewed launch artifacts plus a refreshed Phase 1 subplan; a partial package is insufficient. |

Audit status: passed for launch preparation if the required artifacts exist,
local checks pass, and the bounded Claude reviews converge.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generic nonlinear-SSM program safely launch a fresh anti-drift governance package before any implementation or promotion work begins? |
| Baseline/comparator | chapter-defined target/branch contracts and current code seams. |
| Primary criterion | The core governance package is coherent, locally checked, reviewed, and explicit about target authority, lane taxonomy, branch obligations, and no-choice execution discipline. |
| Veto diagnostics | wrong target identity, wrong-scalar Gaussian closure drift, missing target-and-authority contract, missing stop conditions, missing inherited seam freeze, or phase advance without review. |
| Explanatory diagnostics | artifact existence, keyword coverage, and review notes. |
| Not concluded | No generic lane admission, no value pass, no gradient pass, no HMC readiness, no top-level API promotion, and no production/default claim. |
| Artifact | reviewed launch package, Phase 0 result, and refreshed Phase 1 subplan. |

## Forbidden Claims/Actions

- Do not claim generic support is implemented.
- Do not claim any value or gradient route is admitted.
- Do not ask the user to choose mathematical conventions already fixed by the
  contract.
- Do not run implementation, runtime, benchmark, score, derivative, HMC,
  GPU/CUDA, package/network, release, CI, production, or default-policy
  commands.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if:

- the master program receives Claude `VERDICT: AGREE`;
- the target-and-authority contract receives Claude `VERDICT: AGREE`;
- the visible runbook receives Claude `VERDICT: AGREE`;
- this Phase 0 subplan receives Claude `VERDICT: AGREE`;
- the Phase 0 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 1 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records Phase 0 as reviewed closed rather than merely
  locally prepared.

## Stop Conditions

- Any launch artifact contradicts the exact-target / approximate-scalar / same-
  scalar contract.
- A launch artifact blurs exact-target and Gaussian-closure surrogate status.
- Local document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require implementation, runtime, GPU/HMC, package/network,
  release, CI, default-policy, destructive git/filesystem, or unrelated dirty
  worktree changes.

## End-Of-Phase Requirements

1. Run the required local document checks.
2. Review the launch package with bounded read-only Claude prompts.
3. Write the Phase 0 result.
4. Refresh the Phase 1 subplan.
5. Record launch and Phase 0 review outcomes in the execution ledger and Claude
   review ledger.
