# Phase 6 Subplan: Low-Rank Coupling Prototype

Date: 2026-06-17
Draft timestamp: 2026-06-18T03:22:32+08:00

## Phase Objective

Plan the next candidate phase: a TensorFlow low-rank coupling transport
prototype that exposes coupling factors `Q`, `R`, `g`, a lazy transport
application, marginal diagnostics, transported particles, and a Phase 3-valid
candidate result record.

Phase 6 studies direct low-rank coupling OT as a semantic replacement.  It
constrains or constructs the coupling itself as
`P = Q diag(1/g) R^T`; it is not a low-rank approximation to the dense Gibbs
kernel, and it must not be judged by exact dense Sinkhorn parity alone.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result records `PHASE_1_BASELINE_FIXTURE_PASSED`.
- Phase 2 result records
  `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`.
- Phase 3 result records `PHASE_3_COMMON_INTERFACE_HARNESS_PASSED`.
- Phase 4 result records `PHASE_4_NYSTROM_PROTOTYPE_PASSED`, with rank scope
  `full_rank_factor_correctness_probe`; it is explanatory only for Phase 6.
- Phase 5 result records
  `PHASE_5_POSITIVE_FEATURE_PROTOTYPE_PASSED_SEMANTIC_REPLACEMENT`; it is a
  semantic-replacement validity screen, not dense-equivalence or ranking
  evidence.
- Low-rank coupling audit records `source_locked`, semantic class
  `semantic replacement`, and execution value `execution_value_pending`.
- The comparator remains the Phase 1 local TensorFlow dense/streaming baseline.
  Phase 4 and Phase 5 diagnostics may be used only as explanatory context, not
  as ranking baselines.
- No speedup, ranking, posterior correctness, production readiness, or default
  change has been claimed.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-result-2026-06-17.md`
- TensorFlow implementation artifact if the implementation gate passes:
  `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_transport_tf.py`
- Focused tests under `tests/` if implementation proceeds:
  `tests/test_low_rank_coupling_transport_tf.py`
- Diagnostic script:
  `docs/benchmarks/scalable_ot_p06_low_rank_coupling_prototype_diagnostics.py`
- JSON result:
  `docs/benchmarks/scalable-ot-p06-low-rank-coupling-prototype-diagnostics-2026-06-17.json`
- Markdown result:
  `docs/benchmarks/scalable-ot-p06-low-rank-coupling-prototype-diagnostics-2026-06-17.md`
- Updated execution ledger and stop handoff.
- Phase 7 exact-online/GPU reference subplan draft:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p07-exact-online-gpu-reference-subplan-2026-06-17.md`

## Source Anchors Required Before Coding

| Anchor | Required use |
| --- | --- |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` lines 628-760 | Local equations for nonnegative rank, `Pi_{a,b}(r)`, `P = Q diag(1/g) R^T`, factor constraints, objective, transport application, latent-coupling extension, and rank diagnostics. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-coupling-audit-2026-06-17.md` | Paper-note-code-execution matrix and first execution-value contract for this lane. |
| `.localsource/scalable_ot_code_audit/POT/ot/lowrank.py` lines 24-147 | POT initialization routes for `Q`, `R`, and `g`; deterministic initialization is a key source route. |
| `.localsource/scalable_ot_code_audit/POT/ot/lowrank.py` lines 150-203 | Low-rank squared-Euclidean cost factorization used by POT low-rank Sinkhorn. |
| `.localsource/scalable_ot_code_audit/POT/ot/lowrank.py` lines 206-319 | LR-Dykstra update for enforcing factor marginals. |
| `.localsource/scalable_ot_code_audit/POT/ot/lowrank.py` lines 322-527 | `lowrank_sinkhorn` route returning `Q`, `R`, `g`, lazy plan, and values. |
| `.localsource/scalable_ot_code_audit/POT/ot/utils.py` lines 812-850 | Lazy low-rank tensor convention `Q @ diag(d) @ R^T`. |
| `.localsource/scalable_ot_code_audit/POT/ot/factored.py` lines 17-157 | Factored OT route returning two plans and a low-rank lazy plan. |
| `.localsource/scalable_ot_code_audit/ott-sparse/src/ott/solvers/linear/sinkhorn_lr.py` lines 120-150 | Marginal-deviation diagnostic for low-rank factors. |
| `.localsource/scalable_ot_code_audit/ott-sparse/src/ott/solvers/linear/sinkhorn_lr.py` lines 153-248 | `LRSinkhornOutput` with `q`, `r`, `g`, `matrix`, `apply`, marginals, and transport mass. |
| `.localsource/scalable_ot_code_audit/MANIFEST.md` lines 106-110 and 165-173 | Source availability and reuse posture for POT and OTT low-rank transport operators. |

