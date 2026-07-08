# Reset Memo: Minimal SSL-LSTM Zhao-Cui HMC Validity Gaps

Date: 2026-07-06

Status: `CURRENT_RUNBOOK_CLOSED`

## Current State

The minimal SSL-LSTM `zhaocui_fixed` HMC validity-gaps runbook has been closed
after Phase 8. The latest executed artifact is:

- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_cpu_hidden_2026-07-06.json`

Latest wrapper status: `passed`.

Latest public tuner status: `budget_exhausted`.

Latest public tuner diagnostic role: `budget_exhausted_non_promoting`.

Latest active blocker:

- `screen_acceptance_above_repair_band`
- `joint_l_epsilon_no_viable_pair`
- `phase5_fixed_mass_step_status:repair_or_retry`

No final kernel handoff candidate exists.

## Repaired During This Runbook

- Windowed acceptance telemetry no longer hard-vetoes merely because a constant
  trace appears. Constant traces are accepted only with fixed-size chunk-runner
  runtime decision-count support.
- The Phase 6 public timeout hard veto was repaired/localized by the Phase 7
  enlarged-timeout run.
- The terminal Phase 6 repair slot mechanism was exercised once in Phase 8.

## Preserved Limitations

- Native divergence telemetry remains unavailable; this is not zero
  divergences.
- Phase 3 promotion screen failed on R-hat/ESS/native-divergence availability.
- Phase 8 is CPU-hidden, non-XLA, and smoke-scale diagnostic evidence only.
- No posterior correctness, broad HMC convergence, ranking, default readiness,
  production readiness, public API/package readiness, source-faithful Zhao-Cui
  parity, dimensional generality, or LEDH evidence is established.

## Suggested Next Program

If continuing HMC handoff work, start a new reviewed tuning-design program with
the research question:

Can a redesigned fixed-mass step repair ladder find a viable pair for the
minimal `zhaocui_fixed` target after the Phase 8 terminal repair-slot blocker,
without changing scientific claim boundaries?

The new plan should decide whether to adjust:

- fixed-mass step repair band or acceptance band;
- candidate budget policy;
- joint L/epsilon search neighborhood;
- max attempts or terminal-slot policy;
- diagnostic preset scale;
- CPU-hidden versus trusted GPU/XLA route.

Do not treat any of those adjustments as default-policy changes without a
separate reviewed evidence bar.

## Key Files

- Phase 8 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-terminal-phase6-repair-slot-result-2026-07-06.md`
- Phase 9 closeout:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase9-closeout-result-2026-07-06.md`
- Latest runtime artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_cpu_hidden_2026-07-06.json`
- Latest public tuning artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_public_artifacts_2026-07-06/hmc_kernel_tuning_result.json`
