# P8i Phase 1 Result: Longer-Prefix Particle And Value Ladder

Date: 2026-06-16

Status: `PASS_LONGER_PREFIX_PARTICLE_VALUE_REVIEWED`

## Phase Objective

Test whether the P8h OT-resampled Algorithm 1 route can move beyond horizons
`4,8` to longer-prefix particle/value adequacy under trusted GPU execution,
without treating the result as full production tuning.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the exact P8h route remain finite, transport-valid, trusted-GPU, and adjacent-rung stable at longer prefixes `16,32` for five fixed seeds? |
| Baseline/comparator | P8h Phase 5 short-prefix `4,8` ladder and within-P8i adjacent particle rungs. |
| Primary criterion | Select a diagnostic longer-prefix count by the finite/trusted-GPU/transport/runtime/five-seed-MCSE/adjacent-rung rule, or write an explicit blocker. |
| Veto diagnostics | Nonfinite value; missing trusted GPU evidence; transport residual/covariance carry failure; runtime over budget; five-seed MC uncertainty failure; adjacent-rung instability; schema/provenance still labeled as P8h Phase 5 without P8i manifest fields. |
| Explanatory diagnostics | Runtime, ESS, MCSE, adjacent deltas, per-seed values, transport residuals. |
| Not concluded | Full-horizon adequacy, gradient correctness, HMC readiness, NUTS readiness, ranking, or default sampler policy. |

## Skeptical Audit

- Wrong-baseline check: P8h Phase 5 `N=5` is treated only as short-prefix
  context; Phase 1 re-evaluates `N=5,10,20` at horizons `16,32`.
- Proxy-metric check: ESS is explanatory only. The selection gate is finite
  values, trusted GPU, transport diagnostics, runtime, five fixed seeds, MCSE,
  and adjacent-rung stability.
- Stop-condition check: the pilot rung had to pass before the full ladder.
  No full-horizon `T=1000` run was authorized.
- Artifact-fit check: the JSON/CSV artifacts preserve route, P8i phase
  provenance, plan path, GPU device evidence, seeds, horizons, counts, wall
  time, selected/blocked record, and nonclaims.

## Fresh Trusted GPU Precheck

A trusted `nvidia-smi` precheck was run immediately before the Phase 1 ladder.
It reported an `NVIDIA GeForce RTX 4080 SUPER`, driver `591.86`, CUDA
`13.1`, and no active GPU processes. The Phase 1 JSON artifacts also record
TensorFlow physical and logical GPU devices as `/physical_device:GPU:0` and
`/device:GPU:0`.

## Actions And Checks

Pilot command:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 16 --particles 5,10 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8h-profile-manifest-phase P8I_PHASE1_LONGER_PREFIX_PARTICLE_VALUE_PILOT --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-selected-blocked-2026-06-16.csv
```

Full ladder command:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 16,32 --particles 5,10,20 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8h-profile-manifest-phase P8I_PHASE1_LONGER_PREFIX_PARTICLE_VALUE --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-selected-blocked-2026-06-16.csv
```

Local checks run after the artifacts existed:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h_ot_gradient or p8h_phase5 or p8h_hmc"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-2026-06-16.json
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-2026-06-16.json
```

Results:

- `py_compile`: passed.
- Focused pytest: `8 passed, 18 deselected, 2 warnings`.
- `git diff --check`: passed.
- Both Phase 1 JSON artifacts parse with `python -m json.tool`.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5fdd0819ce0eb2994fb0509e66d9e9cce5f2d47c` |
| Dirty state summary | Full ladder JSON records `218 git-status-short entries`; unrelated Zhao-Cui/monograph dirt remains out of scope. |
| Environment | TensorFlow/TensorFlow Probability particle profile harness. |
| CPU/GPU status | Requested trusted GPU; TensorFlow records `/physical_device:GPU:0` and `/device:GPU:0`. |
| Fresh GPU precheck | Passed; RTX 4080 SUPER visible via trusted `nvidia-smi`. |
| G0 manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md` |
| Seeds | `81120,81121,81122,81123,81124` |
| Horizons | Pilot `16`; full ladder `16,32` |
| Particle counts | Pilot `5,10`; full ladder `5,10,20` |
| Wall time | Pilot `140.275773` seconds; full ladder `610.841803` seconds. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-subplan-2026-06-16.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-result-2026-06-16.md` |