## Required Checks, Tests, And Reviews

Before implementation:

1. Re-read the low-rank coupling audit note, Phase 5 result, Phase 3 schema,
   and the local source anchors above.
2. Record the Phase 6 semantic posture as `semantic_replacement` before
   coding.
3. Choose and record one of two implementation scopes before coding:
   - `solver_route`: a TensorFlow port of the anchored `Q,R,g` low-rank
     Sinkhorn/Dykstra route; or
   - `transport_object_fixture_route`: a deterministic low-rank coupling
     construction that validates the BayesFilter transport object and apply
     semantics without claiming to solve low-rank Sinkhorn.
4. Classify source route:
   - `source_faithful` only for operations that match cited paper/source
     operations, such as `P = Q diag(1/g) R^T`, lazy application, and anchored
     marginal diagnostics;
   - `fixed_hmc_adaptation` for frozen ranks, seeds, initialization, cost
     scaling, floors, and deterministic fixture choices that preserve a cited
     route;
   - `extension_or_invention` for a deterministic coupling construction or
     stabilization not present in the source route.
5. Confirm no NumPy/PyTorch/JAX code is promoted to a BayesFilter default.

If implementation proceeds:

1. Syntax/import checks for all new Python files.
2. Tiny fixed-factor fixture with finite transported particles and exact or
   thresholded factor/coupling marginals.
3. Phase 1 fixture diagnostic with `Q`, `R`, `g`, rank, marginal residuals,
   induced coupling residuals when materialization is tiny enough, transported
   particles, dense-reference particle delta, runtime, and memory proxy.
4. Candidate result must validate under the Phase 3 schema with
   `transport_object.kind = low_rank_coupling_factors`.
5. Hard-veto diagnostics must include finite `Q`, `R`, `g`, finite transported
   particles, nonnegative factors, strictly positive `g`, valid shapes, factor
   marginal residuals, induced row/column residuals, and explicit
   `semantic_replacement` class.
6. Dense-reference transported-particle error is explanatory only.  It is not a
   promotion criterion for this phase.

Review:

- Phase 6 is implementation-bearing.  Run local subplan checks first, then use
  Claude as read-only reviewer for the subplan or material repairs.
