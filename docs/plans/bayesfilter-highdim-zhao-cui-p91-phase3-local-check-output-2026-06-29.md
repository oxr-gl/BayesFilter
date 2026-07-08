# P91 Phase 3 Local Check Output

Date: 2026-06-29

Status: `P91_PHASE3_LIMITED_FD_HARNESS_RAN_MANIFEST_BLOCKED`

## Environment

- Python executable: `/home/chakwong/anaconda3/envs/tf-gpu/bin/python`
- Conda environment: `tf-gpu`
- CPU/GPU status: CPU-only pytest; `CUDA_VISIBLE_DEVICES=-1` was set before
  TensorFlow import.
- Data version: `N/A`; deterministic algebraic fixture.
- Seeds: `N/A`; deterministic algebraic fixture.
- FD manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-manifest-2026-06-29.json`

## Commands And Outputs

### Diff Hygiene

Command:

```bash
git diff --check -- tests/highdim/test_p91_fd_consistency_limited.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

Output:

```text
<no output; exit code 0>
```

### Focused CPU-Only Pytest

Command:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p90_derivative_carry_contract.py tests/highdim/test_p91_fd_consistency_limited.py -q
```

Output summary:

```text
......                                                                   [100%]
6 passed, 2 warnings in 5.52s
```

Warning summary:

```text
TensorFlow Probability distutils Version deprecation warnings from environment imports.
```

## Manifest Status

The pytest harness ran and wrote a valid manifest. The manifest status is:

```text
BLOCK_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY
```

The manifest status, not pytest success, is the authority for the FD gate.

Component summary:

| Component | Passed | Stable | Best max abs error | Best max rel error |
| --- | --- | --- | --- | --- |
| prior | false | false | `7.57154755559597e-13` | `7.57154755559597e-13` |
| transition | false | false | `5.245521328722802e-05` | `5.245521328722802e-05` |
| likelihood | false | false | `3.710864060479935e-08` | `1.080220107504868e-08` |
| negative_log_assembly | false | false | `5.245532266417996e-05` | `5.245532266417996e-05` |

The transition and negative-log assembly best rows narrowly exceed the
pre-registered `5e-5` absolute tolerance. The reviewed ladder-stability rule
also does not pass, so Phase 3 must close as limited-FD blocked/diagnostic
unless a new reviewed repair plan authorizes a changed fixture/tolerance/step
ladder.

## Nonclaims

These outputs do not establish full source-route FD consistency, score
identity, exact likelihood correctness, GPU/XLA readiness, HMC readiness,
benchmark results, package/release/CI readiness, default-policy readiness,
posterior correctness, or production readiness.
