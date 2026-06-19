# P65 Master Program: Fixed-Branch Rank/Capacity Repair And Bug Test

metadata_date: 2026-06-14
status: DRAFT_FOR_REVIEW
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded
predecessor_plan: docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-plan-2026-06-13.md
predecessor_result: docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-result-2026-06-14.md
chapter_anchor: docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex

## Objective

Implement and test a source-preserving fixed-branch rank/capacity repair for the
current P60 d=18 bug: the nominal high-rank candidate collapses to defensive-only
mass at both fitted steps.  The program tests whether a repaired fixed branch can
produce nonzero high-rank fitted square-root mass and pass the same-route
rank-comparator gates without changing the Zhao--Cui square-root-plus-defensive
density, the P63 source-pushed fit-data route, or the fixed-HMC differentiability
constraints.

## Current Baseline

P64 localized the bug:

- current comparator: `p60_author_sir_same_route_rank_comparator(sample_count=1,
  fit_sample_count=2, low_fit_degree=0, high_fit_degree=1, low_fit_rank=1,
  high_fit_rank=2)`;
- status: `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE`;
- blockers include `candidate_high_defensive_only_transport`;
- high candidate defensive-only steps are `(1, 2)`;
- high square-root fitted mass is zero at both steps;
- defensive `tau=1e-8` is source-consistent and must not be removed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can a source-preserving fixed-branch rank/capacity repair prevent high-rank defensive-only collapse in the P60 d=18 comparator while preserving the same target, source-derived fit data, shifted-density normalizer convention, and fixed-branch determinism? |
| Exact baseline/comparator | P64 current P60 comparator result in `docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-result-2026-06-14.md`; local API `bayesfilter.highdim.p60_author_sir_same_route_rank_comparator(...)`. |
| Primary pass criterion | A repaired comparator configuration or implementation path has no `candidate_high_defensive_only_transport`, high square-root fitted mass is nonzero at both steps, and the same-route P60 status passes without threshold weakening or target changes. |
| Veto diagnostics | Changed target/order/previous-marginal axes; artificial reference-grid fit data; removed or rescaled defensive `tau` outside the P50 shifted/original-scale derivation; weakened P60 thresholds; hidden adaptive reselection; nonfinite normalizers/densities; high branch still defensive-only; unsupported source-faithful claim. |
| Explanatory diagnostics | Fit sample count, retained sample count, local clipping fraction, local max absolute coordinate before clipping, target value range, ESS, correction-weight range, normalizer decomposition, log-marginal deltas, rank tuple, degree tuple, ridge. |
| Not concluded even on pass | No paper-scale spatial SIR success, no d=50/d=100 result, no adaptive Zhao--Cui parity, no HMC readiness, no production default change, no general rank convergence theorem. |
| Required artifacts | Phase subplans/results, visible execution ledger, Claude review ledger, final stop handoff, focused test output summaries, and any implementation diff anchors. |

## Source And Document Anchors

- Zhao--Cui paper: Eq. (13), Algorithm 2, Proposition 2, Section 3.2.
- Author source:
  - `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84-124`;
  - `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:1-35`;
  - `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:81-85`;
  - `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:352-354`.
- Local derivation:
  - `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`,
    subsection `A Fixed Branch For A Differentiable Likelihood`;
  - propositions `prop:p50-fixed-square-root-normalized`,
    `prop:p50-fixed-adaptive-relation`, and
    `prop:p50-defensive-only-rank-veto`.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, baseline, and launch readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase0-governance-baseline-subplan-2026-06-14.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase0-governance-baseline-result-2026-06-14.md` |
| 1 | One-factor rank/capacity diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase1-rank-capacity-diagnostic-subplan-2026-06-14.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase1-rank-capacity-diagnostic-result-2026-06-14.md` |
| 2 | Bounded implementation repair | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase2-implementation-repair-subplan-2026-06-14.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase2-implementation-repair-result-2026-06-14.md` |
| 3 | Bug-test closeout and next handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase3-bug-test-closeout-subplan-2026-06-14.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase3-bug-test-closeout-result-2026-06-14.md` |

## Phase Summaries

### Phase 0: Governance, Baseline, And Launch Readiness

Lock the exact baseline, source anchors, forbidden changes, local test commands,
and review loop.  Run only compile/import and a small baseline JSON probe if the
subplan and review pass.

### Phase 1: One-Factor Rank/Capacity Diagnostic

