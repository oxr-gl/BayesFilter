# P8i Phase 2 Result: Longer-Horizon OT Gradient Ladder

Date: 2026-06-16

Status: `PASS_LONGER_PREFIX_GRADIENT_REVIEWED`

## Phase Objective

Check longer-prefix AD gradient stability for the exact P8h/P8i route at the
Phase 1 selected diagnostic particle count, preserving that this is a
fixed-seed relaxed-OT computational graph diagnostic.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are AD gradients finite, connected, repeatable, and finite-difference-consistent enough at horizons `16,32` and `N=5` to justify the next GPU/HMC diagnostic? |
| Baseline/comparator | P8h Phase 6 short-prefix horizon `4` gradient result and P8i Phase 1 selected longer-prefix count. |
| Primary criterion | Horizon `16` and `32` artifacts pass finite connected gradients over five fixed seeds, repeat-value/gradient stability, max finite-difference residual at most `1e-5`, trusted-GPU placement, exact route/count provenance, and P8i phase/plan manifest fields; otherwise explicit blocker. |
| Veto diagnostics | Disconnected gradient; nonfinite value/gradient; max finite-difference residual above `1e-5`; CPU fallback; route/count mismatch; stale P8h-only phase/plan provenance; relaxed-OT AD gradient overclaimed as exact stochastic PF marginal score. |
| Explanatory diagnostics | Gradient norms, finite-difference residuals, repeat deltas, ESS, runtime. |
| Not concluded | Stochastic PF marginal-gradient correctness, HMC readiness, NUTS readiness, posterior convergence, filter ranking, or default sampler policy. |

## Skeptical Audit

- Wrong-baseline check: P8h Phase 6 horizon `4` is treated as a shorter
  predecessor, not evidence that horizons `16,32` already pass.
- Proxy-metric check: finite-difference agreement is a veto diagnostic and
  consistency check, not a proof of the stochastic PF marginal gradient.
- Stop-condition check: horizon `32` was allowed only after the horizon `16`
  pilot passed all executable gates.
- Artifact-fit check: both JSON artifacts preserve P8i phase names, the P8i
  subplan path, runtime budget, FD threshold, trusted GPU tensor devices,
  route/count, seeds, and structured gate/blocker diagnostics.

## Implementation Repair Before Execution

Read-only review found that the original Phase 2 draft had documented gates
that were not fully executable. The repair added:

- CLI forwarding for `--p8h-gradient-manifest-phase`,
  `--p8h-gradient-manifest-plan`, `--runtime-budget-seconds`, and
  `--p8h-gradient-fd-threshold`;
- helper-level GPU-only enforcement for the Phase 2 gradient gate;
- status/blocker logic for finite connected gradients, FD residual threshold,
  trusted requested GPU, and runtime budget;
- focused tests for provenance success, FD/trusted-device blocker, CPU
  rejection, runtime-budget blocker, core-gradient blocker, and CLI forwarding.

Claude review round 9 returned `VERDICT: AGREE` for the repaired Phase 2
execution gate.

## Provenance Note

The Phase 2 JSON artifacts use schema
`filter_bench.p8h_ot_gradient.v1` because the current runner reuses the
reviewed P8h OT-gradient helper as a codepath selector. That schema still
contains inherited P8h evidence-contract text naming P8h Phase 5/4 context and
the legacy run-manifest field `phase6_plan`. For P8i, the controlling
provenance is:

- JSON `phase`: `P8I_PHASE2_LONGER_HORIZON_GRADIENT_H16_PILOT` and
  `P8I_PHASE2_LONGER_HORIZON_GRADIENT_H32`;
- JSON `run_manifest.command`: the exact P8i command with
  `--p8h-gradient-manifest-phase`, `--p8h-gradient-manifest-plan`,
  `--runtime-budget-seconds 1800`, and `--p8h-gradient-fd-threshold 1e-5`;
- JSON `run_manifest.phase6_plan`: the P8i Phase 2 subplan path, despite the
  legacy field name;
