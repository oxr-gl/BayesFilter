# Batched Linear Kalman Value+Score Plan

Date: 2026-06-14

Owning root: `/home/ubuntu/python/BayesFilter`

## Status

`PLAN_DRAFT_READY_FOR_REVIEW`

## Skeptical Audit

Status: passed for a planning artifact, not for implementation or performance
claims.

- Wrong baseline: correctness must compare against the existing scalar
  TensorFlow linear Kalman value path and the existing QR analytic score path,
  not against a weaker hand-written batch fixture.
- Proxy metrics: GPU compile success, runtime, XLA success, and larger batch
  throughput are engineering diagnostics only until scalar parity and analytic
  score parity pass.
- Missing stop conditions: the implementation must stop before promotion if any
  batched row disagrees with the scalar oracle, if row order drifts, if a
  nonfinite likelihood/score appears, if broadcasting hides a shape mismatch, or
  if the gradient corresponds to a different covariance/jitter law than the
  value recursion.
- Unfair comparisons: early timing must not compare batched GPU against scalar
  Python loops as a promotion criterion. The fair engineering baseline is the
  current static-unroll chain helper and scalar graph/XLA calls at matched batch
  size, with correctness established first.
- Hidden assumptions: first slice is dense, time-invariant linear Gaussian SSM,
  shared observation series, first-order score only, and fixed parameter
  dimension. Masked observations, time-varying matrices, Hessians, and nonlinear
  sigma-point filters remain follow-on work.
- Stale context: current BayesFilter already has scalar value and analytic score
  authority; this plan adds a separate batch-native path and does not replace
  the trusted scalar APIs.
- Environment mismatch: deliberate CPU-only checks must hide GPU before
  TensorFlow import. Any command that detects, initializes, benchmarks, or uses
  GPU/CUDA must be run in trusted/elevated context under the repo policy.
- Artifact adequacy: this plan names the API, tensor shapes, parity baselines,
  failure vetoes, and result artifacts needed before implementation can support
  HMC or NeuTra batch use.

Reason to proceed: Kalman filtering isolates the desired batch-over-parameters
mechanism without the sigma-point placement, branch, and nonlinear derivative
complications of UKF/CUT filters.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Can BayesFilter evaluate many independent linear Gaussian likelihoods and analytic scores in one TensorFlow graph by batching over parameter/model rows while remaining scalar-oracle equivalent? |
| Candidate mechanism | A batch-native dense Kalman value+score recursion with tensors carrying leading batch axis `B` and time kept sequential. |
| Expected failure mode | Shape broadcasting mistakes, row-order drift, covariance update derivative mismatch, or numerical differences from scalar QR score under small innovation covariances. |
| Promotion criterion | Batched value and score match per-row scalar references across fixed fixtures and a small parameter grid within declared tolerances. |
| Promotion veto | Any nonfinite required output, scalar parity failure, incompatible shape accepted silently, score/value covariance-law mismatch, or missing row-order test. |
| Continuation veto | Broken scalar oracle, TensorFlow runtime unavailable, or a batched algebra issue that cannot be isolated on a tiny deterministic fixture. |
| Repair trigger | Small numerical drift on stress rows triggers QR/square-root batched follow-up or tightened jitter/covariance-law alignment. |
| Explanatory diagnostics | Runtime, compile count, memory, CPU/GPU timing, Cholesky condition summaries, and batch-size scaling. |
| Must not conclude | No GPU speedup, no HMC convergence, no NeuTra training quality, no nonlinear/UKF readiness, and no default backend change from this first slice. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Does a new batch-native Kalman path return `log_likelihood[B]` and `score[B, p]` equivalent to existing scalar paths for each parameter row? |
| Exact baseline/comparator | Existing `tf_linear_gaussian_log_likelihood` / `tf_kalman_filter` value path and existing `tf_qr_linear_gaussian_score` analytic score path, evaluated row by row. |
| Primary pass/fail criterion | Dense batched value+score parity passes for deterministic fixtures, permuted batch rows, and a small parameter grid. |
| Veto diagnostics | Nonfinite values/scores; row permutation failure; accepted incompatible shapes; score mismatch against scalar analytic QR path; value mismatch against scalar value path; CPU-only test exposes GPU; graph/XLA retracing instability for same shapes. |
| Explanatory only | Runtime, GPU utilization, XLA compile time, batch-size scaling, condition number summaries, and warning counts. |
| Not concluded if passed | No performance superiority, no masked/time-varying/Hessian/nonlinear readiness, no sampler convergence, no production default change. |
| Artifact | This plan, focused tests, implementation result note, and optional benchmark JSON/Markdown under `docs/benchmarks/` after correctness passes. |

## Current Repo Context

- Dense scalar TensorFlow value path lives in
  `bayesfilter/linear/kalman_tf.py` via `tf_kalman_filter` and
  `tf_linear_gaussian_log_likelihood`.
