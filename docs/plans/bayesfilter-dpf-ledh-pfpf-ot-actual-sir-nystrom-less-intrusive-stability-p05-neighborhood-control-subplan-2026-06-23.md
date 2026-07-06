# P05 Neighborhood And Control Gate Subplan

Date: 2026-06-23

## Phase Objective

If P04 passes, test whether the selected repair also handles the nearby brittle
row and preserves the known viable control.

## Entry Conditions Inherited From Previous Phase

- P04 aggregate status is `PASS`.
- P04 paired max and mean deltas are within thresholds.
- P04 trusted GPU/TF32 evidence is present.
- P04 result refreshed this subplan with exact selected repair CLI mode.

## Required Artifacts

- P05 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p05-neighborhood-control-result-2026-06-23.md`
- Row JSON/Markdown/log artifacts for:
  - `rank=64,epsilon=0.3`, `N=1024`, `T=20`, seeds `81920..81924`;
  - `rank=32,epsilon=0.5` control, `N=1024`, `T=20`, seeds `81920..81924`.
- P06 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-promotion-readiness-decision-subplan-2026-06-23.md`

## Required Checks, Tests, And Reviews

- Trusted GPU preflight with GPU1 preference and GPU0 fallback.
- Run two compiled actual-SIR `route both` benchmark rows with diagnostics and
  selected repair mode.
- Stop-on-hard-veto: if the nearby brittle row hard-vetoes, do not run optional
  extra stress rows; still run or preserve the control only if already
  predeclared and useful for classification.
- Summarize finite flags, residuals, paired deltas, selected repair diagnostics,
  and control status.
- Claude read-only review of P05 interpretation before P06 if P05 passes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the repair generalize to the nearby brittle row while preserving the viable control? |
| Baseline/comparator | Compiled streaming TF32 comparator in each row; raw prior artifacts for context. |
| Primary pass criterion | Both predeclared rows pass aggregate hard veto screen and paired thresholds. |
| Veto diagnostics | Any aggregate hard veto, missing GPU evidence, missing selected-repair metadata, missing control, or paired threshold failure. |
| Explanatory diagnostics | Runtime, repair counters, scaling/factor ranges, residual magnitudes. |
| Not concluded | No default readiness, no statistical ranking, no high-N/scalable readiness, no HMC readiness. |
| Artifact preserving result | P05 result and row artifacts. |

## Forbidden Claims And Actions

- Do not run high-N or HMC gates in P05.
- Do not rank repair against streaming by runtime.
- Do not change thresholds or add rows after observing results.
- Do not claim default readiness.

## Exact Next-Phase Handoff Conditions

Advance to P06 only if:

- P05 result says both rows passed;
- required row artifacts exist;
- Claude review of P05 interpretation returns `VERDICT: AGREE`.

If P05 fails but artifacts are valid, route to P06 for neighborhood-failure
classification and next-loop decision.  P06 may close out, recommend fixed
policy, or draft a bounded return-to-P02 repair-selection loop if the failure
is an expected repair-candidate failure rather than a harness or boundary
failure.

## Stop Conditions

Stop or close out if:

- trusted GPU evidence is unavailable;
- a row artifact is invalid/missing;
- selected repair metadata is missing;
- continuing would require changing thresholds, target rows, or repair family.

A valid candidate failure with complete artifacts is not by itself a stop
condition; it is routed to P06 classification or the reviewed repair loop.

## Skeptical Plan Audit

Unfair comparison risk: only testing the first row could overfit.  Mitigation:
P05 requires nearby brittle row and viable control.

Proxy risk: control pass alone would not repair brittle rows.  Mitigation: both
rows must pass.

Statistical risk: five seeds are still limited.  Mitigation: P05 is a viability
gate, not a ranking/default gate.

Audit status: `READY_AFTER_P04_PASS`.
