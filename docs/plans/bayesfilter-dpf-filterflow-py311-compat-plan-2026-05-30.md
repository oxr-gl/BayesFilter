# Plan: Filterflow Python 3.11 Compatibility Patch

## Decision

`PLAN_REVISION_3_READY_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: can the local external JTT94/filterflow checkout be patched narrowly
for Python 3.11 / modern SciPy compatibility so the original LGSSM Section
5.1-style PF, regularized transform, and Kalman comparison paths can run
locally for future BayesFilter cross-implementation audits?

Primary comparator: upstream filterflow commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe` in
`.localsource/filterflow`.

Primary success criterion: a local compatibility branch of
`.localsource/filterflow` runs:

- simple-linear imports without caller-side monkeypatching;
- `ResamplingMethodsEnum.KALMAN` for a bounded simple-linear LGSSM command;
- `ResamplingMethodsEnum.MULTINOMIAL` for the same bounded command;
- `ResamplingMethodsEnum.REGULARIZED` for `epsilon` values `0.25`, `0.5`,
  and `0.75`.

Compatibility-preservation criterion: the patched triangular-solve wrapper must
agree with the corresponding direct modern SciPy `solve_triangular` call on
representative dense and masked-array inputs for lower/upper triangular cases.
The pre-patch wrapper is expected to fail under the current SciPy API; that
failure must be recorded as the compatibility bug being fixed rather than as a
numerical baseline.

Python 3.11 compatibility criterion: legacy pykalman 0.9.5 must be able to call
the removed `inspect.getargspec` name without requiring caller-side monkeypatches.
The only allowed shim is to alias `inspect.getargspec` to
`inspect.getfullargspec` when the old name is absent, before pykalman imports in
the simple-linear script path.

Veto diagnostics:

- compatibility patch changes algorithm semantics, model settings, resampling
  behavior, or reported scalar interpretation;
- filterflow checkout has unrelated dirty changes before patching;
- required patch touches BayesFilter production `bayesfilter/`, `tests/`,
  vendored student code, monograph chapters, or high-dimensional lane files;
- patch requires a dependency downgrade or global package mutation;
- Kalman, PF, or regularized transform bounded smoke commands fail after patch;
- outputs are non-finite;
- patched wrapper fails the dense or masked-array numerical equivalence checks
  against direct SciPy calls.
- Python 3.11 `inspect.getargspec` compatibility shim changes anything beyond
  exposing the old name as `inspect.getfullargspec` before legacy pykalman
  imports.

Explanatory diagnostics: patch diff, branch name, package versions, CPU-only
manifest, exact commands, Kalman output, PF output, regularized transform
outputs, and remaining warnings.

What will not be concluded: no BayesFilter OT-DPF correctness, no full paper
replication, no production readiness, no posterior correctness, and no claim
that the patched external checkout is unchanged upstream code.

## Scope

This task is an external-source compatibility patch.  The patch may modify
`.localsource/filterflow` because the user explicitly approved fixing
filterflow itself for future use.

The patch must be semantics-preserving: compatibility only.

## Allowed Write Set

- `.localsource/filterflow/scripts/base.py`
- `.localsource/filterflow/scripts/simple_linear_common.py`
- `.localsource/filterflow/scripts/simple_linear_smoothness.py`
- `.localsource/filterflow/` git metadata for a local compatibility branch
- `docs/plans/bayesfilter-dpf-filterflow-py311-compat-plan-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-py311-compat-result-2026-05-30.md`
- `experiments/dpf_implementation/reports/filterflow-py311-compat-2026-05-30.md`
- `experiments/dpf_implementation/reports/outputs/filterflow_py311_compat_2026-05-30.json`

## Forbidden Write Set

- production `bayesfilter/`
- `tests/`
- vendored student code
- monograph chapters under `docs/chapters/`
- high-dimensional nonlinear filtering lane files
- global Python or conda package directories
- dependency lockfiles outside the external filterflow checkout
- algorithmic filterflow code unrelated to Python/SciPy compatibility

## Proposed Patch

1. Create or switch to local branch `bayesfilter-py311-compat` in
   `.localsource/filterflow`.
   First verify the checkout is exactly
   `5d8300ba247c4c17e1a301a22560c24fd0670bfe` and clean.
2. Patch the pykalman/SciPy compatibility wrappers in:
   - `scripts/base.py`
   - `scripts/simple_linear_smoothness.py`
3. Preserve the wrapper's masked-array handling:
   - unwrap `a.data` and `b.data` when present.
4. Call modern `scipy.linalg.solve_triangular` using keyword arguments and do
   not pass the obsolete `debug` argument.
5. Keep the wrapper signature accepting `debug=None` so old pykalman calls still
   succeed.
