# Phase 4 subplan: predator-prey SGQF and Zhao-Cui cells

Date: 2026-06-30

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Repair predator-prey leaderboard cells by aligning every emitted value with the source-scope `zhao_cui_predator_prey_T20` T20 observations, preserving or adding SGQF value only when it uses that T20 target, adding strict analytical score only if implemented, and wiring a Zhao-Cui evaluator adapter only if target-compatible.

## Entry Conditions Inherited From Previous Phase

- Phase 3 closed or precisely blocked Zhao-Cui LGSSM m3.
- Leaderboard validator rejects tape/autodiff SGQF scores as analytical.
- Predator-prey value route and current derivative limitation are documented.
- The current source-scope row is `zhao_cui_predator_prey_T20`; lower-rung P47 two-observation fixtures are diagnostic only unless explicitly labeled outside the T20 leaderboard row.

## Required Artifacts

- Focused predator-prey evaluator/derivative code changes, if any.
- Target-alignment check proving emitted predator-prey cells use the T20 source-scope observations or remain blocked.
- Tests for value and score provenance.
- Regenerated highdim leaderboard.
- Phase result:
  `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-result-2026-06-30.md`
- Refreshed Phase 5 subplan.

## Required Checks, Tests, Reviews

- SGQF predator-prey value finite check.
- Check that the fixed-SGQF predator-prey row no longer reports the P47 two-observation lower-rung fixture under the T20 source-scope row.
- Strict analytical derivative test if score is emitted.
- Zhao-Cui predator-prey adapter smoke if implemented.
- FD check as necessary but not sufficient.
- Claude read-only review of result/diff.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can predator-prey cells be upgraded without target drift or mislabeling taped derivatives as analytical? |
| Baseline/comparator | Source-scope T20 predator-prey dataset and current highdim leaderboard row. P47 two-observation fixtures are diagnostic only. |
| Primary criterion | Each predator-prey cell is executed value/value+analytical-score or explicitly blocked with a narrow reason. |
| Veto diagnostics | P47 lower-rung value reported as T20 source-scope value; tape/autodiff analytical score claim; target mismatch; nonfinite likelihood; missing theta coordinate for score. |
| Explanatory diagnostics | FD residual, score norm, runtime. |
| Not concluded | No broad nonlinear production readiness or HMC convergence. |
| Artifact | Regenerated leaderboard and Phase 4 result. |

## Forbidden Claims And Actions

- Do not call the current SGQF derivative adapter analytical while it uses TensorFlow tape.
- Do not invent a Zhao-Cui predator-prey route without classifying it.
- Do not report the P47 two-observation lower-rung fixture as the `zhao_cui_predator_prey_T20` source-scope row.
- Do not compare runtime if value/score validity fails.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 if:

- Predator-prey cells have honest statuses and no invalid analytical-score claims.
- Any emitted predator-prey value uses the T20 source-scope observations, or the cell is blocked with a precise target/evaluator reason.
- Remaining adapter blockers are specific enough for later implementation.

## Stop Conditions

Stop if:

- Predator-prey target cannot be stated with a free theta.
- The only available SGQF/Zhao-Cui route is the lower-rung two-observation diagnostic and no T20 target-compatible route can be wired.
- Analytical derivative derivation is materially unclear after review.
- Adding Zhao-Cui would require unapproved source-route invention.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 4 result/close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 subplan for SIR parameterized-likelihood correctness.
