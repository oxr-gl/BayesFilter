# P69 Phase 4 Subplan: Rank-Channel Activity And Degree-Instability Diagnosis

metadata_date: 2026-06-15
status: READY_AFTER_PHASE3_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Diagnose the structural meaning of the Phase 3 adjacent-ladder result:

- rank ladder passed with zero metric deltas between rank 2 and rank 3;
- degree ladder blocked with all four frozen threshold metrics exceeded;
- all rows had finite available post-fit holdout/replay diagnostics and no
  source-route, branch-identity, route-mismatch, or condition-number veto.

The phase must separate implementation failure, diagnostic insufficiency,
inactive rank channels, degree/basis sensitivity, and evidence against the
current fixed-variant design.

Phase 4 must explicitly classify every inherited Phase 3 hypothesis:

- for rank zero-delta, classify inactive rank channels, deterministic
  degeneracy, and metric-insensitive comparison as supported, weakened, or
  unresolved;
- for degree instability, classify basis/domain sensitivity, design coverage
  insufficiency, overfitting, target scaling, and structural sensitivity of the
  fixed variant as supported, weakened, or unresolved.

## Entry Conditions Inherited From Phase 3

- Phase 3 result exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-rerun-result-2026-06-15.md`.
- Phase 3 JSON exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-diagnostics-2026-06-15.json`.
- Claude read-only review of Phase 3 returns `VERDICT: AGREE`.
- Phase 3 row veto diagnostics are clean for all executed rows.
- Phase 3 top-level ladder status is blocked only because the degree ladder
  exceeds frozen threshold metrics.

## Required Artifacts

- Phase 4 structural diagnosis result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-result-2026-06-15.md`.
- Updated P69 execution ledger and Claude review ledger.
- Refreshed Phase 5 route-decision subplan.
- Optional diagnostic script or JSON only if the Phase 3 JSON does not contain
  enough information to make a bounded structural diagnosis.

## Required Checks/Tests/Reviews

Start with read-only artifact analysis:

```bash
python - <<'PY'
import json
from pathlib import Path
path = Path('docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-diagnostics-2026-06-15.json')
data = json.loads(path.read_text())
print(data['status'])
print(data['rank_ladder']['status'], data['rank_ladder']['deltas'])
print(data['degree_ladder']['status'], data['degree_ladder']['deltas'])
for label, row in sorted(data['rows'].items()):
    bd = row['budget_limitation_diagnostics']
    print(label, row['degree'], row['rank'], row['fit_sample_count'],
          row['budget_limited'], bd['holdout_replay_resolution_status'],
          bd['branch_identity_drift_steps'], bd['route_mismatch_steps'])
PY
```

If no code changes are needed, compile/pytest are not required for Phase 4.

If Phase 4 adds any code or tests, run the smallest focused CPU-only compile
and pytest checks that cover the changed files, and record them in the Phase 4
result.

Claude review must inspect:

- Phase 3 result;
- Phase 3 JSON summary;
- Phase 4 diagnosis result;
- Phase 5 route-decision subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What structural explanation is best supported by Phase 3 for rank zero-delta and degree instability in the fixed-HMC adaptation? |
| Baseline/comparator | Phase 3 row table and P68/P67 prior ambiguity before holdout/replay diagnostics. |
| Primary criterion | Produce a bounded diagnosis that classifies each explanation as supported, weakened, or unresolved using only clean Phase 3 diagnostics and clearly stated limitations. |
| Veto diagnostics | Source-route invariant drift; branch identity drift; route mismatch; missing/nonfinite holdout/replay diagnostics; condition warning/veto; unreviewed threshold tuning; new long experiment without a subplan. |
| Explanatory diagnostics | Rank/degree deltas, fit residuals, holdout/replay residuals, branch hashes, source invariants, sample budgets, nonclaims. |
| Not concluded | No correctness, scaling, HMC readiness, adaptive parity, or proof-level convergence claim. |
| Artifact preserving result | Phase 4 structural diagnosis result. |

## Forbidden Claims/Actions

- Do not treat rank zero-delta as convergence without channel-activity
  evidence.
- Do not treat degree instability as failure of the Zhao--Cui paper.
- Do not tune thresholds or choose a new default route in Phase 4.
- Do not run GPU/CUDA/HMC commands.
- Do not run a new ladder or sweep without a reviewed amendment.
- Do not call finite holdout/replay residuals correctness.

## Exact Next-Phase Handoff Conditions

Phase 4 may hand off to Phase 5 only if:

- each candidate explanation is classified as supported, weakened, or
  unresolved;
- the rank zero-delta explanations explicitly include inactive rank channels,
  deterministic degeneracy, and metric-insensitive comparison;
- the degree-instability explanations explicitly include basis/domain
  sensitivity, design coverage insufficiency, overfitting, target scaling, and
  structural sensitivity of the fixed variant;
- the result states whether the current fixed variant is likely an
  implementation bug, a fit-design limitation, a fixed-HMC adaptation
  limitation, or still underdiagnosed;
- uncertainty and nonclaims are explicit;
- Phase 5 receives a concrete route-decision menu: repair current fixed
  variant, add a bounded diagnostic experiment, fork adaptive-reproduction
  lane, or stop for human direction;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker result if:

- structural attribution cannot be made from the current artifact without a
  new experiment;
- the diagnosis would require threshold tuning;
- the diagnosis would require changing source-route semantics;
- the diagnosis would require GPU/HMC or a long run not covered by this
  subplan;
- Claude and Codex do not converge after five review rounds.
