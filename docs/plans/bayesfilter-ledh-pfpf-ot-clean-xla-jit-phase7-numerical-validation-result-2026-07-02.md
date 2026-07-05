# Phase 7 Result: Numerical Validation

Date: 2026-07-02

Status: `OWNER_ACCEPTED_WITH_FD_WAIVER`

## Phase Objective

Check whether the actual full GPU/XLA LEDH-PFPF-OT route produces finite,
connected, same-scalar directional gradients on a bounded P8p SIR fixture after
the clean-loop repairs.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Owner accepted and promoted Phase 7 with an explicit FD waiver on 2026-07-03. The route ran cleanly on GPU/XLA; the predeclared same-scalar FD sentinel narrowly failed for `log_obs_noise_scale`. |
| Primary criterion status | Not met as originally preregistered. Finite outputs, runtime route evidence, repeat determinism, and HLO watchpoint passed; FD sentinel failed. Promotion is by owner waiver, not by retroactive gate pass. |
| Veto diagnostic status | FD sentinel veto fired under the original rule. Owner waived this narrow veto for bounded promotion. No GPU, finiteness, route-manifest, repeat-determinism, or HLO veto fired. |
| Main uncertainty | The miss is small and only for one parameter, but the exact cause remains uninvestigated. |
| Next justified action | Treat the clean-XLA bounded fixture as promoted by owner acceptance. Future broader validation or HMC use should preserve the waiver caveat and should not claim the original FD gate passed. |
| What is not concluded | No HMC readiness, no broad clean-XLA readiness, no exact nonlinear likelihood proof, no all-model validation, and no claim that stopped-key helpers compute scores. |

## Owner Acceptance

