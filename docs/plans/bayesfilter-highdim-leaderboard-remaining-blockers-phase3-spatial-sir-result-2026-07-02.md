# Phase 3 Result: Spatial SIR Full Observed-Data Filtering Route

Date: 2026-07-02

Status: `BLOCK_PHASE3_SIR_FULL_FILTERING_THETA_BINDING_UNAVAILABLE`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Keep the Zhao-Cui spatial SIR main leaderboard cell blocked for full observed-data/filtering value+score admission. |
| Primary criterion status | Failed by target/theta contract, not by an implementation crash: no reviewed full observed-data/filtering free-theta binding exists for this row. |
| Veto diagnostic status | Veto triggered: the generated source-scope SIR row declares `truth_theta_coordinate: no_free_theta`, and P91 local complete-data evidence is sidecar-only. |
| Main uncertainty | Whether the project wants a new reviewed full-row SIR theta contract based on the existing P8p/P79 parameterized surface. |
| Next justified action | Advance to Phase 4 UKF cleanup; treat a full SIR theta-binding repair as a separate reviewed target-contract phase. |
| What is not being concluded | No claim that SIR analytical components are useless, no claim that the problem is unsolvable, no full observed-data/filtering likelihood or score correctness claim, no HMC/GPU/production readiness claim. |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Can `zhao_cui_spatial_sir_austria_j9_T20` be repaired from P91 sidecar status to full observed-data/filtering value/manual-score status? |
| Baseline/comparator | July 1 leaderboard plus P91 local complete-data sidecar evidence. |
| Primary criterion | Finite full filtering value and manual score with a reviewed theta binding, or precise blocker. |
| Outcome | Precise blocker. The full-row theta binding is unavailable. |
| Veto diagnostics | `no_free_theta` dataset contract and sidecar-only P91 evidence veto score admission. |
| Explanatory diagnostics | P8p/P79/P91 analytical local-component score tests remain relevant sidecar evidence only. |
| Artifact | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-zhaocui-row-2026-07-02.json` |

## Phase 3 Findings

The SIR row is not blocked because all SIR analytical-gradient machinery is
missing. The codebase has `ParameterizedZhaoCuiSIRSSM`, including analytical
local transition and observation density score methods for the P8p/P79/P91
three-parameter surface:

- `log_kappa_scale`;
- `log_nu_scale`;
- `log_obs_noise_scale`.

That evidence is not enough to admit the main Zhao-Cui spatial SIR leaderboard
cell. The generated row contract in
`scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py::_sir_dataset`
still declares:

```text
truth_theta_coordinate = no_free_theta
truth_theta = []
```

The July 1 leaderboard also classifies the Zhao-Cui SIR main row as
`blocked_full_filtering_evaluator_pending_p91_local_component_ready`. Its P91
payload explicitly scopes the available score identity, GPU/XLA, batch, and HMC
smoke evidence to the local complete-data SIR d18 component, not to the full
observed-data/filtering leaderboard row.

## Row-Local Result

Row-local artifact:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-zhaocui-row-2026-07-02.json`

Recorded status:

- `comparison_status`: `blocked_or_status_only`
- `numeric_execution_status`: `blocked_full_filtering_theta_binding_unavailable`
- `theta_binding_status`: `blocked_no_reviewed_full_observed_data_filtering_theta_binding`
- `score_at_true_calibration_status`: `skipped_binding_unavailable`

## Checks

Phase 3 preflight checks run before this closeout:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p91_gpu_xla_local_target.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

Result: `12 passed, 2 warnings`.

Blocker-path boundary check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py -k "sir or p91"
```

Result before closeout: `1 passed, 9 deselected`.

Additional closeout checks are recorded in the execution ledger after this
result is written.

## Boundary Safety

This phase intentionally does not:

- report P91 local complete-data evidence as the full observed-data/filtering
  row;
- admit autodiff or finite-difference score provenance;
- invent a free theta for a row whose reviewed dataset contract says
  `no_free_theta`;
- run GPU/XLA/HMC readiness checks for the full row;
- regenerate the all-row leaderboard.

## Phase 4 Handoff

Phase 4 may start with SIR precisely blocked. The next phase should focus on
UKF analytical-score cleanup for rows whose value route exists but whose score
status is value-only or non-admitted. Any future SIR repair should begin by
reviewing and approving a full observed-data/filtering target and theta-binding
contract before implementation.
