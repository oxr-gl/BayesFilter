# P9 Subplan: Integration Closeout

metadata_date: 2026-06-10
phase: FILTER_BENCH_P9
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Close the filtering benchmark gap-closure program and decide whether the
filtering part of BayesFilter is ready to hand off to Bayesian estimation.
Because P8 has been revised to the synthetic-truth likelihood-geometry
contract, P9 must distinguish a passed benchmark-contract gate from a completed
numeric benchmark run.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Have the pre-benchmark gaps and the revised P8 synthetic-truth benchmark contract been closed enough to trust filtering for Bayesian-estimation handoff? |
| Baseline/comparator | P0-P8 phase results and the benchmark outputs. |
| Primary criterion | Closeout result makes a decision, using engineering completeness, numerical validity, and scientific interpretation ledgers, on whether filtering is ready to hand off to Bayesian estimation. |
| Veto diagnostics | Any phase skipped; any benchmark hole unexplained; old LEDH-PFPF-OT treated as current; exactness overclaimed outside LGSSM; DPF gradient invalidity hidden; P8 numeric benchmark still pending while handoff is claimed. |
| Explanatory diagnostics | Claude review ledger, result matrices, run manifests, post-run red-team notes. |
| Not concluded | No Bayesian-estimation implementation has begun. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p9-closeout-result-2026-06-11.md` |

## Tasks

- Emit a decision table with decision, primary criterion status, veto diagnostic
  status, main uncertainty, next justified action, and what is not concluded.
- Separate engineering completeness, numerical validity, and scientific
  interpretation.
- Summarize P0-P8 pass/block status, including both
  `PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT` and
  `BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING`.
- Link all artifacts.
- State which algorithm/model cells remain diagnostic-only or invalid.
- State which diagnostic-only or approximation-only cells are acceptable for
  filtering closeout and which would force a block.
- State handoff stop conditions for Bayesian estimation: unexplained holes,
  benchmarkable value/gradient rows without reference-gradient policy,
  invalid-gradient cells hidden from matrices, old LEDH-PFPF-OT current evidence,
  exactness overclaimed outside LGSSM, missing frozen roster, missing
  preflight/full-run manifests, or P8 numeric execution still pending must block
  handoff.
- State what the benchmark supports and what it does not support.
- Produce the handoff decision for Bayesian estimation.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P9_CLOSEOUT` only if P0-P8 have durable artifacts,
the benchmark matrices/contracts have no silent holes, the remaining
limitations are explicit, and the decision table justifies handoff to Bayesian
estimation under the predeclared stop conditions.  Block if filtering closeout
evidence is incomplete, if P8 numeric benchmark execution is still pending, or
if remaining limitations invalidate the handoff.

## Validation

- Claude closeout review, max five iterations.
- Focused artifact existence checks.
