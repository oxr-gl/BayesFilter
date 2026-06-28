# P04C3 Subplan: Streaming Comparator Robustness Diagnostic

Date: 2026-06-26

Status: `P04C3_CLOSED_BLOCKED_COMPARATOR_INVALID_FOR_P04C`

## Phase Objective

Determine the smallest reviewed repair or diagnostic that can make the
range-bearing streaming comparator valid for seed `84101` on GPU, or establish
that P04C calibration cannot use the current streaming comparator on this
fixture.

P04C3 is about comparator validity. It must not tune SVD-Nystrom, freeze a
threshold, drop seed `84101`, resume P04C calibration, launch P05, or promote
the method.

The implementation hypothesis for this phase is narrow: replace explicit
posterior precision inversion in the shared LEDH flow core with a Cholesky
solve against identity on the already-stabilized posterior precision path. The
repair is intended to avoid the GPU `MatrixInverse` path without changing
stabilization policy, jitter amount, fixture, threshold, or SVD-Nystrom policy.
The focused tests and GPU canary must validate that this solve-route change is
acceptable for the comparator-validity purpose of P04C3; the subplan does not
claim a general mathematical proof of equivalence.

## Entry Conditions Inherited From Previous Phase

- P04C emitted `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`.
- P04C1 emitted `P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`.
- P04C2A emitted `P04C2A_PASS_TO_P04C2_RERUN`.
- Repaired P04C2 emitted `P04C2_GPU_DEVICE_STREAMING_INVALID`.
- P04C1 CPU/no-TF32/no-JIT seed `84101` streaming control passed.
- Repaired P04C2 GPU/no-TF32/no-JIT seed `84101` streaming row failed with a
  structured TensorFlow `InvalidArgumentError` at `MatrixInverse`.
- P04C calibration remains blocked.
- P05 remains blocked.
- No HMC readiness claim is in scope.

## Required Artifacts

- P04C3 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c3-streaming-comparator-robustness-subplan-2026-06-26.md`
- P04C3 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c3-streaming-comparator-robustness-result-2026-06-26.md`
- Repaired P04C2 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-repaired-streaming-gpu-tf32-jit-isolation-result-2026-06-26.md`
- P04C2 summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-summary-2026-06-26.json`
- If implementation repair is authorized by this subplan after review:
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  - focused tests under `tests/`
  - canary JSON:
    `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101-2026-06-26.json`
  - canary Markdown:
    `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101-2026-06-26.md`
  - canary log:
    `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101.log`
- Updated execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-execution-ledger-2026-06-25.md`
- Updated Claude review ledger if Claude is used:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-claude-review-ledger-2026-06-25.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-stop-handoff-2026-06-25.md`

## Required Checks, Tests, And Reviews

- Local pre-run audit:
  - Confirm the research question is comparator validity, not SVD-Nystrom
    quality or threshold calibration.
  - Confirm the current failure occurs in the streaming comparator flow core at
    posterior covariance inversion.
  - Confirm the planned repair is minimal and scoped to replacing explicit
    matrix inverse with Cholesky solve for the same stabilized precision matrix.
  - Confirm the planned repair does not alter stabilization policy, LEDH
    jitter amount, fixture, threshold, dtype, seed, particle count, or
    SVD-Nystrom policy.
  - Confirm all diagnostic rows remain excluded from P04C threshold scale
    summaries.
- Claude read-only review is required before source edits or GPU rows. Claude
  may review exact P04C3 subplan and exact P04C2/P04C2A result documents under
  standing approval. Claude may not read source code, tests, logs, credentials,
  model files, or unrelated paths without explicit approval; may not run
  commands; may not edit files; and may not authorize promotion/default/
  scientific/HMC boundaries.
- If the reviewed plan authorizes implementation repair, run focused tests that
  cover:
  - existing LEDH flow correctness on regular cases;
  - behavior on a synthetic ill-conditioned posterior precision case;
  - unchanged public route defaults unless the repair explicitly changes a
    documented comparator regularization target.
- Required local commands after implementation:

```bash
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_svd_nystrom_range_bearing_gate.py -q
```

