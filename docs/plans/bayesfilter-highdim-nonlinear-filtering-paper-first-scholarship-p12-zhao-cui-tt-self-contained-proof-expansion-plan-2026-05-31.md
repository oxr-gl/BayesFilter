# P12 Plan: Zhao-Cui TT Self-Contained Proof Expansion

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports."
- Zhao-Cui companion code audit snapshot at `third_party/audit/zhao_cui_tensor_ssm_p10/source`.
- P10 Zhao-Cui code-audit, paper-code crosswalk, filtering-scalar, reproducibility, and gradient-feasibility ledgers.
- P11 Zhao-Cui fixed-branch analytical derivative note and ledgers.

what_is_not_concluded:
- No claim that the adaptive Zhao-Cui companion code has a global smooth analytical gradient.
- No claim that the fixed-branch TT approximation equals the exact posterior filter except under explicitly stated zero-approximation-error conditions.
- No HMC readiness until a concrete same-scalar implementation passes finite-difference parity and branch-stability tests.
- No posterior accuracy, production readiness, NAWM readiness, GPU/XLA readiness, or default-method recommendation.
- No permission to copy third-party LGPL/GPL code into production BayesFilter modules.

## Purpose

Expand the current standalone Zhao-Cui P11 LaTeX derivative note into a
panel-readable mathematical document that proves the two facts a skeptical
reviewer will require:

1. the fixed-branch tensor-train construction is a well-defined approximate
   Bayesian filtering recursion; and
2. the analytical gradient is the exact derivative of the declared approximate
   likelihood scalar computed by that recursion.

The expansion must also give a self-contained exposition of the Zhao-Cui
algorithm before introducing the BayesFilter fixed-branch variant.  The target
reader is a numerical analyst, physicist, chemist, applied mathematician, or
industrial quant who knows probability and numerical linear algebra but does
not already know tensor-train filtering or inverse Rosenblatt transports.

## Target Artifact

Primary target:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex`
- compiled PDF beside the `.tex` file.

Supporting artifacts:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-proposition-proof-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-source-anchor-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-source-support-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-claim-support-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-coverage-and-omission-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-claude-review-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-result-2026-05-31.md`

Allowed writes:

- New P12 files under `docs/plans/`.
- The existing P11 `.tex` note may be copied into the P12 note as starting
  material, but P11 artifacts should not be overwritten.
- No edits to `docs/chapters/` in this pass unless a later execution prompt
  explicitly expands the scope.
- No edits to production `bayesfilter/`, DPF lane files, student-baseline
  files, controlled-DPF files, public APIs, or unrelated dirty files.
- No commits.

## Skeptical Plan Audit

The main failure mode is to write a proof that proves the wrong thing.  The
published Zhao-Cui adaptive algorithm uses approximation choices that are
algorithmically valuable but not globally smooth: TT-cross pivots, rank changes,
rounding/truncation, random/debug samples, stopping criteria, selected
minimizers, and QR/SVD branch choices.  A proposition that treats those choices
as one smooth map would fail review.

The correct plan is to separate three objects:

1. the Zhao-Cui published algorithm, explained faithfully as a sequential
   squared-TT approximation and conditional transport method;
2. the BayesFilter fixed-branch variant, which freezes the approximation
   branch so the recursion is a deterministic mathematical map; and
3. the declared approximate likelihood scalar and its same-scalar derivative.

The proposition about filtering should prove normalized approximate filtering,
not exact posterior accuracy.  The proposition about the gradient should prove
same-scalar differentiation under stated fixed-branch regularity conditions,
not HMC convergence or adaptive-code differentiability.

## Evidence Contract

Question:

Can the Zhao-Cui TT sequential filtering material be expanded into a
self-contained proposition-proof document that rigorously defines the
fixed-branch approximate filtering recursion and proves its same-scalar
analytical gradient?

Baseline/comparator:

- P11 derivative note, which proves the fixed-branch score formula but does not
  yet give a full beginner-accessible exposition or a proposition-proof proof of
  filtering correctness.
- P10 paper-code crosswalk, which identifies the source normalizer and code
  scalar but does not prove a fixed-branch BayesFilter variant.

Primary pass criteria:

- A reader can reconstruct the Zhao-Cui sequential filtering algorithm from the
  document without reading the paper first.
