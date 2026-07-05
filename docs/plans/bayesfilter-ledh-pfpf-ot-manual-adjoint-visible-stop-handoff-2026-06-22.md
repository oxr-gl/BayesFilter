# LEDH-PFPF-OT Manual Adjoint Visible Stop Handoff

Date: 2026-06-22

Status: COMPLETE_MANUAL_ADJOINT_LOCAL_ROUTE_PASSED_P82_WIRING_BLOCKED

## Current State

The manual-adjoint/custom-gradient program has been recreated from verified
checkout state.  P82 FD-only validation is downstream-blocked until this
program produces a reviewed memory-disciplined LEDH actual-gradient route.

## Completed Phases

M0:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase0-reentry-result-2026-06-22.md`

M1:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-derivation-contract-2026-06-22.md`

## Latest Phase

M2 passed after local checks and Claude R1 agreement:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-result-2026-06-22.md`
- `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`

Observed local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -q`: `4 passed`.
- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`: passed.
- `PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`: passed and emitted diagnostics.
- `git diff --check -- tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md`: passed.

## Active Phase

The manual-adjoint/custom-gradient program is complete as a local route success
with downstream P82 wiring blocked.  M6 streaming/chunked memory route has
local checks passed and Claude R3 one-path review agreement.  M7 then blocked
P82 return after Claude R2 agreement because the benchmark path does not yet
expose the manual streaming transport-gradient mode.  M8 closeout passed local
checks.

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase3-dense-custom-gradient-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-loop-integration-design-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase4-loop-adjoint-integration-design-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase5-small-sir-smoke-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase5-small-sir-smoke-subplan-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-subplan-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-subplan-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-p82-validation-handoff-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-result-2026-06-22.md`

M3 local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -q`: `10 passed` after R1 repair.
- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`: passed.
- `PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`: passed and emitted diagnostics.
- `git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md`: passed.

## Program Artifacts

- Master program:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-master-program-2026-06-22.md`
- Visible runbook:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-visible-gated-execution-runbook-2026-06-22.md`
- Execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-visible-execution-ledger-2026-06-22.md`
- Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-claude-review-ledger-2026-06-22.md`

## Boundary Locks

- Do not rerun raw `transport_ad_mode=full` N10000 full-graph AD/JVP as the
  governed actual-gradient route.
- Do not run P82 N1000 regression FD until a memory-disciplined N10000
  actual-gradient route exists.
- Do not claim manual-adjoint correctness before primitive parity and
  integration checks pass.
- Do not claim streaming memory improvement before M6.
- Do not change defaults or public behavior before the opt-in integration gate.
- Do not treat M6 tiny CPU/float64 parity and returned-empty-matrix evidence as
  N10000 feasibility or GPU/TF32 evidence.
- Do not attempt to route around the blocked Claude review through another
  external-model prompt or indirect disclosure path.
- Do not use M6 as Zhao-Cui source-faithfulness evidence.  Any downstream
  Zhao-Cui source-route claim must satisfy repo-root `memory.md` with
  paper/math and local author-source anchors.
- Do not run P82 validation until a separate wiring phase exposes and verifies
  `transport_gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`
  through the SIR d18 benchmark path.

## Not Concluded

No manual-adjoint correctness, no implementation readiness, no streaming memory
improvement, no P82 FD agreement, no HMC/NUTS readiness, no posterior
correctness, no exact likelihood correctness, no default-gradient readiness, and
no production readiness.

## Latest Local Checks

M6 local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py`: passed.
- `git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md`: passed.
- `PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_m6_manual_streaming_value_and_score_tiny_opt_in_smoke tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_m5_manual_dense_value_and_score_tiny_opt_in_smoke tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_phase4_value_and_score_source_has_no_numpy_rng_or_runtime_ess_branch tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_phase3_value_core_source_has_no_numpy_rng_or_runtime_ess_branch -q`: `23 passed in 46.28s`.

M6 observed maxima:

- particle value error: `1.1102230246251565e-16`;
- particle/log-weight gradient error: `4.163336342344337e-17`;
- returned transport-matrix size: `0.0`.

M8 final checks:

- `git diff --check -- AGENTS.md memory.md experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py`: passed.
- unsupported-claim scan: no active readiness overclaim found.
- focused pytest bundle: `23 passed in 51.89s`.

## Safest Next Step

Start a separate P82 wiring subplan for
`transport_gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`
propagation through the SIR d18 benchmark path.  Do not run P82 validation until
that wiring phase passes local checks and review.

M6 local checks do not unblock P82 by themselves.
