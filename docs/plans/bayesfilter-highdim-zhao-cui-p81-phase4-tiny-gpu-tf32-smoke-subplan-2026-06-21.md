# P81 Phase 4 Subplan: Tiny GPU/TF32 Fixed-Branch/JVP-Backed Candidate Smoke

status: REVIEWED_CLAUDE_R3_AGREE_READY_FOR_PHASE4
date: 2026-06-21

## Phase Objective

Run the smallest trusted GPU/TF32 smoke that verifies the Phase 3
fixed-branch/JVP-backed candidate path can execute with GPU-enabled TensorFlow
semantics before any larger SIR d=18 value/gradient comparison.

## Entry Conditions Inherited From Phase 3

- Phase 3 CPU-hidden checks passed.
- Phase 3 result records the horizon-0 limitation and forbids full likelihood
  claims.
- The candidate derivative route is the fixed-branch score path using
  TensorFlow forward-mode autodiff for local model-log-density directional
  derivatives; no closed-form hand derivative is claimed.
- No global defaults were changed in Phase 3.

## Required Artifacts

- Phase 4 result markdown:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase4-tiny-gpu-tf32-smoke-result-2026-06-21.md`.
- Optional tiny JSON manifest under `docs/plans/` if the chosen smoke command
  emits one.
- Updated execution ledger, review ledger, and stop handoff.

## Required Checks, Tests, And Reviews

Before executing any GPU smoke, run and preserve trusted/escalated preflight
logs for:

```bash
nvidia-smi
MPLCONFIGDIR=/tmp python -c "import tensorflow as tf; print(tf.config.list_physical_devices()); print(tf.config.list_physical_devices(\"GPU\"))"
```

Non-escalated GPU failures are sandbox-only evidence and cannot diagnose the
driver, CUDA stack, TensorFlow install, or hardware.  After trusted preflight,
the intended tiny smoke is:

```bash
MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "parameterized_zhao_cui_sir_matches_p8p_p79_theta_convention or parameterized_zhao_cui_sir_terms_are_sensitive"
```

If the tiny model-level GPU-enabled smoke passes and runtime is small, a second
Phase 4 step may run the d=18 horizon-0 score smoke under GPU-enabled
TensorFlow:

```bash
MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "multistate_fixed_design_tt_score_path_runs_on_sir_d18_horizon0_observation_term"
```

Review the Phase 4 result with Claude read-only before moving to Phase 5.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the Phase 3 fixed-branch/JVP-backed candidate route execute under GPU-enabled TensorFlow/TF32 conditions on a tiny bounded smoke? |
| Comparator | Phase 3 CPU-hidden passing tests; this phase checks runtime/backend feasibility, not numerical superiority. |
| Primary criterion | Tiny GPU-enabled smoke reproduces the same bounded horizon-0 behavior: finite value/score where applicable and same-branch finite-difference/JVP checks remain stable. |
| Veto diagnostics | GPU command run without trusted/escalated permissions, missing trusted `nvidia-smi` or TensorFlow device-probe logs, branch instability, tolerance failure against same-branch finite-difference/JVP checks, OOM, nonfinite outputs, TensorFlow device/backend errors, unbounded runtime, global default changes, or any attempt to generalize beyond the one-row horizon-0 boundary. |
| Explanatory diagnostics | Runtime, visible TensorFlow warnings, whether GPU is actually visible, and whether TF32 path is active where applicable. |
| Not concluded | LEDH-PFPF-OT agreement, full likelihood correctness, HMC readiness, posterior validity, production default readiness, or GPU scaling. |
| Artifact preserving result | Phase 4 result markdown plus ledger update. |

## Forbidden Claims And Actions

- Do not use CPU-hidden results as GPU evidence.
- Do not run GPU/CUDA commands non-escalated.
- Do not launch large diagnostics, LEDH-PFPF-OT comparisons, HMC/NUTS, package
  installs, network fetches, detached agents, destructive git actions, or
  default-policy changes.
- Do not claim full transition/filter likelihood correctness from the
  horizon-0 smoke.

## Exact Next-Phase Handoff Conditions

Phase 5 may be drafted only if Phase 4 records a trusted GPU-enabled smoke pass
or a precise GPU/backend blocker.  If Phase 4 passes, Phase 5 must separately
predeclare the actual SIR d=18 value/gradient diagnostic budget, seeds,
candidate route, LEDH-PFPF-OT comparator boundary, and promotion/veto criteria.

## Stop Conditions

Stop with a Phase 4 blocker if trusted GPU setup fails, if the smoke needs a
large-run escalation, if nonfinite outputs appear, if a default change is
needed, or if Claude review does not converge after five rounds.
