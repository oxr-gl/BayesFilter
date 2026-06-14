# P22 Zhao--Cui Integrated Readable Companion Plan

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.
- P21 chair guide and implementation-ready mathematical specification.

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
- No executable prototype claim.

## Purpose

Create P22 as an integrated readable companion that uses P20 as the
mathematical spine and folds in the useful P21 readability and
implementation-specification material without the tone or structure of a
governance checklist.

The intended document is allowed to be long.  A 60--80 page PDF is acceptable
and preferred over a compressed summary.  The goal is a document that a
skeptical numerical panel and a former chemistry academic chair can read
without feeling talked down to, while still preserving enough equations and
implementation detail for a later minimal fixed-branch implementation phase.

Hard non-summarization rule:

- P22 must not summarize, remove, compress, or replace the P20 mathematical
  spine.  P20 remains the source-order companion.  P22 begins from P20 and adds
  readable expansion, orientation, shape contracts, and implementation meaning.

Tone rule:

- Avoid condescending teach-back phrasing such as "the chair should be able to
  say."  Replace it with neutral academic scaffolding:
  "what has been established," "stored object," "integrated object,"
  "differentiated object," "fixed branch object," "implementation meaning,"
  and "failure mode."

## Skeptical Pre-Execution Audit

Decision: `PLAN_DRAFT_AUDIT_PASS_WITH_CONTROLS`.

Main risks:

| Risk | Control |
|---|---|
| P22 becomes a shorter summary and loses P20 source detail. | Copy P20 as the spine and only add material; do not delete P20 mathematical blocks. |
| P21 readability material sounds condescending. | Rewrite P21 "chair" and "teach-back" blocks into neutral reader-orientation and implementation-meaning blocks. |
| The document becomes a duplicated appendix rather than an integrated companion. | Insert P21 material near the P20 blocks it explains: roadmap near introduction, ladder before gradient pass, carried-filter contract near carried filter, finite-difference report near finite differences. |
| The fixed-branch derivative is oversold as full adaptive Zhao--Cui. | Retain and strengthen disclaimers separating exact Zhao--Cui annotation, fixed-branch extension, and future implementation. |
| The future coder still lacks shapes and finite-difference protocol. | Preserve P21's \(Q_t,\dot Q_t,P_t,\dot P_t\) carried-filter contract, branch manifest, and finite-difference report schema. |
| Claude review becomes a rubber stamp. | Require plan review and execution review with explicit veto power for summarization, condescension, lost P20 content, missing implementation shapes, or overclaiming. |

Additional anti-summary control:

- P22 must maintain a P20 carry-forward map.  Every P20 source-order
  Zhao--Cui annotation block and every fixed-branch derivation block must map
  to a P22 destination.  The execution must fail if any required P20 block is
  omitted, reordered before the source-annotation boundary, or reduced to vague
  summary prose.

## Evidence Contract

Question:

Can P22 integrate P20 and P21 into a readable, mathematically detailed,
non-condescending companion that preserves the Zhao--Cui source-order
annotation and adds enough orientation and shape detail for later
fixed-branch implementation work?

Baseline:

- P20: 50-page integrated annotated companion with source-order Zhao--Cui
  reconstruction and fixed-branch gradients.
- P21: 17-page readability and implementation-ready specification supplement.

Primary pass criteria:

- P22 PDF builds.
- P22 is not shorter than P20 and is expected to be substantially longer.
- P22 preserves the P20 source-order annotation structure for Zhao--Cui
  Sections 1--3 and 5.
- P22 integrates P21 material where it helps the reader, rather than appending
  it as a governance checklist.
- P22 removes or rewrites condescending chair-checklist language.
- P22 includes neutral orientation blocks with equations:
  stored object, integrated object, differentiated object, frozen object,
  implementation meaning, and failure mode.
- P22 includes the P21 carried-filter representation contract:
  \(Q_t,\dot Q_t,P_t,\dot P_t\), query basis, evaluator outputs, and next-step
  query rule.
- P22 includes the P21 finite-difference report schema and pass/fail status.
- The implementation-specification ledger records field-level locations for
  the carried-filter representation contract and finite-difference report
  schema.
- P22 TeX line count and PDF page count are recorded beside P20's TeX line
  count and PDF page count, and P22 fails if it is shorter than P20.
- Claude plan and execution reviews accept after Codex-supervisor audit.

Veto diagnostics:

- P22 deletes, compresses, or summarizes away P20 source-order mathematical
  content.
