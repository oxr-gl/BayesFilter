# Phase 6 Result: Low-Rank Coupling Prototype

Date: 2026-06-17
Close timestamp: 2026-06-18T03:39:48+08:00

## Status

`PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED`

## Phase Objective

Implement a TensorFlow low-rank coupling transport-object prototype that
exposes `Q`, `R`, `g`, a lazy application route, marginal diagnostics, and
transported particles under the Phase 3 schema.

This phase used the declared `transport_object_fixture_route`.  It validates
the BayesFilter transport object and factor application for
`P = Q diag(1/g) R^T`, but it does not claim to solve low-rank Sinkhorn, does
not claim dense Sinkhorn equivalence, and does not establish speedup,
scalability, posterior validity, or default readiness.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can a TensorFlow low-rank coupling transport object produce finite factors, valid factor/coupling marginal diagnostics, and transported particles on Phase 1 fixtures while preserving the semantic-replacement boundary? |
| Baseline/comparator | Phase 1 local TensorFlow dense/streaming baseline for descriptive semantic delta only. |
| Primary criterion | Passed for the declared transport-object fixture route.  Candidate JSON validates under the Phase 3 schema, finite nonnegative `Q,R`, strictly positive `g`, finite transported particles, valid residuals, and dense-reference diagnostics marked explanatory were recorded. |
| Veto diagnostics | No hard veto fired.  Hard vetoes `[]`. |
| Explanatory diagnostics | Rank, implementation scope, source-route components, factor marginal residuals, induced row/column residuals, dense-reference particle deltas, materialized tiny checks, runtime fields, and non-claims were recorded. |
| Not concluded | No exact dense Sinkhorn equivalence, no low-rank Sinkhorn solver fidelity, no speedup, no ranking, no posterior correctness, no production/default readiness, and no general scalability claim. |
| Artifact preserving result | Implementation file, unit test, diagnostic script, JSON/Markdown diagnostics, this result, ledger, stop handoff, and Phase 7 subplan. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `7c92eaba6e260973a8af1c54df0d2d3efa4dc150` |
| Timestamp | `2026-06-18T03:39:48+08:00` |
| Environment | CPU-scope TensorFlow diagnostic; `CUDA_VISIBLE_DEVICES=-1`; no package installation; no network; no GPU evidence. |
| Python | `Python 3.13.13` |
| TensorFlow | recorded in diagnostic JSON manifest |
| Plan path | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-subplan-2026-06-17.md` |
| Result path | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-result-2026-06-17.md` |
| Implementation | `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_transport_tf.py` |
| Unit test | `tests/test_low_rank_coupling_transport_tf.py` |
| Diagnostic script | `docs/benchmarks/scalable_ot_p06_low_rank_coupling_prototype_diagnostics.py` |
| Diagnostic JSON | `docs/benchmarks/scalable-ot-p06-low-rank-coupling-prototype-diagnostics-2026-06-17.json` |
| Diagnostic Markdown | `docs/benchmarks/scalable-ot-p06-low-rank-coupling-prototype-diagnostics-2026-06-17.md` |

## Commands And Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Syntax check | `PASS` | `python -m py_compile docs/benchmarks/scalable_ot_p06_low_rank_coupling_prototype_diagnostics.py experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_transport_tf.py tests/test_low_rank_coupling_transport_tf.py` |
| Focused unit test | `PASS` | `pytest -q tests/test_low_rank_coupling_transport_tf.py`: `2 passed` |
| Diagnostic smoke on `/tmp` | `PASS` | Wrote `/tmp/scalable-ot-p06-low-rank-coupling-prototype-diagnostics-smoke.json` and `.md`; status `PASS`. |
| Official diagnostic | `PASS` | `python docs/benchmarks/scalable_ot_p06_low_rank_coupling_prototype_diagnostics.py --output docs/benchmarks/scalable-ot-p06-low-rank-coupling-prototype-diagnostics-2026-06-17.json --markdown-output docs/benchmarks/scalable-ot-p06-low-rank-coupling-prototype-diagnostics-2026-06-17.md` |
| Phase 3 schema validation | `PASS` | `validate_candidate_result(data['candidate_record'])` succeeded inside the diagnostic script. |

The diagnostic command emitted a TensorFlow CUDA initialization warning even
though `CUDA_VISIBLE_DEVICES=-1` was set.  This is recorded as environment
noise, not GPU evidence.

## Diagnostic Summary

