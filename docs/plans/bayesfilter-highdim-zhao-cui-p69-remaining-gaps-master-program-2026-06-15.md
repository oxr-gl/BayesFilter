# P69 Master Program: Zhao--Cui Remaining Gaps Closure

metadata_date: 2026-06-15
status: DRAFT_PENDING_REVIEW
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Objective

Govern the remaining Zhao--Cui work after P65--P68 without losing the
distinction between the Zhao--Cui adaptive algorithm and the BayesFilter
fixed-HMC adaptation.

The current execution target is the fixed-HMC adaptation.  Adaptive
source-faithful Zhao--Cui reproduction is a separate lane unless a reviewed
phase explicitly opens it.  P69 must close or classify the remaining gaps before
any d18 correctness, d50/d100 scaling, adaptive parity, or HMC-readiness claim is
allowed.

## Starting Point

P65 repaired the fixed high-rank zero square-root collapse.  P66 replaced the
invalid old low/high closeness gate with an admissibility and adjacent-ladder
contract.  P67 executed adjacent fixed-budget ladders and remained inconclusive.
P68 exposed fit-quality diagnostics, but the ladder still remained
inconclusive because holdout/replay evidence was unavailable and the degree
ladder exceeded all declared thresholds.

P69 starts from these facts:

- the density and normalizer algebra are paper/source anchored;
- the implemented branch freezing is a `fixed_hmc_adaptation`;
- the current implementation is not adaptive Zhao--Cui parity;
- the rank ladder zero delta may indicate inert additional rank channels;
- the degree ladder instability may indicate overfitting, domain/basis/design
  mismatch, or real structural sensitivity;
- no holdout/replay validation, d18 paper-scale SIR validation, scaling route,
  fixed-branch derivative validation, or HMC diagnostic ladder has passed.

## Source-Governance Boundary

Every implementation or claim must classify each material choice as exactly one
of:

- `source_faithful`;
- `fixed_hmc_adaptation`;
- `extension_or_invention`.

Do not use "faithful", "source-faithful", "paper-scale Zhao--Cui", or
equivalent language unless both Zhao--Cui paper anchors and author source
file/line anchors have been inspected and cited.  Fixed-branch work defaults to
`fixed_hmc_adaptation` unless proven otherwise.

The clean-room boundary in
`docs/plans/bayesfilter-highdim-zhao-cui-source-governance-charter-2026-06-05.md`
remains binding.  MATLAB source may be inspected and cited as behavioral
evidence; it must not be copied or line-translated into BayesFilter code.

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | Governance and claim-boundary baseline | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase0-governance-claim-boundary-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase0-governance-claim-boundary-result-2026-06-15.md` |
| 1 | Holdout/replay diagnostic design | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-holdout-replay-design-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-holdout-replay-design-result-2026-06-15.md` |
| 2 | Holdout/replay implementation and focused tests | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-result-2026-06-15.md` |
| 3 | Adjacent ladder rerun with holdout/replay evidence | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-rerun-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-rerun-result-2026-06-15.md` |
| 4 | Rank-channel activity and degree-instability diagnosis | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-result-2026-06-15.md` |
| 5 | Fixed-variant repair decision or adaptive-reproduction fork | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5-route-decision-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5-route-decision-result-2026-06-15.md` |
| 6 | d18 paper-scale SIR validation ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase6-d18-sir-validation-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase6-d18-sir-validation-result-2026-06-15.md` |
| 7 | d50/d100 scaling-route design and preflight | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase7-scaling-route-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase7-scaling-route-result-2026-06-15.md` |
| 8 | Fixed-branch derivative and HMC-readiness diagnostics | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase8-hmc-readiness-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase8-hmc-readiness-result-2026-06-15.md` |
| 9 | p50, source-ledger, and closeout refresh | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase9-document-closeout-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase9-document-closeout-result-2026-06-15.md` |

