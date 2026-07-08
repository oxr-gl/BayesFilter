# Streaming Manual VJP Phase 4 Subplan: Sinkhorn Recursion VJP

status: DRAFT_REFRESHED_AFTER_S3
date: 2026-06-23
phase: S4-SINKHORN-RECURSION-VJP

## Phase Objective

Implement and test the streaming finite Sinkhorn recursion VJP by mirroring the
dense manual reverse recursion while replacing every dense softmin VJP with the
blockwise softmin VJP.

## Entry Conditions

- S2 and S3 primitive VJPs passed.
- S1 derivation contract fixes finite step count, stopped scale, stopped keys,
  scalar epsilon, epsilon0, and scaling.
- S4 must compose the reviewed S2 blockwise softmin VJP and the S1 finite
  recursion contract.  S3 transport VJP is passed but S4 does not wire the full
  transport custom gradient yet.
- The recursion VJP must treat every Sinkhorn softmin key as stopped and every
  scale quantity as fixed.

## Required Artifacts

- Implementation diff for streaming finite Sinkhorn VJP helper in
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- Focused tests in `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py` or a
  new focused test file.
- S4 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-result-2026-06-23.md`
- S4 blocker, only if needed:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-blocker-2026-06-23.md`
- Refreshed S5 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-subplan-2026-06-23.md`

## Required Checks/Tests/Reviews

- Tolerance rule:
  - default dtype for focused tests: `tf.float64`;
  - value parity tolerance if tested: absolute error `<= 1.0e-10`;
  - VJP parity tolerance: max absolute error `<= 1.0e-8`;
  - directional VJP/JVP tolerance: absolute error `<= 1.0e-8`;
  - tiny autodiff diagnostics remain diagnostic only.
- CPU-hidden pytest for exact and padded chunk recursion fixtures.
- Tests must compare `d_log_alpha`, `d_log_beta`, and `d_x_from_sinkhorn_cost`
  against dense/manual and tiny autodiff diagnostics on tiny fixtures.
- Tests must include at least one `steps=0` fixture and one `steps>=2` fixture
  so final/initial softmin adjoints and reverse-step state order are both
  exercised.
- Tests must include exact and padded chunk fixtures.
- Tests must verify no key-side cost gradient leaks from stopped-key recursion.
- Tests must verify stopped-scale boundaries: `epsilon`, `epsilon0`,
  `scaling`, and `steps` do not receive gradients in the tiny fixtures.
- Directional VJP/JVP consistency on tiny fixtures.
- Source scan for no `GradientTape` inside the new streaming recursion VJP.
- Source/result review must confirm retained state is limited to per-step
  vectors and block-local temporaries.  Full cost/probability/trajectory
  tensors are forbidden retained state.
- `py_compile` and `git diff --check`.
- Claude one-path review of S4 result.

Exact local commands, adjusted only if file names change during implementation:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "sinkhorn_recursion" -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
rg -n "GradientTape|\\[B,N,N\\]|tf\\.einsum\\(|tf\\.matmul\\(" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-subplan-2026-06-23.md
```

The `rg` command is a review aid: existing dense/tiny comparator matches are
not automatic failures.  The S4 result must classify each relevant match and
veto any new-helper `GradientTape` or large-N dense retained state.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the streaming finite Sinkhorn recursion VJP match the dense manual reverse recursion without dense retained state? |
| Baseline/comparator | `_filterflow_manual_dense_finite_sinkhorn_vjp` and tiny autodiff diagnostics. |
| Primary pass criterion | Recursion VJP and directional checks pass within `1.0e-8` tolerance for exact and padded chunks, including `steps=0` and `steps>=2`. |
| Veto diagnostics | Wrong reverse-state order; missing final/initial softmin adjoint; key-side stopped-gradient leakage; stopped-scale gradient leakage; hidden dense cost/probability/trajectory state; `GradientTape` fallback; nonfinite adjoints. |
| Explanatory only | Number of retained vector states, runtime, and chunk sizes. |
| Not concluded | No end-to-end filter-loop correctness, no GPU memory success. |

## Forbidden Claims/Actions

- Do not wire into P82 yet.
- Do not run GPU jobs.
- Do not claim the full route is fixed before S5/S6.
- Do not wire into the full transport custom gradient in S4.
- Do not change stopped-scale/key semantics after seeing results.
- Do not return gradients for `epsilon`, `epsilon0`, `scaling`, or `steps`.

## Exact Next-Phase Handoff Conditions

Advance to S5 only if:

- recursion VJP parity passes;
- S4 result records retained/recomputed states;
- S4 result records stopped-key and stopped-scale leakage checks;
- S4 result records exact fixtures, tolerances, commands, environment, run
  manifest, decision table, and classified source-scan findings;
- S5 subplan names the new opt-in route and source-scan gate.

## Stop Conditions

Stop if:

- reverse recursion needs dense retained matrices;
- directional checks fail and cannot be localized;
- the stopped-scale/key contract changes.
- a correct recursion VJP requires `GradientTape` replay.
- tests show any gradient path into `epsilon`, `epsilon0`, `scaling`, or
  `steps`.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the S4 result or blocker.
3. Draft or refresh S5.
4. Review S5 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.

The S4 result must include a decision table with: decision, primary criterion
status, veto diagnostic status, main uncertainty, next justified action, and
what is not being concluded.  It must also include a run manifest with: git
commit, command, environment, CPU/GPU status, dtype, seeds if any, wall time if
available, output artifact paths, plan file, result file, and touched files.
