# Master Program: Low-Rank LEDH-PFPF-OT TF32 Scale Smoke

Date: 2026-06-20
Owner: peer agent
Supervisor/executor: Codex
Reviewer: Claude Opus read-only reviewer

## Status

`FINAL_TUNED_GPU_SCALE_PASSED_DIAGNOSTIC_ONLY`

## Program Objective

Test whether the low-rank coupling solver-route resampling algorithm can support
LEDH-PFPF-OT-shaped batched particle clouds at particle counts that make dense
OT impractical, especially `N=50k` and, only after a passing 50k gate, `N=100k`.

The algorithm under test is the existing TensorFlow low-rank coupling
solver-route:

`P = Q diag(1/g) R^T`

The program validates the lazy low-rank resampling path on deterministic
LEDH/PFPF-shaped fixtures.  It does not compare against the current-agent
positive-feature lane and does not edit public exports/defaults.

## Algorithm Contract

The candidate route:

- constructs deterministic rank landmarks from particle clouds;
- builds target/source assignment kernels;
- projects `Q`, `R`, and `g` through a Dykstra-style factor marginal route;
- applies `Q diag(1/g) R^T` lazily to particles;
- returns transported particles with normalized uniform log weights;
- records factor, transport, moment, runtime, and memory diagnostics.

The production-sized path must not materialize an `[B, N, N]` transport matrix.
Tiny materialization is allowed only for small invariant tests.

## Governing Inputs

- Independent lane clarification:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-independent-lane-clarification-to-peer-2026-06-20.md`
- Peer low-rank lane note:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-low-rank-independent-lane-note-2026-06-20.md`
- Wave 2 low-rank result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-result-2026-06-19.md`
- Wave 3 downstream result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-result-2026-06-19.md`
- TF32 batched DPF closeout context:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-visible-stop-handoff-2026-06-16.md`
- Low-rank implementation:
  `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`

Positive-feature artifacts are not evidence for this lane.

## Owned Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-*-2026-06-20.md`
- `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-*-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-*-2026-06-20.md`
- `docs/benchmarks/logs/low-rank-tf32-scale-smoke-*.log`
- `tests/test_low_rank_tf32_scale_smoke.py`

Forbidden writes:

- current-agent positive-feature artifacts;
- coordinator merge/synthesis records;
- Phase 1 baseline files;
- Phase 3 schema files;
- public exports/defaults/package metadata;
- unrelated dirty worktree files.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the low-rank coupling solver-route resampler run on LEDH/PFPF-shaped batched particle clouds at 50k and conditionally 100k particles without dense transport materialization, OOM, or invalid numerical artifacts? |
| Baseline/comparator | Exact weighted input estimates are the downstream reference for moment preservation. Naive uniform no-transport estimates are explanatory only. Dense OT is not a comparator at large N. Positive-feature artifacts are not a comparator. |
| Primary pass criterion | Small invariant tests pass; the initial medium CPU-hidden no-dense screen is interpreted through the user-approved tuning amendment if it fails only as an untuned moment-preservation screen; tuned medium CPU-hidden no-dense validation passes; trusted GPU FP32/TF32 50k scale smoke exits 0, writes JSON/Markdown, has empty hard vetoes, finite transported particles/factors, `Q,R >= 0`, `g > 0`, normalized uniform output log weights, residuals and moment errors below predeclared thresholds, and no dense `[B,N,N]` materialization. 100k is attempted only if 50k passes. |
| Veto diagnostics | Missing entry artifacts; compile/test failure; diagnostic failure; invalid JSON; missing embedded run manifest; nonfinite outputs/factors/diagnostics; negative required factors; nonpositive `g`; shape mismatch; output log-weight normalization residual above threshold; factor/transport residual threshold failure; weighted moment threshold failure; dense matrix materialization in scale mode; OOM/resource failure; unsupported claim; threshold change after seeing results; package/network/GPU approval boundary; public/default/API edit. |
| Explanatory diagnostics | Wall time, memory info, projection iterations, rank, factor minima, candidate-vs-naive moment deltas, residual magnitudes, per-fixture/per-size rows, and GPU device metadata. |
| Not concluded | No speedup, ranking, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, full low-rank Sinkhorn solver fidelity, broad scalable-OT selection, or TF32-help claim. |
| Artifacts | Master program, visible runbook, ledger, stop handoff, phase subplans/results, implementation/tests, logs, JSON/Markdown diagnostics with embedded run manifests, and final closeout. |

