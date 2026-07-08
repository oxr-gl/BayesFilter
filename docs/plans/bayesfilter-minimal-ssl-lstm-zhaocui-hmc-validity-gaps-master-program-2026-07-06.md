# Minimal SSL-LSTM Zhao-Cui HMC Validity Gaps Master Program

Date: 2026-07-06

Status: `CLOSED_FIXED_MASS_STEP_BLOCKER_RECORDED`

## Program Objective

Address the remaining gaps after the completed minimal scalar
`zhaocui_fixed` HMC mechanics program. The previous program established an
internal target, CPU regression, GPU/XLA launch smoke, and a short GPU/XLA
hard-veto diagnostic ladder. It did not establish posterior correctness, HMC
convergence, native divergence availability, tuning/adaptation validity,
dimensional generality, source-faithful Zhao-Cui parity, ranking, default
readiness, production readiness, public API readiness, or LEDH evidence.

This program changes the question from "does it launch without hard vetoes?"
to "what evidence is needed before the sampler/target can be trusted for the
next scientific or engineering lift?"

Codex remains supervisor and executor. Claude may be used only as a read-only
reviewer through compact review bundles.

## Baseline

Immediate predecessor:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase6-closeout-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-reset-memo-2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json`

Baseline evidence class:

- Internal adapter mechanics evidence.
- CPU-hidden regression evidence.
- Trusted GPU/XLA launch and short hard-veto diagnostic evidence.
- No convergence, posterior correctness, source-faithful parity, ranking,
  default-readiness, production-readiness, public API, or LEDH evidence.

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | Governance and review setup | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-governance-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-governance-result-2026-07-06.md` |
| 1 | Scalar posterior/reference oracle design | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase1-scalar-oracle-design-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase1-scalar-oracle-design-result-2026-07-06.md` |
| 2 | Minimal oracle implementation and checks | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-result-2026-07-06.md` |
| 3 | Longer HMC convergence diagnostics | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-result-2026-07-06.md` |
| 4 | Native divergence telemetry investigation | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-result-2026-07-06.md` |
| 5 | HMC tuning and mass-matrix ladder design | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase5-tuning-mass-ladder-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase5-tuning-mass-ladder-result-2026-07-06.md` |
| 6 | Windowed-mass acceptance telemetry repair | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase6-dimensional-lift-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase6-windowed-acceptance-telemetry-repair-result-2026-07-06.md` |
| 7 | Frozen-step trajectory timeout handoff | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-frozen-step-trajectory-timeout-handoff-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-frozen-step-trajectory-timeout-handoff-result-2026-07-06.md` |
| 7 deferred | Source-faithful Zhao-Cui anchor track | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-source-faithful-track-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-source-faithful-track-result-2026-07-06.md` |
| 8 | Terminal Phase 6 repair slot | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-terminal-phase6-repair-slot-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-terminal-phase6-repair-slot-result-2026-07-06.md` |
| 8 deferred | Comparator and readiness boundary plan | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-comparator-readiness-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-comparator-readiness-result-2026-07-06.md` |
| 9 | Closeout and reset memo | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase9-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase9-closeout-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar `zhaocui_fixed` HMC path be moved from launch/hard-veto evidence toward posterior/sampler validity evidence without overstating claims? |
| Baseline/comparator | Completed `hmc-next` closeout and Phase 5 GPU/XLA hard-veto artifact. |
| Primary pass criterion | Each phase either produces its predeclared validity artifact and bounded result record, or stops with a blocker that preserves evidence boundaries. |
| Veto diagnostics | Wrong baseline, proxy metrics promoted to validity, missing stop condition, unreviewed long/GPU runtime, unsupported source-faithful claim, unsupported convergence/posterior/ranking/readiness claim, invalid artifact, or review nonconvergence. |
| Explanatory diagnostics | Runtime, acceptance, sample summaries, grid/reference summaries, finite checks, R-hat/ESS only when computed under a reviewed phase, and dirty-worktree summaries. |
| Not concluded | HMC convergence, posterior correctness, ranking/superiority, source-faithful parity, default readiness, production readiness, public API/package readiness, or LEDH evidence unless a later phase explicitly earns that claim. |
| Artifacts | Master program, phase subplans/results, review bundles, visible ledger, runtime JSON/Markdown artifacts, quiet logs, reset memo, and stop handoff. |

## Skeptical Plan Audit

Initial audit result: `PASS_WITH_BOUNDARIES`.

- Wrong baseline risk is controlled by using the completed `hmc-next` closeout
  and Phase 5 artifact as the immediate baseline.
- Proxy metric risk is controlled by keeping Phase 5 acceptance/runtime/sample
  summaries explanatory until a reviewed validity criterion is introduced.
- Missing stop condition risk is controlled by phase-local stop conditions and
  human-required boundaries.
- Unfair comparison risk is controlled by delaying comparator ranking until
  posterior/reference and convergence gates exist.
- Hidden assumption risk is controlled by a default/assumption ledger in the
  visible runbook.
- Environment mismatch risk is controlled by distinguishing CPU reference,
  GPU/XLA runtime, and trusted approval contexts.
- Artifact mismatch risk is controlled by requiring JSON/Markdown/result
  artifacts and compact review bundles.

## Human-Required Boundaries

Do not cross these boundaries without a reviewed phase subplan and explicit
approval where applicable:

- trusted GPU/XLA/HMC runtime beyond smoke or previously approved commands;
- long HMC or convergence runs;
- source-faithful Zhao-Cui parity claims;
- public API/default-policy/product readiness;
- package installation, network fetch, credentials, or model-file edits;
- destructive git/filesystem operations;
- LEDH result claims.

## Review And Repair Loop

Use `claude_review_gate.sh` for material review when allowed. Review bundles
must be compact and stored under `docs/reviews`. If Claude/probe is unavailable
or external review is blocked, record the reason and use a fresh visible
read-only Codex substitute review. Stop after five review rounds for the same
blocker.

## Forbidden Claims

Unless a later reviewed phase explicitly earns them, this program must not
claim:

- HMC convergence;
- posterior correctness;
- R-hat/ESS evidence;
- statistical ranking or superiority;
- source-faithful Zhao-Cui parity;
- public API/package readiness;
- default readiness;
- GPU/XLA production readiness;
- LEDH evidence.
