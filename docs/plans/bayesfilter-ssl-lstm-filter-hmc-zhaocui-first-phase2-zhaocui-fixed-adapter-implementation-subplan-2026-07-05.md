# Phase 2 Subplan: `zhaocui_fixed` Adapter Implementation

Date: 2026-07-05

Status: `DRAFT_NEXT_PHASE_PENDING_REVIEW`

## Phase Objective

Implement the narrow `zhaocui_fixed` SSL-LSTM adapter designed in Phase 1:
a deterministic fixed-HMC clean-room approximation with an analytic first-order
score path and honest route classification.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed through Codex substitute review after Phase 0 Claude export was
  rejected as outside approved scope.
- Phase 1 design result exists and classifies the route as a clean-room fixed
  variant, not source-faithful SSL-LSTM Zhao-Cui parity.
- Phase 1 forbids target-path autodiff, LEDH, public API/default changes, and
  broad TTSIRT/KR source-route claims.
- The existing SGQF/UKF adapters are comparators and reusable local SSL-LSTM
  derivative substrate only.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-adapter-implementation-result-2026-07-05.md`
- New implementation module, expected path:
  `bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`
- Focused tests, expected path:
  `tests/test_ssl_lstm_zhaocui_fixed_adapter.py`
- Updated imports only if needed for tests or internal package consistency.
- Debug/reference value-score JSON artifact for a tiny deterministic fixture.
- Refreshed Phase 3 tests/artifact-schema subplan.

## Required Checks, Tests, And Reviews

- `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py tests/test_ssl_lstm_zhaocui_fixed_adapter.py`
- CPU-hidden focused tests:
  `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_zhaocui_fixed_adapter.py`
- Protocol regression tests if protocol metadata is touched:
  `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_protocol.py`
- Forbidden target-path scan:
  `rg -n 'GradientTape|tf\\.py_function|np\\.|numpy' bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`
  must produce no target-path hits.
- Schema validation for the debug/reference artifact.
- Local review of the Phase 3 subplan after it is refreshed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 2 implement a deterministic, finite, analytic-score `zhaocui_fixed` SSL-LSTM adapter under the Phase 1 design? |
| Baseline/comparator | Phase 1 design ledger, Phase 2 protocol, Phase 3 SGQF/UKF adapter style, Zhao-Cui source anchors for recentering/replay vocabulary. |
| Primary pass criterion | New adapter module and tests pass deterministic, finite score, finite-difference subset, metadata, schema, and forbidden-target-path checks. |
| Veto diagnostics | Autodiff target path, adaptive randomness, unclassified route metadata, non-finite value/score, finite-difference failure, invalid artifact schema, or source-faithful parity claim. |
| Explanatory diagnostics | Runtime, score norm, finite-difference residuals, manifest fields, and recentering diagnostics. |
| Not concluded | HMC readiness, posterior correctness, source-faithful Zhao-Cui parity, method superiority, SGQF/UKF sufficiency, LEDH result, or default readiness. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-adapter-implementation-result-2026-07-05.md` |

## Implementation Boundary

Phase 2 should keep the implementation minimal:

- no public API export unless a local package import requires it;
- no change to benchmark defaults yet;
- no HMC run;
- no GPU benchmark;
- no LEDH code;
- no TTSIRT/KR parity implementation;
- no package install or network fetch.

The adapter may use TensorFlow tensors and existing local SSL-LSTM derivative
helpers. NumPy is allowed only in tests/reference finite differences, not inside
the target adapter implementation path.

## Forbidden Claims And Actions

- Do not claim source-faithful SSL-LSTM Zhao-Cui parity.
- Do not claim HMC readiness or estimation success.
- Do not use `GradientTape`, `tf.py_function`, NumPy implementation logic, or
  finite differences as the actual score path.
- Do not mutate unrelated dirty worktree files.
- Do not change public APIs, default policies, package metadata, model files, or
  benchmark interpretation criteria.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only when:

- Phase 2 result exists and records all required checks;
- the `zhaocui_fixed` adapter exists and has a finite, deterministic analytic
  value/score path on the tiny fixture;
- schema-valid debug/reference artifact exists;
- finite-difference subset checks pass or a blocker result explains the failure;
- forbidden target-path scan passes;
- Phase 3 subplan is drafted/refreshed and reviewed.

## Stop Conditions

- The adapter cannot be implemented without target-path autodiff.
- The analytic score cannot be made finite or finite-difference consistent on
  the tiny fixture.
- A fix would require a broader method family, public API/default-policy change,
  package install, network fetch, model-file edit, or LEDH implementation.
- The route classification would need to be upgraded to source-faithful parity
  without anchors.
- Review finds a material issue that cannot be fixed within five repair rounds.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the Phase 2 result/close record.
3. Draft or refresh the Phase 3 tests/artifact-schema subplan.
4. Review Phase 3 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