## Predeclared Thresholds

These thresholds are fixed before any scale results:

| Diagnostic | Threshold | Role |
| --- | ---: | --- |
| factor marginal residual | `<= 5.0e-3` | hard veto |
| induced row residual | `<= 5.0e-3` | hard veto |
| induced column residual | `<= 5.0e-3` | hard veto |
| tiny materialized apply parity | `<= 1.0e-10` | small invariant hard veto only |
| output log-weight normalization residual | `<= 1.0e-6` | hard veto |
| weighted mean absolute error | `<= 2.5e-2` | downstream hard veto |
| weighted second-moment absolute error | `<= 7.5e-2` | downstream hard veto |

Runtime and memory are explanatory only.  A run can be rejected for OOM or
non-completion, but passing runtime is not speedup evidence.

## Fixture And Manifest Contract

The absolute moment thresholds above are valid only for the frozen deterministic
fixture contract below.  Changing these fixture scales or dimensions after
seeing results is a threshold-change veto.

| Field | Frozen value |
| --- | --- |
| Fixture id | `bounded_smooth_v1` |
| Particle coordinate scale | bounded smooth coordinates with absolute value `<= 1.0` before transport |
| Log-weight logit scale | deterministic centered logits with absolute value `<= 1.25` before normalization |
| Batch offsets | deterministic offsets with absolute value `<= 0.10` |
| Small invariant rows | `B=2`, `N=32`, `D=4`, `rank=8`, `dtype=float64`; tiny dense materialization allowed only here |
| Initial medium CPU rows | `B=2`, `N in {4096, 8192}`, `D=8`, `rank=64`, `assignment_epsilon=0.5`, `dtype=float32`, CPU hidden, timeout `300s`; under the user-approved amendment, this screen is not a route rejection if it only exposes missing tuning |
| Coarse tuning rows | `B=2`, `N=4096`, `D=8`, ranks `{64,128,256,512}`, assignment epsilons `{0.5,0.25,0.125,0.0625}`, `dtype=float32`, CPU hidden |
| Focused tuning rows | `B=2`, `N=4096`, `D=8`, ranks `{64,128}`, assignment epsilons `{0.05,0.04,0.03125,0.025,0.02,0.015625,0.01}`, `dtype=float32`, CPU hidden |
| Tuned medium CPU rows | `B=2`, `N in {4096, 8192}`, `D=8`, `rank=64`, `assignment_epsilon=0.015625`, `dtype=float32`, CPU hidden |
| Trusted GPU rows | `B=2`, `N=50000`, `D=8`, `rank=64`, `assignment_epsilon=0.015625`, `dtype=float32`; `N=100000` attempted only if 50k passes |

Every diagnostic JSON must include a top-level `run_manifest` object with:

- `git_commit` and `git_status_short`;
- `command`, `working_directory`, `python_executable`, and `python_version`;
- `tensorflow_version` and `tensorflow_probability_version`;
- `device_mode`, `cuda_visible_devices`, `gpu_devices`, and CPU/GPU trust
  context;
- `tf32_requested`, `tf32_execution_recorded`, and TensorFlow TF32 policy
  metadata when applicable;
- `fixture_id`, `batch_size`, `state_dim`, `particle_counts`, `rank`,
  `assignment_epsilon`, `dtype`, and `seed`;
