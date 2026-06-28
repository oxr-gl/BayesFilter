# P01 Result: Paired Quality Harness Implementation

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | P01 passed; proceed to P02 trusted GPU paired medium quality screen. |
| Primary criterion status | Passed: wrapper was added, compiles, exposes CLI help, targets the existing streaming precision wrapper, and preserves the repaired evidence contract. |
| Veto diagnostic status | No P01 veto fired. |
| Main uncertainty | The wrapper has not yet run TensorFlow/GPU children; P02 is the first numerical quality gate. |
| Next justified action | Run the P02 trusted GPU command from the subplan. |
| What is not concluded | No GPU validity, no downstream quality pass, no posterior correctness, no HMC readiness, no speedup, and no statistical ranking. |

## Checks Actually Run

```bash
python -m py_compile docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py
```

```bash
python -m py_compile docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py
```

```bash
python -c "import pathlib; p=pathlib.Path('docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py'); text=p.read_text(); required=[...]; missing=[r for r in required if r not in text]; assert not missing, missing"
```

```bash
python docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py --help
```

## Implemented Artifact

- `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py`

## Evidence Preserved By The Wrapper

| Requirement | Status |
| --- | --- |
| Existing child route | Targets `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py`. |
| Paired seeds | Builds deterministic seed list from `--num-seeds`, `--base-seed`, and `--seed-stride`. |
| Drift formula | Records `max(abs(candidate - reference) / max(1.0, abs(reference))) per output array and paired seed`. |
| Required outputs | Requires `log_likelihood`, `filtered_means`, `filtered_variances`, and `ess_by_time`. |
| Per-seed/per-output drift | Stores compact drift records in parent JSON; large output arrays stay in child artifacts. |
| Output array presence | Adds explicit parent `output_arrays_screen` from child hard-screen metadata. |
| Default metadata assertions | Checks `precision_default_policy`, `default_execution_target`, `default_algorithm_target`, `default_target_status`, dtype fields, TF32 mode, and TF32 execution flag. |
| Nonclaims | Records no posterior correctness, HMC readiness, speedup, statistical ranking, dense Sinkhorn equivalence, or public API readiness. |

## Post-Run Red-Team Note

Strongest alternative explanation: a wrapper can compile while still failing on
real TensorFlow child artifacts or trusted GPU placement.

What would overturn P01: P02 showing that the wrapper misreads child payloads,
omits required per-output fields, or fails to distinguish harness/environment
failure from candidate drift failure.

Weakest part of the evidence: P01 is static/compile evidence only.

