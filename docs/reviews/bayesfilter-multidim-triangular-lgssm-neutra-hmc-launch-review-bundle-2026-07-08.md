# Claude Read-Only Review Bundle

Date: 2026-07-08
Review name: `bayesfilter-multidim-triangular-lgssm-neutra-hmc-launch`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run commands, launch agents, approve boundary
crossings, or act as execution authority.

## Objective

Review the launch plan for the multidimensional triangular LGSSM NeuTra-HMC
program. The question is whether the master program, runbook, and Phase 0/1
subplan boundary are internally consistent, feasible, source-aware, and safe.

## Artifacts To Inspect

- `docs/plans/bayesfilter-multidim-triangular-lgssm-neutra-hmc-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-multidim-triangular-lgssm-neutra-hmc-visible-gated-execution-runbook-2026-07-08.md`
- `docs/plans/bayesfilter-multidim-triangular-lgssm-neutra-hmc-phase0-source-identifiability-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-multidim-triangular-lgssm-neutra-hmc-phase1-model-contract-subplan-2026-07-08.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is this launch plan safe and sufficient to begin Phase 0 source/design inventory? |
| Baseline/comparator | User request, local runbook protocol, MARSS/stationarity context, and BayesFilter policy. |
| Primary criterion | No material blocker to starting Phase 0 only. |
| Veto diagnostics | Unsupported identifiability claim, stationarity treated as full identifiability, missing stationary initial law, missing stop conditions, hidden approval crossing, or runtime/training/HMC authorized too early. |
| Explanatory diagnostics | Suggestions for clearer artifact coverage or safer phase boundaries. |
| Not concluded | That the LGSSM implementation, training, or HMC will pass. |

## Review Questions

1. Is there a material correctness or boundary issue in the launch plan?
2. Does the plan correctly separate stationarity, coordinate identification,
   synthetic recoverability, and HMC evidence?
3. Are Phase 0 and Phase 1 scoped safely before implementation/runtime?
4. Are approvals and stop conditions explicit enough?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
