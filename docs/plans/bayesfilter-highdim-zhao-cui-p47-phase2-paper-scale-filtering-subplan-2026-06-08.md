# P47-M2 Subplan: Paper-Scale Readiness And Feasibility Manifests

metadata_date: 2026-06-08
phase: P47-M2
status: `DRAFT_FOR_CLAUDE_PLAN_REVIEW`

## Purpose

Prepare paper-scale or near-paper-scale Zhao--Cui model-suite filtering
readiness, resource caps, and feasibility manifests where source-governed
targets exist, while explicitly excluding S&P 500 real-data reproduction.

M2 is not a correctness-promotion phase.  Model-specific production filtering
correctness belongs to M3--M5 after dense/refined or exact reference gates.

## Phase Prerequisites

- `PASS_P47_M0_GOVERNANCE`
- `PASS_P47_M1_ADAPTIVE_ROUTE`

Every M2 candidate row must carry the M1 route label: `adaptive route
candidate` or `documented-deviation fixed-design substitute`.  A readiness
manifest cannot use generic "Zhao--Cui filtering" language without this label,
and `adaptive route candidate` is not an adaptive reproduction claim.

## Tasks

1. Select model-suite rows from the P47 registry that have passed the relevant
   lower-rung exact/tiny filtering or target-closure gates, not value checks
   alone.
2. Define paper-scale dimensions, horizons, ranks, basis sizes, and wall-time
   caps for synthetic/model-suite runs.
3. Run cheapest diagnostics first, then ladder one axis at a time.
4. Record resource, failure-mode, and branch manifests.  Accuracy summaries are
   explanatory unless the relevant model-specific M3--M5 reference gate has
   already passed.
5. Preserve lower-rung regressions as vetoes.

## Evidence Contract

Question: is BayesFilter ready to attempt source-governed synthetic/model-suite
filtering at paper-like scale, excluding S&P 500, without overclaiming
correctness?

Primary pass criterion: paper-scale candidate rows have explicit eligibility,
resource caps, branch policies, M1 route labels, stop conditions, and failure
manifests; any trial run is classified as feasibility/stress evidence unless a
model-specific reference gate has already passed.

Veto diagnostics:

- S&P 500 data or claims appear;
- M0 or M1 prerequisite token is absent;
- M1 route label is absent or generic Zhao--Cui wording hides a
  documented-deviation substitute;
- paper-scale result lacks tiny/exact lower-rung filtering or closure
  guardrail;
- finite paper-scale outputs are promoted as correctness;
- simultaneous unplanned ladder-axis changes;
- unclassified rank saturation, conditioning, memory, or time failure.

## Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_paper_scale_readiness.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_paper_scale_readiness.py
```

Long or GPU runs require a separate trusted execution plan.

## Claude Gate

Expected token:

```text
PASS_P47_M2_PAPER_SCALE_READINESS
```
