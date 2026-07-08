# Minimal SSL-LSTM Zhao-Cui HMC Ladder Phase 2 Canary

- Status: `passed`
- Artifact role: `tiny_hmc_canary_debug_reference`
- Filter: `zhaocui_fixed`
- Initial log prob: `-1.3985848756201187`
- Initial score norm: `1.624779105977436`
- Initial score shape: `[24]`
- HMC error: `None`
- Sample shape: `[2, 24]`
- Samples all finite: `True`
- Acceptance rate: `1.0`
- Nonfinite sample count: `0`
- Divergence status: `not_exposed_by_kernel`
- Divergence count: `None`

## HMC Settings

- num_results: `2`
- num_burnin_steps: `1`
- step_size: `1e-05`
- num_leapfrog_steps: `1`
- seed: `[20260706, 2201]`
- use_xla: `False`
- jit_compile: `False`
- chain_execution_mode: `tf_function`
- trace_policy: `standard`
- adaptation_policy: `fixed_kernel_no_adaptation`
- target_scope: `minimal_ssl_lstm_zhaocui_hmc_ladder:zhaocui_fixed:phase1`

## Hard Vetoes

- none

## Nonclaims

- Phase 2 tiny HMC canary only
- CPU-hidden non-JIT debug/reference exception only
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
- Subplan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase2-cpu-hidden-canary-subplan-2026-07-06.md`
- Result: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase2-cpu-hidden-canary-result-2026-07-06.md`
