# Phase 5 Result: Compiled Benchmark Ladder

Date: 2026-06-15

## Status

`PASSED_DESCRIPTIVE_BENCHMARKS`

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | What are graph/compiled CPU/GPU timing and capacity characteristics for experimental batched LEDH-PFPF-OT value and value+score? |
| Candidate/mechanism | Experimental TensorFlow batched value and value+score wrappers with `tf.function(jit_compile=True)`. |
| Expected failure mode | GPU timing accidentally run uncompiled, wrong device placement, or benchmark interpreted as production/default evidence. |
| Promotion criterion | Correctness rerun passed; benchmark artifacts record device/JIT/shape/compile/warm-call metadata; GPU timings are compiled and trusted. |
| Promotion veto | Uncompiled GPU timing, wrong device, missing artifact metadata, missing correctness rerun, or unsupported speed/production claim. |
| What must not be concluded | No universal GPU speedup, no production/default readiness, no posterior validity, no HMC/NeuTra readiness, no classical PF score correctness. |

## Checks Run

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_ledh_pfpf_ot_tf.py
```

Result: `20 passed`.

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_benchmark_harness.py
```

Result: `8 passed`.

Trusted GPU probes:

- `nvidia-smi` saw two RTX 4080 SUPER GPUs.
- TensorFlow 2.20.0 saw two physical/logical GPUs in trusted context.

## Benchmark Table

All rows below are warm-call median seconds. Compile/first-call time is recorded
in the JSON artifacts and excluded from warm-call medians.

| Mode | Transport | B | CPU Median | GPU Median | Interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| value | active raw OT | 20 | 0.0004247 | 0.0011840 | GPU slower at this small batch |
| value | active raw OT | 256 | 0.0036069 | 0.0012761 | GPU descriptively faster |
| value | active raw OT | 4096 | 0.0336660 | 0.0016139 | GPU descriptively faster |
| value+score | no resampling/raw | 20 | 0.0014570 | 0.0017820 | GPU slower at this small batch |
| value+score | no resampling/raw | 256 | 0.0099436 | 0.0018915 | GPU descriptively faster |

Compiled value parity:

| Comparator | B | Max Absolute Delta | Status |
| --- | ---: | ---: | --- |
| batched compiled value vs scalar compiled value loop | 20 | `2.220446049250313e-16` | pass |

## Artifacts

Benchmark harness:

- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_cpu_gpu.py`

CPU artifacts:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-cpu-b20-t3-np4-d1-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-cpu-b256-t3-np4-d1-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-cpu-b4096-t3-np4-d1-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-score-cpu-b20-t3-np4-d1-noresampling-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-score-cpu-b256-t3-np4-d1-noresampling-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-parity-cpu-b20-t3-np4-d1-2026-06-15.json`

GPU artifacts:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-gpu1-b20-t3-np4-d1-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-gpu1-b256-t3-np4-d1-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-gpu1-b4096-t3-np4-d1-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-score-gpu1-b20-t3-np4-d1-noresampling-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-score-gpu1-b256-t3-np4-d1-noresampling-2026-06-15.json`

Each JSON has a paired markdown summary.

## Claude Review

Claude reviewed a compact benchmark interpretation digest and returned:

```text
VERDICT: AGREE
```

Accepted wording:

- descriptive single-shape evidence under this trusted runtime configuration;
- no universal GPU speedup claim;
- no production/default readiness claim.

## Decision Table

| Decision | Primary Criterion Status | Veto Diagnostic Status | Main Uncertainty | Next Justified Action | Not Concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 6 closeout | Passed | No Phase 5 veto fired | Tiny fixture only; active score path not benchmarked for FD-equivalence semantics | Write closeout with production gaps and nonclaims | Universal speedup, production readiness, posterior validity, HMC/NeuTra readiness, classical PF score correctness |

## Handoff To Phase 6

Phase 6 should summarize the final experimental readiness and remaining
production-default gaps. It must not promote this experimental lane into the
public API or production default.
