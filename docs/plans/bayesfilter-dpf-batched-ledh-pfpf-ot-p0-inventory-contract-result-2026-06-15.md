# Phase 0 Result: Inventory And Contract Lock

Date: 2026-06-15

## Status

`PASS_READY_FOR_PHASE_1`

## Phase Objective

Inventory current LEDH-PFPF-OT scalar code, deterministic parity requirements,
graph/JIT blockers, tests, and file boundaries before implementation.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Are scalar LEDH-PFPF-OT baseline, determinism needs, graph blockers, and file boundaries clear enough to begin batch contract implementation? |
| Baseline/comparator | Existing scalar `run_ledh_pfpf_ot_tf`, `ledh_flow_batch_tf`, and `annealed_transport_resample_tf`. |
| Primary criterion | `PASS`: scalar paths identified, blockers recorded, import/smoke succeeded, worktree is bounded to new plan docs, and Phase 1 handoff is concrete. |
| Veto diagnostics | No Phase 0 veto fired. |
| Explanatory diagnostics | `.numpy()`/Python loop locations, available scalar tests, CPU TensorFlow version, deterministic branch policy. |
| Not concluded | No batching success, no value parity, no score correctness, no GPU claim, no production readiness. |

## Local Checks

| Check | Status | Notes |
| --- | --- | --- |
| `git status --short --branch` | `PASS_WITH_BOUNDED_NEW_DOCS` | Branch `main...origin/main`; only new `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-*` files are untracked/modified. |
| Scalar/blocker inventory `rg` | `PASS` | Located scalar LEDH-PFPF-OT, LEDH flow, annealed transport, and graph blockers. |
| CPU-only TensorFlow import | `PASS` | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`; TensorFlow `2.20.0`; command set `CUDA_VISIBLE_DEVICES=-1`. |
| Scalar LEDH-PFPF-OT import smoke | `PASS` | Imported `run_ledh_pfpf_ot_tf`, `ledh_flow_batch_tf`, and `annealed_transport_resample_tf`. |
| Scalar LEDH-PFPF-OT execution smoke | `PASS_DIAGNOSTIC_ONLY` | Tiny deterministic 1D CPU-only run returned finite log likelihood and `resampling_count=2`; this is not correctness evidence. |
| Required subplan heading check | `PASS` | All phase subplans contain required headings. |

CPU-only TensorFlow commands emitted a CUDA initialization warning despite
`CUDA_VISIBLE_DEVICES=-1`. This is recorded as an environment note, not as GPU
evidence or failure.

## Scalar Baseline Inventory

Primary scalar comparator:

- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- Function: `run_ledh_pfpf_ot_tf`
- Result dataclass: `LedhPFPFOTTFResult`
- Correction equation:
  `log_weights + target_transition + target_observation - pre_flow_log_density + forward_log_det`
- Default transport method: `annealed_transport`
- Default method id: `ledh_pfpf_ot_annealed_transport_tf`

LEDH flow comparator:

- `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py`
- Function: `ledh_flow_batch_tf`
- Current batching scope: particles within one parameter row, not parameter
  batch rows.

Annealed transport comparator:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- Function: `annealed_transport_resample_tf`
- Supports `[N,D]` and `[B,N,D]` particles, but eager diagnostics and active-row
  masking include `.numpy()` control flow in the public wrapper.

Related historical contracts:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-result-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-result-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-result-2026-06-07.md`

Those historical artifacts are not direct batching evidence, but they provide
the fixed-contract policy for deterministic value/gradient comparison:

- frozen pre-flow particles or transition innovations;
- frozen ESS branch masks;
- frozen OT settings;
- finite differences diagnostic only;
- gradients are fixed-branch relaxed-objective AD gradients, not stochastic or
  categorical resampling gradients.

## Graph And JIT Blockers

Scalar filter blockers:

- `ledh_pfpf_ot_tf.py:68`: Python loop over `tf.unstack(observations)`.
- `ledh_pfpf_ot_tf.py:104`: `.numpy()` ESS branch decision.
- `ledh_pfpf_ot_tf.py:143-146`: `.numpy()` finite checks.
- `ledh_pfpf_ot_tf.py:201-205`: eager diagnostic helper conversions.

LEDH flow blockers:

- `ledh_tf.py:62`: Python loop over particles via `tf.unstack`.
- `ledh_tf.py:199-203`: `.numpy()` diagnostic helper conversions.

Annealed transport blockers:

- `annealed_transport_tf.py:106`: `.numpy()` branch on active mask.
- `annealed_transport_tf.py:231-232`: `.numpy()` finite diagnostics.
- `annealed_transport_tf.py:593`: eager diagnostic helper conversion.

Existing graph-friendly pieces:

- `annealed_transport_tf.py` contains internal `@tf.function` Sinkhorn/transport
  kernels and a `tf.while_loop` implementation for annealed iterations.
- New batched implementation should reuse graph-safe internal algebra where
  possible, while avoiding the eager public wrapper branch/diagnostics.

## Available Tests And Smoke Policy

Exact files named in the Phase 0 subplan were not present:

- `tests/test_ledh_pfpf_ot_tf.py`
- `tests/test_dpf_tf_tfp_smoke.py`

Nearby tests found:

- `tests/test_ledh_pfpf_alg1_ukf_tf.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py`
- `tests/highdim/test_transport.py`

Phase 0 fallback executed import and tiny scalar-run smoke instead. This proves
the comparator is present and executable in eager CPU mode only. It does not
establish scalar correctness, graph compatibility, batching correctness, or
gradient correctness.

## Phase 1 Comparator, Seed, And Tolerance Handoff

Phase 1 must lock these before implementation:

- Comparator artifact: scalar `run_ledh_pfpf_ot_tf` plus a deterministic
  fixed-contract fixture derived from its semantics.
- Seed/noise policy: random ops are forbidden inside the value/score core;
  tests must provide fixed `initial_particles`, transition innovations or
  pre-flow particles, observations, and fixed ESS trigger masks.
- Branch policy: parity tests must use fixed ESS masks, not runtime `.numpy()`
  branch decisions. Runtime ESS can be recorded as explanatory only.
- Scalar parity tolerance: start with `atol=1e-10, rtol=1e-10` for log
  likelihood, filtered means, filtered variances, ESS, and deterministic
  ledger tensors in float64; any loosening requires a blocker note before
  looking at new results.
- Transport parity tolerance: start with `atol=1e-8, rtol=1e-8` for transport
  matrices and transported particles, because Sinkhorn/annealing arithmetic can
  be order-sensitive. Any loosening requires blocker review.
- Score tolerance: Phase 4 must predeclare both analytic/AD row-parity tolerance
  and finite-difference diagnostic tolerance before running score checks.
- Nonclaim: all gradients are gradients of the deterministic relaxed
  fixed-branch objective, not categorical PF/resampling gradients.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PASS_READY_FOR_PHASE_1` | Scalar baseline and blockers inventoried; import/smoke passed; Phase 1 handoff concrete. | No veto fired. | Phase 1 may still discover shape contract drift or missing deterministic fixture needs. | Begin Phase 1 shape contract implementation after reviewing refreshed Phase 1 subplan. | No batching correctness, no score correctness, no GPU/JIT result, no production readiness. |

## Post-Run Red Team

Strongest alternative explanation: the tiny scalar smoke may pass while later
fixed-contract parity fails because scalar runner callbacks and batched
contract callbacks do not encode exactly the same LEDH proposal or branch
semantics.

What would overturn this phase decision: Phase 1 cannot express fixed
initial/pre-flow/branch/transport inputs without changing scalar semantics or
public APIs.

Weakest evidence link: Phase 0 did not run a dedicated scalar LEDH-PFPF-OT
pytest because no exact test file exists.

## Next Phase

Phase 1 may begin after the refreshed Phase 1 subplan is reviewed locally for
consistency, feasibility, artifact coverage, and boundary safety.
