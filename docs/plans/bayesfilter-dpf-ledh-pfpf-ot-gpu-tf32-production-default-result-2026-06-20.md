# BayesFilter DPF LEDH-PFPF-OT GPU TF32 Production Default Result - 2026-06-20

## Decision

GPU-oriented LEDH-PFPF-OT TF32 is promoted to the BayesFilter DPF transport
production/default target by explicit owner directive on 2026-06-20.

The default route is:

- TensorFlow / TensorFlow Probability implementation;
- GPU execution target;
- `float32` tensors;
- TensorFlow TF32 execution enabled;
- streaming/chunked transport where applicable;
- explicit FP64 and FP32-no-TF32 arms retained as reference, comparison, smoke,
  or fallback modes.

The historical module path under `experiments/dpf_implementation` is not a
demotion signal for this route.  Public API exposure remains separately gated.

## Skeptical Plan Audit

- Wrong baseline risk: do not treat CPU or FP64 reference arms as the production
  target.  They remain reference/comparison arms.
- Proxy-metric risk: prior TF32, smoke, and scale diagnostics motivate the
  owner directive but are not recast as proof of posterior correctness,
  statistical superiority, or HMC readiness.
- Missing stop-condition risk: future agents should stop only if a new
  reviewed artifact or human directive supersedes this default, or if a hard
  numerical/device invariant fails for the route under test.
- Environment mismatch risk: GPU/CUDA failures from untrusted or sandboxed
  runs remain sandbox evidence until rerun in a trusted context.
- Artifact mismatch risk: old benchmark artifacts may still say "no production
  default readiness claim" because they were historical records.  New live
  route metadata and generators now record the owner default directive.

Audit status: passed for a policy/metadata promotion by owner directive.  Not
used as proof of posterior correctness, HMC readiness, algorithmic superiority,
dense Sinkhorn equivalence, or public API readiness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the repository default be made unambiguous for future agents? |
| Baseline/comparator | Prior scoped TF32 default policy and current governance files. |
| Primary criterion | Governance and live LEDH-PFPF-OT metadata record GPU-oriented LEDH-PFPF-OT TF32 as production/default by owner directive. |
| Veto diagnostics | Policy still says CPU or experimental/no-production-default is the DPF default; live route metadata contradicts the owner directive; reference controls are removed; tests fail. |
| Explanatory diagnostics | Prior GPU TF32 smoke/precision/capacity artifacts and benchmark metadata. |
| Not concluded | No posterior correctness, HMC readiness, statistical superiority, dense Sinkhorn equivalence, or public API readiness. |
| Preservation artifact | This result note plus code/governance diffs. |

## What Changed

- `AGENTS.md` now states that the repo default execution target is GPU, and
  that DPF transport work defaults to GPU-oriented LEDH-PFPF-OT TF32.
- `CLAUDE.md` mirrors the same default execution target for read-only
  reviewers/workers.
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  now reports `production_ledh_pfpf_ot_gpu_tf32`,
  `default_execution_target=gpu`, and
  `default_target_status=production_default_by_owner_directive`.
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  now documents the route as the default production target, while preserving
  separate public API and HMC/posterior gates.
- Live benchmark/correctness generators for the route now emit
  `production/default target by owner directive` rather than the stale
  "no production default readiness claim" wording.
- Focused tests assert the new precision/default metadata.

## Verification

Syntax check passed:

```bash
python -m py_compile \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_efficiency_matrix.py \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py \
  docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py \
  tests/test_experimental_batched_ledh_pfpf_ot_tf.py \
  tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
```

Focused unit tests passed:

```bash
pytest -q \
  tests/test_experimental_batched_ledh_pfpf_ot_tf.py \
  tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
```

Observed result: `36 passed`.  TensorFlow/gast emitted Python 3.13
deprecation warnings during graph conversion; no test failure or policy veto
was observed.

Live-code stale-phrase check passed for the touched route files:

```bash
rg -n "no production default readiness claim|no production/default readiness|not production/default readiness" \
  experiments/dpf_implementation/tf_tfp/filters \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_efficiency_matrix.py \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py \
  docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py \
  tests/test_experimental_batched_ledh_pfpf_ot_tf.py
```

Observed result: no matches.  Historical benchmark/result artifacts were not
rewritten.

## Decision Table

| Field | Status |
| --- | --- |
| Default-policy decision | Adopted by owner directive for DPF transport work. |
| Primary criterion | Governance and live metadata patched to record GPU-oriented LEDH-PFPF-OT TF32 as production/default. |
| Veto diagnostics | No reference controls removed; FP64/FP32-no-TF32 remain explicit arms. |
| Main uncertainty | Scientific and HMC readiness gates remain open and must be tested separately. |
| Next justified action | Future DPF transport work should start from GPU-oriented LEDH-PFPF-OT TF32 unless a reviewed artifact or human directive supersedes it. |
| What is not concluded | No posterior correctness, HMC readiness, statistical superiority, dense Sinkhorn equivalence, or public API readiness. |

## Inference Status

| Evidence class | Interpretation |
| --- | --- |
| Hard veto screen | No hard veto for policy/metadata promotion. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Prior benchmark timing and drift records remain descriptive. |
| Default-readiness | Default route is ready by owner directive; scientific/HMC readiness claims remain separately gated. |
| Next evidence needed | Trusted GPU route checks and HMC/posterior diagnostics for any claim beyond default execution policy. |

## Post-Run Red-Team Note

Strongest alternative explanation: future agents may confuse "production/default
target by directive" with "scientifically certified for every posterior/HMC use."

What would overturn the decision: a human owner directive superseding this
policy, or a reviewed hard-veto artifact showing the GPU TF32 route is invalid
for the intended DPF default target.

Weakest part of the evidence: this is a policy and metadata promotion, not a new
long-run validation.
