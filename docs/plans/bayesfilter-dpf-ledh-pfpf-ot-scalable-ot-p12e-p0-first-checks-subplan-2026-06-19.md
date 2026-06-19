# P12E-0 Subplan: Intake, Governance, And First Checks

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md`

## Phase Objective

Confirm that the current-agent lane governance is coherent, that the reviewed
P12E evidence contract is in force, and that the minimal local prerequisites
for later LEDH sparse-locality diagnostic implementation are available.

This phase does not implement the diagnostic and does not run the P12E
diagnostic.

## Entry Conditions Inherited From Previous Phase

- Wave 1 coordinator record exists and says exactly two active agents:
  `peer agent` and `current agent`.
- Current-agent status records `SUBPLAN_WRITTEN_CLAUDE_REVIEW_AGREE`.
- The P12E master program exists and lists this phase.
- The reviewed P12E umbrella subplan exists.
- No coordinator question or shared-contract blocker is open.

## Required Artifacts

- This subplan.
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p0-first-checks-result-2026-06-19.md`
- Updated lane status:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md`
- Next subplan, refreshed if needed:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p1-diagnostic-implementation-subplan-2026-06-19.md`

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/scalable_ot_p08_sparse_locality_diagnostics.py
CUDA_VISIBLE_DEVICES=-1 python -c "from experiments.dpf_implementation.tf_tfp.flows.ledh_tf import ledh_flow_batch_tf; print(ledh_flow_batch_tf.__name__)"
```

Review:

- Codex skeptical audit before running commands.
- Claude review is not required after P0 if both checks pass and no plan text
  changes materially affect evidence, claims, or boundaries.
- If either check fails for a fixable planning or import-path reason, patch the
  relevant lane-owned subplan/result/status artifact and ask Claude for
  read-only focused review before proceeding.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the inherited Phase 8 locality code and TensorFlow LEDH flow import path locally usable before implementing the P12E diagnostic? |
| Baseline/comparator | Read-only Phase 8 diagnostic script and `ledh_flow_batch_tf` import path. |
| Primary pass criterion | Both required commands exit 0 and the lane status is updated with exact command results. |
| Veto diagnostics | Phase 8 diagnostic script syntax failure; CPU-scoped LEDH import failure; TensorFlow import requires GPU/trusted hardware evidence; any needed edit outside lane-owned files. |
| Explanatory diagnostics | TensorFlow warnings that do not prevent import; exact printed function name. |
| Not concluded | No P12E diagnostic validity, no sparse locality result, no sparse implementation validity, no speedup/ranking/posterior/default/HMC/API readiness. |
| Artifact preserving result | P0 result note and current-agent status update. |

## Forbidden Claims And Actions

- Do not implement or run the P12E diagnostic.
- Do not edit Phase 1, Phase 3, Phase 8, peer-agent, shared ledger,
  shared stop-handoff, public API, or default-policy files.
- Do not claim sparse locality is present or absent.
- Do not claim speedup, ranking, posterior correctness, HMC readiness, public
  API readiness, production/default readiness, or sparse solver validity.

## Exact Next-Phase Handoff Conditions

P12E-1 may begin only if:

- both P0 local checks pass;
- P0 result note exists;
- current-agent status records `FIRST_CHECKS_RUN`;
- P12E-1 subplan exists and has passed Codex consistency review;
- no human-required stop condition is open.

## Stop Conditions

Stop and write the P0 result as blocked if:

- either required check fails and the failure cannot be repaired within
  lane-owned files;
- GPU/trusted hardware evidence, package install, network fetch, credentials,
  external solver execution, or destructive action would be required;
- resolving the failure would require shared schema/baseline/ledger/peer-file
  edits;
- interpreting the phase would require a forbidden claim.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the P0 result/close record.
3. Draft or refresh the P12E-1 subplan.
4. Review the P12E-1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
