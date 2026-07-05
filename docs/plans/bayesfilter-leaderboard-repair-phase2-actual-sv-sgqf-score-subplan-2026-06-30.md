# Phase 2 subplan: actual-SV SGQF strict analytical score

Date: 2026-06-30

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Implement or formally defer a strict analytical SGQF score for the direct exact-transformed actual-SV route. If strict analytical score cannot be implemented safely in this phase, preserve the row as value-only with a precise blocker.

## Entry Conditions Inherited From Previous Phase

- Phase 1 passed or recorded a finite same-target value row.
- Current actual-SV SGQF score wrapper is known not to qualify while it uses `GradientTape`.
- Score coordinates and transformed target are fixed.

## Required Artifacts

- Derivation/provenance artifact mapping each implemented score term to the exact transformed actual-SV target and Phase 1 value route:
  `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-derivation-2026-06-30.md`
- If implemented, code changes in the narrow SGQF actual-SV derivative path.
- Tests for finite analytical score and provenance guard.
- Regenerated highdim leaderboard.
- Phase result:
  `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-result-2026-06-30.md`
- Refreshed Phase 3 subplan.

## Required Checks, Tests, Reviews

- Focused unit test for direct actual-SV SGQF analytical score.
- AST/text check that the admitted score route does not open `GradientTape`, `.gradient`, or autodiff fallback.
- Derivation/provenance review that the score differentiates the same Phase 1 direct exact-transformed SGQF value target, including transformed-observation and parameter-transform terms where applicable.
- FD consistency check as necessary but not sufficient.
- Strict analytical admission requires either multi-replicate expected-score calibration at true `theta_0` or an independent same-target score reference/derivation review strong enough to replace that calibration for this phase. If neither is available, the required outcome is defer/value-only.
- Boundary-safety checks near admissible transformed-parameter edges and Jacobian-sensitive regions, or an explicit defer/value-only decision if those checks cannot be made meaningful.
- CPU-only smoke for value/score.
- Claude read-only review of implementation diff and result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the direct exact-transformed actual-SV SGQF row emit a strict analytical score? |
| Baseline/comparator | Phase 1 same-target value row, derivation/provenance artifact, FD diagnostic, and either multi-replicate expected-score calibration or an independent same-target score reference/derivation review. |
| Primary criterion | Strict analytical admission requires a reviewed derivation/provenance mapping, finite score vector, analytical provenance with no tape/autodiff, same-target differentiation including transform terms, and at least one non-proxy correctness anchor beyond finiteness/provenance. |
| Veto diagnostics | `GradientTape` or autodiff in admitted provenance; score coordinate mismatch; FD sign/scale contradiction; nonfinite value/score; missing derivation artifact; no expected-score/reference/derivation correctness anchor; unsafe boundary behavior; target or transform-term mismatch. |
| Explanatory diagnostics | FD residuals, score norm, per-coordinate score terms. |
| Not concluded | No exact likelihood proof, no HMC posterior correctness, no GPU performance. |
| Artifact | Tests, regenerated leaderboard, and Phase 2 result. |

## Forbidden Claims And Actions

- Do not call a `GradientTape` wrapper analytical.
- Do not promote FD consistency alone to correctness.
- Do not alter target semantics to make derivatives easier.
- Do not admit a strict analytical score on finiteness and no-tape provenance alone.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 if:

- SGQF actual-SV score is strict analytical, derivation-backed, independently checked as above, and tested, or
- it remains explicitly value-only with a precise analytical-derivative/evidence blocker.

## Stop Conditions

Stop if:

- The analytical derivative requires a target change.
- Score derivation is missing, term mapping is unclear, boundary behavior is unsafe, or no non-proxy correctness anchor is available.
- FD or expected-score calibration diagnostics reveal a material contradiction.
- Workflow budget note: if Claude/Codex cannot converge on the same blocker within five review rounds, write a blocker result and stop.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 2 result/close record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 subplan for Zhao-Cui source-route and adapter safety.
