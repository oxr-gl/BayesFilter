# P16 Plan: Zhao-Cui Annotated Reconstruction For Human Readers

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit, paper-code crosswalk, filtering-scalar, reproducibility, and gradient-feasibility ledgers.
- P15 fixed-branch implementability specification and two-step reference example.

what_is_not_concluded:
- No claim that the adaptive Zhao-Cui code has a globally smooth analytical gradient.
- No claim that a fixed-branch derivative proves posterior accuracy.
- No claim that the method is production-ready in BayesFilter.
- No claim that high-dimensional performance has been validated on the target BayesFilter model.
- No default-method recommendation.

## Purpose

P13--P15 repaired parts of the Zhao--Cui story, but the reader-facing text
regressed away from the paper's natural explanation.  P16 will therefore build
a new annotated reconstruction that follows Zhao--Cui Sections 1--3 and 5 in
order, with selected support only from Section 4, Section 6 numerical
evidence, Appendix A, and checked companion-code paths.  The text must not
summarize the paper.  It must slow the paper down.

The document should be understandable to an educated academic from chemistry,
physics, numerical analysis, or applied mathematics who has not read the
original paper and has not studied tensor trains.  The document may be long.
The target is a 50--60 page teaching note if the PDF layout supports it.

The main reader-facing note must do three things, in this order:

1. Reconstruct Zhao--Cui's sequential filtering algorithm in BayesFilter
   notation, equation by equation.
2. Explain the fixed-branch TT filtering variant only after the original method
   is clear, and prove that the fixed-branch variant performs a normalized
   approximate filtering recursion for its declared approximation.
3. Derive the same-scalar analytical derivative for the fixed-branch scalar and
   prove exactly what scalar is differentiated.

## Skeptical Pre-Execution Audit

This plan passes the pre-execution audit only if all of the following controls
remain in force:

- The baseline is the Zhao--Cui paper itself, not P15's simplified variant.
- The output is a reader-facing mathematical note, not an internal governance
  artifact.
- "Source anchor" means a concise citation to a paper equation, algorithm,
  section, or checked code path; it must not replace the derivation.
- Every numbered equation and algorithm in Zhao--Cui Sections 1--3 and 5 must
  receive an explicit equation-ledger disposition.
- Governance, process, and audit language must stay out of the main
  reader-facing note.  Those terms belong only in ledgers, review artifacts,
  discrepancy reports, and result files.
- The note must not rely on abstracts, introductions, conclusions, metadata, or
  venue rank for theorem or algorithm support.
- The note must not copy long passages from Zhao--Cui.  Equations may be
  restated in BayesFilter notation, and prose must be original.
- Fixed-branch differentiation is presented as a BayesFilter extension needed
  for same-scalar gradients, not as a claim about global differentiability of
  Zhao--Cui's adaptive implementation.
- The plan includes stop conditions for source, derivation, build, and review
  blockers.

Decision: `PRE_EXECUTION_AUDIT_PASS_WITH_SCOPE_NARROWING`.

## Evidence Contract

Question:

Can a self-contained annotated reconstruction of Zhao--Cui Sections 1--3 and 5
teach the algorithm clearly enough that Codex or Claude Code could implement a
minimal squared-TT sequential filter, then understand why a fixed-branch
variant is needed for analytical gradients and implement that variant's
same-scalar derivative?

Baselines and comparators:

- Zhao--Cui JMLR 2024, Sections 1--3 and 5, with selected support only from
  Section 4, Section 6 numerical evidence, Appendix A, and checked
  companion-code paths.
- P10 paper-code crosswalk and filtering-scalar ledgers.
- P15 fixed-branch implementability specification and reference example.
- Fixed sparse-grid Gaussian projection filter from `ch34`, as the other main
  high-dimensional candidate.

Primary pass criteria:

- The note follows Zhao--Cui's order rather than inventing a new compressed
  order.
- Every important Zhao--Cui equation used from Sections 1--3 and 5 is mapped to
  BayesFilter notation, with all symbols defined before use.
- Every numbered Zhao--Cui equation and algorithm from Sections 1--3 and 5 is
  entered in the equation-by-equation ledger with status `expanded`,
  `intentionally_omitted_with_reason`, or `deferred_to_support_section`.
