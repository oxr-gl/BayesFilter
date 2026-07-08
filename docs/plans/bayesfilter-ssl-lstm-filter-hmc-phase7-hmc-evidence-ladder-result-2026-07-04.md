# Phase 7 Result: HMC Launch Smoke

Date: 2026-07-05

Status: `PASSED_WITH_LAUNCH_SMOKE`

## Phase Objective

Run a bounded HMC mechanics smoke on the admitted SSL-LSTM adapters and
classify immediate hard vetoes without pretending to produce convergence,
ranking, or replicated-evidence results.

## Entry Conditions

- Phase 6 shared benchmark artifact and protocol remain active.
- Admitted candidates are `fixed_sgqf` and `svd_ukf`.
- Blocked candidates remain `zhaocui_fixed` and `ledh_streaming_ot`.

## Launch-Smoke Outcome

The launch-smoke runner executed successfully and wrote the persistent JSON and
Markdown artifact pair under this result path.

Hard-veto summary:

- `fixed_sgqf`: no hard veto in the launch smoke.
- `svd_ukf`: no hard veto in the launch smoke.
- `zhaocui_fixed`: blocked, missing SSL-LSTM Zhao-Cui fixed adapter.
- `ledh_streaming_ot`: blocked, missing manual VJP streaming-OT score path.

Observed diagnostics, treated as explanatory only:

- both admitted candidates had finite initial target value and score;
- both admitted candidates completed tiny fixed-kernel HMC launch runs with
  finite samples;
- native divergence telemetry was not exposed by the TFP kernel results;
- acceptance rate was 1.0 in both admitted launch-smoke runs.

## Evidence Boundaries

This phase does not conclude:

- sampler convergence;
- R-hat or ESS;
- invariant-metric promotion;
- ranking or superiority;
- posterior correctness;
- parameter identifiability;
- production/default readiness.

## Decision Table

| Decision | Status | Notes |
| --- | --- | --- |
| Launch-smoke artifact written | Passed | Persistent JSON/Markdown artifacts exist. |
| Hard-veto classification | Passed | No launch hard veto for admitted candidates. |
| Ranking claim | Not allowed | Launch smoke only. |
| Convergence claim | Not allowed | Tiny fixed-kernel smoke only. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for admitted candidates |
| Statistically supported ranking | Not claimed |
| Descriptive-only differences | Present but not interpreted |
| Default-readiness | Not checked |
| Next evidence needed | Phase 8 closeout and any future longer replicated HMC tier |

## Nonclaims

- launch-tier HMC mechanics smoke only
- not a sampler convergence claim
- not R-hat or ESS evidence
- not posterior correctness evidence
- not filter sufficiency evidence
- not parameter-recovery evidence
- not a ranking claim
- not default-readiness evidence
