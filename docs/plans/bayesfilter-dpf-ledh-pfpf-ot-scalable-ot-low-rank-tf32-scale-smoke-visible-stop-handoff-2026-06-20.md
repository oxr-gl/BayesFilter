# Low-Rank TF32 Scale Smoke Visible Stop Handoff

Date: 2026-06-20

## Status

`FINAL_TUNED_GPU_SCALE_PASSED_DIAGNOSTIC_ONLY`

## Current State

The low-rank LEDH-PFPF-OT TF32 scale-smoke master program passed P00
governance after Claude Round 2 returned `VERDICT: AGREE`.  LR-TF32-1 harness
and small invariants passed.  The prior LR-TF32-2 interpretation has been
amended: applying the downstream moment hard gate to one untuned setting was a
planning/usage error.

## Stop Reason

The lane was rerun with explicit tuning.  Focused tuning found a viable
setting, renewed medium CPU no-dense validation passed, and P03 trusted GPU
scale passed at `N=50000` and conditional `N=100000`.  A final read-only
Claude amended-closeout review returned `VERDICT: AGREE` with only two
nonblocking wording/provenance nits; both were patched.

## Latest Artifacts

- `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py`
- `tests/test_low_rank_tf32_scale_smoke.py`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.md`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.md`
- `docs/benchmarks/logs/low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.log`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.md`
- `docs/benchmarks/logs/low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.log`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.md`
- `docs/benchmarks/logs/low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p01-harness-invariants-result-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02-medium-cpu-result-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02b-focused-tuning-result-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02c-medium-cpu-tuned-result-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p03-trusted-gpu-scale-result-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-result-2026-06-20.md`

## Final Evidence Summary

- No-dense factor route ran at `N=4096` and `N=8192` on CPU-hidden medium
  rows.
- Factor residuals, induced row/column residuals, finite checks, sign checks,
  and output log-weight normalization passed.
- Weighted second-moment errors were approximately `2.935e-01` for the untuned
  `rank=64`, `assignment_epsilon=0.5` setting; this is classified as a tuning
  signal only.
- Focused tuning found `rank=64`, `assignment_epsilon=0.015625`.
- Tuned medium CPU no-dense validation passed at `N=4096` and `N=8192` with
  weighted second-moment errors approximately `6.984e-02`, below the `7.5e-02`
  threshold.
- Trusted GPU scale passed at `N=50000` and `N=100000` with no hard vetoes and
  no dense scale transport materialization.
- The final trusted GPU diagnostic manifest records explicit `--phase-id
  LR-TF32-3` and the P03 phase-result path.
- No dense scale transport matrix was materialized.

## Non-Claims

No speedup, ranking, TF32-help, posterior correctness, HMC readiness, public API
readiness, production/default readiness, dense Sinkhorn equivalence, full
low-rank Sinkhorn solver fidelity, broad scalable-OT selection, or coordinator
merge is concluded.