- Use bounded path-based review or no-file micro reviews if file review stalls.
- Claude cannot authorize phase advancement.
- Stop after five review rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a TensorFlow low-rank coupling transport object produce finite factors, valid factor/coupling marginal diagnostics, and transported particles on Phase 1 fixtures while preserving the semantic-replacement boundary? |
| Baseline/comparator | Phase 1 dense/streaming TensorFlow baseline for descriptive semantic delta; Phase 4 Nystrom and Phase 5 positive features are explanatory context only. |
| Primary pass criterion | If implementation proceeds, a Phase 3-valid candidate record exists with `low_rank_coupling_factors`, finite nonnegative `Q,R`, strictly positive `g`, finite transported particles, valid residuals under declared thresholds, and dense-reference diagnostics marked explanatory. |
| Promotion veto | Dense-reference error treated as exact parity; invalid or missing factor marginals; nonpositive `g`; negative factors; missing transported particles; wrong factor orientation; solver-route claim without anchored Dykstra/low-rank Sinkhorn operations; non-TensorFlow default route. |
| Continuation veto | Source anchors contradict planned factor convention; Phase 1 baseline missing; Phase 3 schema cannot represent low-rank coupling factors; implementation requires package installation, network fetch, GPU evidence, or non-TensorFlow default code; implementation scope cannot be chosen without user direction. |
| Repair trigger | Localized orientation, factor normalization, `g` lower bound, rank choice, cost scaling, dtype, residual threshold, or materialization-only-on-tiny-fixtures issue. |
| Explanatory diagnostics | Rank, initialization/scope, factor marginal residuals, induced coupling residuals, dense-reference particle error, runtime, memory proxy, Phase 4/5 descriptive comparison, and downstream fixture behavior if already available. |
| Not concluded | No exact dense Sinkhorn equivalence, no speedup, no ranking, no posterior correctness, no production/default readiness, no general scalability, and no low-rank Sinkhorn solver fidelity unless the `solver_route` is implemented and audited. |
| Artifact preserving result | Phase 6 implementation if any, diagnostic JSON/Markdown, tests/logs, Phase 6 result, ledger, stop handoff, and Phase 7 subplan. |

## Skeptical Plan Audit

- Wrong baseline: Phase 6 must compare descriptively against Phase 1 local
  dense/streaming baseline, not external POT/OTT demos.
- Proxy metric risk: rank, runtime, and memory proxy are explanatory until
  factor and particle validity pass.
- Missing stop conditions: stop if implementation scope cannot be chosen,
  factors cannot be oriented, or only scalar costs/losses are produced.
- Unfair comparisons: low-rank coupling is a semantic replacement and must not
  be ranked against Nystrom or positive features from one fixture.
- Hidden assumptions: rank, `g` lower bound, initialization, normalization,
  cost scaling, and target weights must be recorded.
- Stale context: Phase 4 was a full-rank Nystrom correctness probe; Phase 5 was
  a semantic-replacement positive-feature validity screen.  Neither is Phase 6
  promotion evidence.
- Environment mismatch: no package installation, no network fetch, no GPU
  evidence, no non-TensorFlow default implementation.
- Artifact adequacy: a scalar objective or loss trace is not a BayesFilter
  transport object.

Skeptical audit status: `PASSED_FOR_PHASE_6_LOW_RANK_COUPLING_PROTOTYPE_PLAN`.

## Forbidden Claims And Actions

- Do not claim speedup, ranking, production/default readiness, posterior
  correctness, exact dense Sinkhorn equivalence, or general scalability.
- Do not claim low-rank Sinkhorn solver fidelity if Phase 6 implements only a
  deterministic transport-object fixture route.
- Do not treat dense-reference particle error as a promotion criterion.
- Do not treat POT/OTT NumPy/JAX source as BayesFilter default code.
- Do not install packages, fetch network sources, or use GPU evidence.
- Do not unblock Mini-batch/BoMb.
- Do not modify unrelated dirty user work.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only after:

- Phase 6 result records a pass, non-promoted candidate result, or precise
  blocker/failure result;
- implementation and diagnostic artifacts exist, or the result explains why
  implementation stopped;
- local syntax/import/diagnostic checks pass when implementation proceeds;
- candidate JSON validates against the Phase 3 schema when implementation
  proceeds;
- semantic class, implementation scope, and source-route classification are
  recorded with anchors;
- Phase 7 exact-online/GPU reference subplan exists and has been reviewed for
  consistency, correctness, feasibility, artifact coverage, and boundary
  safety;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- implementation scope cannot be chosen without user direction;
- the route would only produce scalar losses/costs, not factors and transported
  particles;
- source anchors contradict the planned factor convention or `g` convention;
- package installation, network fetch, GPU evidence, credentials, destructive
  action, or non-TensorFlow default code would be required;
- local checks reveal a hard veto not localized to a repair trigger;
- Claude and Codex do not converge after five focused review rounds for the
  same material blocker.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 6 result/close record.
3. Draft or refresh the Phase 7 exact-online/GPU reference subplan.
4. Review the Phase 7 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
