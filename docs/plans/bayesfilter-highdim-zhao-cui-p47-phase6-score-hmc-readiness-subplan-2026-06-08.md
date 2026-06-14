# P47-M6 Subplan: Score API And HMC Readiness

metadata_date: 2026-06-08
phase: P47-M6
status: `DRAFT_FOR_CLAUDE_PLAN_REVIEW`

## Purpose

Create an evidence-class score/API/HMC readiness table and an experimental
`bayesfilter.highdim` score-helper contract only for targets whose value paths
and same-target comparison gates already passed.  The API contract gate and
HMC readiness gate are separate: an experimental lower-rung score contract may
pass while HMC readiness remains blocked.

M6 does not promote a stable top-level public score API, production score API,
or production HMC readiness unless a separately reviewed row supplies the
corresponding P42 Tier 1/2/3 evidence.

## Phase Prerequisites

- `PASS_P47_M0_GOVERNANCE`
- `PASS_P47_M1_ADAPTIVE_ROUTE`
- Per-target equality/filtering tokens listed below.

M6 may define the generic interface before every target passes, but a target
cannot be promoted into the production score API or HMC-readiness table until
its model-specific upstream token certifies value/gradient or filtering
correctness for the same declared target.
Every promoted API/HMC target row must carry the M1 route label: `adaptive
route candidate` or `documented-deviation fixed-design substitute`.

## Tasks

1. Define the evidence-class readiness-table surface, input/output shapes,
   dtype policy, error behavior, branch/floor/fitting freeze semantics,
   deterministic replay behavior, and regression coverage for the experimental
   subpackage helper.
2. For each candidate target, run P42 Tier 1 local numerical correctness:
   value, vector score, absolute/block errors, and at least five directional
   checks.
3. Record P42 Tier 2 statistical-scale simulations as blocked/not-run unless a
   separate reviewed experiment supplies them.
4. Record Tier 3 Hamiltonian/leapfrog probes as blocked/not-run unless a
   separate reviewed experiment supplies them before any HMC-readiness claim.
5. Keep exact-target correctness, statistical smallness, and surrogate
   usefulness as separate claim classes.

## Evidence Contract

Question: are the score API contract and gradients stable enough for the
declared targets, and which of those targets also pass HMC readiness?

Primary pass criterion:

- API contract pass: stable interface, deterministic frozen-branch semantics,
  error behavior, dtype/shape policy, M1 route label, and regression coverage
  pass for a named target.
- HMC readiness pass: P42 Tier 1/2/3 evidence passes for each promoted target
  under the same unconstrained parameterization and fixed branch/floor policy.

Per-target upstream dependency tokens:

- generalized SV: `PASS_P47_M3_GENERALIZED_SV_EQUALITY`;
- spatial SIR lower-rung API/HMC candidate:
  `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`;
- spatial SIR production API/HMC candidate:
  `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`;
- predator-prey lower-rung API/HMC candidate:
  `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`;
- predator-prey production API/HMC candidate:
  `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING`.

M6 must label every promoted target as lower-rung or production.  A lower-rung
token can support only lower-rung API/HMC diagnostics; production API/HMC
claims require the corresponding production-filtering token.

Veto diagnostics:

- value agreement is used as gradient correctness;
- finite differences use a single fragile step size;
- autodiff crosses unfrozen branch changes, clipping, or adaptive fitting;
- near-stationary score rule is ignored;
- HMC readiness is claimed from surrogate usefulness alone.
- API readiness is claimed without interface, error-behavior, dtype/shape, and
  deterministic replay tests.
- M1 route label is absent or generic Zhao--Cui wording hides a
  documented-deviation substitute.
- production API/HMC readiness is claimed from lower-rung spatial SIR or
  predator-prey tokens.

Long-run and trusted-execution controls:

- Tier 2 simulation, Tier 3 Hamiltonian/leapfrog probes, GPU, or runs expected
  to exceed five minutes require a separate reviewed experiment plan;
- each run must declare maximum wall time, memory cap, seed count, data
  replicates, leapfrog length, and early-stop diagnostics;
- GPU/CUDA commands require trusted/escalated execution under `AGENTS.md`.

## Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_score_api.py tests/highdim/test_p47_hmc_readiness.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_score_api.py tests/highdim/test_p47_hmc_readiness.py
```

## Claude Gate

Expected token:

```text
PASS_P47_M6_SCORE_HMC_READINESS
```
