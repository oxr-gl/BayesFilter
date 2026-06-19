# P66 Phase 0 Subplan: Governance, Baseline, And Planning Basis

metadata_date: 2026-06-15
status: DRAFT_REVISED_AFTER_R1
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p66-fixed-branch-validation-ladder-master-program-2026-06-15.md
phase: 0
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Establish the P66 launch baseline and the planning basis for treating the old
P60 low/high closeness gate as an unfair primary convergence gate for the
current SIR fixed-HMC target.

Phase 0 is governance and evidence framing only.  It must not change code.

## Entry Conditions Inherited From Previous Phase

- P65 closed with
  `P65_FIXED_BRANCH_ZERO_TT_REPAIR_PASSED_WITH_RESIDUAL_THRESHOLD_BLOCKERS`.
- The high `(degree=1, rank=2)` branch has positive square-root mass at both
  steps and no defensive-only steps.
- The old P60 comparator still blocks on:
  - `log_marginal_delta_threshold_exceeded`;
  - `normalizer_increment_delta_threshold_exceeded`.
- The current worktree contains unrelated dirty changes.  P66 must preserve
  them.

## Required Artifacts

- This Phase 0 subplan.
- P66 master program.
- P66 visible runbook.
- P66 Claude review ledger.
- P66 visible execution ledger.
- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase0-governance-baseline-result-2026-06-15.md`.
- Refreshed Phase 1 subplan if Phase 0 passes.

## Required Checks/Tests/Reviews

- Local file/context inspection of:
  - P65 closeout result;
  - P65 final handoff;
  - current P60 comparator code.
- Compile/import check for currently touched highdim surfaces:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/fitting.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

- Fresh CPU-only JSON baseline probe for the pinned tuple:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -c 'import json; import bayesfilter.highdim as h; r=h.p60_author_sir_same_route_rank_comparator(sample_count=1, fit_sample_count=2, low_fit_degree=0, high_fit_degree=1, low_fit_rank=1, high_fit_rank=2); m=r.manifest; rows=m["sqrt_tt_core_diagnostics"]["candidate_high"]; d=m["normalizer_decomposition"]; out={"p66_phase0_status_candidate":"WARN_SENTINEL_BRANCH_DIFFERS_FROM_CANDIDATE","p60_status":r.status,"p60_blockers":r.blockers,"high_sqrt_square_normalizers":[x["sqrt_square_normalizer"] for x in d["candidate_high"]],"high_defensive_only_steps":d["candidate_high_defensive_only_steps"],"high_core_norm_ranges":[[x["core_norm_min"],x["core_norm_max"]] for x in rows],"high_near_zero_core_counts":[x["near_zero_core_count"] for x in rows],"old_low_high_deltas":{"log_marginal_abs_delta":m["log_marginal_abs_delta"],"normalizer_increment_abs_deltas":m["normalizer_increment_abs_deltas"],"thresholds":m["thresholds"]},"source_invariants":m["source_invariants"],"cpu_only_intent":"CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp"}; print(json.dumps(out, indent=2, sort_keys=True))'
```

The probe must print:

- high square-root normalizers;
- high defensive-only steps;
- high core norm ranges;
- old P60 blockers and deltas;
- source invariants;
- sentinel classification candidate.

CPU-only is intentional in Phase 0.  Commands must set
`CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp` before framework import and the
result artifact must record that this is a CPU-only governance baseline, not
GPU evidence.

- Bounded Claude review of P66 plan artifacts before Phase 0 launch.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is P66 correctly scoped to replace the old low/high closeness gate as a primary convergence gate, rather than relaxing thresholds or hiding residual evidence? |
| Baseline/comparator | P65 closeout and fresh P66 probe of the pinned tuple: low `(degree=0, rank=1)`, high `(degree=1, rank=2)`, `sample_count=1`, `fit_sample_count=2`. |
| Primary pass criterion | The fresh probe reproduces P65 state: high branch noncollapsed, old P60 blocks only on quantitative low/high deltas, and the Phase 1 handoff demotes the old comparison to sentinel/explanatory status. If the fresh probe does not reproduce this state, Phase 0 stops for rebaseline. |
| Veto diagnostics | High branch defensive-only again; source-route invariants drift; old thresholds weakened; Phase 0 proposes code changes; the sentinel gap is hidden; d=18 correctness is claimed. |
| Explanatory diagnostics | Old P60 deltas, normalizer increments, square-root mass, core norm ranges, sentinel low/high difference, CPU-only TensorFlow warnings. |
| Not concluded | No implementation change, no new validation ladder yet, no d=18 correctness, no adaptive parity, no HMC readiness. |

## Forbidden Claims/Actions

- Do not modify code in Phase 0.
- Do not weaken or reinterpret P60 thresholds.
- Do not call the old P60 comparator a full pass.
- Do not claim source-faithful Zhao--Cui behavior for fixed-HMC adaptation.
- Do not claim d=18 correctness.
- Do not launch detached or background execution.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- Phase 0 review converges;
- compile/import passes;
- the fresh probe confirms high branch noncollapse and old residual threshold
  blockers;
- the Phase 0 result explicitly states that `(0,1)` vs `(1,2)` closeness is
  sentinel/explanatory only for this target;
- Phase 1 subplan is refreshed around validation-contract/API design, not
  implementation-first coding.

## Stop Conditions

- Fresh probe contradicts P65 closeout in a way that changes the baseline.
- Fresh probe does not reproduce the fixed-branch admissibility picture from
  P65; stop and rebaseline before Phase 1.
- High branch is defensive-only again.
- Source-route invariants drift before P66 changes.
- Claude identifies an unresolved material planning flaw after five rounds.
- Continuing would require code changes before Phase 1 design.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 0 result or blocker.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
