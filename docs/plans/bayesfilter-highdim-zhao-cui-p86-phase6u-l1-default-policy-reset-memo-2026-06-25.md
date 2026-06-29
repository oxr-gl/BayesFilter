# Reset Memo: P86 Phase 6U Zhao-Cui L1 Tuning Default Policy

Date: 2026-06-25

## Current State

Owner directive has been implemented as a Zhao-Cui lane policy:

```text
L1 regularization with explicit L1 weight tuning is the default Zhao-Cui
training-base procedure going forward.
```

This does not change the global P75 scalar default. `DEFAULT_L1_WEIGHT` remains
`0.0`, and `l1_weight=0.0` remains a valid comparator arm inside reviewed
tuning grids.

## Key Artifacts

- Phase 6T reviewed diagnostic result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-diagnostic-result-2026-06-25.md`
- Phase 6U subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-subplan-2026-06-25.md`
- Phase 6U result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-result-2026-06-25.md`
- Runner:
  `scripts/p86_author_lagrangep_phase5_budget_fit.py`
- Governance:
  `AGENTS.md`

## Policy Meaning

Future Zhao-Cui training-base decisions must use a reviewed L1 tuning protocol
with validation/audit separation:

- validation/holdout may nominate, select, or veto candidates under a reviewed
  plan;
- audit data remains reserved for final-only checks and must not be used for
  tuning;
- a selected L1 value requires a reviewed tuning/selection ledger;
- Phase 6T's `l1_weight=1e-9` result is promising but not universal.

## What Remains Blocked

Phase 7 correctness/HMC/production work remains blocked. The next governed
phase should be Phase 6V convergence/selection, not Phase 7.

Phase 6V should compare at least:

- `LR=0.0003, l1_weight=0.0`;
- `LR=0.0003, l1_weight=1e-9`;
- nearby L1 values only if the reviewed Phase 6V plan authorizes them.

## Nonclaims

- No final selected L1 scalar.
- No final rank convergence.
- No production readiness.
- No posterior correctness.
- No HMC readiness.
- No LEDH comparison.
- No GPU performance claim.
- No source-faithful TT-cross training claim.
