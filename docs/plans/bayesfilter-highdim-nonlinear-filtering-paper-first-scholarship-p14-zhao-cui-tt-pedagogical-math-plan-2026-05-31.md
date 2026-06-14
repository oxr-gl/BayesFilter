# P14 Plan: Zhao-Cui TT Pedagogical Mathematical Rewrite

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code-audit and source ledgers.
- P11 fixed-branch derivative note.
- P12 self-contained proof expansion note.
- P13 human-readable note and ledgers.

what_is_not_concluded:
- No posterior accuracy claim.
- No HMC readiness claim.
- No global derivative of adaptive TT-cross/rank-changing code.
- No production BayesFilter implementation.
- No default-method recommendation.
- No numerical validation of TT filtering on the target high-dimensional model.

## Purpose

P13 is much cleaner than P12, but it still reads too quickly for an important
panel member with a chemistry/physics background.  P14 must teach the same
fixed-branch Zhao-Cui TT filtering construction with more mathematical
exposition, more intermediate equations, and more prose after the mathematics.

The standard is:

> A former chemistry academic who knows probability, integrals, Gaussian
> likelihoods, and numerical linear algebra should be able to understand the
> purpose of each construction, see why it is mathematically reasonable, and
> explain the method back without opening Zhao-Cui or the P10--P13 ledgers.

## Allowed Writes

