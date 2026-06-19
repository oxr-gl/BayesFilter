# P8j Phase 5b Result: SIR Tuning Blocker Repair Diagnostic

metadata_date: 2026-06-17
status: BLOCKED_REPAIR_CANDIDATE_REVIEW_REQUIRED
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 5b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 5b did not select a SIR d18 particle count and did not authorize Phase 6.  It preserved the bootstrap blocker and identified a bounded LEDH OT Sinkhorn repair candidate requiring review. |
| Primary criterion status | Partially met for diagnosis only.  Bootstrap higher-count diagnostics ran and stayed blocked; LEDH OT first-failure scale diagnostics ran and produced a plausible scale-adaptive epsilon probe. |
| Veto diagnostic status | No SIR model/data mutation; no `N=8` selection; trusted GPU was used for GPU diagnostics; no leaderboard, gradient/HMC, or source-faithfulness claim is made. |
| Main uncertainty | Whether scale-adaptive Sinkhorn epsilon remains finite across five seeds and adjacent particle rungs, and whether bootstrap needs much larger counts or a different scoped decision. |
| Next justified action | Draft/review Phase 5c for a bounded LEDH OT scale-adaptive repair attempt and higher-count bootstrap decision boundary. |
| What is not concluded | No particle-count adequacy, no leaderboard completion, no DPF gradient correctness, no HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity, no production readiness. |

## Required Local Checks

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8j or sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-subplan-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md
```

Results:

- before diagnostic patch: `8 passed, 32 deselected, 2 warnings`;
- after diagnostic patch: `10 passed, 32 deselected, 2 warnings`;
- `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`: passed;
- `git diff --check`: passed.

## Bootstrap Higher-Count Diagnostic

Command:

```bash
MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8j-sir-particle-tuning-stage0 --row sir --algorithms bootstrap_dpf_current --horizons 20 --particles 128,256 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8j-profile-manifest-phase P8J_PHASE5B_BOOTSTRAP_HIGHER_COUNT_DIAGNOSTIC --p8j-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-subplan-2026-06-17.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-bootstrap-higher-count-2026-06-17.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-bootstrap-higher-count-2026-06-17.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-bootstrap-higher-count-selected-blocked-2026-06-17.csv
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-bootstrap-higher-count-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-bootstrap-higher-count-2026-06-17.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-bootstrap-higher-count-selected-blocked-2026-06-17.csv`

Result:

| N | Finite | Trusted GPU | MC SE | Mean log likelihood | Runtime seconds |
| --- | --- | --- | --- | --- | --- |
| 128 | true | true | `10.02446699866811` | `-817.5079550325889` | `7.814613` |
| 256 | true | true | `7.609999974520083` | `-809.5568270985705` | `7.670804` |

The MC SE gate remains approximately `2.0` to `2.05`, so bootstrap remains
blocked with `BLOCK_P8J_SIR_PARTICLE_TUNING_MC_SE`.  This is a tuning-range
blocker, not evidence against bootstrap DPF.

## LEDH OT Sinkhorn Diagnostic

Implementation patch:

- Added diagnostic-only CLI `--p8j-sir-ot-sinkhorn-diagnostic`.
- Added schema `filter_bench.p8j_sir_ot_sinkhorn_diagnostic.v1`.
- The normal filter path and SIR model/data are unchanged.

Command:

```bash
MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8j-sir-ot-sinkhorn-diagnostic --row sir --horizon 20 --particles 16 --seeds 81120 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-ledh-ot-sinkhorn-diagnostic-2026-06-17.json
```

Artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-ledh-ot-sinkhorn-diagnostic-2026-06-17.json`

First resampling event, `N=16`, seed `81120`:

| Diagnostic | Value |
| --- | --- |
| time index | `0` |
| ESS ratio | `0.24966021424924256` |
| cost mean | `116.56402657134574` |
| cost max | `237.97475859459587` |
| nominal epsilon | `1.0` |
| cost max / epsilon | `237.97475859459587` |
| source weight min/max | `0.0005741327232378748` / `0.4565806477311872` |
| source weight perplexity | `6.444932731362863` |
| nominal failure | `FloatingPointError: Sinkhorn row residual exceeded tolerance envelope` |

Scale-adaptive probe:

| Probe | Value |
| --- | --- |
| epsilon | `116.56402657134574` |
| iterations | `500` |
| tolerance | `1e-6` |
| finite | true |
| transport helper max row residual | `4.788947016720613e-13` |
| transport helper max column residual | `4.163336342344337e-17` |
| canonical transport row sum residual | `2.220446049250313e-16` |

Interpretation:

- The LEDH OT failure is a cost-scale/solver-configuration failure at the first
  SIR resampling event under inherited scalar-SV P8h Sinkhorn settings.
- A scale-adaptive epsilon equal to the first-event cost mean is a plausible
  repair candidate.
- This diagnostic does not select the repair.  It must be reviewed and then
  tested across five fixed seeds and adjacent particle counts before Phase 5
  can be rerun.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `94069066a70df6f1f0f2b53d32b9d452bd67f891` |
| Dirty state | Large pre-existing dirty/untracked worktree; P8j changes preserved without reverting unrelated work. |
| Environment | TensorFlow/TensorFlow Probability P8j SIR tuning and diagnostic harness. |
| CPU/GPU status | Local tests intentionally CPU-hidden; diagnostics ran as trusted/escalated GPU and TensorFlow saw `/device:GPU:0`. |
| Seeds | Bootstrap: `81120,81121,81122,81123,81124`; LEDH OT diagnostic: `81120`. |
| Candidate counts | Bootstrap: `128,256`; LEDH OT first-failure diagnostic: `16`. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-result-2026-06-17.md` |

## Post-Run Red Team

Strongest alternative explanation:

- Bootstrap may pass only at much larger counts or with a different resampling
  policy.  The 128/256 result is not an impossibility proof.
- The LEDH OT scale-adaptive probe is one resampling event, one seed, one
  particle count.  It may fail later in the same trajectory or across five
  seeds.

What would overturn the blocker:

- A reviewed Phase 5c implementation of scale-adaptive Sinkhorn settings
  showing finite LEDH OT across the five fixed seeds and an adjacent rung; and
- a higher-count bootstrap decision that either passes MC SE and adjacent
  stability or is explicitly scoped as still blocked.

Weakest part of the evidence:

- The LEDH OT repair candidate has not yet been run as a full trajectory under
  five fixed seeds.

## Handoff

Phase 6 remains blocked.  Phase 5c may begin only after Claude read-only review
of this Phase 5b result and the Phase 5c subplan returns `VERDICT: AGREE`.
