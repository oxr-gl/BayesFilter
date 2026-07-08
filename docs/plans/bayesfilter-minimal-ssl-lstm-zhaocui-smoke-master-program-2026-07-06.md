# BayesFilter Minimal SSL-LSTM Zhao-Cui Smoke Master Program

Date: 2026-07-06

Status: `COMPLETE_PASSED_WITH_CODEX_SUBSTITUTE_REVIEWS`

## Objective

Operationalize the minimal one-dimensional state-space LSTM smoke program:
`latent_dim=1`, `hidden_dim=1`, `observation_dim=1`, short horizon, simplest
nondegenerate parameters, testing `zhaocui_fixed` first and then
`fixed_sgqf`/`svd_ukf` as mechanics comparators only.

The target question is narrow:

Can the existing minimal SSL-LSTM fixture be promoted from focused unit-test
coverage into a visible, reproducible smoke harness with structured artifacts
that prove only finite deterministic mechanics and analytic-score agreement?

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the minimal scalar SSL-LSTM `zhaocui_fixed` lane run as a structured smoke artifact with finite value/score and finite-difference agreement? |
| Candidate/mechanism under test | Existing clean-room deterministic `zhaocui_fixed` fixed replay adapter over scalar SSL-LSTM. |
| Expected failure mode | Shape/layout mismatch, hidden nondeterminism, non-finite score, finite-difference disagreement, schema/artifact mismatch, or unsupported claim leakage. |
| Promotion criterion | Minimal smoke artifact records finite deterministic `zhaocui_fixed` value/score, finite-difference subset agreement, schema validation, and forbidden-target scan pass. |
| Promotion veto | Nonfinite value/score, target-path autodiff/NumPy, adaptive target-path randomness, finite-difference failure, invalid artifact, or source-faithful/HMC-convergence/default-readiness claim. |
| Continuation veto | Required fix would change default policy, broaden into LEDH/source-faithful TTSIRT work, modify model files/public API, install packages, or require a human-approved scope change. |
| Repair trigger | Local implementation/harness/doc failure fixable within the scalar smoke question. |
| What must not be concluded | No posterior correctness, HMC convergence, method superiority, source-faithful Zhao-Cui parity, GPU/XLA production readiness, or default readiness. |

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Whether the scalar SSL-LSTM `zhaocui_fixed` mechanics can be run and preserved as a reproducible smoke artifact. |
| Exact baseline/comparator | Existing `tests/test_ssl_lstm_zhaocui_fixed_adapter.py` minimal fixture and SSL-LSTM protocol; `fixed_sgqf`/`svd_ukf` only as mechanics comparators. |
| Primary pass criterion | Structured artifact and focused tests pass for scalar `zhaocui_fixed`; comparator rows, if run, are descriptive only. |
| Veto diagnostics | Nonfinite target, nondeterminism, target autodiff/NumPy, finite-difference mismatch, invalid schema, unsupported claims, or wrong fixture dimensions. |
| Explanatory diagnostics | Runtime, score norm, finite-difference residual, reference sample count, comparator values, and launch-smoke telemetry if used. |
| Not concluded | Posterior correctness, HMC convergence, ranking, method superiority, source-faithful parity, LEDH result, GPU/XLA production readiness, or default readiness. |
| Preserved artifacts | `docs/plans`, `docs/benchmarks`, `docs/reviews`, visible execution ledger, logs under `docs/benchmarks/logs` if nontrivial commands run. |

## Minimal Fixture Definition

| Quantity | Value | Provenance |
| --- | --- | --- |
| `horizon` | `2` | Existing minimal adapter test fixture; convenience scalar smoke. |
| `latent_dim` | `1` | User request: everything one-dimensional. |
| `hidden_dim` | `1` | User request: minimal LSTM. |
| `observation_dim` | `1` | User request: everything one-dimensional. |
| observation vector | `[[0.12], [-0.03]]` | Existing focused test fixture, nondegenerate debug values. |
| FD subset | `0,4,8,12,13,14,15,16,19,22` | Existing focused test coverage for gate, latent, observation, initial, process, and observation-noise parameters. |

Numeric defaults are smoke-test conveniences unless explicitly labeled
otherwise. Passing this program does not certify scientific adequacy.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, fixture freeze, and review setup | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase0-governance-fixture-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase0-governance-fixture-result-2026-07-06.md` |
| 1 | Minimal smoke harness and artifact writer | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-result-2026-07-06.md` |
| 2 | Local checks and comparator mechanics | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase2-local-checks-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase2-local-checks-result-2026-07-06.md` |
| 3 | Optional launch-smoke bridge, if still in scope | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase3-launch-smoke-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase3-launch-smoke-result-2026-07-06.md` |
| 4 | Closeout and reset memo | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase4-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase4-closeout-result-2026-07-06.md` |

## Review And Repair Loop

1. Codex is supervisor and executor.
2. Claude is read-only reviewer only.
3. Material subplans/results use compact review bundles in `docs/reviews`.
4. Claude review uses `claude_review_gate.sh` only after user approval for
   trusted Claude execution.
5. If Claude returns `REVISE`, patch the same artifact visibly and rerun
   focused checks.
6. If Claude does not respond, use the tiny-probe protocol. If the probe
   responds, redesign the prompt/bundle. If the probe fails, use a fresh Codex
   read-only substitute review and record the fallback.
7. Stop after five review rounds for the same blocker.

## Boundary Rules

- Do not claim source-faithful SSL-LSTM Zhao-Cui parity.
- Do not use autodiff as the actual target gradient path.
- Do not let LEDH into this program.
- Do not change default policy, public API, model files, package metadata, or
  scientific claims.
- Do not launch long, GPU, detached, or Claude review commands before explicit
  approval.