Only Phase 0 is launched by this initial runbook.  Each later phase must have a
dedicated subplan reviewed before execution.

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the remaining Zhao--Cui fixed-HMC adaptation gaps be closed or classified under source-anchor governance without promoting diagnostic evidence to correctness claims? |
| Baseline/comparator | P50 fixed-branch document, P65 zero-TT repair, P66 validation contract, P67/P68 adjacent-ladder results, Zhao--Cui JMLR paper, and author source snapshot under `third_party/audit/zhao_cui_tensor_ssm_p10/source`. |
| Primary program pass criterion | Every listed gap is either closed by reviewed artifacts and checks, or recorded as a blocker with exact source/implementation evidence and forbidden claims preserved. |
| Veto diagnostics | Adaptive parity claimed from fixed branch; d18 correctness claimed from two-step assembly; holdout/replay absence hidden; degree-ladder failure ignored; rank zero-delta treated as convergence without rank-channel diagnostics; d50/d100 scaling claimed without scaling route; HMC readiness claimed without same-branch derivative and sampler diagnostics. |
| Explanatory diagnostics | Fit residuals, holdout/replay residuals, condition numbers, core norms, rank-channel activity, normalizer deltas, probe/retained density deltas, ESS, correction ranges, memory forecasts, finite-difference residuals, HMC diagnostics. |
| Not concluded | No adaptive Zhao--Cui parity, no d18 filtering correctness, no d50/d100 scaling, no HMC production readiness, no formal proof certification unless a dedicated formalization phase passes. |
| Artifacts | P69 master program, visible runbook, visible ledger, review ledger, phase subplans/results, blocker records, updated p50/source ledgers when reached. |

## Phase Objectives

### Phase 0: Governance and claim-boundary baseline

Confirm the launch baseline, source-governance rules, remaining gap list, and
claim taxonomy.  Produce Phase 1 design subplan only after this boundary passes.

### Phase 1: Holdout/replay diagnostic design

Specify source-route-consistent holdout/replay diagnostics for P59/P67-style
fixed-TTSIRT fits.  The design must not change thresholds after seeing new
results.

### Phase 2: Holdout/replay implementation and focused tests

Implement the diagnostics in the smallest code surface needed, add focused
tests, and preserve existing P59/P66/P67 behavior except for newly exposed
holdout/replay fields.

### Phase 3: Adjacent ladder rerun with holdout/replay evidence

Rerun the adjacent ladder under the reviewed contract and interpret rank and
degree rows with holdout/replay diagnostics.  Do not tune thresholds after
seeing data.

### Phase 4: Rank-channel activity and degree-instability diagnosis

Determine whether the rank-zero-delta row reflects inactive extra rank
channels, and whether the degree instability reflects overfitting, design
coverage, basis/domain mismatch, or structural sensitivity.

### Phase 5: Fixed-variant repair decision or adaptive-reproduction fork

Decide whether to continue repairing the fixed-HMC adaptation, open a separate
adaptive source-reproduction lane, or stop with blockers.

### Phase 6: d18 paper-scale SIR validation ladder

Only after lower gates pass, execute or block a paper-scale SIR validation plan
for \(J=9\), \(d=18\), \(T=20\), and appropriate rank/basis/source-route
settings.

### Phase 7: d50/d100 scaling-route design and preflight

Design or block the scaling transition route.  Dense retained-grid semantics are
not a scaling route.

### Phase 8: Fixed-branch derivative and HMC-readiness diagnostics

Run same-branch finite-difference checks and HMC diagnostic tiers only after the
scalar branch and validation gates justify them.

### Phase 9: p50, source-ledger, and closeout refresh

Refresh p50 and related ledgers with the actual results, claim boundaries, and
remaining blockers.

## Global Forbidden Actions

- Do not call fixed-HMC adaptation adaptive Zhao--Cui parity.
- Do not call bounded two-step assembly d18 correctness.
- Do not use low/high branch closeness as the primary criterion for this model.
- Do not weaken thresholds or alter pass/fail criteria after seeing results.
- Do not hide holdout/replay absence.
- Do not treat fit residual, sample adequacy, or condition numbers as
  correctness by themselves.
- Do not claim scaling from dense-equivalent lower-route evidence.
- Do not claim HMC readiness without same-branch derivative checks and sampler
  diagnostics.
- Do not copy or line-translate author MATLAB source.

## Review And Repair Loop

Claude may be used only as a read-only reviewer for material subplans, deltas,
and closeout records.  Codex remains supervisor and executor.

Review prompts must be bounded: use summaries, exact paths, line ranges, and
specific questions.  Do not send whole large files to Claude.  If Claude does
not respond, run a tiny read-only probe.  If the probe responds, treat the
original prompt as faulty, redesign it, and retry.  Stop after five review
rounds for the same blocker.

If review finds a fixable problem, patch the same artifact visibly, rerun
focused checks, and record the repair in the review ledger.  If review does not
converge, write a blocker result and stop.

## Anticipated Approvals

- Foreground Claude read-only reviews via
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh`.
- CPU-only local checks with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`.
- Later long CPU ladder runs may need explicit user confirmation in their
  phase subplans before launch.
- Any GPU/CUDA/HMC command requires separate escalated/trusted approval before
  execution.
