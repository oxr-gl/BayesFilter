# P28 Zhao--Cui Companion Submission Audit Plan

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- Submission-readiness audit of the P27 chair-readable and implementation-ready companion note.
- Source fidelity against Zhao--Cui Sections 1--3 and 5.
- Equation, notation, dimension, implementation, chair-reader, and numerical-test audit.
- Narrow MathDevMCP checks for algebraic proof obligations where the tool is suitable.

what_is_not_concluded:
- This audit does not prove the Zhao--Cui adaptive algorithm is globally differentiable.
- This audit does not prove exact posterior accuracy of any TT approximation.
- This audit does not certify all 754 displayed equation environments by machine proof.
- This audit does not report new large-scale empirical benchmark outcomes.
- This audit does not change production code or chapter text.

## Skeptical Pre-Execution Audit

The audit plan passes the pre-execution gate because it does not treat Claude Code or MathDevMCP as global certifiers.  It separates five failure modes that can otherwise be confused:

1. a source-fidelity failure, where the note summarizes or distorts Zhao--Cui;
2. an algebra failure, where a displayed identity is wrong;
3. a notation/dimension failure, where the formula may be right but the reader cannot tell what measure, space, or coordinate system is being used;
4. an implementation-readiness failure, where the mathematical recipe is too scattered to implement;
5. a reader-trust failure, where the former-chemistry chair can follow local formulas but cannot teach back why the method is plausible.

Known risk before execution: P27 is about 103 PDF pages and contains 754 `equation` environments, 41 `aligned` sub-blocks, 3 propositions, 2 lemmas, and 5 proofs.  A complete line-by-line machine proof is not feasible.  The audit therefore inventories the equations mechanically, performs focused deep checks on high-risk identities, and records remaining human-review-required items honestly.

## Evidence Contract

Question:
- Is P27 ready to give to a skeptical mixed numerical/statistical/chemistry panel as a submission candidate, subject to explicitly recorded residual risk?

Primary pass/fail criterion:
- No known equation-level, source-fidelity, notation/dimension, implementation-readiness, or chair-reader blocker remains unresolved.

Veto diagnostics:
- Any material equation contradicts Zhao--Cui or the project derivation.
- Any central derivative identity differentiates a different scalar from the declared fixed-branch scalar.
- Any coordinate-system transformation omits the relevant Jacobian or measure.
- Any fixed-branch algorithm step lacks enough mathematical detail to be implemented.
- Any Claude finding classified as `ACCEPT` or `PARTIAL` remains unpatched.
- Any unresolved Codex--Claude disagreement after the loop affects submission readiness.

Explanatory diagnostics:
- Overfull/underfull LaTeX warnings.
- Minor wording improvements that do not affect mathematical correctness.
- Equation-count and page-count changes.

Artifact preserving the result:
- P28 audit ledgers and P28 submission audit result under `docs/plans/`.

## Allowed Writes

Allowed:
- New P28 audit artifacts under `docs/plans/`.
- A corrected P28 submission-candidate note and PDF only if audited corrections are required.

Forbidden:
- Editing `docs/chapters/`.
- Editing production `bayesfilter/`.
- Editing DPF lane, student-baseline, controlled-DPF, public APIs, or unrelated dirty files.
- Overwriting P27 artifacts.
- Committing.

## Audit Steps

### 1. Freeze P27

Record the P27 TeX path, PDF path, author/title/date, page count, build status, bibliography status, and dirty-worktree caveat.

### 2. Complete Equation Inventory

Inventory every `equation` environment, theorem-like statement, proof, and algorithm-style displayed formula anchor in P27.  For each item record:

- local id;
- source line;
- containing section;
- label if present;
- first-line formula preview;
- initial status;
- whether the item is high-risk.

The inventory is mechanical and is not itself a correctness certificate.

Risk rubric:

- `CRITICAL`: theorem/proposition/lemma statement, proof step, normalizer, posterior/evidence identity, filtering recursion, derivative identity, KR Jacobian/change-of-variables identity, mass contraction, fixed solve, quotient normalization, finite-difference formula, or equation directly used by a boxed algorithm.
- `HIGH`: any equation that defines a stored object, tensor shape, rank, basis, domain, shift/floor/stabilization parameter, retained filter, proposal/correction weight, benchmark metric, or failure condition.
- `MEDIUM`: explanatory derivation equation whose correctness supports reader understanding but is not directly stored or used as an invariant.
- `LOW`: purely illustrative arithmetic or restatement of a previously audited identity.

Mandatory coverage floor:

- Deep-check all `CRITICAL` equations.
- Deep-check all theorem/proposition/lemma statements and every proof display.
- Deep-check every implementation-relevant equation that feeds a stored object or differentiability claim.
- For `HIGH` equations, either deep-check or explicitly mark why a local consistency check is sufficient.
- For `MEDIUM` and `LOW` equations, perform symbol/dimension/source classification and sample at least five equations per major section family: Bayesian recursion, TT construction, squared TT/KR, preconditioning, fixed-branch filter, fixed-branch derivative, numerical traces, validation models.

### 3. Source-Fidelity Audit

Check Zhao--Cui Sections 1--3 and 5 against P27 in paper order.  The audit rejects vague summaries of material displayed formulas.  Each source item is classified as:

- `EXPANDED`;
- `EXPANDED_AS_PART_OF_LARGER_DERIVATION`;
- `SUPPORT_ONLY`;
- `OMITTED_WITH_REASON`;
- `POTENTIAL_GAP`.

Appendix and dependency escalation rule:

