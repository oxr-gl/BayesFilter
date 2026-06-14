# Result: Filterflow Python 3.11 Compatibility Patch

## Decision

`EXECUTED_AND_READY_FOR_RESULT_REVIEW`

The local external filterflow checkout now has a narrow compatibility branch
that runs the simple-linear LGSSM Kalman, PF, and regularized-transform paths
under Python 3.11 / modern SciPy.

## Evidence Contract Status

Question: can the local external JTT94/filterflow checkout be patched narrowly
for Python 3.11 / modern SciPy compatibility so the original LGSSM Section
5.1-style PF, regularized transform, and Kalman comparison paths can run
locally for future BayesFilter cross-implementation audits?

Status: yes, for the bounded simple-linear LGSSM commands in this result.

Primary comparator: upstream filterflow commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

Patched branch: `bayesfilter-py311-compat`.

What is not concluded: this is not a full Corenflos Section 5.1 reproduction,
not BayesFilter OT-DPF correctness, not posterior correctness, and not
production readiness.

## Claude Review

Plan review:

| Iteration | Claude status | Codex audit |
| --- | --- | --- |
| 1 | `REJECT` | Accepted. Added wrapper-level dense/masked triangular-solve equivalence checks and exact upstream commit gate. |
| 2 | `ACCEPT` | Accepted for the two SciPy wrapper changes. |
| 3 | `ACCEPT` | Accepted after execution exposed the Python 3.11 `inspect.getargspec` pykalman blocker and the plan was revised to allow a minimal single-site shim. |

Result review:

| Iteration | Claude status | Codex audit |
| --- | --- | --- |
| 1 | `REJECT` | Accepted. Added exact command ledger, raw status/diff evidence, and removed stale pending status. |
| 2 | `REJECT` | Accepted as bookkeeping-only. Artifacts showed only the prior rejection and no current review iteration. |
| 3 | `ACCEPT` | Accepted. Minor note: wrapper-equivalence command is summarized, but cases, outputs, and cross-artifact consistency are sufficient for compatibility-only evidence. |

## Patch Summary

Only the external checkout under `.localsource/filterflow` was patched.

Changed files:

- `.localsource/filterflow/scripts/base.py`
- `.localsource/filterflow/scripts/simple_linear_common.py`
- `.localsource/filterflow/scripts/simple_linear_smoothness.py`

Compatibility changes:

- Kept legacy wrapper signatures accepting `debug=None`.
- Stopped forwarding obsolete `debug` as a positional argument to modern
  `scipy.linalg.solve_triangular`.
- Called `solve_triangular` with explicit keyword arguments:
  `trans`, `lower`, `unit_diagonal`, `overwrite_b`, and `check_finite`.
- Added a Python 3.11 shim in `scripts/simple_linear_common.py`:
  `inspect.getargspec = inspect.getfullargspec` only when `getargspec` is
  absent, before importing legacy pykalman.

No filterflow model, likelihood, resampling, Sinkhorn, TensorFlow, or reported
scalar logic was intentionally changed.

Diff summary:

```text
scripts/base.py                     | 7 ++++---
scripts/simple_linear_common.py     | 5 +++++
scripts/simple_linear_smoothness.py | 6 ++++--
3 files changed, 13 insertions(+), 5 deletions(-)
```

Patch excerpt:

```diff
-        return sc_solve(a, b, trans, lower, unit_diagonal,
-                        overwrite_b, debug, check_finite)
+        return sc_solve(a, b, trans=trans, lower=lower,
+                        unit_diagonal=unit_diagonal,
+                        overwrite_b=overwrite_b,
+                        check_finite=check_finite)
```

```diff
+import inspect
 import numpy as np
+
+if not hasattr(inspect, "getargspec"):
+    inspect.getargspec = inspect.getfullargspec
+
 import pykalman
```

## Compatibility Verification

Pre-patch/source gate:

```bash
git -C .localsource/filterflow rev-parse HEAD
```

Output: `5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

```bash
git -C .localsource/filterflow status --short --branch
```

Pre-patch output: `## master...origin/master`.

Post-patch output:

```text
## bayesfilter-py311-compat
 M scripts/base.py
 M scripts/simple_linear_common.py
 M scripts/simple_linear_smoothness.py
```

Wrapper-level equivalence check:

Command:

```bash
.localenv/filterflow-py311/bin/python -c 'exec("""... dense/upper/masked FakeKF triangular-solve equivalence check ...""")'
```

- `scripts.base.kf_loglikelihood` wrapper:
  - dense lower triangular: pass;
  - dense upper triangular: pass;
  - masked lower triangular: pass.
- `scripts.simple_linear_smoothness.kf_loglikelihood` wrapper:
  - dense lower triangular: pass;
  - dense upper triangular: pass;
  - masked lower triangular: pass.

Representative output:

```text
base dense_lower ok [[0.5, 1.0], [1.833333, 2.333333]]
base dense_upper ok [[0.25, 0.666667], [2.0, 2.666667]]
base masked_lower ok [[0.5, 1.0], [1.833333, 2.333333]]
smoothness dense_lower ok [[0.5, 1.0], [1.833333, 2.333333]]
smoothness dense_upper ok [[0.25, 0.666667], [2.0, 2.666667]]
smoothness masked_lower ok [[0.5, 1.0], [1.833333, 2.333333]]
```

Compile check:

