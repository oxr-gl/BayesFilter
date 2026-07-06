# P05 Focused Repair Implementation Subplan

Date: 2026-06-23

Status: `DRAFT_READY_IF_P04_SELECTS_POSITIVE_PROJECTION`

## Phase Objective

Implement the P04-selected opt-in positive-projected Nystrom kernel repair
diagnostic, with focused tests and without altering default policy or promotion
criteria.

## Entry Conditions Inherited From Previous Phase

- P04 selected the opt-in positive-projected Nystrom kernel repair diagnostic.
- Claude review of P04 converged with no material blocker, or P04 records a
  bounded non-material review exception.
- No P04 GPU confirmation row is pending.

## Required Artifacts

- Code changes only in:
  - `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
  - `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
  - `tests/test_nystrom_transport_tf.py`
  - `tests/test_actual_sir_nystrom_compiled_redo.py`
- Focused test output.
- Optional small CPU-hidden diagnostic artifacts if the repair requires a smoke
  row.
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-result-2026-06-23.md`
- Refreshed P06 subplan.

## Required Checks, Tests, Reviews

- Focused unit tests covering old default path and new opt-in repair path,
  including at least one raw-vs-projected fixture that proves the new mode
  exercises a distinct projected-kernel path.
- Existing compiled-redo tiny CPU test if benchmark CLI changes.
- Claude read-only review of implementation diff if algorithm semantics change.

Required local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py
```

Optional syntax check if the implementation touches command-line parsing:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Was the opt-in positive-projected Nystrom kernel repair diagnostic implemented correctly and narrowly enough to test? |
| Baseline/comparator | Pre-repair tests and P04 selected repair contract. |
| Primary pass criterion | Focused tests pass; `kernel_mode="raw"` preserves current behavior by default; `kernel_mode="positive_projected"` is selectable, records projection diagnostics, and has a fixture where projection floor hits are positive. |
| Veto diagnostics | Test failure, broad refactor, default-policy change, missing diagnostics, repair diverging from P04, or hidden threshold/policy change. |
| Explanatory diagnostics | Tiny fixture outputs, code review notes. |
| Not concluded | No repair effectiveness on serious model until P06. |
| Artifacts | Code diff, test output, P05 result. |

## Implementation Contract

The implementation should be as small as possible:

- Add an explicit Nystrom kernel mode argument with allowed values
  `raw` and `positive_projected`.
- Preserve `raw` as the default everywhere.
- In `positive_projected`, form the approximate Nystrom kernel implied by the
  current factors, project it elementwise to at least `denominator_floor`, and
  use that projected kernel for Sinkhorn matvecs, mass/residual diagnostics,
  and final transport application.
- The first implementation may internally materialize `[B,N,N]` in this mode
  only.  That must be recorded as diagnostic-only and must not alter the raw
  streaming/nonmaterialized route.
- Keep existing `denominator_floor` semantics; do not tune its default.
- Record the selected kernel mode in Python diagnostics, tensor row summaries,
  and benchmark `transport` metadata.
- Expose the mode in `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
  as `--nystrom-kernel-mode {raw,positive_projected}`.
- Record projected-kernel diagnostics: raw kernel minimum, projected kernel
  minimum, and projection floor-hit count.

Allowed tests:

- A unit test showing `raw` remains the default in diagnostics and CLI metadata.
- A unit/XLA test showing `positive_projected` is accepted, XLA-compilable,
  finite on a deterministic tiny fixture, and records its mode.
- A discriminating fixture where raw Nystrom kernel reconstruction has at least
  one entry below the projection floor and `positive_projected` records
  positive floor hits.  This fixture may be tiny and diagnostic-only.
- A parse/build-result test showing the benchmark propagates
  `--nystrom-kernel-mode positive_projected`.

Disallowed implementation work:

- No changes to rank/epsilon defaults.
- No changes to residual thresholds or paired thresholds.
- No semantic replacement with positive-feature or low-rank-coupling routes.
- No automatic fallback from raw to projected mode.
- No broad refactor of the actual-SIR benchmark.

## Forbidden Claims And Actions

- Do not claim serious-model rescue from unit tests.
- Do not change default route or default parameter policy.
- Do not edit unrelated files.
- Do not use tests to relax hard veto thresholds.
- Do not call the opt-in mode source-faithful dense Sinkhorn.

## Exact Next-Phase Handoff Conditions

Advance to P06 only if:

- Focused tests pass.
- P05 result names exact repair flag/configuration to test:
  `--nystrom-kernel-mode positive_projected`.
- P06 subplan includes the two failing rows and the control, with shape, seeds,
  dtype, TF32/JIT, rank/epsilon, transport policy, residual thresholds, paired
  thresholds, and GPU selection protocol held fixed while toggling only the
  selected kernel mode.
- Material implementation review, if required, converged.

## Stop Conditions

- Focused tests fail after one focused repair attempt.
- Repair requires broad redesign beyond P04 selection.
- Review non-convergence after five rounds.

## End-Of-Subplan Required Actions

1. Run required local checks.
2. Write P05 result/close record.
3. Draft or refresh P06 subplan.
4. Review P06 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