- If a P27 claim or derivation relies on a Zhao--Cui assumption, theorem, proof step, appendix lemma, cited external theorem, or numerical setting outside Sections 1--3 and 5, inspect the relevant appendix, section, or cited source anchor when locally available.
- Record each escalation in the source-fidelity ledger with source location, claim supported, and whether the P27 text states the dependency accurately.
- If the dependency is unavailable or not inspected, classify the affected P27 claim as `HUMAN_REVIEW_REQUIRED` or `SOURCE_GAP_BLOCKER`, not as passed.

### 4. MathDevMCP Narrow Checks

Use MathDevMCP only for local proof obligations:

- posterior/evidence identity;
- filtering recursion;
- marginalization identity;
- squared-density normalization;
- conditional normalization;
- triangular KR Jacobian/change-of-variables identity;
- pullback/pushforward density identity;
- derivative of log normalizer;
- fixed-matrix least-squares/linear-solve derivative;
- quotient derivative for normalized retained filter.

Allowed statuses:

- `MCP_VERIFIED`;
- `MCP_UNVERIFIED`;
- `MCP_INCONCLUSIVE`;
- `MCP_TOOL_LIMIT`;
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`.

### 5. Notation And Dimension Audit

Check the recurring objects \(x_t,\theta,r,z,u,z_t\), basis vectors, TT cores, ranks, mass matrices, environments, normalizers, shifts, floors, likelihoods, proposal weights, retained filters, and derivative objects.

### 6. Implementation-Readiness Audit

Check whether P27 is sufficient to implement:

- squared-TT sequential filtering;
- fixed-branch filtering;
- fixed-branch analytical derivative;
- sweep environment recomputation;
- retained-filter storage;
- rank ladder and failure exits;
- finite-difference diagnostic.

For every implementation-relevant formula, record:

- input objects;
- output objects;
- tensor shapes and support/domain;
- required numerical primitive;
- log-domain or stabilization note;
- differentiability/autodiff status;
- whether it is directly implementable or still proof-level.

### 7. Chair-Reader Audit

Read as an educated former chemistry academic and panel chair.  Record where the chair would stop, which equation cannot be taught back, what derivation would satisfy the chair, and whether the method is persuasive.

Boundary:

- This ledger is not a general prose-polish pass.
- It records only decision-relevant risks: unsupported claims, missing caveats, broken narrative around assumptions or limitations, and places where a skeptical chair would reject correctness, plausibility, or implementability.

### 8. Numerical Sanity-Test Audit

Audit whether P27 specifies enough mathematical models and diagnostics for:

- low-dimensional brute-force comparator;
- Zhao--Cui benchmark reproduction;
- memory/runtime/accuracy scaling;
- normalizer, mass, stability, and finite-difference checks;
- failure thresholds.

Minimal numerical sanity-test matrix:

- closed-form low-dimensional model with exact or brute-force normalizer;
- normalization and mass-conservation check;
- recursion consistency check across two time steps;
- KR Jacobian sign/shape check;
- derivative finite-difference check with a declared branch-stability window;
- one negative control that should fail, such as intentionally changing rank/pivots or removing the defensive floor while pretending to use the same fixed branch.

Each test must state the comparator, pass/veto condition, and what is not concluded if it passes.

## Cross-Ledger Issue Protocol

Any nontrivial finding receives a canonical issue id `P28-I###`.  Each issue records:

- originating ledger;
- affected equations/sections;
- affected downstream ledgers;
- Codex classification;
- patch or blocking decision;
- re-review status.

When a finding changes notation, measure, equation semantics, or source support, all downstream ledgers that depend on that object must be revisited or explicitly marked stale.

## Claude Review Protocol

Run Claude Code plan review before execution and execution review after drafting all audit ledgers.

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p28-submission-audit-plan-review-iter<N> \
  --model sonnet --effort high \
  "<prompt>"
```

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p28-submission-audit-exec-review-iter<N> \
  --model sonnet --effort high \
  "<prompt>"
```

Plan review maximum: 5 iterations.

Execution review maximum: 10 iterations.

Claude execution review must include:

1. hostile numerical analyst;
2. implementation engineer;
3. source-fidelity auditor against Zhao--Cui;
4. educated former chemistry academic / panel chair.

## Codex-Supervisor Audit Protocol

For every Claude finding, Codex classifies it as:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a narrower or different patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken the document.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

Accepted or partially accepted findings must be patched or recorded as blocking.  Disputed findings must receive a concise rebuttal and be included in the next Claude prompt.  Claude agreement is not sufficient unless Codex independently agrees.

## Validation

- Build P27 PDF if needed.
- If a P28 corrected note is created, build it with `latexmk`.
- Run `git diff --check`.
- Scan LaTeX logs for undefined citations, undefined references, rerun blockers, missing files, or bibliography problems.
- Use `pdftotext` to confirm title/author and audit-relevant sections.
- Confirm all P28 ledgers contain required metadata fields.
- Confirm only allowed files changed.

## Release Gates

Submission readiness requires:

- zero unresolved `ACCEPT` or `PARTIAL` Claude findings that affect equation correctness, source fidelity, notation/dimension consistency, implementation readiness, or chair-reader persuasiveness;
- zero unresolved `CRITICAL` equation audit failures;
- zero unresolved source-fidelity contradictions against Zhao--Cui or inspected dependencies;
- zero unresolved dimension/measure contradictions for central densities, TT cores, mass matrices, KR maps, normalizers, retained filters, or derivative objects;
- zero implementation-blocking ambiguities in the fixed-branch filter and derivative;
- numerical sanity-test coverage either specified with veto conditions or explicitly recorded as a non-claim;
- all cross-ledger issue ids closed, downgraded with justification, or marked as human-review blockers.

## Final Decision Labels

- `READY`
- `READY_WITH_MINOR_RISK`
- `NOT_READY_PATCH_REQUIRED`
- `BLOCKED`
