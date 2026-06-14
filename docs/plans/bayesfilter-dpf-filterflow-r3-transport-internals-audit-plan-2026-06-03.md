# BayesFilter DPF Filterflow R3 Transport Internals Audit Plan

## Evidence Contract

Question: after R3 replay localized the remaining discrepancy to BayesFilter-computed RegularisedTransform transport matrices, which single-step transport internal first diverges from the executable filterflow reference?

Comparator: local executable `.localsource/filterflow` RegularisedTransform internals, evaluated in a non-mutating subprocess on the same traced pre-resampling particles and log weights.

Primary criterion: identify the first transport-internal field, in execution order, whose BayesFilter value differs from filterflow on selected R3 rows. This is a difference audit only.

Veto diagnostics: filterflow trace no longer reproduces official filterflow output, filterflow internals cannot be executed without editing `.localsource/filterflow`, non-finite tensors, CPU-only manifest failure, comparator drift, or production/test/chapter/highdim/vendored/DSGE/NAWM contamination.

Explanatory diagnostics: exact deltas for centered particles, scale, scaled particles, cost matrices, annealed epsilon start, Sinkhorn potentials, iteration count, transport matrix, and transported particles. These diagnose the difference but do not assert which implementation is mathematically correct.

Not concluded: correctness of either implementation, production readiness, posterior correctness, HMC readiness, smoothness-surface gradient correctness, general nonlinear-SSM validity, monograph claim, or dtype default policy.

Artifacts:
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r3_transport_internals_audit_tf.py`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r3_transport_internals_audit_2026-06-03.json`
- `experiments/dpf_implementation/reports/dpf-filterflow-r3-transport-internals-audit-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-r3-transport-internals-audit-result-2026-06-03.md`

## Selected Rows

Use selected R3 rows from the prior proposal-trace/replay result:
- row 7: first downstream full-computed replay failure;
- row 16: first exact-input computed-transport replay failure;
- row 43: largest full-computed transport/post-resample delta in the prior result;
- row 79: largest exact-input post-resample particle delta in the prior result.

## Scope

Allowed writes:
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r3_transport_internals_audit_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-r3-transport-internals-audit-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r3_transport_internals_audit_2026-06-03.json`
- `docs/plans/bayesfilter-dpf-filterflow-r3-transport-internals-audit-*.md`

Forbidden writes:
- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane
- vendored student code
- `.localsource/filterflow`
- DSGE/NAWM artifacts

## Skeptical Pre-Execution Audit

Wrong baseline risk: the audit compares BayesFilter only to executable filterflow, not to paper truth, student work, or residual quality.

Proxy metric risk: transport residuals and Kalman values are not criteria here; direct tensor deltas against executable filterflow are the only localization evidence.

Stale context risk: rerun the non-mutating filterflow trace and require it to reproduce official filterflow before using internals.

Artifact adequacy: selected-row internals directly answer where BayesFilter first diverges inside transport; full-filter replay has already localized the discrepancy to this component.

Stop condition: if exact internals require editing filterflow source, stop and record a blocker.

## Verification

- `python -m py_compile` for the touched runner.
- CPU-only internals audit runner.
- CPU-only validate-only rerun.
- JSON parse/schema check.
- NumPy/import-boundary check, allowing NumPy only inside filterflow subprocess script strings.
- Lane-scoped trailing whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters`.
- `git status --short --branch`.
