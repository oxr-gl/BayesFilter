# Phase 5 Subplan: Positive-Feature Prototype

Date: 2026-06-17

## Phase Objective

Plan the next candidate phase: a TensorFlow positive-feature transport
prototype that returns feature factors, scaling vectors, and transported
particles under the Phase 3 schema.

Phase 5 should decide whether fixed positive features are worth implementing
and testing after the Phase 4 Nystrom factor route passed its full-rank
correctness probe.  Phase 5 must treat the positive-feature kernel as either an
approximation to the dense Gibbs kernel or an explicit semantic replacement;
it must not silently claim dense OT equivalence.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result records `PHASE_1_BASELINE_FIXTURE_PASSED`.
- Phase 2 result records
  `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`.
- Phase 3 result records `PHASE_3_COMMON_INTERFACE_HARNESS_PASSED`.
- Phase 4 result records `PHASE_4_NYSTROM_PROTOTYPE_PASSED`, with rank scope
  `full_rank_factor_correctness_probe`.
- Positive-feature audit records `source_locked`, semantic class
  `approximate kernel / semantic kernel replacement`, and execution value
  `execution_value_pending`.
- The comparator remains the Phase 1 local TensorFlow dense/streaming baseline.
  Phase 4 Nystrom diagnostics may be used as additional explanatory context,
  not as a ranking baseline.
- No speedup, ranking, posterior correctness, production readiness, or default
  change has been claimed.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p05-positive-feature-prototype-result-2026-06-17.md`
- TensorFlow implementation artifact if the implementation gate passes:
  `experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py`
- Diagnostic script:
  `docs/benchmarks/scalable_ot_p05_positive_feature_prototype_diagnostics.py`
- JSON result:
  `docs/benchmarks/scalable-ot-p05-positive-feature-prototype-diagnostics-2026-06-17.json`
- Markdown result:
  `docs/benchmarks/scalable-ot-p05-positive-feature-prototype-diagnostics-2026-06-17.md`
- Focused tests under `tests/` if implementation proceeds.
- Updated execution ledger and stop handoff.
- Phase 6 low-rank coupling subplan draft:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-subplan-2026-06-17.md`

## Source Anchors Required Before Coding