- Every algorithmic object is defined before use: state-space model, filtering
  density, prediction density, unnormalized update, evidence increment,
  tensor-train core, squared-TT density, defensive density, normalizer,
  marginalization, conditional Rosenblatt map, fixed branch, branch-local
  derivative, and same-scalar gradient.
- The note states and proves Proposition 1: fixed-branch TT filtering recursion
  is a well-defined normalized approximate Bayesian filtering recursion.
- The note states and proves Proposition 2: the analytical gradient
  differentiates exactly the declared fixed-branch approximate likelihood
  scalar.
- The proof explicitly carries the recursion from \(t-1\) to \(t\), including
  marginalization over \(x_{t-1}\).
- The derivative proof includes TT-core sensitivity equations and normalizer
  contraction derivatives.
- Claude accepts the plan and final note, or remaining issues are minor
  editorial/layout issues.
- MathDevMCP verifies all narrow algebraic obligations it can represent, with
  tool limits recorded honestly.

Veto diagnostics:

- The note claims exact filtering when only approximate filtering is proved.
- The note claims a full analytical gradient of adaptive TT-cross/rank-changing
  code.
- The note drops the previous-filter derivative in the recursion.
- The note proves a gradient for a scalar different from the scalar defined in
  the algorithm.
- The fixed branch is not mathematically specified.
- Proposition assumptions are too vague to support the proof.
- Source anchors rely on abstracts, metadata, venue prestige, or unsupported
  paraphrase rather than checked technical sections/equations/algorithms.
- Required scoped source-support, claim-support, coverage/omission, or
  quarantine/version ledgers are missing.
- Claude finds a major missing term, unsupported claim, or unreadable
  proposition.
- MathDevMCP contradicts a narrow identity used in the proof.
- LaTeX does not compile.

Explanatory diagnostics:

- MathDevMCP inability to encode function-valued integrals or TT contractions.
- Minor overfull boxes from long code paths.
- Remaining implementation obligations such as finite-difference parity tests.
- Need for later chapter integration into `ch35`/`ch37`.

Artifact preserving the result:

- P12 expanded LaTeX note and PDF.
- P12 proof, source-anchor, source-support, claim-support,
  coverage-and-omission, MathDevMCP, Claude review, and result ledgers.

## Source Discipline

Use Zhao-Cui and Cui-Dolgov only for checked technical constructions:

- Zhao-Cui Algorithm 1: sequential nonseparable density and TT approximation.
- Zhao-Cui equation/section defining squared-TT defensive density and
  normalizer.
- Zhao-Cui Algorithm 2: squared-TT sequential estimation.
- Zhao-Cui Section 4.1: evidence/normalizer and approximation of \(q_t\).
- Cui-Dolgov only for squared inverse Rosenblatt transport substrate where
  directly needed.
- Companion code only for implementation behavior, especially
  `log(sirt.z)-const` and `obj.z = obj.fun_z + obj.tau`.

Do not use abstracts, introductions, conclusions, citation counts, or venue
rankings as theorem support.  If a source anchor is not checked, mark it as a
source gap rather than presenting it as support.

## Literature-Audit Scope

This pass is not a new broad literature survey.  It is a proof-expansion note
for two already-selected seed constructions: Zhao-Cui sequential squared-TT
filtering and the Cui-Dolgov squared inverse Rosenblatt transport substrate.
The literature audit is therefore scoped, but it still must satisfy the
scholarly policy for the sources used as support.

Required scoped ledgers:

- `source-support`: for Zhao-Cui, Cui-Dolgov, and the companion code snapshot,
  record local artifact path, public source or publisher page when checked,
  publication status, retraction/quarantine/version-conflict check status,
  inspected technical anchors, allowed claims, and forbidden claims.
- `claim-support`: map every important proof/exposition claim in the P12 note
  to one of `PRIMARY_TECHNICAL_SUPPORT`, `PROJECT_DERIVATION`,
  `IMPLEMENTATION_EVIDENCE`, `SOURCE_GAP_BLOCKER`, or
  `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`.
- `coverage-and-omission`: record the scoped backward/forward snowball status,
  relevant direct/foundational omitted papers, why they are not needed for the
  two propositions, and what later chapter-integration work may still require.

