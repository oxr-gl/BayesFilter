# Phase 1 Subplan: Internal Reusable Adapter Surface

Date: 2026-07-06

Status: `COMPLETE`

## Phase Objective

Extract the benchmark-only `MinimalZhaoCuiHMCTargetAdapter` and minimal fixture
helpers into a reusable internal BayesFilter module while preserving the
completed ladder behavior and evidence boundaries.

## Entry Conditions Inherited From Previous Phase

- Phase 0 has passed through review before execution.
- The predecessor ladder artifacts remain the baseline.
- No public API, default-policy, GPU/XLA, or long-run boundary is open in this
  phase.
- Dirty worktree changes from other work must be preserved.

## Required Artifacts

- New internal module:
  `bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py`
- Updated benchmark harness:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`
- New focused tests:
  `tests/test_ssl_lstm_zhaocui_hmc_minimal.py`
- Existing ladder tests updated only for import-path migration or an explicitly
  documented artifact-schema repair:
  `tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- Phase 1 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase1-internal-adapter-result-2026-07-06.md`
- Refreshed Phase 2 subplan.

## Required Checks, Tests, Reviews

- `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 pytest -q tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- Immutable predecessor comparator check:
  compare new internal adapter outputs against the pre-extraction harness values
  for schema version, fixture dimensions, `log_prob`, score vector, scalar
  score shape `(24,)`, batch score shape `(2, 24)`, capability metadata,
  nonclaims, and adapter signature. The comparator is the current committed
  predecessor artifact
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_adapter_cpu_hidden_2026-07-06.json`
  plus the current pre-extraction harness behavior before Phase 1 edits.
- Forbidden implementation scan:
  `rg -n "GradientTape|tf\\.py_function|import numpy|np\\." bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`
- `git diff --check`
- Material review of implementation diff and Phase 2 handoff through Claude
  gate if available, otherwise fresh Codex-agent substitute review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar `zhaocui_fixed` HMC target adapter be moved from benchmark-only code into an internal module without behavior drift or evidence inflation? |
| Baseline/comparator | Existing benchmark adapter behavior and existing ladder tests/artifacts. |
| Primary pass criterion | Focused tests and existing ladder tests pass CPU-hidden, immutable predecessor comparator passes or records a justified non-behavioral schema repair, forbidden-token scan has no target-path hits, benchmark harness consumes the internal module, and artifacts/nonclaims remain unchanged or stricter. |
| Veto diagnostics | Nonfinite value/score, shape drift, unexplained value/score/signature drift, target-path NumPy/autodiff bridge, new Zhao-Cui route choice without classification/anchors/approval, public API export, default-policy change, failed tests, invalid artifact role, or unsupported claim. |
| Explanatory diagnostics | Code diff, score norm/log probability equality, runtime, adapter metadata, and dirty-worktree summary. |
| Not concluded | GPU/XLA behavior, HMC convergence, posterior correctness, ranking, source-faithful parity, public API/package readiness, default readiness, or LEDH result. |
| Artifact preserving result | Phase 1 result file, test output/log paths if needed, and updated benchmark JSON/Markdown only if a CPU regression rerun is explicitly part of Phase 2. |

## Implementation Design

Create `bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py` with:

- `MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS`;
- `minimal_ssl_lstm_config()`;
- `minimal_ssl_lstm_theta()`;
- `minimal_ssl_lstm_observations()`;
- `minimal_ssl_lstm_zhaocui_manifest()`;
- `MinimalZhaoCuiHMCTargetAdapter`;
- `initial_minimal_ssl_lstm_hmc_state()`;
- `minimal_ssl_lstm_fixture_payload()`.

The module may import TensorFlow and existing BayesFilter SSL-LSTM/Zhao-Cui
modules. It must not use NumPy for the algorithmic target path. It should remain
internal and should not be added to top-level package exports in this phase.

The benchmark harness should become a consumer of these helpers and should keep
the same JSON/Markdown artifact schema for predecessor tests.

This phase is mechanical extraction only. It must not introduce a new Zhao-Cui
route choice, change fixed replay/recentering behavior, change the likelihood,
change seeds, change prior geometry, or alter HMC settings. If an implementation
need appears to require any non-mechanical Zhao-Cui route behavior, stop before
coding and classify the proposed choice as `source_faithful`,
`fixed_hmc_adaptation`, or `extension_or_invention` with the required paper and
author-source anchors, or get explicit human approval for an extension target.

The `GradientTape` scan is intentionally conservative for this phase. The
predecessor adapter uses the existing manual first-order score path, and Phase 1
is only allowed to move that path into an internal module. Any newly introduced
`GradientTape` use would be a route/authority change from mechanical extraction
to native autodiff and therefore requires a separate reviewed plan. This does
not mean TensorFlow autodiff is forbidden repository-wide.

## Forbidden Claims And Actions

- Do not expose the new module as public API.
- Do not run GPU/CUDA/XLA or long sampler diagnostics.
- Do not change HMC pass/fail thresholds after seeing results.
- Do not alter Zhao-Cui fixed replay/recentering, likelihood, seeds, prior
  geometry, HMC settings, or route classification in this phase.
- Do not claim source-faithful Zhao-Cui parity.
- Do not claim convergence, posterior correctness, ranking, default readiness,
  GPU/XLA production readiness, public API readiness, or LEDH evidence.
- Do not edit unrelated dirty files.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if:

- internal module exists and benchmark harness imports it;
- required compile/pytest/forbidden-token checks pass;
- immutable predecessor comparator passes or records a reviewed
  non-behavioral schema-only repair;
- Phase 1 result records behavior preservation and nonclaims;
- material review returns `VERDICT: AGREE` or documented Codex substitute
  `VERDICT: AGREE`;
- Phase 2 CPU regression subplan is refreshed with exact commands/artifacts.

## Stop Conditions

Stop and write a blocker result if:

- extraction causes unexplained behavior/schema drift;
- forbidden target-path tokens appear;
- any non-mechanical Zhao-Cui route change is needed;
- tests fail and repair is not clearly Phase 1-scoped;
- review does not converge after five rounds;
- continuing requires public API/default-policy/GPU/long-run boundary.

## End-Of-Phase Requirements

At the end of Phase 1:

1. run required local checks;
2. write the Phase 1 result/close record;
3. draft or refresh the Phase 2 subplan;
4. review Phase 2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
