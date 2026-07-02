# Claude Review Packet: Total-VJP GPU/XLA Phase 3 To Phase 4

Status: `READY_FOR_REVIEW`

## Role Contract

Codex is supervisor and executor.  Claude is read-only reviewer only.  Claude
must not edit files, run experiments, launch agents, or change state.

## Question

Check whether Phase 3 is properly closed as passed and whether the refreshed
Phase 4 direction diagnostic is a valid next step for same-scalar gradient
direction agreement.

## Scope

Review only these files:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n64-t3-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n256-t3-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n1000-t3-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-subplan-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-execution-ledger-2026-07-01.md`

Out of scope:

- code edits;
- posterior correctness;
- production/default promotion;
- claims about the stopped partial derivative route.

## Evidence

Phase 3 rungs:

| Rung | Status | Elapsed seconds | Peak TF allocator bytes | Objective | Gradient values | MCSE |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `N=16,T=1,seeds=2` | `pass` | `138.15769824199378` | `50466816` | `-36.1256103515625` | `[-9.37370777130127, 3.432502508163452, 4.548910617828369]` | `{log_kappa_scale: 0.3407630920410156, log_nu_scale: 0.1250770092010498, log_obs_noise_scale: 0.3113260269165039}` |
| `N=64,T=3,seeds=5` | `pass` | `715.8411605180008` | `87696128` | `-124.877685546875` | `[-259.3408203125, 103.57362365722656, 44.914710998535156]` | `{log_kappa_scale: 3.0782182216644287, log_nu_scale: 1.2480616569519043, log_obs_noise_scale: 0.9125424027442932}` |
| `N=256,T=3,seeds=5` | `pass` | `688.3836792290676` | `468697856` | `-125.1681137084961` | `[-259.8353576660156, 103.83641052246094, 45.78861618041992]` | `{log_kappa_scale: 1.1120595932006836, log_nu_scale: 0.4503864347934723, log_obs_noise_scale: 0.3991796672344208}` |
| `N=1000,T=3,seeds=5` | `pass` | `505.82778843608685` | `6726029824` | `-125.3008041381836` | `[-260.80517578125, 104.21639251708984, 46.0502815246582]` | `{log_kappa_scale: 0.6466002464294434, log_nu_scale: 0.2674814760684967, log_obs_noise_scale: 0.23570899665355682}` |

All Phase 3 rungs passed GPU output, XLA JIT, full-route metadata, finite
objective, finite gradient, finite MCSE, and connected-gradient gates.

Phase 4 proposed command:

- same runner: `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`;
- `--fd-mode enabled`;
- `--basis-set raw`;
- `--direction-filter raw_log_kappa_scale,raw_log_nu_scale,raw_log_obs_noise_scale`;
- `--ad-evaluation-mode manual-reverse`;
- `--manual-reverse-compiler xla`;
- `--num-particles 1000`;
- `--time-steps 3`;
- same seeds as Phase 3 `N=1000`;
- same streaming transport and `--transport-ad-mode full`.

## Pass/Block Criteria

Pass if:

- Phase 3 result correctly states viability through `N=1000,T=3`;
- Phase 3 does not claim HMC direction validity;
- Phase 4 command compares the corrected full-route total derivative to
  regression FD for the same finite scalar;
- Phase 4 pass rule is exactly: every raw direction passes if within `2 MCSE`,
  or within `4 MCSE` with the Phase 3 MCSE decreasing trend, or relative error
  below `1%`;
- Phase 4 vetoes CPU fallback, missing XLA, route metadata not full, nonfinite
  estimates, unavailable MCSE, or same-scalar mismatch.

Block if:

- Phase 4 uses a different scalar, route, dtype, device target, or derivative
  target;
- Phase 4 could pass from Phase 3 MCSE decrease alone without inspecting FD
  direction results;
- the subplan overclaims HMC readiness or exact likelihood correctness;
- the result parser requirement is too vague to apply the stated rule.

## Nonclaims

Even if this review passes, do not conclude:

- HMC readiness;
- posterior correctness;
- exact nonlinear likelihood score correctness;
- production/default promotion;
- that the stopped partial derivative route is a score.

## Requested Verdict

Findings first if any.  End with exactly:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
