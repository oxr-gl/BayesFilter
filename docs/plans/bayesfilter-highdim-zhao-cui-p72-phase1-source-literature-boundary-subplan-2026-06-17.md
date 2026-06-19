# P72 Phase 1 Subplan: Source And Literature Boundary Audit

metadata_date: 2026-06-17
status: READY_FOR_PHASE1_EXECUTION_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Classify every proposed P72 repair operation before code is designed or
edited.  The phase must separate:

- operations that are `source_faithful` only when backed by checked Zhao--Cui
  paper anchors and local author-source file/line anchors;
- operations that are `fixed_hmc_adaptation` because they freeze an author
  route component to define a differentiable same scalar;
- operations that are `extension_or_invention` because they add finite
  support, stability, guard, or admission machinery not yet shown in the paper
  or author source.

The phase must also record which literature directions can support numerical
stability claims and which remain source gaps.  It does not implement the
repair and does not run repaired diagnostics.

## Entry Conditions Inherited From Phase 0

Phase 1 may begin only if all conditions hold:

- P70 Phase 6h result exists and remains the failed baseline:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-result-2026-06-17.md`;
- P72 repair note and PDF exist;
- Phase 0 result exists and states that no code or repaired diagnostic was
  launched;
- Phase 0 records MathDevMCP diagnostics as inconclusive/diagnostic-only, not
  as proofs;
- Claude review of the Phase 0 close record and this Phase 1 subplan returns
  `VERDICT: AGREE`, or all material findings have been patched within the
  five-round review limit;
- downstream validation and d18 validation remain blocked.

## Required Artifacts

Phase 1 must produce:

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md`;
- repair-operation classification ledger inside the Phase 1 result, with one
  row per proposed operation and one of the three allowed classifications;
- source-support and source-gap ledger for each claimed paper/source anchor;
- literature-support and literature-gap ledger for stable weighted least
  squares, Christoffel/leverage sampling, oversampling, conditioning, and
  polynomial/TT approximation stability candidates;
- omitted-paper/reviewer-risk notes when an important method family is left
  unaudited;
- updated P72 Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`;
- updated P72 execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`;
- refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-subplan-2026-06-17.md`.

Candidate local inputs to inspect include, at minimum:

- Zhao--Cui paper/source ledgers:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-*.md`,
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-*.md`,
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-*.md`;
- local author source:
  `third_party/audit/tensor-ssm-paper-demo`;
- current fixed-branch implementation surface candidates:
  `bayesfilter/highdim/source_route.py`,
  `bayesfilter/highdim/fitting.py`,
  `bayesfilter/highdim/squared_tt.py`;
- P72 repair note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-repair-note-2026-06-17.tex`;
- local bibliography:
  `docs/references.bib`.

Network/API metadata lookup is not required for Phase 1 unless separately
approved.  If citation counts, rankings, retraction checks, or forward
snowballing require unavailable network metadata, record the blocker instead
of inventing metadata.

## Required Checks, Tests, And Reviews

Local read-only checks before writing the Phase 1 result:

```bash
test -f docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-result-2026-06-17.md
test -d third_party/audit/tensor-ssm-paper-demo
rg -n "Zhao and Cui|Tensor-Train Methods for Sequential State and Parameter Learning|source_faithful|fixed_hmc_adaptation|extension_or_invention" docs/plans docs/chapters docs/references.bib bayesfilter/highdim third_party/audit/tensor-ssm-paper-demo
rg -n "Christoffel|leverage|weighted least squares|least-square|oversampling|condition" docs/plans docs/chapters docs/references.bib third_party/audit/tensor-ssm-paper-demo
```

Local checks after writing the Phase 1 result and Phase 2 subplan:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md
rg -n "source_faithful|fixed_hmc_adaptation|extension_or_invention|BLOCK_SOURCE_UNGROUNDED|not concluded|forbidden" docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-subplan-2026-06-17.md
```

Reviews:

- Codex skeptical plan audit before executing Phase 1.
- Claude read-only review of the Phase 1 result and refreshed Phase 2 subplan.
- If Claude returns `VERDICT: REVISE`, patch the same artifact visibly and
  rerun focused checks.  Stop after five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which P72 repair operations are source-faithful author-route behavior, which are fixed-HMC freezing adaptations, and which are our support/stability extensions? |
