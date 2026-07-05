# Claude Read-Only Review Bundle

Date: 2026-07-03
Review name: `bayesfilter-ledh-leaderboard-score-repair-phase3-resume-amendment`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.  Do not edit files, run commands, launch agents, or
change state.

Claude is not execution authority and cannot approve scientific-claim,
runtime, GPU, model-file, product, funding, or human-boundary crossings.

## Objective

Review only the Phase 3 resume amendment after Phase 2 was retracted for using
an invalid tape-gradient LEDH score route.

The review question is whether the amended master program, runbook, and Phase 3
subplan are now consistent with these hard rules:

- LEDH score means total derivative of the stated leaderboard likelihood
  target.
- `GradientTape` and `ForwardAccumulator` are forbidden for production LEDH
  score computation.
- Phase 3 must use manual VJP or a documented analytical equivalent.
- Value and score for an admitted row must come from the same scalar route:
  `value_route_id == score_route_id` and
  `value_score_route_status == same_route_value_score`.
- Finite differences must perturb the same scalar objective whose value is
  reported.
- CPU-hidden diagnostics are debugging only; material LEDH default-route score
  evidence requires trusted GPU/XLA/TF32 execution.

## Artifacts To Inspect

Inspect only these bounded local paths:

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-master-program-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-gated-execution-runbook-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-execution-ledger-2026-07-03.md`

## Self-Contained Summary Of Current State

Phase 2 attempted a same-target LGSSM score runner, then retracted it because
the route used `GradientTape`.  That score route is invalid for this program.
No LEDH leaderboard score row is admitted.

The current active phase is Phase 3.  It must repair the same-target LGSSM
score route using manual VJP or a documented analytical equivalent, preserve
the same scalar value/score route, and run only local no-autodiff checks before
any trusted GPU/XLA score smoke.

Local checks already run by Codex after the amendment:

- resume amendment text check: passed for the Phase 3 subplan;
- `git diff --check` on amended plan/runbook/subplan/ledger files: passed.

The ledger still says this amendment is pending review.  This bundle is that
bounded review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the resumed Phase 3 plan internally consistent with manual-total-score, no-tape/no-forward-accumulator, same-route value/score, and trusted GPU/XLA evidence rules? |
| Baseline/comparator | Phase 2 retraction and the July 3 LEDH-inclusive leaderboard state with no admitted LEDH score rows. |
| Primary criterion | The amended artifacts must make it impossible to admit a row unless the score is same-target, total-derivative, same-scalar-route, and not computed by `GradientTape` or `ForwardAccumulator`. |
| Veto diagnostics | Any text that permits tape/autodiff score computation, admits partial derivatives as scores, allows value/score route mismatch, promotes Contract E as same-target LGSSM score evidence, or treats CPU-hidden diagnostics as material LEDH default-route evidence. |
| Explanatory diagnostics | Wording clarity, artifact coverage, review-loop sufficiency. |
| Not concluded | No code correctness, no LGSSM score admission, no nonlinear score readiness, no HMC readiness. |

## Pass Criteria

Return `VERDICT: AGREE` only if all are true:

- the amended plan uses plain total-derivative score language;
- production LEDH score routes cannot use `GradientTape`;
- production LEDH score routes cannot use `ForwardAccumulator`;
- Phase 3 requires manual VJP or a documented analytical equivalent;
- admitted value+score rows require `value_route_id == score_route_id`;
- admitted value+score rows require
  `value_score_route_status == same_route_value_score`;
- finite-difference checks must use the same scalar objective;
- CPU-hidden diagnostics cannot be used as material GPU/XLA/TF32 score
  evidence;
- Claude remains read-only reviewer only.

Return `VERDICT: REVISE` if any item fails.

## Required Output

Findings first, concise.  End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
