# P8i Phase 5 Result: NUTS Readiness Decision

Date: 2026-06-16

Status: `BLOCK_NUTS_NOT_READY_REVIEWED`

## Phase Objective

Decide whether a bounded NUTS diagnostic is justified after Phase 4 Tier-1, or
write a blocker that preserves why NUTS is not yet warranted.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is a NUTS diagnostic scientifically and computationally justified for the selected P8i route now? |
| Baseline/comparator | Phase 4 HMC diagnostics and Phase 1-3 value/gradient/GPU gates. |
| Primary criterion | Write a blocker decision if NUTS lacks implementation path, adaptation budget, or diagnostics; otherwise require a separate reviewed NUTS subplan before any run. |
| Veto diagnostics | NUTS readiness claimed from two-sample fixed-kernel HMC; no NUTS command path; no adaptation/tuning diagnostics; no posterior convergence evidence; runtime budget not reviewed for NUTS. |
| Explanatory diagnostics | HMC acceptance, runtime, gradient cost, chain stability, projected NUTS cost. |
| Not concluded | NUTS readiness, production HMC readiness, posterior convergence, default sampler policy. |

## Skeptical Audit

- Wrong-baseline check: Phase 4 is not a tuned HMC run; it is a tiny execution
  diagnostic.
- Proxy-metric check: acceptance rate `1.0` and finite samples do not imply
  NUTS readiness.
- Stop-condition check: no NUTS command path, adaptation budget, or NUTS
  diagnostics are present in the runner.
- Artifact-fit check: the decision can be made from Phase 4 JSON plus code
  search; no new numerical run is needed or authorized.

## Checks

```bash
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-fixed-kernel-2026-06-16.json
rg -n "NoUTurn|NUTS|nuts|tfp.mcmc" scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*
```

Results:

- Phase 4 HMC JSON validation: passed.
- NUTS search found no NUTS command path; only `tfp.mcmc.HamiltonianMonteCarlo`
  and NUTS nonclaim/readiness text are present.
- `git diff --check`: passed.

## Decision

NUTS is blocked for P8i at this gate.

Reasons:

- the runner has no NUTS command path;
- no reviewed NUTS adaptation budget exists;
- no NUTS-specific diagnostics are defined;
- Phase 4 used only two retained samples, one burn-in step, one leapfrog step,
  fixed step size `0.005`, and one PF seed;
- Phase 4 did not establish posterior convergence, valid tuning, production
  HMC readiness, or NUTS readiness.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Block NUTS for P8i now, pending review. | Primary criterion selects blocker because NUTS lacks implementation path, adaptation budget, and diagnostics. | NUTS readiness from Phase 4 alone is vetoed. | A future reviewed NUTS plan might become justified after stronger HMC tiers and a NUTS implementation path. | Proceed to Phase 6 claim-boundary classification while preserving NUTS as blocked. | No NUTS readiness, production HMC readiness, posterior convergence, default sampler policy, or sampler recommendation. |

## Post-Run Red-Team Note

Strongest alternative explanation: NUTS might eventually be useful, but P8i
does not yet have the implementation, budget, or evidence to test it
responsibly.

What would overturn this result: a reviewed plan adding a NUTS implementation
path, adaptation/tuning budget, runtime projection, diagnostics, and stop
conditions after stronger HMC evidence.

Weakest part of the evidence: this is a governance decision, not a NUTS
experiment.

## Handoff

Proceed to Phase 6 only after read-only review accepts this blocker decision
and the refreshed Phase 6 subplan. Phase 6 must preserve that NUTS is blocked
and must not promote Phase 4 execution success into sampler readiness.
