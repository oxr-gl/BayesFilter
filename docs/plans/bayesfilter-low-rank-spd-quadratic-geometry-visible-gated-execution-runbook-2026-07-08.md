# Low-Rank SPD Quadratic Geometry Visible Gated Execution Runbook

Date: 2026-07-08
Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only. Claude cannot authorize human, runtime, model-file, funding, product, release, public-benchmark, default-policy, or scientific-claim boundaries.

This runbook is visible and recoverable inside the current conversation. It must not launch detached or nested execution.

## Program

Master program:

- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-master-program-2026-07-08.md`

Execution ledger:

- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-visible-execution-ledger-2026-07-08.md`

Stop handoff:

- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-visible-stop-handoff-2026-07-08.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, plan, and review gate | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase0-governance-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase0-governance-result-2026-07-08.md` |
| 1 | General utility and focused unit tests | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase1-utility-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase1-utility-result-2026-07-08.md` |
| 2 | Minimal SSL-LSTM diagnostic integration | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase2-minimal-ssl-lstm-integration-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase2-minimal-ssl-lstm-integration-result-2026-07-08.md` |
| 3 | Focused checks and bounded CPU-hidden diagnostic | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase3-checks-diagnostic-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase3-checks-diagnostic-result-2026-07-08.md` |
| 4 | Closeout and next handoff | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase4-closeout-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase4-closeout-result-2026-07-08.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a reusable low-rank SPD quadratic geometry utility be implemented and tried as a non-promoting minimal SSL-LSTM diagnostic geometry path? |
| Baseline/comparator | Existing Phase 5 initial geometry path and 2026-07-07 geometry/tau-gate result. |
| Primary pass criterion | Focused utility/integration checks pass and bounded diagnostic writes structured provenance or honest fallback. |
| Veto diagnostics | Failed tests, invalid SPD/condition/sample gates, missing provenance, unsupported scientific/default-readiness claims. |
| Explanatory diagnostics | Fit residuals, condition number, score norm, HMC acceptance, runtime, tau summaries. |
| Not concluded | Posterior correctness, convergence, zero divergences, statistical ranking, superiority, default readiness, GPU/XLA readiness, Zhao-Cui source-faithfulness. |
| Artifacts | Phase docs, review bundle/status, logs, JSON/Markdown diagnostic artifacts. |

## Skeptical Plan Audit

Before each phase, Codex must verify:

- no wrong baseline;
- no proxy metric promoted to a scientific or runtime claim;
- stop conditions remain active;
- comparisons are not ranking claims;
- assumptions and numeric defaults are labeled;
- CPU-hidden diagnostics are not GPU evidence;
- commands write artifacts that answer the phase question.

Current audit status: `PASS_WITH_BOUNDARIES` for Phase 0 planning and review.

## Quiet Visible Execution Pattern

Commands expected to produce large output must write logs under `docs/benchmarks/` or `/tmp` and only summarized output should be shown in chat. Full logs must be referenced from result notes.

## Review Gate

Material review uses:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name bayesfilter-low-rank-spd-quadratic-geometry-phase0 \
  --bundle /home/ubuntu/python/BayesFilter/docs/reviews/bayesfilter-low-rank-spd-quadratic-geometry-phase0-review-bundle-2026-07-08.md \
  --probe-timeout 90 \
  --timeout-seconds 120 \
  --max-retries 1 \
  --allow-bounded-fallback
```

If Claude review is blocked or unavailable, write a Codex substitute review and record that it is weaker than full external review.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch, credentials, destructive git/filesystem actions, default-policy changes, public API/release claims, model-file edits, or scientific/runtime claims not already permitted by the plan.