On 2026-07-03, the owner explicitly approved treating this as accepted and
promoted because the result is closed enough and not worth extra repair effort.
This is a scientific waiver of the narrow FD-sentinel miss, not a rewrite of
the evidence. The original same-scalar FD gate remains recorded as failed for
`log_obs_noise_scale`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745`; worktree dirty (`git status --short` line count 907). |
| Commands | `nvidia-smi`; `python scripts/collect_ledh_clean_xla_phase7_validation.py --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-2026-07-02.json --device /GPU:0 --expect-device-kind gpu --batch-seeds 81120 --time-steps 1 --num-particles 16 --theta 0.02,-0.01,0.01 --fd-steps 0.002,0.001,0.0005 --sinkhorn-iterations 2 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --dtype float32 --tf32-mode enabled`; Phase 5 static/parity checks. |
| Environment | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python`; TensorFlow 2.19.1; TF32 enabled. |
| CPU/GPU status | Trusted GPU execution. `nvidia-smi` reported NVIDIA GeForce RTX 4080 SUPER. TensorFlow outputs were all on `/job:localhost/replica:0/task:0/device:GPU:0`. |
| Data version | P8p actual SIR d18 fixed tensor fixture, generated locally by the benchmark helper. |
| Random seeds | `batch_seeds=[81120]`; fixed stateless process-noise tensor policy inherited from Phase 2. |
| Wall time | Cold compile plus first call 23.452s; warm calls 0.038s and 0.037s; FD sentinel 0.413s; HLO retrieval 4.608s; script wall time 28.612s. |
| Output artifact | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-2026-07-02.json` |
| Static audit artifact | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-static-audit-2026-07-02.json` |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-subplan-2026-07-02.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-result-2026-07-02.md` |

## Runtime Route Manifest Summary

The executed scalar used:

- `transport_plan_mode="streaming"`;
- `transport_gradient_mode="manual_streaming_finite_sinkhorn_stopped_scale_keys"`;
- `transport_ad_mode="full"`;
- `score_route="manual_reverse_scan_no_autodiff"`;
- selected full-route helper:
  `_filterflow_manual_streaming_finite_transport_total_vjp`;
- `stopped_key_helper_selected_for_score_evidence=false`.

The FD sentinel used the same compiled manual value/score function objective
for plus/minus theta calls. The stopped-key helpers remain present in the code,
but they are partial-derivative helpers and are not score evidence.

## Numerical Evidence

| Check | Result |
| --- | --- |
| Decision | `OWNER_ACCEPTED_WITH_FD_WAIVER_PHASE7_NUMERICAL_VALIDATION` |
| Output finite | `true` |
| Route manifest pass | `true` |
| Repeat determinism pass | `true` |
| HLO watchpoint pass | `true` |
| Same-scalar FD sentinel pass | `false`; owner waived the narrow miss for promotion. |

The reported full-route mean gradient was:

| Parameter | Analytic score | FD outcome |
| --- | ---: | --- |
| `log_kappa_scale` | `-9.70480728149414` | Passed. FD values were about `-9.715` with tolerance about `0.195`. |
| `log_nu_scale` | `3.55403995513916` | Passed. FD values were about `3.555` to `3.559` with tolerance about `0.072`. |
| `log_obs_noise_scale` | `4.833810806274414` | Failed. FD values were `4.935264587402344`, `4.9343109130859375`, and `4.98199462890625`. |

For the failing `log_obs_noise_scale` direction:

| FD step | FD value | Absolute error | Predeclared tolerance | Pass |
| ---: | ---: | ---: | ---: | --- |
| `0.002` | `4.935264587402344` | `0.10145378112792969` | `0.09970529174804688` | `false` |
| `0.001` | `4.9343109130859375` | `0.10050010681152344` | `0.09968621826171875` | `false` |
| `0.0005` | `4.98199462890625` | `0.14818382263183594` | `0.100639892578125` | `false` |

The closest miss is small, but it is still a failure under the reviewed
predeclared rule. The accepted status comes from the explicit owner waiver.

## Compiler And Guardrail Evidence

| Metric | Value |
| --- | --- |
| `jit_compile` | `true` |
| Concrete function count | `1` |
| Unexpected retrace | `false` |
| HLO text length | `27,766,809` |
| HLO line count | `52,059` |
| HLO `while` marker count | `199,199` lower-case matches |
| HLO watchpoint | Passed: same fixture as Phase 6, not more than `4x` Phase 6 HLO length. |

Post-run local checks:

```text
CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-static-audit-2026-07-02.json
decision: FAIL_CURRENT_ROUTE
current_veto_ids: SINK-STOPPED-VALUE-KEY, SINK-STOPPED-VJP-KEY
warning_ids: SINK-TOTAL-CUSTOM-TAPE

CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py::test_phase5_sinkhorn_target_helpers_have_no_python_step_loop_or_state_list tests/test_audit_ledh_clean_xla.py::test_phase5_streaming_sinkhorn_loop_state_matches_preedit_fixture
2 passed, 2 warnings in 5.18s

CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py
10 passed, 2 warnings in 8.35s

CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py::test_streaming_sinkhorn_recursion_vjp_matches_manual_and_tiny_autodiff
2 passed in 9.31s
```

The static audit remains `FAIL_CURRENT_ROUTE` for stopped-key partial-derivative
helpers and the total helper's local custom tape warning. This does not
invalidate the full-route Phase 7 run, but it does block broad clean-XLA claims.

## Post-Run Red-Team Note

The strongest misleading interpretation would be to say the preregistered FD
gate passed because the miss is tiny. That is wrong: the FD tolerance and step
rule were reviewed before execution, and the `log_obs_noise_scale` direction
did not pass them. The correct statement is that the owner accepted the bounded
result with an explicit waiver.

The other misleading interpretation would be to say the GPU/XLA route failed
structurally. That is also wrong. The route compiled, ran on GPU, reused one
concrete function, produced finite outputs, passed repeat determinism, and
selected the total-VJP full-route helper. The remaining failure is the
same-scalar derivative check for one parameter.

## Next Handoff

Phase 7 is promoted by owner acceptance with the FD waiver above. A future
repair plan may still isolate the `log_obs_noise_scale` discrepancy, but it is
no longer required before closing this clean-XLA bounded fixture program. Do
not use this waiver to claim HMC readiness or exact nonlinear likelihood
correctness.
