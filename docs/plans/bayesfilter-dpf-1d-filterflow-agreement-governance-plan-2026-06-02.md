# Plan: 1D Filterflow Agreement Governance Audit

## Scope

This plan redoes the scalar-state 1D LGSSM debug ladder under corrected
governance. The question is whether BayesFilter's experimental TF/TFP
annealed-transport implementation matches the local executable filterflow
reference on the same numeric 1D setting. It does not assert that either
implementation is mathematically correct.

Lane boundary: use only BayesFilter-owned experimental DPF code under
`experiments/dpf_implementation/tf_tfp/` and reports under
`experiments/dpf_implementation/reports/` plus this `docs/plans` result. Do not
edit production `bayesfilter/`, `tests/`, monograph chapters, high-dimensional
lane artifacts, student/vendored code, DSGE/NAWM artifacts, or
`.localsource/filterflow` source.

## Evidence Contract

Primary question: under matched 1D scalar LGSSM inputs and matched filterflow
transport settings, does BayesFilter match local executable filterflow?

Primary comparator: the current local patched filterflow executable checkout
under `.localsource/filterflow`, identified by HEAD commit plus local
diff/status fingerprint. The branch string is descriptive only.

Primary pass criterion:

- filterflow subprocess executes;
- parent and filterflow subprocess run CPU-only with no visible GPU devices;
- BayesFilter/filterflow trigger flags match;
- scalar, forward ledger, transport matrix, post-transport particles, and
  residual values agree within comparison tolerances;
- finite scalar values are recorded.

Veto diagnostics:

- filterflow subprocess blocker;
- non-finite scalar;
- trigger mismatch;
- BayesFilter/filterflow scalar or ledger mismatch;
- BayesFilter/filterflow residual mismatch.

Diagnostic-only quantities:

- absolute row/column residual magnitude when shared by both implementations;
- AD and finite-difference gradients;
- runtime;
- resampling frequency.

What must not be concluded:

- no production readiness;
- no public API readiness;
- no posterior correctness;
- no HMC readiness;
- no general nonlinear-SSM validity;
- no full smoothness LGSSM validation;
- no claim that filterflow or BayesFilter is mathematically correct.

## Execution

Use the filterflow-style settings recovered from the local executable smoothness
script:

- `convergence_threshold = 1e-6`;
- `max_iterations = 500`;
- `epsilon = 0.25`;
- `scaling = 0.9`;
- scalar-state 1D LGSSM fixture.

Run fixed/controlled horizons:

- prior fixed anchors: `T=2`, `T=4`;
- generated scalar horizons: `T=4`, `T=8`, `T=16`, `T=32`, `T=64`, `T=100`.

Stop only on implementation disagreement or filterflow blocker. Do not stop
because both implementations share a large absolute residual; record that as a
shared-quality diagnostic.

## Artifacts

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_agreement_governance_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-1d-agreement-governance-2026-06-02.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_agreement_governance_2026-06-02.json`
- `docs/plans/bayesfilter-dpf-1d-filterflow-agreement-governance-result-2026-06-02.md`

## Skeptical Pre-Execution Audit

- Wrong goal risk: residual magnitude must not become a veto unless
  BayesFilter and filterflow disagree.
- Wrong comparator risk: use local executable filterflow only, not pristine
  upstream and not student code.
- Hidden drift risk: record comparator fingerprint and do not mutate
  `.localsource/filterflow`.
- Backend risk: BayesFilter algorithmic path remains TF/TFP; no NumPy backend.
- Scope risk: this answers 1D agreement only, not full smoothness validation.

Audit status: passed for this narrow agreement audit.

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_agreement_governance_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_agreement_governance_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_agreement_governance_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_agreement_governance_2026-06-02.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_agreement_governance_tf.py
rg -n "^\\s*(from|import)\\s+.*(student|vendored|vendor|highdim|dsge|DSGE|nawm|NAWM)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_agreement_governance_tf.py
rg -n "[ \t]$" docs/plans/bayesfilter-dpf-1d-filterflow-agreement-governance-*.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_agreement_governance_tf.py experiments/dpf_implementation/reports/dpf-filterflow-1d-agreement-governance-2026-06-02.md
git diff --check
git status --short -- bayesfilter tests docs/chapters
git status --short --branch
```
