# P8h Phase 5 Result: Value And Filtering Tuning

Date: 2026-06-16

Status: `PASS_STAGE0_PREFIX_SELECTED_REVIEWED`

## Phase Objective

Create and run the P8h-specific trusted-GPU Stage 0 particle/value tuning
ladder for the exact OT-resampled Algorithm 1 route that passed Phase 4.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What Stage 0 prefix particle count is adequate for the OT-resampled scalar-SV route under trusted GPU execution? |
| Baseline/comparator | Phase 4 local diagnostics and within-P8h adjacent-rung comparisons for the exact route. P8g no-resampling G4 is historical context only. |
| Primary criterion | Select the smallest Stage 0 prefix count or emit explicit blocker using the predeclared finite/trusted-GPU/transport/runtime/five-seed-MCSE/adjacent-rung rule. |
| Veto diagnostics | Nonfinite values; transport residual failure; missing trusted GPU evidence; runtime budget failure; missing five-seed uncertainty; MCSE failure; adjacent-rung instability; stale P8g schema reuse. |
| Explanatory diagnostics | ESS, runtime, per-seed values. |
| Not concluded | Full-horizon particle-count adequacy, gradient correctness, GPU scaling, HMC readiness, generic high-dimensional readiness, or filter ranking. |

## Skeptical Audit

- Wrong-baseline check: the P8g G4 no-resampling blocker is historical context
  only and is not an operative comparator.
- Proxy-metric check: ESS is reported as diagnostic context and is not the sole
  pass criterion.
- Stop-condition check: the P8h-specific tuning runner and focused tests had
  to pass before any trusted GPU ladder launch.
- Artifact-fit check: the JSON/CSV artifacts preserve route, manifest,
  transport, trusted-GPU, seed, runtime, and uncertainty fields needed for the
  Phase 5 question.

## Implementation And Checks

Implemented Phase 5-specific tuning support in:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`;
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`.

Local checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h or particle or blocked or uncertainty"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*
```

Results:

- `py_compile`: passed.
- Focused pytest: `8 passed, 13 deselected, 2 warnings`.
- `git diff --check`: passed.

## Trusted GPU Run

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --horizons 4,8 --particles 5,10,20 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-stage0-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-stage0-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-selected-blocked-2026-06-16.csv
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-stage0-2026-06-16.json`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-stage0-2026-06-16.csv`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-selected-blocked-2026-06-16.csv`.

Run manifest highlights:

| Field | Value |
|---|---|
| Git commit | `5fdd0819ce0eb2994fb0509e66d9e9cce5f2d47c` |
| Device | Trusted GPU; TensorFlow recorded `/device:GPU:0` |
| G0 manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md` |
| Seeds | `81120,81121,81122,81123,81124` |
| Horizons | `4,8` |
| Particles | `5,10,20` |
| Wall time | `335.076978` seconds |

Programmatic JSON/CSV validation passed.

## Stage 0 Results

| Horizon | N | Finite | Transport | Trusted GPU | Runtime seconds | MCSE | Mean log likelihood | Min relative ESS |
|---:|---:|---|---|---|---:|---:|---:|---:|
| 4 | 5 | true | true | true | `37.890096` | `0.12193456145119645` | `-2.5683584481630004` | `0.8038143813839937` |
| 4 | 10 | true | true | true | `41.98124` | `0.08867057298002864` | `-2.6810565676304408` | `0.7544068195810831` |
| 4 | 20 | true | true | true | `50.778277` | `0.07282043876490764` | `-2.750720037539467` | `0.8296134638275836` |
| 8 | 5 | true | true | true | `42.846304` | `0.5092899481855204` | `-4.634369087625792` | `0.40324545666386885` |
| 8 | 10 | true | true | true | `51.921047` | `0.34975722827069927` | `-4.928059070994341` | `0.44278208320912543` |
| 8 | 20 | true | true | true | `70.376854` | `0.23170144037339388` | `-5.028074890384251` | `0.4297295225132133` |

Selected/blocked verdict:

| Row | Algorithm | Route | Verdict | Selected N | Next rung | Blocker |
|---|---|---|---|---:|---:|---|
| `zhao_cui_sv_actual_nongaussian_T1000` | `ledh_pfpf_alg1_ukf_current` | `ot_sinkhorn_barycentric_covariance_carry` | `selected_particle_count` | 5 | 10 | N/A |

Adjacent-rung checks for `N=5 -> N=10`:

| Horizon | Adjacent mean delta | Combined MCSE | Threshold | Pass |
|---:|---:|---:|---:|---|
| 4 | `0.11269811946744035` | `0.15076640139269157` | `1.3015328027853832` | true |
| 8 | `0.2936899833685489` | `0.617823898898717` | `2.235647797797434` | true |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Select `N=5` for P8h Stage 0 prefix diagnostics, pending review | Passed the predeclared Stage 0 rule. | No Phase 5 veto fired in the Stage 0 artifact. | The selected count is prefix-only and may not be adequate for full horizon or HMC. | Review this result and refresh Phase 6 to use `N=5` for OT-gradient checks, while preserving that Phase 7/8 require their own gates. | No full-horizon adequacy, no gradient correctness, no GPU scaling, no HMC readiness, no final filter ranking. |

## Post-Run Red-Team Note

Strongest alternative explanation: the Stage 0 horizons are short enough that
`N=5` can look stable while longer horizons still require larger particle
counts or fail runtime/transport stability.

What would overturn this decision: a reviewed full-horizon or longer-prefix
ladder showing nonfinite values, transport failures, unstable adjacent rungs,
or unacceptable runtime at `N=5`.

Weakest part of the evidence: Stage 0 uses only horizons `4` and `8`.
Therefore this result may feed Phase 6 gradient checks at `N=5`, but it must
not be treated as full-horizon adequacy or HMC readiness.

## Handoff

Proceed to Phase 6 only after read-only review accepts this result and the
refreshed Phase 6 subplan. Phase 6 should check gradients for the exact route
`ot_sinkhorn_barycentric_covariance_carry` at the selected Stage 0 count
`N=5`, and must not claim stochastic PF marginal-gradient correctness or HMC
readiness from gradient finiteness alone.
