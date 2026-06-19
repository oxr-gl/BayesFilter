# P12 Result: Agent C Low-Rank Coupling Solver Route

Date: 2026-06-18

## Status

`LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`

This is an Agent C lane result for a TensorFlow low-rank coupling solver-route
diagnostic.  It does not validate Phase 6 transport fixture files, does not
change shared contracts, and does not make default, production, posterior, HMC,
speedup, ranking, or dense Sinkhorn equivalence claims.

## Owned Artifacts

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- `tests/test_low_rank_coupling_solver_tf.py`
- `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-result-2026-06-18.md`

No Phase 6 fixture files, shared schema files, Phase 1 baseline files, shared
ledger or handoff files, Agent A Nystrom artifacts, or BayesFilter public
exports were edited by this lane.

## Source-Route Classification

| Component | Classification | Evidence boundary |
| --- | --- | --- |
| `Q diag(1/g) R^T` factor form | `source_faithful` | Anchored to the local survey notation and POT/OTT low-rank factor conventions listed in the subplan. |
| Lazy apply through low-rank factors | `source_faithful` | Uses factor apply rather than materializing the primary transport matrix. Tiny materialization is diagnostic only. |
| Factor marginal diagnostics | `source_faithful` | Records `Q`, `R`, and induced row/column residuals. |
| Dykstra-style projection | `source_faithful` for the mirrored projection structure | Mirrors the anchored POT low-rank Dykstra projection route for factor marginal enforcement. |
| Deterministic initialization, rank, floors, fixed schedules | `fixed_hmc_adaptation` | Frozen for deterministic TensorFlow diagnostics; not an HMC-readiness claim. |
| Phase 1 scaled transport adapter | `fixed_hmc_adaptation` | Preserves the existing Phase 1 particle scaling convention for local comparison. |
| Cost-nudged assignment kernel and simplified solver update | `extension_or_invention` | Useful diagnostic route only; it cannot close a full low-rank Sinkhorn solver-fidelity gap. |

Overall route classification: `extension_or_invention`, because the local
solver uses simplified deterministic initialization and a cost-nudged assignment
kernel outside the cited source route.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the Agent C TensorFlow route produce finite, nonnegative, Phase 3-valid `Q,R,g` low-rank coupling factors and transported particles on deterministic fixtures? |
| Comparator | Phase 1 dense/streaming TensorFlow baseline is used only for descriptive semantic deltas. Phase 6 fixture checks are pre-implementation context only and do not validate P12. |
| Primary pass criterion | Passed for diagnostic scope: candidate record validates, factors are finite and nonnegative, `g` is positive, transported particles are finite, factor and induced residuals are below threshold, and tiny materialized apply parity passes. |
| Promotion vetoes | None fired in the P12 diagnostic run. |
| Continuation vetoes | None fired. No shared contract change, package install, network, GPU evidence, POT/external solver execution, public export edit, or non-TensorFlow BayesFilter implementation path was used. |
| Explanatory only | Dense-reference particle deltas, runtime, memory, rank, and iteration counts. |
| Not concluded | No dense Sinkhorn equivalence, speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, or full solver-fidelity claim for extension components. |
| Preserving artifact | `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json` and this result note. |

## Fixture Results

Thresholds:

- factor and induced residual hard veto: `5.0e-3`
- tiny materialized apply parity hard veto: `1.0e-10`
- dense-reference errors: explanatory only

| Fixture | Rank | Validity | Factor residual | Induced row residual | Induced column residual | Tiny apply parity | Dense max error, explanatory |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| `tiny_manual_solver` | 3 | `PASS` | `1.144962e-07` | `5.267489e-07` | `5.724812e-07` | `2.775558e-17` | `3.783889e-01` |
| `small_batch_solver` | 3 | `PASS` | `4.448633e-08` | `2.224317e-07` | `2.181370e-07` | `1.110223e-16` | `4.657416e-01` |

Summary maxima:

