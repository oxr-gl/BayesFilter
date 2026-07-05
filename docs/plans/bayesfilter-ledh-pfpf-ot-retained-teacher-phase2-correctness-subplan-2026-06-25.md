# Subplan: LEDH-PFPF-OT retained-teacher Phase 2 correctness rung

## Parent program
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md`

## Purpose
Compare `cold`, `heuristic`, and `learned` only on correctness-preservation before any
runtime gain is interpreted.

## Question
Do the warm-start arms preserve the same transport object, residual contract, and
barycentric semantics as the frozen exact baseline?

## Scope
- Arms: `cold`, `heuristic`, `learned`
- Route: exact same batched streaming LEDH-PFPF-OT path only
- Budget: fixed matched corrective budget across all compared arms
- Device / precision / seeds / particle count: frozen from Phase 1 baseline contract
- No semantic-changing alternatives allowed in this subplan

## Correctness contract
The compared arm must preserve:
- finite outputs
- residual parity
- no teacher/object drift
- same route metadata
- same barycentric semantics
- same declared transport path and output interpretation

## Veto diagnostics
- non-finite outputs
- residual failure
- route drift
- teacher/object mismatch
- hidden warm-start budget mismatch
- changed output semantics

## Diagnostics
Primary:
- teacher-preservation discrepancy / RMSE
- residual summary by arm
- finite-output flags
- route metadata by arm

Secondary:
- timing summaries (not promotable here)
- memory snapshots
- latent/state diagnostics if available

## Expected failure modes
- learned warm start changes the route silently
- heuristic and learned arms preserve finiteness but break residual parity
- route-preserving replay differs enough to indicate teacher drift
- warm-start mode appears faster only because semantics changed

## What would change our mind
- If learned warm start fails semantic-preservation checks, the retained-teacher lane should not advance to effectiveness interpretation no matter how fast it appears.

## Command template
```bash
# repeat the exact same baseline command, varying only --warmstart-mode
--warmstart-mode none
--warmstart-mode heuristic
--warmstart-mode learned
```

## Interpretation rule
- Only arms that pass the correctness gates may advance to the effectiveness rung.
- If `learned` fails but `heuristic` passes, learned is blocked while heuristic remains admissible for later comparison.