- Exact trusted GPU canary, only after focused tests pass:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route streaming --seed 84101 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --paired-threshold-mode record-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode disabled --no-jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04C3-GPU-NOTF32-NOJIT-STREAMING-CANARY-SEED84101 --capture-route-exceptions --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101-2026-06-26.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101-2026-06-26.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101.log 2>&1
```

`${GPU}` and `${GPU_NOTE}` must come from the immediately preceding trusted GPU
preflight. Use GPU1 if suitable, otherwise GPU0.
- The canary must be exactly the predeclared seed/device/mode row
  `gpu-notf32-nojit-streaming-canary-seed84101`: seed `84101`, GPU execution,
  TF32 disabled, JIT off, route `streaming`, `T=20`, `N=4096`, `float32`,
  active-all transport, and the exact JSON/Markdown/log trio listed above.
  Only if that row becomes structured-valid may a reviewed follow-up decide
  whether to rerun the full P04C2/P04C panel.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the streaming comparator be made deterministic-valid on seed `84101` GPU execution by a principled minimal numerical robustness repair, or is the comparator invalid for P04C calibration on this fixture? |
| Baseline/comparator | P04C1 CPU/no-TF32/no-JIT streaming pass and repaired P04C2 GPU/no-TF32/no-JIT streaming exception on seed `84101`. |
| Primary criterion | Focused tests pass and a reviewed repair/diagnostic either produces a structured-valid GPU/no-TF32/no-JIT streaming canary for seed `84101`, or records a comparator-invalid blocker with exact evidence. |
| Veto diagnostics | Unreviewed source edit, tuning SVD-Nystrom, changing thresholds, dropping seed `84101`, treating diagnostics as calibration rows, default behavior drift without review, malformed artifacts, or unsupported promotion/scientific/HMC claims. |
| Explanatory diagnostics | Matrix inverse exception type, solve-route metadata if added, finite route status, ESS, log likelihood, runtime. |
| Not concluded | No SVD-Nystrom rejection, no threshold freeze, no P04C resume, no P05 launch, no default promotion, no posterior correctness, no HMC readiness, no statistical superiority. |
| Artifact | P04C3 result and exact canary/diagnostic artifacts. |

## Forbidden Claims And Actions

- Do not tune SVD-Nystrom or change the locked candidate policy.
- Do not change LEDH jitter, fixture, seed, dtype, particle count, transport
  policy, or threshold as part of P04C3.
- Do not change stabilization policy or regularization target as part of P04C3.
- Do not drop seed `84101` or count it as a non-exceedance.
- Do not resume P04C calibration rows `84102..84111`.
- Do not freeze or validate a nonlinear threshold.
- Do not launch P05.
- Do not use P04C3 as method-quality or promotion evidence.
- Do not send source code or tests to Claude without explicit approval.
- Do not make default, product, HMC-readiness, posterior-correctness,
  statistical-superiority, or broad scientific-validity claims.

## Exact Next-Phase Handoff Conditions

- `P04C3_PASS_STREAMING_COMPARATOR_REPAIRED_TO_P04C2_RERUN`: focused tests pass
  and the exact seed `84101` GPU/no-TF32/no-JIT streaming canary writes the
  predeclared JSON/Markdown/log trio and is structured-valid.
- `P04C3_BLOCKED_COMPARATOR_INVALID_FOR_P04C`: reviewed diagnostics show the
  current streaming comparator remains invalid on the P04C fixture, or repair
  would require changing the comparator target beyond this lane.
- `P04C3_BLOCKED_REVIEW_SCOPE`: source/test review is needed from Claude but
  not approved.
- `P04C3_BLOCKED_TEST_FAILURE`: focused tests fail in a way not fixable inside
  the reviewed P04C3 scope.

Any handoff still requires a later reviewed subplan before P04C calibration can
resume, a threshold can be frozen, seed `84101` can be handled, or P05 can run.

## Stop Conditions

- The repair would change SVD-Nystrom policy or thresholds.
- The repair would change the LEDH jitter amount, stabilization policy, or
  regularization target rather than only the solve route for the
  already-stabilized posterior precision.
- The repair would change the comparator mathematical target without explicit
  owner approval and result labeling.
- A GPU canary artifact is missing, malformed, route/device mismatched, or
  requires unplanned command changes after seeing results.
- Continuing would require source disclosure to Claude without approval,
  package installation, network fetches, commits, pushes, destructive actions,
  P04C calibration continuation, P05 execution, threshold freeze, default/
  product/scientific/HMC authorization, or dropping seed `84101`.

## End-Of-Phase Requirements

At P04C3 close, Codex must:

1. run required local checks;
2. write the P04C3 result/close record;
3. update the execution ledger and stop handoff;
4. draft or refresh the next subplan only if the result justifies one;
5. review any material next subplan locally and, when authorized and useful,
   with Claude.

## Local Self-Review Of This Subplan

Skeptical audit:

- Wrong baseline: P04C3 compares GPU streaming invalidity to the P04C1 CPU
  control, not to SVD-Nystrom quality.
- Proxy metric: route validity is a comparator-validity gate, not a promotion
  criterion.
- Missing stop conditions: source-review scope, default-behavior drift,
  artifact malformedness, and calibration continuation are explicit stops.
- Unfair comparison: P04C3 does not rank methods or use diagnostic rows in a
  threshold summary.
- Hidden assumption: a small numerical repair may be possible, but success must
  be shown by tests and a GPU canary before any calibration rerun.
- Implementation specificity: the only planned code repair is replacing
  explicit inverse with Cholesky solve on the already-stabilized precision
  path; changing jitter, stabilization policy, regularization target, or
  thresholds is out of scope.
- Environment mismatch: GPU canary requires trusted GPU preflight and GPU1 if
  available otherwise GPU0.
- Artifact fit: exact P04C3 result and canary artifacts must answer comparator
  validity, not method promotion.
