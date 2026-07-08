# Visible Stop Handoff: Minimal SSL-LSTM Zhao-Cui HMC Validity Gaps

Date: 2026-07-06

Status: `PHASE4_REVIEW_PENDING`

## Current State

Phase 0 governance, Phase 1 oracle design, and Phase 2 conditional-slice oracle
implementation passed. Phase 2 JSON status is `passed`, with no hard vetoes,
no conditional-slice edge-mass failures, max target/reference relative error
`8.881784197001252e-16`, and finite-difference score max absolute error
`9.438116954640918e-11`.

Phase 3 longer trusted GPU/XLA HMC diagnostic has executed with approval. The
trusted rerun superseded an initial non-trusted GPU-visibility blocker artifact.
The final Phase 3 JSON status is `passed`, with continuation vetoes `[]`, sample
shape `[64, 4, 24]`, finite samples, GPU `/physical_device:GPU:0`,
`use_xla=True`, and `jit_compile=True`.

The Phase 3 promotion screen failed:

- split R-hat threshold failed, max `2083851.3177999416`;
- cross-chain ESS threshold failed, min `4.000003545362901`;
- native divergence telemetry was `not_exposed_by_kernel`;
- sampled-state target/reference check passed with max absolute error
  `4.440892098500626e-16`.

Interpretation: Phase 3 produced a valid artifact and rejects only the current
fixed-kernel sampler setting. It does not reject the target or the research
direction.

Claude review remains blocked by the escalation reviewer for private repository
context transfer. The Phase 3 subplan was reviewed by a fresh visible Codex
substitute reviewer with `VERDICT: AGREE`.

## Resume Point

Resume at Phase 4 subplan review:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-subplan-2026-07-06.md`

Phase 4 is CPU-hidden, short, and telemetry-inspection-only. It must determine
whether a native boolean divergence field is exposed by TFP HMC result objects,
or record that it is unavailable without proxy substitution.

## Key Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-result-2026-07-06.md`
- Phase 2 JSON:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.json`
- Phase 3 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-result-2026-07-06.md`
- Phase 3 JSON:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json`
- Phase 4 subplan:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-subplan-2026-07-06.md`

## Nonclaims

Do not claim full posterior correctness, broad HMC convergence, ranking,
source-faithful Zhao-Cui parity, default readiness, production readiness, public
API/package readiness, or LEDH evidence. Do not claim zero divergences from
`not_exposed_by_kernel`.
