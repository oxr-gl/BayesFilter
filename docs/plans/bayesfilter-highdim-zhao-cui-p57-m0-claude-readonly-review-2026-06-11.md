# P57-M0 Claude Read-Only Review

metadata_date: 2026-06-11
phase: P57-M0
reviewer: Claude Code Opus max-effort, read-only
supervisor: Codex

## Iteration 1

Verdict:

`VERDICT: REVISE`

Summary:

- Claude agreed that M0 substantively satisfied the governance primary
  criterion.
- Claude agreed that `BLOCK_SOURCE_UNGROUNDED` is binding.
- Claude agreed that P52/P53 UKF/rank artifacts are diagnostic-only for
  source-faithful claims.
- Claude agreed that adaptive parity, S&P reproduction, and smoothing are
  correctly excluded from P57 missing gaps.
- Claude found one material weakness: the paper-anchor side was not durable
  enough because M0 still listed ephemeral `/tmp/zhao_cui_jmlr_2024.txt` line
  references and a vague `computeL.m` pointer.

Disposition:

- Accepted.
- M0 result was patched to reject `/tmp` extracted-text paths as durable
  anchors and to require direct paper identifiers plus author source file/line
  anchors, or checked-in artifacts that record those anchors.

## Iteration 1 Verbatim Findings

```text
- Primary criterion: substantively satisfied. The M0 result does record the binding governance rule, demotes P52/P53 UKF/rank work to diagnostic-only for source-faithful claims, and lists required anchors to re-open later (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:10-15`, `:21-39`, `:41-58`, `:72-86`). The subplan's stated pass criterion is therefore met in substance (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-subplan-2026-06-11.md:9-12`).

- `BLOCK_SOURCE_UNGROUNDED` is binding. It is already a checked-in governance rule in `AGENTS.md:32-60`, and M0 correctly reasserts it as binding for P57 (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:21-39`). Good: the lock is not relying on mutable `memory.md` as authority.

- P52/P53 UKF/rank artifacts are correctly treated as diagnostic-only. M0 explicitly forbids using `transition_route.py`, `rank_budget.py` `R_eff`, local/operator routes, all-grid retained storage, or UKF as likelihood/correctness/final-rank evidence for source-faithful Zhao-Cui claims (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:41-58`). This is consistent with the P56 audit's discrepancy ledger (`docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:258-270`).

- Adaptive parity, S&P reproduction, and smoothing are correctly excluded from P57 missing gaps, and the result does not overclaim success. M0 removes them as blockers (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:60-70`), matching P56's explicit non-claims on adaptive parity, S&P, and smoothing (`docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:21`, `:285-295`). It also explicitly says M0 concludes no filtering correctness, rank readiness, HMC readiness, or paper-scale SIR success (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:13-15`).

- Material weakness requiring revision: the paper-anchor side is not durable/self-contained enough for later phases. The "required anchors" still depend on ephemeral `/tmp/zhao_cui_jmlr_2024.txt` line references and even "`computeL.m` anchors recorded in P56 review" (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:80-85`, `:113-118`). For a governance gate whose purpose is to bind later implementation claims, that is a stale-context / artifact-mismatch weakness: later phases could nominally comply while depending on non-durable local extracts instead of a checked-in anchor note or direct equation/algorithm citations. I would tighten M0 so later phases must cite direct paper identifiers (section/equation/algorithm/proposition) plus checked-in source-anchor artifacts, not `/tmp` paths.

VERDICT: REVISE
```

## Iteration 2

Verdict:

`VERDICT: AGREE`

Summary:

- Claude agreed the iteration-1 blocker is closed.
- Claude agreed `/tmp` extracted-text paths are no longer accepted as durable
  anchors in the M0 result.
- Claude agreed later phases are now bound to direct paper identifiers plus
  author source file/line anchors.
- Claude agreed P52/P53 UKF/rank artifacts remain diagnostic-only.
- Claude agreed M0 does not overclaim implementation, filtering, rank, HMC, or
  spatial SIR success.
- Claude noted one residual non-blocking issue: `computeL.m` exact line anchors
  are deferred to the future phase that modifies recentering, but the M0
  governance rule is sufficient because that future phase cannot pass without
  reopening line-level anchors.

## Iteration 2 Verbatim Findings

```text
- Iteration-1 blocker is closed. The M0 result now explicitly rejects ephemeral extracted-text paths as durable anchors: `/tmp/...` extracts may be used only as inspection convenience, while cited evidence must be direct paper identifiers plus author source file and line-level anchors, or a checked-in artifact that records them (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:77-82`). The companion review note records that this was the exact repair made after iteration 1 (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-claude-readonly-review-2026-06-11.md:26-31`), and the visible ledger says the same (`docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-execution-ledger-2026-06-11.md:99-111`).

- Later phases are now correctly bound to direct paper IDs plus source anchors. The binding rule requires both the Zhao-Cui paper/math anchor and the local author source file/line operation before "faithful" or equivalent language is valid (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:25-39`). This matches the checked-in governance rule in `AGENTS.md:32-60`.

- P52/P53 UKF/rank artifacts remain diagnostic-only. M0 still demotes `transition_route.py`, `rank_budget.py` `R_eff`, local/operator routes, all-grid storage, and UKF-based certification to lower-rung diagnostics rather than source-faithful closure evidence (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:41-58`).

- M0 does not overclaim implementation success. The result explicitly says it concludes no filtering correctness, rank readiness, HMC readiness, paper-scale SIR success, or faithful implementation completion (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:13-15`, `:123-129`). The visible ledger likewise preserves those non-claims (`docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-execution-ledger-2026-06-11.md:62-63`).

- Residual issue check: one table entry still defers exact `computeL.m` line anchors to the future phase that modifies recentering (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:90`). I do not consider that material enough to block M0, because M0's repaired governance rule already forbids accepting that later-phase work without reopening line-level anchors at that time (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md:74-82`).

VERDICT: AGREE
```