- this result file's evidence contract and decision table.

Therefore the inherited schema wording is not treated as the P8i Phase 2
baseline/comparator. The P8i baseline remains P8h Phase 6 horizon `4` plus
the P8i Phase 1 selected longer-prefix count.

## Commands And Checks

Local repair checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h_ot_gradient"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*
```

Results:

- `py_compile`: passed.
- Focused pytest: `6 passed, 24 deselected, 2 warnings`.
- `git diff --check`: passed.

Horizon `16` trusted GPU pilot:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-ot-gradient-check --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 16 --particles 5 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --runtime-budget-seconds 1800 --p8h-gradient-fd-threshold 1e-5 --p8h-gradient-manifest-phase P8I_PHASE2_LONGER_HORIZON_GRADIENT_H16_PILOT --p8h-gradient-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h16-pilot-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h16-pilot-2026-06-16.csv
```

Horizon `32` trusted GPU gate:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-ot-gradient-check --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 32 --particles 5 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --runtime-budget-seconds 1800 --p8h-gradient-fd-threshold 1e-5 --p8h-gradient-manifest-phase P8I_PHASE2_LONGER_HORIZON_GRADIENT_H32 --p8h-gradient-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h32-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h32-2026-06-16.csv
```

Post-run checks:

```bash
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h16-pilot-2026-06-16.json
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h32-2026-06-16.json
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*
```

All passed.

## Results

| Horizon | Status | Wall seconds | Max FD residual | Max repeat grad delta | All finite | All connected | Trusted GPU | Runtime within budget |
|---:|---|---:|---:|---:|---|---|---|---|
| 16 | `executed_p8h_ot_gradient_check` | `259.910317` | `7.556148151621755e-09` | `0.0` | true | true | true | true |
| 32 | `executed_p8h_ot_gradient_check` | `444.488749` | `1.1271613864494157e-08` | `0.0` | true | true | true | true |

Mean diagnostics:

| Horizon | Mean log likelihood | Mean gradient |
|---:|---:|---|
| 16 | `-8.206925764133295` | `[-0.815475926290094, -3.2727333945478803]` |
| 32 | `-16.271024752723953` | `[-2.364142106656983, -3.491229989619664]` |

All value and gradient tensors were recorded on
`/job:localhost/replica:0/task:0/device:GPU:0`; both artifacts have
`blocker: null`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass Phase 2 longer-prefix relaxed-OT AD gradient diagnostic, pending review. | Passed at horizons `16,32`, `N=5`, five fixed seeds, FD threshold `1e-5`, trusted GPU, runtime budget `1800s`. | No Phase 2 veto fired. | This is still a fixed-seed relaxed-OT graph diagnostic, not a stochastic PF marginal-score proof or HMC validity result. | Refresh Phase 3 for GPU scaling/runtime profiling at the same route/count/horizons before HMC tiers. | No stochastic PF marginal-gradient correctness, no HMC or NUTS readiness, no posterior convergence, no filter ranking, no default sampler policy. |

## Post-Run Red-Team Note

Strongest alternative explanation: the gradient graph is internally stable for
fixed seeds and relaxed OT, but HMC may still fail because repeated target
evaluations are too slow, noisy, or geometrically unsuitable.

What would overturn this result: a reviewed rerun showing nonfinite or
disconnected gradients, FD residual above threshold, wrong route/count,
untrusted GPU placement, runtime budget failure, or stale P8h-only provenance.

Weakest part of the evidence: finite-difference agreement checks the
implemented deterministic graph at fixed seeds. It does not establish that the
gradient is the exact stochastic particle-filter marginal likelihood score.

## Handoff

Proceed to Phase 3 only after read-only review accepts this result and the
refreshed Phase 3 subplan. Phase 3 should use the same route/count and
horizons `16,32`, with any adjacent `N=10` comparison gated by runtime
projection. Phase 3 must not claim a full GPU scaling law, HMC readiness, or
full-horizon performance.
