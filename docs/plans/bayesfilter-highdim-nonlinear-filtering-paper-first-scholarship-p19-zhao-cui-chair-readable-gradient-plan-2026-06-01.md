# P19 Zhao--Cui Chair-Readable Gradient Plan

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui filtering-scalar and gradient-feasibility ledgers.
- P15 implementable fixed-branch squared-TT specification.
- P18 true annotated Zhao--Cui companion and review ledgers.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross, rank selection,
  pivot selection, changing domains, changing shifts, or changing fitting
  points.
- No HMC convergence claim.
- No production BayesFilter implementation claim.
- No empirical validation on BayesFilter target models.
- No default-method recommendation.

## Purpose

P18 is audit-sound as a Zhao--Cui companion, but its fixed-branch analytical
gradient is still too compressed for the panel chair, a former chemistry
academic, and too dense even for a numerical computation expert reading under
time pressure.  P19 creates a separate chair-readable fixed-branch gradient
note.  It treats the P18/P15 scalar as fixed and decomposes the derivative from
normalizing constants through squared approximations, tensor-train mass
contractions, linear solves, carried filters, and same-branch finite
differences.

P19 is not a new source reconstruction of Zhao--Cui Sections 1--3 and 5.  It is
a pedagogical and mathematical expansion of the BayesFilter fixed-branch
extension that P18 placed after the Zhao--Cui annotation boundary.

## Skeptical Pre-Execution Audit

Decision: `PRE_EXECUTION_AUDIT_PASS_WITH_STRICT_SCOPE`.

The user's criticism is materially correct: P18's gradient section states the
right skeleton, but it starts too close to full TT notation and compressed
linear-solve/mass-contraction derivatives.  That can satisfy an audit ledger
while failing a chair who needs to understand and teach back the derivative.

The plan is allowed to proceed only because it fixes the problem by expanding
the derivation, not by weakening the mathematics.  The high-risk failure modes
are:

- creating another audit-flavored document instead of a chair-readable note;
- treating prose as a substitute for mathematical derivation;
- jumping from scalar calculus to full tensor trains without rank-one and
  rank-\(R\) warmups;
- blurring fixed branch and adaptive algorithm;
- claiming HMC readiness or exact posterior accuracy from a local derivative;
- writing a note that is readable to Codex/Claude but not to the chemistry
  chair.

The evidence contract below turns these risks into veto checks.

## Evidence Contract

Question:

Can P19 make the fixed-branch analytical gradient of the Zhao--Cui-inspired
squared-TT filtering scalar understandable, teachable, and persuasive to a
former chemistry academic who chairs the panel, while remaining mathematically
honest for numerical computation experts?

Baselines:

- P18 fixed-branch gradient section.
- P15 fixed-branch implementation specification.
- P10 filtering-scalar and gradient-feasibility ledgers.
- Zhao--Cui paper/code only as source support; the P19 reader must not need to
  open them.

Primary pass criteria:

- The chair can explain what scalar is differentiated.
- The chair can explain why the branch must be fixed.
- The chair can follow the derivative of \(\log Z\).
- The chair can follow the derivative of a squared approximation.
- The chair can follow the derivative of a fixed linear solve.
- The chair can follow a two-coordinate/rank-one TT before the full TT case.
- The chair can follow the rank-\(R\) mass-matrix warmup before the full TT
  mass contraction.
- The chair can follow how the carried-filter derivative enters the next time
  step.
- A numerical expert can verify that the derivative is of the same approximate
  scalar, not an adaptive algorithm.
- An implementation agent can translate the derivation into code without
  reading the original paper.

Veto diagnostics:

- The main note reverts into a governance artifact: it contains audit/review
  lexicon, pushes core mathematics into ledgers or review artifacts, or asks the
  reader to trust process instead of derivation.
- The gradient derivation begins with full TT notation before scalar/toy cases.
- The document differentiates adaptive branch choices.
- The same-scalar claim is ambiguous.
- The carried-filter derivative is not derived.
- The linear-solve derivative is not derived step by step.
- The TT environment derivative is introduced without a two-coordinate/rank-one
  warmup.
- The mass-contraction derivative is introduced without a rank-\(R\) warmup.
- The finite-difference test does not freeze the branch.
- The chemistry-chair persona cannot teach back the derivation.
- The numerical computation professor persona finds the same-scalar derivative
  mathematically ambiguous or incomplete.
- Claude flags a veto finding that Codex accepts and it is not patched.

Explanatory diagnostics:

- Page count, equation count, and Claude `ACCEPT` are explanatory.  They cannot
  override a failed chair teach-back or same-scalar veto.

What will not be concluded:

