# DPF3 Kernel PFF Exclusion Check

## Status

DPF3 execution artifact.  Kernel PFF remains excluded from routine DPF
implementation and benchmark plans.

## Evidence Reviewed

- `experiments/student_dpf_baselines/reports/advanced-particle-filter-kernel-pff-debug-gate-result-2026-05-11.md`
- DPF0-A ledger row DPF0A-012
- DPF0 implementation obligation DPF0-O08

## Decision

`kernel_pff_excluded_pending_debug`

## Rationale

The student debug gate reports completed reduced runs, but also records that
kernel PFF should remain excluded from routine panels because completed filter
runs can still hit the maximum flow-iteration cap.  That is debug evidence, not
routine comparison readiness.

## Required Future Debug Gate

Kernel PFF may be reconsidered only after a separate BayesFilter-owned debug
gate specifies:

- scalar versus matrix kernel variants;
- tolerance ladder;
- max-iteration hit fraction threshold;
- convergence residuals;
- runtime cap;
- finite output checks;
- independent reference/proxy comparator;
- explicit non-implications for posterior, HMC, production, and model-risk use.

## DPF3 Consequence

No DPF3, DPF5, or DPF7 handoff may list kernel PFF as an implementation
candidate except as excluded/deferred work.
