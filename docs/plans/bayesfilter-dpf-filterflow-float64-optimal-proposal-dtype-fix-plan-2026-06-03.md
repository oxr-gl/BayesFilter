# Plan: FilterFlow Float64 Optimal-Proposal Dtype Fix

## Question

Can the local float64 FilterFlow reference branch run the R3 optimal-proposal
trace/replay without the BayesFilter runner applying a subprocess-only monkey
patch?

## Evidence Contract

- Comparator: `.localsource/filterflow` branch
  `bayesfilter-py311-float64-reference`.
- Baseline issue: `OptimalProposalModel.__init__` uses raw `tf.eye(...)`
  tensors that default to float32 and fail when paired with float64 Cholesky
  factors.
- Primary criterion: after a source-level dtype-aware identity patch, the R3
  BayesFilter-vs-FilterFlow float64 trace/replay passes without runtime shims.
- Veto diagnostics: wrong branch, dirty unrelated FilterFlow source, failed
  FilterFlow compile/smoke, failed R3 validate-only, path-boundary drift, or
  production/tests/chapter edits.
- Explanatory only: exact tiny float64 roundoff deltas.
- Not concluded: mathematical correctness, posterior correctness, gradient
  correctness, production readiness, paper authority, or broader nonlinear SSM
  validity.

## Allowed Write Set

- `.localsource/filterflow/filterflow/proposal/optimal_proposal.py`
- `experiments/dpf_implementation/tf_tfp/runners/filterflow_reference_policy.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r3_float64_trace_replay_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-float64-optimal-proposal-dtype-fix-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-optimal-proposal-dtype-fix-result-2026-06-03.md`
- Refreshed R3 result/report/JSON artifacts from the targeted runner.

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored/student code
- unrelated FilterFlow files

## Skeptical Pre-Execution Audit

- Wrong comparator risk: verify the branch and commit before patching.
- Over-patch risk: change only identity dtype, not proposal math or transport.
- Hidden shim risk: remove the R3 subprocess monkeypatch after the source fix.
- Evidence relevance: rerun the exact R3 trace/replay so the artifact answers
  whether the reference branch itself now works.
- Governance risk: this is a local reference-code patch, not BayesFilter
  production implementation and not paper authority.

Audit result: pass.

## Verification

- FilterFlow branch/status check.
- `python -m py_compile` on the touched FilterFlow source and touched
  BayesFilter experimental runner.
- Targeted CPU-only R3 trace/replay.
- Targeted R3 validate-only.
- JSON parse/schema check.
- NumPy import gate for touched BayesFilter runner.
- Import-boundary search for protected lanes.
- Lane-scoped trailing whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters`.
- `git -C .localsource/filterflow status --short --branch`.
- `git status --short --branch`.
