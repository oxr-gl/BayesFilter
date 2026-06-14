# P23 Zhao--Cui Chemist And Implementation Gap-Closure Plan

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P22 integrated readable companion and fixed-branch gradient note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross, rank selection,
  pivot selection, changing domains, changing shifts, changing fitting points,
  or changing preconditioners.
- No HMC convergence claim.
- No production BayesFilter implementation claim.
- No empirical validation on BayesFilter target models.
- No default-method recommendation.
- No executable prototype claim.

## Purpose

Create P23 as a gap-closure companion built by copying P22 as the spine and
adding the eleven gap closures identified by Codex after reading P22 as a
former chemistry academic and as an implementation engineer.

P23 must not replace, summarize, shorten, or remove P22.  The P22 document is
the inherited mathematical spine.  P23 adds:

1. a threaded one-dimensional nonlinear example;
2. a worked two-dimensional KR map example;
3. a before/after preconditioning flattening derivation;
4. an equation dependency diagram for Proposition 2;
5. a rank-count plausibility comparison;
6. a complete fixed-branch TT fitting sweep protocol;
7. an explicit domain-selection policy;
8. stabilization defaults for \(\tau_t,\lambda_t,c_t\), floors, and ridge;
9. operational KR map construction details;
10. a multidimensional retained-filter storage/evaluation contract;
11. a saved branch-manifest schema.

## Skeptical Pre-Execution Audit

Decision: `PLAN_DRAFT_AUDIT_PASS_WITH_CONTROLS`.

| Risk | Control |
|---|---|
| P23 accidentally becomes a shorter summary of P22. | Start by copying P22 to the P23 TeX path.  P23 must be longer than P22 in TeX line count and not shorter in PDF page count. |
| Additions are appended as disconnected notes. | Insert gap closures where the relevant P22 topic appears and add a gap ledger mapping each addition to exact P23 anchors. |
| The chemist-facing material becomes condescending prose. | Use math-first examples and derivations, then explanatory prose.  Avoid teach-back and audience-assessment language. |
| Implementation detail becomes executable code. | Write mathematical protocols, tables, schemas, and object-flow equations only.  Do not create `.py`, `.m`, `.jl`, shell, or production files. |
| The gradient extension is overclaimed. | Preserve P22 non-claims and explicitly state that the fixed-branch derivative differentiates only the declared saved-branch scalar. |
| Defaults are arbitrary and could be mistaken for validated production settings. | Label stabilization/domain/ridge policies as minimal deterministic defaults for reproducibility, with diagnostics and failure conditions. |
| Claude review rubber-stamps the plan. | Require hostile plan and execution reviews.  Codex must classify every Claude finding before patching or accepting. |

## Evidence Contract

Question:

Can P23 close the eleven chemist-reader and implementation-engineer gaps in
P22 while preserving P22's mathematical spine and non-executable document
scope?

Baseline:

- P22 integrated readable companion: 4815 TeX lines and 55 PDF pages.
- P22 TeX path:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.tex`.
- P22 PDF path:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.pdf`.

Primary pass criteria:

- P23 PDF builds.
- P23 is longer than P22 in TeX line count and not shorter in PDF page count.
- P23 contains exact anchors for all eleven gap closures.
- P23 threads the one-dimensional nonlinear example through multiple sections,
  not only at the end.
- P23 includes a worked two-dimensional KR conditional-CDF example.
- P23 includes a before/after preconditioning flattening derivation.
- P23 includes an equation dependency diagram for Proposition 2.
- P23 includes a full-grid versus TT rank-count comparison.
- P23 includes a deterministic fixed-branch TT sweep protocol.
- P23 includes explicit domain-selection, stabilization, KR construction,
  multidimensional retained-filter, and branch-manifest contracts.
- P23 includes a P22-preservation ledger keyed to inherited P22 section and
  equation anchors.
- Claude plan review and execution review accept after Codex-supervisor audit.

