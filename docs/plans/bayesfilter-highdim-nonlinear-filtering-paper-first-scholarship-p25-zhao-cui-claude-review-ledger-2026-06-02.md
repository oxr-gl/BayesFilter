# P25 Zhao--Cui Claude Review Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P24 Zhao--Cui human-facing companion note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.
- No completed execution-review acceptance yet.

## Plan Review Iteration 1

reviewer: Claude Code bounded hostile reviewer

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p25-zhao-cui-chair-implementation-plan-review-iter1 \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

decision: `ACCEPT`

Claude residual risks:

1. Structural presence of five expansion blocks is not the same as adequacy.
2. P24 preservation could still be weakened by local compression unless
   section-level preservation is checked.
3. Claude/Codex audit protocol depends on honest stall recording.
4. Validation cannot prove pedagogical sufficiency.
5. Execution must faithfully copy P24 as a spine rather than selectively
   transplanting sections.

Codex classification: `ACCEPT`

Codex audit:

The residual risks are materially correct but do not require plan rejection.
Controls already present in the plan include line/page-count preservation, no
P24 edits, five detailed expansion checklists, and explicit blocking if Claude
execution review stalls.  During execution, Codex will create a five-gap closure
ledger with per-gap controls and will verify P25 is no shorter than P24.

## Execution Review

status: `TOOL_STALLED_FOR_FILE_REVIEW`

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p25-zhao-cui-chair-implementation-exec-review-iter1 \
  --model sonnet --effort high \
  "<compact five-section hostile execution review prompt>"
```

outcome:

- No review output was returned after repeated polling.
- The worker was stopped with `pkill -f
  highdim-p25-zhao-cui-chair-implementation-exec-review-iter1`.

Codex classification: `CLARIFY`

Codex audit:

Claude did not provide substantive execution-review findings to classify.
Local validation confirms that P25 builds, expands P24, and contains all five
new expansion sections, but this does not replace the required Claude
execution-review acceptance.

Execution-review decision after Codex audit:

`BLOCKED_BY_CLAUDE_REVIEW_TOOLING`.

## Execution Review Iteration 2

reviewer: Claude Code bounded hostile reviewer

status: `TOOL_STALLED_FOR_FILE_REVIEW`

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p25-zhao-cui-chair-implementation-exec-review-iter2 \
  --model sonnet --effort high \
  "<narrow five-section file-inspection execution review prompt>"
```

outcome:

- No review output was returned after repeated polling.
- The worker was stopped with `pkill -f
  highdim-p25-zhao-cui-chair-implementation-exec-review-iter2`.
- A separate tiny health check returned `CLAUDE_HEALTHCHECK_OK`, so the stall
  appears related to file-inspection review size rather than total Claude
  unavailability.

Codex classification: `CLARIFY`

Codex audit:

Claude did not provide substantive findings to classify in iteration 2.

## Execution Review Iteration 3

reviewer: Claude Code bounded hostile reviewer

status: `BOUNDED_EXCERPT_REVIEW_COMPLETED`

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p25-zhao-cui-excerpt-exec-review-iter3 \
  --model sonnet --effort high \
  "<bounded excerpt review prompt>"
```

Claude final decision: `ACCEPT_WITH_MINOR_RESIDUALS`

Claude findings and Codex audit:

| Finding | Claude class | Codex class | Control added |
|---|---:|---:|---|
| Five additions are directionally respectful to P24 scale and intent. | `ACCEPT` | `ACCEPT` | No patch required. |
| TT-rank plausibility needs explicit anti-overclaim sentence. | `MINOR` | `ACCEPT` | Added a sentence after Eq. `p25-bridge-16` stating that locality is a modeling/numerical heuristic, not a uniform rank theorem. |
| Coordinate section needs one measure-bookkeeping reminder. | `MINOR` | `ACCEPT` | Added Eq. `p25-walk-measure-bookkeeping`, explicitly separating reference-coordinate objects integrated with `\dd z` from the recovered physical density. |
| Fixed least-squares lane needs index/shape ledger. | `MINOR` | `ACCEPT` | Added Eqs. `p25-ls-shape-ledger`, `p25-ls-flattening`, `p25-ls-basis-mass`, and `p25-ls-mass-contract`. |
| Fixed scalar derivative story is sufficient. | `ACCEPT` | `ACCEPT` | No patch required. |
| Two-point numeric trace needs one verification line. | `MINOR` | `ACCEPT` | Added Eqs. `p25-trace2-9a`, `p25-trace2-12a`, and `p25-trace2-residual-check`. |

Codex audit:

Codex independently agrees that all four minor residuals were materially
correct and narrowly patchable.  No Claude finding was disputed.  The review is
bounded because Claude reviewed an execution summary and excerpts after two
full-file review attempts stalled; it is therefore evidence for the five new
P25 additions, not full-document machine certification.

Execution-review decision after Codex audit:

`BOUNDED_ACCEPT_WITH_MINOR_RESIDUALS_PATCHED`.