- Scalar analytic score-only authority lives in
  `bayesfilter/linear/kalman_qr_derivatives_tf.py` via
  `tf_qr_sqrt_kalman_score` and `tf_qr_linear_gaussian_score`.
- Existing HMC chain batching uses static row unroll in
  `bayesfilter/inference/hmc.py::static_unroll_chain_value_and_score`; it is a
  safe bridge but not a true batch-native filter kernel.

## Proposed First-Slice Scope

Implement dense, time-invariant, first-order, batch-native Kalman value+score.

In scope:

- shared observations `y[T, m]`;
- batched model tensors with leading batch axis `B`;
- first-order derivative tensors with leading axes `[B, p, ...]`;
- value-only low-level kernel;
- combined value+score low-level kernel;
- optional filtered state return for the value path after core parity passes;
- CPU graph/XLA correctness tests first;
- GPU timing only after parity and only as an explanatory diagnostic.

Out of scope for first slice:

- observation masks;
- time-varying model matrices;
- Hessians;
- square-root/QR batch implementation unless direct covariance stress fails;
- UKF/CUT/nonlinear filters;
- replacing existing scalar public APIs.

## Proposed API

Add an experimental module:

```text
bayesfilter/linear/batched_kalman_tf.py
```

Low-level dense value kernel:

```python
tf_batched_kalman_filter(
    observations,                  # [T, m]
    transition_offset,             # [B, n]
    transition_matrix,             # [B, n, n]
    transition_covariance,         # [B, n, n]
    observation_offset,            # [B, m]
    observation_matrix,            # [B, m, n]
    observation_covariance,        # [B, m, m]
    initial_state_mean,            # [B, n]
    initial_state_covariance,      # [B, n, n]
    jitter=0.0,
    return_filtered=False,
) -> (log_likelihood[B], filtered_means[T, B, n] | None, filtered_covariances[T, B, n, n] | None)
```

Low-level dense value+score kernel:

```python
tf_batched_kalman_value_and_score(
    observations,                  # [T, m]
    batched model tensors,          # [B, ...]
    batched first derivatives,      # [B, p, ...]
    jitter=0.0,
    jitter_updates_filtered_covariance=True,
) -> (log_likelihood[B], score[B, p])
```

Optional wrapper after tests stabilize:

```python
tf_batched_linear_gaussian_score(
    observations,
    batched_model,
    batched_derivatives,
    *,
    backend="tf_batched_dense_kalman_score",
    jitter=0.0,
)
```

The first implementation can avoid a new dataclass by keeping the low-level
kernel tuple-based. If a public wrapper is promoted, add a small batched result
container or explicitly update the existing TF result container documentation so
vector log likelihoods are not mislabeled as scalar results.

## Algebraic Kernel

For each time step, with all operations batched over `B`:

```text
a      = c + T m
Pp     = T P T' + Q
v      = y_t - d - Z a
S      = Z Pp Z' + R + jitter I
Sinv   = solve(S, I)
K      = Pp Z' Sinv
ll_t   = -0.5 * (m log(2pi) + logdet(S) + v' Sinv v)
m_next = a + K v
P_next = (I - K Z) Pp (I - K Z)' + K R_update K'
```

First-order score contribution:

```text
dll_t = -0.5 * [tr(Sinv dS) + 2 dv' Sinv v - v' Sinv dS Sinv v]
```

Sensitivity update:

```text
da      = dc + dT m + T dm
dPp     = dT P T' + T dP T' + T P dT' + dQ
dv      = -dd - dZ a - Z da
dS      = dZ Pp Z' + Z dPp Z' + Z Pp dZ' + dR
dSinv   = -Sinv dS Sinv
dK      = dPp Z' Sinv + Pp dZ' Sinv + Pp Z' dSinv
dA      = -dK Z - K dZ
dm_next = da + dK v + K dv
dP_next = dA Pp A' + A dPp A' + A Pp dA' + dK R_update K' + K dR_update K' + K R_update dK'
```

This direct covariance/Joseph update is the simplest GPU-batch demonstration.
If stress tests show unacceptable drift versus scalar QR score, the follow-up is
a batched QR/square-root kernel rather than weakening tolerances.

## Why Combine Value And Gradient?

There is a real benefit to a combined value+score path for HMC and NeuTra:

- the likelihood and score share prediction, innovation, Cholesky, solves,
  `S^{-1}`, Kalman gain, and covariance updates;
- computing value and score separately would rerun the filter and duplicate the
  dominant `O(T * B * m^3)` innovation factorizations plus state updates;
- the combined path guarantees the score differentiates the same implemented
  jitter/covariance law as the reported value;
- HMC APIs naturally consume `log_prob_and_grad(theta_batch)`.

