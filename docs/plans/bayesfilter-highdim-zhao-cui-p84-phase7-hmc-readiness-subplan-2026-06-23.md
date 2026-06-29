# P84 Phase 7 Subplan: HMC Readiness

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE6_AND_APPROVAL`

## Phase Objective

Evaluate or block HMC/NUTS readiness after derivative repair.

## Entry Conditions Inherited From Previous Phase

- Phase 6 derivative readiness passed.
- Exact HMC/NUTS commands, seeds, runtime posture, and artifacts are frozen.
- Explicit human approval is required before any HMC/MCMC command.

## Required Artifacts

- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase7-hmc-readiness-result-2026-06-23.md`
- HMC diagnostics manifest.
- Updated execution ledger and Phase 8 subplan.

## Required Checks / Tests / Reviews

Before execution, exact commands must be added.  Design checks:

```bash
rg -n "HMC|NUTS|divergence|R-hat|ESS|gradient|derivative readiness|sampler" \
  docs/plans \
  bayesfilter/highdim -S
```

Claude review and explicit human approval are required before HMC/MCMC.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are value/gradient and sampler diagnostics sufficient for HMC readiness? |
| Baseline/comparator | Phase 6 derivative-ready route and predeclared sampler diagnostics. |
| Primary criterion | No veto diagnostics, finite value/gradient checks, and sampler diagnostics pass under declared uncertainty scope. |
| Veto diagnostics | Divergences, failed R-hat/ESS thresholds, nonfinite gradients, short-chain overclaim. |
| Explanatory diagnostics | Runtime, acceptance, step size, posterior summaries. |
| Not concluded | No posterior correctness beyond declared sampler scope; no production default. |
| Artifact | HMC diagnostics manifest and result. |

## Forbidden Claims / Actions

- Do not run HMC/MCMC without exact approval.
- Do not rank speed if sampler validity vetoes fail.

## Exact Next-Phase Handoff Conditions

Phase 8 may begin only if HMC readiness is pass or explicitly out of scope for
the LEDH comparison.

## Stop Conditions

Stop if derivative or sampler vetoes fail.
