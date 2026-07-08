# BayesFilter SSL-LSTM Zhao-Cui-First Master Program

Date: 2026-07-05

Status: `DRAFT_UNDER_REVIEW`

## Objective

Unblock the SSL-LSTM `zhaocui_fixed` lane first, using a deterministic fixed-variant adapter with an analytic score path and a fail-closed source-anchor policy. LEDH is explicitly deferred to a later, separate master program.

The target question is narrow:

Can a Zhao-Cui-first, fixed-branch SSL-LSTM adapter produce a finite, repeatable, HMC-compatible value/score path that survives the shared benchmark and launch-smoke gates without claiming source-faithful parity it does not have?

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can `zhaocui_fixed` be admitted as a deterministic fixed-variant SSL-LSTM adapter with analytic gradient support? |
| Mechanism under test | A clean-room fixed-variant route that reuses Zhao-Cui source anchors for frozen recentering / normalizer structure while keeping SSL-LSTM-specific code in the BayesFilter tree. |
| Estimand | Filter-induced posterior over SSL-LSTM parameters under the `zhaocui_fixed` likelihood path. |
| Baseline/comparator | Existing SSL-LSTM `fixed_sgqf` and `svd_ukf` adapters, plus the local Zhao-Cui author-source audit bundle. LEDH is not part of this program. |
| Expected failure modes | Source-anchor gaps, hidden adaptive randomness, inability to keep the target path analytic, invalid fixed-branch metadata, non-finite score, or a route that requires autodiff to function. |
| Promotion criterion | The lane passes deterministic/value-score tests, finite-difference checks, artifact-schema checks, and the shared benchmark/HMC gate without overclaiming source-faithfulness. |
| Promotion veto | Any source-faithfulness claim without anchors, non-finite target value/score, adaptive branch selection in the target path, or fallback to autodiff as the actual score path. |
| Continuation veto | A required fix would broaden into a new method family, change default policy, or require a human-approved scope change. |
| Repair trigger | Local implementation or artifact failure that can be fixed without changing the research question. |
| What must not be concluded | No exact posterior correctness claim, no method superiority claim, no source-faithful Zhao-Cui parity claim, no LEDH conclusion. |

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific question | Whether a Zhao-Cui-first fixed-variant SSL-LSTM lane can be made deterministic, finite, and HMC-compatible. |
| Exact comparator | The Phase 3 SGQF/UKF adapters and the local Zhao-Cui source-anchor audit bundle. |
| Primary pass criterion | `zhaocui_fixed` exists, returns finite value/score, passes finite-difference checks, records honest classification, and can enter the shared benchmark/HMC harness. |
| Veto diagnostics | Missing source anchors, adaptive target-path randomness, autodiff fallback, invalid artifact schema, non-finite score, or unclassified route claims. |
| Explanatory diagnostics | Runtime, finite-difference residuals, branch stability, and HMC launch telemetry. |
| Not concluded | Source-faithful parity, posterior correctness, method superiority, LEDH sufficiency, or default readiness. |
| Preserved artifacts | `docs/plans`, `docs/reviews`, benchmark JSON/Markdown outputs, and phase result/close records. |

## Skeptical Plan Audit

Before any execution phase:

- verify the comparison is against the shared SSL-LSTM benchmark, not a one-off fixture;
- verify the target path is still analytic and deterministic;
- verify source-anchor claims are bounded to what the local audit can support;
- verify no LEDH work is smuggled into this program;
- verify the artifact being produced actually answers the phase question.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Source-anchor governance and route classification | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-source-anchor-governance-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-source-anchor-governance-result-2026-07-05.md` |
| 1 | Fixed-variant design and classification ledger | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase1-fixed-variant-design-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase1-fixed-variant-design-result-2026-07-05.md` |
| 2 | `zhaocui_fixed` adapter implementation | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-adapter-implementation-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-adapter-implementation-result-2026-07-05.md` |
| 3 | Focused tests and artifact schema | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase3-tests-and-artifact-schema-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase3-tests-and-artifact-schema-result-2026-07-05.md` |
| 4 | Shared benchmark and launch-smoke integration | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase4-benchmark-and-launch-smoke-integration-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase4-benchmark-and-launch-smoke-integration-result-2026-07-05.md` |
| 5 | Closeout and LEDH deferral handoff | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase5-closeout-and-ledh-deferral-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase5-closeout-and-ledh-deferral-result-2026-07-05.md` |

## Review And Repair Loop

1. Codex is supervisor and executor.
2. Claude is a read-only reviewer only.
3. Material plan/subplan/result artifacts use bounded review bundles.
4. If Claude returns `REVISE`, patch the same artifact visibly and rerun focused checks.
5. If Claude does not respond, send a tiny probe. If the probe responds, revise the prompt or bundle. If the probe fails, use a separate Codex read-only substitute review on the same bounded bundle.
6. Stop after five review rounds for the same blocker.
7. If the blocker does not converge, write a blocker result and stop for human direction.

## Boundary Rules

- Do not claim source-faithful SSL-LSTM Zhao-Cui parity.
- Do not use autodiff as the actual target gradient path.
- Do not let LEDH into this master program.
- Do not change default policy, public API, model files, or scientific claims outside the phase contract.