Still keep a separate value-only kernel. Likelihood-only grids, diagnostics,
filter output inspection, and some surrogate workflows should not pay the
sensitivity cost.

Recommended structure:

- separate public value-only function;
- separate public value+score function;
- shared private batched step helpers for prediction, innovation solve, and
  covariance update;
- no separate gradient-only function unless a downstream consumer truly needs
  score without likelihood, which is uncommon for HMC.

## Implementation Phases

### Phase 0: Shape Contract And Tiny Fixture

Add tests that build a batch from existing scalar fixtures:

- `B=1` parity with scalar value and scalar analytic score;
- `B=3` manually selected parameter rows;
- permuted batch rows preserve corresponding values/scores;
- incompatible shapes fail closed before TensorFlow silently broadcasts.

No GPU or performance claims.

### Phase 1: Dense Batched Value Kernel

Implement `tf_batched_kalman_filter` using batched Cholesky and batched
`cholesky_solve`.

Primary tests:

- value parity against row-wise `tf_linear_gaussian_log_likelihood`;
- optional filtered mean/covariance parity for `B=1` and `B=3`;
- graph mode and CPU XLA compile for fixed shapes;
- no `tf.TensorArray` over batch axis.

### Phase 2: Dense Batched Value+Score Kernel

Implement `tf_batched_kalman_value_and_score` with first-order sensitivities
carried as `[B, p, ...]`.

Primary tests:

- score parity against row-wise `tf_qr_linear_gaussian_score`;
- value parity against Phase 1 value kernel;
- finite-difference or GradientTape oracle on a tiny `n=1, m=1, p=2` fixture;
- row permutation and shape-fail tests.

### Phase 3: HMC/NeuTra Adapter Fixture

Add a small adapter exposing:

```python
log_prob_and_grad(theta_batch) -> (target_log_prob[B], target_score[B, p])
```

The adapter should map `theta_batch[B, p]` to batched model and derivative
tensors, call the batched value+score kernel, and add batched prior terms.

Primary tests:

- custom-gradient HMC target returns gradient with shape `[B, p]`;
- existing chain-batched HMC shape broadcast tests still pass;
- scalar and batched adapter agree row-by-row.

### Phase 4: Benchmark Ladder After Correctness

Only after Phases 0-3 pass, add a diagnostic benchmark:

- CPU eager/graph/XLA row-wise static unroll baseline;
- CPU graph/XLA batch-native kernel;
- trusted GPU XLA batch-native kernel;
- batch sizes such as `B in {1, 4, 16, 64, 256}`;
- horizons such as `T in {16, 64, 256}`;
- state/observation dimensions selected to avoid tiny-shape GPU underuse.

Runtime remains explanatory until uncertainty and matched-baseline evidence are
planned separately.

## Test Targets

Suggested new tests:

```text
tests/test_batched_linear_kalman_tf.py
tests/test_batched_linear_kalman_derivatives_tf.py
tests/test_batched_linear_kalman_hmc_adapter_tf.py
```

Suggested focused commands:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 \
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q \
tests/test_batched_linear_kalman_tf.py \
tests/test_batched_linear_kalman_derivatives_tf.py
```

If an HMC adapter fixture is added:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 \
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q \
tests/test_batched_linear_kalman_hmc_adapter_tf.py \
tests/test_nonlinear_ssm_phase4_full_chain_hmc.py
```

GPU benchmark commands require trusted/elevated execution under the repo GPU
policy and must record that status in the result note.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Start with dense batched Kalman value+score | Planned, not run | Planned fail-closed checks | Direct covariance score may drift on hard cases versus QR | Implement tiny dense batch fixture first | No performance or default-backend claim |
| Combine value+score for HMC/NeuTra | Justified by shared algebra | Must ensure score matches same covariance law | Memory cost of sensitivities at large `B,T,p` | Keep value-only kernel plus combined value+score kernel | No need to remove scalar APIs |
| Defer Hessian | Accepted for first slice | HMC/NeuTra need score, not Hessian, for primary loop | Mass-matrix workflows may later need approximate curvature | Use existing scalar Hessian or later batched Hessian plan | No batched Hessian readiness |

## Post-Plan Red-Team Note

Strongest alternative explanation if early GPU timing looks good: the speedup
may come from replacing Python/static unroll overhead rather than from better
linear algebra throughput. That is still useful engineering evidence but not a
scientific or sampler-quality result.

Result that would overturn the first-slice design: repeated parity failures
against scalar QR score that disappear under a square-root formulation. In that
case, switch the batch-native derivative kernel to QR/square-root instead of
loosening tolerances.

Weakest part of the evidence before implementation: the direct covariance
analytic derivative has not yet been proven against the repo's QR derivative
implementation for batched TensorFlow shapes. The first tests should be tiny,
deterministic, and row-wise comparable.
