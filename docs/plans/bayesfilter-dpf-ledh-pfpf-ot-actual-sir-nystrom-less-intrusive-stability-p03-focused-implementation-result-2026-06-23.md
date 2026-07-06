# P03 Focused Implementation Result

Date: 2026-06-23

Status: `P03_PASS_FOCUSED_TESTS_PENDING_CLAUDE_IMPLEMENTATION_REVIEW`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Accept the opt-in balanced Sinkhorn scaling gauge-normalization implementation for read-only implementation review | `PASS`: focused tests pass, balanced path is exercised, default `none` metadata is preserved, and P04 handoff is refreshed | `PASS`: no threshold change, default-policy change, positive-projection promotion, or broad file scope expansion | Unit and tiny compiled tests prove mechanics and metadata only; they do not prove repair effectiveness on the brittle row | Run mandatory Claude read-only implementation review, then P04 if review agrees | No GPU repair success, no default readiness, no ranking, no posterior correctness, no HMC readiness |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Is balanced Sinkhorn scaling gauge normalization implemented as a scoped opt-in path without changing default raw behavior? |
| Baseline/comparator | Existing raw Nystrom behavior and focused tests. |
| Primary pass criterion | `PASS`: focused tests pass; balanced path records positive gauge-shift/application diagnostics; default `scaling_normalization="none"` records zero balancing diagnostics; P04 artifact contract is ready. |
| Veto diagnostics | `PASS`: no focused test failure, default behavior change, missing metadata, threshold change, or broad unrelated edit in the scoped implementation. |
| Explanatory diagnostics | Local fixture outputs, metadata fields, and code diff. |
| Not concluded | No repair effectiveness, no default readiness, no scientific validity. |

## What Changed

Scoped files changed:

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`;
- `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`;
- `tests/test_nystrom_transport_tf.py`;
- `tests/test_actual_sir_nystrom_compiled_redo.py`.

Implementation summary:

- added opt-in `scaling_normalization` with allowed values `none` and
  `balanced`, defaulting to `none`;
- implemented batchwise `[B,N]` balancing after each full Sinkhorn `u/v`
  update:
  - `mean_log_u = mean(log(max(u, denominator_floor)), axis=1, keepdims=True)`;
  - `mean_log_v = mean(log(max(v, denominator_floor)), axis=1, keepdims=True)`;
  - `log_c = 0.5 * (mean_log_u - mean_log_v)`;
  - `c = exp(log_c)`;
  - `u <- u / c`, `v <- v * c`;
- added `max_abs_log_scaling_gauge_shift` and
  `scaling_normalization_applications` diagnostics to tensor diagnostics,
  Python diagnostics, compiled Nystrom rows, and benchmark transport metadata;
- added CLI `--nystrom-scaling-normalization {none,balanced}`.

This did not change rank/epsilon defaults, residual thresholds, paired
thresholds, kernel mode defaults, core solver defaults, or the default
`scaling_normalization="none"` route.

## Local Checks

Syntax check:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py
```

Result: `PASS`.

Focused CPU-hidden tests:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py
```

Log:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-tests-2026-06-23.log`

Result: `13 passed, 15109 warnings in 30.10s`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu`; CPU-hidden by `CUDA_VISIBLE_DEVICES=-1` before TensorFlow imports |
| GPU status | Intentionally hidden for focused CPU tests |
| Data/model | Tiny deterministic Nystrom fixtures and tiny actual-SIR compiled benchmark fixture |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for implementation mechanics and metadata. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Local gauge-shift diagnostics only; no performance or effectiveness comparison. |
| Default-readiness | `NO`. |
| Next evidence needed | Claude implementation review, then P04 trusted GPU brittle-row repair gate if review agrees. |

## Post-Run Red Team

Strongest alternative explanation: balanced gauge normalization can be
implemented correctly and still fail on the brittle row if the dominant failure
is low-rank kernel approximation quality or paired-likelihood semantic drift.

What would overturn this P03 decision: Claude finds an implementation boundary
or math/metadata defect, or P04 artifacts show the selected metadata was not
actually propagated to the serious run.

Weakest part of evidence: P03 uses tiny CPU-hidden fixtures; it is not repair
effectiveness evidence.

## Next Action

Run mandatory Claude read-only implementation review.  If review returns
`VERDICT: AGREE`, run P04 with trusted GPU context using GPU1 if available,
otherwise GPU0.
