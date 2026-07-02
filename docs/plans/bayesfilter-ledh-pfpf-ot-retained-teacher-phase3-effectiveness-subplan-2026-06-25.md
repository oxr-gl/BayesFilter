# Subplan: LEDH-PFPF-OT retained-teacher Phase 3 effectiveness rung

## Parent program
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md`

## Purpose
Evaluate whether a correctness-preserving retained-teacher warm-start route reduces
warm-call median time or effective correction burden on the real LEDH-PFPF-OT path.

## Question
Conditional on passing Phase 2 correctness, does `learned` outperform `cold` (and
possibly `heuristic`) on the primary runtime/correction-burden metric at fixed
transport semantics?

## Scope
- Primary comparison: `cold` vs `learned`
- Secondary comparison: `heuristic` vs `learned`
- Route: exact same batched streaming LEDH-PFPF-OT path
- Budget: fixed matched corrective budget
- Device / precision / seeds / particle count: frozen from master program
- Promotion phase: yes, this is the only promotable effectiveness phase

## Effectiveness contract
A promotable success requires:
- correctness gates already passed,
- no worse teacher-preservation discrepancy than the baseline envelope,
- no residual regression,
- improved warm-call median seconds or reduced effective correction burden.

## Veto diagnostics
- any runtime gain with failed residual parity
- any teacher/object drift
- any route mismatch
- unfair budget mismatch
- learned route slower than heuristic and cold without compensating correctness advantage

## Diagnostics
Primary:
- warm-call median seconds
- corrected replay discrepancy / RMSE
- residual parity
- iteration burden where meaningful

Secondary:
- warm-call mean/min/max
- compile + first-call time
- memory before/after
- descriptive TF32 timing if collected separately

## Expected failure modes
- latent prediction improves but corrected replay does not
- runtime improves only in tiny pilot cases, not in the real target rung
- heuristic matches learned closely enough that learned is not justified
- GPU/JIT overhead absorbs the potential gain

## What would change our mind
- If learned is correctness-preserving but not meaningfully faster than heuristic or cold, the retained-teacher neural route should remain unpromoted.
- If heuristic and learned tie, prefer heuristic until stronger evidence appears.

## Command template
```bash
# exact same benchmark command family as Phase 2, but now interpreted on runtime/correction metrics
--warmstart-mode none
--warmstart-mode heuristic
--warmstart-mode learned
```

## Interpretation rule
- Runtime or correction-burden gain is promotable only if correctness parity still holds.
- If the learned arm wins only on explanatory metrics, record that as narrow evidence rather than a promoted effectiveness result.
