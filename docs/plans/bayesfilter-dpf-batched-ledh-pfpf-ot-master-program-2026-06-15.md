# Batched LEDH-PFPF-OT Master Program

Date: 2026-06-15

## Status

`REVIEWED_PHASE_0_READY`

## Purpose

Build and validate an experimental batch-native TensorFlow implementation of
LEDH-PFPF-OT where the leading batch axis indexes independent model-parameter
proposals evaluated against the same observation sequence.

This program is limited to LEDH-PFPF-OT. It does not cover bootstrap PF,
Algorithm 1 UKF, CUT4, HMC, NeuTra, or production default promotion.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can LEDH-PFPF-OT value and value+score evaluation be parallelized across model-parameter proposals with a compiled TensorFlow batch axis? |
| Mechanism under test | A new experimental tensor-core path with shapes `[B,N,D]` for particles and `[B]` / `[B,p]` for value and score. |
| Expected failure mode | Current scalar path contains Python loops, `.numpy()` decisions, and scalar diagnostics that block fair JIT/GPU benchmarking. |
| Promotion criterion | Batched path passes scalar parity, stacked-row parity, finite score checks, finite-difference checks on small fixtures, and compiled CPU smoke. |
| Promotion veto | Scalar parity failure, row cross-talk, nonfinite values/scores, uncompiled benchmark evidence, changed relaxed-target semantics, or unsupported categorical-PF gradient claim. |
| Continuation veto | Environment cannot import TensorFlow, current scalar LEDH-PFPF-OT cannot be made deterministic for parity, or reviewed plan/review loop fails to converge after five rounds. |
| Repair trigger | Fixable shape, parity, diagnostics, or graph-compatibility failures with clear local cause. |
| Explanatory diagnostics | ESS, transport residuals, Jacobian/log-det ranges, compile time, warm-call time, memory/capacity observations. |
| Must not conclude | No categorical resampling gradient, no posterior correctness, no HMC/NeuTra readiness, no production default, no unconditional GPU speedup. |

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can a dedicated experimental LEDH-PFPF-OT tensor core batch independent parameter rows while preserving the scalar relaxed-objective contract? |
| Baseline/comparator | Existing scalar `run_ledh_pfpf_ot_tf` and existing LEDH flow / annealed transport components. |
| Primary pass criterion | Each phase completes its local checks, writes result artifacts, refreshes the next subplan, and receives read-only Claude review when material. |
| Veto diagnostics | Wrong scalar baseline; proxy metrics promoted to correctness; missing stop conditions; row cross-talk; stochastic noise mismatch in parity; unsupported target/gradient claim; uncompiled GPU benchmark; missing artifacts. |
| Explanatory diagnostics | Runtime, compile time, transport residuals, ESS, score finite-difference gaps, memory estimates, implementation complexity. |
| Not concluded | No production default, no categorical PF gradient, no posterior or sampler validity, no broad nonlinear correctness, no GPU speedup claim before compiled benchmarks. |
| Required artifacts | Master program, runbook, launch plan, phase subplans/results, Claude reviews, pytest artifacts, benchmark JSON/MD when benchmarks are reached, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| New experimental module | Current scalar path has Python loops and `.numpy()` decisions | Avoids destabilizing existing DPF artifacts and allows clean tensor contract | Duplicate logic drifts from scalar semantics | Phase 0 inventory and Phase 2 scalar parity | hypothesis |
| Precomputed noise tensors | Needed for deterministic parity and gradients | Removes RNG from value/score core and makes row parity meaningful | Noise contract differs from scalar runner | Phase 1 deterministic callback contract and B=1 parity fixture | hypothesis |
| Annealed transport first | Existing annealed transport supports `[B,N,D]` | It is the closest current component to batch-native OT resampling | Transport diagnostics still use eager scalar conversions | Phase 0 inventory and Phase 2 compiled-safe core checks | hypothesis |
| Relaxed objective score only | DPF governance docs distinguish relaxed target from categorical PF | Prevents false categorical resampling gradient claim | User or downstream code treats score as PF gradient | Phase 1/4 nonclaim checks | reviewed |
| JIT-only GPU benchmark rule | User instruction from prior batched filtering work | Eager GPU comparisons are misleading | Benchmark run claims speed without compilation | Phase 5 benchmark harness must fail closed without JIT | reviewed |

## Phase Index

| Phase | Name | Objective | Subplan | Result |
| ---: | --- | --- | --- | --- |
| 0 | Inventory And Contract Lock | Inventory current LEDH-PFPF-OT code, scalar baselines, determinism gaps, and plan boundaries. | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p0-inventory-contract-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p0-inventory-contract-result-2026-06-15.md` |
| 1 | Batched Callback And Shape Contract | Define the experimental batch callback/data contract and minimal fixture scaffolding. | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p1-shape-contract-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p1-shape-contract-result-2026-06-15.md` |
| 2 | Batched LEDH Flow And Transport Core | Implement compiled-safe batched LEDH flow plus transport core adapter without value recursion. | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p2-flow-transport-core-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p2-flow-transport-core-result-2026-06-15.md` |
| 3 | Batched Value Recursion And Parity | Implement batched LEDH-PFPF-OT value recursion and prove B=1/B=20 parity. | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p3-value-parity-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p3-value-parity-result-2026-06-15.md` |
| 4 | Batched Value+Score | Add value+score wrapper and finite-difference checks for the relaxed objective. | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p4-value-score-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p4-value-score-result-2026-06-15.md` |
| 5 | Compiled Benchmark Ladder | Run JIT-only CPU/GPU benchmark ladder with scalar-stack comparators and memory notes. | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p5-compiled-benchmark-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p5-compiled-benchmark-result-2026-06-15.md` |
| 6 | Closeout And Promotion Boundary | Produce final experimental-readiness decision and unresolved production gaps. | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p6-closeout-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p6-closeout-result-2026-06-15.md` |

## Cross-Agent Review Contract

Codex is supervisor and executor.

Claude Opus max effort is read-only reviewer only. Claude may inspect referenced
paths and report findings, but must not edit files, run experiments, launch
agents, authorize boundary crossing, change claims, or approve production
defaults.

Claude review prompts must be path-based or excerpt-bounded. Do not paste whole
files. If Claude does not respond, Codex must run a small read-only probe. If
the probe responds, Codex must redesign the review prompt and retry.

## Repair Loop

For each material phase:

1. Run a skeptical plan audit before execution.
2. Execute the smallest visible implementation/check that answers the phase.
3. Write the phase result.
4. Draft or refresh the next subplan.
5. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
6. Send material plans/results to Claude read-only review.
7. If review finds a fixable problem, patch the same subplan/result visibly,
   rerun focused checks, and retry review.
8. Stop after five Claude rounds for the same blocker.

## Anticipated Approval Needs

- Claude Code read-only review through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh` requires
  trusted execution.
- GPU/CUDA detection or GPU benchmarks require trusted execution.
- Package installation, network fetches, credentials, destructive filesystem or
  git actions, detached supervisors, and production default changes require
  separate human approval.

## Forbidden Claims And Actions

- Do not claim categorical-resampling PF gradients.
- Do not claim posterior correctness or sampler readiness.
- Do not benchmark GPU without JIT/compiled mode.
- Do not change production defaults or public APIs.
- Do not overwrite unrelated files or existing DPF artifacts.
- Do not let Claude execute or authorize work.
- Do not treat proxy RMSE, finite smoke output, or speed as correctness.

## Final Handoff Requirements

The final handoff must list final phase reached, status, artifacts, Claude
review trail, local checks/benchmarks actually run, unresolved blockers, what
was not concluded, and exact next human decision required.
