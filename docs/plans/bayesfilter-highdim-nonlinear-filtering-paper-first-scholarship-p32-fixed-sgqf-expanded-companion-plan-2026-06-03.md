# P32 FixedSGQF Expanded Companion Plan

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- P32 will not conclude that FixedSGQF gives exact nonlinear posterior filtering.
- P32 will not conclude that sparse-grid polynomial exactness implies posterior accuracy.
- P32 will not conclude HMC convergence, production readiness, or superiority over Zhao--Cui.
- P32 will not edit `docs/chapters/`, production `bayesfilter/`, DPF, student-baseline, controlled-DPF, public APIs, or unrelated dirty files.
- P32 will not claim broad machine certification of all equations.

## Goal

Create a P32 standalone LaTeX document that raises the FixedSGQF and analytical-gradient lane to the same explanatory standard as the Zhao--Cui companion work.  P32 builds from P31, keeps the useful P31 content, and expands it into a human-readable mathematical companion.  The intended reader is a mixed panel: a former chemistry academic should be able to follow the story without feeling talked down to, and an implementation engineer should be able to implement a value-and-gradient prototype from the equations.

## Non-Regression Guardrail

P32 must not summarize away P31.  It must preserve the core P31 mathematical content:

- what FixedSGQF computes and does not compute;
- Gaussian projection limitation example;
- exact filtering recursion and Gaussian projection;
- sparse-grid rule and fixed cloud;
- duplicate-node toy grid;
- fixed value path and same-scalar contract;
- analytical gradient recursions;
- boxed value-and-gradient algorithm;
- implementation contract;
- finite-difference same-scalar diagnostics;
- adaptive-grid-to-frozen-grid interpretation;
- comparison with Zhao--Cui.

P32 must expand these blocks, not replace them with shorter prose.

## Skeptical Pre-Execution Audit

Potential plan failures checked before execution:

- wrong baseline: treating P31 as final rather than as a seed;
- proxy metric: treating page count alone as quality;
- missing stop condition: no explicit Claude veto criteria;
- unfair comparison: overselling FixedSGQF against Zhao--Cui despite Gaussian-projection limits;
- hidden assumption: differentiating through adaptive grid choice, Cholesky pivot, floors, or clipping without declaring a new scalar;
- stale context: ignoring P31 Claude blockers already patched;
- environment mismatch: using source PDFs only through abstracts or metadata;
- artifact mismatch: editing `ch34` instead of creating a standalone `docs/plans` note.

Audit decision:
- Proceed.  The plan answers the current question because it creates a standalone P32 expansion, preserves P31, uses local primary sources, and imposes review gates that can reject summary-like text or same-scalar drift.

## Evidence Contract

Question:
- Can P32 make FixedSGQF and its analytical gradient clear enough for a skeptical mixed panel and detailed enough for implementation design?

Primary pass criteria:
- P32 is a larger annotated mathematical companion than P31.
- P32 reconstructs Jia--Xin--Cheng's SGQF construction in source order with equations, meaning, and implementation interpretation.
- P32 gives a full same-scalar value-and-gradient derivation for FixedSGQF, including square-root branch, prediction, observation, innovation score, posterior sensitivity, branch vetoes, and finite-difference checks.
- P32 separates source-supported SGQF material from BayesFilter extensions.
- Claude plan review and execution review produce no accepted unpatched blockers.

Veto diagnostics:
- P32 claims exact nonlinear posterior accuracy for FixedSGQF.
- P32 summarizes Jia--Xin--Cheng instead of annotating the mathematical construction.
- P32 omits the same-scalar contract or differentiates a different scalar than the value path.
- P32 uses hidden adaptive grid changes, floors, clipping, pivoting, or covariance repair without declaring a new scalar.
- P32 lacks a single end-to-end mathematical algorithm with inputs, outputs, invariants, and failure exits.
- P32 cannot be built into a PDF.
- P32 contains undefined citations or references.
- Claude returns a blocker or major finding that Codex accepts and does not patch.

Explanatory diagnostics:
- PDF page count and equation count relative to P31;
- MathDevMCP narrow algebra checks for score, covariance/factor identities, Kalman update derivatives, and finite differences;
- `pdftotext` scans for source-order reconstruction, same-scalar contract, gradient, validation ladder, and comparison;
- log scans for undefined references, undefined citations, rerun blockers, missing files, and amsmath warnings.

What will not be concluded even if P32 passes:
- mathematical flawlessness of every line;
- empirical large-scale performance;
- exact likelihood or exact posterior accuracy;
- downstream thesis integration readiness.

Artifact:
- P32 plan, note, PDF, source-support ledger, gradient ledger, validation ledger, MathDevMCP ledger, Claude review ledger, discrepancy report, and result under `docs/plans/`.

## Planned Files

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-plan-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-source-support-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-gradient-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-validation-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-claude-review-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-discrepancy-report-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex`
- compiled PDF beside the note
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-result-2026-06-03.md`

## Reader-Facing Expansion Requirements

The P32 note must:

