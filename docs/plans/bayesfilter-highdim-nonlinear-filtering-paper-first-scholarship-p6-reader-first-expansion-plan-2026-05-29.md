# P6 Reader-First Pedagogical Expansion Plan

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U/P2R/P3/P4/P5 high-dimensional nonlinear
filtering artifacts, `ch33`--`ch37`, `docs/references.bib`, `docs/main.tex`,
`docs/main.log`, `docs/main.pdf`, and the scholarly literature audit policy.

what_is_not_concluded: This plan does not conclude production readiness, NAWM
readiness, posterior accuracy, HMC convergence, tensor-method validation,
transport-method validation, GPU/XLA readiness, default readiness,
machine-certified proof validity, or exhaustive literature coverage.

## Skeptical Plan Audit

The P5 block is mathematically stronger, but the user correctly identifies a
different failure mode: it is still too compact to teach.  A mixed numerical
panel may reject the block not because a derivation is absent, but because the
reader cannot keep track of the object being approximated, where the
approximation enters, or how the synthesis consumes the earlier chapters.

The wrong P6 response would be to add a new broad orientation chapter or to add
more literature.  Earlier chapters already cover the broad introduction, and
P1--P5 already handle source discipline.  The right P6 response is a
reader-first expansion inside the existing chapters: one running example,
repeatable section rhythm, proposition pedagogy, short reader checkpoints,
export-to-synthesis rows, and clarifying tables.

The plan passes the skeptical audit if:

- the baseline is the current P5 chapter block;
- the primary criterion is readability and teachability, not new novelty;
- no new source-dependent theorem claim is introduced without existing checked
  support;
- every new proposition wrapper, table entry, or synthesis sentence restates a
  claim already mapped to `PRIMARY_TECHNICAL_SUPPORT`, `PROJECT_DERIVATION`, or
  an explicit source-gap/nonclaim status in existing P1--P5 ledgers;
- running examples are explicitly non-validating pedagogical cells;
- Claude review focuses on whether mixed numerical professors can follow the
  material;
- PDF validation confirms the new P6 material is rendered.

## Evidence Contract

Question: Can `ch33`--`ch37` be made linearly readable for a mixed numerical
review panel by adding a running example, proposition pedagogy, reader
checkpoints, export-to-synthesis tables, and clarifying object tables, without
adding a new orientation chapter or weakening source discipline?

Baseline: the current P5 state of `ch33`--`ch37` and P5 result/ledgers.

Primary pass criterion:

- each chapter uses the scalar nonlinear running example or explicitly connects
  to it;
- key propositions have a plain-English/object/assumption/derivation/failure/
  industrial-meaning wrapper where needed;
- method sections separate object, exact target, approximation, algorithm,
  derivation, failure, mitigation, and industrial role;
- reader checkpoints are pedagogical and short;
- `ch37` explicitly consumes exported defects, diagnostics, cost variables, and
  promotion gates from `ch33`--`ch36`;
- rendered PDF contains P6 markers.

Veto diagnostics:

- a major readability defect remains after review;
- the running example is inconsistent across chapters;
- a checkpoint becomes internal audit clutter rather than reader help;
- new source-dependent claims rely on abstracts, metadata, venue rank,
  citation count, blocked originals, or quarantined sources;
- a retained or newly reused source becomes `RETRACTED_OR_QUARANTINED` or has
  an unresolved version conflict under the scholarly audit policy;
- new text claims NAWM readiness, production readiness, posterior accuracy,
  HMC convergence, tensor validation, transport validation, GPU/XLA readiness,
  or default readiness;
- LaTeX build fails or new undefined citations/references appear.

Explanatory diagnostics:

- MathDevMCP checks for narrow new algebra when feasible;
- PDF layout warnings;
- Claude minor editorial suggestions.

Artifact preserving the result:

- this plan;
- P6 reader-first, running-example, checkpoint, MathDevMCP, Claude, and result
  ledgers;
