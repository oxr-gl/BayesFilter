# P21 Zhao--Cui Chair Guide And Reference Implementation Plan

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P18 true annotated Zhao--Cui companion note and ledgers.
- P19 chair-readable fixed-branch gradient note and ledgers.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross, rank selection,
  pivot selection, changing domains, changing shifts, or changing fitting
  points.
- No HMC convergence claim.
- No production BayesFilter implementation claim.
- No empirical validation on BayesFilter target models.
- No default-method recommendation.
- No claim that the full adaptive Zhao--Cui algorithm has been implemented.
- No executable prototype claim; P21 is an implementation-ready mathematical
  specification and guided derivation, not a coding phase.

## Purpose

P20 is a serious integrated companion, but Codex identified two remaining
defects:

1. **Chair understanding defect.**  The main algorithm story is teachable, but
   the fixed-branch gradient is still dense for a former chemistry academic who
   chairs the panel.  The chair may believe the result without being able to
   teach back the derivative recursions.
2. **Implementation completeness defect.**  P20 is enough to motivate a
   minimal fixed-branch prototype, but it is not yet a complete implementation
   specification.  Before writing code, the mathematical details must be
   spelled out as if a Python implementation were about to be written: arrays,
   shapes, loops, contraction order, solve systems, branch manifests, derivative
   recursions, and finite-difference checks.  This must be done as derivation
   and pseudocode, not executable code.

P21 addresses both defects without rewriting P20 from scratch.

Hard guardrail:

- P21 must be strictly additive.  It must not summarize, shorten, remove,
  overwrite, replace, or deprecate any P20 pages or P20 files.  The P20 PDF and
  TeX remain the accepted integrated companion.  P21 may point to P20 equation
  anchors and may expand difficult P20 ideas, but it must not compress P20 into
  a shorter substitute.

The intended outputs are:

- a chair-facing mathematical guide that sits beside P20 and teaches the
  difficult gradient path slowly;
- an implementation-ready fixed-branch mathematical specification that follows
  the P20 equation numbers and is detailed enough to code later;
- an equation-to-specification ledger that lets a reviewer trace each
  would-be implementation object back to the note;
- a full-Zhao--Cui gap register that prevents the implementation-ready
  specification from being oversold.

## Skeptical Pre-Execution Audit

Decision: `PLAN_CREATION_AUDIT_PASS_WITH_STRONG_CONTROLS`.

The plan is necessary because adding more text to P20 alone risks repeating the
same failure mode: a longer document that still feels dense.  The plan must
force two new evidential channels:

- **teachability evidence**, where the chair persona must state whether he can
  teach back the normalizer, mass contraction, carried filter, fixed solve, and
  same-scalar derivative;
- **implementation-readiness evidence**, where the document spells out the
  same scalar and gradient objects, array shapes, pseudocode steps, branch
  manifest, and finite-difference protocol that a later Python implementation
  must follow.

Main risks and controls:

| Risk | Control |
|---|---|
| P21 becomes a prose-only simplification perceived as condescending. | Require math first, prose after math, and teach-back checkpoints with equations. |
| P21 becomes another dense derivation without helping the chair. | Require a 6--10 page roadmap plus repeated scalar-to-two-coordinate-to-TT-to-filtering ladders. |
| The implementation specification becomes detached from the note. | Require an equation-to-specification ledger naming P20/P21 equation anchors, array shapes, and pseudocode blocks. |
| The future implementation could silently test the wrong derivative. | Require a branch-manifest identity protocol and finite-difference pseudocode that recomputes fitted cores under the same fixed fitting rule. |
| The implementation-ready specification is mistaken for production Zhao--Cui. | Require a gap register for adaptive TT-cross, rank selection, KR engineering, nonlinear preconditioning, high-dimensional diagnostics, and production failure handling. |
| P21 accidentally becomes a replacement or summary of P20. | Require P21 to be strictly additive: no P20 file edits, no P20 page removal, no shortened substitute, and no compressed restatement of P20 in place of the accepted P20 companion. |
| Claude review becomes a rubber stamp. | Claude must review both chair teachability and implementation traceability, with explicit veto power. |

