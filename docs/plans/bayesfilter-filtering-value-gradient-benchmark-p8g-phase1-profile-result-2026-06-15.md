# P8g-G1 Result: Current Bottleneck Profile

Date: 2026-06-15

Status: `PASS_PROFILE_VECTOR_TARGET_IDENTIFIED_REVIEWED`

## Phase Objective

Profile the current repaired P8d LEDH path to identify whether a GPU
vectorization route is admissible and where the Python particle/time loops
dominate.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there a concrete batched TensorFlow rewrite target that can plausibly make P8g GPU execution useful? |
| Baseline/comparator | Current CPU reference and trusted GPU profile of the existing implementation. |
| Primary criterion | Identify vectorizable hotspots and project feasibility for at least five-seed full-horizon `N=32` LEDH SV-style gate within a recorded budget. |
| Veto diagnostics | Serious route still dominated by unvectorizable Python loops; silent CPU fallback; profile does not cite G0 manifest; profile commands do not answer bottleneck question. |
| Explanatory diagnostics | Time by phase, device placement, loop counts, op placement, memory observations. |
| Not concluded | GPU implementation correctness or speedup after rewrite. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `eae3f22fb8fe4a7740d7dc67066522303aaaf083` |
| Worktree state | Dirty before/during G1; unrelated Zhao-Cui/SGQF work and P8g planning/result artifacts were preserved. |
| G0 manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md` |
| CPU profile JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-cpu-2026-06-15.json` |
| GPU profile JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-gpu-2026-06-15.json` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md` |
| Python/TensorFlow environment | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python`, TensorFlow/TFP profile harness |
| CPU/GPU status | CPU profile deliberately hid GPU; GPU profile used trusted GPU execution and recorded `/device:GPU:0` tensors. |
| Seeds | `81120,81121,81122,81123,81124` |
| Row/algorithm | `zhao_cui_sv_actual_nongaussian_T1000`, `ledh_pfpf_alg1_ukf_current` |
| Horizon/particles | prefix horizon `50`, particles `32` |

## Commands Run

Local checks and focused tests:

```bash
git diff --check
python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8g_profile or ledh_sv_style_short_cells"
```

CPU profile:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 50 --particles 32 --seeds 81120,81121,81122,81123,81124 --device cpu --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-cpu-2026-06-15.json
```

Trusted GPU profile:

```bash
MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row zhao_cui_sv_actual_nongaussian_T1000 --algorithm ledh_pfpf_alg1_ukf_current --horizon 50 --particles 32 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-gpu-2026-06-15.json
```

## Local Check Results

- `git diff --check`: passed.
- `python -m py_compile ...`: passed.
- Focused pytest: `3 passed, 9 deselected, 2 warnings`.

## Profile Results

| Metric | CPU profile | Trusted GPU profile |
|---|---:|---:|
| Status | `executed_p8g_prefix_profile` | `executed_p8g_prefix_profile` |
| Wall seconds | `84.068564` | `338.817931` |
| Mean seed runtime seconds | `16.811629` | `67.760382` |
| Seconds per seed-time-particle | `0.010508571` | `0.042352241` |
| GPU/CPU wall-time ratio | N/A | `4.030257` |
| Mean log likelihood | `-33.05635467922677` | `-33.056354679226786` |
| CPU/GPU mean delta | N/A | `-1.4210854715202004e-14` |
| Result tensor devices | `/device:CPU:0` | `/device:GPU:0` |
| Silent CPU fallback? | N/A | No; result tensors recorded GPU devices. |

The trusted GPU profile is numerically matched to the CPU profile for this
prefix row/seed/particle contract, but it is much slower than CPU in the
current eager/Python-loop route. This is not a GPU speedup claim. It is direct
evidence that the current route is unsuitable as the serious GPU implementation
and that G2 must vectorize the Algorithm 1 core.

## Bottleneck Diagnosis

The G1 profile harness records these known Python/eager bottlenecks:

- outer Python seed loop in the profile harness;
- current TensorFlow filter implementation iterates over time in Python/eager
  mode;
- current Algorithm 1 LEDH implementation iterates over particles for
  per-particle UKF/flow state.

The first vectorization targets for G2 are:

