# P75 Closeout Erratum: UKF Warm-Start Hypothesis Untested

metadata_date: 2026-06-18
status: P75_CLOSED_ERRATUM_CLAUDE_AGREE
superseded_by: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Erratum

P75 should be closed as a negative record for random initialization,
calibrated-constant initialization, and source-route square-root prefit.  It
must not be used as evidence that a true UKF-informed warm start has failed.

The planning error entered in Phase 7.  Phase 7 correctly identified that UKF
moments could provide geometry, but then selected source-route square-root
prefit as the Phase 8 implementation target because a full UKF Gaussian-to-TT
initializer surface was not yet present.  That substitution changed the
scientific question.  Phases 8--10 therefore tested
\[
  \text{calibrated constant}
  \longrightarrow
  \text{source-route supervised square-root prefit}
  \longrightarrow
  \text{mini-batch density training},
\]
not
\[
  \text{UKF-informed geometry warm start}
  \longrightarrow
  \text{mini-batch density training}.
\]

## What P75 Established

The following conclusions are supported by P75:

- Random initialization failed by defensive-floor collapse.
- Calibrated constant initialization fixed scale and gradient flow but not
  target geometry or audit-line behavior.
- Source-route square-root prefit was mechanically executable, preserved
  provenance separation in the tested lanes, and produced no material
  improvement over calibrated constant under the Phase 10 frozen criterion.
- Phase 10 produced zero mechanism wins out of four source-guided-prefit
  mechanism rows.

The following conclusions are not supported by P75:

- P75 did not test a true UKF-informed initializer.
- P75 did not disprove UKF warm-starting.
- P75 did not repair the lower gate.
- P75 did not establish validation readiness, HMC readiness, scaling,
  source-faithfulness, final rank/sample policy, or authorization for the
  degree-2/rank-4/batch-1024/500-batch pilot.

## Baseline Status For Future Work

Random, calibrated constant, and source-route prefit are failed historical
baselines for the lower-gate geometry problem.  Future planning may mention
them as provenance or sanity sentinels, but must not spend new ladder rows
tuning or promoting them as live candidate repairs unless the user explicitly
approves a different scientific question.

The remaining live hypothesis is:
\[
  \text{use UKF moments }(m_{\rm UKF},P_{\rm UKF})
  \text{ to initialize } h_\theta
  \text{ before mini-batch stochastic density training.}
\]

## Required Supersession Rule

Any continuation must use a new master program.  The new program must:

- target an actual UKF-informed warm start;
- use mini-batch stochastic density training after that initialization;
- keep UKF as `scout_not_truth`, not validation or correctness evidence;
- forbid source-route prefit as a substitute for UKF initialization;
- preserve audit-data separation;
- require reviewed mathematical design before implementation.

## Local Checks Planned

```text
rg -n "UKF|source-route prefit|random|calibrated constant|not supported|superseded" docs/plans/bayesfilter-highdim-zhao-cui-p75-closeout-erratum-ukf-hypothesis-untested-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-closeout-erratum-ukf-hypothesis-untested-2026-06-18.md
```

## Skeptical Erratum Audit

This erratum does not erase P75 evidence.  It narrows the interpretation:
P75 is valid negative evidence for the methods it actually ran, and invalid
evidence against the UKF warm-start method it did not run.
