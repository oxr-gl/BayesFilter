# P26 Zhao--Cui Claude Review Ledger

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P25 Zhao--Cui chair and implementation bridge note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.
- No Claude review has been completed yet.

## Status

status: `PLAN_REVIEW_ITERATION_1_PATCHED`

## Plan Review Iteration 1

reviewer: Claude Code bounded hostile reviewer

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p26-zhao-cui-panel-readable-plan-review-iter1 \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Claude final decision: `REVISE`

Codex audit classifications:

| Finding | Claude class | Codex class | Control added |
|---|---:|---:|---|
| P25 preservation needs more than line-count gate. | `MAJOR` | `ACCEPT` | Added section-preservation hard stop condition. |
| Validation checks must be release-blocking. | `MAJOR` | `ACCEPT` | Added final-acceptance hard stop for build/log/equation/whitelist checks. |
| Excerpt-review fallback needs minimum excerpt set. | `MAJOR` | `ACCEPT` | Added required excerpt set for bounded review fallback. |
| Cross-agent review must run in trusted context. | `MAJOR` | `ACCEPT` | Added trusted/elevated Claude review requirement. |
| Dirty-worktree gate needs whitelist snapshots. | `MINOR` | `ACCEPT` | Added pre/post `git status --short` whitelist gate. |
| Anti-overclaim guard is strong. | `ACCEPT` | `ACCEPT` | No patch needed. |
| Requested content changes are actionable. | `ACCEPT` | `ACCEPT` | No patch needed. |
| Write scope is appropriately constrained. | `ACCEPT` | `ACCEPT` | No patch needed. |

No Claude finding was disputed.

## Execution Review Iteration 1

reviewer: Claude Code bounded hostile reviewer

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p26-zhao-cui-panel-readable-exec-review-iter1 \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Claude final decision: `REVISE`

Codex audit classifications:

| Finding | Claude severity | Codex class | Control added or rationale |
|---|---:|---:|---|
| Section title `End of Zhao and Cui Annotation and Start of BayesFilter Fixed-Branch Extension` is process/version framing. | `MAJOR` | `ACCEPT` | Rename to a mathematical reader-facing fixed-branch title and remove transition tone. |
| Main note still uses process-sounding prose such as stored object, persisted state, metadata, workflow, report field. | `MAJOR` | `PARTIAL` | Replace visible non-human terms where they are internal/process wording. Retain mathematically necessary storage/evaluator language when it specifies implementation contract. |
| Defaults table lacks explicit one-to-one rows for \(\lambda_t\), \(c_t\), and residual tolerance. | `MAJOR` | `ACCEPT` | Expand defaults table with explicit rows for defensive reference, shift policy, target floor, sweep residual tolerance, relative normalizer tolerance, retained normalization tolerance, compression tolerances, and finite-difference schedule. |
| Preconditioning teach-back needs a compact chair-facing paragraph tying bridge, KR, and proposal construction together. | `MEDIUM` | `ACCEPT` | Add a short math-first paragraph after the preconditioning/KR equations. |
| Boxed algorithm cites only recomputation equations through 10, missing right-to-left and stale-cache equations 11--12. | `MEDIUM` | `ACCEPT` | Update boxed algorithm reference to include \eqref{eq:p26-sweep-recompute-12} and state stale cached environments must be refreshed. |
| Compressed retained-filter storage needs compact failure diagnostics. | `MEDIUM` | `ACCEPT` | Add a diagnostics table for normalization drift, derivative-mass drift, compression residual, derivative compression residual, and query evaluator mismatch. |
| Trace should explicitly point to the numeric finite-difference comparison. | `MINOR` | `ACCEPT` | Add a sentence linking the trace finite-difference definition to the displayed synthetic table. |
| BayesFilter branding remains visible. | `MINOR` | `PARTIAL` | Remove internal project framing in section titles/prose where visible. Retain `BayesFilter Technical Note` author and `BayesFilter notation` where scholarly context requires it. |

No execution-review finding was disputed.

## Execution Review Iteration 3

reviewer: Claude Code bounded hostile reviewer

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p26-zhao-cui-panel-readable-exec-review-iter3 \
  --model sonnet --effort high \
  "<narrow final cleanup review prompt>"
```

Claude final decision: `ACCEPT`

Claude confirmed:

- No visible `BayesFilter` branding remains in the main note.
- No visible `lane` / `Lane` wording remains in the main note.
- No `Data Structures` section title remains.
- No visible `ledger`, `artifact`, `governance`, `Claude`, `Codex`,
  `manifest`, or `P25 lane` terms remain.
- Internal LaTeX labels such as `eq:p25-...` remain but are not visible in the
  rendered note.

Codex audit classification: `ACCEPT`.

## Execution Review Iteration 2

reviewer: Claude Code bounded hostile reviewer

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p26-zhao-cui-panel-readable-exec-review-iter2 \
  --model sonnet --effort high \
  "<focused iteration-2 execution review prompt>"
```

Claude final decision: `REVISE`

Codex audit classifications:

| Finding | Claude severity | Codex class | Control added or rationale |
|---|---:|---:|---|
| Internal `BayesFilter` branding remains visible in main note. | `BLOCKER` | `ACCEPT` | Remove or neutralize visible project branding in title/author, section title, equation-introduction prose, and relation appendix; replace with neutral `this note` / `fixed-branch notation` phrasing. |
| Forbidden `lane` wording remains visible. | `BLOCKER` | `ACCEPT` | Rename `Consolidated Fixed Least-Squares Lane`; replace visible `lane` wording with `fixed least-squares formulation`, `specialization`, or `construction`. |
| Section title `Implementable Fixed-Branch Objects And Data Structures` sounds too internal. | `BLOCKER` | `ACCEPT` | Retitle to `Fixed-Branch Objects And Array Shapes`. |

Resolved items confirmed by Claude iteration 2:

- Original process divider removed.
- Defaults table now includes \(\lambda_t,\tau_t,c_t\) and floor/ridge/threshold/tolerance terms.
- Preconditioning teach-back bridge/KR paragraph present.
- Boxed derivative algorithm calls out full recomputation and stale cached prefixes/suffixes.
- Retained-filter compression diagnostics listed.
- Finite-difference trace points to numeric table.

No execution-review finding was disputed.