| Baseline/comparator | P72 repair note, P70 Phase 6h failure, BayesFilter Zhao-Cui source-governance gate, local Zhao--Cui paper ledgers, local author source, and local bibliography. |
| Primary criterion | Every proposed operation has exactly one classification with cited evidence or an explicit source gap; no source-faithfulness claim is emitted without both paper and local author-source anchors; the Phase 2 subplan consumes only the classified operations. |
| Veto diagnostics | Unsupported use of "faithful"; treating guard/stability additions as author behavior without anchors; using literature metadata or abstracts as theorem support; silently omitting relevant stable least-squares or TT/SIRT anchors; author-source paths not inspected; Phase 2 authorized to implement unclassified behavior. |
| Explanatory only | Candidate papers without checked technical anchors, citation/venue metadata if unavailable, source-code line searches that reveal possible but not yet interpreted anchors. |
| Not concluded | No implementation, no repaired diagnostic, no proof that guard additions are optimal, no continuum support certificate, no original Zhao--Cui failure claim, no adaptive parity, no d18 validation, no HMC readiness. |
| Artifact preserving result | Phase 1 result, review ledger, execution ledger, and refreshed Phase 2 subplan. |

## Required Classification Targets

The Phase 1 result must classify at least the following operations:

| Operation family | Default classification before audit | Required Phase 1 action |
| --- | --- | --- |
| Squared TT density, SIRT/KR transport role, defensive density, normalizer/marginalization route | `source_faithful` only if paper and author-source anchors are cited | Verify anchors or downgrade to source gap. |
| Freezing rank, basis, domain, samples, sweep schedule, branch identity, and beta branch | `fixed_hmc_adaptation` | Cite the author route being frozen and explain what is frozen for the same-scalar objective. |
| UKF-guided center/scale/orientation used as a branch-design scout | `fixed_hmc_adaptation` or source gap, never truth | Preserve "scout not oracle" boundary. |
| Guard cloud, audit cloud, collocation residuals, line probes, maximum residual gates, support-distance gates, normalizer admission gates | `extension_or_invention` | Decide whether useful for fixed-variant repair, but do not use to close a Zhao--Cui source-faithfulness gap. |
| Line-growth penalties, shape penalties, derivative-energy penalties | `extension_or_invention` | Require literature/project-derivation support before Phase 2 can include them. |
| Column scaling, stable least-squares solves, singular-value/effective-rank gates, conditioning veto | `extension_or_invention` unless author/source anchors are found | Tie to numerical-stability literature or record as project engineering guard. |
| Christoffel/leverage/oversampling/stable-sampling ideas | candidate support/source gap | Inspect technical anchors if used; otherwise preserve as deferred literature gap. |
| Rank-direction activity gates | `extension_or_invention` | Explain that they address fixed-variant inactive-direction hiding and are not author-route proof. |

## Forbidden Claims And Actions

- Do not edit production code.
- Do not run repaired diagnostics, Phase 7 validation, d18 validation, HMC, or
  GPU diagnostics.
- Do not use "source-faithful", "faithful", "paper-scale", or "adaptive
  parity" without paper and author-source file/line anchors.
- Do not treat the P72 repair note's MathDevMCP inconclusive diagnostics as
  proof.
- Do not cite abstracts, titles, citation counts, or venue rank as support for
  algorithmic or theorem-level claims.
- Do not claim the original Zhao--Cui adaptive method has the Phase 6h bug.
- Do not authorize Phase 2 to implement any operation not classified or
  explicitly recorded as a source/literature gap.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 result exists and includes the required classification ledger;
- all operations needed by Phase 2 are either classified with anchors or
  explicitly marked as `extension_or_invention` approved for design as a
  fixed-variant stabilization candidate;
- literature-support claims are tied to checked technical anchors, project
  derivations, or explicit source gaps;
- Phase 2 subplan exists and freezes the design-only boundary: guard cloud,
  audit cloud, line-probe observables, conditioning conventions, and thresholds
  can be designed, but implementation still waits for Phase 4;
- local checks pass;
- Claude returns `VERDICT: AGREE` for the Phase 1 result and Phase 2 subplan.

## Stop Conditions

Stop and write a blocker if:

- the Zhao--Cui paper/source anchors needed for any `source_faithful` claim
  cannot be located;
- local author source is unavailable or cannot be inspected;
- Phase 2 would require unclassified behavior;
- literature support would require network/API metadata or full text that is
  not locally available and not approved;
- Claude and Codex do not converge after five review rounds for the same
  blocker;
- the user redirects the lane.

## Skeptical Plan Audit

This phase is safe to execute after Phase 0 review because it is read-only
with respect to production code and diagnostic runs.  It addresses the main
planning risk left by the P72 repair note: confusing useful fixed-variant
stabilization additions with the original Zhao--Cui adaptive method.  The
phase also blocks a common proxy-metric mistake by requiring all Phase 2 gates
to be classified before any threshold or implementation design is allowed.