- max factor marginal residual: `1.144962e-07`
- max induced row residual: `5.267489e-07`
- max induced column residual: `5.724812e-07`
- max materialized tiny apply parity: `1.110223e-16`
- max dense-reference particle error, explanatory: `4.657416e-01`
- max dense-reference RMS error, explanatory: `1.723903e-01`

## Decision Table

| Decision field | Status |
| --- | --- |
| Decision | Keep P12 as a diagnostic-only viable Agent C solver-route prototype. |
| Primary criterion | Passed on deterministic fixtures under the predeclared P12 residual and parity thresholds. |
| Veto diagnostic status | No hard vetoes or continuation vetoes fired. |
| Main uncertainty | The simplified update and cost-nudged assignment kernel are extension/invention components, so this is not full low-rank Sinkhorn solver fidelity. |
| Next justified action | Downstream review may inspect P12 as an independent low-rank-coupling route candidate, preserving all non-claims. |
| Not concluded | No production/default readiness, public API readiness, HMC readiness, posterior correctness, dense equivalence, speedup, or ranking. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for finite factors, positive `g`, finite transported particles, residual thresholds, tiny apply parity, and schema validation. |
| Statistically supported ranking | None. No stochastic comparison or uncertainty analysis was run. |
| Descriptive-only differences | Dense-reference particle deltas and runtime are descriptive only. |
| Default-readiness | Not established. |
| Next evidence needed | Source-fidelity review for any stronger solver claim, broader deterministic fixtures, and separate downstream validation before any public/default/HMC boundary. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `b4156c4b0cbfdc443440fc6df4b6044e09040abb` |
| Conda/Python | Python `3.13.13` from Anaconda |
| TensorFlow | `2.20.0` |
| Device scope | CPU scope with `CUDA_VISIBLE_DEVICES=-1` |
| GPU status | GPU intentionally hidden; TensorFlow CUDA/no-device log messages are environment noise, not GPU evidence. |
| Data version | N/A, deterministic lane-local fixtures |
| Seeds | N/A, deterministic fixture construction |
| Dtype | `tf.float64` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-subplan-2026-06-18.md` |
| Result JSON | `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json` |
| Result Markdown | `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md` |

Commands executed for P12 validation:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py tests/test_low_rank_coupling_solver_tf.py docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py
pytest -q tests/test_low_rank_coupling_solver_tf.py
python docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py --output docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json --markdown-output docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md
```

## Post-Run Red-Team Note

Strongest alternative explanation: the route may be a well-conditioned
diagnostic construction that satisfies low-rank factor marginals on tiny
fixtures without matching the full source low-rank Sinkhorn objective.

Result that would overturn this close record: a focused review showing that the
recorded `Q,R,g` convention, orientation, Dykstra projection, residuals, or
schema fields are inconsistent with the source anchors or Phase 3 transport
object contract.

Weakest evidence point: solver-fidelity remains intentionally open because the
cost-nudged assignment kernel and simplified update are classified as
`extension_or_invention`.

## 2026-06-19 Governed Replay Confirmation

The P12 visible runbook replay confirmed this diagnostic-only result under the
2026-06-19 master program:

- P12-0 governance/source-lock result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p00-governance-source-lock-result-2026-06-19.md`
- P12-1 intake result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p01-intake-artifact-baseline-result-2026-06-19.md`
- P12-2 replay result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p02-implementation-diagnostic-replay-result-2026-06-19.md`

Replay status: `P12_2_IMPLEMENTATION_DIAGNOSTIC_REPLAY_PASSED`.

Replay checks:

- CPU-only py_compile: passed.
- CPU-only unit tests: `3 passed`.
- CPU-only diagnostic replay: passed.
- hard vetoes: `[]`.
- status: `LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`.

This replay does not add any speedup, ranking, dense Sinkhorn equivalence,
posterior correctness, HMC readiness, public API readiness, or
production/default readiness claim.

## Close Record

P12 produced finite, nonnegative `Q,R,g` low-rank coupling factors and finite
transported particles on the required deterministic fixtures without changing
shared contracts or touching another lane's files.  The lane is closed as
diagnostic-only viable under `LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`.
