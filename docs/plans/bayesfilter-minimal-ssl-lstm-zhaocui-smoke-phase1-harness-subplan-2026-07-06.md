# Phase 1 Subplan: Minimal Smoke Harness And Artifact Writer

Date: 2026-07-06

Status: `DRAFT_PENDING_PHASE0_REVIEW`

## Phase Objective

Create a minimal scalar SSL-LSTM smoke harness that emits a structured artifact
for `zhaocui_fixed` first, with optional mechanics comparator rows for
`fixed_sgqf` and `svd_ukf`.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result exists and freezes scalar fixture dimensions.
- Review path is approved/completed or substitute-reviewed and recorded.
- No unapproved Claude/GPU/long/detached command is required for this phase.
- `zhaocui_fixed` remains a clean-room fixed adaptation, not source-faithful
  Zhao-Cui parity.

## Required Artifacts

- Harness script, expected path:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py`
- Focused test, expected path:
  `tests/test_minimal_ssl_lstm_zhaocui_smoke.py`
- JSON output artifact, expected path:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json`
- Markdown output artifact, expected path:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.md`
- Phase 1 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-result-2026-07-06.md`
- Draft/refreshed Phase 2 subplan.

## Required Checks, Tests, And Reviews

- `python -m compileall -q docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_minimal_ssl_lstm_zhaocui_smoke.py`
- Run the harness once with CPU hidden and write JSON/Markdown artifacts.
- Validate artifact fields:
  `latent_dim=1`, `hidden_dim=1`, `observation_dim=1`, `horizon=2`,
  `primary_filter=zhaocui_fixed`, finite value/score, FD residual, schema role
  declarations, and nonclaims.
- Forbidden target-path scan over `bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`.
- Bounded review of Phase 1 result/Phase 2 subplan only if approved.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar SSL-LSTM `zhaocui_fixed` mechanics be materialized as a structured smoke artifact? |
| Baseline/comparator | Existing `tests/test_ssl_lstm_zhaocui_fixed_adapter.py` fixture; `fixed_sgqf` and `svd_ukf` rows are mechanics comparators only. |
| Primary pass criterion | Harness emits schema-valid artifact with scalar dimensions, finite deterministic `zhaocui_fixed` value/score, and finite-difference subset residual. |
| Veto diagnostics | Nonfinite value/score, nondeterminism, FD mismatch, target autodiff/NumPy, invalid artifact, wrong dimensions, or unsupported claim. |
| Explanatory diagnostics | Runtime, score norm, comparator values, reference sample count, and recenter diagnostics. |
| Not concluded | Posterior correctness, HMC convergence, ranking, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |

## Forbidden Claims And Actions

- Do not claim HMC convergence, posterior correctness, method superiority,
  source-faithful parity, GPU/XLA production readiness, default readiness, or
  LEDH result.
- Do not change default policy, public API, model files, package metadata, or
  unrelated dirty worktree files.
- Do not use finite differences as the target score path.
- Do not use `GradientTape`, `tf.py_function`, or NumPy target implementation.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only when:

- harness/test files exist;
- compile/test/harness run pass;
- JSON/Markdown artifacts exist;
- Phase 1 result records checks, artifact paths, and evidence boundaries;
- Phase 2 local-checks subplan exists and has been reviewed or queued for
  approved review.

## Stop Conditions

Stop if the scalar harness cannot pass without broadening the fixture, changing
adapter semantics, adding target autodiff, using GPU/long execution without
approval, changing default policy/public API/model files, or making unsupported
scientific claims.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write Phase 1 result/close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
