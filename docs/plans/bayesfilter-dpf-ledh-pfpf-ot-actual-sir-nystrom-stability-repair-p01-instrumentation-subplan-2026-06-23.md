# P01 Instrumentation Implementation Subplan

Date: 2026-06-23

Status: `DRAFT_READY_AFTER_P00_REVIEW`

## Phase Objective

Add diagnostics that localize the first Nystrom nonfinite source without
changing default Cholesky behavior or benchmark pass/fail criteria.

## Entry Conditions Inherited From Previous Phase

- P00 local checks passed.
- Claude read-only review converged with `VERDICT: AGREE`.
- Master program and visible runbook are current.

## Required Artifacts

Allowed write set for P01:

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
- `tests/test_nystrom_transport_tf.py`
- `tests/test_actual_sir_nystrom_compiled_redo.py`
- at most one narrowly scoped diagnostic helper under `docs/benchmarks/`, only
  if the P01 result explains why the existing harness cannot preserve the
  required diagnostics.

No other files may be edited in P01 except the P01 result and refreshed P02
subplan.
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p01-instrumentation-result-2026-06-23.md`
- Next subplan refresh:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-subplan-2026-06-23.md`

## Required Checks, Tests, Reviews

- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py`
- Focused import/argument parse check if new CLI flags are added.
- Claude read-only review if implementation changes more than reporting
  fields or if pass/fail criteria are touched.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the harness record where the Nystrom failure starts without changing algorithm behavior? |
| Baseline/comparator | Existing P09D code path and focused tests. |
| Primary pass criterion | Focused tests pass and default `cholesky` behavior remains unchanged except for added diagnostics. |
| Veto diagnostics | Default behavior change, new nonfinite in tiny tests, CLI incompatibility, missing diagnostic fields, or altered promotion thresholds. |
| Explanatory diagnostics | Diagnostic schema details and optional tiny fixture values. |
| Not concluded | No repair, no robustness, no default readiness. |
| Artifacts | Code diff, focused test output, P01 result. |

## Forbidden Claims And Actions

- Do not run serious GPU rows before P02.
- Do not change residual or paired thresholds.
- Do not rank solver variants.
- Do not add broad algorithm abstractions unrelated to diagnostics.

## Exact Next-Phase Handoff Conditions

Advance to P02 only if:

- Focused tests pass.
- P01 result states diagnostic fields and unchanged default behavior.
- P02 subplan names exact failing/control rows and artifact paths.
- Review is complete if material implementation changed.

## Stop Conditions

- Focused tests fail after one focused repair attempt.
- Diagnostics require large algorithm changes rather than reporting.
- Reviewer identifies unsupported claim or unsafe boundary not fixed within five
  rounds.

## End-Of-Subplan Required Actions

1. Run required local checks.
2. Write P01 result/close record.
3. Draft or refresh P02 subplan.
4. Review P02 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
