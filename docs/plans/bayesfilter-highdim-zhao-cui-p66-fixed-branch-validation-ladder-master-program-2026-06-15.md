# P66 Master Program: Fixed-Branch Validation Ladder Replacement

metadata_date: 2026-06-15
status: P66_FIXED_BRANCH_VALIDATION_LADDER_REPLACEMENT_PASSED
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Objective

Replace the old P60 low/high closeness gate with a validation ladder that is
appropriate for the Zhao--Cui SIR fixed-HMC variant.

The old P60 gate compares `(degree=0, rank=1)` against `(degree=1, rank=2)` and
treats large differences as a rank-convergence blocker.  For the 36D SIR
filtering target, that comparison is not a valid primary convergence criterion:
the low branch is intentionally crude and should plausibly differ greatly from
the first nontrivial high branch.

P66 must demote that old comparison to a sentinel/explanatory diagnostic.  It
must not relax the old thresholds and call that a fix.

## Replacement Validation Design

P66 replaces the old primary P60 rank-convergence question with three gates.

1. Strict source-route invariant gate:
   - target dimension `36`;
   - realized target `[x_t, x_{t-1}]`;
   - previous marginal keep axes `0..17`;
   - previous marginal input axes `18..35`;
   - source-pushed fit-data route;
   - defensive `tau = 1e-8`;
   - fixed-HMC adaptation metadata recorded;
   - no unqualified source-faithful Zhao--Cui claim.

2. Fixed-branch admissibility and noncollapse gate:
   - fit status `OK`;
   - finite target values, shift constants, density values, and normalizers;
   - positive square-root normalizer at every step;
   - no defensive-only steps;
   - no zero/near-zero fitted TT core collapse;
   - condition-number veto not triggered;
   - branch identity records degree, rank, fit samples, initialization rule,
     and adaptation class.

3. One-factor adjacent stability ladder contract:
   - sentinel diagnostic: `(degree=0, rank=1)` versus `(degree=1, rank=2)`,
     explanatory only;
   - rank ladder: candidate `(degree=1, rank=2)` versus stronger
     `(degree=1, rank=3)`;
   - degree ladder: candidate `(degree=1, rank=2)` versus stronger
     `(degree=2, rank=2)`;
   - Phase 2 implements schema-only adjacent rows and sample-adequacy
     permission-to-diagnose checks;
   - actual convergence-style diagnostics require executing both adjacent
     ladders under a reviewed experiment plan.

## Proposed Statuses

- `PASS_FIXED_BRANCH_ADMISSIBLE_NONCOLLAPSED`
- `READY_FIXED_BRANCH_VALIDATION_LADDER_SCHEMA`
- `PASS_ADJACENT_LADDER_DIAGNOSTICS_STABLE`
- `WARN_SENTINEL_BRANCH_DIFFERS_FROM_CANDIDATE`
- `BLOCK_SOURCE_ROUTE_INVARIANT_DRIFT`
- `BLOCK_FIXED_BRANCH_DEFENSIVE_ONLY`
- `BLOCK_FIT_DESIGN_UNDERDETERMINED_FOR_CONVERGENCE`
- `BLOCK_ADJACENT_RANK_LADDER_NOT_STABLE`
- `BLOCK_ADJACENT_DEGREE_LADDER_NOT_STABLE`
- `BLOCK_VALIDATION_LADDER_IMPLEMENTATION_SCOPE`

## Phase Index

| Phase | Name | Subplan | Required Result |
| --- | --- | --- | --- |
| 0 | Governance, baseline, and planning basis | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase0-governance-baseline-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase0-governance-baseline-result-2026-06-15.md` |
| 1 | Validation contract and API design | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase1-validation-contract-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase1-validation-contract-result-2026-06-15.md` |
| 2 | Implementation and focused tests | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase2-implementation-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase2-implementation-result-2026-06-15.md` |
| 3 | Closeout and handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase3-closeout-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase3-closeout-result-2026-06-15.md` |

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the invalid P60 low/high closeness gate be replaced by an admissibility plus adjacent-ladder validation contract without weakening thresholds, changing the source route, or overclaiming correctness? |
| Baseline/comparator | P65 final status: zero-TT repair passed; old P60 still blocks only because `(0,1)` and `(1,2)` differ in log marginal and normalizer increments. |
| Primary program pass criterion | New artifacts and code demote `(0,1)` vs `(1,2)` to sentinel evidence, add admissibility/noncollapse as a primary fixed-branch gate, add adjacent rank/degree schema/status rows with sample-adequacy checks, and pass focused tests/reviews. |
| Veto diagnostics | Old thresholds weakened; sentinel gap hidden; source-route invariants changed; defensive `tau` changed; fixed-HMC adaptation called source-faithful Zhao--Cui; d=18 correctness claimed from admissibility; adjacent-ladder evidence treated as correctness without checks. |
| Explanatory diagnostics | Old P60 deltas, square-root normalizers, core norms, condition numbers, ESS, correction ranges, fit residuals, sample adequacy ratios, adjacent-ladder deltas. |
| Not concluded | No d=18 correctness, no d=50/d=100 scaling, no adaptive Zhao--Cui parity, no HMC production readiness, no theorem that adjacent-ladder stability is sufficient for scientific validity. |

## Required Review Discipline

- Claude is a read-only reviewer only.
- Claude prompts must use bounded excerpts and summaries, not whole files.
- Claude cannot authorize scientific, product, funding, model-file, runtime, or
  human-approval boundary crossings.
- Stop after five Claude rounds for the same blocker.
- If Claude does not respond, run a tiny read-only probe.  If the probe
  responds, redesign the stalled prompt.

## Global Forbidden Actions

- Do not weaken P60 thresholds and call that a fix.
- Do not hide the old sentinel gap.
- Do not use `(degree=0, rank=1)` versus `(degree=1, rank=2)` closeness as a
  primary convergence gate for this target.
- Do not claim d=18 correctness from admissibility or adjacent-ladder stability
  alone.
- Do not claim adaptive Zhao--Cui parity.
- Do not call fixed-HMC constant-path initialization source-faithful Zhao--Cui.
- Do not change target/order/axes, defensive `tau`, or source-pushed fit-data
  route without a new reviewed plan.

## Interpretation Discipline

- Fixed-branch admissibility is a necessary precondition, not convergence
  evidence.
- Sample adequacy is a permission-to-diagnose gate, not evidence that
  convergence holds.
- Adjacent one-factor ladder stability is the intended P66 convergence-style
  diagnostic, but it has not been executed in Phase 2 and even a future pass
  would not imply d=18 correctness.
- The old `(0,1)` versus `(1,2)` gap must remain visible as sentinel evidence;
  the neutral status is `WARN_SENTINEL_BRANCH_DIFFERS_FROM_CANDIDATE`.

## Adjacent-Ladder Comparison Invariants

Adjacent ladder rows are fair only when these are held fixed or any intentional
difference is recorded explicitly:

- target and source route;
- source-pushed fit-data policy;
- fixed-HMC adaptation metadata;
- defensive `tau`;
- initialization rule;
- sample-adequacy rule and fit-sample policy;
- target/order/axes and previous-marginal axes;
- threshold definitions used for diagnostics.

## Anticipated Approvals

- Foreground Claude worker review via
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh`.
- CPU-only local tests and probes with `CUDA_VISIBLE_DEVICES=-1
  MPLCONFIGDIR=/tmp`.
- Any GPU/CUDA run would require separate escalated approval, but P66 is planned
  as CPU-only unless a later reviewed phase says otherwise.
