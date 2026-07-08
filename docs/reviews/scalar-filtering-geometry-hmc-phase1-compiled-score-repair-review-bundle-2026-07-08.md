# Codex Substitute Review Bundle

Date: 2026-07-08
Review name: `scalar-filtering-geometry-hmc-phase1-compiled-score-repair`
Supervisor/executor: Codex
Reviewer: local Codex substitute reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. This is a substitute review because external Claude review was policy-blocked for private repository context transfer risk. It is weaker than full Claude review.

## Objective

Review the Phase 1 compiled-score repair subplan before code edits and parent-scale retry execution.

## Artifacts To Inspect

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-runtime-repair-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-compiled-score-repair-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-execution-ledger-2026-07-08.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is compiling the value/score wrapper a valid bounded repair for the parent Phase 1 timeout? |
| Baseline/comparator | The prior eager horizon-30/72 parent run that timed out without artifacts. |
| Primary criterion | Plan preserves target/criteria, requires compiled/eager parity, keeps CPU-hidden non-XLA status explicit, and blocks Phase 2 on timeout/missing artifact/rejected geometry. |
| Veto diagnostics | Hidden HMC execution, hidden GPU/XLA/default readiness claim, changing pass/fail criteria after timeout, skipping parity check, timeout treated as scientific failure, unsupported source-faithfulness claim. |
| Explanatory diagnostics | Minor wording or artifact naming suggestions. |
| Not concluded | No HMC readiness, no posterior correctness, no convergence, no default readiness. |

## Review Questions

1. Is this a bounded execution-flow repair rather than a scientific gate downgrade?
2. Does the plan prevent non-XLA CPU graph execution from being treated as production/GPU evidence?
3. Are parity and timeout vetoes sufficient?
4. Does Phase 2 remain blocked unless the parent artifact passes the declared gate?

## Required Output

Return concise findings first. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
