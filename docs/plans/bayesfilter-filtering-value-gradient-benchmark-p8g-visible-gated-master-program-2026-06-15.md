# P8g Visible Gated Master Program: GPU-First LEDH/DPF Value And Gradient

Date: 2026-06-15

Status: `REVIEWED_READY_FOR_G0_LAUNCH_APPROVAL`

## Source Plan

This master program operationalizes the reviewed P8g program:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-gpu-ledh-gradient-dpf-program-2026-06-15.md`

Codex is supervisor and executor. Claude is a read-only reviewer only.

Canonical execution and review ledgers:

- execution ledger: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-execution-ledger-2026-06-15.md`;
- stop handoff: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-stop-handoff-2026-06-15.md`.

## Program Objective

Turn the repaired P8d LEDH/DPF lane into a GPU-first, gradient-bearing,
HMC-diagnostic-capable implementation while preserving all scientific and
artifact boundaries:

- GPU is the serious implementation path;
- CPU is for smoke, parity, and debugging only;
- LEDH gradients are required for usefulness;
- the first HMC-facing target is the fixed-randomness/no-resampling conditional
  surrogate objective, not the stochastic PF marginal target;
- value, gradient, HMC diagnostic, callback, and blocked-row ledgers remain
  separate.

## Phase Index

| Phase | Name | Subplan | Result artifact |
|---|---|---|---|
| G0 | GPU device and backend gate | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md` |
| G1 | Current bottleneck profile | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md` |
| G2 | Vectorized GPU Algorithm 1 core | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md` |
| G3 | Fixed-randomness LEDH gradient objective | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md` |
| G4 | GPU particle-count tuning | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-result-2026-06-15.md` |
| G5 | KSC and Spatial SIR callback closure | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-result-2026-06-15.md` |
| G6 | HMC diagnostic tiers | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-result-2026-06-15.md` |
| G7 | P8d/P8g artifact refresh | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase7-artifact-refresh-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase7-artifact-refresh-result-2026-06-15.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P8g execute as a visible gated program that produces a GPU-first, gradient-bearing LEDH/DPF implementation and honest refreshed artifacts? |
| Baseline/comparator | P8e repaired P8d runner, reviewed P8g plan, and value-only P8f tuning plan now superseded into P8g. |
| Primary pass criterion | Every phase either passes its declared gate and writes a result artifact, or stops with a blocker result that preserves claims and handoff state. |
| Veto diagnostics | GPU seriousness without trusted G0 manifest; stale P8d artifacts reused; fixed-randomness surrogate overclaimed as stochastic PF target; CPU-only runtime treated as real-life implementation; missing blocked rows in refreshed tables; Claude treated as execution authority. |
| Explanatory diagnostics | Runtime profiles, GPU device info, CPU/GPU parity, ESS/MC-SE tuning, gradient directional checks, HMC diagnostic tiers, Claude review findings. |
| Not concluded | Production HMC readiness, stochastic PF marginal HMC readiness, exact nonlinear likelihood proof, Zhao-Cui source-faithful TT/SIRT equivalence, or final filter ranking. |
| Artifacts | This master program, phase subplans/results, visible runbook, execution ledger including its `Review Loop Ledger` section, stop handoff, and refreshed P8d/P8g outputs. |

## Repair Loop Protocol

At the end of each phase:

1. run the phase-required local checks;
2. write the phase result or blocker result;
3. draft or refresh the next phase subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

For material subplans or material repairs, Claude may review local repo files
read-only. Claude cannot authorize crossing human, runtime, GPU, model-file,
funding, product-capability, or scientific-claim boundaries.

If review finds a fixable issue, patch the same subplan visibly and rerun
focused checks. Stop after five Claude rounds for the same blocker. If Claude
does not respond, probe Claude with a small liveness prompt. If the probe
works, redesign the review prompt; if the probe fails, write a tooling blocker.

Every Claude or Codex review round must be recorded in the canonical execution
ledger under `Review Loop Ledger` with: phase, artifact, blocker key, round,
verdict, disposition, next action, and review prompt scope.

Every phase subplan must preserve a `Planned Command And Artifact Contract`
section before launch. If the required execution script or test does not exist
yet, the subplan must name the exact planned entry point and block phase
passage until that entry point exists, is checked, and is cited in the phase
result.

## Approval Boundary

Before launching G0 or any later GPU/overnight/long run, Codex must ask for
approval for the exact commands or wrapper prefixes to be used. Planning and
read-only Claude review may proceed under already approved wrapper policy.

## Stop Conditions

- G0 trusted GPU probe fails.
- The vectorized route cannot remove the Python particle loop from serious GPU
  execution.
- CPU/GPU parity fails beyond tolerance.
- Fixed-randomness gradients are non-finite, unstable, or parameter-coordinate
  inconsistent.
- Particle tuning does not converge by the reviewed maximum count.
- KSC/Spatial SIR callback closure requires unreviewed target changes.
- HMC tiers fail but artifacts try to claim HMC readiness.
- Claude/Codex review fails to converge after five rounds for the same blocker.
- Continuing requires user approval that has not yet been granted.
