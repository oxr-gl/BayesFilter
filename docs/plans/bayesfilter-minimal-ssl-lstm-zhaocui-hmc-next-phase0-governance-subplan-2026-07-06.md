# Phase 0 Subplan: Governance And Review Setup

Date: 2026-07-06

Status: `COMPLETE`

## Phase Objective

Establish the new three-branch program, evidence contract, review path, and
boundary gates before any runtime-code extraction, GPU/XLA command, or longer
sampler diagnostic.

## Entry Conditions Inherited From Previous Phase

- The predecessor minimal scalar CPU-hidden HMC ladder is complete.
- Predecessor closeout and reset memo state that only CPU-hidden mechanics
  evidence was established.
- Dirty worktree state must be preserved.
- Claude may be read-only reviewer only; Codex remains supervisor/executor.

## Required Artifacts

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-program-master-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-visible-execution-ledger-2026-07-06.md`
- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-phase1-review-bundle-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-governance-result-2026-07-06.md`
- Draft Phase 1 subplan.

## Required Checks, Tests, Reviews

- `git status --short`
- `python -m compileall -q docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- Forbidden-claim scan across new plan files:
  `rg -n "source-faithful|convergence|posterior correctness|default readiness|production readiness|superior|best|LEDH" docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-*.md docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-*.md`
- Material review:
  - first attempt Claude review gate with compact bundle, `--model opus`,
    `--effort max`;
  - if Claude is unavailable or external review is denied, use a fresh
    Codex-agent read-only review and record the fallback.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the next program sufficiently gated to start with internal adapter extraction while preserving GPU/XLA and longer-diagnostics boundaries? |
| Baseline/comparator | Predecessor closeout/reset memo and benchmark/test harness. |
| Primary pass criterion | Required artifacts exist, skeptical audit passes, review path is recorded, and no plan text claims evidence not yet produced. |
| Veto diagnostics | Missing artifact, unsupported claim, unapproved boundary crossing, stale predecessor status, missing stop condition, no review path, or plan that treats CPU debug evidence as GPU/default/convergence evidence. |
| Explanatory diagnostics | File inventory, git status preview, review gate status, and local compile result. |
| Not concluded | Runtime correctness after extraction, GPU/XLA behavior, HMC convergence, posterior correctness, ranking, source-faithful parity, default readiness, or LEDH result. |
| Artifact preserving result | Phase 0 result file and ledger entry. |

## Forbidden Claims And Actions

- Do not edit runtime code in Phase 0.
- Do not run HMC, GPU/CUDA/XLA, long sampler diagnostics, detached agents, or
  package/network commands.
- Do not claim convergence, posterior correctness, ranking, source-faithful
  parity, GPU/XLA readiness, default readiness, or LEDH evidence.
- Do not treat Claude fallback/no-response as proof of correctness.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only if:

- required plan/runbook/ledger/review-bundle artifacts exist;
- compile check passes;
- skeptical audit is recorded as passed or repaired;
- material review returns `VERDICT: AGREE` through Claude or documented Codex
  substitute review;
- Phase 1 subplan is refreshed and reviewed.

## Stop Conditions

Stop and write a blocker result if:

- material review returns unfixable `REVISE`;
- five review rounds for the same blocker do not converge;
- required predecessor artifacts are missing or contradictory;
- continuing requires unapproved GPU/long-run/default/API/model-file boundary;
- local checks fail and the repair is not clearly Phase 0-scoped.

## End-Of-Phase Requirements

At the end of Phase 0:

1. run required local checks;
2. write the Phase 0 result/close record;
3. draft or refresh Phase 1 subplan;
4. review Phase 1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
