# P8g-G2b Subplan: SV Scalar Graph Repair For Algorithm 1

Date: 2026-06-15

Status: `READY_FOR_G2B_SV_SCALAR_GRAPH_REPAIR_REVIEW`

## Phase Objective

Repair the reviewed G2 speed blocker by adding a TensorFlow graph/GPU route for
the actual scalar stochastic-volatility LEDH row used by the P8g gate, while
preserving the generic Algorithm 1 reference route as the correctness baseline.

## Entry Conditions

- G0 trusted GPU probe passed and was reviewed:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md`.
- G1 profile passed and recorded the `30` minute/full-horizon feasibility budget:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md`.
- G2 parity/GPU placement passed but speed feasibility failed:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md`.
- The P8g stop handoff blocks G3/G4/G6 until G2 is repaired or the user changes
  the gate:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-stop-handoff-2026-06-15.md`.

## Required Artifacts

- Code changes:
  - `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
  - `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
  - focused tests in `tests/test_ledh_pfpf_alg1_ukf_tf.py` and
    `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- A distinct opt-in route flag, payload field, and route variant label for the
  scalar-SV graph repair, separate from the existing G2
  `p8g_vectorized_particles` route.
- Smoke JSONs:
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-smoke-gpu-2026-06-15.json`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-smoke-cpu-2026-06-15.json`
  - optionally a focused looped comparator JSON if the G2 comparator cannot be
    reused directly.
- Result:
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md`
- Ledger and handoff updates:
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-execution-ledger-2026-06-15.md`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-stop-handoff-2026-06-15.md`

## Required Checks/Tests/Reviews

- `git diff --check`
- `python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- CPU-hidden focused tests:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sv_scalar_graph or p8g_profile"`
- Trusted GPU smoke for the graph route on the same actual SV prefix/scope used
  in G2 unless a focused implementation failure requires a smaller diagnostic.
- Claude read-only review of the G2b subplan before implementation and of the
  G2b result before any handoff.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the reviewed G2 speed blocker be repaired for the actual SV LEDH row by moving the scalar Algorithm 1 time loop and particle computation into TensorFlow graph operations? |
| Baseline/comparator | Generic looped/vectorized Algorithm 1 route from G2 on `zhao_cui_sv_actual_nongaussian_T1000`, same horizon, particles, and seeds. |
| Primary criterion | Short-horizon graph route preserves value parity with the G2 looped/vectorized reference, records a distinct scalar-SV graph route variant, and achieves at least `5x` speedup over the G2 GPU looped comparator, or records a reviewed blocker. |
| Veto diagnostics | Non-finite values, silent CPU fallback in GPU run, value parity failure beyond tolerance, Python particle loop in the scalar-SV graph route, surviving Python/eager time loop in the scalar-SV graph route, missing distinct graph-route payload/schema label, or speed below the G1/G2 feasibility gate. |
| Explanatory diagnostics | Cold/warm graph timing if available, tensor device placement, seconds per seed-time-particle, compile/retrace warnings, and route identifiers. |
| Not concluded | Tuned particle counts, gradient correctness, HMC readiness, full filter ranking, or generic high-dimensional Algorithm 1 performance. |

## Skeptical Repair Audit

- Wrong baseline risk: controlled by comparing against the already recorded G2
  looped/vectorized SV scope rather than a new easier row.
- Proxy metric risk: graph compilation, placement, and small smoke speed are not
  promotion by themselves; parity and the G1/G2 speed gate remain binding.
- Missing stop risk: if parity, finiteness, GPU placement, or speed fails, write
  a G2b blocker result and do not advance to G3/G4/G6.
- Unfair comparison risk: use the same actual SV row, same prefix horizon,
  same particle count, same seed list, and same raw target density correction.
- Hidden assumption risk: the repair is intentionally scalar-SV-specific. It
  must not be described as a generic high-dimensional GPU implementation.
- Route ambiguity risk: controlled by requiring a separate graph-route flag,
  route variant, and result label rather than reusing the G2
  `p8g_vectorized_particles` label.
- Time-loop risk: controlled by requiring the scalar-SV repair to move the
  benchmark time loop into a TensorFlow graph path, with any remaining Python
  loops recorded as harness-only orchestration rather than serious filter work.
- Environment mismatch risk: CPU checks intentionally hide CUDA; GPU smokes use
  the trusted/escalated GPU policy.
- Artifact-answer risk: JSONs and the result file must record route variant,
  devices, value parity, timing, and nonclaims.

Audit disposition: `PASS_G2B_REPAIR_AUDIT_READY_FOR_READONLY_REVIEW`.

## Forbidden Claims/Actions

- Do not claim a generic high-dimensional LEDH GPU implementation from the
  scalar SV graph route.
- Do not label the scalar-SV graph route as the existing generic vectorized
  particle route.
- Do not change the SV model, target observation density, flow surrogate
  observation, seed schedule, or likelihood correction to improve speed/parity.
- Do not advance to particle tuning, gradients, or HMC unless G2b closes the
  reviewed G2 blocker.
- Do not use Claude as execution authority or approval authority.

## Exact Next-Phase Handoff Conditions

G2b may hand off to G3 only if:

- CPU-hidden tests pass;
- trusted GPU graph smoke is finite and uses GPU tensors;
- the payload records the scalar-SV graph route with a distinct route variant
  label;
- the scalar-SV graph route has no Python/eager time loop inside the serious
  filter computation;
- graph value parity with the G2 reference is within recorded tolerance;
- graph speed meets the `5x`/feasibility gate or has a reviewed exception
  explicitly approved by the user;
- Claude read-only result review returns no material blocker;
- the ledger and stop handoff are updated visibly.

## Stop Conditions

- The scalar graph route cannot be made finite without changing the target or
  seed schedule.
- CPU/GPU or graph/reference parity fails beyond tolerance.
- The graph route still cannot meet the speed/feasibility gate.
- Claude review identifies a material blocker that does not converge within
  five focused rounds.
