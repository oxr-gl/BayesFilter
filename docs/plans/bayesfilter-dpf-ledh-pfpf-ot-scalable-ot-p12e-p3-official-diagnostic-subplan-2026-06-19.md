# P12E-3 Subplan: Official Diagnostic

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md`

## Phase Objective

Run the official P12E LEDH sparse-locality screen and write the lane-owned
JSON/Markdown diagnostic artifacts.

This phase produces the official diagnostic evidence but does not write the
final interpretation result note.

## Entry Conditions Inherited From Previous Phase

- P12E-2 result records pass.
- Smoke artifacts validated required fields and non-claims.
- No unresolved smoke artifact issue remains.
- No shared-contract blocker is open.

## Required Artifacts

- This subplan.
- Official JSON:
  `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json`
- Official Markdown:
  `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p3-official-diagnostic-result-2026-06-19.md`
- Updated lane status.
- Next subplan, refreshed if needed:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p4-closeout-handoff-subplan-2026-06-19.md`

## Required Checks, Tests, And Reviews

Official command:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py \
  --output docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json \
  --markdown-output docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md
```

Post-run validation:

- JSON readability and required fields;
- finite/dense/truncated status fields;
- fixture provenance, seeds, observation maps, covariance settings, and
  content digests;
- diagnostic role classifications;
- decision status belongs to the approved status family;
- Markdown non-claims.

Review:

- Claude read-only review is required for official diagnostic artifacts before
  P12E-4 closeout if any result is used to reopen sparse implementation
  planning.
- If the official result blocks sparse reopening with clean artifacts and no
  boundary issue, Claude review may be deferred to P12E-4 final closeout.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What do the official deterministic LEDH-like fixture diagnostics say under the predeclared locality/truncation thresholds? |
| Baseline/comparator | Dense TensorFlow transport on the same LEDH-like post-flow particles, preserving Phase 1/Phase 8 orientation and truncation semantics. |
| Primary pass criterion | Official JSON/Markdown artifacts exist, are readable, preserve required fields/non-claims, and record a valid decision status. |
| Reopen criterion | Every fixture passes all reviewed threshold and finite/provenance checks. |
| Block criterion | Any fixture fails a reviewed threshold or finite/provenance check. |
| Veto diagnostics | Artifact unreadable; required field missing; unsupported claim; threshold drift; non-finite required artifact; external/GPU/package/network need; shared-file edit need. |
| Explanatory diagnostics | Runtime, memory, support curves outside the 99% screen, nearest-neighbor mass, LEDH log-det ranges, and descriptive Phase 8 comparison. |
| Not concluded | No sparse solver validity, no speedup, no ranking, no posterior correctness, no HMC readiness, no public API/default readiness. |

## Forbidden Claims And Actions

- Do not write final synthesis or compare against peer lane.
- Do not change thresholds after seeing official results.
- Do not implement sparse solver behavior.
- Do not claim sparse speedup, ranking, posterior correctness, HMC readiness,
  public API readiness, production/default readiness, or general sparse-OT
  validity.
- Do not edit shared or peer-owned files.

## Exact Next-Phase Handoff Conditions

P12E-4 may begin only if:

- official command exits 0 or a precise blocker result is written;
- official artifacts exist and pass artifact validation, or the blocker says
  why not;
- P3 result note exists;
- current-agent status records `DIAGNOSTIC_RUN_COMPLETE` or a blocker;
- P12E-4 subplan exists and has passed Codex consistency review.

## Stop Conditions

Stop and write P3 blocker result if:

- official diagnostic cannot produce valid artifacts within lane-owned files;
- result interpretation would require changing thresholds or forbidden claims;
- external/GPU/package/network/destructive action is required;
- shared schema/baseline/peer-file edits are required.
- Claude/Codex do not converge after five review rounds for the same material
  official-diagnostic blocker.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write the P3 result/close record.
3. Draft or refresh the P12E-4 subplan.
4. Review the P12E-4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
