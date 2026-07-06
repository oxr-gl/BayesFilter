# BayesFilter NeuTra c603 Integration Phase 4 Review Bundle

Date: 2026-07-06
Review name: `bayesfilter-neutra-c603-integration-phase4`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, or approve
boundary crossings.

## Objective

Review the c603 generic-interface close record. The question is whether the
design note is correctly bounded by the evidence from the c603 import and
mechanics work, and whether it avoids overclaiming arbitrary nonlinear SSM or
HMC readiness.

## Primary Exact Path

- `docs/plans/bayesfilter-neutra-c603-integration-phase4-generic-interface-result-2026-07-06.md`

## Supporting Exact Paths If Needed

- `docs/plans/bayesfilter-neutra-c603-integration-phase3-fixed-transport-mechanics-result-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-c603-integration-phase4-generic-interface-subplan-2026-07-06.md`
- `bayesfilter/ssm/contracts.py`
- `bayesfilter/ssm/target_builder.py`
- `bayesfilter/inference/batched_value_score.py`
- `bayesfilter/inference/fixed_transport_hmc.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the Phase 4 generic-interface result note consistent with the repo’s actual interfaces and bounded correctly by the c603 evidence? |
| Baseline/comparator | The completed Phase 3 mechanics result and the concrete BayesFilter interfaces named in the result note. |
| Primary criterion | The note separates target identity, transport binding, mechanics binding, and HMC validation gates, and does not claim universal nonlinear SSM or HMC readiness. |
| Veto diagnostics | Overclaiming arbitrary nonlinear SSM support, blurring mechanics into HMC readiness, or misnaming the actual code surfaces. |
| Explanatory diagnostics | Suggestions for tighter wording or a cleaner close-record shape that do not change the substance. |
| Not concluded | No new code correctness claim, no HMC readiness claim, no production readiness claim. |

## Review Questions

1. Is there a material correctness or boundary issue in the Phase 4 result note?
2. Does it clearly preserve the evidence boundary from c603 import/mechanics work?
3. Are there unsupported claims or missing nonclaims?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