| Anchor | Required use |
| --- | --- |
| `.localsource/scalable_ot_survey/2006.07057.txt` lines 201-204 | Positive feature map and kernel definition. |
| `.localsource/scalable_ot_survey/2006.07057.txt` lines 224-271 | Feature matrices, finite positive features, and approximation route. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` lines 546-624 | Local equations for positive features, feature kernel, induced cost, factorization, dual, finite features, transport application, and semantic warning. |
| `.localsource/scalable_ot_code_audit/LinearSinkhorn/FastSinkhorn.py` lines 77-99 | Reference positive-feature scaling updates for `K = A B`. |
| `.localsource/scalable_ot_code_audit/LinearSinkhorn/FastSinkhorn.py` lines 102-161 | Reference RBF feature route and random feature map. |
| `.localsource/scalable_ot_code_audit/MANIFEST.md` lines 82-87 | Source availability and reuse posture for LinearSinkhorn/positive-feature scripts. |

## Required Checks, Tests, And Reviews

Before implementation:

1. Re-read the positive-feature audit note, Phase 4 result, Phase 3 schema, and
   the local source anchors.
2. Decide and record the Phase 5 semantic posture before coding:
   `approximate_kernel` if the feature map is intended to approximate the dense
   Gibbs kernel, or `semantic_replacement` if the feature kernel is treated as a
   new cost.
3. Classify source route:
   - `source_faithful` for anchored positive-feature factor/scaling operations;
   - `fixed_hmc_adaptation` for frozen seeds/features/radius choices used only
     for deterministic BayesFilter testing;
   - `extension_or_invention` for any feature map or stabilization not
     present in the source route.
4. Confirm no NumPy/PyTorch code is promoted to BayesFilter default.

If implementation proceeds:

1. Syntax/import checks for all new Python files.
2. Tiny fixed-feature fixture with finite transported particles.
3. Phase 1 fixture diagnostic with feature factors, scaling vectors, residuals,
   dense-reference particle error, and Nystrom explanatory comparison when
   available.
4. Candidate result must validate under the Phase 3 schema.
5. Hard-veto diagnostics must include finite features/scalings/particles,
   strictly positive feature kernel denominators, valid shapes, row residual,
   column residual, and explicit semantic class.
6. Promotion diagnostics must include dense-reference transported-particle
   error only if Phase 5 is declared as `approximate_kernel`; if declared as
   `semantic_replacement`, dense-reference error is explanatory only.

Review:

- Phase 5 is implementation-bearing.  Run local checks first, then use Claude
  as read-only reviewer for the subplan or material repairs.
- Use bounded path-based review or no-file micro reviews if file review stalls.
- Claude cannot authorize phase advancement.
- Stop after five review rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can fixed positive features produce finite, diagnostically valid transported particles on Phase 1 fixtures, with the semantic delta from dense entropic OT explicitly classified? |
| Baseline/comparator | Phase 1 dense/streaming TensorFlow baseline; Phase 4 Nystrom result is explanatory context only. |
| Primary pass criterion | If implementation proceeds, a Phase 3-valid candidate record exists with finite feature factors/scalings/particles, valid residuals under declared thresholds, and dense-reference or semantic-delta diagnostics consistent with the declared semantic class. |
| Promotion veto | Scalar loss only; nonpositive/zero feature kernel causing invalid scaling; missing transported particles; wrong orientation; feature seed/radius not recorded; dense-equivalence claim without approximation contract; non-TensorFlow default route. |
| Continuation veto | Source anchors contradict planned feature route; Phase 1 baseline missing; schema cannot represent feature factors; implementation requires package installation, network fetch, GPU evidence, or non-TensorFlow default code; semantic class cannot be chosen without user direction. |
| Repair trigger | Localized orientation, scaling, epsilon/reg map, feature count, seed/radius rule, dtype, or denominator stabilization issue. |
| Explanatory diagnostics | Feature count, seed/radius rule, feature positivity, denominator floor hits, residuals, dense-reference error, Nystrom comparison, runtime, and memory proxy. |
| Not concluded | No dense OT equivalence unless approximation evidence supports it, no speedup, no ranking, no posterior correctness, no production/default readiness. |
| Artifact preserving result | Phase 5 implementation if any, diagnostic JSON/Markdown, tests/logs, Phase 5 result, ledger, stop handoff, and Phase 6 subplan. |

## Skeptical Plan Audit

- Wrong baseline: Phase 5 must compare against Phase 1 local dense/streaming
  baseline, not a standalone LinearSinkhorn scalar cost.
- Proxy metric risk: runtime and feature count are explanatory until transport
  validity passes.
- Missing stop conditions: stop if semantic class cannot be declared, feature
  route lacks anchors, or only scalar-loss code is available.
- Unfair comparisons: positive-feature transport may be a semantic replacement;
  it cannot be ranked against Nystrom by source availability or one fixture.
- Hidden assumptions: feature map, seed, radius, epsilon/reg map, orientation,
  and target weights must be recorded.
- Stale context: Phase 4 passed only a full-rank Nystrom correctness probe; it
  is not a scaling benchmark.
- Environment mismatch: no package installation, no network fetch, no GPU
  evidence, no non-TensorFlow default implementation.
- Artifact adequacy: a scalar cost or loss trace is not a BayesFilter transport
  object.

Skeptical audit status: `PASSED_FOR_PHASE_5_POSITIVE_FEATURE_PROTOTYPE_PLAN`.

## Forbidden Claims And Actions

- Do not claim speedup, ranking, production/default readiness, posterior
  correctness, or general scalability.
- Do not claim exact dense OT equivalence unless the declared approximation
  contract passes.
- Do not treat LinearSinkhorn NumPy/PyTorch code as BayesFilter default.
- Do not install packages, fetch network sources, or use GPU evidence.
- Do not unblock Mini-batch/BoMb.
- Do not modify unrelated dirty user work.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only after:

- Phase 5 result records a pass, non-promoted candidate result, or precise
  blocker/failure result;
- implementation and diagnostic artifacts exist, or the result explains why
  implementation stopped;
- local syntax/import/diagnostic checks pass when implementation proceeds;
- candidate JSON validates against the Phase 3 schema when implementation
  proceeds;
- semantic class and source-route classification are recorded with anchors;
- Phase 6 low-rank coupling subplan exists and has been reviewed for
  consistency, correctness, feasibility, artifact coverage, and boundary
  safety;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- the semantic class cannot be chosen without user direction;
- the feature route would only produce scalar loss, not transported particles;
- source anchors contradict the planned factor/scaling/application operation;
- package installation, network fetch, GPU evidence, credentials, destructive
  action, or non-TensorFlow default code would be required;
- local checks reveal a hard veto not localized to a repair trigger;
- Claude and Codex do not converge after five focused review rounds for the
  same material blocker.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 5 result/close record.
3. Draft or refresh the Phase 6 low-rank coupling prototype subplan.
4. Review the Phase 6 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
