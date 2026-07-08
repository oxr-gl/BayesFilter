# P86 Zhao-Cui Production Decision Reset Memo

Date: 2026-06-24

Status: `BLOCK_P86_ZHAO_CUI_SIR_NOT_PRODUCTION_PROMOTED`

## Bottom Line

Zhao-Cui SIR is not production-promoted by P86.

P86 repaired meaningful author-route plumbing through an admissible
training-base full-budget fit and an admissible rank-5 comparator artifact, but
the mandatory Phase 6 rank/degree convergence gate is reviewed-blocked:

```text
BLOCK_P86_PHASE6_RANK_DEGREE_CONVERGENCE_NOT_ESTABLISHED_REVIEWED
```

The rank-5 comparator fit completed, but its fit and holdout residuals are much
worse than the rank-4 lower rung, and degree convergence still needs a reviewed
configurable-basis execution path. Downstream correctness, KR, HMC, LEDH,
scale, and production gates therefore remain blocked/deferred.

## What Passed

- Phase 0: P86 governance, source, approval, and XLA/static setup freeze.
- Phase 1: author `Lagrangep` mass/integral implementation.
- Phase 2: algebraic measure convention contract.
- Phase 3: downstream author-route wiring.
- Phase 4: tiny author-route fit smoke.
- Phase 5: budget-compliant CPU-hidden training-base fit admission.
- Phase 6 comparator artifact: approved same-route rank-5 fit completed and is
  admissible as a comparator artifact.

## What Blocked

- Phase 6 rank convergence is not established.
- Phase 6 degree convergence is blocked pending a reviewed configurable-basis
  execution path.
- Phase 7 correctness bridge is blocked/deferred by Phase 6.
- Phase 8 KR/transport closure is blocked/deferred by upstream gates.
- Phase 9 derivative/HMC readiness is blocked/deferred by upstream gates.
- Phase 10 LEDH comparator and scale stress are blocked/deferred by upstream
  gates.
- Phase 11 production promotion is blocked.

## Key Artifacts

- `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-result-2026-06-24.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank5-comparator-fit-2026-06-24.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-ledger-2026-06-24.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-result-2026-06-24.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase11-production-decision-reset-result-2026-06-24.md`

## Nonclaims

P86 does not conclude rank convergence, degree convergence, posterior
correctness, KR closure, analytical derivative readiness, HMC readiness, LEDH
superiority, d=50/d=100 scaling, GPU performance, source-faithful author
TT-cross training, default-policy change, or production readiness.

## Safest Next Program

The next useful program is a Phase 6 repair program with two branches:

- make basis/order/elements setup-configurable in the training-base runner while
  preserving setup-static XLA semantics;
- serialize or otherwise preserve enough trained TT state to compute reviewed
  functional rank/degree convergence diagnostics, not just summary residuals.

Any new fit, GPU, HMC, LEDH, scale, or long command still needs exact approval.
