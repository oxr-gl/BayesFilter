# P69 Phase 5b Result: Fixed-Variant Repair/Design Diagnostic

metadata_date: 2026-06-15
status: P69_PHASE5B_FIXED_VARIANT_REPAIR_DESIGN_DIAGNOSTIC_PASSED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 5b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 5b remained read-only.  Claude review returned `VERDICT: AGREE`.
Existing Phase 3 JSON artifacts are sufficient to choose the next bounded
repair/design target without a new ladder, code change, GPU/HMC command, or
threshold change.

Selected next repair/design target:

`RANK_ACTIVITY_AND_DEGREE_NORMALIZER_DESIGN_DIAGNOSTIC`

This target should be handled by a new subplan before execution.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Which bounded repair/design diagnostic should be applied to the fixed-HMC adaptation before validation/scaling/HMC phases? |
| Baseline/comparator | Phase 3/4 rank zero-delta and degree-instability artifacts. |
| Primary criterion | Satisfied: a concrete next diagnostic target is identified without changing thresholds or making correctness claims. |
| Veto diagnostics | No adaptive parity claim; no long/GPU/HMC work; no threshold change; no d18/scaling/HMC readiness claim. |
| Not concluded | No correctness, scaling, HMC readiness, adaptive parity, or paper-failure claim. |

## Read-Only Diagnostic Extraction

Read-only command:

```bash
python - <<'PY'
import json
from pathlib import Path
path = Path('docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-diagnostics-2026-06-15.json')
data = json.loads(path.read_text())
# Printed rank branch hashes/core summaries and degree fit/holdout/normalizer summaries.
PY
```

No files were changed by this analysis.

## Rank Activity Diagnosis

Rank 2 and rank 3 are not literally the same branch:

- fit branch hashes differ;
- density branch hashes differ;
- rank tuples differ.

But their observable diagnostics are identical:

- normalizer terms by step are identical;
- effective sample size by step is identical: `[1.0, 1.0]`;
- correction log-weight ranges are identical;
- fit residuals are identical by step;
- holdout/replay residuals are identical by step;
- all four ladder metric deltas are zero.

Core summaries show the only visible difference is the rank capacity itself:

- rank 2 nonzero entries per core: 2;
- rank 3 nonzero entries per core: 2;
- near-zero core counts: 0 for both.

Bounded conclusion:

- additional rank capacity is present in the branch identity but functionally
  inactive under the current initialization/fitting path and metrics;
- deterministic degeneracy remains unresolved because the existing JSON does
  not inspect TT gauge directions, singular directions, or per-channel
  coefficient activity beyond aggregate core summaries.

## Degree Normalizer/Design Diagnosis

Degree 2 is not a simple fit failure:

- degree 2 improves in-sample fit residuals:
  - step 1: `0.08234689014371575` to `0.040451316910524164`;
  - step 2: `0.10990965252882855` to `0.0024177977036540545`.

But degree 2 strongly changes normalizers and downstream diagnostics:

- step 1 `log_transport_normalizer`: `15.954892344716342` to
  `75.49537300217852`;
- step 2 `log_transport_normalizer`: `66.8323667216454` to
  `46.49926837338214`;
- step 1 mixture normalizer: `8.494184787799247e6` to
  `6.126661753753613e32`;
- step 2 mixture normalizer: `1.0590783246288742e29` to
  `1.564500358856323e20`;
- degree 2 nonzero entries per core increase from 2 to 3.

Holdout/replay behavior is mixed:

- step 1 degree 2 worsens holdout/replay residuals sharply;
- step 2 degree 2 improves holdout/replay residuals sharply.

Bounded conclusion:

- the next diagnostic should not be a broad rerun;
- it should directly inspect degree-normalizer sensitivity, target scaling, and
  design coverage, because in-sample residual improvement does not protect the
  normalizer/downstream metrics;
- overfitting and target scaling remain live explanations.

## Selected Next Diagnostic Target

The next subplan should implement or inspect, in this order:

1. rank-channel activity diagnostics:
   - per-rank-channel coefficient norms;
   - embedded-rank comparison of rank 2 inside rank 3 if available;
   - direct evidence for whether the extra rank channel is unused or merely
     gauge-hidden;
2. degree-normalizer sensitivity diagnostics:
   - per-step normalizer decomposition for degree 1 vs degree 2;
   - target-value and shifted-target scale summaries;
   - design coverage summaries for polynomial degree 2;
3. conservative branch recommendation:
   - whether degree 1/rank 2 should be the only candidate for later d18
     validation until the degree-2 instability is repaired;
   - or whether validation must remain blocked.

## Remaining Unresolved Explanations

- Deterministic degeneracy: unresolved.
- Overfitting: unresolved.
- Target scaling: unresolved.
- Design coverage insufficiency: supported as an inference, not a proven
  mechanism.
- Adaptive Zhao--Cui comparison: deferred to a separate lane.

## Nonclaims

- No d18 correctness claim.
- No scaling-readiness claim.
- No HMC-readiness claim.
- No adaptive Zhao--Cui parity claim.
- No paper-failure claim.
- No threshold tuning.

## Next Handoff

Write a Phase 5c subplan for
`RANK_ACTIVITY_AND_DEGREE_NORMALIZER_DESIGN_DIAGNOSTIC` before execution.

If the user wants to change the scientific target to adaptive Zhao--Cui
reproduction instead, stop and open a separate reviewed adaptive-reproduction
program.

Claude residual risks for Phase 5c:

- rank diagnosis remains observational until direct channel-level diagnostics
  distinguish inactive from gauge-hidden extra capacity;
- degree-2 diagnosis remains a shortlist, not a proven root cause;
- if bounded CPU-only diagnostics cannot expose the needed internals, Phase 5c
  must use the blocker path;
- any later d18 validation recommendation must not be narrated as adaptive
  parity or readiness evidence.
