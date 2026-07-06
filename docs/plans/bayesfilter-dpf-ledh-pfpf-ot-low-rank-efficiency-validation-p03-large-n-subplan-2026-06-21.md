# P03 Large-N Low-Rank Executable-Envelope Ladder Subplan

Status: `DRAFT_AFTER_P02_ROUND_2`

## Phase Objective

Run low-rank-only trusted GPU ladder rows at large particle counts to test
whether the candidate extends the executable LEDH/PFPF-OT envelope beyond
the last completed paired streaming comparison.  This phase does not establish
superiority over streaming at unpaired sizes.

## Entry Conditions Inherited From Previous Phase

P02 must have produced a valid paired result or bounded failure result.  P03
inherits the selected physical GPU and TF32 state.  If the selected GPU changes
mid-phase, rows before and after the change cannot be combined into one large-N
claim.  P03 must not make speed claims from low-rank-only rows.

## Required Artifacts

- Large-N JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json`
- Large-N Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p03-large-n-result-2026-06-21.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-efficiency-p03-large-n.log`

## Required Checks, Tests, And Reviews

- Trusted/elevated GPU command with selected GPU.
- Fixed per-row timeout: `1200s` wall time for every P03 low-rank row.
- Low-rank rows at `N=50000` and conditional `N=100000`; if P02 already
  paired either size successfully, P03 records that row as paired-context
  evidence instead of low-rank-only evidence.
- JSON inspection for finite output, route-fired evidence, no dense transport,
  TF32 state, selected physical GPU, timeout status, and memory/runtime fields.
- Claude review if large-N pass is used in final envelope claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does low-rank run large-particle LEDH/PFPF-OT rows beyond the last completed streaming comparator while preserving hard validity and nonmaterialization checks? |
| Baseline/comparator | P02 paired streaming context and the first fixed streaming timeout/OOM/failure boundary, if observed.  Dense memory infeasibility may explain why no dense 50k/100k materialization is attempted, but dense infeasibility is not the primary comparator for an efficiency claim. |
| Primary pass criterion | `N=50000` passes hard validity and nonmaterialization checks; `N=100000` is attempted only if 50k passes and is recorded as pass/fail/skipped. |
| Veto diagnostics | Low-rank validity failure, missing route-fired evidence, dense transport materialized, TF32 state mismatch/off for TF32 claim, mixed physical GPU without restart, timeout/resource failure, missing artifact, or unsupported speed/posterior/default claim. |
| Explanatory diagnostics | Runtime, memory, ESS/output previews, and dense materialization byte estimates. |
| Not concluded | No speedup by itself, no superiority over streaming at an unpaired size, no posterior correctness, no HMC readiness, no public API readiness, no production/default readiness, no dense Sinkhorn equivalence, and no broad scalable-OT selection. |
| Artifact | P03 JSON/Markdown/result/log. |

## Forbidden Claims And Actions

- Do not call large-N low-rank-only completion a speedup.
- Do not call large-N low-rank-only completion more efficient than streaming at
  that `N` unless streaming was actually paired under P02 rules.
- Do not attempt dense 50k/100k materialization.
- Do not use GPU0 if GPU1 is available without recording why.
- Do not change public defaults.

## Exact Next-Phase Handoff Conditions

P04 may start once P03 writes a pass/fail/blocker result with explicit
large-N validity status and claim boundaries.

## Stop Conditions

- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_GPU_UNAVAILABLE`
- `LOW_RANK_LEDH_EFFICIENCY_NOT_SUPPORTED_CURRENT_EVIDENCE`
- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the P03 result/close record.
3. Draft or refresh P04 subplan.
4. Review P04 for consistency, correctness, feasibility, artifact coverage, and boundary safety.
