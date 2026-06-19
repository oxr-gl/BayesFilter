# P75 Phase 5 Result: Collapse Diagnosis And Next Diagnostic

metadata_date: 2026-06-18
status: PHASE5_DIAGNOSIS_PASSED_LOCAL_CHECKS_CLAUDE_AGREE_READY_FOR_PHASE6
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-subplan-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | What is the most likely cause of the Phase 4 defensive-floor collapse, and what is the smallest justified next action? |
| Exact baseline/comparator | Phase 4 tiny target smoke JSON; Phase 1 objective design; P73 blocked diagnostic as historical context only. |
| Primary criterion | Satisfied pending local checks and Claude review.  The Phase 4 artifact separates execution success from diagnostic failure and identifies initialization/objective-scale collapse as the first discriminating hypothesis. |
| Diagnostics that veto | The larger degree 2/rank 4 pilot remains vetoed.  The Phase 4 audit line veto and defensive-floor collapse are blocking evidence. |
| Explanatory only | Loss cancellation, tiny gradient norm, line residual magnitude, holdout/replay relative residuals, runtime. |
| What is not concluded | No final algorithmic success/failure, production readiness, rank/sample policy, or source-faithful Zhao--Cui parity. |
| Artifact preserving result | This result, Phase 6 subplan, updated ledgers. |

## Diagnosis

The Phase 4 tiny target smoke completed two finite optimizer batches, but it
did not learn a meaningful square-root TT component.  The final manifest
recorded:

- `rho_min=rho_max=1e-8`;
- `normalizer=1e-8`;
- `gradient_norm=8.65590982995174e-09`;
- near-zero line predictions against large line residuals;
- `audit_line_veto`.

For the P75 objective
\[
\rho_\theta(z)=h_\theta(z)^2+\tau q_0(z),
\]
this is the signature of the defensive component \(\tau q_0\) dominating the
trainable component.  The immediate discriminating question is whether the
problem is caused by starting \(h_\theta\) at an exponentially small scale in
36 dimensions.

## Selected Next Action

Run exactly one bounded warm-start smoke before any larger pilot:

- keep the Phase 4 tiny target scale: degree 1, rank 1, batch size 16, two
  batches, seed 7501, CPU-only;
- compare the existing random initialization against a guided
  calibrated-constant initialization on identical target-smoke and audit
  draws;
- the guided initializer uses the source-route local target cloud to set a
  rank-1 constant path so that \(h_0^2\) has target-scale mass on the fit
  cloud;
- judge only whether the warm start escapes the defensive floor and produces
  non-tiny gradients, and whether it materially improves over the concurrent
  random-initialization arm.

This is a minimal proxy for the user's UKF-guidance hypothesis.  The current
code does not yet expose a full UKF-Gaussian-to-TT initializer for the
author-SIR step.  The available guided information is the same local
source-route frame and target cloud used by the fixed variant.  If calibrated
target-scale initialization does not move the diagnostic off the floor, a
larger UKF-guided implementation is not justified without deeper objective
changes.  If it does move off the floor, the next phase can formalize a proper
UKF/source-guided warm-start design.

## Nonclaims

- No lower-gate repair is claimed.
- No validation, HMC, scaling, or rank-promotion readiness is claimed.
- No source-faithful Zhao--Cui claim is made.
- The warm-start smoke is not a full UKF-guided algorithm.
- The warm-start smoke cannot select degree, rank, learning rate, or
  regularization from audit samples.

## Local Checks

Passed:

```text
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p75-target-smoke-2026-06-17.json
rg -n "defensive-floor|rho_min|rho_max|normalizer|gradient_norm|guided|warm-start|larger pilot|degree 2" docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-subplan-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md
```

## Claude Review

Claude reviewed the Phase 5 result and Phase 6 subplan.  Claude first returned
`VERDICT: REVISE` because the warm-start test needed a relative comparison
against the random arm and identical target/audit draws.  The plan was patched
to require seed 7501, identical target-smoke/audit draws, and a relative win in
`rho_max` and gradient norm over random initialization.  Claude then returned
`VERDICT: AGREE`.
