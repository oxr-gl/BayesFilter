# P8h Phase 2 Result: Algorithm And Evidence Contract

Date: 2026-06-15

Status: `PASS_REVIEWED`

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_REVIEWED`: the design contract passed local checks and focused read-only review after repair. |
| Primary criterion | Pass: revised design states route IDs, exact implementation entry points, canonical transport convention, covariance carry, OT trigger/resampler hookup, PF-PF correction attachment, diagnostics, gradient semantics, and stop rules. |
| Veto diagnostics | Closed for Phase 2: first review found a pre-implementation ambiguity in raw OT transport-matrix orientation/normalization. The contract now requires a canonical `A[target, source]` matrix before particle/covariance carry, and focused re-review accepted the repair. The design still does not claim categorical-resampling gradients, HMC readiness, or implementation correctness. |
| Main uncertainty | Implementation may still fail finite, shape, covariance PSD, value, gradient, GPU, or HMC gates in later phases. |
| Next justified action | Launch Phase 3 implementation under its reviewed subplan, starting with skeptical audit and local CPU checks before trusted GPU smoke. |
| Not concluded | No implementation pass, value adequacy, performance conclusion, gradient correctness, GPU scaling, HMC readiness, stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, generic high-dimensional readiness, production readiness, or filter ranking. |

## Artifacts

- Design contract:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase2-ot-resampled-alg1-design-contract-2026-06-15.md`
- Phase 2 subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase2-algorithm-design-contract-subplan-2026-06-15.md`
- Phase 3 subplan to review next:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-gpu-ot-implementation-subplan-2026-06-15.md`

## Code Inspection Anchors

| Contract role | Anchor |
|---|---|
| Algorithm 1 result state | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:68` |
| Algorithm 1 time-step state | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:50` |
| Algorithm 1 runner | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:731` |
| Current PF-PF correction formula | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:819` |
| Classical covariance gather precedent | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py:1634` |
| Finite Sinkhorn result/resampler | `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py:15`, `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py:30` |
| Annealed transport result/resampler | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:15`, `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:22` |
| Historical OT dispatch wrapper | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py:162` |
| Current benchmark hard-coded no-resampling call | `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:1863` |
| P8g diagnostic gradient harness | `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:2238` |
| P8g value/tuning harness | `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:2816` |

## Checks Run

| Check | Outcome | Notes |
|---|---|---|
| `git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*` | Pass | No whitespace errors reported. |
| Code search for exact Algorithm 1, PF-PF correction, covariance gather, and OT resampler anchors | Pass | `rg` found the declared symbols/routes in the implementation and resampler files. |
| Document search for route IDs, covariance carry, PF-PF correction route, relaxed-resampling boundary, and gradient semantics | Pass | `rg` found the required boundary terms in the Phase 2 design contract. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | Dirty worktree; commit not changed by Phase 2. |
| Commands | Code/document inspection and local text checks only. |
| Environment | Local repo `/home/chakwong/BayesFilter`. |
| CPU/GPU status | GPU not used. |
| Data version | N/A. |
| Random seeds | N/A. |
| Wall time | Short interactive design-contract drafting cycle. |
| Output paths | This result and the design contract above. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase2-algorithm-design-contract-subplan-2026-06-15.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: covariance carry through a barycentric OT map
could alter the practical filter target enough that later value/gradient gates
fail. Phase 2 does not decide that question. It only makes the route explicit
enough for Phase 3 to implement and Phase 4--6 to test without silently
returning to the P8g no-resampling regression.

## Handoff

Phase 3 may proceed. This result, the design contract, and the Phase 3 subplan
passed focused read-only review. Phase 3 must implement the scalar-SV route
first and must preserve the TensorFlow/TFP backend, route IDs, covariance carry
diagnostics, transport diagnostics, canonical `A[target, source]` convention,
P8g quarantine, and PF-PF correction attachment named here.
