# Phase 1 Result: Fixed-Variant Entry Point Inventory

Date: 2026-07-03

Status: `PASS_PHASE1_ENTRYPOINT_INVENTORY`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 1 passes. The fixed-variant Zhao-Cui SIR entrypoints exist and support a scoped local complete-data/component value and analytical/manual score. |
| Primary criterion status | Passed: the inventory classifies the route quantity as local complete-data/component, not full observed-data filtering. |
| Veto diagnostic status | Passed: the demoted retained-grid route is not needed; manual score methods exist; XLA/tape helper evidence is separated from leaderboard score provenance. |
| Main uncertainty | Phase 2 must decide whether this scoped local component appears as a scoped leaderboard cell under the existing SIR row or a separate scoped row. |
| Next justified action | Start Phase 2 row scope and evidence contract. |
| What is not being concluded | No full observed-data/filtering likelihood or score identity, no exact likelihood proof, no posterior correctness, and no universal GPU speed claim. |

## Inventory

| Surface | Location | Quantity | Leaderboard use |
| --- | --- | --- | --- |
| `parameterized_zhao_cui_sir_austria_model()` | `bayesfilter/highdim/models.py` and `bayesfilter/highdim/__init__.py` | Builds `ParameterizedZhaoCuiSIRSSM` over the SIR Austria d18 base model. | Eligible model factory for scoped fixed-variant row. |
| `initial_log_density_parameter_score` | `ParameterizedZhaoCuiSIRSSM` | Analytical/manual initial-density score; zero for this parameterization. | Eligible score component. |
| `transition_log_density_parameter_score` | `ParameterizedZhaoCuiSIRSSM` | Analytical/manual transition score through the fixed RK4 parameter Jacobian. | Eligible score component. |
| `observation_log_density_parameter_score` | `ParameterizedZhaoCuiSIRSSM` | Analytical/manual observation score for the log observation-noise scale. | Eligible score component. |
| `zhao_cui_sir_austria_local_complete_data_log_density_xla` | `bayesfilter/highdim/models.py` | XLA-oriented local complete-data scalar value. | Eligible value helper and GPU/XLA capability evidence, but its tape gradient is not the leaderboard score provenance. |
| `zhao_cui_sir_austria_batched_local_complete_data_log_density_xla` | `bayesfilter/highdim/models.py` | Batched XLA-oriented local complete-data scalar values. | Eligible batched/GPU capability evidence only under P91 scope. |
| `tests/highdim/test_p91_score_identity.py` | test harness | Empirical score-at-true check using manual score methods. | Primary score-provenance evidence. |
| `tests/highdim/test_p91_gpu_xla_local_target.py` | test harness | XLA helper parity and batched helper parity, including tape-gradient parity diagnostics. | Capability/parity evidence only; do not cite as manual leaderboard score provenance. |

## Scope Classification

The eligible quantity is:

```text
local_complete_data_zhao_cui_sir_d18_component
```

It is conditioned on a fixed latent state path and observation path. It is not
the full observed-data/filtering likelihood for the SIR row.

The eligible score coordinate system is:

```text
theta = (log_kappa_scale, log_nu_scale, log_obs_noise_scale)
```

The eligible score provenance is:

```text
zhao_cui_sir_d18_local_complete_data_manual_parameter_score_methods
```

The XLA helper provenance is value/capability provenance only:

```text
zhao_cui_sir_d18_local_complete_data_xla_value_helper
```

## Local Checks

Commands:

```bash
rg -n "zhao_cui_sir_austria|ParameterizedZhaoCuiSIRSSM|parameter_score|score_for|local_complete|log_density|scaled_model|simulate" bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py tests/highdim/test_p91_score_identity.py tests/highdim/test_p91_batched_score_api.py tests/highdim/test_p91_gpu_xla_local_target.py scripts/p91_performance_benchmark.py scripts/p91_hmc_smoke.py
sed -n "1,260p" tests/highdim/test_p91_score_identity.py
sed -n "1,260p" tests/highdim/test_p91_batched_score_api.py
sed -n "1,260p" tests/highdim/test_p91_gpu_xla_local_target.py
sed -n "920,1175p" bayesfilter/highdim/models.py
sed -n "1335,1420p" bayesfilter/highdim/models.py
sed -n "1,190p" scripts/p91_performance_benchmark.py
sed -n "45,120p" scripts/p91_hmc_smoke.py
rg -n "parameterized_zhao_cui_sir|local_complete_data|transition_log_density_parameter_score|observation_log_density_parameter_score|initial_log_density_parameter_score|zhao_cui_sir_austria_local_complete_data_log_density_xla|zhao_cui_sir_austria_batched_local_complete_data_log_density_xla" bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py tests/highdim/test_p91_score_identity.py tests/highdim/test_p91_gpu_xla_local_target.py
git diff --check -- docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-*.md
```

Outcome:

- Entry point and export `rg` checks passed.
- Manual score harness inspection passed.
- XLA helper inspection passed.
- Current leaderboard sidecar/blocking tests were located for Phase 2/3
  contract update.
- `git diff --check` over current program artifacts passed.

## Phase 2 Handoff

Phase 2 may start because:

- the eligible fixed-variant value and score quantity is classified;
- the correct leaderboard gradient source is the manual score method family;
- existing P91 XLA/tape evidence is classified as capability evidence only;
- no retained-grid production route is required.

Phase 2 must decide the row/cell scope before runner edits.
