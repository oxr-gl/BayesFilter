# P47-M5 Subplan: Predator-Prey Filtering And Preconditioning

metadata_date: 2026-06-08
phase: P47-M5
status: `DRAFT_FOR_CLAUDE_PLAN_REVIEW`

## Purpose

Establish matched predator-prey nonlinear filtering and preconditioning
evidence in two explicit evidence classes:

- lower-rung dense/refined reference filtering and matched-budget
  preconditioning evidence;
- production- or near-paper-scale filtering evidence with the lower-rung gate
  and M2 readiness as prerequisites.

Proposal or preconditioner metrics are explanatory unless downstream filtering
quality on the declared target also passes.

## Phase Prerequisites

- `PASS_P47_M0_GOVERNANCE`
- `PASS_P47_M1_ADAPTIVE_ROUTE`
- `PASS_P47_M2_PAPER_SCALE_READINESS` for
  `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING`; small dense/refined
  filtering work may proceed without M2 but may emit only
  `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`.
Every promoted filtering, comparison, or preconditioning row must carry the M1
route label: `adaptive route candidate` or `documented-deviation fixed-design
substitute`.

## Tasks

1. Freeze predator-prey dynamics, observation law, discretization, and domain
   policy.
2. Build a matched linear bridge and matched nonlinear bridge with identical
   budgets and target identity.
3. Add small dense/refined references before production-scale rows.
4. Compare accuracy, cost-normalized ESS-like diagnostics, wall time, and
   failure modes without promoting raw ESS alone.
5. If CUT4 comparison is attempted, ensure it uses the same declared closure
   target as Zhao--Cui.

## Evidence Contract

Question: does nonlinear predator-prey filtering/preconditioning improve a
declared metric under fair comparison controls?

Primary pass criteria:

- Reference-filtering gate: matched linear and nonlinear rows use the same
  target, same data, same budget, M1 route label, and small dense/refined
  references; downstream filtering value/state-quality metrics pass the
  reviewed tolerance; proposal or preconditioner metrics are cost-normalized
  explanatory diagnostics and cannot alone satisfy
  `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`.
- Production-filtering gate: `PASS_P47_M2_PAPER_SCALE_READINESS` and
  `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING` have passed; at least one
  production- or near-paper-scale predator-prey row runs under the declared
  resource caps, preserves target identity and route label, reports downstream
  filtering value/state-quality metrics, and satisfies the reviewed production
  tolerance or records a blocker without emitting the production token.

Veto diagnostics:

- unmatched budgets;
- nonfinite ODE/filter values;
- domain failure or negative-state policy drift;
- raw ESS-only promotion when cost-normalized evidence fails;
- proposal/preconditioner improvement is promoted without downstream filtering
  quality passing;
- M1 route label is absent or generic Zhao--Cui wording hides a
  documented-deviation substitute;
- closure target and native target are mixed.
- `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING` is emitted without M2
  readiness, the reference-filtering token, and a production- or
  near-paper-scale row.

Long-run and trusted-execution controls:

- long nonlinear bridge, GPU, or runs expected to exceed five minutes require a
  separate reviewed experiment plan;
- each run must declare maximum wall time, memory cap, ODE step cap, rank cap,
  and early stop if the small dense/refined reference or matched-budget control
  regresses;
- GPU/CUDA commands require trusted/escalated execution under `AGENTS.md`.

## Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_predator_prey_filtering.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_predator_prey_filtering.py
```

## Claude Gate

Expected token:

```text
PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING
```

The production token is reviewed only by a separate M5b production or
near-paper-scale row after the reference-filtering token has passed.
