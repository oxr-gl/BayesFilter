# Planning Block Skeptical Audit

## Scope

This audit covers the draft master program and P0-P10 subplans before Claude
review and before execution.

## Audit Findings

- Wrong-baseline risk: the V1 nonlinear performance rows are narrow tested-cell
  evidence, not a production baseline.  The master program preserves this.
- Proxy-metric risk: smoke tests, point counts, finite values, and XLA compile
  success are explanatory unless a phase declares a promotion criterion.  The
  subplans forbid promotion from these proxies.
- Hidden-assumption risk: tensor-train, transport, sparse-grid, and HNN methods
  require structure that may not hold for NAWM.  P5 and P7 require rank,
  localization, gradient, and downstream diagnostics before promotion.
- Unfair-comparison risk: the benchmark harness is a diagnostic, not a method
  winner selection.  P8 records non-implication text and skip rows.
- Environment risk: GPU commands require trusted execution; CPU-only runs must
  hide GPU.  P8 includes this policy.
- Artifact-risk: chapter drafts and benchmark artifacts stay inside the allowed
  write set.  No public API or production default change is planned.

## Audit Outcome

Initial planning block was safe to send to Claude for read-only review, but the
first Claude review returned `REJECT`.  Codex agreed with the substantive
objections and patched:

- per-claim and per-row source-support classes for P1;
- stronger MathDevMCP gates for P2/P9;
- mandatory chapter gates, unresolved-claim registers, and non-implication
  sections;
- P8 chapter-use restrictions;
- concrete phase stop rules;
- explicit HMC diagnostic reroute rules;
- a concrete P10 execution-result artifact.

Execution should remain conservative: produce reviewer-grade drafts and bounded
evidence, not a claim of solved high-dimensional nonlinear filtering.
