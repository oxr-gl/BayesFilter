# BayesFilter HMC Kernel Tuning XLA Parameter Repair Result

Date: 2026-06-22

Status: `passed_focused_checks`

Plan:

- `docs/plans/bayesfilter_hmc_kernel_tuning_xla_parameter_repair_plan_2026_06_22.md`

## Objective

Allow the generic BayesFilter one-call HMC kernel tuning path to select either
non-XLA or XLA HMC execution through an explicit `use_xla` parameter while
keeping XLA authority fail-closed.

## Changes

- Added `use_xla: bool = False` to:
  - `HMCBootstrapScreenConfig`;
  - `HMCWindowedMassStageConfig`;
  - `HMCFixedMassStepStageConfig`;
  - `HMCFrozenStepTrajectoryStageConfig`;
  - `HMCTuneVerifyRepairLoopConfig`;
  - `HMCKernelTuningConfig`.
- Included `use_xla` in config payloads and public-to-internal Phase 7 handoffs.
- Replaced generic tuning hard-coded `use_xla=False` with `use_xla=config.use_xla`
  in bootstrap, windowed mass, fixed-mass step, frozen-step trajectory, and
  final verification HMC configs.
- Updated the latent fixed-mass wrapper so it preserves accepted full-chain XLA
  authority from the base adapter when target scope matches, and remains
  non-XLA for unauthorized or mismatched-scope adapters.
- Adjusted the public nonclaim wording so XLA execution is treated as runtime
  selection, not as a broad GPU/readiness claim.

## Checks

Compile:

```bash
env PYTHONPYCACHEPREFIX=/tmp/bayesfilter_pycache_xla_repair \
  python -m py_compile \
  /home/ubuntu/python/BayesFilter/bayesfilter/inference/hmc_kernel_tuning.py
```

Result: passed.

Focused tests:

```bash
env PYTHONPYCACHEPREFIX=/tmp/bayesfilter_pycache_xla_repair \
  PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=. \
  /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_hmc_kernel_tuning_bootstrap.py \
  tests/test_hmc_kernel_tuning_windowed_mass.py \
  tests/test_hmc_kernel_tuning_fixed_mass_step.py \
  tests/test_hmc_kernel_tuning_frozen_step_trajectory.py \
  tests/test_hmc_kernel_tuning_outer_loop.py \
  tests/test_hmc_kernel_tuning_public_api.py
```

Result: `80 passed, 1 skipped, 47 warnings in 10.85s`.

Import/config smoke:

```bash
env PYTHONPYCACHEPREFIX=/tmp/bayesfilter_pycache_xla_repair \
  PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 \
  PYTHONPATH=/home/ubuntu/python/BayesFilter \
  /home/ubuntu/anaconda3/envs/tfgpu/bin/python - <<'PY'
from bayesfilter.inference import HMCKernelTuningConfig
cfg = HMCKernelTuningConfig.standard(target_scope="scope", use_xla=True)
print({
    "use_xla": cfg.use_xla,
    "chain_execution_mode": cfg.chain_execution_mode,
    "payload_use_xla": cfg.payload()["use_xla"],
})
PY
```

Result: `{'use_xla': True, 'chain_execution_mode': 'tf_function', 'payload_use_xla': True}`.

BayesFilter/MacroFinance local-HMC import audit:

```bash
rg -n "(^|[^A-Za-z0-9_])(from|import) +(filters|inference\.(hmc|hmc_diagnostics|hmc_performance|mass_matrix|posterior_adapter))" \
  cross_country_multi_asset_macro_mixed_frequency_hmc_kernel_tuning.py \
  cross_country_multi_asset_macro_mixed_frequency_target.py \
  /home/ubuntu/python/BayesFilter/bayesfilter/inference/hmc_kernel_tuning.py
```

Result: no hits.

## Evidence Contract Status

| Item | Status |
| --- | --- |
| Default non-XLA behavior | Passed: configs default to `use_xla=False`. |
| Explicit XLA parameter | Passed: `use_xla=True` propagates through public, stage, loop, and full-chain config payloads. |
| Fail-closed XLA authority | Passed: wrapper preserves full-chain XLA authority only from accepted, matching-scope base authority; unauthorized/mismatched adapters remain non-XLA. |
| HMC mechanics exposure | Passed: no step size, leapfrog count, budget schedule, mass window schedule, or draw count added as public inputs. |
| Local MacroFinance HMC runtime | Passed: no active local-HMC import hits in the audited path. |

## Nonclaims

This result does not claim posterior convergence, sampler superiority,
performance improvement, GPU readiness, scientific validity, or default
readiness. It only establishes that generic BayesFilter HMC kernel tuning can
now request XLA execution when the adapter has already supplied reviewed
full-chain XLA authority.

## Handoff

MacroFinance can now wire `HMCKernelTuningConfig(..., use_xla=True,
chain_execution_mode="tf_function")` for the CCMA macro mixed-frequency wrapper,
but the model adapter must advertise accepted full-chain XLA authority. The
current Phase 2 augmented adapter should be checked before rerunning Phase 10c;
if it does not expose `value_score_capability()` with
`full_chain_xla_diagnostic_ready=True`, BayesFilter will correctly fail closed.
