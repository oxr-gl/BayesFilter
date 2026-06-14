# P24 Zhao--Cui Human-Facing Companion Plan

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing, 2011.
- P23 Zhao--Cui chemist and implementation gap-closure note.

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

Create P24 as the human-facing scholarly companion derived from P23.  P23 is
the audit/specification artifact.  P24 is the panel-facing note.

P24 must preserve and expand the mathematical content needed for a skeptical
chair, numerical reviewer, and implementation engineer, but it must remove the
visible governance/process language that makes P23 look like an internal
agent artifact.

The P24 note should read like a 60--80 page expository technical note, not a
review-loop ledger.  It must not summarize P23 down.  It must rewrite,
expand, and organize the material for human readers.

## Skeptical Pre-Execution Audit

Decision: `PLAN_DRAFT_AUDIT_PASS_WITH_CONTROLS`.

| Risk | Control |
|---|---|
| P24 becomes a shorter summary and loses P23 mathematical content. | Use P23 as the source spine, keep or expand all substantive derivations, require P24 TeX line count and PDF page count to be no shorter than P23 unless a specific removed-governance table is counted and justified. |
| P24 still looks like an internal governance artifact. | Ban visible governance/process language from the main note and move audit controls to ledgers only. |
| P24 keeps strange displayed audit tags. | Replace displayed tags such as `P23-E1`, `P22-C1`, `P19-90` with normal LaTeX equation numbering and ordinary `\label{...}` labels not shown in the PDF. |
| Citation prose remains informal. | Require all scholarly source references to use `\cite{...}`.  The text may say "Zhao and Cui" only as ordinary prose, but every source-supported claim must include `\cite{zhao2024ttsequential}` or the relevant key. |
| Chair gaps remain underexplained. | Add dedicated mathematical sections for TT-rank plausibility, coordinate-system map, and adaptive-versus-fixed-branch gradient scope. |
| Implementation gaps remain scattered. | Add an end-to-end boxed algorithm, explicit derivative-through-sweep equations, rank ladder, default numerical table, and a two-time-step numeric trace. |
| P24 becomes polished but source provenance is not auditable. | Maintain separate scholarly-audit ledgers for source support, citation/venue metadata, backward snowballing, forward snowballing, claim support, and omitted-paper risk.  Keep these ledgers outside the main note. |
| P24 overclaims method readiness. | Preserve caveats in human language: approximate filtering, fixed-branch derivative only, no adaptive global smoothness, no production/empirical claim. |

## Evidence Contract

Question:

Can P24 turn P23 into a proper human-facing scholarly note with normal citation
practice, normal equation numbering, and enough expanded mathematics to satisfy
the chair and implementation-engineer gaps identified after P23?

Baseline:

- P23 note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.tex`
- P23 PDF:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.pdf`
- P23 size: 5966 TeX lines and 67 PDF pages.

Primary pass criteria:

- P24 PDF builds.
- P24 main note contains no visible governance/process language.
- P24 uses normal equation numbering and hidden `\label{...}` references; no
  displayed audit tags such as `P23-*`, `P22-*`, `P20-*`, or `P19-*`.
- P24 uses `\cite{...}` for every scholarly source reference.
- P24 includes a bibliography using `docs/references.bib` or an explicit
  local bibliography compatible with the existing repo style.
- P24 does not summarize away P23 mathematics; it preserves or expands the
  substantive Zhao--Cui reconstruction, fixed-branch recursion, and gradient
  derivation.
- P24 directly addresses the three chair gaps and five implementation gaps
  listed below.
- P24 is backed by complete scholarly-audit ledgers for source support,
  citation/venue metadata, backward snowballing, forward snowballing,
  claim support, and omitted-paper/reviewer risk.
- Claude plan review and execution review accept after Codex-supervisor audit.

Veto diagnostics:

- Any visible phrase in the main P24 note such as "governance", "artifact",
  "ledger", "allowed writes", "Claude", "Codex", "P23", "P22", "P21",
  "P20", "DPF lane", "student-baseline", "controlled-DPF", "public API",
  "review loop", "execution review", or "source coverage summary".
- Any displayed equation tag of the form `P23-*`, `P22-*`, `P21-*`, `P20-*`,
  `P19-*`, or similar audit numbering.
- Any informal scholarly source reference not accompanied by `\cite{...}`.
- Any source-supported claim about Zhao and Cui, tensor trains, squared TT, KR
  maps, or TT decomposition without a citation or project derivation.
