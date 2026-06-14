# P47-M4 Subplan: Spatial SIR Filtering And Equality

metadata_date: 2026-06-08
phase: P47-M4
status: `DRAFT_FOR_CLAUDE_PLAN_REVIEW`

## Purpose

Move spatial SIR from first-gate model-contract evidence to two explicit
evidence classes:

- lower-rung dense/refined reference and same-target equality evidence;
- production- or near-paper-scale filtering evidence with the lower-rung gate
  and M2 readiness as prerequisites.

Production-scale resource manifests are feasibility evidence unless the phase
also satisfies the production-filtering gate below.

## Phase Prerequisites

- `PASS_P47_M0_GOVERNANCE`
- `PASS_P47_M1_ADAPTIVE_ROUTE`
- `PASS_P47_M2_PAPER_SCALE_READINESS` for
  `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`; small-`J`
  reference/equality work may proceed without M2 but may emit only
  `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`.
Every promoted filtering or equality row must carry the M1 route label:
`adaptive route candidate` or `documented-deviation fixed-design substitute`.

## Tasks

1. Freeze the SIR state, observation law, positivity/domain policy, ODE/RK
   discretization, and closure target.
2. Build small-`J` dense/refined references before any paper-scale `J=9` run.
3. Use P46/P47 multistate retained-grid contracts for Zhao--Cui filtering.
4. Use CUT4 only on a declared additive-Gaussian closure target.
5. Report observed and unobserved state accuracy separately.

## Evidence Contract

Question: can spatial SIR filtering be run and compared on a declared same
target without silently replacing the native epidemiological model?

Primary pass criteria:

- Reference/equality gate: small-`J` dense/refined reference passes, the
  Zhao--Cui route evaluates the declared target, observed and unobserved state
  filtering errors satisfy the reviewed tolerance, the M1 route label is
  preserved, and any CUT4 equality row uses a same-target CUT4/Zhao--Cui pair
  with justified value and gradient tolerances.
- Production-filtering gate: `PASS_P47_M2_PAPER_SCALE_READINESS` and
  `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY` have passed; at least one
  production- or near-paper-scale spatial SIR row runs under the declared
  resource caps, preserves target identity and route label, reports observed
  and unobserved filtering errors, and satisfies the reviewed production
  tolerance or records a blocker without emitting the production token.

Production-scale or near-paper-scale manifests may be recorded only as
feasibility/stress evidence unless they also satisfy the same model-specific
reference/equality criteria.  Finite production outputs alone cannot satisfy
`PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`.

Veto diagnostics:

- negative populations are silently accepted;
- observed-only accuracy is presented as full-state accuracy;
- ODE/RK step mismatch;
- native SIR and additive-Gaussian closure are mixed as one target;
- no dense/refined small-`J` reference exists.
- M1 route label is absent or generic Zhao--Cui wording hides a
  documented-deviation substitute;
- finite production manifests are promoted as filtering correctness.
- `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING` is emitted without M2
  readiness, the reference/equality token, and a production- or
  near-paper-scale row.

Long-run and trusted-execution controls:

- paper-scale `J=9`, GPU, or runs expected to exceed five minutes require a
  separate reviewed experiment plan;
- each run must declare maximum wall time, memory cap, ODE step cap, rank cap,
  and early stop if the small-`J` reference regresses;
- GPU/CUDA commands require trusted/escalated execution under `AGENTS.md`.

## Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_spatial_sir_filtering.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_spatial_sir_filtering.py
```

## Claude Gate

Expected token:

```text
PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY
PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING
```
