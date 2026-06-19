# P8h Phase 3 Subplan: Scalar-SV GPU OT Implementation

Date: 2026-06-15

Status: `PASS_REVIEWED`

## Phase Objective

Implement the scalar-SV graph/GPU route for Algorithm 1 UKF LEDH + PF-PF
correction + Corenflos OT/Sinkhorn or annealed-transport resampling, including
Algorithm 1 covariance auxiliary-state carry.

## Entry Conditions

- Phase 2 algorithm design contract passed.

## Required Artifacts

- Scoped TensorFlow/TFP code changes, initially limited to:
  - `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
    at the Algorithm 1 runner and route identifiers;
  - `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py` only if
    a canonical transport helper must be exposed there;
  - `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
    only if a canonical transport helper or diagnostic must be exposed there;
  - `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py` only for a
    P8h-specific adapter/schema, not by mutating P8g evidence semantics;
  - `tests/test_ledh_pfpf_alg1_ukf_tf.py`;
  - `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
    only if the P8h benchmark adapter is touched.
- Implementation checklist:
  - add P8h route IDs without reusing P8g route metadata;
  - expose/compute canonical `A[target, source]` transport matrix for every
    enabled OT method;
  - carry particles and Algorithm 1 covariance state with the same canonical
    matrix;
  - compute PF-PF corrected weights before OT trigger/resampling;
  - reset weights to uniform only on triggered OT rows;
  - emit transport, covariance-carry, ESS, route, finite, and relaxed-not-
    categorical diagnostics;
  - keep P8g no-resampling/fixed-randomness and G4 tuning harnesses
    quarantined as historical diagnostics unless a reviewed P8h schema is
    added.
- Phase 3 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-gpu-ot-implementation-result-2026-06-15.md`.

## Required Checks, Tests, Reviews

- `git diff --check -- experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- Focused CPU pytest:
  `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- If full focused pytest is too slow, first run a narrower smoke selection and
  record that it is not a full Phase 3 pass:
  `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_pfpf_alg1_ukf_tf.py -k "alg1 or resampling or gradient or scalar_sv"`
- Trusted GPU smoke only after CPU/local tests pass. Candidate command must be
  run with escalated/trusted permissions:
  `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --help`
  followed by the smallest implemented P8h GPU smoke command if the CLI exposes
  one during Phase 3.
- CPU-only fallback for debugging must set `CUDA_VISIBLE_DEVICES=-1` before any
  TensorFlow import and record CPU-only status in the Phase 3 result.
- Claude read-only review of material implementation diff and Phase 3 result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the scalar-SV OT-resampled Algorithm 1 route exist with finite CPU smoke, route IDs, covariance carry, and tests? |
| Baseline/comparator | P8g scalar-SV no-resampling graph route and existing OT/Sinkhorn components. |
| Primary criterion | Code path exists, local tests pass, route emits diagnostics, and no serious-route claim is made before Phase 4/5. |
| Veto diagnostics | NumPy backend for algorithmic path; dropped covariance state; nonfinite smoke; missing route IDs; stale no-resampling default. |
| Explanatory diagnostics | CPU smoke values, diagnostics payloads, code review findings. |
| Not concluded | Particle tuning adequacy, gradient correctness, GPU scaling, or HMC readiness. |

## Forbidden Claims And Actions

- Do not run long tuning or HMC in Phase 3.
- Do not use PyTorch/JAX.
- Do not change unrelated lanes.
- Do not claim that P8g no-resampling/fixed-randomness artifacts validate the
  P8h OT-resampled route.
- Do not claim stochastic PF marginal-gradient correctness, exact nonlinear
  likelihood correctness, value adequacy, GPU scaling, HMC readiness, or filter
  ranking from Phase 3.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 only after implementation smoke/tests pass and result review
converges.

## Stop Conditions

- Implementation requires unapproved package installation or broad refactor.
- Covariance carry cannot be made finite/PSD under the Phase 2 contract.
