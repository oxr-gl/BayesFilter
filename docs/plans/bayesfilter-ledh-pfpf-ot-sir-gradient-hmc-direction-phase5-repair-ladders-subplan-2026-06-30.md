# Phase 5 Subplan: Per-Budget Process-Isolation Repair

Date: 2026-06-30

Status: `DRAFT_READY_FOR_REVIEW`

## Phase Objective

Repair the Phase 4 exit-137 memory blocker by running the same material SIR
gradient diagnostic one Sinkhorn budget per trusted GPU/XLA/TF32 Python
process, then aggregating completed per-budget artifacts under the frozen Phase
1 HMC-direction gate.

The goal is not to broaden the scientific claim.  The goal is to obtain the
first complete material artifact, or a sharper memory/runtime blocker, without
changing the estimator, comparator, route, or gate.

## Entry Conditions Inherited From Previous Phase

- Phase 4 route launch was correct: GPU was visible, XLA initialized for CUDA,
  and the manual route compiled.
- Phase 4 complete material artifact was blocked by exit code 137 during
  budget 100 in a monolithic process, even after the reviewed exact chunking
  repair `--seed-microbatch-size 1` and `--theta-offset-batch-size 2`.
- Phase 4 partial budget-10 progress is explanatory only and must be
  regenerated as a complete per-budget artifact before being used in the gate.
- The Phase 1 gate remains frozen.
- The repaired diagnostic must remain GPU/XLA/TF32; CPU evidence is not
  material.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-result-2026-06-30.md`
- Per-budget wrappers or a wrapper-generator script under `scripts/`.
- Per-budget JSON outputs:
  - `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.json`
  - `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget100-2026-06-30.json`
  - optional only after budget 100 completes:
    `...phase5-budget200-2026-06-30.json`
  - optional only after budget 200 completes:
    `...phase5-budget400-2026-06-30.json`
- Per-budget Markdown outputs with matching names.
- Aggregated Phase 5 summary JSON/Markdown if at least budgets 10 and 100
  complete.
- Updated Phase 6 subplan.

## Required Checks, Tests, And Reviews

Local checks before material execution:

```bash
bash -n <new phase5 wrapper>
python -m py_compile docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
```

Claude read-only review is required before material execution.  Review scope:

- Phase 5 subplan;
- new wrapper(s);
- the Phase 4 blocker result.

Material execution, one budget at a time, with escalation:

```bash
bash <phase5 wrapper for budget 10>
bash <phase5 wrapper for budget 100>
```

Only run budget 200 after budget 100 completes and the local result review says
the next budget remains necessary and feasible.  Only run budget 400 after
budget 200 completes under the same rule.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does process isolation remove the Phase 4 memory blocker enough to classify SIR gradient direction at budgets 10 and 100 under the frozen gate? |
| Baseline/comparator | Same fixed seeds, theta, FD offsets, raw-theta regression, route prerequisites, exact chunking knobs, and gate as repaired Phase 4; only the process boundary changes. |
| Primary criterion | Budgets 10 and 100 each produce complete JSON/Markdown artifacts with route prerequisites passing and direction summaries classified by the Phase 1 gate, or a sharper blocker is written. |
| Veto diagnostics | CPU route, non-XLA, TF32 disabled, GPU outputs missing, missing MCSE/FD SE, row residual violation for any claimed pass, nonfinite outputs, exit 137, or changed thresholds. |
| Explanatory diagnostics | Row residual trend, max FD z, max combined z, relative error, R2, runtime, memory behavior, and whether budget 100 changes the direction classification relative to budget 10. |
| Not concluded | No HMC readiness, no posterior correctness, no global production budget, no nonlinear-model generalization, no finite-N conclusion. |

## Forbidden Claims And Actions

- Do not treat Phase 4 partial progress as a completed gate result.
- Do not change the Phase 1 gate.
- Do not change seeds, theta, FD offsets, `--seed-microbatch-size 1`,
  `--theta-offset-batch-size 2`, dtype, TF32 mode, compiler mode, or transport
  gradient mode while claiming same-comparator evidence.
- Do not run budget 200 or 400 if budget 100 already fails with exit 137 or if
  budgets 10/100 already provide a discriminating blocker.
- Do not use CPU fallback as material evidence.
- Do not claim process isolation improves numerical correctness; it only
  addresses runtime memory accumulation.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 if:

- budgets 10 and 100 complete and the result either classifies the SIR gradient
  under the frozen gate or identifies the next smallest reviewed mechanism; or
- budget 100 still blocks with exit 137 or another runtime failure and the
  result records that per-budget isolation did not remove the memory blocker.

Remain in Phase 5 only if:

- budgets 10 and 100 complete but the result specifically requires budget 200
  to discriminate Sinkhorn-budget behavior, and resource checks show budget 200
  is feasible.

## Stop Conditions

- A per-budget run exits 137 or exhausts memory/swap.
- A per-budget artifact lacks route prerequisite fields or cannot be parsed.
- Claude review finds a material flaw that does not converge within five
  rounds.
- Further execution would require changing the estimator, comparator, or
  frozen gate.

## End-Of-Phase Close Protocol

1. Run required local checks.
2. Run reviewed per-budget material checks until a handoff or stop condition is
   reached.
3. Write the Phase 5 result.
4. Draft or refresh Phase 6 subplan.
5. Review Phase 6 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
