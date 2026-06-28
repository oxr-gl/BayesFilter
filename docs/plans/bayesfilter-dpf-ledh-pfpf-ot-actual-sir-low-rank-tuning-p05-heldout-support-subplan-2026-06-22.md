# P05 Held-Out Paired Support Ladder Subplan

Status: `DRAFT_AFTER_P04`

## Phase Objective

Run held-out paired actual-SIR support rows for the frozen candidate and decide
whether bounded efficiency support exists under the predeclared gates.

## Entry Conditions Inherited From Previous Phase

P04 must freeze exact candidate parameters. Held-out rows and seeds must be
recorded before execution.

## Required Artifacts

- Held-out aggregate:
  `docs/benchmarks/actual-sir-low-rank-tuning-p05-heldout-support-2026-06-22.json`
- Held-out Markdown:
  `docs/benchmarks/actual-sir-low-rank-tuning-p05-heldout-support-2026-06-22.md`
- Row artifacts/logs:
  `docs/benchmarks/actual-sir-low-rank-tuning-p05-heldout-support-2026-06-22-row-*.json`
  and `docs/benchmarks/logs/actual-sir-low-rank-tuning-p05-heldout-support-2026-06-22*.log`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p05-heldout-support-result-2026-06-22.md`

## Required Checks/Tests/Reviews

- First held-out support row: `B=5,T=20,N=1024`, held-out or partly held-out
  seeds not used as the sole tuning basis.
- For this program, adjacent support rows mean adjacent entries in the
  predeclared held-out ladder, not powers-of-two adjacency:
  `N=1024 -> N=4096 -> N=8192`.
- Second adjacent support row: `B=5,T=20,N=4096` only if `N=1024` passes hard
  validity, paired comparability, same-GPU provenance, and warm-time screen.
- GPU1 is preferred unless busy/unavailable; every paired support row must
  record the physical GPU UUID and must not mix UUIDs within the row.
- Claude read-only review of support interpretation before P06.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the frozen candidate pass held-out paired actual-SIR support gates? |
| Baseline/comparator | Compiled streaming actual-SIR TF32/GPU route on the same physical GPU UUID. |
| Primary pass criterion | At least two adjacent paired support rows pass hard validity, paired comparability, same-GPU provenance, TF32 provenance, and warm-time ratio `>= 1.25`. |
| Veto diagnostics | Any hard validity failure, paired comparability failure on a required row, same-GPU UUID mismatch, missing TF32/GPU provenance, missing artifacts, or speed screen failure after comparability. |
| Explanatory diagnostics | Runtime distribution, memory, ESS, projection iterations, residuals, first-call time. |
| Not concluded | No posterior correctness, HMC readiness, default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or statistical ranking. |
| Artifact | P05 aggregate, row artifacts/logs, phase result, Claude review ledger. |

## Forbidden Claims/Actions

- Do not continue to `N=4096` if `N=1024` fails.
- Do not continue to large-N envelope if held-out support fails.
- Do not claim speedup before hard validity and paired comparability pass.
- Do not treat low-rank-only rows as same-row speed comparison.

## Exact Next-Phase Handoff Conditions

Advance to P06 only if P05 passes the primary criterion. If P05 passes validity
and comparability but fails warm-time support, write `ROUTE_REPAIR_REQUIRED`.
If P05 fails comparability or hard validity, write `TUNING_REQUIRED` or blocker
according to the result cause.

## Stop Conditions

- Stop if the first held-out row fails hard validity or paired comparability.
- Stop if same-GPU provenance cannot be preserved.
- Stop if trusted GPU is unavailable for support evidence.
- Stop after five unresolved Claude review rounds for the same support blocker.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P05 phase result.
3. Draft or refresh P06 only if P05 passes.
4. Review P06 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
