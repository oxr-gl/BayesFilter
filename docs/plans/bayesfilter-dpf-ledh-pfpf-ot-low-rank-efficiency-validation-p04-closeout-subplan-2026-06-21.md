# P04 Final Efficiency Closeout And Claim Audit Subplan

Status: `DRAFT_AFTER_P03_ROUND_2`

## Phase Objective

Write the final efficiency result, separating bounded paired resource-proxy
efficiency support, executable-envelope support, validity failures, and
non-claims.

## Entry Conditions Inherited From Previous Phase

P03 must have written a pass/fail/blocker result.  P04 must not synthesize with
the positive-feature lane and must not claim posterior correctness or default
readiness.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-result-2026-06-21.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-visible-execution-ledger-2026-06-21.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-visible-stop-handoff-2026-06-21.md`

## Required Checks, Tests, And Reviews

- Artifact existence checks for all phase results on the observed path.
- Non-claim `rg` check over final result.
- JSON consistency checks for P02/P03 statuses and claim class.
- Claude read-only review if final result supports bounded efficiency or
  executable-envelope support.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What efficiency claim, if any, is supported by the governed evidence? |
| Baseline/comparator | P02 paired streaming evidence and P03 large-N low-rank evidence with explicit paired/unpaired classification for each row. |
| Primary pass criterion | Final result accurately classifies evidence as bounded paired resource-proxy efficiency support, executable-envelope support only, unsupported current evidence, or blocker. |
| Veto diagnostics | Unsupported speedup/ranking claim, missing artifact, conflating large-N low-rank-only completion with streaming superiority, ignoring validity/TF32/same-GPU/output-comparability vetoes, or changing thresholds/timeouts post hoc. |
| Explanatory diagnostics | Runtime/memory tables, GPU selection, TF32 state, paired boundary, large-N rows, and dense materialization byte estimates. |
| Not concluded | No posterior correctness, dense Sinkhorn equivalence, HMC readiness, public API readiness, production/default readiness, or broad scalable-OT selection. |
| Artifact | Final result and ledger. |

## Forbidden Claims And Actions

- Do not perform mid-lane synthesis with other Wave 2 lanes.
- Do not rank methods statistically without uncertainty evidence.
- Do not claim default readiness.
- Do not claim streaming superiority at unpaired 50k/100k rows.
- Do not change code except closeout docs.

## Exact Next-Phase Handoff Conditions

There is no next phase.  Final handoff must state the claim class, artifacts,
validity vetoes, GPU used, and what remains unproven.

## Stop Conditions

- Missing required evidence artifact.
- Unsupported claim cannot be patched without changing result meaning.
- Claude review nonconvergence after five rounds for the same final blocker.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write final result/close record.
3. Refresh stop handoff.
4. Review final result for consistency, correctness, artifact coverage, and boundary safety.
