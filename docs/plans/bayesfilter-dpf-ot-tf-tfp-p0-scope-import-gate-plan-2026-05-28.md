# P0 Plan: Scope And Import Gate

Date: 2026-05-28

## Evidence Contract

Question: can the TF/TFP OT-DPF lane establish a clean implementation scope and
NumPy import gate before code is added?

Primary criterion: root governance is read, implementation is scoped to
`experiments/dpf_implementation/tf_tfp/`, CPU-only import discipline is stated,
and the NumPy gate is executable.

Veto diagnostics: forbidden write scope, missing CPU-only rule, or acceptance of
NumPy implementation imports.

What must not be concluded: no implementation, production, posterior, HMC, or
monograph claim.

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-plan-2026-05-28.md`

## Outputs

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p0-scope-import-gate-result-2026-05-28.md`

The result note must include a decision table, skeptical audit outcome, CPU-only
manifest with `pre_import_cuda_visible_devices=-1`, exact TF/TFP import probe
command/output summary, NumPy import-gate command/result, unrelated dirty-file
summary, structured blocker status, and non-conclusions.

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p0-*-2026-05-28.md`
- `experiments/dpf_implementation/tf_tfp/`

## Forbidden Write Set

`bayesfilter/`, `tests/`, `docs/chapters/`, vendored code, high-dimensional
lane files, production API files, and existing NumPy prototype modules.

## Skeptical Audit Checklist

Check stale context, wrong backend, NumPy implementation drift, proxy overclaim,
missing stop conditions, production drift, monograph drift, vendored-code
contamination, high-dimensional-lane contamination, and artifact fitness.

## Stop Conditions

Stop if TF/TFP import is unavailable under CPU-only mode or if the import gate
cannot be expressed without broad exceptions.

If a stop condition fires, write the same P0 result artifact with decision
`P0_STRUCTURED_BLOCKER` and include the failed command, evidence, and whether
later phases may continue.

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -c "import os; pre=os.environ.get('CUDA_VISIBLE_DEVICES'); assert pre == '-1'; import tensorflow as tf; import tensorflow_probability as tfp; assert pre == '-1'; print({'pre_import_cuda_visible_devices': pre, 'tensorflow': tf.__version__, 'tfp': tfp.__version__, 'gpu_devices_visible': tf.config.list_physical_devices('GPU')})"
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or max
5 iterations.
