# P37-M2.6d Subplan: SV TT Lane Replay And Governance Closeout

metadata_date: 2026-06-05
phase: P37-M2.6d

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-remaining-phases-gated-execution-master-plan-2026-06-05.md`

depends_on:
- P37-M2.6c short sequential SV TT value path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-result-2026-06-05.md`

## Purpose

Close the scalar SV TT lane before moving to M3.  This phase audits replay,
branch manifests, traceability rows, result-ledger claim boundaries, and
non-claims for M2.6a--M2.6c.

This phase does not add new mathematical capability.  It prevents later SIR,
predator-prey, stress, or derivative phases from inheriting an ambiguous SV TT
evidence boundary.

## Source-Governance Status

- P30 anchors identified: inherited from M2.6a--M2.6c; closeout must list exact
  anchors used by each promoted SV TT claim.
- Zhao--Cui paper anchors identified: inherited from M2.6a--M2.6c; closeout
  must separate paper-source claims from BayesFilter extensions.
- MATLAB behavioral anchors identified: inherited from M2.6a--M2.6c; MATLAB
  remains audit material only unless a phase explicitly matched behavior.
- BayesFilter code/test anchors identified: M2.6a--M2.6c code and tests.
- Deviations listed: yes, expected fixed-design scalar BayesFilter extension.
- Clean-room boundary respected: must be re-attested.
- Unsupported claims removed: must be re-attested.
- Reviewer verdict: pending Claude review.

## Closeout Inputs

Passed phase ledgers:

```text
M2.6a result =
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-result-2026-06-05.md
M2.6a Claude ledger =
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-claude-review-ledger-2026-06-05.md
M2.6b result =
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-result-2026-06-05.md
M2.6b Claude ledger =
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-claude-review-ledger-2026-06-05.md
M2.6c result =
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-result-2026-06-05.md
M2.6c Claude ledger =
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-claude-review-ledger-2026-06-05.md
traceability ledger =
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

Required pass tokens before M2.6d can pass:

```text
PASS_M2P6A
PASS_M2P6A_CODE_GOVERNANCE
PASS_M2P6B
PASS_M2P6B_CODE_GOVERNANCE
PASS_M2P6C
PASS_M2P6C_CODE_GOVERNANCE
```

Promoted SV TT lane claims to preserve:

```text
M2.6a = fixed-design degree-64 square-root TT fitting for scalar initial and
  transition adjacent SV targets against dense oracle values.
M2.6b = squared-density normalizer and scalar all-retained normalized density
  for the fixed M2.6a adjacent targets.
M2.6c = TT-only two-observation scalar sequential value path with
  TT-generated retained propagation against dense GL321 comparator.
```

Claims that must remain blocked/non-promoted:

```text
paper-scale T=1000
adaptive MATLAB TT-cross/SIRT reproduction
integrated-axis generic marginalization
SMC or real-data S&P 500 validation
derivatives, HMC, DSGE, GPU production
high-dimensional scalability
stable top-level public API
```

## Evidence Contract

Question: after M2.6a--M2.6c, is the scalar SV TT lane sufficiently governed
and replayable to serve as a prerequisite for later model-suite phases without
overclaiming?

Baseline/comparator:

- M2.6a, M2.6b, and M2.6c result ledgers;
- traceability ledger statuses;
- branch replay hashes and fixture IDs;
- broad highdim guardrails.

Primary pass criteria:

- all M2.6a--M2.6c promoted claims have traceability rows;
- no promoted row is `BLOCKED_UNTRACEABLE` or `BLOCKED_UNVALIDATED`;
- branch fixtures and replay identities are deterministic under rerun;
- result ledgers contain non-claims and post-run red-team notes;
- broad highdim guardrails remain green.
- focused SV lane closeout tests pass:
  `test_p30_sv_fixed_design_tt_target.py`,
  `test_p30_sv_squared_density_normalizer_marginal.py`,
  `test_p30_sv_short_sequential_tt_value_path.py`;
- traceability row for stochastic volatility explicitly names M2.6a, M2.6b,
  and M2.6c and preserves the non-promoted claims above.

Veto diagnostics:

- unresolved M2.6a/M2.6b/M2.6c blocker;
- missing traceability row for a promoted claim;
- public/API/HMC/DSGE/GPU/high-dimensional scalability overclaim;
- copied or line-translated MATLAB structure;
- branch replay mismatch.

Explanatory-only diagnostics:

- wall time, file counts, number of traceability rows, test count, warning
  count, and dirty-worktree summary.

What will not be concluded:

- no new numerical accuracy claim beyond M2.6c;
- no paper-scale or adaptive TT-cross reproduction;
- no derivative/HMC/DSGE/GPU readiness.

Artifacts preserving result:

- result ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-result-2026-06-05.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-claude-review-ledger-2026-06-05.md`

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_AFTER_PATCH`.

This phase exists to prevent a common failure mode: after a technical gate
passes, later work often treats it as broader evidence than it is.  M2.6d must
be a governance closeout, not a new implementation sprint.

M2.6c has passed local evidence and Claude code/governance review.  M2.6d may
therefore start plan review.  Implementation remains limited to ledgers and
traceability unless Claude returns a blocker requiring a narrow test or
artifact amendment.

Wrong baseline risk: M2.6d must not rerun only the newest M2.6c test and infer
that M2.6a/M2.6b remain valid.  The focused closeout command includes all
three SV TT lane test files.

Proxy risk: test count, wall time, and clean diff status are explanatory only.
The promotion criterion is governed traceability plus focused and broad
guardrails, not performance or number of tests.

Claim-drift risk: the traceability row must say M2.6c is a two-observation
scalar fixed-design TT bridge only.  It must not call the lane paper-scale,
adaptive, high-dimensional, derivative-ready, HMC-ready, DSGE-ready, or
GPU-ready.

## Planned Closeout Tasks

1. Verify that the M2.6a, M2.6b, and M2.6c result ledgers contain their pass
   tokens and Claude code/governance pass tokens.
2. Verify the stochastic-volatility traceability row names M2.6a, M2.6b, and
   M2.6c evidence and preserves blocked/non-promoted claims.
3. Run focused SV lane tests for M2.6a--M2.6c.
4. Run broad highdim guardrail from the overnight runbook.
5. Write the M2.6d result ledger with a decision table, run manifest,
   closeout checklist, non-claims, and post-run red-team note.
6. Run Claude code/governance review and require explicit
   `PASS_M2P6D_CODE_GOVERNANCE`.

## Planned File Ownership

Allowed writes after M2.6c passes:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

Optional test-only writes require a reviewed amendment.

## Planned Commands

Focused closeout command to refine after M2.6c:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py
```

Broad highdim guardrail follows the overnight runbook.
