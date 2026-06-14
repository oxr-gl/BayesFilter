# P47-M0 Subplan: Governance Freeze And Target Registry

metadata_date: 2026-06-08
phase: P47-M0
status: `DRAFT_FOR_CLAUDE_PLAN_REVIEW`

## Purpose

Freeze the P47 target registry, claim classes, dependency graph, and explicit
S&P 500 exclusion before any implementation or long experiment begins.

## Inputs

- P37 closeout result.
- P42 validation rules.
- P45 target registry and closeout.
- P46 multistate adapter and resume-governance results.

## Tasks

1. Create or update a P47 target registry with one row for each remaining
   target:
   - adaptive TT-cross/SIRT route;
   - synthetic/paper-scale SV filtering excluding S&P 500;
   - generalized SV comparison;
   - spatial SIR filtering/comparison;
   - predator-prey filtering/comparison;
   - score/HMC readiness.
2. For each row, record:
   - target law and parameterization;
   - reference route;
   - CUT4 route, if applicable;
   - Zhao--Cui route;
   - M1 route label: `adaptive route candidate` or
     `documented-deviation fixed-design substitute`;
   - value and score claim class;
   - blocker state;
   - forbidden nonclaims.
3. Add tests that verify S&P 500 reproduction is out of scope and cannot be
   silently added to P47 promoted rows.

## Evidence Contract

Question: is P47 target identity and claim governance frozen enough to start
implementation phases without target drift?

Primary pass criterion: machine-readable registry and tests exist, with no
promoted row lacking a reference route and no S&P 500 row in scope.

Veto diagnostics:

- missing target identity or parameterization;
- missing reference route for a promoted candidate;
- missing M1 route label for a promoted Zhao--Cui row;
- S&P 500 is included;
- P45 blocker rows are overwritten instead of amended.

## Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json
```

## Claude Gate

Expected token:

```text
PASS_P47_M0_GOVERNANCE
```
