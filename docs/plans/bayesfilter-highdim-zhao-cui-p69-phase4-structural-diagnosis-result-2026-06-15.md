# P69 Phase 4 Result: Rank-Channel Activity And Degree-Instability Diagnosis

metadata_date: 2026-06-15
status: P69_PHASE4_STRUCTURAL_DIAGNOSIS_PASSED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 4 is analysis-only.  Claude review returned `VERDICT: AGREE`.  The Phase
3 JSON contains enough evidence for a bounded structural diagnosis, so no new
code, ladder rerun, GPU/HMC command, or threshold change was needed.

The best supported diagnosis is:

- the rank-3 branch is functionally inactive relative to rank 2 under the
  current fixed branch and metrics;
- the degree-2 branch is structurally sensitive under the current fixed variant
  and should be treated as a fixed-variant fit-design problem, not as a
  Zhao--Cui paper failure.

This is a diagnosis of the current fixed-HMC adaptation only.

## Analysis Command

Read-only artifact analysis:

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

Result: analysis completed; no code changes were needed in Phase 4.

## Evidence Summary

Clean veto diagnostics:

- all five rows have status `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY`;
- all five rows have `budget_limited = false`;
- all five rows have
  `PASS_HOLDOUT_REPLAY_DIAGNOSTICS_AVAILABLE`;
- no row has missing fit-resolution fields;
- no row has branch-identity drift or route mismatch;
- no row has missing/nonfinite holdout or replay diagnostics;
- no row has condition warning/veto.

Rank comparison:

- rank candidate: degree 1, rank 2, fit samples 36;
- rank stronger: degree 1, rank 3, fit samples 36;
- authorized difference: `fit_rank`;
- unauthorized comparison differences: none;
- all four ladder deltas are exactly zero;
- fit residuals are identical by step:
  `0.09573780350980712`, `0.04261274001476897`;
- post-fit holdout/replay residuals are identical by step:
  `0.9935996341954345 / 0.6201368738236436`,
  `0.5231985709493626 / 0.4838067615965225`.

Degree comparison:

- degree candidate: degree 1, rank 2, fit samples 24;
- degree stronger: degree 2, rank 2, fit samples 24;
- authorized difference: `fit_degree`;
- unauthorized comparison differences: none;
- all four ladder threshold metrics fail:
  - `log_marginal_abs_delta = 39.90354896700583`;
  - `normalizer_increment_abs_deltas = [59.54048065746218, 19.636931690456336]`;
  - `probe_log_density_median_abs_delta = 21.25481599004719`;
  - `retained_log_density_median_abs_delta = 335.22761346150156`;
- degree 2 improves in-sample fit residuals:
  - degree 1: `0.08234689014371575`, `0.10990965252882855`;
  - degree 2: `0.040451316910524164`, `0.0024177977036540545`;
- degree 2 has mixed post-fit diagnostic behavior:
  - step 1 holdout/replay residuals worsen sharply relative to degree 1;
  - step 2 holdout/replay residuals improve sharply relative to degree 1.

## Hypothesis Classification

Classification labels are mutually exclusive per hypothesis:

- `supported`: the Phase 3 artifact gives positive evidence for this
  explanation as a current working diagnosis;
- `weakened`: the Phase 3 artifact gives evidence against this explanation;
- `unresolved`: the Phase 3 artifact does not isolate the explanation.

### Rank Zero-Delta

| Hypothesis | Classification | Evidence |
| --- | --- | --- |
| Inactive rank channels | `supported` | Rank 2 and rank 3 have identical ladder deltas, fit residuals, and holdout/replay residuals under the same degree and sample budget, while the only authorized difference is `fit_rank`.  This supports functional inactivity of the added rank capacity under the current fixed branch. |
| Deterministic degeneracy | `unresolved` | The branch is deterministic and fixed, so deterministic degeneracy remains plausible, but Phase 3 did not inspect TT core gauges, singular directions, or channel activity directly.  The artifact supports functional inactivity, not the mechanism that caused it. |
| Metric-insensitive comparison | `weakened` | The zero result is not limited to one comparison metric: log marginal, normalizer increments, probe density, retained density, fit residuals, and holdout/replay residuals all match.  A hidden metric-insensitivity explanation is therefore less likely, though not formally impossible. |

