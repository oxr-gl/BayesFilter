# Phase 6 Subplan: Windowed-Mass Acceptance Telemetry Repair

Date: 2026-07-06

Status: `READY_FOR_REVIEW`

## Phase Objective

Localize and repair the Phase 5 staged tuning blocker
`windowed_stage_acceptance_telemetry_invalid_or_default` before any dimensional
lift. This phase must determine whether the hard veto is caused by acceptance
telemetry extraction/default-fill policy, public tuner routing, target behavior,
or another implementation issue.

## Entry Conditions Inherited From Previous Phase

- Phase 3 longer HMC artifact exists and has no continuation vetoes, but its
  fixed-kernel promotion screen failed.
- Phase 4 native divergence telemetry artifact exists and records
  `native_divergence_not_exposed_by_kernel`; this is not zero divergences.
- Phase 5 staged tuning artifact exists, wrapper status is `passed`, and public
  tuner status is `hard_veto` with
  `windowed_stage_acceptance_telemetry_invalid_or_default`.
- Phase 5 produced no final kernel handoff candidate.

## Required Artifacts

- Focused telemetry localization harness or test additions, scoped to
  `run_hmc_windowed_mass_stage` / `_windowed_stage_segmented_capture_payload`
  and the minimal `zhaocui_fixed` target.
- JSON/Markdown diagnostic artifact if a runtime localization command is needed.
- Phase 6 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase6-windowed-acceptance-telemetry-repair-result-2026-07-06.md`
- Refreshed next subplan after repair outcome:
  either a rerun of Phase 5 tuning or a blocker handoff.

## Required Checks, Tests, Reviews

Before execution:

- Skeptical plan audit: confirm the command answers only why acceptance
  telemetry is default-like/missing in the windowed-mass stage.
- Inspect the Phase 5 public tuning artifact and progress artifact for the
  exact stage and hard-veto path.
- Inspect existing windowed-mass tests covering default-like acceptance trace.
- Compile any new harness/tests.
- Run focused CPU-hidden tests.
- Run `git diff --check`.
- Claim-boundary scan over Phase 6 files.
- Use visible Codex substitute review if Claude remains blocked by private
  context-transfer policy.

After execution:

- If a fix is made, rerun the focused `hmc_kernel_tuning` windowed-mass tests
  and the minimal Phase 5 test harness.
- If a runtime diagnostic is run, validate JSON with `python -m json.tool`.
- Write Phase 6 result with decision and inference-status tables.
- Refresh the next subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Why did Phase 5 windowed-mass capture classify acceptance telemetry as invalid/default-like, and can that be repaired without weakening the hard-veto policy? |
| Baseline/comparator | Phase 5 public tuning artifact with hard veto `windowed_stage_acceptance_telemetry_invalid_or_default`, plus existing windowed-mass unit tests for default-like traces. |
| Candidate/mechanism under test | Acceptance trace extraction and provenance in the windowed-mass stage on the minimal target. |
| Primary pass criterion | A focused diagnosis identifies the cause and either patches it with tests or records a precise blocker. |
| Veto diagnostics | Using default-filled acceptance as real telemetry, removing the hard veto without evidence, proxy-divergence substitution, nonfinite target/value/score, invalid artifact, or unsupported readiness/correctness claim. |
| Explanatory diagnostics | Trace keys, acceptance trace shape/dtype/counts, runtime metadata, capture policy, public tuner route, and whether the HMC runtime actually executed. |
| Not concluded | Zero divergences, posterior correctness, HMC convergence, tuned-kernel superiority, dimensional generality, default readiness, production readiness, source-faithful Zhao-Cui parity, or LEDH evidence. |

## Forbidden Claims And Actions

- Do not demote default-like acceptance telemetry to a warning without evidence.
- Do not treat acceptance/log-accept/target-log-prob as native divergence.
- Do not claim zero divergences while Phase 4 telemetry remains unavailable.
- Do not proceed to dimensional lift until this blocker is repaired or a
  reviewed alternative is approved.
- Do not change public HMC defaults, model files, package state, or
  source-faithful Zhao-Cui route in this phase.

## Exact Next-Phase Handoff Conditions

Proceed to a Phase 5 rerun subplan only if:

- acceptance telemetry provenance is repaired or validated as non-default real
  runtime telemetry;
- focused tests pass; and
- the next subplan preserves Phase 4 divergence unavailability and Phase 5
  nonclaims.

Write a blocker result and stop if the cause cannot be localized without
crossing an unreviewed runtime/product/scientific/model-file/source-faithful
boundary.

## Stop Conditions

Stop on invalid artifact, nonfinite target/value/score, inability to distinguish
real acceptance telemetry from default-filled telemetry, pressure to weaken the
hard-veto policy without evidence, unsupported correctness/readiness claims, or
review nonconvergence.
