# Phase 0 Result: Inventory And Boundary Audit

Date: 2026-06-14

## Status

`PASSED_WITH_REVIEWED_HANDOFF_TO_PHASE_1`

## Phase Objective

Confirm the current state of the batched filtering experimental work, record
the dirty-worktree boundary, verify master/runbook consistency, and prepare the
Phase 1 correctness-stabilization subplan.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | The visible gated program, runbook, and Phase 0 boundary are coherent enough to start correctness stabilization. |
| Baseline/comparator | Existing scalar production APIs remain the comparator; current experimental artifacts were revalidated as baseline evidence. |
| Primary criterion | Passed: local checks passed, Claude converged with `VERDICT: AGREE`, and this result records the boundary and handoff. |
| Veto diagnostics | No veto fired. |
| Explanatory diagnostics | Dirty worktree, artifact inventory, environment version, and smoke-test warnings are recorded as context only. |
| Not concluded | No production readiness, no default change, no broad nonlinear correctness claim, no GPU performance conclusion, no HMC/NeuTra integration claim. |

## Local Checks Actually Run

| Check | Command summary | Result |
| --- | --- | --- |
| Required headings | `rg -n "^## ..."` over master, runbook, Phase 0 subplan | Passed |
| Python/TensorFlow environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "import sys, tensorflow as tf; ..."` | Passed: executable `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, TensorFlow `2.20.0` |
| No obvious Python time loop | `rg -n "for t in range\\(|range\\(n_timesteps\\)" bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py` | Passed: no matches |
| Quantitative artifact baseline | JSON inspection of SVD/Kalman parity and compiled GPU artifacts | Passed |
| Dirty worktree boundary | `git status --short` | Recorded; many unrelated modified/untracked files remain untouched |
| Artifact inventory | `rg --files docs/benchmarks | rg "experimental-batched-(kalman|svd)"` | Passed; relevant artifacts present |
| Kalman CPU smoke | `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_linear_kalman_tf.py` | Passed: `9 passed` |
| SVD-UKF CPU smoke | `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py --mode parity --backend tf_svd_ukf --batch-size 3 --time-steps 5 --state-dim 2 --obs-dim 2 --parameter-dim 2 --rows all --device-scope cpu --device /CPU:0 --expect-device-kind cpu --output docs/benchmarks/experimental-batched-svd-ukf-phase0-smoke-b3-t5-n2-m2-2026-06-14.json` | Passed: all rows exact parity, finite outputs, CPU placement |

## Quantitative Baseline Validation

| Artifact | Required field | Observed |
| --- | --- | --- |
| `docs/benchmarks/experimental-batched-svd-ukf-parity-b20-t200-n10-m10-whileloop-2026-06-14.json` | `passed=true` | `true` |
| same | `max_abs_value_error <= 2e-13` | `1.7053025658242404e-13` |
| same | `max_abs_score_error <= 5e-13` | `4.547473508864641e-13` |
| `docs/benchmarks/experimental-batched-kalman-parity-b200-t200-n10-m10-2026-06-14.json` | `passed=true` | `true` |
| `docs/benchmarks/experimental-batched-kalman-parity-b4096-t200-n10-m10-2026-06-14.json` | `passed=true` | `true` |
| `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b20-t200-n10-m10-whileloop-2026-06-14.json` | `compiler.jit_compile=true`, finite outputs | `true`, `true` |
| `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b256-t200-n10-m10-whileloop-2026-06-14.json` | `compiler.jit_compile=true`, finite outputs | `true`, `true` |
| `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b4096-t200-n10-m10-whileloop-2026-06-14.json` | `compiler.jit_compile=true`, finite outputs | `true`, `true` |

## Dirty Worktree Boundary

The worktree was dirty before this program.  Pre-existing modified files include:

- `bayesfilter/inference/posterior_adapter.py`
- `docs/benchmarks/benchmark_tfp_nuts_gaussian.py`
- `tests/test_macrofinance_adapter.py`
- `tests/test_macrofinance_linear_compat_tf.py`

Pre-existing untracked batched-filtering files and benchmark artifacts are
present and are treated as current experimental baseline material.  This phase
added only new plan/review/result files and one new Phase 0 SVD smoke artifact:

- `docs/benchmarks/experimental-batched-svd-ukf-phase0-smoke-b3-t5-n2-m2-2026-06-14.json`

No production files were modified by Phase 0.

## Claude Review Trail

| Round | Artifact | Verdict | Action |
| ---: | --- | --- | --- |
| 1 | `docs/plans/bayesfilter-batched-filtering-claude-review-round-01-2026-06-14.md` | `REVISE` | Patched master/runbook/Phase 0 subplan for baseline validation, live SVD smoke, environment blockers, NeuTra gate status, and fair GPU comparators. |
| 2 | `docs/plans/bayesfilter-batched-filtering-claude-review-round-02-2026-06-14.md` | `AGREE` | Accepted as Phase 0 plan convergence. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 1 planning | Passed | No veto fired | Phase 1 implementation may reveal missing test seams in experimental SVD code | Draft and review Phase 1 subplan, then add focused correctness tests | No production readiness or default change |
| Preserve CUT4 exclusion | Passed for default-scope boundary | No veto fired | Tiny CUT4 may still be useful outside default program | Keep CUT4 out of Phase 1 default-promotion tests | No CUT4 readiness claim |
| Treat GPU artifacts as baseline only | Passed: artifacts are JIT compiled and finite | No new GPU work in Phase 0 | Phase 4 still needs fair scalar/batched comparator ladder | Defer GPU benchmarking to Phase 4 with trusted execution | No GPU speedup conclusion |

## Next-Phase Handoff Conditions

Phase 1 may begin only after its subplan exists and is reviewed for:

- consistency with this Phase 0 result;
- correctness and feasibility of the proposed test scope;
- artifact coverage;
- boundary safety around existing dirty worktree changes;
- no production default change.

Phase 1 must remain CPU-only unless its reviewed subplan is revised and a
trusted GPU approval is explicitly obtained.  The intended Phase 1 scope is
pytest-sized correctness stabilization for batched Kalman and SVD sigma-point
value+score paths.
