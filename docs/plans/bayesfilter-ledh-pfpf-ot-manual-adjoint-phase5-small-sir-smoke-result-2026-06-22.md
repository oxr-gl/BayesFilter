# Manual Adjoint Phase 5 Result: Opt-In Integration And Tiny Smoke

Date: 2026-06-22

Status: PASSED_AFTER_CLAUDE_R1_AGREE

## Evidence Contract

| Field | Result |
|---|---|
| Question | Can the private manual/custom-gradient route be invoked through an opt-in filter-loop path on small bounded cases without changing defaults? |
| Baseline/comparator | M3 stopped-key value helper for transport values; tiny raw AD of the same stopped-key helper for transport gradients; existing tiny fixed-branch LEDH value/score fixture for integration smoke. |
| Primary criterion | Locally passed: opt-in route accepted in the experimental batched core, defaults remain unchanged, unsupported combinations reject, mixed-mask behavior passes, transport value/gradient parity passes, and tiny value/score smoke is finite with graph/eager parity. |
| Veto diagnostics | No default route changed; generic resampling API still rejects the manual route name; no governed N10000/P82 run launched; no streaming claim; no nonfinite values/gradients observed. |
| Explanatory diagnostics | Per-fixture error maxima and commands below. |
| Not concluded | No N10000 feasibility, no streaming/chunked memory improvement, no SIR d18 validation, no P82 FD agreement, no GPU/TF32 evidence, no HMC/default/posterior readiness, and no production readiness. |

## Implementation

M5 added a narrow opt-in experimental route name:

```text
manual_dense_finite_sinkhorn_stopped_scale_keys
```

Implementation artifact:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`

The route is accepted only by `batched_annealed_transport_core_tf` in the
experimental batched LEDH-PFPF-OT module.  The generic
`annealed_transport_resample_tf` API still rejects this route name.

The route branch:

- requires dense transport;
- rejects warmstarts;
- rejects non-`stabilized` `transport_ad_mode`;
- rejects vector `epsilon`;
- requires static positive `max_iterations`;
- calls the M3 private transport-matrix custom-gradient helper;
- leaves downstream `transported = matmul(T, x)` as ordinary TensorFlow;
- uses the existing full-batch mask/log-weight blending for active/inactive
  rows.

## Tests Added

Focused tests in:

- `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`

cover:

- M5 opt-in acceptance in the experimental batched core only;
- generic resampling API rejection;
- transport-matrix value parity against the M3 value helper;
- transport-matrix gradient parity against tiny raw AD of the same helper;
- mixed active/inactive mask blending;
- rejection of streaming, warmstart, non-`stabilized` mode, and vector
  `epsilon`.

Tiny value/score smoke in:

- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`

covers:

- finite log likelihood and score;
- eager/graph parity for the opt-in route;
- existing no-RNG/source discipline checks.

This is a tiny fixed-branch LEDH mechanics smoke.  It is not SIR d18
validation.  The artifact filename follows the prewritten phase ladder, but
the evidence in this result should be read as tiny opt-in LEDH mechanics only.

## Local Checks

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -q
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_m5_manual_dense_value_and_score_tiny_opt_in_smoke tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_phase4_value_and_score_source_has_no_numpy_rng_or_runtime_ess_branch tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_phase3_value_core_source_has_no_numpy_rng_or_runtime_ess_branch -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py
PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md
```

Observed results:

- focused primitive/integration pytest: `15 passed in 7.76s`;
- M5 plus source-discipline pytest: `18 passed in 19.33s`;
- py_compile: passed;
- diagnostics script: passed and printed JSON diagnostics;
- diff whitespace check: passed.

## Diagnostics

M5 tolerance contract:

- transport value max absolute error: `1e-10`;
- transport gradient max absolute error: `1e-8`;
- tiny value/score graph/eager parity: `1e-10`;
- finite value/score/gradient: required.

M5 transport core per-fixture maxima:

| Fixture | Transport value error | Transport gradient error |
|---|---:|---:|
| `B=1,N=3,D=1` | 0.0 | 1.8865117801247777e-17 |
| `B=1,N=4,D=2` | 0.0 | 1.734723475976807e-17 |
| `B=2,N=3,D=2` | 0.0 | 5.0306980803327406e-17 |

Overall M5 maxima:

- transport value error: `0.0`;
- transport gradient error: `5.0306980803327406e-17`.

Prior M2/M3 primitive checks still pass in the same focused test module:

- finite Sinkhorn loop VJP maximum: `2.0816681711721685e-17`;
- M3 private dense custom-gradient maximum: `5.204170427930421e-18`.

## Remaining Memory Bottleneck

The M5 route is still dense:

- materializes transport matrix `T` with shape `[B,N,N]`;
- recomputes dense costs and finite-loop states in the M3 VJP;
- is appropriate only for tiny/small bounded tests.

This does not solve the original memory explosion.  M6 must either implement a
streaming/chunked manual-adjoint route or write a blocker/rejection result based
on bounded memory/runtime evidence.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Accept M5 local opt-in tiny integration | Passed after local checks and Claude R1 agreement | No veto observed | Whether a streaming/chunked route can preserve this scalar without dense `[B,N,N]` memory | Advance to M6 memory route | No memory discipline, SIR d18 validation, P82 validation, GPU/TF32 evidence, or production readiness |

## Handoff

M6 may proceed.  It should start from the dense opt-in route and decide, with
bounded parity and memory/runtime evidence, whether a streaming/chunked
manual-adjoint route is viable.  M6 must not run P82 validation.