The coverage-and-omission ledger may state that full citation-count and
venue-rank metadata are not used as truth evidence and are not required for
the two local propositions.  It must not silently omit obvious direct sources:
Rosenblatt/Knothe for KR terminology, Oseledets/TT-cross for TT background, and
the Zhao-Cui/Cui-Dolgov referenced transport substrate must be classified as
source support, background, or out of proof scope.

Required quarantine/version checks:

- Check the local Zhao-Cui PDF against the public JMLR page or otherwise record
  if network access is unavailable.
- Check the local Cui-Dolgov PDF against the publisher page or otherwise
  record if network access is unavailable.
- Record whether any retraction, withdrawal, expression of concern, major
  erratum, or version mismatch was found in the checked public source.
- If a check cannot be performed, record `SOURCE_STATUS_NOT_EXTERNALLY_CHECKED`
  and do not claim release-grade source completeness.

The note itself should cite only the sources directly needed for the
construction and proof.  The ledgers carry the scholarly audit trail.

## Required Expanded Note Structure

The P12 note should use the following structure.

1. `Introduction And Reader Contract`
   - State what is proved and what is not proved.
   - Explain why a fixed-branch variant is needed for an analytical gradient.
   - State that exact posterior accuracy is empirical or approximation theory,
     not proved by this note.

2. `State-Space Filtering From First Principles`
   - Define state \(x_t\), parameter \(\vartheta\), observations \(y_t\).
   - Define transition density \(f_\alpha(x_t\mid x_{t-1},\vartheta)\),
     observation density \(g_\alpha(y_t\mid x_t,\vartheta)\), prior, filtering
     density, prediction density, update density, and evidence increment.
   - Derive the exact recursion:
     \[
       p(x_t,\vartheta\mid y_{1:t})
       =
       \frac{
       g_\alpha(y_t\mid x_t,\vartheta)
       \int f_\alpha(x_t\mid x_{t-1},\vartheta)
       p(x_{t-1},\vartheta\mid y_{1:t-1})\,dx_{t-1}
       }
       {Z_t(\alpha)}.
     \]

3. `Tensor Trains From First Principles`
   - Define tensor-product basis, TT cores, TT ranks, and evaluation
     \(G_1(r_1)\cdots G_D(r_D)\).
   - Explain why TT is a compression format for high-dimensional functions.
   - Define one-dimensional mass matrices and the contraction used to integrate
     \(\phi^2\).

4. `Zhao-Cui Sequential Squared-TT Algorithm`
   - Reconstruct the published algorithm in BayesFilter notation.
   - Define \(q_t(x_t,\vartheta,x_{t-1})\).
   - Derive why approximating \(q_t\) and integrating it gives an evidence
     increment.
   - Define \(\phi_t\), \(\widehat q_t=\phi_t^2+\tau_t\lambda_t\), normalizer,
     marginal filter, and conditional KR transport role.
   - Explain, in human language, which steps are adaptive in the paper/code.
   - Include pseudocode for the published-style recursion.

5. `Fixed-Branch TT Filtering Variant`
   - Define fixed branch precisely: fixed basis, domains, variable ordering,
     interpolation/cross sets, ranks, local solve schedule, random/debug
     samples, truncation choices, QR/SVD signs/ranks, defensive term policy,
     coordinate maps, and stabilizing constant rule.
   - Explain key differences from the published adaptive code.
   - Explain why freezing is needed: to get a deterministic differentiable
     scalar for same-scalar gradient checks.
   - Include pseudocode for the fixed-branch recursion.

6. `Proposition 1: Fixed-Branch TT Recursion Is A Normalized Approximate Filter`
   - State assumptions clearly.
   - Define the recursive map.
   - Prove:
     - nonnegativity of \(\widehat q_t\);
     - positivity and finiteness of \(\widehat Z_t\);
     - normalization of \(\widehat\pi_t=\widehat q_t/\widehat Z_t\);
     - normalization of the marginal \(\widehat p_t\);
     - induction over time;
     - exact-filter recovery only if \(\widehat q_t=q_t\) at every step.

