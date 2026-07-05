# Phase 4 Result: Generic Analytical-Derivative Contract

Date: 2026-07-01

Status: `GENERIC_NSSM_PHASE4_REVIEWED_CLOSED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 4 closes the generic analytical-derivative contract as a reviewed, document-only branch-discipline pass. Same-branch signature rules, backend taxonomy, and the distinction between current-score objects and propagation-only objects are now frozen before implementation. |
| Primary criterion status | Met locally: derivative obligations are explicit and fail-closed, and no derivative lane is promoted without the value gate. |
| Veto diagnostic status | Passed locally: no autodiff fallback was silently treated as analytical admission, no same-branch mismatch rule was omitted, and no derivative claim was advanced ahead of the value gate. |
| Main uncertainty | The code-wiring phase must still align implementation with these frozen derivative obligations. |
| Next justified action | Execute Phase 5 by first writing a reviewed executable implementation refresh. |
| What is not being concluded | No implementation pass, no gradient pass, no HMC readiness, and no top-level/production promotion. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What analytical-derivative obligations must a generic nonlinear-SSM lane satisfy before value/score admission is allowed? |
| Baseline/comparator | Phase 3 lane architecture, chapter-defined branch-valid derivative contracts, and current derivative code seams. |
| Primary criterion | Met locally: Phase 4 fixes same-branch signature rules, backend taxonomy, and analytical-gradient admission boundaries without authorizing implementation or promotion. |
| Veto diagnostics | Passed locally: no same-branch mismatch omission, no autodiff fallback silently treated as analytical admission, and no blurred score/path objects in the derivative contract. |
| Explanatory diagnostics | derivative-anchor inventory, backend taxonomy notes, and review-ready observations. |
| Not concluded | No implementation pass, no gradient pass, no HMC readiness, and no top-level/production promotion. |
| Artifact | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase4-derivative-contract-result-2026-07-01.md` and refreshed `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-subplan-2026-07-01.md`. |

## Derivative Contract Summary

Reviewed obligations now fixed for later implementation phases:

- same-branch signature equality is required for any same-scalar derivative
  claim;
- value-before-gradient remains a hard gate;
- derivative backend categories must distinguish:
  - analytically admitted,
  - fallback/autodiff-only,
  - blocked/missing derivative route;
- current-score objects and propagation-only objects must be separated in the
  implementation contract and later validation artifacts.

Current seam implications from the codebase:

- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py` already carries the
  same-branch signature machinery and lane-local analytical derivative scaffold;
- `bayesfilter/highdim/derivatives.py` carries fixed-branch derivative and
  replay-tape machinery for the highdim lane;
- later phases may not treat existence of derivative code as evidence of generic
  analytical-gradient admission without value-gate and same-branch validation.

## Local Checks

Commands:

```bash
test -f bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py
test -f bayesfilter/highdim/derivatives.py
test -f bayesfilter/highdim/filtering.py
test -f bayesfilter/highdim/models.py
rg -n "same_branch|same_scalar|derivative_method|branch_identity|d_transition_fn|d_observation_fn|parameter_score|GradientTape|replay" bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py bayesfilter/highdim/derivatives.py bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py
git diff --check -- docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient*.md
```

Outcome:

- Required derivative seam files existed locally.
- Grep coverage confirmed same-branch, derivative-method, branch-identity,
  replay, and parameter-derivative anchor language in the expected files.
- Document diff hygiene passed.

## Bounded Claude Reviews

Reviewed artifacts and outcomes:

- refreshed Phase 5 subplan: not yet independently reviewed in this turn; prepared for the next bounded review packet
- Phase 4 result: prepared for review; no independent wrapper-based result review has been recorded yet in this turn

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: the derivative contract is anchored to chapter-defined same-scalar and branch-validity obligations. |
| Proxy metric promoted | Avoided: reverse-mode availability or FD agreement alone is not analytical admission. |
| Missing stop condition | Avoided: any lane lacking branch-valid obligations remains blocked or fallback-only. |
| Unfair comparison | Avoided: current-score objects and propagation-only objects are kept distinct. |
| Hidden assumption | Avoided: Phase 4 does not assume autodiff fallback and model-provided scores have the same authority. |
| Stale context | Avoided: derivative semantics are derived from current derivative code and chapter contracts. |
| Environment mismatch | Avoided: Phase 4 remained code/document inspection only. |
| Artifact-answer mismatch | Avoided: the result closes with explicit derivative obligations and backend categories. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Worktree status | Dirty pre-existing research/doc worktree; unrelated dirty changes preserved. |
| Execution target | Document-only generic analytical-derivative contract phase. |
| CPU/GPU status | No TensorFlow numerical command and no GPU/CUDA command were run in Phase 4. |
| Runtime status | No implementation, runtime, benchmark, HMC, package/network, release, CI, production, or default-policy command was run. |
| Plan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase4-derivative-contract-subplan-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase4-derivative-contract-result-2026-07-01.md` |
| Refreshed Phase 5 subplan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-subplan-2026-07-01.md` |

## Phase 5 Handoff

Phase 5 may start only after the ledgers record that:

- same-branch derivative obligations and backend taxonomy are the active
  derivative authority;
- the Phase 4 result is reviewed `AGREE`;
- the refreshed Phase 5 subplan is reviewed `AGREE`;
- and no derivative route may be promoted before the value gate.

Phase 5 must first write a reviewed executable implementation refresh before any
code edit or test command runs.
