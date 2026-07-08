# Phase 6 Closeout: SIR Gradient HMC-Direction Program

Date: 2026-07-01

Status: `CLOSED_WITH_BUDGET100_MEMORY_BLOCKER`

## Decision

The program established that the SIR gradient route wiring is not the current
blocker: the diagnostic can run on the intended GPU/XLA/TF32 manual reverse
route and emit route-gated direction diagnostics.

The program did not establish SIR gradient correctness or HMC readiness.  It
closed with a sharper engineering blocker:

- budget 10 completes as a full material artifact;
- budget 100 exits with code 137 even as a separate process;
- the next target is finer-grained artifact construction, not threshold
  revision or CPU fallback.

## Decision Table

| Item | Status | Evidence |
| --- | --- | --- |
| Route wiring | Passed for smoke and budget 10 | Phase 3 route smoke and Phase 5 budget-10 route prerequisites. |
| Phase 1 gate implementation | Passed local tests and Claude review | Phase 1/2 results and `tests/test_p8p_sir_hmc_direction_gate.py`. |
| Budget 10 SIR direction gate | Partial numerical pass only | `log_obs_noise_scale` passes; `log_kappa_scale` precision-vetoed; `log_nu_scale` needs ladder certificate. |
| Budget 100 material diagnostic | Blocked | Exit code 137 before final JSON/Markdown. |
| Sinkhorn-budget root-cause claim | Not established | Budget 100 did not complete. |
| HMC readiness | Not established | Out of scope and unsupported by artifacts. |
| Next justified action | Finer-grained artifact construction | Split by seed group and FD direction/offset process, then aggregate. |

## Key Artifacts

Plans and ledgers:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-master-program-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-gated-overnight-execution-runbook-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-execution-ledger-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`

Phase results:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase2-diagnostic-reporting-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-result-2026-06-30.md`

Diagnostic artifacts:

- Phase 3 route smoke:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json`
- Phase 5 budget 10:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.json`
- Phase 5 budget 100 progress blocker:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget100-progress-2026-06-30.json`

Wrappers:

- `scripts/run_sir_gradient_phase3_gpu_smoke.sh`
- `scripts/run_sir_gradient_phase4_material_diagnostic.sh`
- `scripts/run_sir_gradient_phase5_budget10.sh`
- `scripts/run_sir_gradient_phase5_budget100.sh`

## Budget 10 Numerical Summary

Completed artifact:

- `T=3`, `N=64`, five fixed seeds.
- `route_prerequisite_pass`: `true`
- `max_row_residual`: `1.4722347259521484e-05`
- `row_residual_pass`: `true`
- `all_raw_directions_hmc_direction_pass`: `false`

Direction classifications:

- `log_kappa_scale`: `inconclusive_precision_veto`
- `log_nu_scale`: `within_4_combined_se_requires_ladder_certificate`
- `log_obs_noise_scale`: `within_2_combined_se`

This is enough to say that row residual pass at budget 10 is not by itself a
certificate of all raw SIR gradient directions.  It is not enough to say
whether budget 100 would repair the gate.

## Active Blocker

`BLOCKED_SINGLE_BUDGET100_EXIT137`

Budget 100 failed to produce final JSON/Markdown even when:

- run in its own Python process;
- run on the trusted GPU/XLA/TF32 route;
- preserving `--seed-microbatch-size 1`;
- preserving `--theta-offset-batch-size 2`.

## Next Engineering Target

Create a new reviewed subplan for scalar artifact construction:

1. Manual score:
   run one process per budget and seed group, write per-seed gradients and
   log-likelihoods.
2. FD objective:
   run one process per budget, raw direction, theta-offset chunk, and seed
   group, write objective values only.
3. Aggregation:
   combine per-seed gradients by exact mean, combine per-offset objectives by
   exact seed mean, then apply the existing regression and Phase 1 gate.
4. Review:
   Claude review must check that aggregation exactly reproduces the current
   estimator/comparator before material execution.

## Nonclaims

- No SIR gradient correctness claim.
- No HMC/NUTS readiness claim.
- No posterior correctness claim.
- No global production Sinkhorn budget claim.
- No nonlinear-model generalization claim.
- No CPU fallback evidence.