7. `Proposition 2: Same-Scalar Analytical Gradient`
   - State fixed-branch differentiability assumptions.
   - Define:
     \[
       \widehat\ell_T(\alpha)
       =
       \sum_t\{\log\widehat Z_t(\alpha)-c_t(\alpha)\}.
     \]
   - Prove:
     - derivative of \(\log \widehat Z_t-c_t\);
     - derivative of \(\widehat Z_t=\int\phi_t^2+\tau_t\);
     - product-rule derivative of TT evaluation;
     - differentiated mass-matrix contraction;
     - core sensitivity by fixed interpolation equations;
     - core sensitivity by fixed least-squares equations;
     - recursive derivative of previous filter entering \(q_t\);
     - final score formula.

8. `Corollaries And Boundaries`
   - Corollary: exactness only under zero approximation error.
   - Corollary: adaptive algorithm is piecewise/branch-local unless branch
     choices are frozen or smoothed.
   - State finite-difference parity tests required before HMC use.

9. `Implementation Checklist`
   - Inputs, outputs, dimensions, scalar, derivative objects, branch-stability
     diagnostics, and value-gradient parity diagnostics.

10. `Source Anchors And Code Anchors`
    - List exact paper sections/equations/algorithms and code paths used.

## Proposition 1 Skeleton

Title:

`Fixed-Branch Squared-TT Recursion Defines A Normalized Approximate Filter`

Assumptions:

- All densities are dominated by fixed measures.
- \(\widehat p_{t-1}\ge0\) and integrates to one.
- Fixed branch produces measurable \(\phi_t\).
- \(\lambda_t\ge0\) integrates to one.
- \(\tau_t\ge0\).
- \(0<\widehat Z_t<\infty\).

Definitions:

\[
  q_t(u_t;\alpha)
  =
  \widehat p_{t-1}(x_{t-1},\vartheta;\alpha)
  f_\alpha(x_t\mid x_{t-1},\vartheta)
  g_\alpha(y_t\mid x_t,\vartheta),
\]
\[
  \widehat q_t(u_t;\alpha)
  =
  \phi_t(u_t;\alpha)^2+\tau_t(\alpha)\lambda_t(u_t),
  \qquad
  \widehat Z_t(\alpha)=\int\widehat q_t(u_t;\alpha)\,du_t,
\]
\[
  \widehat\pi_t(u_t;\alpha)
  =
  \widehat q_t(u_t;\alpha)/\widehat Z_t(\alpha),
  \qquad
  \widehat p_t(x_t,\vartheta;\alpha)
  =
  \int \widehat\pi_t(x_t,\vartheta,x_{t-1};\alpha)\,dx_{t-1}.
\]

Proof obligations:

- \(\widehat q_t\ge0\).
- \(\widehat\pi_t\ge0\).
- \(\int\widehat\pi_t=1\).
- \(\int\widehat p_t=1\) by Fubini/Tonelli.
- Induction starts at the prior and propagates normalized approximate filters.
- If \(\widehat q_t=q_t\) for all \(t\), then \(\widehat Z_t=Z_t\) and the
  exact filtering recursion is recovered.

## Proposition 2 Skeleton

Title:

`Analytical Gradient Differentiates The Declared Fixed-Branch Approximate Likelihood`

Assumptions:

- Proposition 1 assumptions hold.
- All branch choices are fixed.
- \(\alpha\mapsto f_\alpha\), \(g_\alpha\), coordinate maps, basis maps,
  core coefficients, \(\tau_t\), and \(c_t\) are differentiable on the branch.
- Differentiation may pass through finite contractions and required integrals.
- Fixed interpolation or least-squares core systems are nonsingular or use a
  declared differentiable pseudoinverse branch.
- \(\widehat Z_t>0\).

Definitions:

\[
  \widehat\ell_T(\alpha)
  =
  \sum_{t=1}^T
  \{\log\widehat Z_t(\alpha)-c_t(\alpha)\}.
\]

Main formula:

\[
  \partial_i\widehat\ell_T(\alpha)
  =
  \sum_{t=1}^T
  \left[
  \frac{\partial_i\widehat Z_t(\alpha)}
       {\widehat Z_t(\alpha)}
  -
  \partial_i c_t(\alpha)
  \right],
\]

\[
  \partial_i\widehat Z_t
  =
  2\int \phi_t(u;\alpha)\partial_i\phi_t(u;\alpha)\,du
  +\partial_i\tau_t.
\]

If \(\phi_t=G_{t,1}\cdots G_{t,D}\), then

