# P25 Zhao--Cui Chair And Implementation Bridge Expansion Plan

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
- No global differentiability claim for adaptive TT-cross, rank-changing,
  pivot-changing, domain-changing, shift-changing, or preconditioner-changing
  algorithms.
- No production BayesFilter implementation claim.
- No empirical validation claim.
- No final panel endorsement claim.

## Purpose

Create P25 as an expansion of P24 that closes five reader and implementation
gaps found by a Codex chemist-chair and implementation-engineer read-through.
P25 must not summarize P24 down.  It must copy P24 as the source spine and add
targeted mathematical exposition, walkthroughs, and implementation contracts.

## Skeptical Pre-Execution Audit

decision: `PLAN_DRAFT_AUDIT_PASS_WITH_CONTROLS`

| Risk | Control |
|---|---|
| P25 repeats the P19/P21 regression pattern and becomes shorter than P24. | Copy P24 to a new P25 note and require P25 TeX line count and PDF page count to be no shorter than P24. |
| Added chair prose sounds patronizing or replaces mathematics. | Every new explanatory section must put equations first, then prose; no "for beginners", "obviously", "simply", or governance language. |
| The chemist chair understands formulas locally but not why the approximation family is plausible for the inference task. | Add a full Bayesian-to-TT plausibility bridge: posterior geometry, separability, split-rank, local interactions, preconditioning, and failure modes in one continuous argument. |
| Coordinate notation remains mentally expensive. | Add a single observation-step walkthrough carrying one density through physical \(r\), reference \(z\), preconditioned \(u\), retained \(z_t\), and next-step evaluation. |
| Proposition 2 remains too dense. | Add a pre-proposition gradient teaching layer: named scalar, frozen fields, differentiable fields, dependency table, scalar path, derivative path, and a small finite-dimensional example before the proof. |
| Numerical trace remains too toy-like. | Add a second trace with a nonconstant \(p=2\), rank-one/separable fit at multiple points and visible nonzero derivative contribution; keep the constant trace as orientation. |
| Implementation remains mathematically scattered. | Add one consolidated fixed least-squares implementation lane and derivative lane: initialization, sweep order, stopping rule, \(\dot L,\dot R,\dot A,\dot N,\dot d,\dot g\), retained filter, failure exits. |
| P24 source/audit issues recur. | Keep citations with `\cite{...}` in the note and inherit/update P24 source-support and claim-support ledgers. |
| Claude file-review stalls again. | Run a small smoke test before review.  If file review still stalls, record the tool failure honestly and mark formal acceptance blocked. |

## Evidence Contract

Question:

Can P25 expand P24 so that a former chemistry academic chair can see why the
Zhao--Cui squared-TT method is a plausible high-dimensional filtering method,
and a mathematical implementation engineer can implement the fixed
least-squares squared-TT lane and derivative pass from the note alone?

Baseline:

- P24 TeX:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.tex`
- P24 PDF:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.pdf`
- P24 size: 6518 TeX lines and 73 PDF pages.

Primary pass criteria:

- P25 PDF builds.
- P25 TeX line count is no shorter than P24.
- P25 PDF page count is no shorter than P24.
- P25 does not remove P24 substantive derivations.
- P25 adds all five required expansion blocks.
- P25 contains no visible governance/process language in the main note.
- P25 uses `\cite{...}` for scholarly references.
- P25 local validation passes.
- Claude plan review and execution review either accept, or any tool failure is
  explicitly recorded and formal acceptance is blocked rather than silently
  granted.

Veto diagnostics:

- P25 is shorter than P24 without an explicit non-substantive build-format
  reason.
- Any P24 mathematical section is removed or replaced by a summary.
- Any of the five expansion blocks is missing.
- The main note contains visible governance/process language, old audit tags,
  or informal source references unsupported by `\cite{...}`.
- The note claims exact posterior accuracy, adaptive global differentiability,
  production readiness, empirical validation, or default-method readiness.
- Any required P25 markdown artifact lacks `metadata_date`, `seed_papers`, or
  `what_is_not_concluded`.
- Claude returns a material rejection finding that Codex accepts or partially
  accepts but does not patch.

Explanatory diagnostics:

- Page count is only a guardrail.
- A Claude chemistry persona is not the actual chair.
- P25 remains a mathematical note, not executable code.

## Allowed Writes

Allowed:

- New P25 files under `docs/plans/`.
- P25 compiled PDF and LaTeX build byproducts beside the note.

Not allowed:

