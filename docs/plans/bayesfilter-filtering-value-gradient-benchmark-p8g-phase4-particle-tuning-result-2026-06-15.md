# P8g-G4 Result: GPU Particle-Count Tuning Stage 0

Date: 2026-06-15

Status: `BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS`

## Phase Objective

Replace `N=8` wiring evidence with reviewed GPU particle-count evidence for the
actual scalar SV LEDH route `p8g_sv_scalar_graph`.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What particle counts are adequate for the actual-SV scalar graph LEDH value summary under the reviewed GPU path? |
| Baseline/comparator | `N=8` finite wiring evidence from P8d/P8e and G3 small-scope fixed-randomness diagnostics. |
| Primary criterion | Select the smallest passing count or emit an explicit blocker, with other rows preserved as deferred/blocked. |
| Veto diagnostics | Non-finite run; relative ESS collapse; unstable adjacent-rung mean; missing next-rung check where required; runtime blowup; blocked rows disappearing. |
| Explanatory diagnostics | Per-seed values, MC SE, ESS, runtime, adjacent deltas. |
| Not concluded | Gradient correctness, HMC readiness, full-horizon tuning adequacy, stochastic PF marginal-gradient correctness, generic high-dimensional LEDH readiness, or filter ranking. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `eae3f22fb8fe4a7740d7dc67066522303aaaf083` |
| Worktree state | Dirty; unrelated Zhao-Cui/SGQF changes preserved. |
| Device | Trusted GPU, `NVIDIA GeForce RTX 4080 SUPER` recorded by TensorFlow in run output. |
| G0 manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md` |
| G2b result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md` |
| G3 result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md` |
| G4 subplan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-subplan-2026-06-15.md` |
| Stage 0 JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.json` |
| Stage 0 CSV | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.csv` |
| Selected/blocked CSV | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-selected-blocked-2026-06-15.csv` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-result-2026-06-15.md` |

## Commands Run

Local checks:

```bash
git diff --check
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8g or particle or blocked or uncertainty"
```

Trusted GPU Stage 0:

```bash
python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-particle-tuning-stage0 --rows actual_sv --algorithms ledh_pfpf_alg1_ukf_current --route-variant p8g_sv_scalar_graph --horizons 50,200 --particles 16,32 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-selected-blocked-2026-06-15.csv
```

Implementation repair during G4:

- Added Stage 0/full particle-tuning CLI surfaces and selected/blocked CSV
  emission.
- Added focused tests for schema, deferred rows, `N=8` rejection, and blocked
  verdicts.
- Repaired the selected/blocked reducer after the first Stage 0 run exposed a
  reporting bug: multi-horizon Stage 0 duplicate particle counts were being
  summarized as `BLOCK_DPF_PARTICLE_TUNING_MISSING_NEXT_RUNG` instead of the
  actual ESS failure.
- Reran focused checks and regenerated the trusted GPU Stage 0 artifact.

## Check Results

- `git diff --check`: passed.
- `python -m py_compile ...`: passed.
- Focused pytest after reducer repair: `6 passed, 11 deselected, 2 warnings`.
- Trusted GPU Stage 0 completed and wrote JSON/CSV artifacts.

## Stage 0 Results

Scope:

- row: `zhao_cui_sv_actual_nongaussian_T1000`;
- algorithm: `ledh_pfpf_alg1_ukf_current`;
- route variant: `p8g_sv_scalar_graph`;
- horizons: `50`, `200`;
- particles: `16`, `32`;
- seeds: `81120,81121,81122,81123,81124`;
- device: trusted GPU;
- runtime budget: `1800` seconds per rung.

| Horizon | N | Finite | Runtime seconds | MC SE | Min relative ESS | Mean relative ESS | Budget |
|---:|---:|---|---:|---:|---:|---:|---|
| 50 | 16 | true | `29.798041` | `0.32002129594743906` | `0.07350442292297953` | `0.29735924870553676` | within |
| 50 | 32 | true | `30.618781` | `1.0974483362407554` | `0.03261977758968511` | `0.2071288422058431` | within |
| 200 | 16 | true | `27.731062` | `4.6451187686349344` | `0.06250000006961234` | `0.1453143556169516` | within |
| 200 | 32 | true | `27.795772` | `1.6845362342821042` | `0.031250001327425746` | `0.09192307079896037` | within |

Selected/blocked verdict:

| Row | Algorithm | Route | Verdict | Selected N | Blocker |
|---|---|---|---|---:|---|
| `zhao_cui_sv_actual_nongaussian_T1000` | `ledh_pfpf_alg1_ukf_current` | `p8g_sv_scalar_graph` | `blocked_particle_tuning_not_converged` | N/A | `BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS` |

## Gate Assessment

Decision: `BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS`.

| Criterion | Status | Evidence |
|---|---|---|
| Trusted GPU execution | Pass | Run manifest records `requested_device=gpu`, G0 manifest, and GPU tensors in per-seed outputs. |
| Finite outputs | Pass | All four Stage 0 rungs are finite. |
| Runtime budget | Pass | All rungs are below `1800` seconds. |
| `N=8` not selectable | Pass | Runner rejects candidates at or below historical `N=8`; Stage 0 used `N=16,32`. |
| MC SE gate | Mixed/explanatory | `T50,N16` and `T200,N32` have MC SE under the default absolute floor; `T200,N16` does not. This is not decisive because ESS veto fires first. |
| Relative ESS gate | Fail | All rungs have min relative ESS far below `0.25`; the best min relative ESS is about `0.0735`. |
| Selection | Blocked | No count can be selected from Stage 0. |
| Review gate | Pending | This result still requires Claude read-only result review before any next-phase launch. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Stop G4 with relative-ESS blocker | Failed; no particle count selected. | Relative ESS veto fired for every probed rung. | Whether ESS collapse is caused mainly by no-resampling route choice, too-small particle ladder, scalar-SV graph route behavior, or the Stage 0 prefix diagnostic. | Review this result, then draft a G4 repair subplan before any full-horizon tuning. The likely smallest discriminating repair is to test a reviewed resampling/state-resampling scalar-SV graph route or a larger GPU particle ladder with explicit ESS stop rules. | No tuned count, no full-horizon adequacy, no HMC readiness, no filter ranking, no evidence against LEDH as a scientific idea. |

## Post-Run Red-Team Note

Strongest alternative explanation: Stage 0 used the reviewed no-resampling
scalar-SV graph route. The low ESS may indicate that no-resampling is not a
usable tuning path at these horizons/counts, not that LEDH or GPU execution is
scientifically invalid.

What would overturn this blocker: a reviewed scalar-SV graph route with
state/covariance resampling that maintains finite outputs and improves minimum
relative ESS, or a larger particle ladder showing ESS recovery without runtime
blowup.

Weakest part of the evidence: Stage 0 is prefix-horizon diagnostic evidence,
not a full-horizon tuning result. It is strong enough to block immediate
selection of `N=16` or `N=32`, but not enough to conclude that no particle count
or resampling variant can work.