Veto diagnostics:

- Any of the eleven gap closures is absent or vague.
- P23 compresses, deletes, or summarizes away P22 content.
- P23 replaces inherited P22 derivation text by shorter cross-references such
  as "see P22" or "as above" instead of preserving the copied derivation.
- P23 is shorter than P22 by TeX line count or PDF page count.
- P23 adds executable code.
- P23 claims exact posterior accuracy, global differentiability of adaptive
  branches, HMC convergence, production readiness, or empirical validation.
- Claude raises a substantive veto finding that Codex accepts and does not
  patch.

Explanatory diagnostics:

- Page count is a guardrail, not proof of understanding.
- Claude's chemistry-chair persona is a proxy, not a guarantee of real panel
  endorsement.
- P23 remains a mathematical document and implementation specification, not a
  runnable implementation.

## Allowed Writes

Allowed:

- New P23 files under `docs/plans/`.
- P23 compiled PDF beside the P23 TeX note.

Not allowed:

- Do not edit P20, P21, or P22 artifacts.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not create executable Python, MATLAB, Octave, Julia, shell, TensorFlow,
  JAX, or production code.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-plan-2026-06-02.md`
- `...p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.tex`
- compiled PDF beside the note
- `...p23-zhao-cui-eleven-gap-ledger-2026-06-02.md`
- `...p23-zhao-cui-p22-preservation-ledger-2026-06-02.md`
- `...p23-zhao-cui-claude-review-ledger-2026-06-02.md`
- `...p23-zhao-cui-discrepancy-report-2026-06-02.md`
- `...p23-zhao-cui-chemist-implementation-gap-closure-result-2026-06-02.md`

Every markdown artifact must contain:

- `metadata_date`
- `seed_papers`
- `what_is_not_concluded`

## Execution Plan

1. Inspect P22 note, P22 integration ledger, P22 implementation-specification
   ledger, P22 review ledger, and P22 result.
2. Run Claude hostile plan review.  Patch accepted or partially accepted plan
   findings before drafting.
3. Copy P22 TeX to the P23 TeX path as the base spine.
4. Patch title, abstract, and opening contract to state that P23 closes the
   eleven P22 gaps without replacing P22.
5. Add a threaded one-dimensional nonlinear example near the beginning, with
   anchors reused later in filtering, squared-TT, preconditioning, and gradient
   sections.
6. Add a rank-count plausibility section near the TT introduction.
7. Add a complete deterministic sweep protocol after the least-squares core
   fitting equations.
8. Add explicit domain-selection and stabilization-default sections in the
   fixed-branch implementation lane.
9. Add a worked two-dimensional KR map example after the general KR formulas.
10. Add operational KR CDF/inversion construction details after the map
    contracts.
11. Add a before/after preconditioning flattening derivation in the
    preconditioning section.
12. Add a multidimensional retained-filter storage/evaluation contract after
    the one-coordinate carried-filter contract.
13. Add a saved branch-manifest schema before the finite-difference diagnostic.
14. Add an equation dependency diagram before Proposition 2.
15. Create ledgers recording all eleven gap closures, Claude review history,
    P22 preservation, discrepancies, and result.
16. Build PDF and validate.
17. Run Claude hostile execution review.  Patch accepted or partially accepted
    findings and rerun until accepted or blocked.

## Required P23 Gap Anchors

The P23 note must include exact anchors for:

- `P23-E*`: threaded nonlinear example;
- `P23-RANK*`: full grid versus TT rank-count comparison;
- `P23-SWEEP*`: fixed-branch TT sweep protocol;
- `P23-DOM*`: domain-selection policy;
- `P23-STAB*`: stabilization defaults;
- `P23-KR2*`: two-dimensional KR example;
- `P23-KROPS*`: operational KR construction details;
- `P23-PREC*`: preconditioning flattening derivation;
- `P23-MD*`: multidimensional retained-filter contract;
- `P23-MAN*`: branch-manifest schema;
- `P23-GDAG*`: Proposition 2 dependency diagram.

The eleven-gap ledger must cite these anchors exactly.

## Required P22 Preservation Ledger

The P23 preservation ledger must contain exact inherited P22 anchors for:

1. opening reader contract and non-summary rule;
2. notation and five-object orientation;
3. Zhao--Cui Section 1 reconstruction;
4. Zhao--Cui Section 2 TT representation, basis, marginalization, and
   Algorithm 1;
5. Zhao--Cui Section 3 squared-TT, defensive density, mass matrices, KR maps,
   Algorithm 2, particle correction, and smoothing;
6. Zhao--Cui Section 5 preconditioning and Algorithm 5 dataflow;
7. transition from Zhao--Cui annotation to fixed-branch extension;
8. fixed-branch object/data structure section;
9. fixed-branch recursion and Proposition 1;
10. fixed-branch gradient expansion and Proposition 2;
11. finite-difference diagnostic and minimal mathematical example;
12. inherited non-claims and integrated conclusion.

For every required inherited P22 block row, record:

- P22 source section/equation anchor;
- P23 destination section/equation anchor;
- status: `copied_verbatim` or `extended_in_place`;
- whether inherited text was shortened;
- whether any derivation was replaced by a shorter cross-reference;
- exact P23 gap additions inserted nearby, if any;
- failure flag.

Validation fails if any inherited P22 block has a failure flag, if any
inherited substantive text or derivation is replaced by a shorter
cross-reference, or if any modified inherited section lacks a preservation
row.  Cross-reference-only entries are allowed only for auxiliary navigational
notes outside the required inherited block rows; they cannot count as
preservation evidence.

## Minimum Content Contract For The Eleven Closures

Each closure must satisfy the minimum content below.

| Gap | Anchor family | Minimum required payload |
|---|---|---|
| Threaded nonlinear example | `P23-E*` | Model equations; exact transition/observation densities; time-1 target; squared-TT target; preconditioned residual; gradient scalar; recurrence table showing appearances in filtering, squared-TT, preconditioning, and gradient sections. |
| Worked 2D KR example | `P23-KR2*` | Joint density, two marginals, two conditional densities, two CDFs, triangular map, Jacobian determinant, inverse sampling equations, monotonicity and endpoint diagnostics. |
| Preconditioning flattening derivation | `P23-PREC*` | Before target \(q\), bridge \(\rho\), ratio \(q/\rho\), transformed residual, rank-pressure explanation, failure case when \(\rho\) is too small. |
| Proposition 2 dependency diagram | `P23-GDAG*` | Equation chain from target values to least-squares solve, cores, mass contraction, normalizer, carried filter, next target, and log-likelihood derivative. |
| Rank-count plausibility | `P23-RANK*` | Full-grid \(p^D\) count, TT \(O(DpR^2)\) storage/evaluation count, contraction cost \(O(DpR^3)\), and explicit statement that small stable \(R\) is empirical. |
| TT sweep protocol | `P23-SWEEP*` | Initialization, left/right sweep order, environment update, ridge solve, residual calculation, optional rescaling, stopping rule, rank-fixed failure recovery. |
| Domain selection | `P23-DOM*` | At least prior/transition scale, pilot particles or moments, tail-mass target, expansion factor, out-of-domain diagnostic, and branch-freezing rule. |
| Stabilization defaults | `P23-STAB*` | Rules for \(\lambda_t,\tau_t,c_t,\varepsilon_{\rm floor},\rho\), units/scale interpretation, and threshold diagnostics. |
| KR operations | `P23-KROPS*` | CDF representation, quadrature/integration rule, clipping, monotonic projection or rejection, inverse bisection/Newton fallback, endpoint checks. |
| Multidimensional retained filter | `P23-MD*` | Matrix/tensor storage for retained block with dimension \(m>1\), basis product features, coefficient tensor shape, evaluator, derivative evaluator, next-step query rule. |
| Branch manifest | `P23-MAN*` | Frozen fields, differentiable fields, manifest equality rule, hash/identity fields as mathematical labels, and finite-difference branch comparison rule. |

## Required Non-Gap Control Anchors

The P23 ledgers must cite exact anchors for:

- inherited non-claims;
- opening "P23 does not replace P22" contract;
- no-executable-code scope statement;
- allowed-writes boundary;
- P22-preservation ledger rows;
- P22/P23 count validation table.

## Claude Review Protocol

Claude Code is a bounded hostile reviewer only.  Codex remains supervisor and
final authority.

Both plan-review and execution-review Claude worker commands must be run with
elevated/trusted permissions, following repository cross-agent policy.

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p23-zhao-cui-gap-closure-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p23-zhao-cui-gap-closure-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Maximum iterations:

- Plan review: 5.
- Execution review: 8.

Claude execution review must include:

1. former chemistry academic chair;
2. numerical computation professor;
3. implementation engineer;
4. hostile mathematical reviewer.

Claude must reject if:

- any of the eleven gaps is not materially addressed;
- P23 compresses or removes P22 content;
- P23 is shorter than P22;
- the running example is not threaded through multiple sections;
- KR maps lack a worked two-dimensional example;
- preconditioning lacks the before/after flattening derivation;
- Proposition 2 lacks a dependency diagram;
- rank plausibility lacks \(p^D\) versus \(O(DpR^2)\);
- TT fitting protocol remains underspecified;
- domain, stabilization, KR, multidimensional retained-filter, or branch
  manifest specifications remain vague;
- overclaims appear;
- executable code is created.
- inherited P22 derivations are replaced by shorter cross-references.
- exact non-gap control anchors are missing.

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

Any Claude finding alleging one of the following remains a veto blocker unless
Codex provides a cited file/anchor rebuttal and Claude withdraws or narrows the
finding on rereview:

- P22 compression, removal, or substitution by shorter cross-reference;
- missing or vague eleven-gap closure;
- overclaiming;
- forbidden executable, chapter, production, DPF, student-baseline, or
  controlled-DPF edits.

If any material Claude finding remains `ACCEPT`, `PARTIAL`, or unresolved
`CLARIFY` at the iteration cap, the P23 result must be marked
`BLOCKED_REJECTED`, not accepted.  If Codex and Claude still disagree on a
material `DISPUTE` at the cap, record the disagreement in the discrepancy
report and block downstream acceptance unless the human explicitly decides.

## Validation Requirements

- Build the P23 PDF with `latexmk`.
- Run `git diff --check` on P23 files.
- Scan LaTeX log for errors, undefined references, citation warnings, rerun
  blockers, missing files, and serious overfull boxes.
- Record P22 and P23 TeX line counts and PDF page counts.  Fail if P23 is
  shorter than P22 by TeX line count or PDF page count.
- Record the count validation table with:
  `artifact path | method used | P22 lines/pages | P23 lines/pages | pass/fail`.
  This failure is non-waivable.
- Confirm every required P23 gap anchor appears in the TeX and PDF text.
- Confirm the threaded nonlinear example recurrence table lists exact section
  anchors for filtering, squared-TT, preconditioning, and gradient reuse.
- Confirm the P22-preservation ledger has no failure flags and no shorter
  cross-reference replacements.
- Confirm non-gap control anchors are present in the TeX and ledgers.
- Confirm every markdown artifact contains required metadata fields.
- Confirm only allowed P23 files changed.

## Final Response Requirements

Final response must include:

- what Codex inspected;
- P22 gaps addressed;
- Claude plan review history;
- Claude execution review history;
- Codex audit classifications summary;
- files changed;
- PDF build status;
- validation commands run;
- remaining chemist-reader gaps;
- remaining implementation-engineer gaps;
- final probability estimate that P23 passes a skeptical mixed
  chemistry/numerical/implementation panel.
