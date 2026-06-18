# Phase 7 Subplan: Exact Online/GPU Reference Study

Date: 2026-06-17
Draft timestamp: 2026-06-18T03:39:48+08:00

## Phase Objective

Plan the exact-semantics reference lane for online/GPU Sinkhorn ideas.  Phase 7
decides whether to keep GeomLoss/KeOps, FlashSinkhorn, and OTT-JAX style
operators as references only, or to design a later TensorFlow operator refactor
that preserves the Phase 1 dense transport semantics while reducing dense
materialization.

Phase 7 is a reference/operator planning phase unless a reviewed implementation
repair is explicitly added.  It must not run GPU evidence, install packages,
execute PyTorch/JAX/Triton/KeOps sources, or treat external sources as
BayesFilter default code without approval.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result records `PHASE_1_BASELINE_FIXTURE_PASSED`.
- Phase 2 result records
  `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`.
- Phase 3 result records `PHASE_3_COMMON_INTERFACE_HARNESS_PASSED`.
- Phase 4 result records `PHASE_4_NYSTROM_PROTOTYPE_PASSED`.
- Phase 5 result records
  `PHASE_5_POSITIVE_FEATURE_PROTOTYPE_PASSED_SEMANTIC_REPLACEMENT`.
- Phase 6 result records
  `PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED`.
- Exact online/GPU audit records `source_reference_only`, semantic class
  `exact semantics / reference-only`, and execution value
  `execution_value_pending`.
- The comparator remains the Phase 1 local TensorFlow dense/streaming baseline.
- No GPU performance, speedup, ranking, posterior correctness, production
  readiness, or default change has been claimed.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p07-exact-online-gpu-reference-result-2026-06-17.md`
- If implementation proceeds after a focused repair decision:
  `docs/benchmarks/scalable_ot_p07_exact_online_reference_diagnostics.py`
- If implementation proceeds, JSON result:
  `docs/benchmarks/scalable-ot-p07-exact-online-reference-diagnostics-2026-06-17.json`
- If implementation proceeds, Markdown result:
  `docs/benchmarks/scalable-ot-p07-exact-online-reference-diagnostics-2026-06-17.md`
- Updated execution ledger and stop handoff.
- Phase 8 sparse/localized diagnostic subplan draft:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p08-sparse-localized-diagnostic-subplan-2026-06-17.md`

## Source Anchors Required Before Execution