- New P14 files under `docs/plans/`.
- New P14 `.tex` note and compiled `.pdf`.
- Do not overwrite P13.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.tex`
- compiled PDF beside it
- `...p14-zhao-cui-tt-pedagogical-math-ledger-2026-05-31.md`
- `...p14-zhao-cui-tt-reader-panel-ledger-2026-05-31.md`
- `...p14-zhao-cui-tt-gradient-teaching-ledger-2026-05-31.md`
- `...p14-zhao-cui-tt-source-support-ledger-2026-05-31.md`
- `...p14-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md`
- `...p14-zhao-cui-tt-claude-review-ledger-2026-05-31.md`
- `...p14-zhao-cui-tt-discrepancy-report-2026-05-31.md`
- `...p14-zhao-cui-tt-pedagogical-math-result-2026-05-31.md`

## Core Critiques To Fix

1. Proposition 2 is still dense.  It must be broken into mathematical layers:
   scalar, one-step derivative, square-root derivative, TT contraction
   derivative, core sensitivity, previous-filter sensitivity, and final score.
2. Section 3 is too dense for a chemistry/physics reader.  It must teach tensor
   trains through a low-dimensional grid and low-rank coupling example before
   the full TT notation.
3. Sections 4--11 need more mathematics, not merely more prose.  Each section
   should first display the mathematical object or construction, then explain
   its meaning in prose.
4. Prose must not sound condescending.  It should explain why the displayed
   equations are there, not replace them.
5. Human-readable caveats should remain mathematical: approximation error,
   rank growth, branch changes, conditioning, and finite-difference parity.

## Pedagogical Rule

For Sections 3--11, use the pattern:

1. Display the mathematical object.
2. Work through a small or intermediate construction.
3. Then explain in prose what the equations mean and why the reader should care.
4. State the failure mode in mathematical terms.

Avoid the reverse order when possible.  The target audience likes math and
likes explanation, but will not trust prose that arrives without equations.

## Source-Discipline Execution Rule

Every substantive teaching claim in Sections 4--11, Proposition 1, and
Proposition 2 must be labeled in the P14 source-support ledger as one of:

- `PAPER_EXPLICIT`: stated in checked technical parts of Zhao--Cui or
  Cui--Dolgov, with section/equation/algorithm/proposition anchor.
- `DERIVED_IN_NOTE`: derived in the P14 note or inherited from P12/P13 project
  derivation, with equation/proposition anchor.
- `IMPLEMENTATION_INTERPRETATION`: inferred from inspected companion-code
  behavior, with code path and a statement that mathematical justification is
  still the note derivation.

No major teaching claim may be left unlabeled.  Paper pointers may appear only
after the construction has been derived or clearly identified as source
context.

## Required P14 Note Structure

1. Filtering Objects Before Tensor Notation
2. Scalar Nonlinear Filtering Example
3. Tensor Trains As Low-Rank Coupling, Not Magic Compression
4. From Square-Root Approximation To A Filter
5. The Zhao-Cui Sequential Construction
6. Why Adaptive TT Filtering Is Not Automatically A Gradient Method
7. The Fixed-Branch Filtering Algorithm
8. Proposition 1: Normalized Approximate Filtering
9. Proposition 2 In Layers: Same-Scalar Gradient
10. Algorithmic Gradient Recipe
11. What The Construction Gives And What Must Be Tested
Appendix: Source and code anchors.

## Section-Specific Requirements

### Section 3

Must include:
- a two-coordinate coefficient matrix \(F_{ab}\);
- rank factorization \(F_{ab}\approx\sum_{\ell=1}^r U_{a\ell}V_{\ell b}\);
- three-coordinate extension
  \(F_{abc}\approx\sum_{\ell_1,\ell_2}G_1(a,\ell_1)G_2(\ell_1,b,\ell_2)G_3(\ell_2,c)\);
- the functional version
  \(\phi(u)=G_1(u_1)\cdots G_D(u_D)\);
- storage comparison;
- physical/chemical interpretation as limited long-range coupling, not a
  guarantee.

### Sections 4--5

Must derive:
- why approximating \(\sqrt q\) and squaring gives nonnegativity;
- why the defensive term is added;
- normalizer and marginal filter;
- conditional distributions and KR map at the level needed for understanding,
  not implementation-heavy code details.

### Section 6

Must mathematically show:
- adaptive branch \(B(\alpha)\);
- branch-dependent scalar \(\widehat\ell(\alpha;B(\alpha))\);
- fixed-branch derivative differentiates
  \(\alpha\mapsto\widehat\ell(\alpha;B_0)\), not the piecewise adaptive map.

### Section 7

Must give enough equations and pseudocode for a minimal fixed-branch prototype,
including interpolation and least-squares alternatives, saved branch objects,
and marginal numerator \(a_t\).

### Section 9

Must split Proposition 2 into reader layers:
- layer A: derivative of \(\log z-c\);
- layer B: derivative of \(z=\int(\phi^2+\tau\lambda)\);
- layer C: derivative of \(\phi=G_1\cdots G_D\);
- layer D: derivative of mass contraction;
- layer E: derivative of interpolation/least-squares core solve;
- layer F: derivative of previous filter;
- final proposition and proof.

### Section 10

Must provide a full algorithmic gradient recipe with inputs, forward pass,
saved objects, sensitivity pass, and finite-difference parity test.

## Evidence Contract

Question:

Can the fixed-branch Zhao-Cui TT filtering and gradient construction be taught
in a mathematically rich way that a skeptical chemistry/physics panel member
can follow and find non-condescending?

Baseline:

- P13 human-readable note.

Primary pass criteria:

- Section 3 teaches TT through low-rank coupling examples before core notation.
- Sections 4--11 use equations first, prose second.
- Proposition 2 is decomposed into layers before the formal statement.
- The fixed-branch algorithm remains implementable.
- Source/code anchors stay out of the main teaching flow.
- The reader-panel ledger verifies, for each required section:
  1. a displayed mathematical object appears before the main explanatory prose;
  2. at least one intermediate worked step exists between definition and
     conclusion;
  3. the section states why the object matters to filtering or gradients;
  4. the section states at least one mathematical failure mode or caveat;
  5. prose explains the displayed equations without replacing them.
- Proposition 2 layers A--F are each followed by plain mathematical prose
  explaining what the layer contributes to the same-scalar gradient.
- The source-support ledger labels every major teaching claim as
  `PAPER_EXPLICIT`, `DERIVED_IN_NOTE`, or `IMPLEMENTATION_INTERPRETATION`.
- Claude execution review accepts, or remaining issues are minor editorial
  layout issues.

Veto diagnostics:

- Section 3 remains a notation dump.
- Proposition 2 remains a single dense proof wall.
- Sections 4--11 add prose without adding mathematical exposition.
- Sections 4--11 add equations without intermediate derivation or explanation
  of what each displayed object contributes to the filter construction.
- The text sounds patronizing or hand-wavy.
- Paper pointers replace derivations.
- Major teaching claims are not labeled in the source-support ledger.
- The fixed-branch gradient scalar is weakened or changed without saying so.
- LaTeX fails to build.

Explanatory diagnostics:

- The note may become longer than P13; length is acceptable if the math is
  clear and purposeful.
- The note is still not a numerical validation or implementation.

## MathDevMCP Protocol

Use MathDevMCP only for narrow algebraic obligations:
- log-normalizer derivative;
- normalized-density derivative;
- square-root normalizer derivative in scalar symbolic form;
- rank-factorized storage algebra if useful;
- fixed linear solve derivative \(Ag=b\);
- least-squares normal-equation derivative in simplified form if feasible.

Record:
- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Do not claim broad machine certification of the full TT proof.

Layer boundary:
- Layers A and B of Proposition 2 may use MathDevMCP for scalar log and
  normalizer derivative checks.
- Layer D may use MathDevMCP only for scalar or matrix product-rule sanity
  checks; the TT contraction argument must remain a human-readable derivation.
- Layers C, E, F, and the final proposition linkage must be justified in the
  note and ledgers; MathDevMCP is auxiliary only.
- The MathDevMCP ledger must name the exact lemma or identity checked and the
  surrounding human argument that does not depend on MCP trust.

## Claude Review Loop

Claude Code is a bounded hostile reviewer only.  Codex remains final authority.

Plan review command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p14-zhao-cui-tt-pedagogical-math-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p14-zhao-cui-tt-pedagogical-math-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile pedagogical mathematical review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.

After each Claude review, Codex must classify every finding as:
- `ACCEPT`
- `PARTIAL`
- `DISPUTE`
- `CLARIFY`

Accepted and partially accepted findings must be patched and recorded.  Disputed
findings must be rebutted with file/section evidence and carried into the next
Claude prompt.  If disagreement remains after round 5, record it in the
discrepancy report and stop unless the human explicitly decides.

The Claude review ledger must maintain a no-silent-drop finding register with:
- review round;
- finding ID;
- Claude finding summary;
- Codex classification;
- action taken;
- evidence path;
- current status: `open`, `resolved`, `disputed`, or `carried_forward`.

No finding may disappear between rounds without an explicit status entry.

## Validation

Run:

```text
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.tex
latexmk -cd -c docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.tex
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-*
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.pdf - | rg -n "Tensor Trains As Low-Rank Coupling|Proposition 2 In Layers|Algorithmic Gradient Recipe|What The Construction Gives"
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.pdf - | rg -n "Layer A|Layer B|Layer C|Layer D|Layer E|Layer F|Why this matters|Failure mode"
```

Also check the final log before cleanup for undefined citation/reference,
rerun, overfull, and underfull warnings.

## Skeptical Plan Audit

P13 is the correct baseline because it already preserves the P12 proof spine,
has a compiled PDF, and was accepted by Claude, yet its own result records that
Proposition 2 remains dense and that a future reader-facing version should be
more pedagogical.  The risk in P14 is not mathematical novelty; it is
pedagogical failure caused by either adding equations without teaching them or
adding prose that feels condescending because it is not anchored in equations.

Claude acceptance is only a bounded hostile pedagogical review, not a
truth-certification or a panel guarantee.  MathDevMCP can check small algebraic
identities, but the main evidence for the note must be the written derivation,
the source-support ledger, and the reader-panel ledger.

The planned artifacts answer the question because the note is the reader-facing
object, the reader-panel ledger checks the chemistry/physics audience standard
section by section, the source-support ledger prevents unsupported pedagogical
drift, the MathDevMCP ledger records narrow algebraic checks honestly, and the
Claude ledger/discrepancy report records hostile review closure.

## Stop Conditions

Stop and report a blocker if:
- the rewrite would weaken the fixed-branch scalar or Proposition 1/2;
- the mathematical exposition cannot be made understandable without changing
  the claim;
- Claude identifies a major mathematical or pedagogical blocker that Codex
  accepts and cannot patch in scope;
- Codex and Claude disagree after five iterations;
- LaTeX fails after focused repair.

Decision:
`PLAN_READY_FOR_CLAUDE_REVIEW`