### Degree Instability

| Hypothesis | Classification | Evidence |
| --- | --- | --- |
| Basis/domain sensitivity | `supported` | Changing only polynomial degree from 1 to 2, with rank and fit sample count fixed, produces large changes in log marginal, normalizer increments, probe density, retained density, and holdout/replay residual scales.  This is direct evidence of degree/basis sensitivity on the current local `[-1,1]^d` frame. |
| Design coverage insufficiency | `supported` | Degree 2 improves in-sample fit residuals while the downstream metrics and diagnostic residuals remain unstable.  With only the fixed budget used in the ladder, the artifact supports insufficient design coverage for interpreting degree escalation cleanly. |
| Overfitting | `unresolved` | Degree 2 lowers in-sample residuals and worsens step 1 holdout/replay residuals, which is overfitting-like.  But degree 2 improves step 2 holdout/replay residuals, so the artifact does not isolate overfitting as the explanation. |
| Target scaling | `unresolved` | The normalizer and residual scales are large and unstable, making target scaling a plausible contributor.  Phase 3 did not run a scaling-normalization comparison, so this remains unresolved. |
| Structural sensitivity of the fixed variant | `supported` | Source invariants, branch identity, route match, finite diagnostics, and condition checks are clean; the authorized degree change alone produces threshold failures.  This supports structural sensitivity of the current fixed-HMC adaptation. |

## Implementation-Failure And Diagnostic-Sufficiency Ledger

| Explanation | Classification | Evidence |
| --- | --- | --- |
| Implementation failure in the source-route wiring | `weakened` | Source invariants pass for every row; branch identity does not drift; previous-marginal axes and target order are unchanged; no route mismatch appears. |
| Numerical diagnostic insufficiency from missing holdout/replay | `weakened` | Phase 3 removed the P68 ambiguity: holdout and replay diagnostics are present and finite for every row. |
| Fit-design limitation of the current fixed variant | `supported` | Degree escalation changes downstream quantities despite clean route diagnostics and improved in-sample residuals, so the current fixed fit design remains underdiagnosed and unstable. |
| Evidence against the adaptive Zhao--Cui algorithm | `weakened` | The run is a fixed-HMC adaptation with deterministic branch freezing and post-fit diagnostics; it is not an adaptive Zhao--Cui reproduction. |

## Route Implication For Phase 5

The current evidence does not justify claiming d18 correctness, scaling
readiness, or HMC readiness.  It also does not justify treating the degree
failure as a paper failure or immediately opening adaptive-reproduction as the
only route.

Phase 5 should decide among:

1. continue the fixed-variant lane with a bounded repair/design diagnostic
   focused on degree/basis sensitivity, design coverage, target scaling, and
   direct rank-channel activity;
2. open a separate adaptive-reproduction lane only if the scientific target is
   changed from fixed-HMC adaptation to author-algorithm reproduction;
3. stop for human direction if the next scientific target is no longer the
   fixed variant.

The analysis favors option 1 as the next engineering route, with option 2 kept
separate as a distinct scientific program.

## Nonclaims

- No rank-convergence proof.
- No d18 filtering correctness claim.
- No d50 or d100 scaling claim.
- No HMC production-readiness claim.
- No adaptive Zhao--Cui parity claim.
- No claim that degree instability falsifies the Zhao--Cui paper.
- No claim that whole-batch hash disjointness proves pointwise set
  disjointness.

## Next-Phase Handoff

Phase 5 should convert this diagnosis into a route decision.  A valid Phase 5
decision must preserve the fixed-HMC/adaptive-reproduction boundary and must
not authorize later validation, scaling, or HMC phases until the degree/basis
and rank-channel questions are either repaired, bounded, or explicitly accepted
as blockers.

Claude residual risks for Phase 5:

- do not upgrade design coverage insufficiency into a proven mechanism without
  a direct coverage diagnostic;
- keep deterministic degeneracy, overfitting, and target scaling as competing
  unresolved explanations;
- treat fixed-variant repair as an engineering next step, not evidence against
  adaptive Zhao--Cui in principle;
- do not upgrade clean source-route invariants into correctness, scaling
  readiness, HMC readiness, or paper-level conclusions.