## Evidence Contract

Question:

Can P21 make the Zhao--Cui squared-TT sequential filter and the BayesFilter
fixed-branch derivative both:

1. teachable to a former chemistry academic chair; and
2. ready for a minimal fixed-branch Python implementation from the document,
   pseudocode, shape contracts, and equation ledgers alone?

Baselines:

- P20 integrated note, 50-page PDF, accepted after Claude review.
- P18 annotated Zhao--Cui companion.
- P19 chair-readable fixed-branch gradient supplement.
- Zhao--Cui paper Sections 1--3 and 5.
- Existing P10 code-audit and paper-code crosswalk ledgers.

Primary pass criteria:

- P21 chair guide PDF builds.
- P21 guide gives a 6--10 page front roadmap and teach-back checkpoints.
- P21 guide expands the gradient through a repeated ladder:
  \[
  \text{scalar case}
  \rightarrow
  \text{two-coordinate case}
  \rightarrow
  \text{TT case}
  \rightarrow
  \text{filtering meaning}.
  \]
- The chair persona says he can teach back, in his own words, all five
  elementary derivative ideas:
  \[
  \partial\log Z,\quad
  \partial(\phi^2),\quad
  \partial\text{ mass contraction},\quad
  \partial\text{ linear solve},\quad
  \partial(a/Z).
  \]
- The implementation-ready specification fully spells out a \(T=2\),
  one-dimensional nonlinear state-space example.
- The specification defines the exact value and derivative objects a later
  implementation must compute:
  \[
  \widehat\ell_2(\beta),\qquad
  \partial_\beta\widehat\ell_2(\beta),\qquad
  D(h),\qquad
  |D(h)-\partial_\beta\widehat\ell_2(\beta)|.
  \]
- The specification fixes domains, basis, fitting points, ranks, shifts, ridge
  parameter, sweep order, and recomputation of fitted core values at perturbed
  \(\beta\).
- The finite-difference protocol states the expected decreasing-error window
  and the exact branch-identity checks, but does not claim a numerical result.
- The equation-to-specification ledger maps each would-be implementation
  routine and pseudocode block to exact P20/P21 equations.
- Claude plan and execution reviews accept after Codex-supervisor audit.

Veto diagnostics:

- Chair persona cannot teach back the mass contraction, carried-filter
  derivative, or same-scalar derivative.
- P21 uses prose instead of equations for a mathematically essential step.
- The implementation specification permits or implies copying fitted cores from
  \(\beta_0\) instead of recomputing them at \(\beta_0\pm h\) under the fixed
  fitting rule.
- The finite-difference protocol permits changing ranks, points, domains,
  shifts, or sweep order between \(\beta_0\), \(\beta_0+h\), and
  \(\beta_0-h\).
- The specification defines a value path and gradient path that are not the
  same scalar.
- Equation-to-specification mapping is vague or missing for any major
  operation.
- P21 modifies, deletes, summarizes away, or replaces P20 material instead of
  adding a companion guide and implementation-ready specification beside it.
- The document or result claims production readiness, full adaptive Zhao--Cui
  implementation, exact posterior accuracy, or HMC readiness.
- Claude raises a substantive veto finding that Codex accepts and does not
  patch.

Explanatory diagnostics:

- No prototype runtime or derivative error is produced in P21.  The
  finite-difference protocol is an implementation-readiness artifact only.
- Line count, page count, and equation count are explanatory only; they cannot
  prove chair understanding.
- MathDevMCP checks, if used during execution, are narrow algebra checks only.

## Allowed Writes

Allowed:

