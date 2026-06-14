# Synthetic-Truth Filter Benchmark Methodology Claude Review Ledger

metadata_date: 2026-06-11
status: REVIEW_CONVERGED
owner: Codex
reviewer: Claude Code read-only

## Scope

This ledger records Claude read-only review for:

- proposal:
  `docs/plans/bayesfilter-synthetic-truth-filter-benchmark-methodology-proposal-2026-06-11.md`
- LaTeX chapter target:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p40-fixed-sgqf-expanded-companion-note-2026-06-08.tex`

Review loop:

- proposal review until convergence or max 5 iterations;
- LaTeX-vs-proposal audit until convergence or max 5 iterations;
- Claude is read-only reviewer only; Codex remains supervisor and editor.

## Iterations

### Proposal Review Iteration 1

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name synthetic-truth-benchmark-proposal-review-iter1 \
  --model claude-opus-4-7 \
  --effort max \
  "<read-only proposal review prompt>"
```

Claude initially took longer than expected.  A minimal probe returned
`PROBE_OK`, and the original review completed on the next poll.  No prompt
redesign was needed.

Verdict: `VERDICT: REVISE`.

Major findings:

- Freeze canonical derivative coordinates and transform/Jacobian policy.
- Use replicate-level curvature summaries; do not rely on
  `min eig(-mean H)` as primary.
- Add a variance decomposition/policy for averaging over truth draws.
- Add an operational rule for choosing stochastic-filter seed count \(S\).

Minor findings:

- Preserve componentwise signed score means and intervals.
- Specify benchmark-prior acceptance rules and draw manifests.
- Keep the no-nonlinear-oracle and stale `LEDH-PFPF-OT` guardrails.
- Add a row capability matrix.

Repairs applied:

- Added benchmark-coordinate transform contract, score/Hessian chain rule, and
  missing-transform status.
- Added row capability matrix.
- Added hierarchical variance decomposition across truth draws, data
  replicates, and time.
- Added acceptance-rule and draw-manifest requirements.
- Replaced mean-Hessian primary curvature with replicate-level
  `lambda_min(-H)` summaries and positive-definite fraction.
- Added stochastic-filter seed ladder and MC/data SE separation rule.
- Added componentwise signed score artifact.

### Proposal Review Iteration 2

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name synthetic-truth-benchmark-proposal-review-iter2 \
  --model claude-opus-4-7 \
  --effort max \
  "<read-only iteration-2 proposal review prompt>"
```

Claude was quiet for a normal polling cycle.  A minimal probe returned
`PROBE_OK`; the original review then completed on the next poll.

Verdict: `VERDICT: REVISE`.

Remaining blockers:

- Bind accepted truth draws and row capability status at the row/artifact
  level, not only as separate manifest and capability-matrix requirements.
- State that the stochastic-filter MC-noise rule applies componentwise to
  canonical score coordinates as well as scalar score summaries.

Repairs applied:

- Added required `(model_row, truth_draw_id, algorithm)` capability crosswalk
  fields.
- Clarified that MC SE must be controlled for average log likelihood, every
  canonical score coordinate, and scalar score summaries.

### Proposal Review Iteration 3

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name synthetic-truth-benchmark-proposal-review-iter3 \
  --model claude-opus-4-7 \
  --effort max \
  "<read-only final proposal re-review prompt>"
```

Verdict: `VERDICT: REVISE`.

Remaining blocker:

- The crosswalk recorded score/Hessian coordinate systems but not derivative
  provenance, so two cells could both say canonical coordinates while one was
  native, another chain-rule converted, and another missing a reviewed Hessian
  transform.

Repair applied:

- Added `score_derivative_provenance` and
  `hessian_derivative_provenance_or_gap` fields and described accepted
  provenance classes.

### Proposal Review Iteration 4

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name synthetic-truth-benchmark-proposal-review-iter4 \
  --model claude-opus-4-7 \
  --effort max \
  "<read-only final proposal check prompt>"
```

Verdict: `VERDICT: AGREE`.

Claude found no unresolved major issue on the derivative-provenance blocker.

Status:

- `PROPOSAL_REVIEW_CONVERGED_ITERATION_4`

### LaTeX Audit Iteration 1

Commands:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name synthetic-truth-benchmark-latex-audit-iter1 \
  --model claude-opus-4-7 \
  --effort max \
  "<read-only LaTeX-vs-proposal audit prompt>"
```

The broader audit was initially quiet.  A minimal probe returned `PROBE_OK`, so
Codex launched a shorter audit prompt.  The original broad audit then returned,
and the shorter audit returned afterward.

Verdicts:

- broad audit: `VERDICT: AGREE`, with two minor completeness suggestions;
- short audit: `VERDICT: AGREE`, no major or minor findings.

Minor improvements applied despite `AGREE`:

- Split the LaTeX capability crosswalk Hessian row into separate coordinate and
  derivative-provenance fields.
- Added an explicit `diagnostic-only reason` field.
- Added ESS, resampling, and degeneracy diagnostics to the stochastic-filter
  uncertainty table item.

### LaTeX Audit Iteration 2

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name synthetic-truth-benchmark-latex-audit-iter2 \
  --model claude-opus-4-7 \
  --effort max \
  "<read-only final LaTeX check prompt>"
```

Verdict: `VERDICT: AGREE`.

Claude confirmed:

- separate Hessian coordinate/provenance fields are explicit;
- a dedicated diagnostic-only reason field is present;
- ESS, resampling, and degeneracy diagnostics are included in the
  stochastic-filter table list;
- no new major issue was introduced by those edits.

Status:

- `LATEX_AUDIT_CONVERGED_ITERATION_2`
