# Phase 2 Subplan: Candidate Audit Notes

Date: 2026-06-17

## Phase Objective

Write paper-note-code audit notes for each scalable OT candidate lane before
any candidate implementation begins.  Each note must compare the original paper,
the local survey/note, the downloaded source code, and the first execution-value
test that would be needed for that lane.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result records `PHASE_1_BASELINE_FIXTURE_PASSED`.
- Baseline fixture spec, JSON diagnostics, Markdown summary, and log exist.
- Dense and streaming TensorFlow baseline diagnostics are available for the
  required fixtures.
- Mini-batch/BoMb remains blocked for decision-grade use until clean source is
  available.
- No human-required stop condition is active.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-candidate-audit-notes-result-2026-06-17.md`
- Candidate audit notes:
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-exact-online-gpu-audit-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-nystrom-audit-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-audit-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-coupling-audit-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sparse-localized-audit-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sliced-subspace-audit-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-minibatch-bomb-audit-2026-06-17.md`
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p03-common-interface-harness-subplan-2026-06-17.md`

## Required Checks, Tests, And Reviews

Local checks:

1. Verify each audit note contains the mandatory comparison matrix:
   original paper, local note, downloaded code, execution-value test, and
   required resolution.
2. Verify each audit note states whether the lane is exact semantics,
   approximate kernel, semantic replacement, reference-only, or blocked.
3. Verify each audit note cites at least one paper/survey anchor and one
   downloaded source-code anchor, or marks the lane blocked.
4. Verify Mini-batch/BoMb is marked `source_partial_user_needed` unless clean
   source has been supplied.
5. Verify no audit note claims execution value or ranking before candidate
   runs.
6. Verify no audit note promotes PyTorch/JAX/Triton/C++ source as a BayesFilter
   default implementation path.

Review:

- Claude read-only review is required for this phase because candidate audit
  notes affect implementation order and boundaries.
- Review should be concise and may be split by lane group if a whole-phase
  prompt stalls.
- `VERDICT: AGREE` is review-convergence evidence only, not authorization.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the candidate lanes sufficiently source-grounded and semantically classified to design a common interface harness and first candidate prototypes? |
| Baseline/comparator | Phase 1 TensorFlow dense/streaming baseline fixtures and the Phase 0 source-lock result. |
| Primary pass criterion | Every lane has an audit note with paper-note-code-execution comparison; blocked lanes are explicitly blocked; no execution-value or ranking claim is made. |
| Veto diagnostics | Missing paper/source anchor; missing transport-object classification; Mini-batch unblocked without clean source; non-TensorFlow default path; scalar loss treated as transport; execution value inferred from source inspection. |
| Explanatory diagnostics | Implementation effort, backend mismatch, transport object shape, approximation knob, and first fixture needed. |
| Not concluded | No candidate correctness, no speedup, no production readiness, no public API readiness, no statistical ranking. |
| Artifact preserving result | Candidate audit notes, Phase 2 result, review artifacts, and ledger entry. |

## Skeptical Plan Audit

- Wrong baseline: audit notes must reference Phase 1 baseline fixtures, not
  external library demos as the comparator.
- Proxy metric risk: implementation maturity and GitHub validity are
  explanatory only.
- Missing stop conditions: missing anchors, source blockers, and semantic
  mismatch are vetoes.
- Unfair comparisons: exact, approximate-kernel, and semantic-replacement lanes
  must be classified separately.
- Hidden assumptions: each note must state cost/kernel, orientation/marginals,
  returned object, backend, and approximation knob.
- Stale context: use dated Phase 0/1 artifacts and local `.localsource`
  manifests.
- Environment mismatch: do not install or run external packages in this phase.
- Artifact adequacy: audit notes answer the source-grounding question; no code
  implementation is needed here.

Skeptical audit status: `PASSED_FOR_PHASE_2_CANDIDATE_AUDIT_PLAN`.

## Forbidden Claims And Actions

- Do not implement candidate algorithms in this phase.
- Do not install packages, fetch network sources, or run external library tests.
- Do not rank candidates empirically.
- Do not claim execution value from static source/code inspection.
- Do not unblock Mini-batch/BoMb without clean source.
- Do not let Claude edit files or authorize phase advancement.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only after:

- Phase 2 result records `PHASE_2_CANDIDATE_AUDITS_PASSED`;
- all required candidate audit notes exist;
- local checks pass;
- required Claude review converges with `VERDICT: AGREE` as
  review-convergence evidence;
- Phase 3 common-interface-harness subplan exists and has been reviewed for
  consistency, correctness, feasibility, artifact coverage, and boundary
  safety;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- required paper/source anchors are missing for a non-blocked lane;
- a source-code checkout is incomplete and the lane cannot be safely marked
  blocked;
- continuing would require package installation, network fetch, credentials, or
  destructive action;
- Claude review does not converge after five rounds for the same blocker;
- user direction is needed to provide Mini-batch/BoMb source or change candidate
  scope.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 2 result/close record.
3. Draft or refresh the Phase 3 common-interface-harness subplan.
4. Review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