- Do not edit P24 or earlier artifacts.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not create executable Python, MATLAB, Octave, Julia, shell, TensorFlow,
  JAX, or production code.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-plan-2026-06-02.md`
- `...p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.tex`
- compiled PDF beside the note
- `...p25-zhao-cui-chair-implementation-bridge-result-2026-06-02.md`
- `...p25-zhao-cui-five-gap-closure-ledger-2026-06-02.md`
- `...p25-zhao-cui-source-support-ledger-2026-06-02.md`
- `...p25-zhao-cui-claim-support-ledger-2026-06-02.md`
- `...p25-zhao-cui-claude-review-ledger-2026-06-02.md`
- `...p25-zhao-cui-discrepancy-report-2026-06-02.md`

Every markdown artifact must contain:

- `metadata_date`
- `seed_papers`
- `what_is_not_concluded`

## Required Expansion Blocks

### Gap 1: Bayesian-To-TT Plausibility Bridge

Add a chair-facing mathematical bridge before or near the moderate-rank
section:

- start from the exact filtering posterior as a high-dimensional function;
- show why Gaussian projection may be too restrictive after nonlinear
  observations;
- show how separability generalizes independence without requiring full
  independence;
- derive split-rank from matrix unfolding and then map it to TT rank;
- connect local transition/observation dependence to moderate split-rank;
- explain how preconditioning changes the function whose rank is tested;
- state failure modes as equations and diagnostics.

### Gap 2: One Observation-Step Coordinate Walkthrough

Add a single worked density walk:

- physical target \(q_t(r)\);
- reference target \(\widetilde q_t(z)=q_t(\Psi_t(z))|\det\nabla\Psi_t(z)|\);
- square-root target and squared-TT approximation;
- retained marginal \(a_t(z_t)\) and normalized filter \(\widehat p_t(z_t)\);
- physical retained density with inverse map/Jacobian;
- optional preconditioned residual \(q_t^\sharp(u)\);
- next-step evaluation of \(\widehat p_t\) at a new fitting point.

### Gap 3: Gradient Teaching Layer Before Proposition 2

Add a section before Proposition 2:

- define the scalar \(\widehat\ell_T(\beta;B)\) in one box;
- split fields into frozen structural fields and recomputed differentiable
  fields;
- give a dependency table from target values to log normalizer;
- give the derivative table beside it;
- show a small finite-dimensional scalar analog with one least-squares solve;
- state exactly why the derivative is useful and exactly why it is not the
  adaptive derivative.

### Gap 4: Less-Toy Numerical Trace

Keep the existing constant-basis trace, but add a second trace:

- \(p=2\) basis \((1,z)\) or normalized Legendre basis;
- at least three fitting points;
- visible target values and square-root values;
- a small least-squares coefficient vector;
- approximate normalizer and retained filter value at one point;
- one nonzero \(\partial_\beta f_\beta\) contribution;
- finite-difference check formula for the same branch.

The trace may remain hand-computable and low accuracy, but it must not make TT
look like only a constant approximation.

### Gap 5: Consolidated Fixed Least-Squares Implementation And Derivative Protocol

Add one consolidated mathematical protocol:

- fixed least-squares lane, explicitly distinguished from adaptive TT-cross;
- inputs, outputs, frozen branch fields, differentiable fields;
- initialization;
- left-to-right and right-to-left sweep order;
- update equations for \(L,R,A,N,d,g\);
- derivative equations for \(\dot L,\dot R,\dot A,\dot N,\dot d,\dot g\);
- stopping rule;
- retained-filter construction;
- failure-exit table with condition, mathematical test, and report field.

## Claude Review Protocol

Claude Code is a bounded hostile reviewer only.  Codex remains supervisor and
final authority.

Run Claude worker commands with elevated/trusted permissions.

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p25-zhao-cui-chair-implementation-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p25-zhao-cui-chair-implementation-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Claude reviews must include:

- former chemistry academic chair;
- numerical computation professor;
- implementation engineer focused on mathematical implementability;
- scholarly citation/style reviewer.

Claude must reject if P25 summarizes away P24 or if any of the five expansion
blocks is materially missing.

## Codex-Supervisor Audit Protocol

For every Claude finding, Codex must classify it as:

- `ACCEPT`;
- `PARTIAL`;
- `DISPUTE`;
- `CLARIFY`.

If Codex accepts or partially accepts a finding, patch the relevant files and
record the exact control added.  If Codex disputes a finding, record a concise
rebuttal with file/section evidence and include it in the next Claude prompt.

If Claude execution review stalls, record the attempted commands, smoke-test
status, and block formal acceptance rather than claiming review success.

## Validation Requirements

- Build P25 PDF with `latexmk`.
- Run `pdftotext` and confirm required expansion block headings appear.
- Confirm P25 TeX and PDF are no shorter than P24.
- Scan PDF text for banned governance/process language and old audit tags.
- Scan LaTeX log for errors, undefined references, undefined citations,
  missing files, and rerun blockers.
- Run whitespace and scoped `git diff --check`.
- Confirm all P25 markdown artifacts contain the required metadata fields.
- Confirm only allowed P25 files changed, ignoring unrelated pre-existing dirty
  files.

## Final Response Requirements

Final response must include:

- what Codex inspected;
- Claude plan review history;
- Claude execution review history;
- Codex audit classifications summary;
- files changed;
- PDF build status;
- validation commands run;
- remaining chemist-chair gaps;
- remaining implementation-math gaps;
- final probability estimate that P25 passes a skeptical mixed panel.
