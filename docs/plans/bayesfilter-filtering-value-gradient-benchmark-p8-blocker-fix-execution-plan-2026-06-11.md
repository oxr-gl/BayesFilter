# P8 Blocker Fix Execution Plan

metadata_date: 2026-06-11
status: CODEX_DRAFT_PENDING_CLAUDE_REVIEW

## Role Contract

| Role | Agent |
| --- | --- |
| Supervisor and executor | Codex in this dialogue |
| Read-only critical reviewer | Claude Code, opus, max effort |
| Detached Codex agent | Not allowed |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Which Phase 8 blockers can be repaired now, and which remaining blockers require source evidence or full numeric benchmark execution before the filtering benchmark can close? |
| Baseline/comparator | Current P8 blocker-closure manifest, P8-B2 synthetic dataset result, source-paper scope contract, generalized-SV testing spec, P58/P59 SIR source-route ledgers, and focused Phase 8 tests. |
| Primary criterion | Emit reviewed, machine-readable blocker-fix gates for B3 horizon policy, B4 stochastic seed policy, and B5 source-row adapter status; regenerate the central blocker manifest; preserve row-level hard blocks for LGSSM `C`, generalized-SV estimates, and SIR d=18 source-route assembly. |
| Veto diagnostics | P44 diagnostic rows re-enter promoted source-paper scope; source-paper values are replaced by project fixtures; generalized-SV author defaults or SP500 returns are used as benchmark truth/data; Octave/NumPy is substituted for MATLAB `rng(0); rand(3,3)`; B3/B4 protocol gates are claimed as numeric calibration results; DPF filters are ranked before MC uncertainty is measured; old LEDH-PFPF-OT results are used as current evidence; old local/operator/all-grid SIR route is used as source-route evidence. |
| Explanatory-only diagnostics | Protocol readiness, status matrices, finite dataset summaries, no-silent-hole adapter ledgers, focused tests, compile checks, and Claude read-only comments. |
| Not concluded even if this plan passes | No filter ranking, no full numeric value/score/curvature benchmark, no generalized-SV numeric readiness, no exact LGSSM source dataset until the MATLAB `C` matrix is materialized, no SIR d=18 validation, no Bayesian-estimation handoff, and no universal DPF gradient certification. |
| Result artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-execution-result-2026-06-11.md` plus the JSON/CSV/Markdown gate artifacts emitted by this plan. |

## Skeptical Plan Audit

Initial audit status: `PASS_FOR_BOUNDED_BLOCKER_FIX_EXECUTION_PENDING_CLAUDE`.

- Wrong baseline risk: controlled by using only source-paper promoted or replacement rows from the 2026-06-11 source-scope contract.
- Proxy metric risk: controlled by labeling B3/B4 as protocol gates unless and until numeric likelihood/score and MC-SE outputs are emitted.
- Missing stop conditions: every gate has pass, partial-pass, and block tokens; only missing source evidence, failed tests, failed Claude review, or nonfinite generated artifacts may block execution.
- Unfair comparison risk: UKF, SVD, CUT4, Zhao-Cui, bootstrap DPF, and Algorithm-1 LEDH-PFPF are not declared invalid for nonlinear/non-Gaussian models; they are marked adapter-pending or value/score-pending. Kalman is exact only for LGSSM and mixture/surrogate-only where explicitly declared.
- Hidden assumption risk: gradient and Hessian cells must carry coordinate/provenance status; value-only and diagnostic-only cells are allowed but must be explicit.
- Stale context risk: P59-9a is preparation evidence only; it does not close P59-9b through P59-9e.
- Artifact adequacy risk: the execution must add focused tests that rerun the emitters and check no silent holes.

## Blocker Repair Phases

| Phase | Blocker | Execution action | Pass or partial token | Block token |
| --- | --- | --- | --- | --- |
| P8-F0 | Plan review | Claude reviews this plan before implementation. | `PASS_P8_BLOCKER_FIX_PLAN_REVIEW` | `BLOCK_P8_BLOCKER_FIX_PLAN_REVIEW` |
| P8-F1 | B3 horizon calibration | Emit source-horizon and long-run variance protocol gate for source-paper rows. This is not numeric calibration unless likelihood/score runs are present. | `PASS_P8_B3_HORIZON_PROTOCOL_READY_NUMERIC_PENDING` | `BLOCK_P8_B3_HORIZON_PROTOCOL` |
| P8-F2 | B4 stochastic calibration | Emit DPF seed-ladder and MC-SE/data-SE promotion gate. Ranking remains disabled until measured MC-SE exists. | `PASS_P8_B4_STOCHASTIC_PROTOCOL_READY_NUMERIC_PENDING` | `BLOCK_P8_B4_STOCHASTIC_PROTOCOL` |
| P8-F3 | B5 adapter closure | Emit a source-row x algorithm adapter status matrix with no silent holes and explicit value/score/curvature readiness. | `PASS_P8_B5_ADAPTER_STATUS_MATRIX_READY_NUMERIC_PENDING` | `BLOCK_P8_B5_ADAPTER_STATUS_MATRIX` |
| P8-F4 | Hard source gates | Preserve LGSSM MATLAB `C`, generalized-SV estimated-values, and SIR P59-9b..9e blockers as row-level blocks. | `PASS_P8_SOURCE_BLOCKS_PRESERVED` | `BLOCK_P8_SOURCE_BLOCKS_MISCLASSIFIED` |
| P8-F5 | Central manifest refresh | Regenerate P8 blocker-closure status from the new gate artifact. | `PASS_P8_BLOCKER_CLOSURE_STATUS_MANIFEST_WITH_REMAINING_BLOCKERS` | `BLOCK_P8_STATUS_REGENERATION` |
| P8-F6 | Execution review | Claude reviews the execution artifacts; Codex repairs review findings until convergence or five iterations. | `PASS_P8_BLOCKER_FIX_EXECUTION_REVIEW` | `BLOCK_P8_BLOCKER_FIX_EXECUTION_REVIEW` |

## Hard Blocks That Must Not Be Papered Over

| Row/block | Current blocker | Accepted unblock route |
| --- | --- | --- |
| LGSSM source row | `BLOCK_P8_B2_LGSSM_AUTHOR_C_MATRIX_PENDING` | Materialize the exact MATLAB `rng(0); rand(3,3)` matrix from MATLAB or a checked source artifact. Octave/NumPy substitutes are forbidden. |
| Generalized SV | `BLOCK_GENERALIZED_SV_NUMERIC_RUN_ESTIMATED_VALUES_PENDING` | Use a checked reported estimate, a reviewed digitized estimate with uncertainty, or rerun the author SP500 pipeline and export the posterior/weighted samples. Author defaults are forbidden as estimates. |
| Spatial SIR d=18 | `BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE` | Complete P59-9b through P59-9e: source-route step specs, comparator-tier manifest, route/preconditioner decision, bounded runner path, and validation ladder. |
| Full numeric P8 | `BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN` | Run reviewed value, score, curvature, failure, and stochastic uncertainty tables on the promoted source-paper rows after the row-level preconditions and adapters are ready. |

## Commands

Planned CPU-only commands:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_p8_blocker_fix_gates.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_p8_blocker_closure.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_generalized_sv_spec.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py tests/highdim/test_p58_m9_source_route_pipeline_readiness.py tests/highdim/test_p59_author_sir_36d_target_fit.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_p8_blocker_fix_gates.py scripts/filtering_value_gradient_benchmark_emit_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py
git diff --check -- scripts/filtering_value_gradient_benchmark_emit_p8_blocker_fix_gates.py scripts/filtering_value_gradient_benchmark_emit_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-execution-plan-2026-06-11.md
```

Claude review uses:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name p8-blocker-fix-review --model opus --effort max "<bounded prompt>"
```

If Claude does not respond, run a minimal probe. If the probe responds, shorten and redesign the prompt.

## Nonclaims

- This plan is not a numeric benchmark result.
- This plan does not rank filters.
- This plan does not certify DPF gradients.
- This plan does not unblock generalized SV without materialized estimates.
- This plan does not unblock the source LGSSM row without the exact MATLAB `C` matrix.
- This plan does not close SIR d=18 source-route validation from P59-9a alone.