\[
  \partial_i\phi_t
  =
  \sum_{k=1}^D
  G_{t,1}\cdots(\partial_iG_{t,k})\cdots G_{t,D}.
\]

For fixed interpolation equations:

\[
  A_{t,k}g_{t,k}=b_{t,k},
  \qquad
  A_{t,k}\partial_i g_{t,k}
  =
  \partial_i b_{t,k}-(\partial_iA_{t,k})g_{t,k}.
\]

For fixed weighted least squares:

\[
  g_{t,k}=\arg\min_g\|W_{t,k}^{1/2}(A_{t,k}g-b_{t,k})\|_2^2,
\]

\[
  N_{t,k}\partial_i g_{t,k}
  =
  (\partial_iA_{t,k})^\top W_{t,k}(b_{t,k}-A_{t,k}g_{t,k})
  +
  A_{t,k}^\top W_{t,k}
  (\partial_i b_{t,k}-(\partial_iA_{t,k})g_{t,k}),
\]

where \(N_{t,k}=A_{t,k}^\top W_{t,k}A_{t,k}\), assuming fixed \(W_{t,k}\).

Mass-matrix contraction derivative:

\[
R_{t,D}=1,\qquad
R_{t,k-1}
=
\sum_{a,b}M_k[a,b]C_{t,k,a}R_{t,k}C_{t,k,b}^\top,
\]

\[
\partial_iR_{t,k-1}
=
\sum_{a,b}M_k[a,b]\{
(\partial_iC_{t,k,a})R_{t,k}C_{t,k,b}^\top
+C_{t,k,a}(\partial_iR_{t,k})C_{t,k,b}^\top
+C_{t,k,a}R_{t,k}(\partial_iC_{t,k,b})^\top
\}.
\]

Proof obligations:

- Chain rule for \(\log\widehat Z_t-c_t\).
- Square derivative for \(\phi_t^2\).
- Product rule through TT cores.
- Differentiated contraction equals the integral derivative under fixed basis.
- Core equations give implementable sensitivities.
- Previous-filter derivative enters \(q_t\), so the proof is recursive, not
  time-local.

## MathDevMCP Protocol

Use MathDevMCP only for narrow obligations:

- \(\partial(\log Z-c)=\dot Z/Z-\dot c\).
- \(\dot(q/Z)=(\dot qZ-q\dot Z)/Z^2\).
- Product rule for finite products in scalar notation.
- Differentiated fixed linear system \(Ag=b\).
- Differentiated least-squares normal equations in scalar/matrix-symbolic form
  where feasible.
- Sparse or TT contraction product-rule identities if representable.

Record statuses:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Do not claim broad machine certification of Zhao-Cui, SIRT, TT-cross, or the
full adaptive code.

## Claude Review Loop

Claude Code is a bounded hostile reviewer only.  Codex remains final authority.

Plan review command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p12-zhao-cui-tt-proof-expansion-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p12-zhao-cui-tt-proof-expansion-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile mathematical exposition/proof review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.  If Claude rejects and Codex
agrees, patch and resubmit.  Loop to convergence or max five iterations.  Stop
for major proof, source-support, readability, same-scalar, or LaTeX blockers.
On iteration five, accept only if remaining issues are minor editorial/layout
issues.

Plan review criteria:

- Does the plan force a self-contained exposition before proofs?
- Does it distinguish Zhao-Cui adaptive code from BayesFilter fixed-branch
  variant?
- Are Proposition 1 and Proposition 2 stated with enough assumptions to be
  provable?
- Are proof obligations explicit enough for a skeptical mixed numerical panel?
- Are source-support, claim-support, coverage/omission, and
  quarantine/version checks required with a scoped rationale?
- Are MathDevMCP obligations narrow and honest?
- Are overclaims excluded?

Execution review criteria:

- Could a reader with probability and numerical linear algebra follow the
  Zhao-Cui algorithm without prior TT filtering background?
- Are all equations derived, not merely asserted?
- Are claims in proposition-proof form where needed?
- Does Proposition 1 prove normalized approximate filtering and avoid exact
  posterior overclaim?
- Does Proposition 2 prove a same-scalar gradient and include previous-filter
  recursion?
- Are adaptive branch limitations mathematically clear?
- Are source and code anchors exact?
- Are tables/checklists secondary to exposition?