- use `\cite`, `\citet`, and `\citep`; no informal "Jia-Xin-Cheng says" without citation;
- avoid governance/process language in the reader-facing note;
- use normal scholarly equation numbering and cross references;
- put mathematical definitions and derivations before prose explanation whenever the point is technical;
- reconstruct the SGQF source in paper order: state-space model, Bayesian filtering, Gaussian approximation filter, one-dimensional quadrature, tensor products, sparse-grid/Smolyak construction, univariate point selection, Algorithm 1, exactness, UKF relation, point counts, nested/repeated-point consequences, and numerical-test interpretation;
- include a source-order "annotated reconstruction" section, not only a source map at the end;
- explain why moderate sparse-grid levels can be plausible, and why that plausibility is weaker than a posterior-accuracy theorem;
- give a detailed coordinate walk from standard normal coordinate \(\xi\), physical state \(x\), predicted state \(a=f_\theta(x)\), observation coordinate \(z=h_\theta(x)\), and saved carried Gaussian \((m_t,P_t)\);
- state the exact approximation hierarchy: exact Bayes filter, Gaussian projection, quadrature approximation, fixed branch, approximate likelihood;
- expand the analytical gradient as a derivation story followed by formal equations;
- provide a one-page plain-math "story of the gradient" before the long derivation;
- give a single boxed algorithm for value and gradient together;
- include memory/performance/accuracy validation models with mathematical definitions;
- compare FixedSGQF and Zhao--Cui as complementary proposals without making FixedSGQF look like a non-Gaussian density method.

## Implementation Completeness Requirements

P32 must specify:

- all inputs, outputs, saved objects, shapes, and invariants;
- exact fixed sparse-grid cloud construction and duplicate merge;
- level/rank/grid selection policy for a deterministic ladder before failure;
- square-root/factor branch and derivative;
- prediction and observation point placement;
- all moment, innovation, cross-covariance, score, and update equations;
- derivative recursions through every object used by the next time step;
- finite-difference step ladder, branch-validity rule, and pass metric;
- synthetic finite-difference table;
- default stabilization constants and what they do not mean;
- failure exits and diagnostic messages;
- validation models for small exact checks, cloud-sensitive nonlinear checks, and large-scale memory/performance tests.

## MathDevMCP Checks

Use MathDevMCP only for narrow checks, recording one of:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Candidate checks:

- derivative of \(\log\det S\);
- derivative of \(v^\top S^{-1}v\);
- derivative of \(C S^{-1}\);
- covariance update identity \(P^+ = P^- - KSK^\top\);
- Cholesky sensitivity identity on a fixed branch;
- scalar finite-difference toy derivative.

Do not claim broad machine certification.

## Claude Review Protocol

Claude is a bounded hostile reviewer.  Codex is supervisor and final authority.

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p32-fixed-sgqf-plan-review-iter1 \
  --model sonnet --effort high \
  "<focused P32 plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p32-fixed-sgqf-exec-review-iter1 \
  --model sonnet --effort high \
  "<focused P32 execution review prompt>"
```

Plan review max iterations: 5.

Execution review max iterations: 5.

Execution review must include three personas:

- hostile numerical analyst;
- implementation engineer;
- panel chair / former chemistry academic.

The chemistry persona must explicitly answer:

- What is still not self-contained?
- Which equation or concept could not be taught back?
- What exact additional derivation would satisfy the panel chair?
- Would the chair endorse FixedSGQF as one of two high-dimensional filtering proposals, alongside Zhao--Cui?

## Codex-Supervisor Audit Protocol

After each Claude review round, Codex must independently audit Claude's findings before patching or accepting.

For every Claude finding, classify it as:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a different or narrower patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken the document.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

Record the classification in the Claude review ledger.

If Codex accepts or partially accepts a finding:

- patch the relevant file;
- record the exact section/equation/control added.

If Codex disputes a finding:

- write a concise rebuttal with file/section evidence;
- include that rebuttal in the next Claude prompt;
- ask Claude to withdraw, revise, or explain why the rebuttal is wrong.

Do not silently ignore disputed findings.  Do not treat Claude agreement as sufficient unless Codex independently agrees.

If Codex and Claude still disagree after max iterations, record the disagreement in the discrepancy report and block final acceptance unless the human explicitly decides.

## Validation

Run:

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex`
- `git diff --check`
- LaTeX log scan for undefined references, undefined citations, rerun blockers, missing files, and amsmath warnings.
- `pdftotext` content scan for source-order reconstruction, FixedSGQF, same-scalar contract, gradient story, boxed algorithm, finite difference, validation models, adaptive-grid relation, and Zhao--Cui comparison.
- Confirm required ledgers contain `metadata_date`, `seed_papers`, and `what_is_not_concluded`.
- Confirm only allowed files changed for P32.

## Final Result Requirements

The result file must include:

- what Codex inspected;
- how P32 expands P31;
- Claude plan review history;
- Claude execution review history;
- Codex audit classification summary;
- MathDevMCP status;
- files created/changed;
- PDF build status;
- validation commands run;
- remaining self-containedness gaps;
- whether the chemistry persona was satisfied;
- probability estimate that P32 passes a skeptical mixed panel as a standalone FixedSGQF proposal note.