Add or run a diagnostic that varies one factor at a time around the P64 failing
baseline: fit sample count, retained sample count, bounded-support clipping, rank
or degree, ridge, and resampling degeneracy.  Phase 1 may produce a candidate
repair hypothesis, but it must not patch production behavior unless a bounded
implementation target is identified.

### Phase 2: Bounded Implementation Repair

If Phase 1 identifies a minimal repair, patch only the narrow comparator or
fixed-branch diagnostic path needed to test the hypothesis.  Preserve P63
source-pushed `computeL` fit data, defensive `tau`, target order, previous
marginal axes, and P60 thresholds.

### Phase 3: Bug-Test Closeout

Run the repaired comparator and focused P59/P60 tests.  Decide whether the P60
bug is fixed, still blocked, or moved to a new localized blocker.  Record what
is and is not concluded.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| CPU-only focused tests | AGENTS GPU/CUDA policy | No GPU evidence is needed for this rank/capacity logic; avoids sandbox GPU ambiguity. | Framework still emits CUDA chatter despite CPU-only setting. | Set `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp` and record CPU-only. | baseline |
| P64 comparator is the baseline | P64 result artifact | It is the current localized failing bug. | Stale context if code changed after P64. | Re-run a small JSON probe with the full pinned tuple: `sample_count=1`, `fit_sample_count=2`, low `(degree=0, rank=1)`, high `(degree=1, rank=2)`, including high defensive-only steps and high square-root fitted masses. | to verify |
| One factor at a time | P64 next-step recommendation | Prevents attributing success to a mixed confound. | Too slow if every rung runs full tests. | Start with minimal diagnostic rows and stop on first discriminating artifact. | planned |
| Claude review bounded excerpts | User instruction and cross-agent policy | Avoids approval blocks and overly broad review prompts. | Review may miss context. | Include exact source/result anchors and line excerpts, not whole files. | planned |

## Skeptical Plan Audit

status: PASSED_FOR_PHASE0_ONLY

The program does not treat probe metrics as scientific validation; they can only
diagnose or veto.  The baseline is the P64 failing comparator, not a weaker
toy.  The primary criterion requires the same-route P60 gate and explicit
defensive-only veto clearance.  Stop conditions are declared per phase.  The
main remaining risk is that Phase 1 could become an expensive sweep; its subplan
therefore requires a smallest-discriminating diagnostic and one-factor changes.

## Claude Review Policy

Claude is a read-only reviewer only.  It may review material subplans, result
artifacts, and bounded implementation diffs.  It cannot authorize scientific
claims, threshold changes, hidden adaptive reselection, package installs, network
fetches, detached runs, GPU claims, or product/API boundary crossings.

Claude review must use bounded prompts with paths, line spans, and exact
questions.  Do not send whole large files.  If Claude does not respond, run a
tiny read-only probe.  If the probe responds, treat the original prompt as too
large or malformed, redesign it, and retry.  Stop after five review rounds for
the same material blocker.

## Anticipated Approvals

Required during execution:

- trusted/escalated foreground `bash scripts/claude_worker.sh ... --model opus
  --effort max` for bounded read-only Claude reviews that cite exact paths,
  line spans, and questions, and whose output is preserved in the review ledger;
- CPU-only focused tests that may take several minutes.

Not planned:

- GPU/CUDA runs;
- package installation;
- network fetches;
- detached/background/overnight supervisor scripts;
- destructive git commands;
- writes outside `/home/chakwong/BayesFilter` and `/tmp`.

## Forbidden Claims And Actions

- Do not weaken P60 thresholds.
- Do not remove defensive `tau`.
- Do not rescale defensive mass except according to the P50 shifted/original-scale
  derivation and only under an explicit reviewed target.
- Do not reintroduce artificial reference-grid fit data.
- Do not silently switch target order, previous-marginal axes, source callbacks,
  branch identity, or baseline.
- Do not call adaptive Zhao--Cui parity repaired.
- Do not claim d=18 correctness, d=50/d=100 scaling, HMC readiness, source
  faithfulness, or paper-scale reproduction unless a later evidence contract
  explicitly supports it.

## Launch Rule

Launch Phase 0 only after this master program, the Phase 0 subplan, and the
visible execution runbook survive local skeptical review and bounded Claude
read-only review ending in `VERDICT: AGREE`.  Later phases launch only after the
previous phase writes its result, refreshes the next subplan, and satisfies the
review rule declared in that subplan.
