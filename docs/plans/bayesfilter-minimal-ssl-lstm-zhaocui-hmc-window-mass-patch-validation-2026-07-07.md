# Minimal SSL-LSTM Zhao-Cui HMC Window-Mass Patch Validation

Date: 2026-07-07

Status: `READY_TO_EXECUTE`

## Objective

Test whether the current worktree repair to
`bayesfilter/inference/hmc_kernel_tuning.py` helps the minimal scalar
`zhaocui_fixed` HMC tuning case that previously closed with the Phase 8
fixed-mass blocker:

- `screen_acceptance_above_repair_band`
- `joint_l_epsilon_no_viable_pair`
- `phase5_fixed_mass_step_status:repair_or_retry`

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Does the current window-mass / fixed-mass tuning repair change the prior Phase 8 terminal repair-slot outcome on the same minimal target? |
| Mechanism under test | Current worktree changes to `hmc_kernel_tuning.py`, especially the repaired window-mass seed behavior and joint L/epsilon fixed-mass route. |
| Expected failure mode | The run may still end without a final kernel, either at fixed-mass step repair, frozen trajectory repair, timeout, or another structured blocker. |
| Promotion criterion | None. This is a patch-validation diagnostic only. |
| Promotion veto | Any attempt to treat a final kernel, if produced, as posterior correctness, convergence, zero-divergence evidence, ranking, readiness, or source-faithful Zhao-Cui parity. |
| Continuation veto | Compile failure, focused test failure in the touched contract, runtime exception, invalid JSON artifact, missing Phase 3/4 baseline preconditions, private mechanics exposure in public artifact, nonfinite target/value/score, or unsupported claim boundary crossing. |
| Repair trigger | If the blocker changes to a new precise structured blocker, record it and use it to design the next reviewed tuning program. |
| Explanatory diagnostics | Final status, hard vetoes, active repair triggers, attempt count, stage statuses, final-kernel hash presence/absence, public-safe summaries, private diagnostic event count. |
| What must not be concluded | No posterior correctness, broad HMC convergence, zero-divergence, statistical ranking, default readiness, production readiness, public API/package readiness, source-faithful Zhao-Cui parity, dimensional generality, or LEDH evidence. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific / engineering question | Does the user-supplied window-mass tuning repair help the previously blocked minimal `zhaocui_fixed` HMC terminal repair-slot case? |
| Exact baseline | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_cpu_hidden_2026-07-06.json` and its public tuning artifact. |
| Candidate | Current dirty worktree implementation in `bayesfilter/inference/hmc_kernel_tuning.py`. |
| Primary pass/fail criterion | A fresh structured CPU-hidden artifact is produced under the same Phase 8-style settings and shows whether the previous fixed-mass blocker is cleared, unchanged, or replaced by a new precise blocker. |
| Diagnostics that can veto | Compile/test failure, runtime exception, invalid JSON, public hard veto, nonfinite target/value/score, missing baseline preconditions, unsupported zero-divergence/proxy-divergence substitution, or unsupported readiness/correctness/ranking/source-faithful claim. |
| Explanatory only | Runtime, acceptance, stage status, repair triggers, attempt count, private event count, final-kernel hash presence/absence. |
| Not concluded even if the run passes | Posterior correctness, HMC convergence, zero divergences, tuned-kernel superiority, statistical ranking, default readiness, production readiness, source-faithful Zhao-Cui parity, dimensional generality, LEDH evidence. |
| Artifact preserving result | Fresh JSON/Markdown under `docs/benchmarks` plus this plan/result note. |

## Skeptical Plan Audit

Result: `PASS_WITH_BOUNDARIES`.

- Wrong baseline risk is controlled by using the closed Phase 8 terminal
  repair-slot artifact as the comparator.
- Proxy metric risk is controlled because acceptance, runtime, stage status,
  and final-kernel hash are diagnostic only.
- Missing stop-condition risk is controlled by compile/test/runtime/JSON and
  claim-boundary vetoes above.
- Unfair comparison risk is controlled by rerunning the same minimal target and
  Phase 8-style settings with fresh artifact paths.
- Hidden assumption risk is controlled by treating the current worktree patch
  as the candidate and not claiming source-faithful Zhao-Cui parity.
- Environment mismatch risk is controlled by using explicit CPU-hidden
  execution, matching the previous Phase 8 diagnostic route.
- Artifact mismatch risk is controlled by validating JSON and comparing the
  public-safe stage summaries against Phase 8.

## Planned Checks And Command

Pre-run checks:

- Compile `bayesfilter/inference/hmc_kernel_tuning.py`, the Phase 5 harness,
  and focused tests.
- Run focused tests for Phase 5/terminal repair-slot/fixed-mass contracts.
- Run `git diff --check`.

Diagnostic command:

```bash
PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 \
python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py \
  --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_window_mass_patch_validation_cpu_hidden_2026-07-07.json \
  --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_window_mass_patch_validation_cpu_hidden_2026-07-07.md \
  --tuning-output-dir docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_window_mass_patch_validation_public_artifacts_2026-07-07 \
  --public-timeout-budget-s 300.0 \
  --terminal-phase6-repair-extra-attempts 1
```

Post-run checks:

- Validate output JSON.
- Inspect public tuning result and stage summaries.
- Count private diagnostic events without exposing private mechanics.
- Record whether the prior blocker was cleared, unchanged, or replaced.