- New P21 files under `docs/plans/`.
- A P21 implementation-ready mathematical specification under `docs/plans/`.
- A compiled P21 PDF beside the P21 guide.
- P21 plan, review, result, equation-to-specification,
  finite-difference-protocol, chair teachability, implementation-readiness, and
  gap ledgers.

Not allowed:

- Do not overwrite P18, P19, or P20 artifacts.
- Do not edit, shorten, regenerate, or remove P20 TeX/PDF pages.
- Do not produce P21 as a condensed replacement for P20.
- Do not create executable Python, MATLAB, Octave, TensorFlow, JAX, or
  production code in P21.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not commit.

## Required Outputs

Planning/review:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-plan-2026-06-02.md`
- `...p21-zhao-cui-chair-guide-reference-implementation-claude-review-ledger-2026-06-02.md`

Execution outputs:

- `...p21-zhao-cui-chair-guide-reference-implementation-note-2026-06-02.tex`
- compiled PDF beside the note
- `...p21-zhao-cui-fixed-branch-implementation-ready-spec-ledger-2026-06-02.md`
- `...p21-zhao-cui-equation-to-specification-ledger-2026-06-02.md`
- `...p21-zhao-cui-finite-difference-protocol-ledger-2026-06-02.md`
- `...p21-zhao-cui-chair-teachability-ledger-2026-06-02.md`
- `...p21-zhao-cui-implementation-readiness-ledger-2026-06-02.md`
- `...p21-zhao-cui-full-algorithm-gap-register-2026-06-02.md`
- `...p21-zhao-cui-discrepancy-report-2026-06-02.md`
- `...p21-zhao-cui-chair-guide-reference-implementation-result-2026-06-02.md`

Every markdown artifact must contain:

- `metadata_date`
- `seed_papers`
- `what_is_not_concluded`

## Workstream A: Chair-Facing Mathematical Guide

Create a new P21 LaTeX note.  It must not replace P20.  It must be a guided
companion that makes the hardest P20 material easier to learn.

The P21 note must state near the beginning that P20 remains the complete
integrated companion.  P21 is a guided reading layer and implementation-ready
specification companion, not a summary, substitute, code artifact, or
page-reduction of P20.

### A1. Front Roadmap

Write a 6--10 page front roadmap with five mathematical objects:

1. unnormalized density \(q_t\);
2. square-root approximation \(\phi_t\);
3. tensor train cores \(C_{t,k}\);
4. normalizer \(\widehat Z_t\);
5. derivative \(\partial_\beta\log\widehat Z_t\).

For each object, include:

- the question it answers;
- the simplest scalar formula;
- the filtering meaning;
- the implementation object stored;
- the failure mode if the object is wrong.

### A2. Repeated Derivation Ladder

For each hard operation, use the same four-stage ladder:

\[
\text{scalar}
\rightarrow
\text{two-coordinate}
\rightarrow
\text{TT}
\rightarrow
\text{filtering recursion}.
\]

Required operations:

- normalizer derivative;
- squared-density derivative;
- mass contraction derivative;
- fixed ridge-solve derivative;
- carried-filter quotient derivative;
- next-step target derivative;
- finite-difference same-branch test.

### A3. Teach-Back Checkpoints

After each major block, include a checkpoint with exact answers to:

- What is stored?
- What is integrated?
- What is differentiated?
- What is frozen?
- What would break the claim?

The checkpoint must include equations, not only prose.

### A4. Chair Endorsement Section

Add a final chair-facing section titled `Why This Is A Plausible High-Dimensional Filtering Method`.

It must make the argument mathematically:

\[
\text{nonnegative approximation}
+
\text{computable mass}
+
\text{recursive marginal}
\Longrightarrow
\text{valid normalized approximate filter}.
\]

Then explain, in human language after the math, why this is a plausible
candidate rather than a proven default method.

## Workstream B: Implementation-Ready Fixed-Branch Specification

Create a mathematical specification section in the P21 note and a matching
implementation-readiness ledger.  Do not write executable code.  The section
must be explicit enough that a later Python implementation can be written
mechanically from the derivation, pseudocode, array shapes, and branch
manifest.

### B1. Model

Use the \(T=2\), one-dimensional nonlinear model from P20:

\[
    x_t=\beta x_{t-1}+\sigma\epsilon_t,\qquad
    y_t=\sin(x_t)+\eta_t.
\]

Fix data, seeds, domains, basis degree, fitting points, ranks, ridge parameter,
defensive floor, and sweep count.

### B2. Required Specification Pieces

Specify, with equations, shapes, and pseudocode:

- Legendre basis evaluation and basis mass matrices;
- fixed deterministic fitting points;
- TT core data structure for the one-dimensional two-block case;
- fixed-rank ridge core solve;
- squared-TT evaluation;
- square-mass contraction;
- retained marginal numerator;
- carried filter evaluator;
- analytical derivative through:
  - model density values;
  - square-root target values;
  - design rows;
  - ridge solves;
  - mass contractions;
  - normalizers;
  - carried filters;
  - next-step targets;
- centered finite-difference check.

For each item, the note must state:

- mathematical formula;
- input symbols and dimensions;
- output symbols and dimensions;
- array shape contract using Python-like tuple notation;
- loop or contraction order;
- derivative counterpart;
- failure diagnostic.

### B3. Branch Manifest

The specification must define a branch manifest that a later implementation
would print or hash.  The manifest must contain:

- domains;
- basis family and degree;
- fitting point rule;
- ranks;
- shift values;
- defensive mass;
- ridge parameter;
- sweep count;
- random seed, if any.

The finite-difference protocol must require the same manifest for
\(\beta_0\), \(\beta_0+h\), and \(\beta_0-h\).

### B4. Required Pseudocode Outputs

The specification must define the quantities a later implementation must print:

- \(\widehat\ell_2(\beta_0)\);
- analytical \(\partial_\beta\widehat\ell_2(\beta_0)\);
- finite differences for \(h\in\{10^{-2},10^{-3},10^{-4},10^{-5}\}\);
- absolute and relative errors;
- branch manifest equality checks;
- finite-difference pass/fail status.

The finite-difference protocol ledger must record:

- declared quantities;
- branch identity rule;
- recompute-core rule;
- step sizes;
- expected convergence pattern;
- failure interpretations;
- what is not concluded.

## Workstream C: Equation-To-Specification Ledger

Create a ledger mapping would-be implementation routines and pseudocode blocks
to equations.

Required mappings:

| Specified operation | Required equation anchors |
|---|---|
| transformed target | P20 `FB1`, P19-46 |
| square-root target | P20 `C10`, P19-47 |
| TT evaluation | P20 `D1`--`D2`, P19-48 |
| core ridge solve | P19-62--P19-65 and P21 fixed-solve derivation |
| square-mass contraction | P19-66--P19-72 |
| carried numerator | P19-73--P19-74d |
| carried filter quotient | P19-75--P19-76 |
| log evidence scalar | P19-85 |
| finite difference | P19-94--P19-101 |

Each ledger row must state:

- would-be function or pseudocode block name;
- input arrays and shapes;
- output arrays and shapes;
- equation anchor;
- whether the block is value-only or derivative-producing;
- diagnostics and failure modes.

## Workstream D: Full Zhao--Cui Gap Register

Create a gap register separating the minimal P21 implementation-ready
specification from full Zhao--Cui.

Required gap items:

- adaptive TT-cross;
- rank selection;
- pivot selection;
- adaptive fitting points;
- automatic domain choice;
- \(\tau_t\) and \(\lambda_t\) adaptation;
- KR map construction beyond the simple fixed branch;
- inverse conditional sampling in high dimension;
- nonlinear preconditioning;
- full static-parameter learning as a random coordinate;
- smoothing/path estimation;
- high-dimensional rank diagnostics;
- positivity, mass, normalization, support, and branch-stability diagnostics;
- production failure recovery;
- performance engineering.

For each item state:

- whether P20 teaches the math;
- whether P21 specifies it for the minimal fixed branch;
- why it matters;
- what would be required next;
- whether it blocks the minimal fixed-branch derivative.

## Workstream E: Claude Review Protocol

Claude Code is a bounded hostile reviewer only.  Codex is supervisor and final
authority.

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p21-zhao-cui-chair-guide-implementation-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p21-zhao-cui-chair-guide-implementation-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Maximum iterations:

- Plan review: 5.
- Execution review: 8.

Claude plan review must judge whether this plan is specific enough to fix the
two defects while deliberately postponing executable code.  Claude execution
review must use four personas:

1. former chemistry academic and panel chair;
2. numerical computation professor;
3. implementation engineer;
4. hostile mathematical reviewer.

The chair persona must explicitly answer:

- Can I teach back the normalizer derivative?
- Can I teach back the squared-density derivative?
- Can I teach back the mass contraction derivative?
- Can I teach back the fixed solve derivative?
- Can I teach back the carried-filter quotient derivative?
- Can I explain why the fixed branch is needed?
- Would I endorse this as a plausible high-dimensional filtering candidate?
- What exact remaining sentence, equation, shape contract, or protocol step
  prevents endorsement?

The implementation engineer must explicitly answer:

- Could I implement the minimal fixed-branch prototype later from the note and
  ledger alone?
- Are all array shapes and data structures specified?
- Is the branch manifest sufficient?
- Is the finite-difference protocol testing the same scalar?
- What exact missing pseudocode block, shape contract, or equation anchor
  blocks implementation?

## Codex-Supervisor Audit Protocol

After each Claude review round, Codex must independently audit Claude's
findings before patching or accepting them.

For every Claude finding, Codex must classify it as:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a different or narrower patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken
  the document.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

Codex must record this classification in the review-loop artifact.

If Codex accepts or partially accepts a finding:

- patch the relevant files;
- record the exact control added.

If Codex disputes a finding:

- write a concise rebuttal with file/section evidence;
- include that rebuttal in the next Claude prompt;
- ask Claude to withdraw, revise, or explain why the rebuttal is wrong.

Codex must not silently ignore disputed findings.  Codex must not treat Claude
`ACCEPT` as sufficient unless Codex independently agrees.

If Codex and Claude still disagree after the maximum iterations, record the
disagreement in the discrepancy report and block final acceptance unless the
human explicitly decides.

## Validation Requirements

For plan creation:

- Claude plan review must accept.
- Review ledger must record all Claude findings and Codex classifications.
- `git diff --check` must pass on P21 plan/review files.
- P21 markdown artifacts must contain required metadata fields.

For execution:

- Build the P21 PDF with `latexmk`.
- Run `git diff --check` on P21 files.
- Scan LaTeX log for errors, undefined references, citation warnings, rerun
  blockers, missing files, and serious overfull boxes.
- Confirm the finite-difference protocol includes branch manifest equality,
  recomputed-core rule, step sizes, expected trend, and failure
  interpretations.
- Confirm every equation-to-specification ledger row has a would-be function or
  pseudocode block name, shape contract, equation anchor, and diagnostic.
- Confirm P20 TeX and PDF artifacts were not edited, removed, shortened, or
  regenerated as part of P21 execution.
- Confirm no disallowed files changed.

## Final Response Requirements After Execution

The final execution response must include:

- what Codex inspected;
- Claude plan review history;
- Claude execution review history;
- Codex audit classification summary;
- chair teachability result;
- implementation-readiness result;
- finite-difference protocol summary;
- equation-to-specification ledger summary;
- full-Zhao--Cui gap register summary;
- files changed;
- PDF build status;
- validation commands run;
- residual risks;
- final probability estimate that the package passes a skeptical
  numerical/chemistry panel.
