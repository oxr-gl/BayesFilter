# P26 Zhao--Cui Panel-Readable Implementation Completion Plan

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P25 Zhao--Cui chair and implementation bridge note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.
- No claim that a real chemistry chair or implementation engineer has endorsed
  the note.

## Goal

Create a P26 version of the P25 note that addresses the remaining
chemist-facing and implementation-facing gaps while preserving P25's expanded
mathematical substance.  P26 must be more readable for a skeptical former
chemistry academic chair and more directly usable as a mathematical
implementation specification, without turning into software governance prose.

## Inputs

- Source note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.tex`
- Source PDF:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.pdf`
- Local Zhao--Cui PDF when needed:
  `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf`
- Prior P24/P25 ledgers and review notes under `docs/plans/`.

## Allowed Writes

- New P26 files under `docs/plans/`.
- Compiled P26 PDF beside the P26 note.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.tex`
- compiled PDF beside it
- `...p26-zhao-cui-panel-readable-implementation-plan-2026-06-03.md`
- `...p26-zhao-cui-chemist-gap-ledger-2026-06-03.md`
- `...p26-zhao-cui-implementation-gap-ledger-2026-06-03.md`
- `...p26-zhao-cui-human-facing-cleanup-ledger-2026-06-03.md`
- `...p26-zhao-cui-claude-review-ledger-2026-06-03.md`
- `...p26-zhao-cui-discrepancy-report-2026-06-03.md`
- `...p26-zhao-cui-panel-readable-implementation-result-2026-06-03.md`

Every markdown artifact must contain `metadata_date`, `seed_papers`, and
`what_is_not_concluded`.

## Skeptical Pre-Audit

Before execution, confirm:

- P26 preserves P25 and expands it; it must not summarize or remove P25's
  mathematical spine.
- The work is a readability and mathematical-specification pass, not a claim of
  exact posterior accuracy, adaptive differentiability, production readiness,
  or empirical validation.
- Claude review is a hostile review input, not final authority.
- A full-file Claude review may stall; if so, use bounded excerpt review and
  clearly record that limitation.
- The main note must avoid process/governance language.

Hard stop conditions before final acceptance:

- P26 must pass a section-preservation checklist against P25.  A longer line
  count is necessary but not sufficient: no P25 theorem statement, proof
  obligation, derivative equation group, implementation bridge, caveat, or
  finite-difference diagnostic may be removed or weakened without an explicit
  recorded reason.
- No final result artifact may claim success unless the PDF builds, the LaTeX
  log has no undefined references/citations or rerun blockers, the numbered
  equation audit passes, and the allowed-file whitelist passes.
- Every Claude finding classified by Codex as `ACCEPT` or `PARTIAL` must be
  patched before final acceptance, or reclassified with written justification.
- Claude worker reviews must be run in the trusted/elevated context required by
  repository policy.  Non-trusted hangs, auth failures, or network failures are
  sandbox evidence only and cannot close the review gate.
- If full-file Claude execution review stalls, bounded excerpt review must cover
  at least the KR teach-back, derivative-story page, boxed end-to-end algorithm,
  alternating sweep protocol, retained-filter storage recipe, default
  stabilization table, and finite-difference table.
- Take pre/post `git status --short` snapshots.  Fail final acceptance if any
  newly modified tracked file outside the P26 whitelist appears.

## Required P26 Changes

### Chemist-Facing Expansions

1. Add a teach-back subsection before or within the KR map material explaining
   why conditional/Knothe--Rosenblatt maps are the right transport device:
   conditional density, cumulative probability, inverse conditional CDF,
   triangular ordering, and why this converts density approximation into
   sampling/proposal construction.

2. Add a vivid moderate-rank example tied to a physical/high-dimensional
   setting: local sensors or local interactions on a spatial chain/grid.  Show
   mathematically how nearby interactions cross few coordinate splits, while a
   global constraint can force rank growth.

3. Add a one-page "story of the derivative" immediately before Proposition 2:
   what the forward pass computes, what is held fixed, what is recomputed, what
   the derivative follows through, and why the proposition is narrower than the
   adaptive Zhao--Cui algorithm.

4. Expand the sequential numerical trace so it shows more than one isolated
   value: time 1 fit, retained filter, time 2 target use of the retained filter,
   normalizer update, and derivative/finite-difference comparison.

### Implementation-Facing Expansions

5. Add one boxed end-to-end mathematical algorithm for the fixed-branch filter
   and derivative together.  It must include inputs, frozen branch fields,
   differentiable fields, forward outputs, derivative outputs, invariants, and
   failure exits.

6. Expand the alternating sweep protocol: exactly when \(L_{j,k}\), \(R_{j,k}\),
   \(A_k\), \(N_k\), and \(d_k\) are recomputed after a core update during
   left-to-right and right-to-left sweeps.

7. Add a retained-filter storage recipe for multi-dimensional \(z_t\) when the
   full product-basis matrix is too large.  Include full matrix storage,
   compressed TT/low-rank storage, evaluator contract, derivative evaluator
   contract, and failure diagnostics.

8. Replace purely symbolic stabilization choices with a minimal default table
   for \(\lambda_t\), \(\tau_t\), \(c_t\), \(\epsilon_{\rm floor}\),
   \(\epsilon_{\rm root}\), ridge, condition threshold, and residual tolerances.
   State that these are defaults for reproducibility, not theorem constants.

9. Add a finite-difference table with plausible/synthetic values for
   \(h,D(h),G,|D(h)-G|\), and interpret what decreasing error means and does
   not mean.

### Human-Facing Cleanup

10. Rename artificial or process-sounding sections:
    - `Saved Branch Manifest Schema` -> `What Must Be Held Fixed For The Derivative`.
    - `Reader Orientation Blocks For The Fixed-Branch Derivation` ->
      `Four Checklists For Reading The Derivative`.
    - `Notes On Scope And Source Use` -> `Relation To Zhao And Cui`.
    - Ensure no visible `P25 lane`, `ledger`, `artifact`, `governance`, or
      similar process language remains in the main note.

11. Maintain visible equation numbering for labeled displays.  No labeled
    equation may remain inside an unnumbered `\[...\]` block.

## Claude Review Protocol

Run a plan review before substantive edits and an execution review after
drafting.

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p26-zhao-cui-panel-readable-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p26-zhao-cui-panel-readable-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Claude execution review must include two personas:

- hostile former chemistry academic chair;
- implementation engineer focused on mathematical explanation.

Codex must independently classify each Claude finding as `ACCEPT`, `PARTIAL`,
`DISPUTE`, or `CLARIFY`.  Accepted or partially accepted findings must be
patched.  Disputed findings must receive a concise rebuttal in the review
ledger.  If full-file review stalls, use bounded excerpt review and record the
limitation.

## Validation

- Build P26 PDF with `latexmk`.
- Run `git diff --check` for P26 files.
- Scan the LaTeX log for undefined references, citation warnings, rerun
  blockers, or missing files.
- Use `pdftotext` to verify the P26 PDF contains the new sections and contains
  no visible process/governance terms.
- Verify no labeled equation is inside an unnumbered display.
- Verify P26 line count is not smaller than P25.
- Verify only allowed P26 files changed, aside from pre-existing unrelated dirty
  files.
- Verify the P25 preservation checklist is complete.

## Final Response Requirements

Report:

- files created;
- what was added for the chemist;
- what was added for implementation;
- Claude plan and execution review status;
- Codex audit classifications;
- PDF build status;
- validation commands;
- remaining gaps and caveats.
