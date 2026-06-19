# P65 Phase 1 Subplan: One-Factor Rank/Capacity Diagnostic

metadata_date: 2026-06-14
status: DRAFT_FOR_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p65-fixed-branch-rank-capacity-master-program-2026-06-14.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded for material findings

## Phase Objective

Determine why the high-rank fixed branch in the P60 d=18 comparator has zero
fitted square-root mass under the tiny P64 baseline, varying only one factor at a
time and preserving the P63 source-pushed `computeL` fit-data route.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result passed.
- Fresh P64 baseline still reproduces high defensive-only steps `(1, 2)`.
- Fresh P64 baseline still reports high fitted square-root masses `(0.0, 0.0)`.
- Master program and runbook have accepted review.
- No implementation repair has been made yet in P65.

## Required Artifacts

- This subplan, refreshed after Phase 0.
- Diagnostic implementation or script, if needed, under the existing P65 lane.
- Phase result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase1-rank-capacity-diagnostic-result-2026-06-14.md`.
- Updated Phase 2 subplan if a bounded repair is identified.
- Diagnostic outputs embedded in the Phase 1 result; no separate long-running
  sweep artifact is required unless a focused script is introduced.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which single factor first prevents high-rank defensive-only collapse: fit sample count, retained sample count, bounded-domain clipping/support, degree/rank tuple, ridge, or deterministic resampling degeneracy? |
| Baseline/comparator | Phase 0 reproduced P64 baseline row: `sample_count=1`, `fit_sample_count=2`, low `(degree=0, rank=1)`, high `(degree=1, rank=2)`, status `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE`, high defensive-only steps `(1, 2)`, high fitted square-root masses `(0.0, 0.0)`. |
| Primary diagnostic criterion | A one-factor diagnostic identifies either a minimal source-preserving setting with high nonzero square-root mass at both steps or a narrower blocker explaining why no tested single factor resolves collapse. |
| Veto diagnostics | Mixed-factor change presented as cause; artificial reference-grid fit data; target/order/axis changes; defensive `tau` removal; threshold weakening; hidden adaptive reselection; nonfinite density or normalizer. |
| Explanatory diagnostics | `sqrt_square_normalizer`, mixture normalizer, local clipping fraction, local max absolute before clip, target value min/max, ESS, correction-weight range, log-marginal delta, normalizer increment delta. |
| Not concluded | No bug fix, no promotion of new defaults, no d=18 correctness, no rank convergence theorem. |

## Planned One-Factor Ladder

Run the smallest rows first and stop once a discriminating artifact exists.
Execute rows through a small local Python diagnostic that records every row as
`executed`, `infeasible`, or `error`.  A row is evidentiary only when it is
`executed` and preserves the source-pushed fit-data route, target order,
previous-marginal axes, defensive convention, and P60 thresholds.

Candidate row families:

1. Baseline confirmation:
   - `(sample_count=1, fit_sample_count=2)`.
2. Fit-data capacity only:
   - hold retained `sample_count=1`;
   - vary `fit_sample_count` through `3`, `4`, then `6`;
   - stop this family early if one row clears high defensive-only collapse at
     both steps.
3. Retained sample count only:
   - before running retained-count rows, determine the admissible sample-count
     domain from the local API contract;
   - rows are admissible only when changing `sample_count` does not also change
     the source-pushed fit-data route, target order, previous-marginal axes, or
     defensive convention;
   - infeasible rows must be logged as infeasible and do not count as evidence
     for or against retained sample count;
   - admissible retained-count rows may vary `sample_count` through `2`, then
     `3`;
   - stop retained-count testing if the API contract or first attempted row
     shows retained count cannot be varied without changing another factor.
4. Degree/rank tuple only:
   - hold counts fixed;
   - compare high degree/rank variants `(degree=0, rank=2)` and
     `(degree=1, rank=3)` only if fit-data capacity rows do not already produce
     a bounded repair hypothesis.
5. Ridge only:
   - hold counts and rank fixed;
   - test at most two ridge rows only if recorded diagnostics indicate solve
     degeneracy rather than sample-capacity collapse.
6. Support/clipping only:
   - do not change source-pushed fit data;
   - record clipping diagnostics first;
   - patch support radius only in Phase 2 if Phase 1 proves clipping is the
     blocker and source classification is reviewed.

## Phase 1 Skeptical Audit Before Execution

Status: PASSED_FOR_REVIEW_ONLY.

The planned diagnostic preserves the P64 baseline and changes only one declared
factor per row.  Nonzero high fitted square-root mass is diagnostic evidence, not
a bug-fix claim; the P60 same-route gate and veto diagnostics remain decisive.
The ladder has stop rules and separates infeasible rows from negative evidence.
The main residual risk is that row execution could be slow; the plan therefore
starts with the smallest fit-data-capacity rows and stops on the first
discriminating artifact.

## Required Checks/Tests/Reviews

- Compile any diagnostic code touched.
- Run focused diagnostic rows CPU-only.
- If a code patch is needed only to expose diagnostic data, run focused P60 tests.
- Bounded Claude review is required before executing Phase 1 because the phase
  chooses the repair search boundary after Phase 0.
- Claude review is also required if Phase 1 proposes a Phase 2 repair;
  otherwise a result-only review is optional unless the interpretation is
  ambiguous.

## Forbidden Claims/Actions

- Do not change production comparator behavior in Phase 1 unless the subplan is
  amended and reviewed.
- Do not treat nonzero high square-root mass alone as a bug fix.
- Do not use artificial reference-grid fit data.
- Do not weaken thresholds.
- Do not claim source-faithful repair unless paper/source anchors are recorded.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if Phase 1 identifies a bounded, source-preserving repair
target with:

- exact changed factor;
- why it resolves or may resolve high defensive-only collapse;
- required implementation surface;
- expected tests;
- forbidden side effects.

If no bounded repair is identified, write a blocker result and stop or ask for
human direction.

Infeasible ladder rows are not failures and not negative evidence.  They are
admissibility findings only, and the Phase 1 result must separate infeasible
rows from rows that were executed and interpreted.

## Stop Conditions

- Single-factor ladder becomes too expensive for visible execution.
- Any row requires a scope change not in this subplan.
- Diagnostic result is inconclusive and cannot be narrowed without broad sweeps.
- Claude and Codex do not converge after five review rounds for the same
  interpretation blocker.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 1 result or blocker.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
