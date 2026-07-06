# P01 Diagnostic Adequacy And Missing-Instrumentation Gate Subplan

Date: 2026-06-23

## Phase Objective

Determine whether existing Nystrom diagnostics are sufficient to select a
less-intrusive repair.  If they are not sufficient, implement only the smallest
opt-in diagnostic instrumentation needed for P02 repair selection, without
changing default/raw behavior.

## Entry Conditions Inherited From Previous Phase

- P00 local checks passed.
- Claude read-only review converged with `VERDICT: AGREE`.
- P00 result exists.
- The closed positive-projection program remains closed.
- P01 may inspect and minimally edit only Nystrom diagnostic/harness/test files
  needed for opt-in diagnostics.

## Required Artifacts

- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-diagnostic-adequacy-result-2026-06-23.md`
- P02 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-repair-selection-subplan-2026-06-23.md`
- Optional implementation files if diagnostics are missing:
  - `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
  - `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
  - `tests/test_nystrom_transport_tf.py`
  - `tests/test_actual_sir_nystrom_compiled_redo.py`
- Optional focused test log:
  `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-focused-tests-2026-06-23.log`

## Required Checks, Tests, And Reviews

- Inspect current diagnostic fields in the Nystrom tensor result and compiled
  redo harness.
- If no code change is needed, run a local structural check proving required
  diagnostic fields exist in code and harness output rows.
- If code changes are needed, run focused CPU-hidden tests:
  `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py`
- Draft or refresh P02 subplan based on available diagnostics.
- Review P02 subplan for consistency, correctness, feasibility, artifact
  coverage, and boundary safety.
- Claude review is required if P01 changes code or materially changes P02
  repair-selection criteria.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are diagnostics sufficient to select one less-intrusive repair, or is minimal opt-in instrumentation needed? |
| Baseline/comparator | Current Nystrom diagnostics and compiled redo harness output fields. |
| Primary pass criterion | Required diagnostic fields are available or minimally implemented with focused tests passing and no default/raw behavior change. |
| Veto diagnostics | Default behavior change, CLI incompatibility, missing focused tests after code edit, diagnostic changes that alter raw computation, or missing P02 handoff. |
| Explanatory diagnostics | Which fields exist: factor diagonal error, factor ranges, core ranges, kernel negativity, denominator floor hits, scaling ranges, residuals, spectra. |
| Not concluded | No repair selection, no repair effectiveness, no default readiness. |
| Artifact preserving result | P01 result file and optional focused test log. |

## Forbidden Claims And Actions

- Do not select or implement a repair in P01 unless only diagnostic
  instrumentation is needed to make P02 possible.
- Do not change default `kernel_mode="raw"` behavior.
- Do not change paired thresholds or residual thresholds.
- Do not run long GPU benchmarks in P01 unless P00/P01 are patched to require
  a tiny diagnostic artifact and Claude agrees.
- Do not claim diagnostic adequacy proves repair feasibility.

## Exact Next-Phase Handoff Conditions

Advance to P02 only if:

- P01 result states whether diagnostics were already adequate or what minimal
  diagnostics were added;
- required local checks/tests pass;
- P02 subplan is refreshed and internally reviewed;
- any material code or criterion change has Claude `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker result if:

- diagnostics cannot be made adequate without changing algorithm behavior;
- focused tests fail and cannot be repaired within the scoped files;
- instrumentation would require a new dependency or backend;
- continuing would require broad refactor, default-policy change, or modifying
  unrelated dirty work.

## Skeptical Plan Audit

Wrong baseline risk: instrumentation could be mistaken for repair.  Mitigation:
P01 explicitly forbids repair effectiveness claims.

Proxy risk: diagnostic fields may explain failure but cannot promote a repair.
Mitigation: P02/P04 retain hard paired criteria.

Artifact risk: fields might exist in tensor code but not in benchmark JSON.
Mitigation: P01 checks both code and harness row serialization.

Audit status: `READY_AFTER_P00_PASS`.
