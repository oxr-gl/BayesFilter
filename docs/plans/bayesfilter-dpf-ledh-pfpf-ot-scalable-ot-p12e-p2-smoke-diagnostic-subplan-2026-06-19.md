# P12E-2 Subplan: Smoke Diagnostic And Artifact Validation

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md`

## Phase Objective

Run a small smoke diagnostic to `/tmp` using the lane-owned script and validate
that the JSON/Markdown artifacts contain the required fields, diagnostic role
classifications, thresholds, finite checks, fixture provenance, and non-claims.

The smoke result is not the official P12E evidence artifact.

## Entry Conditions Inherited From Previous Phase

- P12E-1 result records pass.
- Diagnostic script exists and passed syntax/import checks.
- Material Claude implementation review converged.
- No shared-contract blocker is open.

## Required Artifacts

- This subplan.
- Smoke JSON:
  `/tmp/scalable-ot-p12e-ledh-sparse-locality-screen-smoke.json`
- Smoke Markdown:
  `/tmp/scalable-ot-p12e-ledh-sparse-locality-screen-smoke.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p2-smoke-diagnostic-result-2026-06-19.md`
- Updated lane status.
- Next subplan, refreshed if needed:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p3-official-diagnostic-subplan-2026-06-19.md`

## Required Checks, Tests, And Reviews

Smoke command:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py \
  --output /tmp/scalable-ot-p12e-ledh-sparse-locality-screen-smoke.json \
  --markdown-output /tmp/scalable-ot-p12e-ledh-sparse-locality-screen-smoke.md
```

Artifact validation:

- bounded JSON structure check for required top-level fields;
- non-claim text check in Markdown;
- finite/status/threshold field presence check;
- fixture provenance and content digest presence check.

Review:

- Claude review is required if smoke artifacts reveal a material contract,
  claim, or boundary issue.
- If smoke only exposes a local formatting/schema omission, Codex may patch and
  rerun focused checks; use Claude if the fix affects interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the lane-owned diagnostic execute on a smoke path and produce structurally valid artifacts without crossing boundaries? |
| Baseline/comparator | Smoke artifacts against reviewed P12E schema expectations and Phase 8-style diagnostics. |
| Primary pass criterion | Smoke command exits 0 and artifacts contain required provenance, finite checks, thresholds, diagnostic roles, decisions, and non-claims. |
| Veto diagnostics | Crash, non-finite required fields, missing provenance/digests, missing threshold roles, unsupported claim, shared-file edit need, or external/GPU/package/network need. |
| Explanatory diagnostics | Smoke metric values; runtime; warnings that do not affect artifacts. |
| Not concluded | No official P12E pass/fail, no sparse implementation validity, no speedup/ranking/posterior/default/HMC/API readiness. |
| Artifact preserving result | Smoke artifacts and P2 result note. |

## Forbidden Claims And Actions

- Do not treat smoke metrics as official evidence.
- Do not update official JSON/Markdown paths in this phase.
- Do not implement sparse solver behavior.
- Do not change thresholds after seeing smoke results.
- Do not edit shared or peer-owned files.

## Exact Next-Phase Handoff Conditions

P12E-3 may begin only if:

- smoke command exits 0;
- smoke artifacts pass validation;
- P2 result note exists;
- current-agent status records smoke completion;
- P12E-3 subplan exists and has passed Codex consistency review;
- no material smoke issue remains unresolved.

## Stop Conditions

Stop and write P2 blocker result if:

- smoke failure cannot be repaired within lane-owned files;
- smoke exposes a shared-contract ambiguity requiring coordinator amendment;
- smoke would require external/GPU/package/network/destructive action;
- interpreting smoke would require a forbidden claim;
- Claude/Codex do not converge after five review rounds for the same material
  blocker.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write the P2 result/close record.
3. Draft or refresh the P12E-3 subplan.
4. Review the P12E-3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
