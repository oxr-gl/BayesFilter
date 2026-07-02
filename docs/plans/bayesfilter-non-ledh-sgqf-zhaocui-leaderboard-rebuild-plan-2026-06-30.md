# Non-LEDH SGQF/Zhao-Cui Leaderboard Rebuild Plan

Date: 2026-06-30

## Objective

Rebuild the BayesFilter leaderboard artifacts with fixed SGQF included and
LEDH/PFPF-OT omitted for this pass. The rebuild must use fresh dated artifacts
rather than mutating the June 24 leaderboard results in place.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current non-LEDH leaderboard include SGQF and the post-P91 Zhao-Cui evidence without reviving stale blocker labels or overclaiming scope? |
| Baseline/comparator | Existing June 24 two-lane leaderboard scripts and artifacts, plus P91 Zhao-Cui SIR d18 scoped readiness artifacts. |
| Primary criterion | New June 30 leaderboard artifacts list SGQF as a first-class algorithm where same-target support exists, explicitly omit LEDH/PFPF-OT algorithms, and preserve blocker/status-only labels where target support is missing. |
| Veto diagnostics | Any LEDH/PFPF-OT row emitted; any P91 Zhao-Cui local-complete-data evidence represented as full observed-data/filtering readiness; any actual-SV/KSC-SV target merge; any SGQF row admitted without same-target support or explicit status-only/blocker classification; any overall-winner claim. |
| Explanatory diagnostics | Per-row algorithm status, target contract status, absolute value gaps where a reference exists, runtime fields where measured, and reason codes for blocked/status-only cells. |
| Not concluded | No LEDH/DPF transport comparison, no overall winner, no full observed-data Zhao-Cui SIR filtering score readiness, no universal SGQF superiority, no production-GPU timing claim unless separately run under GPU policy. |
| Artifact | `docs/plans/bayesfilter-non-ledh-sgqf-zhaocui-leaderboard-*-2026-06-30.{json,md}` plus this plan and a result note if execution runs. |

## Skeptical Plan Audit

| Risk | Guardrail |
| --- | --- |
| Wrong baseline | Use June 24 leaderboard emitters only as prior scaffolding; write June 30 artifacts. |
| Proxy metrics promoted | Runtime and value gaps are reported as row diagnostics only, not as proof of scientific validity. |
| Stale Zhao-Cui blocker drift | Replace stale P8D SIR adapter-required labels only where P91 scope applies; preserve full filtering blockers. |
| Hidden LEDH inclusion | Emit explicit `excluded_algorithms` and check generated rows for `ledh`/`pfpf` algorithm ids. |
| Unfair comparisons | Mark rows as rankable only when they share the same target and reference semantics. |
| Environment mismatch | CPU-only leaderboard commands hide GPU before TensorFlow import; GPU timing is out of scope for this pass. |
| Missing stop conditions | Stop if an emitted row violates the non-LEDH exclusion, same-target contract, or P91 scope boundary. |

Audit status: passed for a scoped non-LEDH leaderboard rebuild. Execution may
begin with local CPU-only checks and artifact emission.

## Planned Edits

1. Refresh the lowdim leaderboard emitter to use 2026-06-30 artifact names and
   include fixed SGQF on same-target LGSSM rows when the direct affine SGQF
   route is available.
2. Refresh the highdim leaderboard emitter to use 2026-06-30 artifact names,
   explicitly exclude LEDH/PFPF-OT, retain SGQF cells already admitted, and add
   P91 Zhao-Cui status/evidence only under its scoped local-complete-data SIR
   d18 component route.
3. Add checks that generated row algorithm ids do not contain LEDH/PFPF-OT
   identifiers.
4. Run focused local checks before any full benchmark interpretation.

## Required Checks

- `python -m py_compile docs/benchmarks/benchmark_two_lane_lowdim_leaderboard.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- A CPU-only low-repeat artifact smoke for each leaderboard emitter.
- `rg -n "ledh|pfpf" <new artifact paths>` must show only exclusion/nonclaim
  text, not emitted row algorithm ids.
- `git diff --check -- <changed files>`

## Stop Conditions

- Any generated row has a LEDH/PFPF-OT algorithm id.
- Any Zhao-Cui SIR d18 source-scope filtering row is promoted using only P91
  local-complete-data evidence.
- Any SGQF row is rankable without same-target support.
- Any command needs GPU/CUDA; that requires a separate trusted GPU plan.
