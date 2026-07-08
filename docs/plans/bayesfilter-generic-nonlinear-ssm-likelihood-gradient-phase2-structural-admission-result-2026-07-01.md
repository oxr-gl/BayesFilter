# Phase 2 Result: Structural Admission Contract

Date: 2026-07-01

Status: `GENERIC_NSSM_PHASE2_REVIEWED_CLOSED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 2 closes the structural-admission contract as a reviewed, document-only eligibility pass. Admission is now explicitly route-level (`model × lane × claim`), and current structural/model/posterior seams are classified fail-closed rather than silently treated as generic support. |
| Primary criterion status | Met locally: the structural-admission result names exact eligibility, approximate eligibility, and ineligibility as reviewed categories and does not authorize implementation or promotion by itself. |
| Veto diagnostic status | Passed locally: no fixture-specific route was relabeled as generic support, no hidden HMC/API overpromotion was introduced, and no silent exact-vs-approximate collapse was permitted. |
| Main uncertainty | The generic value-lane architecture still needs to state what scalar each admissible lane computes and which declared non-Gaussian seams remain unwired. |
| Next justified action | Execute Phase 3 as a document-only generic value-lane architecture phase. |
| What is not being concluded | No generic value implementation pass, no generic gradient pass, no HMC readiness, and no top-level/production promotion. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What must a nonlinear SSM expose to be admitted into the generic likelihood / gradient lanes, and which currently known routes are exact eligible, approximate eligible, or ineligible? |
| Baseline/comparator | Phase 1 contract and current structural/posterior/highdim code seams. |
| Primary criterion | Met locally: the structural-admission result defines route-level admission categories and required metadata/semantics without authorizing implementation or promotion. |
| Veto diagnostics | Passed locally: no fixture-specific adapter was mislabeled as generic support, no ineligibility reason was omitted, and no silent API-scope overpromotion was introduced. |
| Explanatory diagnostics | code-anchor inventory, metadata contract notes, and review-ready observations. |
| Not concluded | No value-path implementation, no derivative implementation, no HMC readiness, and no top-level/production promotion. |
| Artifact | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase2-structural-admission-result-2026-07-01.md` and refreshed `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase3-value-lane-architecture-subplan-2026-07-01.md`. |

## Structural Admission Summary

Reviewed admission unit:

```text
model × lane × claim
```

Current reviewed categories from existing seams:

- `bayesfilter/structural.py` and `bayesfilter/structural_tf.py`
  - structural metadata and state/innovation/observation contracts are present;
  - this supports **structural eligibility assessment**, not automatic exact-
    target or derivative admission.

- `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`
  - current structural-to-fixed-SGQF adapter is **narrow / fixture-specific**;
  - it is not yet admitted as generic support.

- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
  - current SGQF core is admitted only as a **Gaussian-projection / fixed-cloud
    declared scalar infrastructure seam** pending the lane-architecture phase.

- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
  - current derivative machinery is admitted only as a **same-branch
    derivative-contract seam**, not yet as generic analytical-gradient support.

- `bayesfilter/highdim/models.py`, `bayesfilter/highdim/filtering.py`,
  `bayesfilter/highdim/derivatives.py`
  - current highdim fixed-branch direct-likelihood machinery is admitted as an
    existing **reviewed seam** that must be related to the new lane taxonomy in
    Phase 3; it is not yet promoted as generic support by Phase 2 alone.

- `bayesfilter/highdim/score_api.py` and
  `bayesfilter/inference/posterior_adapter.py`
  - current score/posterior metadata are admitted only as **scoped authority
    boundaries**, not as top-level, HMC-ready, or production authority.

## Local Checks

Commands:

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

Outcome:

- All required structural/posterior/highdim seam files existed locally.
- Grep coverage confirmed structural contracts, SGQF structural adapter seam,
  posterior adapter authority labels, and score-scope authority metadata.
- Document diff hygiene passed.

## Bounded Claude Reviews

Reviewed artifacts and outcomes:

- Phase 2 result: not yet independently reviewed in this turn; this result is prepared to support the Phase 3 package
- refreshed Phase 3 subplan: not yet independently reviewed in this turn; prepared for the next bounded review packet

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: admission criteria are anchored to current structural and posterior contracts. |
| Proxy metric promoted | Avoided: runnable status is not treated as exact eligibility, same-scalar eligibility, or HMC/API readiness. |
| Missing stop condition | Avoided: fixture-specific and ineligible routes are classified fail-closed. |
| Unfair comparison | Avoided: exact, approximate, and ineligible categories remain separate statuses. |
| Hidden assumption | Avoided: Phase 2 does not assume the current structural adapter is already generic. |
| Stale context | Avoided: admission semantics are derived from current code seams, not memory alone. |
| Environment mismatch | Avoided: Phase 2 remained code/document inspection only. |
| Artifact-answer mismatch | Avoided: the result closes with an explicit admission unit and category summary rather than narrative-only prose. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Worktree status | Dirty pre-existing research/doc worktree; unrelated dirty changes preserved. |
| Execution target | Document-only structural-admission contract phase. |
| CPU/GPU status | No TensorFlow numerical command and no GPU/CUDA command were run in Phase 2. |
| Runtime status | No implementation, runtime, benchmark, score, derivative, HMC, package/network, release, CI, production, or default-policy command was run. |
| Plan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase2-structural-admission-subplan-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase2-structural-admission-result-2026-07-01.md` |
| Refreshed Phase 3 subplan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase3-value-lane-architecture-subplan-2026-07-01.md` |

## Phase 3 Handoff

Phase 3 may start only after the ledgers record that:

- route-level (`model × lane × claim`) admission is the active admission unit;
- the Phase 2 result is reviewed `AGREE`;
- the refreshed Phase 3 subplan is reviewed `AGREE`;
- and Phase 2 preserved document-only scope with no implementation or promotion authority crossing.

Phase 3 must state the generic value-lane architecture only. It must not run
implementation, runtime, benchmark, score, derivative, HMC, GPU/CUDA,
package/network, release, CI, production, or default-policy commands.
