# P57-M7 Claude Read-Only Review

metadata_date: 2026-06-11
phase: P57-M7
reviewer: Claude Opus via read-only worker
status: AGREE

## Prompt Handling

An initial compact M7 review prompt stalled.  Per the visible runbook
nonresponse protocol, Codex killed only the stalled review worker and ran a
minimal probe through the same Claude worker.  The probe returned `PROBE_OK`,
so Codex shrank the review prompt.

## Review Summary

Claude reviewed the M7 gate claim:

- source-faithful rank selection may pass only with
  `fixed_ttsirt_source_route` comparator evidence;
- no dense or same-route-higher-rank comparator blocks;
- failed tolerances block;
- UKF is `scout_not_truth` only;
- old P52/P53 local/operator `R_eff` rank code cannot close source-faithful
  spatial SIR;
- M7 does not claim d=18 spatial SIR success or HMC readiness.

Claude noted the hidden assumptions that must be operationally enforced:

- the comparator must actually be stronger same-route or dense reference;
- tolerances must be predeclared and matched to the claim;
- a pass means source-faithful rank selection eligibility only, not broader
  readiness.

These assumptions are enforced by `P57RankComparatorEvidence`,
`p57_select_source_faithful_rank(...)`, and focused M7 tests.

## Verdict

```text
VERDICT: AGREE
```