| Anchor | Required use |
| --- | --- |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-exact-online-gpu-audit-2026-06-17.md` | Paper-note-code-execution matrix and first execution-value contract for exact online/GPU lane. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` lines 390-435 | Local equations and explanation for exact online/GPU Sinkhorn as semantics-preserving memory/IO/GPU engineering. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-source-lock-result-2026-06-17.md` lines 78 and 91 | Source-lock row for exact online/GPU and reference-only classification. |
| `.localsource/scalable_ot_code_audit/MANIFEST.md` lines 31-54 and 205 | GeomLoss/FlashSinkhorn source posture and exact-reference classification. |
| `.localsource/scalable_ot_code_audit/MANIFEST.md` lines 165-173 | OTT-JAX operator/source posture and non-default backend classification. |

## Required Checks, Tests, And Reviews

Before any implementation or external execution:

1. Re-read the exact online/GPU audit note, Phase 1 baseline result, Phase 3
   schema, and source anchors above.
2. Record the Phase 7 semantic posture as `exact_semantics` only if the route
   preserves the Phase 1 dense transported particles within declared parity
   tolerance; otherwise keep the lane `reference_only`.
3. Classify implementation route:
   - `source_reference_only` for GeomLoss/FlashSinkhorn/OTT-JAX paper/source
     inspection;
   - `fixed_hmc_adaptation` for a TensorFlow streaming/operator refactor that
     preserves the Phase 1 route;
   - `extension_or_invention` for a new operator route not anchored in the
     inspected sources.
4. Confirm no PyTorch/JAX/Triton/KeOps route is promoted to BayesFilter default.
5. Stop for approval before package installation, network fetch, GPU evidence,
   or external library execution.

If a TensorFlow operator/reference diagnostic proceeds:

1. Syntax/import checks for new Python files.
2. Phase 1 fixture parity against dense transported particles.
3. Transport object must be `streaming_nonmaterialized` or `lazy_operator`
   under the Phase 3 schema.
4. Hard-veto diagnostics must include finite particles, orientation parity,
   dense-reference transported-particle parity, row/column residuals or a
   recorded reason they cannot be recomputed without materialization, and
   explicit `exact_semantics` or `reference_only` classification.
5. Runtime and memory proxy are explanatory only unless parity passes first.

Review:

- Phase 7 is boundary-sensitive.  Run local checks first, then use Claude as
  read-only reviewer for the subplan or material repairs.
- Claude cannot authorize GPU, network, installation, or default-code boundary
  crossings.
- Stop after five review rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Should exact online/GPU Sinkhorn sources remain reference-only, or is there a bounded TensorFlow operator/parity diagnostic worth implementing next? |
| Baseline/comparator | Phase 1 dense/streaming TensorFlow baseline. |
| Primary pass criterion | A Phase 7 result records either reference-only retention with source/boundary rationale, or a Phase 3-valid TensorFlow operator diagnostic with dense transported-particle parity and explicit nonmaterialization reason. |
| Promotion veto | Runtime-only evidence; GPU warning interpreted as hardware evidence; wrong orientation; missing transported particles; external PyTorch/JAX/Triton/KeOps route promoted as default; package/network/GPU action without approval. |
| Continuation veto | Exact semantic parity cannot be specified; Phase 1 baseline missing; TensorFlow operator path would require non-approved package install or external backend; GPU evidence is required but unapproved. |
| Repair trigger | Localized orientation, chunking, operator shape, parity tolerance, dtype, or schema representation issue. |
| Explanatory diagnostics | Source maturity, operator API shape, chunk/tile size, memory proxy, runtime after parity, GPU-readiness notes, and implementation effort. |
| Not concluded | No speedup, no GPU performance, no ranking, no posterior correctness, no production/default readiness, no subquadratic arithmetic improvement. |
| Artifact preserving result | Phase 7 result, optional diagnostics, ledger, stop handoff, and Phase 8 subplan. |

## Skeptical Plan Audit

- Wrong baseline: Phase 7 must use Phase 1 dense/streaming TensorFlow baseline,
  not external library demos.
- Proxy metric risk: runtime, memory proxy, and GPU/source maturity are
  explanatory until exact transported-particle parity passes.
- Missing stop conditions: stop for unapproved GPU, package, network, external
  backend, or default-policy boundary crossings.
- Unfair comparisons: exact online/GPU preserves semantics and all-pairs work;
  it must not be ranked against low-rank/semantic-replacement candidates from
  static source evidence.
- Hidden assumptions: epsilon/blur/cost-scale mapping, orientation, chunking,
  device context, and backend must be recorded.
- Stale context: Phase 4, Phase 5, and Phase 6 do not rank this lane.
- Environment mismatch: GPU/CUDA evidence requires trusted context and
  approval; PyTorch/JAX/Triton/KeOps sources are references only.
- Artifact adequacy: source inspection or runtime-only output is not a
  BayesFilter transport artifact.

Skeptical audit status:
`PASSED_FOR_PHASE_7_EXACT_ONLINE_GPU_REFERENCE_STUDY_PLAN`.

## Forbidden Claims And Actions

- Do not claim speedup, GPU performance, ranking, production/default readiness,
  posterior correctness, or subquadratic arithmetic.
- Do not execute external PyTorch/JAX/Triton/KeOps sources without approval.
- Do not install packages, fetch network sources, or use GPU evidence without
  approval.
- Do not treat external code as BayesFilter default.
- Do not modify unrelated dirty user work.
- Do not unblock Mini-batch/BoMb.

## Exact Next-Phase Handoff Conditions

Phase 8 may begin only after:

- Phase 7 result records reference-only retention, a passed TensorFlow parity
  diagnostic, or a precise blocker/failure result;
- required diagnostics exist, or the result explains why implementation did not
  proceed;
- local checks pass for any implementation artifact;
- schema validation passes for any candidate JSON;
- semantic class and source-route classification are recorded;
- Phase 8 sparse/localized diagnostic subplan exists and has been reviewed for
  consistency, correctness, feasibility, artifact coverage, and boundary
  safety;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- exact semantic parity cannot be specified;
- package installation, network fetch, GPU evidence, credentials, destructive
  action, or external backend execution would be required without approval;
- the route would only produce runtime/source evidence, not a transport object
  or explicit reference-only decision;
- local checks reveal a hard veto not localized to a repair trigger;
- Claude and Codex do not converge after five focused review rounds for the
  same material blocker.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 7 result/close record.
3. Draft or refresh the Phase 8 sparse/localized diagnostic subplan.
4. Review the Phase 8 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
