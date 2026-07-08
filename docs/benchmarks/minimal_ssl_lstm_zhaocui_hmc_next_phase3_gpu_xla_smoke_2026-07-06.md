# Minimal SSL-LSTM Zhao-Cui HMC Next Phase 3 GPU/XLA Smoke

- Status: `passed`
- Artifact role: `trusted_gpu_xla_runtime_smoke`
- Filter: `zhaocui_fixed`
- Trusted approval recorded: `True`
- CUDA_VISIBLE_DEVICES: `0`
- GPU devices: `['/physical_device:GPU:0']`
- Initial log prob: `-1.3985848756201187`
- Initial score norm: `1.6247791059774361`
- HMC error: `None`
- Not-run reason: `None`
- Sample shape: `[2, 24]`
- Samples all finite: `True`
- Acceptance rate: `1.0`

## HMC Settings

- num_results: `2`
- num_burnin_steps: `1`
- step_size: `1e-05`
- num_leapfrog_steps: `1`
- seed: `[20260706, 3301]`
- use_xla: `True`
- jit_compile: `True`
- chain_execution_mode: `tf_function`
- trace_policy: `standard`
- adaptation_policy: `fixed_kernel_no_adaptation`
- target_scope: `minimal_ssl_lstm_zhaocui_hmc_ladder:zhaocui_fixed:phase1`
- trusted_gpu_xla_approval: `True`

## Hard Vetoes

- none

## Nonclaims

- Phase 3 trusted GPU/XLA launch smoke only
- not HMC convergence evidence
- not R-hat or ESS evidence
- not posterior correctness evidence
- not a method ranking or superiority claim
- not source-faithful SSL-LSTM Zhao-Cui parity evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not LEDH evidence

## Artifact Paths

- Plan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-master-program-2026-07-06.md`
- Subplan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase3-gpu-xla-smoke-subplan-2026-07-06.md`
- Result: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase3-gpu-xla-smoke-result-2026-07-06.md`