## Execution Steps For A Future Codex Pass

1. Inspect:
   - P11 derivative note and ledgers;
   - P10 paper-code crosswalk and code audit ledgers;
   - Zhao-Cui local PDF and source anchors;
   - companion code paths for normalizer and scalar;
   - scholarly audit policy and Claude review template.

2. Run the skeptical plan audit in this file.  Patch this plan before
   execution if the audit reveals missing assumptions, wrong scalar, or
   unsupported source claims.

3. Launch Claude plan review.  Record `ACCEPT` or `REJECT` in the P12 Claude
   review ledger.

4. Create the P12 expanded LaTeX note by using the P11 note as a starting point
   but changing the structure to the required self-contained proof exposition.

5. Build the P12 source-anchor ledger, mapping each Zhao-Cui or Cui-Dolgov
   claim to inspected technical sections/equations/algorithms and each
   implementation claim to code paths.

6. Build the P12 source-support ledger:
   - record local PDF/code paths;
   - record public JMLR/Springer or equivalent source status checks when
     available;
   - record retraction/quarantine/version-conflict status;
   - list inspected technical anchors;
   - list allowed and forbidden claims.

7. Build the P12 claim-support ledger:
   - map each important claim in the note to checked source support, project
     derivation, implementation evidence, or source gap;
   - separate what the paper states from what the P12 note derives.

8. Build the P12 coverage-and-omission ledger:
   - state that this is a scoped proof expansion, not a broad survey;
   - record backward-snowball status from Zhao-Cui/Cui-Dolgov for the directly
     relevant TT/KR/filtering sources;
   - record forward-snowball or metadata lookup status if network access is
     available;
   - classify obvious omitted direct/foundational papers and explain why the
     omission does not block these two propositions.

9. Build the P12 proposition-proof ledger:
   - list each proposition/corollary;
   - list assumptions;
   - list proof obligations;
   - mark whether each is proved in the note, audited by MathDevMCP, or
     human-reviewed only.

10. Run MathDevMCP on the narrow identities.  Patch the note if MathDevMCP
   reveals an algebraic error.  Record inconclusive/tool-limit cases honestly.

11. Compile the note:

```text
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex
```

12. Launch Claude execution review.  Patch and rerun up to five iterations.

13. Validate:

```text
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-*
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.pdf - | rg -n "State-Space Filtering From First Principles|Zhao-Cui Sequential Squared-TT Algorithm|Fixed-Branch TT Filtering Variant|Proposition 1|Proposition 2|Same-Scalar|What Is Not Proved"
```

14. Clean LaTeX auxiliary files:

```text
latexmk -cd -c docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex
```

15. Write the P12 result file with:
   - what was inspected;
   - Claude `ACCEPT`/`REJECT` history;
   - MathDevMCP statuses;
   - source-support, claim-support, and coverage/omission status;
   - source anchors used;
   - proof summary for Proposition 1;
   - proof summary for Proposition 2;
   - LaTeX build status;
   - validation commands;
   - remaining proof/readability/implementation gaps;
   - what is not concluded.

## Stop Conditions

Stop and ask for direction, or record a structured blocker, if:

- the local Zhao-Cui PDF or code anchors are unavailable;
- a core equation cannot be tied to source or project derivation;
- the fixed branch cannot be stated without hiding adaptive choices;
- Proposition 1 cannot be proved without assuming the conclusion;
- Proposition 2 cannot be proved for the declared scalar;
- Claude identifies a major proof or source-support blocker that Codex agrees
  with and cannot patch in scope;
- MathDevMCP exposes a real algebraic contradiction;
- LaTeX fails to compile after focused repair.

## Final Response Requirements For Execution

The final response for the future execution pass must include:

- what Codex inspected;
- plan and execution summary;
- Claude `ACCEPT`/`REJECT` history;
- MathDevMCP audit status;
- files changed;
- self-contained Zhao-Cui exposition summary;
- fixed-branch variant summary and why it is needed;
- Proposition 1 statement/proof summary;
- Proposition 2 statement/proof summary;
- source anchors used;
- LaTeX/PDF build status;
- validation commands run;
- residual proof, readability, and implementation gaps;
- what is not concluded.

Decision:

`PLAN_READY_FOR_CLAUDE_REVIEW_AND_EXECUTION`