- P22 contains condescending reader-assessment language as the dominant framing.
- P22 relegates P21 to an unrelated appendix without integration.
- P22 loses the carried-filter storage contract or finite-difference report
  schema.
- The P20 carry-forward map is incomplete or shows any P20 mathematical block
  reduced to a vague summary.
- P22 TeX line count or PDF page count is less than P20's.
- Any field-level carried-filter or finite-difference report-schema item is
  missing from the implementation-specification ledger.
- P22 claims exact posterior accuracy, global differentiability of adaptive
  branches, production implementation readiness, or HMC readiness.
- P22 creates executable code.
- Claude raises a substantive veto finding that Codex accepts and does not
  patch.

Explanatory diagnostics:

- Page count is an explanatory signal, not proof of readability.
- Claude's chemistry-chair persona is a proxy for the real panel chair, not a
  guarantee of endorsement.
- No empirical or finite-difference numerical result is produced.

## Allowed Writes

Allowed:

- New P22 files under `docs/plans/`.
- P22 compiled PDF beside the P22 TeX note.
- P22 plan, review ledger, integration ledger, readability ledger,
  implementation-specification ledger, discrepancy report, and result.

Not allowed:

- Do not edit P20 or P21 artifacts.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not create executable Python, MATLAB, Octave, TensorFlow, JAX, or
  production code.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-plan-2026-06-02.md`
- `...p22-zhao-cui-integrated-readable-companion-note-2026-06-02.tex`
- compiled PDF beside the note
- `...p22-zhao-cui-integration-ledger-2026-06-02.md`
- `...p22-zhao-cui-readable-orientation-ledger-2026-06-02.md`
- `...p22-zhao-cui-implementation-specification-ledger-2026-06-02.md`
- `...p22-zhao-cui-claude-review-ledger-2026-06-02.md`
- `...p22-zhao-cui-discrepancy-report-2026-06-02.md`
- `...p22-zhao-cui-integrated-readable-companion-result-2026-06-02.md`

Every markdown artifact must contain:

- `metadata_date`
- `seed_papers`
- `what_is_not_concluded`

## Execution Plan

1. Copy the P20 TeX note to the P22 TeX path as the base spine.
2. Patch the P22 title, abstract, and opening contract to say that P22 is an
   integrated readable companion derived from P20 plus P21.
3. Insert a neutral "Reader Orientation: Five Mathematical Objects" section
   after the introductory notation block, using P21's five-object roadmap but
   removing audience-assessment language.
4. Insert neutral orientation blocks after difficult P20 blocks:
   - Zhao--Cui filtering recursion;
   - squared-TT nonnegativity and mass;
   - marginalization and KR maps;
   - preconditioning;
   - fixed-branch data structures;
   - fixed-branch derivative pass;
   - propositions for normalized approximate filtering and same-scalar
     derivative.
5. Integrate P21's six derivative ladders into the fixed-branch gradient
   section before the dense derivative pass.  Rewrite labels as "Scalar
   warmup," "Two-coordinate form," "TT form," and "Filtering meaning."
6. Insert P21's carried one-coordinate representation contract near the
   carried-filter derivative section.
7. Insert P21's finite-difference report schema near P20's finite-difference
   protocol.
8. Replace condescending chair-checklist or audience-assessment language in the
   copied/added P22 text with neutral academic language.
9. Create ledgers recording:
   - where P20 content was preserved through a P20 carry-forward map;
   - where P21 content was integrated;
   - which orientation blocks were added;
   - which implementation-specification controls were added;
   - which claims remain not concluded.
10. Build PDF and validate.
11. Run Claude execution review.
12. Patch accepted Claude findings and rerun as needed until accepted or until
    review disagreement must be recorded.

## Required P20 Carry-Forward Map

The P22 integration ledger must contain a carry-forward table with, at
minimum, all of these P20 block families:

1. introductory notation, measures, and parameter/state distinction;
2. Zhao--Cui Section 1 model setup, joint density, evidence, posterior, and
   marginal tasks;
3. Zhao--Cui Section 2 recursive posterior update, tensor trains from first
   principles, basis expansion, marginalization, and Algorithm 1;
4. Zhao--Cui Section 3 squared-TT nonnegativity, shifted/defensive density,
   normalizer, mass matrices, marginalization, conditional/KR maps, Algorithm
   2, particle proposal/correction, backward smoothing, and Algorithm 4;
5. Zhao--Cui Section 5 preconditioning, bridging, pullback/pushforward
   identities, transformed normalizer, nonlinear preconditioning, Algorithm 5
   dataflow, and implementation signatures;
6. transition from Zhao--Cui annotation to BayesFilter fixed-branch extension;
7. implementable fixed-branch objects and data structures;
8. fixed-branch filtering recursion and normalized-approximate-filter proof;
9. fixed-branch gradient motivation, warmups, forward pass, derivative pass,
   proposition 1, proposition 2, finite-difference protocol, and limitations.

For every row, the ledger must record:

- P20 source line or section anchor;
- P22 destination line or section anchor;
- status: `preserved`, `preserved_and_expanded`, or `not_applicable_with_reason`;
- whether P21 material was inserted nearby;
- whether the block remains source-order or belongs after the fixed-branch
  boundary;
- failure flag if it was reduced to summary prose.

Validation fails if any required row is missing or if any failure flag is
raised.

## Required Field-Level Implementation Controls

The P22 implementation-specification ledger must record exact P22 anchors for
each item below.

Carried-filter representation contract:

- \(Q_t:(p,p)\);
- \(\dot Q_t:(p,p)\);
- \(P_t:(p,p)\);
- \(\dot P_t:(p,p)\);
- query basis \(B^{\rm query}:(M,p)\);
- evaluator outputs
  \(\widehat p_t^{\rm ref},\dot{\widehat p}_t^{\rm ref}:(M,)\);
- next-step query rule \(z^{\rm query}_j=Z_{\rm fit}[j,2]\).

Finite-difference report schema:

- declared scalar \(\widehat\ell_2(\beta_0;\mathcal M_0)\);
- analytical derivative \(G\);
- branch-manifest equality rule;
- recompute-core rule;
- step sizes;
- \(D(h)\), absolute error, and relative error;
- pass/fail criterion;
- expected decreasing-error trend;
- failure interpretations;
- what is not concluded.

## Claude Review Protocol

Claude Code is a bounded hostile reviewer only.  Codex remains supervisor and
final authority.

Both plan-review and execution-review Claude worker commands must be run with
elevated/trusted permissions, following the repository cross-agent execution
policy.  Non-elevated hangs, auth failures, network failures, or missing output
are sandbox evidence only and must not be treated as content vetoes until the
same review has been rerun in a trusted context.

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p22-zhao-cui-integrated-readable-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p22-zhao-cui-integrated-readable-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Maximum iterations:

- Plan review: 5.
- Execution review: 8.

Claude execution review must include:

1. former chemistry academic chair persona;
2. numerical computation professor;
3. implementation engineer;
4. hostile mathematical reviewer.

Claude must reject if:

- P22 is a summary rather than an expansion;
- P22 sounds condescending;
- P20 source-order content is lost;
- P21 implementation-critical shape/report controls are lost;
- overclaims appear;
- P22 is not buildable.

## Codex-Supervisor Audit Protocol

After each Claude review round, Codex must independently audit Claude's
findings before patching or accepting them.

For every Claude finding, Codex must classify it as:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a different or narrower patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken
  the document.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

If Codex accepts or partially accepts a finding, patch the relevant files and
record the exact control added.  If Codex disputes a finding, record a concise
rebuttal with file/section evidence and include it in the next Claude prompt.

## Validation Requirements

- Build the P22 PDF with `latexmk`.
- Run `git diff --check` on P22 files.
- Scan LaTeX log for errors, undefined references, citation warnings, rerun
  blockers, missing files, and serious overfull boxes.
- Record P20 and P22 TeX line counts and PDF page counts.  Fail if P22 is
  shorter than P20 by either measure.
- Confirm the P20 carry-forward map is complete and has no failure flags.
- Use `pdftotext` to confirm P22 contains:
  - Zhao--Cui annotation;
  - reader orientation;
  - fixed-branch recursion;
  - derivative ladders;
  - carried-filter representation contract;
  - finite-difference report schema;
  - what is not claimed.
- Confirm the implementation-specification ledger has field-level anchors for
  every carried-filter and finite-difference report-schema item listed above.
- Confirm all P22 markdown artifacts contain required metadata fields.
- Confirm no executable P22 code files exist.
- Confirm P20 and P21 artifacts were not edited.
- Confirm only allowed files changed intentionally.

## Final Response Requirements

The final response must include:

- what Codex inspected;
- Claude plan review history;
- Claude execution review history;
- Codex audit classification summary;
- P22 integration summary;
- readability/tone result;
- implementation-specification result;
- PDF build status and page count;
- validation commands run;
- files changed;
- residual risks;
- final probability estimate that P22 passes a skeptical mixed
  numerical/chemistry panel.
