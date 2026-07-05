# Phase 0 Subplan: Route And Artifact Inventory

Date: 2026-07-01

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Freeze the corrected total-derivative target, verify that the local artifacts
and code paths needed for GPU/XLA validation exist, run cheap local checks, run
a trusted GPU availability probe, write a Phase 0 result, and refresh Phase 1.

## Entry Conditions Inherited From Previous Phase

- The manual total-VJP CPU float64 repair result exists:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-total-vjp-score-repair-result-2026-07-01.md`.
- The target derivative is the total derivative of the finite fixed-Sinkhorn
  scalar.
- The stopped route is a partial derivative and is wrong relative to a score
  claim for active transport.
- No GPU/TF32 production viability has been concluded.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase0-route-inventory-result-2026-07-01.md`.
- Updated visible execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-execution-ledger-2026-07-01.md`.
- Refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-subplan-2026-07-01.md`.
- Claude review notes in:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-claude-review-ledger-2026-07-01.md`.

## Required Checks, Tests, Reviews

Local non-GPU checks:

```bash
python -m py_compile \
  docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py
```

```bash
pytest -q \
  tests/test_p8p_sir_active_transport_comparator_contract.py \
  tests/test_ledh_pfpf_ot_p7_manual_score.py \
  tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Static dispatch proof:

Record exact file/line anchors showing that the Phase 1 CLI arguments reach the
correct full branch.  The Phase 0 result must cite at least these facts:

- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py` builds
  microbatch contexts preserving `args.transport_ad_mode`;
- its manual-reverse compiler path calls
  `p8p._manual_value_and_score_from_components`;
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py` branches on
  `args.transport_ad_mode == "full"` in both manual forward transport and
  manual transport VJP;
- the full branch calls
  `_filterflow_manual_streaming_finite_transport_total_vjp`;
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  also selects `_filterflow_manual_streaming_finite_transport_total_vjp` when
  the manual streaming gradient mode is paired with any non-`stabilized`
  transport AD mode.

The Phase 0 result must state directly whether the selector pair in Phase 1:

```text
--transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys
--transport-ad-mode full
```

dispatches to the total-derivative helper.  If this cannot be proven from code
anchors, Phase 0 fails and Phase 1 must not launch.

Trusted GPU probe:

```bash
nvidia-smi
```

Optional TensorFlow GPU probe if needed:

```bash
python - <<'PY'
import tensorflow as tf
print("physical", tf.config.list_physical_devices("GPU"))
print("logical", tf.config.list_logical_devices("GPU"))
print("tf32", tf.config.experimental.tensor_float_32_execution_enabled())
PY
```

Claude review:

- Review Phase 0 result and refreshed Phase 1 subplan read-only.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the corrected total-derivative route artifacts present, locally checkable, and ready for a tiny trusted GPU/XLA smoke? |
| Baseline/comparator | CPU float64 repair artifact and local tests from the repair. |
| Primary criterion | Required artifacts exist; local checks pass; static dispatch proof shows the Phase 1 selector pair reaches the total-derivative helper; trusted GPU is visible; Phase 1 subplan states an exact GPU/XLA smoke command and nonclaims. |
| Veto diagnostics | Missing artifacts; compile/test failure not explained and repaired; dispatch proof absent; trusted GPU not visible; Phase 1 still uses stopped partial route as score; no exact output path. |
| Explanatory diagnostics | Worktree status, route symbol locations, GPU model, TensorFlow GPU device list. |
| Not concluded | No GPU/XLA viability of the corrected route, no HMC readiness, no production promotion. |
| Artifact preserving result | Phase 0 result markdown and execution ledger entry. |

## Forbidden Claims And Actions

- Do not run the material GPU/XLA smoke in Phase 0.
- Do not claim GPU viability from `nvidia-smi` alone.
- Do not call the stopped route a score.
- Do not rely on output metadata alone to prove full-route dispatch.
- Do not edit algorithm code unless a Phase 0 local check exposes a trivial
  documentation or test-hygiene issue directly blocking Phase 1.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- all required Phase 0 local checks pass or any failure is explicitly repaired
  and rerun;
- static dispatch proof is recorded with exact code anchors;
- trusted GPU probe succeeds;
- Phase 1 subplan names exact command(s), output artifacts, pass/fail criteria,
  and stop conditions;
- Claude review returns `VERDICT: AGREE`, or a blocker result is written after
  five rounds for the same blocker.

## Stop Conditions

- GPU not visible in trusted context.
- Required total-VJP repair artifacts missing.
- Local checks fail and the fix is not small or clearly in scope.
- Claude identifies a material Phase 1 boundary problem that cannot be fixed
  within five rounds.