- No exact posterior accuracy.
- No global differentiability of adaptive TT-cross/rank/pivot/domain selection.
- No HMC convergence.
- No production implementation readiness.
- No empirical validation on BayesFilter target models.

## Allowed Writes

Allowed:

- Only the exact P19 files listed under `Required Outputs`.
- The compiled P19 PDF beside the note.
- `latexmk`-generated auxiliary files sharing the note basename:
  `.aux`, `.fdb_latexmk`, `.fls`, `.log`, `.out`, `.toc`.

Not allowed:

- Do not overwrite P18 artifacts.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-plan-2026-06-01.md`
- `...p19-zhao-cui-chair-readable-gradient-note-2026-06-01.tex`
- compiled PDF beside the note
- `...p19-zhao-cui-gradient-teaching-ledger-2026-06-01.md`
- `...p19-zhao-cui-gradient-equation-ledger-2026-06-01.md`
- `...p19-zhao-cui-fixed-branch-scalar-ledger-2026-06-01.md`
- `...p19-zhao-cui-finite-difference-ledger-2026-06-01.md`
- `...p19-zhao-cui-mathdevmcp-ledger-2026-06-01.md`
- `...p19-zhao-cui-claude-review-ledger-2026-06-01.md`
- `...p19-zhao-cui-discrepancy-report-2026-06-01.md`
- `...p19-zhao-cui-chair-readable-gradient-result-2026-06-01.md`

Every ledger must contain `metadata_date`, `seed_papers`, and
`what_is_not_concluded`.

## Reader-Facing Note Requirements

The main note must not use audit/governance language such as `source unit`,
`ledger`, `review gate`, `artifact`, or `exported`.

Style requirements:

- Prose should come after math, not instead of math.
- Use many small derivation steps.
- Use scalar and two-coordinate examples before full TT notation.
- Include math flow boxes and tables where helpful.
- Do not compress the gradient derivation to save pages.
- The note may be 50--60 pages if needed.
- Every caveat must be stated in human mathematical language.

## Required Note Structure

1. **Motivation For The Chair**
   - State the problem in plain mathematical terms.
   - Explain why the panel cares about the gradient.
   - Explain why "same scalar" is the central issue.
   - Present \(\widehat\ell_T(\beta)=\sum_t\log \widehat Z_t(\beta)\) as a
     sequence of approximate normalizing constants, analogous to partition
     functions.

2. **Warmup 1: Derivative Of A Normalizing Constant**
   - Derive \(\partial_\beta\log \widehat Z
     =(\partial_\beta \widehat Z)/\widehat Z\).
   - State conditions for differentiating under the integral sign.

3. **Warmup 2: Squared Approximation**
   - Derive the derivative of
     \(\widehat q=e^{-c}\phi^2+\tau\lambda\) with fixed \(c,\tau,\lambda\).
   - Explain the extra terms that would appear if \(c,\tau,\lambda\) changed,
     and why P19 does not claim that derivative.

4. **Warmup 3: Two-Coordinate Rank-One And Rank-\(R\) TT**
   - Start from \(\phi(z_1,z_2)=h_1(z_1)h_2(z_2)\).
   - Derive \(\partial_\beta\int\phi^2\) fully.
   - Then derive the rank-\(R\) case
     \(\phi(z_1,z_2)=\sum_r h_{1r}(z_1)h_{2r}(z_2)\) and show how mass
     matrices appear.

5. **Warmup 4: Linear Solve Derivative**
   - Derive \(N g=d\Rightarrow N\dot g=\dot d-\dot N g\).
   - Explain ridge regularization and nonsingularity.

6. **Full Fixed-Branch Forward Pass**
   - Present a table mapping every forward object to what is stored and why it
     is needed later: domain map, fitting points, basis, ranks, sweeps, shifts,
     cores, mass contractions, normalizer, carried filter.

7. **Full Fixed-Branch Derivative Pass**
   - Present a matching table mapping derivative objects to forward objects.
   - Derive target derivative, square-root target derivative, design matrix
     derivative, core derivative, mass contraction derivative, normalizer
     derivative, carried-filter derivative, and next-step target derivative.

8. **Full Proposition 1**
   - State and prove that the fixed-branch recursion defines a normalized
     approximate filtering recursion for the declared scalar.

9. **Full Proposition 2**
   - State and prove that the fixed-branch derivative computes the analytical
     derivative of exactly the scalar computed by the fixed-branch forward pass.

10. **What This Does Not Prove**
    - Explain what remains outside the claim: adaptive branches, exact posterior
      accuracy, small-rank guarantees, HMC convergence.

11. **Finite-Difference Test**
    - Specify same-branch finite-difference protocol, what is frozen, what is
      recomputed, what is compared, and what failure means.

12. **Minimal Runnable Example Specification**
    - Use \(x_t=\beta x_{t-1}+\sigma\epsilon_t\),
      \(y_t=\sin(x_t)+\eta_t\).
    - Specify exactly what code should store and print.

## Finite-Difference Ledger Requirements

The finite-difference ledger must include:

- frozen branch manifest;
- explicit branch-identity confirmation for \(\beta_0\), \(\beta_0+h\), and
  \(\beta_0-h\);
- centered-difference formula;
- epsilon schedule;
- error metric and tolerance;
- pass/fail interpretation;
- statement that rebuilding any branch object changes the scalar and invalidates
  the same-scalar gradient check.

## MathDevMCP Protocol

Use MathDevMCP only for narrow checks:

- derivative of \(\log Z\);
- derivative of squared integral;
- fixed linear-solve derivative;
- quotient derivative for normalized carried filter;
- simple two-coordinate mass-contraction derivative.

Record statuses:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Do not claim broad machine certification.

## Claude Plan Review Loop

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p19-zhao-cui-chair-gradient-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.

Plan review maximum: 5 iterations.

The Claude wrapper must be run with trusted/elevated permissions according to
project cross-agent policy.  Non-trusted Claude hangs, authentication failures,
or network/API failures are sandbox evidence only and must be rerun in the
trusted context before being treated as review findings.

Codex must audit every Claude finding and classify it as `ACCEPT`, `PARTIAL`,
`DISPUTE`, or `CLARIFY`.  Accepted or partially accepted findings must be
patched before execution.

## Claude Execution Review Loop

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p19-zhao-cui-chair-gradient-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Execution review maximum: 10 iterations.

The Claude wrapper must be run with trusted/elevated permissions according to
project cross-agent policy.  Non-trusted Claude hangs, authentication failures,
or network/API failures are sandbox evidence only and must be rerun in the
trusted context before being treated as review findings.

Claude execution review must include four personas:

1. former chemistry academic and panel chair;
2. numerical computation professor;
3. implementation engineer;
4. hostile mathematical reviewer.

The chemistry-chair persona must explicitly answer:

- What is still not self-contained?
- Which equation or concept could not be taught back?
- What exact additional derivation would satisfy the chair?
- Would the chair be convinced that the fixed-branch gradient is
  mathematically honest?

The numerical computation professor must explicitly answer:

- Is the same-scalar derivative claim correct?
- Are all frozen/adaptive branches separated?
- Is the linear-solve derivative sufficient?
- Is the mass-contraction derivative sufficient?
- Is the carried-filter derivative sufficient?

Codex-supervisor audit protocol:

- For every Claude finding, classify it as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
  `CLARIFY`.
- If accepted or partially accepted, patch the relevant file and record the
  exact section/equation/control added.
- If disputed, write a concise rebuttal with file/section evidence and include
  it in the next Claude prompt.
- Do not silently ignore disputed findings.
- Do not treat Claude `ACCEPT` as sufficient unless Codex independently agrees.
- If Codex and Claude still disagree after max iterations, record the
  disagreement and block final acceptance unless the human explicitly decides.

## Validation

- Build the P19 PDF with `latexmk`.
- Run `git diff --check`.
- Scan the LaTeX log for undefined references, citation warnings, rerun
  blockers, missing files, and serious overfull boxes.
- Scan the main note source and extracted PDF text for banned audit/governance
  terms: `source unit`, `ledger`, `review gate`, `artifact`, `exported`, and
  `governance`.  These terms may appear in P19 ledgers and result files, but
  not in the main reader-facing note.
- Use `pdftotext` to confirm the PDF contains:
  - normalizer warmup;
  - squared approximation derivative;
  - rank-one and rank-\(R\) TT warmups;
  - linear solve derivative;
  - forward-pass table;
  - derivative-pass table;
  - Proposition 1;
  - Proposition 2;
  - finite-difference protocol;
  - minimal runnable example.
- Confirm every ledger contains `metadata_date`, `seed_papers`, and
  `what_is_not_concluded`.
- Confirm the finite-difference ledger contains the frozen branch manifest,
  branch-identity check, centered-difference formula, epsilon schedule, error
  metric/tolerance, and pass/fail interpretation.
- Confirm only allowed files changed.

## Final Result Requirements

The result note must include:

- what Codex inspected;
- Claude plan review history;
- Claude execution review history;
- Codex audit classification summary;
- MathDevMCP status;
- files changed;
- PDF build status;
- validation commands run;
- remaining chair-readable gaps;
- whether the chemistry-chair persona was satisfied;
- whether the numerical computation professor persona was satisfied;
- final probability estimate that P19 passes a skeptical mixed panel chaired by
  the chemist.