```bash
python -m py_compile \
  .localsource/filterflow/scripts/base.py \
  .localsource/filterflow/scripts/simple_linear_common.py \
  .localsource/filterflow/scripts/simple_linear_smoothness.py
```

Status: pass.

No-runtime-shim import check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=.cache/filterflow-mpl \
PYTHONPATH=.localsource/filterflow \
.localenv/filterflow-py311/bin/python -c \
"from scripts.simple_linear_common import get_data; from scripts.simple_linear_comparison import main; print('import_ok')"
```

Output: `import_ok`.

## Simple-Linear LGSSM Results

Run settings:

| Field | Value |
| --- | --- |
| `T` | `150` |
| `batch_size` | `100` |
| `n_particles` | `25` |
| `data_seed` | `111` |
| `filter_seed` | `555` |
| resampling threshold | `0.5` |
| CPU setting | `CUDA_VISIBLE_DEVICES=-1` |
| Matplotlib cache | `MPLCONFIGDIR=.cache/filterflow-mpl` |

Kalman command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=.cache/filterflow-mpl \
PYTHONPATH=.localsource/filterflow \
.localenv/filterflow-py311/bin/python -c \
"from scripts.simple_linear_comparison import main; from scripts.simple_linear_common import ResamplingMethodsEnum; main(ResamplingMethodsEnum.KALMAN, 0.5, T=150, batch_size=100, n_particles=25, data_seed=111, filter_seed=555, savefig=False)"
```

Kalman output, now unblocked:

| theta | log likelihood per time |
| --- | ---: |
| 0.250 | -3.052 |
| 0.500 | -2.958 |
| 0.750 | -3.015 |

PF command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=.cache/filterflow-mpl \
PYTHONPATH=.localsource/filterflow \
.localenv/filterflow-py311/bin/python -c \
"from scripts.simple_linear_comparison import main; from scripts.simple_linear_common import ResamplingMethodsEnum; main(ResamplingMethodsEnum.MULTINOMIAL, 0.5, T=150, batch_size=100, n_particles=25, data_seed=111, filter_seed=555, savefig=False)"
```

Multinomial PF output:

| theta | mean | std |
| --- | ---: | ---: |
| 0.250 | -4.077 | 0.176 |
| 0.500 | -3.818 | 0.153 |
| 0.750 | -3.938 | 0.198 |

Regularized transform command template:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=.cache/filterflow-mpl \
PYTHONPATH=.localsource/filterflow \
.localenv/filterflow-py311/bin/python -c \
"from scripts.simple_linear_comparison import main; from scripts.simple_linear_common import ResamplingMethodsEnum; main(ResamplingMethodsEnum.REGULARIZED, 0.5, T=150, batch_size=100, n_particles=25, data_seed=111, filter_seed=555, savefig=False, resampling_kwargs=dict(epsilon=EPS, scaling=0.9, convergence_threshold=1e-3))"
```

Regularized transform output with `epsilon=0.25`:

| theta | mean | std |
| --- | ---: | ---: |
| 0.250 | -4.077 | 0.179 |
| 0.500 | -3.815 | 0.155 |
| 0.750 | -3.930 | 0.193 |

Regularized transform output with `epsilon=0.5`:

| theta | mean | std |
| --- | ---: | ---: |
| 0.250 | -4.078 | 0.179 |
| 0.500 | -3.817 | 0.154 |
| 0.750 | -3.938 | 0.190 |

Regularized transform output with `epsilon=0.75`:

| theta | mean | std |
| --- | ---: | ---: |
| 0.250 | -4.078 | 0.178 |
| 0.500 | -3.818 | 0.154 |
| 0.750 | -3.943 | 0.189 |

## Run Manifest

| Field | Value |
| --- | --- |
| Filterflow path | `.localsource/filterflow` |
| Upstream commit | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| Branch | `bayesfilter-py311-compat` |
| Environment | `.localenv/filterflow-py311` |
| Python | `3.11.14` |
| NumPy | `1.26.4` |
| SciPy | `1.17.1` |
| TensorFlow | `2.19.1` |
| TFP | `0.25.0` |
| pykalman | `0.9.5` |
| CPU-only command intent | `CUDA_VISIBLE_DEVICES=-1` |

Note: TensorFlow still emitted CUDA plugin/cuInit warnings despite
`CUDA_VISIBLE_DEVICES=-1`.  The commands were run as CPU-intended smoke checks;
no GPU evidence is claimed.

## Decision Table

| Decision | Status |
| --- | --- |
| Exact upstream commit verified before patching | pass |
| Local compatibility branch created | pass |
| Patch limited to allowed filterflow files | pass |
| Wrapper dense/masked equivalence checks | pass |
| No-runtime-shim simple-linear import | pass |
| Kalman branch | pass |
| Multinomial PF branch | pass |
| Regularized transform branch | pass |
| Full paper reproduction | not claimed |

## Final Verification Snapshot

```bash
git -C .localsource/filterflow diff --check
```

Status: pass.

```bash
git status --short -- bayesfilter tests docs/chapters
```

Status: no output; no production, test, or chapter edits.

## Next Justified Action

Use `bayesfilter-py311-compat` as the external implementation baseline for the
cross-implementation LGSSM audit.  The next audit should compare filterflow
Kalman/PF/regularized outputs against BayesFilter on matched LGSSM settings,
particle counts, seeds, resampling trigger, `epsilon`, `scaling`, and Sinkhorn
stopping policy.