The runner flag `--p8h-particle-tuning-stage0` is a codepath selector only.
P8i provenance is carried by `phase`, `run_manifest.environment`,
`run_manifest.plan`, and P8i output paths.

## Results

| Horizon | N | Finite | Transport | Trusted GPU | Runtime seconds | MCSE | Mean log likelihood | Min relative ESS |
|---:|---:|---|---|---|---:|---:|---:|---:|
| 16 | 5 | true | true | true | `51.90346` | `0.4239197536475199` | `-8.206925764133295` | `0.3171734228962384` |
| 16 | 10 | true | true | true | `68.870002` | `0.264306830814899` | `-8.12720112559305` | `0.28129792005599485` |
| 16 | 20 | true | true | true | `101.376405` | `0.3746864787405128` | `-7.735971715346809` | `0.14412218983409492` |
| 32 | 5 | true | true | true | `71.215893` | `0.638939306310582` | `-16.271024752723953` | `0.3171734228962384` |
| 32 | 10 | true | true | true | `106.295015` | `0.2245172697039196` | `-15.725237466322332` | `0.26070678480212783` |
| 32 | 20 | true | true | true | `173.483498` | `0.27976723882837157` | `-14.495601857829389` | `0.10422568165815715` |

Selected/blocked verdict:

| Verdict | Selected N | Next rung | Horizons | Counts |
|---|---:|---:|---|---|
| `selected_particle_count` | 5 | 10 | `16,32` | `5,10,20` |

Adjacent checks for `N=5 -> N=10`:

| Horizon | Adjacent mean delta | Combined MCSE | Threshold | Pass |
|---:|---:|---:|---:|---|
| 16 | `0.07972463854024525` | `0.4995658698790277` | `1.9991317397580555` | true |
| 32 | `0.5457872864016213` | `0.6772380981190813` | `2.3544761962381626` | true |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Select `N=5` for diagnostic longer-prefix value/count gates at horizons `16,32`, pending review. | Passed the predeclared five-seed finite/trusted-GPU/transport/runtime/MCSE/adjacent-rung rule. | No Phase 1 veto fired in the pilot or full ladder. | Horizons `16,32` are still prefixes; this does not establish full-horizon adequacy or sampler validity. | Refresh Phase 2 to test gradient connectivity at `N=5`, horizons `16,32`, with P8i provenance fields. | No full-horizon adequacy, no gradient correctness beyond the future Phase 2 graph diagnostic, no HMC/NUTS readiness, no ranking, no default policy. |

## Post-Run Red-Team Note

Strongest alternative explanation: `N=5` may pass the chosen prefix gate while
still being too small for full horizon, HMC energy stability, or any generic
high-dimensional setting.

What would overturn this result: a reviewed longer-prefix or full-horizon
diagnostic showing nonfinite values, failed transport/covariance carry,
untrusted GPU fallback, runtime failure, MCSE failure, or adjacent-rung
instability at `N=5`.

Weakest part of the evidence: the gate is value/filtering only; it does not
test gradients, HMC, NUTS, or exact likelihood claims.

## Handoff

Phase 2 may proceed after read-only review accepts this result and the
refreshed Phase 2 subplan. Phase 2 must use:

- row: `actual_sv`;
- algorithm: `ledh_pfpf_alg1_ukf_current`;
- resampling route: `ot_sinkhorn_barycentric_covariance_carry`;
- coordinate: `canonical_unconstrained`;
- particle count: `5`;
- horizons: `16,32`;
- seeds: `81120,81121,81122,81123,81124`;
- trusted GPU execution.

Phase 2 must not claim exact stochastic PF marginal-gradient correctness or
HMC readiness from gradient finiteness alone.
