# P03 Subplan: Closeout And Next-Rung Handoff

## Phase Objective

Synthesize P00-P02 into a bounded result and draft the next justified validation
rung without overclaiming from the medium paired quality screen.

## Entry Conditions Inherited From Previous Phase

- P02 either passed, failed with a clear candidate/harness interpretation, or
  stopped with a blocker result.
- Required P02 artifacts have been inspected before interpretation.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-result-2026-06-20.md`
- Updated visible execution ledger.
- Updated stop handoff.
- Optional next-rung draft if P02 passes:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-next-target-shape-repeated-stability-subplan-2026-06-20.md`

## Required Checks, Tests, And Reviews

- Local artifact consistency check for P00-P02 results and P02 JSON fields.
- Result note must include a decision table, inference-status table, run
  manifest, post-run red-team note, and explicit nonclaims.
- Result note must carry forward the exact comparator definition, tolerance
  formula/semantics, paired seed count, field-level default metadata assertions,
  and worst per-seed/per-output default-arm drifts that justify the gate
  outcome.
- Claude read-only review may be used if P02 interpretation is ambiguous or if
  a material repair is needed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What does the medium paired quality rung justify next? |
| Baseline/comparator | P02 FP64 paired-reference artifacts and default-impact ladder artifacts. |
| Primary pass criterion | Final result faithfully reflects P02 hard screens, exact comparator definition, tolerance formula/semantics, per-seed/per-output drift evidence, metadata assertions, nonclaims, uncertainty, and next action. |
| Veto diagnostics | Missing artifacts, missing per-seed/per-output drift summary, missing comparator/tolerance semantics, unsupported claim, statistical ranking without uncertainty, treating timing as speedup, or ignoring a hard veto. |
| Explanatory diagnostics | Drift summaries, timing summaries, and next-rung sizing suggestions. |
| Not concluded | No posterior correctness, HMC readiness, sampler convergence, speedup, statistical superiority, or target-shape scientific validity. |
| Artifact | Final result and optional next-rung subplan. |

## Forbidden Claims And Actions

- Do not merge peer low-rank conclusions into this lane.
- Do not call the default scientifically validated from a medium synthetic
  quality screen.
- Do not launch target-shape repeated stability runs in P03.

## Exact Next-Phase Handoff Conditions

The program is complete when:

- the final result exists;
- the stop handoff points to all relevant artifacts;
- any next-rung subplan is clearly marked as not launched.

## Stop Conditions

Stop and ask for direction if:

- P02 artifacts are internally inconsistent;
- the proper next rung would require longer runtime, new model files, funding,
  package installation, or a scientific/default-policy boundary not already
  granted.
