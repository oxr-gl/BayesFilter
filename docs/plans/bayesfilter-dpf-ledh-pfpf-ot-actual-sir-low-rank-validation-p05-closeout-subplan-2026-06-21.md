# P05 Closeout And Claim Classification Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Synthesize phase evidence into a bounded decision label, write final result and
stop handoff, and preserve nonclaims and residual risks.

## Entry Conditions Inherited From Previous Phase

- P04 wrote a result or a documented blocker.
- All required JSON/Markdown artifacts are preserved.
- Any material Claude review findings have been patched or documented.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-result-2026-06-21.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-visible-stop-handoff-2026-06-21.md`
- Updated Claude review ledger.
- Updated visible execution ledger.

## Required Checks, Tests, Reviews

- Verify all referenced result/artifact paths exist.
- Verify final result has decision table, inference-status table, run manifest,
  hard veto status, paired comparability status, runtime/memory status,
  timeout-boundary status, descriptive-only differences, and nonclaims.
- Claude read-only final closeout review until `VERDICT: AGREE` or max five
  rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What bounded decision is supported by the actual-SIR validation artifacts? |
| Baseline/comparator | Existing streaming actual-SIR route and paired P03 artifacts. |
| Primary pass criterion | Final label is supported by phase artifacts without unsupported claim upgrades. |
| Veto diagnostics | Unsupported speedup/default/posterior/API/HMC claim, missing artifact, unreviewed material result, or contradicted phase evidence. |
| Explanatory diagnostics | Runtime/memory/ESS/log-likelihood details not used as unsupported claims. |
| Not concluded | Preserve all nonclaims from the master program. |
| Artifact | Final result, stop handoff, review ledger. |

## Forbidden Claims/Actions

- Do not claim production/default readiness.
- Do not claim posterior correctness or HMC readiness.
- Do not claim broad scalable-OT selection.
- Do not claim dense Sinkhorn equivalence.
- Do not hide failed or timed-out rows.

## Exact Next-Phase Handoff Conditions

There is no next phase. Mark the visible program complete or stopped with a
clear final status and safest next human decision.

## Stop Conditions

- Stop with blocker result if final evidence is internally inconsistent.
- Stop for human direction if changing claim criteria would be necessary.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write final result / close record.
3. Write final stop handoff.
4. Review final result for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