- P24 is substantially shorter than P23 in a way that indicates summary rather
  than cleanup.
- P24 omits any of the three chair-gap sections or five implementation-gap
  sections.
- Any supporting source lacks recorded local/full-text status,
  publication/version status, retraction/quarantine/erratum check, or a
  recorded blocker.
- Any major mathematical, algorithmic, or literature claim lacks a claim-support
  ledger entry mapping it to an exact source anchor or an explicit P24
  derivation.
- The backward-snowball, forward-snowball, or omitted-paper-risk ledgers are
  missing, empty without justification, or do not record a blocker when metadata
  access is unavailable.
- P24 claims exact posterior accuracy, global differentiability of adaptive
  branches, HMC convergence, production readiness, empirical validation, or
  default-method readiness.
- P24 edits chapters, production code, DPF lane, student-baseline,
  controlled-DPF, public APIs, P20/P21/P22/P23 artifacts, or unrelated dirty
  files.

Explanatory diagnostics:

- Page count is a guardrail, not proof of readability.
- Claude's chair persona is a proxy, not real panel endorsement.
- P24 remains a mathematical and algorithmic exposition, not executable code.

## Allowed Writes

Allowed:

- New P24 files under `docs/plans/`.
- P24 compiled PDF beside the note.
- P24 LaTeX build byproducts beside the note.
- If and only if necessary for correct `\cite{...}` use, a narrow addition to
  `docs/references.bib` for a missing source key.  Existing discovered keys
  include `zhao2024ttsequential`, `cui2021deep`, `oseledets2011tt`, and
  `rosenblatt1952remarks`.

Not allowed:

