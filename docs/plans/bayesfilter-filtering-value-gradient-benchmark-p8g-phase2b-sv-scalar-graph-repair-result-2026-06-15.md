# P8g-G2b Result: SV Scalar Graph Repair For Algorithm 1

Date: 2026-06-15

Status: `PASS_P8G_G2B_SV_SCALAR_GRAPH_FEASIBILITY_REVIEWED`

## Phase Objective

Repair the reviewed G2 speed blocker for the actual scalar stochastic-volatility
LEDH row by adding a distinct TensorFlow graph/GPU route while preserving the
generic Algorithm 1 route as the correctness reference.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the reviewed G2 speed blocker be repaired for the actual SV LEDH row by moving the scalar Algorithm 1 time loop and particle computation into TensorFlow graph operations? |
| Baseline/comparator | G1/G2 generic Algorithm 1 route on `zhao_cui_sv_actual_nongaussian_T1000`, same horizon, particles, and seeds. |
| Primary criterion | Graph route preserves value parity, records a distinct scalar-SV graph route variant, and meets the `5x`/`30` minute feasibility gate or records a reviewed blocker. |
| Veto diagnostics | Non-finite values, silent CPU fallback in GPU run, value parity failure, Python/eager time loop in serious graph route, missing route label, or speed below the G1/G2 feasibility gate. |
| Explanatory diagnostics | Tiny cold-compile smoke speed, feasibility-scale prefix speed, device placement, MC-SE, and route identifiers. |
| Not concluded | Tuned particle counts, gradient correctness, HMC readiness, full filter ranking, or generic high-dimensional Algorithm 1 performance. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `eae3f22fb8fe4a7740d7dc67066522303aaaf083` |
| Worktree state | Dirty before/during G2b; unrelated Zhao-Cui/SGQF changes preserved. |
| G0 manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md` |
| G1 result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md` |
| G2 blocker result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md` |
| G2b subplan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-subplan-2026-06-15.md` |
| CPU smoke JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-smoke-cpu-2026-06-15.json` |
| GPU tiny smoke JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-smoke-gpu-2026-06-15.json` |
| GPU feasibility JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-prefix50-5seed-gpu-2026-06-15.json` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md` |
| Row/algorithm | `zhao_cui_sv_actual_nongaussian_T1000`, `ledh_pfpf_alg1_ukf_current` |
| Graph route | `p8g_sv_scalar_graph` |

## Code Changes

- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
  - added `run_ledh_pfpf_alg1_scalar_sv_graph_tf(...)`;
  - added a deterministic XLA-compiled scalar-SV graph kernel using
    `tf.while_loop` for the time loop and vector TensorFlow operations for
    particles;
  - precomputes reference stateless random draws outside XLA, because XLA
    stateless RNG changes the stream relative to the reviewed generic route.
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
  - added `--p8g-sv-scalar-graph`;
  - records `sv_scalar_graph` and route variant `p8g_sv_scalar_graph`;
  - rejects combining `--p8g-sv-scalar-graph` with
    `--p8g-vectorized-particles`.
- Tests:
  - direct scalar graph versus generic looped reference parity;
  - P8g profile payload route-label and guardrail coverage.

## Commands Run

Local checks:

```bash
git diff --check
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sv_scalar_graph or p8g_profile"
```

Trusted GPU and CPU profiles:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 10 --particles 32 --seeds 81120 --device cpu --p8g-sv-scalar-graph --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-smoke-cpu-2026-06-15.json

MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 10 --particles 32 --seeds 81120 --device gpu --p8g-sv-scalar-graph --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-smoke-gpu-2026-06-15.json

MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 50 --particles 32 --seeds 81120,81121,81122,81123,81124 --device gpu --p8g-sv-scalar-graph --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-prefix50-5seed-gpu-2026-06-15.json
```

## Local Check Results

- `git diff --check`: passed.
- `python -m py_compile ...`: passed.
- Focused CPU-hidden pytest: `2 passed, 27 deselected, 2 warnings`.

## Smoke And Feasibility Results

| Metric | G2 looped GPU tiny | G2 vectorized GPU tiny | G2b scalar graph GPU tiny | G1 looped GPU T50/5seed | G2b scalar graph GPU T50/5seed |
|---|---:|---:|---:|---:|---:|
| Route variant | `current_looped_particles` | `p8g_vectorized_particles` | `p8g_sv_scalar_graph` | current generic route | `p8g_sv_scalar_graph` |
| Horizon/seeds/particles | `10/1/32` | `10/1/32` | `10/1/32` | `50/5/32` | `50/5/32` |
| Wall seconds | `20.262948` | `11.332614` | `7.018199` | `338.817931` | `31.904669` |
| Seconds per seed-time-particle | `0.063321712` | `0.035414418` | `0.021931871` | `0.042352241` | `0.003988084` |
| Mean log likelihood | `-7.82682759136567` | `-7.82682759136567` | `-7.82682759136567` | `-33.056354679226786` | `-33.05635467922677` |
| Tensor placement | GPU | GPU | GPU | GPU | GPU |

Computed gate diagnostics:

- Tiny cold-compile graph speedup versus G2 looped GPU: about `2.89x`.
- Feasibility-scale graph speedup versus G1 looped GPU: about `10.62x`.
- Linear projection from T50/5seed graph run to T1000/5seed: about `638.09`
  seconds, or `10.63` minutes.
- G2b graph T50 value minus G1 looped GPU T50 value: about `1.42e-14`.

## Gate Assessment

Decision: `PASS_P8G_G2B_SV_SCALAR_GRAPH_FEASIBILITY_REVIEWED`.

| Criterion | Status | Evidence |
|---|---|---|
| CPU/reference parity | Pass | Focused tests and CPU/GPU profile values match the generic reference to floating precision. |
| Finite values/ESS/covariances | Pass | All smoke/profile artifacts are `executed_p8g_prefix_profile` and focused tests pass. |
| Real GPU placement | Pass | GPU artifacts record `/device:GPU:0` result tensors and no silent CPU fallback. |
| Distinct route label | Pass | Payload records `p8g_sv_scalar_graph`; route identifiers record `graph_specialization_route`, `time_loop_route`, and `particle_batch_route`. |
| Serious time loop not Python/eager | Pass | Graph route records `time_loop_route=tf_while_loop`; only the harness seed loop remains Python. |
| G1/G2 feasibility gate | Pass at feasibility scale | T50/5seed graph route is about `10.62x` faster than the G1 looped GPU profile and projects under the `30` minute full-horizon budget. |
| Tiny cold-compile speed | Explanatory caveat | T10/1seed cold graph run is only about `2.89x` faster than G2 looped GPU because XLA compile/startup dominates. |
| Review gate | Pass | Claude read-only result review returned `VERDICT: AGREE` with one minor non-blocking note about the inherited JSON `phase` label. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Mark G2b as reviewed pass | Passed at G1 feasibility scale, despite tiny cold-compile caveat. | No parity, finiteness, GPU placement, route-label, or time-loop veto remains. | Whether the scalar-SV specialization is sufficient for the next fixed-randomness gradient phase without overgeneralizing beyond SV. | Refresh G3 subplan with scalar-SV graph entry conditions before any gradient work. | No tuned particle count, no gradient correctness, no HMC readiness, no generic high-dimensional GPU implementation, no filter ranking. |

## Post-Run Red Team Note

Strongest alternative explanation: the feasibility pass relies on the scalar SV
closed-form specialization and amortized XLA compilation; it does not imply the
generic Algorithm 1 path is fast or high-dimensional-ready.

What would overturn this result: a reviewed parity bug in the scalar equations,
evidence that the graph path silently changed the random stream or target
correction, or a failed result review showing the T50 feasibility comparison is
not the intended G1/G2 gate.

Weakest part of the evidence: tiny cold-start smoke remains below `5x`, so the
speed claim should be tied to feasibility-scale runs, not one-seed smoke timing.

## Next-Phase Handoff

G3 may proceed only through the refreshed G3 subplan, scoped initially to the
actual scalar SV row and the reviewed `p8g_sv_scalar_graph` route.
