# Phase 8 Subplan: Terminal Phase 6 Repair Slot

Date: 2026-07-06

Status: `READY_FOR_REVIEW`

## Phase Objective

Execute the smallest reviewed follow-up to Phase 7 by enabling the existing
capped terminal Phase 6 repair slot:
`terminal_phase6_repair_extra_attempts=1`.

This phase tests whether the frozen-step trajectory repair handoff can be
consumed by one additional terminal attempt. It must not widen the scientific
claim boundary or treat a handoff candidate as posterior correctness,
convergence, ranking, readiness, zero-divergence evidence, source-faithful
Zhao-Cui parity, dimensional generality, or LEDH evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 6 repaired the windowed-mass acceptance telemetry blocker.
- Phase 7 enlarged the public timeout to `300.0` seconds and eliminated the
  `phase6_public_timeout_soft_deadline` hard veto.
- Phase 7 wrapper artifact status was `passed`.
- Phase 7 public tuner status was `budget_exhausted` with diagnostic role
  `phase7_repair_handoff_budget_exhausted_no_attempt_slot`.
- Phase 7 frozen-step trajectory stage returned `repair_or_retry`, hard vetoes
  `[]`, and repair triggers:
  `trajectory_length_outside_window`, `trajectory_length_above_window`, and
  `acceptance_outside_pass_band`.
- Phase 7 terminal budget guard recorded configured `max_attempts=1` and
  remaining attempt slots `0`.
- The implementation already supports one terminal Phase 6 repair slot through
  `terminal_phase6_repair_extra_attempts=1`, with existing focused tests.
- Phase 4 native divergence telemetry remains unavailable; this is not zero
  divergences.

## Required Artifacts

- Route review:
  `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-terminal-repair-slot-codex-substitute-review-2026-07-06.md`
- Runtime JSON artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_cpu_hidden_2026-07-06.json`
- Runtime Markdown artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_cpu_hidden_2026-07-06.md`
- Public tuning output directory:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_public_artifacts_2026-07-06`
- Phase 8 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-terminal-phase6-repair-slot-result-2026-07-06.md`
- Refreshed next subplan:
  either source-anchor/deferred-track planning, dimensional-lift blocker
  planning, or closeout depending on the result.

## Required Checks, Tests, Reviews

Before execution:

- Skeptical plan audit: confirm the command answers only whether one terminal
  Phase 6 repair slot consumes the Phase 7 repair handoff.
- Confirm Phase 7 JSON validates and has public tuner status
  `budget_exhausted` with diagnostic role
  `phase7_repair_handoff_budget_exhausted_no_attempt_slot`.
- Confirm Phase 7 public artifact has no hard vetoes and no
  `phase6_public_timeout_soft_deadline`.
- Compile the harness and focused tests.
- Run focused tests covering Phase 5/Phase 7 harness plumbing and terminal
  Phase 6 repair slot behavior.
- Run `git diff --check`.
- Run a claim-boundary scan over Phase 8 files.
- Use visible Codex substitute review if Claude remains blocked by private
  context-transfer policy.

Execution route:

- Rerun the same public tuner with Phase 8 artifact paths,
  `public_timeout_budget_s=300.0`, and
  `terminal_phase6_repair_extra_attempts=1`.
- Do not change target, seed, acceptance band, repair band,
  `max_leapfrog_steps`, CPU-hidden/non-XLA route, model files, public defaults,
  package state, or source-faithful route.

After execution:

- Validate JSON with `python -m json.tool`.
- Count private diagnostic events when present and report only the count.
- Write Phase 8 result with decision and inference-status tables.
- Refresh the next subplan and record whether source-anchor/comparator tracks
  remain deferred or can resume.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the existing one-slot terminal Phase 6 repair mechanism consume the Phase 7 frozen-step trajectory repair handoff and produce either a non-promoting final-kernel handoff or a new precise blocker? |
| Baseline/comparator | Phase 7 enlarged-timeout artifact with `phase7_repair_handoff_budget_exhausted_no_attempt_slot`. |
| Candidate/mechanism under test | `terminal_phase6_repair_extra_attempts=1` under the same CPU-hidden smoke diagnostic route. |
| Primary pass criterion | A valid structured artifact either records a non-promoting final-kernel handoff candidate or records a precise blocker after the terminal repair slot is consumed. |
| Promotion criterion | None in this phase. A final kernel, if produced, is a handoff artifact only and requires later validation. |
| Veto diagnostics | Invalid artifact, runtime exception, nonfinite target/value/score, hard veto, proxy divergence substitution, private mechanics exposure, unsupported zero-divergence claim, post-hoc threshold edits, or unsupported correctness/readiness/ranking claim. |
| Continuation veto | Broken target/reference precondition, missing Phase 7 artifacts, private artifact exposure, inability to identify terminal-slot outcome, or review nonconvergence. |
| Explanatory diagnostics | Stage statuses, repair triggers, terminal-slot payload, runtime, private event count, public-safe resume summary, and final-kernel hash presence/absence. |
| Not concluded | Zero divergences, posterior correctness, broad HMC convergence, tuned-kernel superiority, ranking, default readiness, production readiness, public API/package readiness, source-faithful Zhao-Cui parity, dimensional generality, or LEDH evidence. |

## Forbidden Claims And Actions

- Do not treat a final kernel handoff, if produced, as posterior correctness,
  convergence, default readiness, production readiness, or sampler superiority.
- Do not claim zero divergences while native divergence telemetry remains
  unavailable.
- Do not treat acceptance/log-accept/target-log-prob as native divergence.
- Do not expose private HMC mechanics, private paths, raw draws, positions,
  log-prob values, or private candidate grids in public artifacts.
- Do not change public HMC defaults, model files, package state, or the
  source-faithful Zhao-Cui route in this phase.

## Exact Next-Phase Handoff Conditions

Proceed to source-anchor or deferred-track planning only if Phase 8 records:

- a valid non-promoting handoff candidate; or
- a precise blocker that explains why continuing non-HMC documentation tracks
  is still useful.

Proceed to comparator/readiness planning only after a separate reviewed plan
establishes the validity evidence needed for comparison. A terminal repair-slot
run alone cannot justify comparator ranking or readiness claims.

## Stop Conditions

Stop on invalid artifact, runtime exception, nonfinite target/value/score,
hard veto, missing Phase 7 artifacts, private mechanics exposure, inability to
identify terminal-slot outcome, proxy-divergence substitution, unsupported
readiness/correctness/ranking/source-faithful claims, review nonconvergence, or
any need to cross an unreviewed runtime/product/scientific/model-file boundary.
