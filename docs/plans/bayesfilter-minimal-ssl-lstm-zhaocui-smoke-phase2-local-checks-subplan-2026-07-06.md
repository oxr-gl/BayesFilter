# Phase 2 Subplan: Local Checks And Comparator Mechanics

Date: 2026-07-06

Status: `DRAFT_READY_FOR_EXECUTION`

## Phase Objective

Rerun focused local checks, validate the generated minimal smoke artifacts, and
confirm that comparator mechanics remain descriptive-only before deciding
whether an optional launch-smoke bridge is needed.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result exists and records a passing minimal scalar `zhaocui_fixed`
  smoke artifact.
- JSON and Markdown artifacts exist under `docs/benchmarks`.
- The run remains CPU-hidden debug evidence only.
- No posterior correctness, HMC convergence, ranking, source-faithful parity,
  GPU/XLA production readiness, default readiness, or LEDH claim has been made.

## Required Artifacts

- Existing JSON artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json`
- Existing Markdown artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.md`
- Phase 2 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase2-local-checks-result-2026-07-06.md`
- Draft/refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase3-launch-smoke-subplan-2026-07-06.md`

## Required Checks, Tests, And Reviews

- `python -m compileall -q docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_minimal_ssl_lstm_zhaocui_smoke.py`
- JSON validation for scalar dimensions, `primary_filter=zhaocui_fixed`,
  passing primary gate diagnostics, finite comparator rows, and CPU-hidden run
  manifest.
- Markdown/nonclaim scan to ensure unsupported claims are absent or negated.
- `git diff --check`.
- Review Phase 3 subplan for consistency, correctness, feasibility, artifact
  coverage, and boundary safety.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the Phase 1 harness and artifacts satisfy local boundary and schema checks without unsupported claims? |
| Baseline/comparator | Phase 1 generated artifact and existing scalar adapter tests. |
| Primary pass criterion | Focused compile/test/artifact validations pass and artifacts preserve primary/comparator role boundaries. |
| Veto diagnostics | Missing artifact, invalid schema, wrong dimensions, failed primary gate, nonfinite comparator row, unsupported claim, target-path autodiff/NumPy hit, or CPU-hidden run mislabeled as GPU/production evidence. |
| Explanatory diagnostics | Runtime, score norm, FD residual, comparator values, TensorFlow CUDA warning under CPU-hidden execution. |
| Not concluded | Posterior correctness, HMC convergence, ranking, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |

## Forbidden Claims And Actions

- Do not claim posterior correctness, HMC convergence, method superiority,
  source-faithful parity, GPU/XLA production readiness, default readiness, or
  LEDH result.
- Do not change public APIs, model files, package metadata, default policy, or
  unrelated dirty worktree files.
- Do not run GPU/CUDA, long, detached, package-install, network, or external
  reviewer commands in this phase.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only when:

- Phase 2 checks pass;
- Phase 2 result exists;
- Phase 3 launch-smoke subplan exists;
- Phase 3 explicitly states whether launch smoke is needed and what it would
  prove or not prove;
- any required approvals for Phase 3 runtime scope are requested before launch.

## Stop Conditions

Stop if artifacts are missing or invalid, if local checks fail in a way that
requires changing adapter semantics, if unsupported claims are found, if
CPU-hidden debug evidence has been mislabeled as GPU/production evidence, or if
continuing would require unapproved GPU/long/detached/external-review actions.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write Phase 2 result/close record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
