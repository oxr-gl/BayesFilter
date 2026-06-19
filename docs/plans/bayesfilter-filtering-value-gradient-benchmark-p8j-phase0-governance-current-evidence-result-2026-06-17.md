# P8j Phase 0 Result: Governance And Current Evidence Audit

metadata_date: 2026-06-17
status: PASS
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 0
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Advance to Phase 1 callback contract. |
| Primary criterion status | Passed.  Local evidence shows SIR d18 DPF remains missing while P8j is scoped to that gap. |
| Veto diagnostic status | No veto fired.  No P71/monograph drift, no actual-SV evidence promoted to SIR evidence, no score/Hessian/theta-gradient/HMC/NUTS claim. |
| Main uncertainty | Phase 0 does not prove SIR DPF callbacks are correct or executable; that is Phase 1/2/3/4 work. |
| Next justified action | Draft and review Phase 1 SIR d18 DPF callback contract. |
| What is not concluded | No SIR d18 bootstrap DPF result, no LEDH-PFPF-OT result, no particle-count adequacy, no leaderboard refresh, no HMC readiness. |

## Evidence Summary

The P8d reset memo preserves the exact gap:

- DPF route callbacks existed for LGSSM, raw SV, predator-prey, and generalized SV.
- Spatial SIR gradients remained `not_applicable_no_free_theta`.
- Spatial SIR DPF callback remained a structured callback gap unless implemented later.
- DPF score/Hessian was not certified and must not be fabricated.

The current P8d runner preserves the target row:

- `SIR_ROW = "zhao_cui_spatial_sir_austria_j9_T20"`;
- `ROW_HORIZONS[SIR_ROW] = 20`;
- `_sir_structural()` builds a fixed-parameter 18-state, 9-observation structural route;
- `_dpf_route()` admits LGSSM, actual SV, predator-prey, and generalized SV, but raises `ValueError(f"no DPF callback route for {row_id}")` for SIR;
- `_has_dpf_route(row_id)` returns true only for LGSSM, actual SV, predator-prey, and generalized SV.

The current route test preserves the same mechanical boundary:

- `assert not p8d._has_dpf_route(SIR_ROW)`;
- SIR deterministic value-only cells preserve `score_adapter_status == "not_applicable_no_free_theta"`;
- SIR deterministic value-only cells preserve `hessian_adapter_status == "not_applicable_no_free_theta"`.

P8g/P8h/P8i are historical non-SIR DPF/LEDH/OT provenance only:

- P8g Phase 5 identified Spatial SIR callbacks as a closure target and forbade unreviewed Spatial SIR LEDH execution.
- P8h/P8i repaired and tested the serious route on the actual scalar-SV row, not SIR d18.

## Local Checks

Commands run:

```bash
rg -n "P8j|SIR d18|zhao_cui_spatial_sir_austria_j9_T20|not the Zhao-Cui fixed-branch/P71 lane|no free theta|five fixed seeds" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-*
rg -n "SIR_ROW|def _dpf_route|def _has_dpf_route|no DPF callback route|_sir_structural|zhao_cui_spatial_sir_austria_j9_T20" scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-subplan-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-gated-execution-runbook-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md
```

Results:

- P8j artifact text search: passed.
- P8d runner/test route search: passed.
- `git diff --check`: passed.

## Claude Review

Claude review iteration 1 returned `VERDICT: REVISE` for fixable provenance
and gating issues.  Patches made:

- P8d reset memo plus current runner/tests are now primary missing-route
  baseline.
- P8g/P8h/P8i are now historical non-SIR DPF/LEDH/OT provenance only.
- Phase 6 now requires Phase 5-reviewed selected SIR d18 particle count plus
  five fixed seeds; five seeds are necessary but not sufficient.
- Execution ledger and stop handoff now include explicit artifact/review
  pointers.

Claude review iteration 2 returned `VERDICT: AGREE`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Recorded by later run artifacts; Phase 0 used local source inspection only. |
| Dirty state | Repository had substantial pre-existing dirty/untracked work outside P8j; Phase 0 edited only P8j plan artifacts. |
| Commands | Local `rg`, `sed`, `git diff --check`, and Claude read-only worker review. |
| Environment | Local repo, no GPU command, no numerical DPF run. |
| CPU/GPU status | N/A; no compute run. |
| Data version | Current local P8d synthetic/source-scope artifacts. |
| Seeds | N/A; no stochastic run. |
| Wall time | N/A. |
| Output artifacts | This result, updated execution ledger, updated Claude review ledger, updated stop handoff, Phase 1 subplan. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-result-2026-06-17.md` |

## Handoff

Phase 1 may proceed only as a callback-contract phase.  It must not launch
SIR DPF numerics.  It must define the exact TensorFlow callback route for
bootstrap DPF and Algorithm 1 UKF LEDH on SIR d18, including observation
Jacobian, Gaussian observation density, process-noise policy, shape contracts,
metadata, and tests.