| Metric | Value |
| --- | ---: |
| Phase 6 status | `PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED` |
| Status | `PASS` |
| Semantic class | `semantic_replacement` |
| Implementation scope | `transport_object_fixture_route` |
| Validity pass | `True` |
| Hard vetoes | `[]` |
| Max factor marginal residual | `8.981518210115363e-06` |
| Max induced row residual | `0.00037098044636496574` |
| Max induced column residual | `0.0005748171654471612` |
| Max dense-reference particle error, explanatory | `0.0988415860043588` |
| Max dense-reference RMS error, explanatory | `0.04010294568295044` |

## Fixture Results

| Fixture | Rank | Valid | Factor residual | Row residual | Column residual | Max dense error, explanatory | RMS dense error, explanatory |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| `tiny_manual` | 4 | `True` | `6.969942e-06` | `2.657128e-05` | `4.181965e-05` | `9.884159e-02` | `4.010295e-02` |
| `small_parity` | 4 | `True` | `8.056853e-06` | `1.199952e-04` | `1.289097e-04` | `8.689544e-02` | `3.555603e-02` |
| `high_dim_low_rank` | 4 | `True` | `5.796569e-06` | `3.709804e-04` | `1.312180e-04` | `7.290280e-02` | `2.352029e-02` |
| `high_dim_locality` | 4 | `True` | `8.981518e-06` | `3.008620e-04` | `5.748172e-04` | `6.560401e-02` | `2.594369e-02` |

Tiny materialized checks for `tiny_manual` and `small_parity` confirmed that
the nonmaterialized low-rank application matched materialized matrix
application to floating-point tolerance.

## Source-Route Classification

| Operation | Classification | Evidence |
| --- | --- | --- |
| Factored coupling `P = Q diag(1/g) R^T` | `source_faithful` | Local survey equations `eq:factored-coupling` and `eq:factored-transport`; POT/OTT source anchors. |
| Lazy low-rank apply | `source_faithful` | POT `get_lowrank_lazytensor` and OTT `LRSinkhornOutput.apply` source anchors. |
| Factor marginal diagnostics | `source_faithful` | OTT `solution_error` marginal-deviation route. |
| Phase-1 scaled transport adapter | `fixed_hmc_adaptation` | Required because the Phase 1 comparator uses row sums equal to one and column target `N * weights`. |
| Deterministic latent assignment factors | `extension_or_invention` | Chosen fixture route to validate a BayesFilter transport object without claiming solver fidelity. |

The whole prototype is therefore classified as `extension_or_invention` under
the Phase 3 schema, with semantic class `semantic_replacement` and
implementation scope `transport_object_fixture_route`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED` | Passed for finite low-rank factors, transported particles, residual checks, materialized tiny parity, and Phase 3 schema validation. | No hard veto fired. | This is not a low-rank Sinkhorn solver; it does not optimize the low-rank OT objective or certify rank sufficiency. | Draft Phase 7 exact-online/GPU reference subplan and preserve a true solver-route port as a separate future phase or repair ladder. | No dense equivalence, no solver fidelity, no speedup, no ranking, no posterior/default readiness. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for semantic-replacement transport-object fixture validity on deterministic Phase 1 fixtures. |
| Statistically supported ranking | None; no multi-seed or uncertainty-aware comparison was run. |
| Descriptive-only differences | Dense-reference particle errors and runtime fields are descriptive only. |
| Default-readiness | Not assessed and not claimed. |
| Next evidence needed | Exact online/GPU reference study, sparse/localized diagnostics, sliced/subspace lane, and later comparative decision under separate reviewed subplans. |

## Post-Run Red Team

Strongest alternative explanation: the fixture route passes because it
constructs easily scaled factors, but those factors may not solve a useful
low-rank OT optimization problem.  The result validates the transport object,
not the low-rank Sinkhorn algorithm.

What would overturn this phase decision: a replay finds the candidate record no
longer validates, materialized tiny parity fails, factor residuals exceed the
declared threshold, or a source audit shows the factor/apply route was
misclassified.

Weakest evidence link: the deterministic latent assignment factors are an
extension/invention.  A true `solver_route` would need a separate TensorFlow
port of the anchored low-rank Sinkhorn/Dykstra route.

## Exact Phase 7 Handoff

Phase 7 may begin after this result because:

- this result records
  `PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED`;
- implementation and diagnostic artifacts exist;
- syntax/import, focused unit tests, official diagnostics, and schema
  validation passed;
- semantic class, implementation scope, and source-route classification are
  recorded with anchors;
- dense-reference transported-particle errors are recorded as explanatory only;
- Phase 7 exact-online/GPU reference subplan exists and has been locally
  reviewed;
- no human-required stop condition is active for Phase 7 planning.