- Do not edit P20, P21, P22, or P23 artifacts.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not create executable Python, MATLAB, Octave, Julia, shell, TensorFlow,
  JAX, or production code.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-plan-2026-06-02.md`
- `...p24-zhao-cui-human-facing-companion-note-2026-06-02.tex`
- compiled PDF beside the note
- `...p24-zhao-cui-human-facing-companion-result-2026-06-02.md`
- `...p24-zhao-cui-human-facing-cleanup-ledger-2026-06-02.md`
- `...p24-zhao-cui-chair-gap-ledger-2026-06-02.md`
- `...p24-zhao-cui-implementation-gap-ledger-2026-06-02.md`
- `...p24-zhao-cui-citation-ledger-2026-06-02.md`
- `...p24-zhao-cui-source-support-ledger-2026-06-02.md`
- `...p24-zhao-cui-citation-venue-metadata-ledger-2026-06-02.md`
- `...p24-zhao-cui-backward-snowball-ledger-2026-06-02.md`
- `...p24-zhao-cui-forward-snowball-ledger-2026-06-02.md`
- `...p24-zhao-cui-claim-support-ledger-2026-06-02.md`
- `...p24-zhao-cui-omitted-paper-risk-ledger-2026-06-02.md`
- `...p24-zhao-cui-claude-review-ledger-2026-06-02.md`
- `...p24-zhao-cui-discrepancy-report-2026-06-02.md`

Every markdown artifact must contain:

- `metadata_date`
- `seed_papers`
- `what_is_not_concluded`

## Human-Facing Rewrite Requirements

The main P24 note must:

- remove visible governance/process paragraphs from P23;
- remove or rewrite the P23 opening equations `P22-C1`--`P23-C3`;
- remove the "Source Coverage Summary" section from the main note and place
  any needed source accounting in ledgers;
- replace displayed audit tags with normal equation numbers;
- use normal scholarly section titles;
- use `\cite{...}` consistently;
- include a proper bibliography;
- avoid phrases that make the note look like an AI-agent control document;
- preserve mathematical caveats in reader-facing language.

The main P24 note must not contain visible:

- `P23-`, `P22-`, `P21-`, `P20-`, `P19-` equation tags;
- "Codex", "Claude", "ledger", "artifact", "allowed writes",
  "governance", "execution review", "review loop", "source coverage
  summary", "DPF lane", "student-baseline", "controlled-DPF",
  "public-API edit", "Python", "MATLAB", "Octave", "Julia", or "shell"
  when used as process/no-edit text.

Technical mentions of implementation languages are not needed in the main
note and should be omitted.

The main P24 note must also avoid patronizing instructional cues.  Do not use
phrases such as "for beginners", "just", "simply", "obviously", "it is easy
to see", or "the reader only needs" as substitutes for derivation.  When a
concept is hard, write the equations first, then give a respectful explanation
of what the equations mean.

## Citation Requirements

Always use `\cite{...}`.

Required citation keys already present in `docs/references.bib`:

- Zhao and Cui 2024: `\cite{zhao2024ttsequential}`;
- Cui and Dolgov arXiv entry: `\cite{cui2021deep}`;
- Oseledets TT decomposition: `\cite{oseledets2011tt}`;
- Rosenblatt transformation: `\cite{rosenblatt1952remarks}`.

If P24 needs a different bibliographic entry, add it narrowly to
`docs/references.bib` and record the addition in the citation ledger.

Every major source-grounded claim must be either:

- cited with `\cite{...}`;
- tied to a derivation in P24;
- or clearly labeled as a BayesFilter fixed-branch extension.

Generic citations are not enough for technical claims.  Every major claim must
also appear in the claim-support ledger with an exact technical anchor such as
source section, equation, theorem, proof, algorithm, appendix, table, or a
P24 derivation label.

## Scholarly-Audit Provenance Requirements

P24 is a human-facing note, but its scholarly provenance must be auditable in
separate ledgers.  The main note must not expose these controls to the chair.

Required source-support ledger fields for every supporting paper:

- title, authors, year, DOI/arXiv/URL when known;
- bibliography key used in P24;
- local artifact path or source-blocked status;
- publication status;
- full-text status;
- inspected technical sections, equations, propositions, algorithms,
  appendices, or experiments;
- retraction, withdrawal, expression-of-concern, erratum, and quarantine
  status;
- version-consistency status between local PDF/arXiv/published record when
  applicable;
- claims allowed from this source;
- claims not allowed from this source.

Required citation/venue metadata ledger fields:

- citation count when metadata access is available;
- citation-count source and access date;
- venue or publication outlet;
- venue metadata source and access date when used;
- caveat that citation and venue metadata are coverage signals only, not
  correctness evidence;
- blocker entry when metadata access is unavailable.

Required backward-snowball ledger fields:

- seed paper;
- inspected related-work, introduction, method-comparison, or literature-survey
  anchor;
- relevant referenced work;
- classification: foundational, direct method, competitor, survey/tutorial,
  implementation/software, empirical example, background, peripheral,
  superseded, source-blocked, or quarantined;
- action: cite, inspect next, omit with reason, quarantine, or block pending
  source.

Required forward-snowball ledger fields:

- seed paper;
- metadata source and access date, or explicit metadata-access blocker;
- highly cited citing works when available;
- recent citing works when available;
- known follow-up, correction, replication, or negative-result papers when
  found;
- action and omission rationale.

Required claim-support ledger fields:

- P24 section/equation/algorithm/proposition;
- claim text;
- support class: `PRIMARY_TECHNICAL_SUPPORT`, `PROJECT_DERIVATION`,
  `IMPLEMENTATION_EVIDENCE`, `SURVEY_CONTEXT_ONLY`,
  `SOURCE_GAP_BLOCKER`, or `QUARANTINED`;
- exact source anchor or P24 derivation label;
- what the source explicitly states;
- what P24 derives or infers;
- forbidden overclaim.

Required omitted-paper/reviewer-risk ledger fields:

- plausible omitted paper or topic;
- why a skeptical panel might ask about it;
- source status;
- omission reason;
- risk level;
- next action or reason no action is needed for P24.

## Chair Gap Closure Requirements

P24 must add or substantially rewrite sections that address the three chair
gaps.

### Chair Gap 1: Why Moderate TT Rank Is Plausible

Do not stop at storage counts.  Include:

- an explanation of separability, local dependence, and coordinate ordering;
- matrix SVD rank analogy, then TT split-rank generalization;
- examples of low-rank structure in filtering targets;
- examples of high-rank failure modes;
- how preconditioning reduces rank pressure;
- diagnostics: fitted rank, residual, condition number, bridge ratio, and
  failure thresholds;
- a clear statement that moderate rank is an empirical/structural hypothesis,
  not a theorem for arbitrary nonlinear posteriors.

### Chair Gap 2: Coordinate-System Map

Add a dedicated section and diagram-equation chain for:

- physical coordinates \(r\);
- reference coordinates \(z\);
- preconditioned coordinates \(u\);
- retained coordinates \(z_t\);
- maps \(\Psi\), \(T\), \(T^{-1}\), and retained projection;
- where densities transform and where Jacobians enter;
- which coordinate system is used by fitting, KR maps, retained filters, and
  derivative checks;
- a small table: symbol, space, dimension, density, stored object, failure
  mode.

### Chair Gap 3: Why Fixed-Branch Gradient Is Useful But Narrow

Add a plain but mathematical section explaining:

- the full adaptive algorithm chooses ranks, pivots, points, domains,
  preconditioners, shifts, and stopping times;
- those choices define a branch \(B\);
- the fixed-branch scalar \(\widehat\ell_T(\beta;B)\) is differentiable under
  stated conditions;
- this derivative is useful for local diagnostics, finite-difference checks,
  and possible HMC on a declared approximation;
- it is deliberately not the derivative of the globally adaptive algorithm;
- what would be required to study adaptive derivatives separately.

## Implementation Gap Closure Requirements

P24 must add or substantially rewrite sections that address the five
implementation gaps.

### Implementation Gap 1: End-To-End Boxed Algorithm

Include one boxed algorithm for the fixed-branch squared-TT filter with:

- inputs;
- outputs;
- saved branch fields;
- invariants;
- failure exits;
- initialization;
- target evaluation;
- square-root fit;
- mass contraction;
- retained filter construction;
- optional KR map construction;
- derivative pass;
- finite-difference check.

This is not executable code.  It is a mathematical algorithm written in
pseudocode/prose equations.

### Implementation Gap 2: Derivative Through Sweep Environments

Place explicit derivative equations beside the sweep protocol:

- \(\dot y_j\);
- \(\dot H_k^{(j)}\);
- \(\dot L_{j,k}\);
- \(\dot R_{j,k}\);
- \(\dot A_k[j,:]\);
- \(\dot N_k\);
- \(\dot d_k\);
- solve equation for \(\dot g_k\);
- how updates propagate during forward and backward sweeps;
- conditioning caveat.

### Implementation Gap 3: Deterministic Rank Ladder

Add a deterministic rank ladder protocol:

- rank candidates \(R\in\mathcal R\);
- fixed points/domains for all candidate ranks;
- residual and conditioning pass criteria;
- defensive mass and floor-fraction vetoes;
- rule for choosing the smallest acceptable rank;
- rule for declaring branch failure rather than silently adapting during
  differentiation;
- how the chosen rank is frozen in finite-difference checks.

### Implementation Gap 4: Minimal Default Stabilization Table

Add a table with reproducibility defaults and caveats for:

- \(\epsilon_{\rm floor}\);
- \(\epsilon_{\rm ridge}\);
- \(\delta_\tau\);
- \(\delta_{\rm floor}\);
- \(\gamma\);
- \(N_{\rm fit}\);
- \(S_{\max}\);
- \(\varepsilon_{\rm rel}\);
- \(\varepsilon_{\rm abs}\);
- \(\varepsilon_{\rm root}\);
- \(N_{\rm root}\);
- bridge diagnostic threshold.

Defaults must be labeled as first-pass reproducibility choices, not validated
production recommendations.

### Implementation Gap 5: Two-Time-Step Numerical Trace

Add a small numerical trace for the running example.  It must include actual
numbers for a simple two-step scalar model, such as:

- chosen \(\beta,\sigma,r,\mu_0,\sigma_0,y_1,y_2\);
- domain intervals and reference map;
- a tiny basis/rank choice, e.g. \(p=2\), \(R=1\), explained as pedagogical;
- a few fitting points;
- target values \(q_1\);
- shifted square-root values \(y_j\);
- a simple constant or rank-one fitted core illustration;
- approximate \(\widehat Z_1\), retained filter idea, and \(q_2\) formation;
- one derivative term \(\partial_\beta q_t\) and a finite-difference check
  formula.

The numerical trace may be hand-computable and low accuracy; it is for
orientation, not validation.

## Execution Plan

1. Inspect P23 note/result/ledgers and the existing bibliography keys.
2. Inspect the P23/P18/P17 scholarly-audit ledgers and the local Zhao--Cui PDF
   anchors.  Reuse verified provenance where still valid, but do not silently
   inherit unsupported claims.
3. Run Claude hostile plan review.  Patch accepted or partially accepted
   findings before drafting.
4. Build P24 TeX from P23 as source material, not by editing P23.
5. Remove visible governance/process text from the main P24 note.
6. Convert displayed audit equation tags into normal equation numbering and
   hidden labels.
7. Add `natbib`/bibliography support compatible with `docs/references.bib`,
   and replace informal source references with `\cite{...}`.
8. Create or update the six scholarly-audit ledgers before finalizing
   technical claims: source support, citation/venue metadata, backward
   snowball, forward snowball, claim support, and omitted-paper risk.  Record
   blockers instead of inventing unavailable metadata.
9. Add the three chair-gap sections.
10. Add the five implementation-gap sections.
11. Create ledgers for human-facing cleanup, chair gaps, implementation gaps,
   citations, Claude review, discrepancy report, and result.
12. Build the P24 PDF and validate.
13. Run Claude hostile execution review with chair, numerical reviewer,
    implementation engineer, and scholarly citation reviewer personas.
14. Patch accepted or partially accepted findings and rerun review until
    accepted or blocked.

## Claude Review Protocol

Claude Code is a bounded hostile reviewer only.  Codex remains supervisor and
final authority.

Run Claude worker commands with elevated/trusted permissions.

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p24-zhao-cui-human-facing-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p24-zhao-cui-human-facing-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Maximum iterations:

- Plan review: 5.
- Execution review: 8.

Claude execution review must include:

1. former chemistry academic chair;
2. numerical computation professor;
3. implementation engineer focused on mathematical implementability;
4. scholarly citation/style reviewer.

Claude must reject if:

- the main note still visibly contains governance/process language;
- source references do not use `\cite{...}`;
- displayed audit equation tags remain;
- P24 summarizes away P23 mathematics rather than rewriting/expanding it;
- any chair or implementation gap remains materially unaddressed;
- any required scholarly-audit ledger is missing, empty without justification,
  or lacks required source-status, claim-anchor, snowballing, metadata, or
  omission-risk fields;
- major technical claims lack exact source anchors or explicit P24 derivations;
- supporting sources lack retraction/quarantine/erratum/version checks or
  recorded blockers;
- overclaims appear;
- executable code is created.

## Codex-Supervisor Audit Protocol

After each Claude review round, Codex must independently audit Claude's
findings before patching or accepting them.

For every Claude finding, classify it as:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a different or narrower patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken
  the document.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

If Codex accepts or partially accepts a finding, patch the relevant files and
record the exact control added.  If Codex disputes a finding, record a concise
rebuttal with file/section evidence and include it in the next Claude prompt.

If any material Claude finding remains `ACCEPT`, `PARTIAL`, or unresolved
`CLARIFY` at the iteration cap, the P24 result must be marked
`BLOCKED_REJECTED`, not accepted.  If Codex and Claude still disagree on a
material `DISPUTE` at the cap, record the disagreement in the discrepancy
report and block downstream acceptance unless the human explicitly decides.

## Validation Requirements

- Build the P24 PDF with `latexmk`.
- Run `git diff --check` on P24 files and any narrow bibliography edit.
- Scan the LaTeX log for errors, undefined references, undefined citations,
  rerun blockers, missing files, and serious overfull boxes.
- Confirm bibliography/citation resolution.
- Confirm the PDF text contains no banned governance/process terms.
- Confirm the TeX contains no displayed audit tags of the form `P23-*`,
  `P22-*`, `P21-*`, `P20-*`, or `P19-*`.
- Confirm every scholarly source reference in the main note uses `\cite{...}`.
- Confirm P24 contains the three chair-gap sections and five
  implementation-gap sections.
- Confirm all six scholarly-audit ledgers exist and contain required
  provenance fields.
- Confirm every major P24 claim maps to an exact source anchor or explicit P24
  derivation in the claim-support ledger.
- Confirm source-support ledger records local/full-text status, inspected
  technical anchors, publication/version status, and
  retraction/quarantine/erratum checks or blockers for each supporting paper.
- Confirm backward-snowball, forward-snowball, and omitted-paper-risk ledgers
  contain actioned entries or explicit blockers.
- Confirm every markdown artifact contains required metadata fields.
- Confirm only allowed P24 files changed, plus any explicitly justified
  bibliography edit.

## Final Response Requirements

Final response must include:

- what Codex inspected;
- Claude plan review history;
- Claude execution review history;
- Codex audit classifications summary;
- files changed;
- citation/bibliography status;
- PDF build status;
- validation commands run;
- remaining human-facing readability gaps;
- remaining implementation-math gaps;
- final probability estimate that P24 passes a skeptical mixed
  chemistry/numerical/implementation panel.