- Every major formula is derived in intermediate steps before prose
  interpretation.
- The text explains why the formula matters for filtering before moving on.
- The note covers the user's missing implementability list:
  exact domain/reference measure; basis evaluation; mass matrices; fitting
  point choices; TT-cross/interpolation/least-squares core construction;
  rank/fixed-rank protocol; defensive \(\tau_t\) and reference \(\lambda_t\);
  scaling constant \(c_t\); TT marginalization; conditional/KR maps; data
  structures; stored branch objects; gradient recursion; numerical
  stabilization; finite-difference tests; minimal runnable example.
- The fixed-branch section proves normalized approximate filtering for the
  declared approximation, not exact posterior accuracy.
- The gradient section proves the derivative of the declared approximate scalar
  and distinguishes smooth, branch-local, adaptive, and unsupported operations.
- Claude plan review and execution review accept, or remaining findings are
  minor editorial/layout issues after the maximum loop.

Veto diagnostics:

- Any main-text phrase equivalent to "fit a TT" without an immediately nearby
  mathematical construction and one concrete implementable protocol.
- Any normalizer/evidence formula that is not tied to a computable contraction.
- Any conditional map or KR map that appears before the reader has seen the
  marginal/conditional density formula it uses.
- Any gradient formula that does not differentiate the same scalar used by the
  forward pass.
- Any adaptive TT-cross, rank change, pivot change, domain change, or branch
  change treated as globally smooth.
- Any code-path sentence in the main note that is not translated into a
  mathematical object first.
- Any material Claude finding accepted or partially accepted by Codex but not
  patched.
- Any unresolved Codex-Claude disagreement after round 5 unless the human
  explicitly overrides.
- LaTeX build failure, undefined references/citations that block the document,
  or missing generated PDF.

Explanatory diagnostics:

- Code anchors, source ledgers, fit residuals, mass ratios, condition numbers,
  rank counts, and finite-difference parity errors explain implementation risk;
  they do not prove posterior accuracy or production readiness.

Artifact preserving the result:

- P16 plan, note, PDF, ledgers, Claude review ledger, discrepancy report, and
  result file under `docs/plans/`.

## Allowed Writes

Allowed:

- New P16 files under `docs/plans/`.
- The compiled P16 PDF and auxiliary LaTeX files beside the P16 note.

Not allowed:

- Do not overwrite P10--P15 artifacts.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane files, student-baseline files, controlled-DPF files, or
  public APIs.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.tex`
- compiled PDF beside it
- `...p16-zhao-cui-annotated-reconstruction-ledger-2026-06-01.md`
- `...p16-zhao-cui-equation-by-equation-ledger-2026-06-01.md`
- `...p16-zhao-cui-bayesfilter-translation-ledger-2026-06-01.md`
- `...p16-zhao-cui-code-crosswalk-ledger-2026-06-01.md`
- `...p16-zhao-cui-fixed-branch-ledger-2026-06-01.md`
- `...p16-zhao-cui-gradient-derivation-ledger-2026-06-01.md`
- `...p16-zhao-cui-source-support-ledger-2026-06-01.md`
- `...p16-zhao-cui-citation-venue-metadata-ledger-2026-06-01.md`
- `...p16-zhao-cui-backward-snowball-ledger-2026-06-01.md`
- `...p16-zhao-cui-forward-snowball-ledger-2026-06-01.md`
- `...p16-zhao-cui-claim-support-ledger-2026-06-01.md`
- `...p16-zhao-cui-omitted-paper-risk-ledger-2026-06-01.md`
- `...p16-zhao-cui-mathdevmcp-ledger-2026-06-01.md`
- `...p16-zhao-cui-claude-review-ledger-2026-06-01.md`
- `...p16-zhao-cui-discrepancy-report-2026-06-01.md`
- `...p16-zhao-cui-annotated-reconstruction-result-2026-06-01.md`

Every ledger must contain:

- `metadata_date`
- `seed_papers`
- `what_is_not_concluded`

The source-support ledger must also record, for each supporting source:

- publication status;
- local full-text path or full-text blocker;
- retraction, withdrawal, erratum, and quarantine status;
- version/publisher consistency status when applicable;
- inspected technical sections, equations, algorithms, theorems, proofs,
  appendices, or experiments;
- allowed claims and forbidden claims.

The citation/venue metadata ledger must record dated metadata when available.
If network or metadata access is unavailable or not authorized, the ledger must
record `metadata_blocked` rather than inventing citation counts, venue ranks, or
fresh forward-snowball coverage.

## Reader-Facing Note Structure

The note must use this structure unless a plan patch is reviewed:

1. What problem is being solved?
2. State-space model and BayesFilter notation.
3. From joint density to filtering, parameter learning, path learning, and
   smoothing.
4. The exact recursion that creates the computational bottleneck.
5. Tensor trains from first principles.
6. Why TT marginalization is cheap once the representation exists.
7. Zhao--Cui Algorithm 1, fully annotated.
8. Why nonnegativity fails and why square-root TT repairs it.
9. Squared-TT density, defensive reference, and normalizer.
10. Squared-TT marginalization, with a full mass-matrix derivation.
11. Conditional densities and KR maps from marginal ratios.
12. Zhao--Cui Algorithm 2, fully annotated.
13. Forward conditional map and the particle-filter correction.
14. Backward conditional map, path estimation, and smoothing.
15. Error propagation: what it proves and what it does not prove.
16. Preconditioning: change of variables, bridge density, pushforward ratio,
    composition, and normalizer.
17. Implementable branch objects and data structures.
18. Fixed-branch TT filtering recursion.
19. Proposition 1: fixed-branch recursion is a normalized approximate filtering
    recursion for the declared scalar.
20. Same-scalar analytical derivative.
21. Proposition 2: fixed-branch gradient differentiates the declared scalar.
22. Numerical stabilization, failure diagnostics, and finite-difference test.
23. Minimal runnable example specification.
24. Reader-facing conclusion.

## Equation-By-Equation Protocol

The equation-by-equation ledger must enumerate every numbered equation and
algorithm in Zhao--Cui Sections 1--3 and 5 in source order.  Each item must have
one status:

- `expanded`: reconstructed in the P16 note with the protocol below.
- `intentionally_omitted_with_reason`: not needed for the P16 target, with a
  human-readable reason.
- `deferred_to_support_section`: discussed briefly because it supports, but is
  not central to, the P16 target.

The validation fails if any numbered item lacks a disposition.

For each source equation or algorithm from Zhao--Cui that the note expands:

1. Give a concise source anchor, for example "Zhao--Cui Eq. (15)".
2. Restate the equation in BayesFilter notation.
3. Define every symbol, dimension, and measure.
4. Derive the formula from the previous formula, using explicit integrals.
5. Explain the filtering meaning in prose after the derivation.
6. State what would be stored in an implementation.
7. State the failure mode or approximation risk.

The prose must be original.  Long quotations from the paper are forbidden.
Governance, process, and audit language is forbidden in the main note except
where it is ordinary mathematical language.  Review history, source-status
language, and process labels belong in ledgers and result files.

## BayesFilter Notation Protocol

Use these names consistently:

- State \(x_t\in\mathbb R^{m_x}\).
- Static parameter \(\alpha\in\mathbb R^{m_\alpha}\).
- Observation \(y_t\in\mathbb R^{m_y}\).
- Transition density \(f_\alpha(x_t\mid x_{t-1})\).
- Observation density \(g_\alpha(y_t\mid x_t)\).
- Previous approximate filter \(\widehat p_{t-1}(x_{t-1},\alpha)\).
- New unnormalized target
  \[
    q_t(x_t,\alpha,x_{t-1})
    =
    \widehat p_{t-1}(x_{t-1},\alpha)
    f_\alpha(x_t\mid x_{t-1})
    g_\alpha(y_t\mid x_t).
  \]
- Approximate normalizer
  \[
    \widehat Z_t=\int \widehat q_t(x_t,\alpha,x_{t-1})
      \,dx_t\,d\alpha\,dx_{t-1}.
  \]
- Approximate log scalar
  \[
    \widehat\ell_T(\alpha)=\sum_{t=1}^T\log \widehat Z_t(\alpha).
  \]

When the paper uses \(\theta\), the P16 note should explain once that
BayesFilter writes the unknown parameter as \(\alpha\) to avoid confusion with
generic derivative directions.

## Fixed-Branch And Gradient Protocol

The fixed-branch variant is introduced only after Zhao--Cui's adaptive method is
understood.  It freezes:

- domain/reference map;
- basis family and degrees;
- fitting points and weights;
- rank pattern;
- core-construction protocol and sweep count;
- ridge or interpolation regularization;
- defensive reference \(\lambda_t\);
- defensive mass \(\tau_t\);
- scaling shift \(c_t\);
- preconditioner branch if used;
- all conditional-map rootfinding tolerances and branch decisions.

The derivative must be through every stored object that the forward scalar uses:

- transformed fitting target;
- fitted TT core coefficients;
- square-core/mass contractions;
- marginal numerator;
- normalizer;
- carried filter object;
- next-step target evaluations;
- final \(\sum_t\log\widehat Z_t\).

Adaptive variants may be described as piecewise smooth only after freezing the
realized branch.  Without freezing, the note must say the ordinary analytical
gradient is not the derivative of a single smooth scalar.

## MathDevMCP Protocol

Use MathDevMCP only for narrow identities:

- normalization derivative;
- derivative of \(\log Z\);
- derivative of a fixed finite-dimensional linear solve;
- contraction derivative by product rule;
- change-of-variables identity for a triangular map when locally stated;
- determinant/Jacobian chain rule identities.

Record one of:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Do not claim broad certification of TT filtering.

## Claude Review Loops

### Plan Review

Run up to five rounds:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p16-zhao-cui-annotated-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.  Codex must independently audit
every Claude finding before patching or accepting the plan.

### Execution Review

Run up to ten rounds:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p16-zhao-cui-annotated-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

The execution review prompt must include two personas:

1. Technical reviewer: source support, derivation, same-scalar gradient,
   implementability, code-crosswalk honesty.
2. Fresh chemist-reader reviewer: explicitly state what is not self-contained,
   what is not convincing, and exactly what would satisfy the reader.

## Codex-Supervisor Audit Protocol

After each Claude Code review round, Codex must independently audit Claude's
findings before patching or accepting them.

For every Claude finding, Codex must classify it as:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a different or narrower patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken
  the document.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

Codex must record this classification in the review-loop artifact.

If Codex accepts or partially accepts a finding, Codex must patch the relevant
files and record the exact control added.

If Codex disputes a finding, Codex must write a concise rebuttal with
file/section evidence and include that rebuttal in the next Claude prompt,
asking Claude to either:

1. withdraw the finding;
2. revise it with a more precise required change; or
3. explain why the rebuttal is wrong.

Codex must not silently ignore disputed findings.  Claude `ACCEPT` is not
sufficient unless Codex also independently agrees that the current text enforces
the required controls.

If Codex and Claude still disagree after round 5, record the disagreement in
the final discrepancy report and block downstream execution unless the human
explicitly decides.

## Validation

Run:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.tex
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-*
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.pdf -
rg -n "undefined|Rerun|Warning: Citation|Warning: Reference|Label\\(s\\) may have changed" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.log
```

The `pdftotext` check must confirm that the note contains:

- annotated Zhao--Cui Algorithm 1;
- annotated squared-TT Algorithm 2;
- KR conditional-map derivation;
- preconditioning derivation;
- fixed-branch recursion;
- same-scalar gradient proposition;
- diagnostics and finite-difference test;
- minimal runnable example specification.

## Stop Conditions

Stop and report before downstream execution if:

- the local Zhao--Cui PDF is unavailable;
- any supporting source lacks a clean source-support disposition for
  publication status, full-text status, retraction/quarantine status, and
  version/publisher consistency, or is quarantined;
- the plan review has unresolved major blockers after five rounds;
- the note cannot be made self-contained without copying protected text;
- the gradient proof cannot be honestly stated as same-scalar and fixed-branch;
- Claude and Codex have unresolved major disagreements after round 5 and no
  human override is given;
- LaTeX cannot build for reasons unrelated to a minor syntax patch;
- validation shows the PDF omits a required P16 section.