6. Avoid changing model, resampling, likelihood, TensorFlow, or Sinkhorn logic.
7. Run wrapper-level diagnostics that compare the patched wrapper with direct
   modern SciPy calls on:
   - dense lower-triangular input;
   - dense upper-triangular input;
   - masked-array lower-triangular input where `.data` unwrapping matters.
   The diagnostic must assert finite results and `np.allclose` agreement.
8. Add the Python 3.11 compatibility shim:
   `inspect.getargspec = inspect.getfullargspec` only when the old attribute is
   absent.  Place it before the pykalman import in the simple-linear data path.
   This is a compatibility alias for legacy pykalman only; do not change
   pykalman, filterflow algorithm code, model settings, or resampling logic.

## Skeptical Pre-Execution Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| stale context | pass | Legacy-env result and current filterflow source were inspected on 2026-05-30. |
| wrong target | pass | Target is external filterflow compatibility, not BayesFilter implementation. |
| algorithm semantic drift | watch | Patch only wrapper calls to SciPy and inspect the diff before running. |
| hidden production drift | pass | Forbidden write set excludes production and tests. |
| monograph/highdim drift | pass | Forbidden write set excludes chapter and highdim files. |
| vendored contamination | pass | No vendored student code involved. |
| dependency drift | pass | Use existing `.localenv/filterflow-py311`; no new installs planned. |
| overclaiming smoke | pass | Result will state bounded smoke, not full paper replication. |
| artifact answers question | pass | Kalman/PF/regularized commands directly test the compatibility blockers. |
| wrapper semantic drift | watch | Add direct SciPy equivalence checks for dense and masked-array triangular solves. |
| getargspec shim semantic drift | watch | Shim only aliases a missing legacy inspect name to `inspect.getfullargspec` before pykalman imports. |

## Claude Review Protocol

Use Claude Code exactly as:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude must review the plan read-only and return `ACCEPT` or `REJECT` with
findings.  Codex audits Claude's findings.  If rejected and Codex agrees, patch
the plan and resubmit.  Loop until `ACCEPT` or max 5 iterations.  On iteration
5, accept only for user inspection unless there is a major blocker.

After execution, review the result with the same protocol.

## Verification Commands

- `git -C .localsource/filterflow status --short --branch`
- `git -C .localsource/filterflow rev-parse HEAD`
- `test "$(git -C .localsource/filterflow rev-parse HEAD)" = "5d8300ba247c4c17e1a301a22560c24fd0670bfe"`
- `git -C .localsource/filterflow diff`
- wrapper-level dense/masked triangular-solve equivalence command
- no-runtime-shim simple-linear import command
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=.cache/filterflow-mpl PYTHONPATH=.localsource/filterflow .localenv/filterflow-py311/bin/python -c "from scripts.simple_linear_common import get_data; from scripts.simple_linear_comparison import main; print('import_ok')"`
- targeted Kalman simple-linear command
- targeted PF simple-linear command
- targeted regularized transform simple-linear commands for `epsilon=0.25`,
  `0.5`, and `0.75`
- `python -m json.tool experiments/dpf_implementation/reports/outputs/filterflow_py311_compat_2026-05-30.json`
- `git status --short -- bayesfilter tests docs/chapters`
- `git diff --check`
- `git status --short --branch`

## Stop Conditions

- Claude rejects with a major blocker that Codex agrees with;
- filterflow checkout is dirty before patching in a way unrelated to this task;
- branch creation/switching would overwrite local changes;
- patch requires changing filterflow algorithm semantics;
- patch requires touching files beyond `scripts/base.py`,
  `scripts/simple_linear_common.py`, and `scripts/simple_linear_smoothness.py`;
- checkout is not exactly `5d8300ba247c4c17e1a301a22560c24fd0670bfe` before
  patching;
- Kalman branch still fails after the compatibility patch;
- wrapper-level dense or masked-array equivalence check fails;
- any forbidden write would be required;
- required verification fails in a way that invalidates the compatibility
  evidence.

## Claude Plan Review Iterations

Iteration 1: `REJECT`.

Codex audit: accepted.  The first plan proved execution but did not explicitly
prove the triangular-solve compatibility patch preserved the intended numerical
call semantics.  Revision 2 adds exact upstream commit gating, wrapper-level
dense/masked SciPy equivalence diagnostics, and a stop condition if the patch
extends beyond the two intended wrapper files.

Iteration 2: `ACCEPT`.

Execution then exposed an additional Python 3.11 compatibility blocker:
pykalman 0.9.5 calls removed `inspect.getargspec` during
`KalmanFilter.sample`.  Codex audit: this is still compatibility-only, but it
expands the needed write set beyond the accepted two-wrapper plan.  Revision 3
adds a minimal getargspec alias before the legacy pykalman import in the
simple-linear data path and expands the stop condition accordingly.