- `started_at`, `ended_at`, `wall_time_seconds`, and artifact/log paths;
- `plan_path` and phase result path when known.

Markdown diagnostics and phase results summarize the same manifest fields
needed to recover the command, environment, device context, fixture, and
artifacts.

## Phase Index

| Phase | Name | Subplan | Result artifact |
| --- | --- | --- | --- |
| LR-TF32-0 | Governance, Evidence, And Review Gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p00-governance-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p00-governance-result-2026-06-20.md` |
| LR-TF32-1 | Harness And Small Invariants | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p01-harness-invariants-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p01-harness-invariants-result-2026-06-20.md` |
| LR-TF32-2 | Medium CPU No-Dense Smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02-medium-cpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02-medium-cpu-result-2026-06-20.md` |
| LR-TF32-2A | Coarse Low-Rank Solver-Route Tuning | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02a-tuning-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02a-tuning-result-2026-06-20.md` |
| LR-TF32-2B | Focused Low-Epsilon Tuning | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02b-focused-tuning-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02b-focused-tuning-result-2026-06-20.md` |
| LR-TF32-2C | Tuned Medium CPU No-Dense Validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02c-medium-cpu-tuned-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02c-medium-cpu-tuned-result-2026-06-20.md` |
| LR-TF32-3 | Trusted GPU FP32/TF32 Scale Smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p03-trusted-gpu-scale-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p03-trusted-gpu-scale-result-2026-06-20.md` |
| LR-TF32-4 | Closeout And Stop | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p04-closeout-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-result-2026-06-20.md` |

## Repair Loop Protocol

For each phase:

1. Run the required local checks.
2. Write a phase result/close record.
3. Draft or refresh the next subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

Fixable lane-owned issues are patched visibly and rerun with focused checks.
Material subplans/results may be reviewed by Claude Opus as read-only reviewer.
Claude cannot authorize human, runtime, model-file, funding,
product-capability, shared-contract, public/default/API, GPU, package/network,
or scientific-claim boundary crossings.  Stop after five Claude review rounds
for the same material blocker.

## Approval Gates

Anticipated approvals required:

- Claude Code read-only review via
  `/home/ubuntu/python/claudecodex/scripts/claude_worker.sh` with path-only
  prompts.  These reviews must be launched in trusted/elevated context; any
  non-elevated hang, missing output, auth error, or network error is sandbox
  evidence only until a trusted minimal probe is rerun.
- Trusted GPU/TF32 scale commands for Phase LR-TF32-3.
- `nvidia-smi`/GPU memory probes before trusted GPU scale runs.
- Long-running `timeout`-wrapped diagnostic commands if the 50k/100k smoke is
  expected to run beyond a quick local test.

No package install, network fetch, credential access, destructive git command,
or public/default/API edit is planned.

## Skeptical Plan Audit

Pre-execution audit checklist:

- Wrong baseline: dense OT is not used as large-N comparator; exact weighted
  input estimates are the downstream reference.
- Proxy promotion: runtime, memory, and TF32 metadata are explanatory only.
- Missing stop conditions: OOM, invalid factors, invalid particles, failed
  moment screen, dense materialization, GPU approval boundary, and unsupported
  claims all stop or block.
- Unfair comparison: no positive-feature comparison or ranking occurs.
- Hidden assumption: small/medium CPU checks validate harness shape,
  invariants, and no-dense behavior at the fixed medium sizes; they do not
  establish 50k/100k feasibility.
- Environment mismatch: trusted GPU evidence is required for GPU/TF32 claims;
  CPU-hidden runs cannot establish GPU feasibility.
- Artifact sufficiency: JSON/Markdown/logs plus phase result records preserve
  pass/fail evidence.

Audit status: `P00_PASSED_AFTER_CLAUDE_ROUND_2_AGREE`; final interpretation
amended after the user identified the missing tuning phase as a planning/usage
error rather than a route rejection.
