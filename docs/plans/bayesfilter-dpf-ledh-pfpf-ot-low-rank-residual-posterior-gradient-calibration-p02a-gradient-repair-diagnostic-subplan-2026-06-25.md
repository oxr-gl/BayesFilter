# P02A Low-Rank Gradient Repair Diagnostic Subplan

Date: 2026-06-25

Status: `READY_FOR_FOCUSED_GPU_DIAGNOSTIC`

## Phase Objective

P02A is a repair-loop diagnostic launched by the visible gated runbook after
P02 stopped with `LOW_RANK_GRADIENT_REPAIR_REQUIRED`.  It does not advance to
P03.  It runs only the P02 failing low-rank seed/probe pairs and localizes
whether the nonfinite posterior gradients arise in the route likelihood, prior,
final transported particles, or route output layer.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Where do the P02 low-rank nonfinite gradients first appear for the failing probes? |
| Baseline/comparator | Canonical P02 result note plus the P02 raw data payload and same LGSSM exact-reference fixture/probe definitions.  The P02 raw artifact's internal phase/title metadata is stale and must not be used for phase identity. |
| Primary pass/fail criterion | A focused JSON/Markdown artifact identifies finiteness of value gradient, log-likelihood gradient, prior gradient, final-particle gradient, route outputs, and low-rank factor diagnostics for every failing probe. |
| Veto diagnostics | Missing GPU/XLA provenance, corrupt artifact, missing failing probes, or a diagnostic that cannot distinguish likelihood/prior/output-layer gradient finiteness. |
| Explanatory diagnostics | Low-rank factor residuals, induced row/column residuals, projection iterations, timings, and output device. |
| Not concluded | No residual threshold calibration, no P03 handoff, no holdout validation, no posterior correctness, no HMC readiness, no default readiness, no statistical superiority, and no scientific-validity claim. |
| Artifact | `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.json` plus Markdown/log and result note. |

P02 baseline metadata caveat: the P02 reproduction JSON/Markdown data payload is
the relevant failing-probe source, but its internal phase/title metadata is
quarantined as stale.  Use the P02 result note, command, filenames, and ledger
for phase identity.

## Command

```bash
python docs/benchmarks/benchmark_low_rank_ledh_gradient_nonfinite_diagnostic.py \
  --case-id lgssm_small_exact_ref \
  --num-particles 1024 \
  --time-steps 12 \
  --low-rank-rank 16 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-alpha 1.0e-8 \
  --low-rank-max-projection-iterations 120 \
  --particle-chunk-size 64 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.md \
  --quiet
```

Stdout/stderr:
`docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02a-gradient-repair-diagnostic-gpu.log`

## Stop/Handoff

Stop after the diagnostic artifact.  If it localizes the nonfinite source,
write a P02A result and propose the smallest code repair.  Do not run P03 until
P02 is rerun and passes hard validity vetoes.
