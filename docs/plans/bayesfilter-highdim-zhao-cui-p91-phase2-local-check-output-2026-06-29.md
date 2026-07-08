# P91 Phase 2 Local Check Output

Date: 2026-06-29

Status: `P91_PHASE2_LOCAL_CHECKS_PASS`

## Environment

- Python executable: `/home/chakwong/anaconda3/envs/tf-gpu/bin/python`
- Conda environment: `tf-gpu`
- CPU/GPU status: CPU-only pytest; `CUDA_VISIBLE_DEVICES=-1` was set before
  TensorFlow import.
- Seeds: `N/A`; deterministic algebraic fixtures only.

## Commands And Outputs

### Diff Hygiene

Command:

```bash
git diff --check -- bayesfilter/highdim/score_api.py bayesfilter/highdim/__init__.py tests/highdim/test_p91_batched_score_api.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

Output:

```text
<no output; exit code 0>
```

### Focused CPU-Only Pytest

Command:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p51_stable_score_api.py tests/highdim/test_p91_batched_score_api.py -q
```

Output summary:

```text
..........                                                               [100%]
10 passed, 2 warnings in 3.53s
```

Warning summary:

```text
TensorFlow Probability distutils Version deprecation warnings from environment imports.
```

## Nonclaims

These outputs are Phase 2 semantic/API evidence only. They do not establish FD
consistency, score identity, GPU/XLA readiness, HMC readiness, CPU/GPU
performance, package/release/CI readiness, default-policy readiness, exact
likelihood correctness, posterior correctness, or production readiness.