- rebuilt `docs/main.pdf`.

## Allowed Writes

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/main.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p6-*`

Forbidden writes: broad orientation chapters, DPF implementation lane files,
student-baseline files, controlled-DPF files, production `bayesfilter/` code,
public APIs, `.local_sources/` commits, `docs/references.bib` unless explicitly
needed and source-checked, and unrelated dirty files.

Minimum completion set:

- updated `ch33`--`ch37`;
- P6 plan, reader-first ledger, running-example ledger, checkpoint ledger,
  MathDevMCP ledger, Claude review ledger, and result note;
- successfully rebuilt `docs/main.pdf`.

## Stop Conditions

Stop as `BLOCKED` if:

- the chapters cannot build;
- a needed new technical claim requires unavailable primary technical support;
- a reused source supporting a retained claim becomes quarantined, retracted, or
  version-conflicted under the scholarly literature audit policy;
- Claude finds a major readability or overclaim defect unresolved after five
  iterations;
- the running example introduces a mathematical inconsistency that cannot be
  repaired in scope.
- reader checkpoints cannot be kept to short teaching aids without breaking
  the mathematical flow.

Stop as `PARTIAL_READY_WITH_BLOCKERS` if:

- readability improves but the block remains too compact for a non-filtering
  numerical reader;
- only layout warnings remain after successful build;
- broad propositions remain human-reviewed and not machine-certified.

## Running Example Design

The running scalar cell is
\[
  x_t=\rho x_{t-1}+\eta_t,\qquad
  \eta_t\sim\calN(0,Q),\qquad
  y_t=x_t^2+\epsilon_t,\qquad
  \epsilon_t\sim\calN(0,R).
\]

It is used only as a pedagogical cell.  It is not NAWM validation, production
evidence, or posterior-accuracy evidence.
It cannot validate multimodality severity, transport behavior, tensor
tractability, HMC behavior, or industrial adequacy in the macro-finance stress
cell except by analogy.

Use it to teach:

- `ch33`: conditioning, normalizer, likelihood, bimodality, and score target;
- `ch34`: why a Gaussian moment projection can miss two posterior lobes;
- `ch35`: how sharp likelihoods cause particle weight concentration and why
  transports require correction/support;
- `ch36`: how HMC needs the scalar likelihood or declared approximate scalar
  and its gradient;
- `ch37`: how the scalar cell expands into the macro-finance stress cell.

## Proposition-Expansion Template

For prioritized propositions, add a compact wrapper:

- plain-English claim;
- object being approximated or preserved;
- assumptions;
- derivation step;
- approximation step if any;
- failure if assumptions break;
- industrial interpretation.

Priorities:

- `prop:bf-hd-likelihood-sensitivity`;
- `prop:bf-hd-affine-projection`;
- `prop:bf-hd-exactness-not-accuracy`;
- `prop:bf-hd-pf-collapse`;
- `prop:bf-hd-transport-correction`;
- `prop:bf-hd-factor-gate`;
- `prop:bf-hd-hmc-gradient-contract`;
- `prop:bf-hd-same-scalar`;
- `prop:bf-hd-particle-collapse-calculus`;
- `prop:bf-hd-local-cubature-diagnostic`;
- `prop:bf-hd-tensor-viability`;
- `prop:bf-hd-transport-auditability`;
- `prop:bf-hd-hmc-downstream`;
- `prop:bf-hd-sparse-grid-promotion`;
- `prop:bf-hd-performance-after-veto`;
- `prop:bf-hd-block-scaffold-first`;
- `prop:bf-hd-useful-not-novel`.

Any displayed proposition or theorem-like claim reused by a later chapter must
receive the wrapper or be explicitly recorded as already sufficiently
pedagogical.

## Reader-Checkpoint Template

Use short pedagogical checkpoints after major sections.  Preferred wording:

- "Reader checkpoint."
- "What should now be clear: ..."
- "Object preserved: ..."
- "Approximation enters at: ..."
- "Exported to synthesis: ..."

These are teaching aids, not evidence boxes.  They should be short enough not
to interrupt the mathematical flow.

Checkpoint limit: at most one compact checkpoint per major section unless
Claude or Codex identifies a specific readability gap.  If the checkpoint
language begins to read like internal compliance or audit clutter, remove it or
move the content into normal prose.

## Export/Import Schema For Synthesis

Each of `ch33`--`ch36` must end with a compact export table using this schema:

| object | exact target | approximation site | failure mode | diagnostic/veto | cost variable | promotion gate | citation/derivation anchor |

`ch37` may import only these fields when claiming that the earlier chapters
export a defect, diagnostic, cost variable, or promotion gate.  `ch37` must not
invent a new cross-method promotion gate unless it is written as a new local
project derivation/nonclaim and recorded in the P6 ledger.

Decision/promotion boundary: `ch33`--`ch36` may describe mechanisms and local
failure/mitigation.  Cross-method promotion, ranking, default advice, or
architecture-level decision synthesis belongs in `ch37`.

## Chapter-By-Chapter Rewrite Scope

`ch33`:

- add the running example and object table;
- use the example to show why \(x^2\) observations can create two posterior
  lobes;
- add checkpoint after exact recursion and after likelihood-gradient
  derivation;
- add export-to-synthesis table.

`ch34`:

- reuse the running example to explain Gaussian projection failure;
- add a table distinguishing moment closure, quadrature, and posterior
  accuracy;
- add pedagogical wrapper for affine projection and exactness-not-accuracy;
- add export-to-synthesis table.

`ch35`:

- reuse the running example for particle collapse, transport correction, and
  tensor semantic checks;
- add a table separating empirical measure, proposal density, transport map,
  TT density, and TN covariance;
- add export-to-synthesis table.

`ch36`:

- reuse the running example to connect scalar likelihood, approximate scalar,
  analytical gradient, and HMC potential;
- add exact-gradient versus approximate-gradient table;
- add export-to-synthesis table.

`ch37`:

- add an imports-from-chapters table;
- explicitly connect the scalar running cell to the existing macro-finance
  stress cell;
- state that the scalar cell is conceptual only and cannot validate high-
  dimensional macro-finance severity or method behavior except by analogy;
- add a short reader checkpoint before the final synthesis algorithm.

## MathDevMCP Use Protocol

P6 is mostly pedagogical.  Use MathDevMCP only for new or materially changed
narrow algebra.  Record:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Do not claim broad machine certification.
MathDevMCP can audit derivation fragments only.  It cannot certify exposition
quality, literature coverage, reviewer readiness, source support, or
chapter-level correctness.

## Diagram/Table Scope

P6 should prefer compact LaTeX tables.  No new graphical diagrams are required.
Do not add decorative figures.  A diagram is allowed only if it encodes an
object-to-approximation-to-failure flow more clearly than a table and remains
inside the allowed write set.

## Claude Review Loop

Claude is read-only and hostile.  Codex remains supervisor and final authority.
Claude must output `ACCEPT` or `REJECT` first.  Loop up to five iterations per
plan or execution block.  Accept iteration five only if remaining issues are
minor editorial/layout issues.

Review criteria:

- mixed numerical professors can follow the chapter without already knowing
  nonlinear filtering jargon;
- running example is consistent and pedagogical;
- propositions are teachable rather than dense;
- survey, derivation, failure, mitigation, and industrial synthesis are
  separated;
- reader checkpoints help rather than clutter;
- `ch37` consumes exports from `ch33`--`ch36`;
- tables clarify rather than decorate;
- overclaims are absent and source blockers/quarantines are respected.

## PDF Validation

Run:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references|Rerun to get outlines" docs/main.log
pdftotext docs/main.pdf - | rg -n "Running quadratic-observation cell|Reader checkpoint|Exported to synthesis|P6|imports from the preceding chapters"
git diff --check
```

Record layout warnings separately from scholarly blockers.