1. batch the per-particle Algorithm 1 UKF predict/update operations;
2. move per-time particle transforms into TensorFlow graph kernels;
3. keep five-seed orchestration outside the serious GPU kernel until the G2/G4
   route is vectorized.

## Feasibility Projection And Budget

Recorded minimum G2 feasibility budget:

- contract: one LEDH SV-style full-horizon row, five fixed seeds, `N=32`;
- wall-time budget after G2 vectorization: projected full-horizon wall time
  must be at most `30` minutes for this single-row gate, or G2 must emit a
  reviewed feasibility blocker;
- this is only a minimum engineering admissibility budget, not a production
  real-life usefulness claim.

Linear projection from the measured prefix profile:

| Route | Prefix wall seconds | Linear full-horizon multiplier | Projected full-horizon wall time |
|---|---:|---:|---:|
| Current CPU route | `84.068564` | `20` | `1681.37128` seconds, about `28.02` minutes |
| Current trusted GPU route | `338.817931` | `20` | `6776.35862` seconds, about `112.94` minutes |
| G2 minimum 5x speedup target vs current GPU route | N/A | N/A | about `22.59` minutes |

Interpretation:

- the current trusted GPU route fails the recorded budget and is not an
  acceptable serious GPU implementation;
- the G1 pass is not a runtime pass for the current route;
- G1 only passes the handoff criterion because it identifies concrete
  vectorization targets whose G2 minimum speedup gate would project under the
  recorded budget;
- if G2 cannot remove enough Python/eager work to reach at least the 5x
  measured-speedup target or another reviewed feasible exception, G2 must block
  rather than continue to tuning or gradients.

## Gate Assessment

Decision: `PASS_PROFILE_VECTOR_TARGET_IDENTIFIED_REVIEWED`.

| Criterion | Status | Evidence |
|---|---|---|
| G0 manifest cited | Pass | GPU profile command and JSON cite the G0 result artifact. |
| CPU reference profile executed | Pass | CPU profile completed with GPU hidden and CPU tensor devices. |
| Trusted GPU profile executed | Pass | GPU profile completed in trusted context with GPU tensor devices. |
| No silent CPU fallback | Pass | GPU JSON records `/device:GPU:0` for log likelihood, ESS, and filtered means. |
| Numerical CPU/GPU parity | Pass | Mean log-likelihood delta is about `1.42e-14` for the same prefix contract. |
| Current serious GPU route acceptable as-is | Fail/explanatory | GPU is about `4.03x` slower than CPU because Python/eager loops dominate. |
| Concrete vectorization target | Pass | G2 target is batched per-particle Algorithm 1 UKF/flow and time-loop graphing. |
| Full-horizon feasibility projection | Pass for handoff target only | Current GPU projects to about `112.94` minutes and fails the `30` minute budget; the G2 target must deliver at least 5x speedup or a reviewed feasible exception, which would project to about `22.59` minutes. |
| Review gate | Pass | Claude read-only review round 2 returned `VERDICT: AGREE` and is recorded in the canonical review ledger. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass G1 as vectorization-target identification after review | Passed: G1 found concrete vectorization targets, recorded a full-horizon budget/projection, and demonstrated the current route is not a serious GPU path. | No silent fallback; no nonfinite result; no profile/artifact mismatch. The slow trusted GPU route is not promoted; it is a G2 repair target. | Actual batched GPU implementation may still fail parity, finiteness, or the `30` minute projected full-horizon budget in G2. | Execute G2 vectorized Algorithm 1 core subplan. | No post-rewrite speedup, no full-horizon tuning adequacy, no gradient correctness, no HMC readiness, no callback closure, no filter ranking. |

## Next-Phase Handoff

G1 handoff conditions are met:

1. Claude read-only review of this G1 result converged with `VERDICT: AGREE`;
2. the review is recorded in
   `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-execution-ledger-2026-06-15.md`;
3. this result status is
   `PASS_PROFILE_VECTOR_TARGET_IDENTIFIED_REVIEWED`;
4. G2 cites the vectorization target and the `30` minute projected
   full-horizon budget above.

No G2 implementation, G4 tuning, or G6 HMC command is launched by this result.
