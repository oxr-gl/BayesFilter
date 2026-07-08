# Codex Substitute Review Bundle

Date: 2026-07-08
Review name: `scalar-filtering-geometry-hmc-phase6-closeout`
Supervisor/executor: Codex
Reviewer: local Codex substitute reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. This is a substitute review because external Claude review was policy-blocked for private repository context transfer risk. It is weaker than full Claude review.

## Objective

Review the Phase 6 closeout subplan before writing closeout artifacts.

## Artifacts To Inspect

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-result-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase6-closeout-subplan-2026-07-08.md`
- `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.json`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is Phase 6 sufficient and bounded for documentation-only closeout of the scalar filtering geometry-to-HMC readiness runbook? |
| Baseline/comparator | Phase 0-5 artifacts. |
| Primary criterion | Subplan requires closeout result/reset memo/ledger that separate passed engineering gates from unsupported scientific/runtime/default claims. |
| Veto diagnostics | Posterior correctness, convergence, zero-divergence, tuned-kernel, default-readiness, GPU/XLA-readiness, source-faithful Zhao-Cui, or sampler-superiority claim unsupported by the runbook; new experiments in closeout. |
| Explanatory diagnostics | Minor wording or artifact naming suggestions. |
| Not concluded | No new HMC/scientific/default readiness claim. |

## Review Questions

1. Does Phase 6 keep closeout documentation separate from new evidence generation?
2. Are the remaining gaps and non-claims explicit enough?
3. Does the subplan retain Phase 5 cautions about finite log-accept tails and native divergence unavailability?
4. Are stop and final handoff conditions sufficient before final response?

## Required Output

Return concise findings first. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
