# P06 Large-N Envelope Subplan

Status: `DRAFT_BLOCKED_UNTIL_P05_PASS`

## Phase Objective

Run large-N actual-SIR envelope diagnostics for the frozen candidate only after
held-out paired support passes, preserving the distinction between executable
envelope and same-row speed evidence.

## Entry Conditions Inherited From Previous Phase

P05 must pass at least two adjacent held-out paired support rows. Without that,
P06 is blocked.

## Required Artifacts

- Large-N aggregate:
  `docs/benchmarks/actual-sir-low-rank-tuning-p06-large-n-envelope-2026-06-22.json`
- Large-N Markdown:
  `docs/benchmarks/actual-sir-low-rank-tuning-p06-large-n-envelope-2026-06-22.md`
- Row artifacts/logs:
  `docs/benchmarks/actual-sir-low-rank-tuning-p06-large-n-envelope-2026-06-22-row-*.json`
  and `docs/benchmarks/logs/actual-sir-low-rank-tuning-p06-large-n-envelope-2026-06-22*.log`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p06-large-n-envelope-result-2026-06-22.md`

## Required Checks/Tests/Reviews

- Start with the smallest next row justified by P05, typically `N=8192` or
  `N=16384`, not `N=50000/100000` immediately.
- Low-rank-only large-N rows may use `warmups=0,repeats=1` and are
  executable-envelope diagnostics only.
- Same-row speed comparison at large N requires streaming under the same row
  policy and timeout boundary.
- Claude read-only review before closeout.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After held-out paired support, how far does the frozen low-rank route execute on larger actual-SIR rows without hard vetoes? |
| Baseline/comparator | P05 held-out support is the comparator basis; same-row large-N comparison only if streaming also runs under the same policy. |
| Primary pass criterion | Large-N row artifacts pass hard validity and preserve GPU/TF32 provenance under predeclared timeout and artifact rules. |
| Veto diagnostics | Hard validity failure, dense materialization, missing provenance, missing artifact, corrupted artifact, or unreviewed jump to unsupported large N. |
| Explanatory diagnostics | Runtime, memory, first-call time, projection iterations, ESS, residuals. |
| Not concluded | Low-rank-only large-N rows do not establish same-row speedup, posterior correctness, HMC readiness, default readiness, or statistical ranking. |
| Artifact | P06 aggregate, row artifacts/logs, phase result. |

## Forbidden Claims/Actions

- Do not run P06 if P05 did not pass.
- Do not call low-rank-only rows paired speed evidence.
- Do not jump directly to `N=50000/100000` unless the refreshed P06 subplan
  justifies the row order from P05 results.
- Do not change product/default policy.

## Exact Next-Phase Handoff Conditions

Advance to P07 after P06 writes its result or after P06 is explicitly blocked by
P05 failure. P07 must classify claims according to the actual phase reached.

## Stop Conditions

- Stop if P05 did not pass.
- Stop if trusted GPU is unavailable for GPU envelope evidence.
- Stop if artifacts cannot be preserved.
- Stop after five unresolved Claude review rounds for the same envelope blocker.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P06 phase result or blocked result.
3. Draft or refresh P07.
4. Review P07 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
