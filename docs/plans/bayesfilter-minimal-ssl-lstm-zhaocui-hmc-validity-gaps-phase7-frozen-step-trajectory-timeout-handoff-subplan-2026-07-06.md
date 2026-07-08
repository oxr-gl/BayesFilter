# Phase 7 Subplan: Frozen-Step Trajectory Timeout Handoff

Date: 2026-07-06

Status: `READY_FOR_REVIEW`

## Phase Objective

Repair or localize the Phase 6 frozen-step trajectory hard veto
`phase6_public_timeout_soft_deadline` without weakening the timeout policy,
without exposing private HMC mechanics, and without claiming posterior
correctness, convergence, ranking, readiness, zero divergences, or
source-faithful Zhao-Cui parity.

This phase replaces the earlier placeholder Phase 7 source-anchor track as the
immediate next runbook step. The source-anchor and comparator/readiness tracks
remain deferred until the HMC handoff timeout is resolved or recorded as a
blocker.

## Entry Conditions Inherited From Previous Phase

- Phase 2 scalar oracle artifact exists and passed its selected reference
  checks.
- Phase 3 longer HMC artifact exists and has no continuation vetoes, but its
  sampler-setting promotion screen failed.
- Phase 4 native divergence telemetry artifact exists and records
  `native_divergence_not_exposed_by_kernel`; this is not zero divergences.
- Phase 5 public tuning artifact originally hard-vetoed on
  `windowed_stage_acceptance_telemetry_invalid_or_default`.
- Phase 6 repaired the windowed-mass acceptance telemetry policy and final
  rerun passed the windowed-mass and fixed-mass step stages.
- Phase 6 final public tuner artifact hard-vetoed in the frozen-step trajectory
  stage with `phase6_public_timeout_soft_deadline`.
- Phase 6 produced no `final_kernel_hash` or public final-kernel handoff.
- The final Phase 6 progress artifact records a private resume-split public
  summary with `private_resume_payload_available: true` and no public exposure
  of private paths, HMC draws, log-prob values, or private tuning mechanics.

## Required Artifacts

- Phase 7 review bundle, if material runtime policy changes are proposed:
  `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-timeout-handoff-review-bundle-2026-07-06.md`
- Runtime JSON artifact, if a rerun is executed:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase7_timeout_handoff_cpu_hidden_2026-07-06.json`
- Runtime Markdown artifact, if a rerun is executed:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase7_timeout_handoff_cpu_hidden_2026-07-06.md`
- Public tuning output directory, if a rerun is executed:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase7_timeout_handoff_public_artifacts_2026-07-06`
- Quiet log, if a rerun is executed:
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase7_timeout_handoff_cpu_hidden_2026-07-06.log`
- Phase 7 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-frozen-step-trajectory-timeout-handoff-result-2026-07-06.md`
- Refreshed next subplan:
  either the existing source-anchor track, a dimensional-lift blocker plan, or
  a closeout plan depending on the result.

## Required Checks, Tests, Reviews

Before execution:

- Skeptical plan audit: confirm the proposed command answers only whether the
  frozen-step trajectory timeout can be repaired or localized.
- Confirm Phase 6 final JSON exists, validates, has wrapper status `passed`,
  and records public tuner hard veto `phase6_public_timeout_soft_deadline`.
- Confirm the final Phase 6 public tuning result has no
  `windowed_stage_acceptance_telemetry_invalid_or_default` hard veto.
- Inspect the public timeout closeout fields: elapsed time, remaining time,
  reserve, estimated next-candidate seconds, candidate count, completed
  candidate count, and resume-split public summary.
- Compile any changed harness or tests.
- Run focused CPU-hidden tests covering windowed acceptance provenance and
  Phase 5/Phase 6 artifact plumbing.
- Run `git diff --check`.
- Run claim-boundary scan over Phase 7 files.
- Use visible Codex substitute review if Claude remains blocked by private
  context-transfer policy.

Execution may choose exactly one of these routes after review:

- `route_a_timeout_budget`: rerun the same public tuner with a reviewed larger
  public timeout budget and unchanged target/settings except for artifact
  paths and timeout policy.
- `route_b_split_resume`: use the existing Phase 6 private resume-split public
  summary to resume from the Phase 5 selected handoff, if a BayesFilter-owned
  public-safe entry point exists and tests cover the handoff contract.
- `route_c_scope_reduction`: reduce frozen-step trajectory candidate scope only
  if the review explains why the reduced scope still answers the timeout
  localization question and does not create a false pass.

After execution:

- Validate JSON with `python -m json.tool`.
- Count private diagnostic event lines when present and report the count only
  as handoff/provenance context.
- Write Phase 7 result with decision and inference-status tables.
- Refresh the next subplan and record whether source-anchor/comparator tracks
  remain deferred or can resume.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the frozen-step trajectory stage complete, or can its timeout be localized, under a reviewed timeout/resume/scope route after the Phase 6 acceptance-telemetry repair? |
| Baseline/comparator | Phase 6 final rerun artifacts with public tuner hard veto `phase6_public_timeout_soft_deadline`; Phase 4 native divergence unavailability carried forward. |
| Candidate/mechanism under test | Only the frozen-step trajectory timeout/handoff route selected by review. |
| Primary pass criterion | A valid structured artifact either completes the frozen-step trajectory stage and produces a non-promoting public final-kernel handoff candidate, or records a precise timeout/runtime blocker with required provenance. |
| Promotion criterion | None in this phase. A final kernel, if produced, is a handoff artifact only and requires later validation. |
| Veto diagnostics | Invalid artifact, nonfinite target/value/score, missing required public tuning artifact, unsupported default-like telemetry, proxy divergence substitution, private mechanics exposure, unsupported zero-divergence claim, post-hoc threshold edits, or unsupported correctness/readiness/ranking claim. |
| Continuation veto | Broken target/reference precondition, missing Phase 6 artifacts, inability to distinguish timeout from implementation failure, private artifact exposure, or review nonconvergence. |
| Explanatory diagnostics | Public timeout closeout fields, stage statuses, runtime, repair triggers, private event count, selected-pair existence, and public-safe resume-split summary. |
| Not concluded | Zero divergences, posterior correctness, broad HMC convergence, tuned-kernel superiority, ranking, default readiness, production readiness, public API/package readiness, source-faithful Zhao-Cui parity, dimensional generality, or LEDH evidence. |

## Forbidden Claims And Actions

- Do not treat the Phase 6 timeout as evidence against the target, math, or
  HMC direction unless a reviewed continuation veto fires.
- Do not weaken timeout hard vetoes without artifact-backed replacement
  provenance.
- Do not expose private HMC mechanics, private paths, raw draws, positions,
  log-prob values, or private candidate grids in public artifacts.
- Do not claim zero divergences while native divergence telemetry remains
  unavailable.
- Do not treat acceptance/log-accept/target-log-prob as native divergence.
- Do not claim posterior correctness, broad HMC convergence, ranking,
  superiority, default readiness, production readiness, public API/package
  readiness, source-faithful Zhao-Cui parity, dimensional generality, or LEDH
  evidence.
- Do not change public HMC defaults, model files, package state, or
  source-faithful Zhao-Cui route in this phase.

## Exact Next-Phase Handoff Conditions

Proceed to a refreshed source-anchor or dimensional-lift planning subplan only
if Phase 7 records one of:

- a completed frozen-step trajectory stage with a valid non-promoting final
  kernel handoff candidate and no hard vetoes; or
- a valid blocker result that explains why HMC handoff remains blocked and why
  the next non-HMC documentation track is still useful.

Proceed to comparator/readiness planning only after a separate reviewed plan
establishes the validity evidence needed for comparison. A Phase 7 timeout
repair alone cannot justify comparator ranking or readiness claims.

## Stop Conditions

Stop on invalid artifact, nonfinite target/value/score, missing required Phase
6 artifacts, private mechanics exposure, inability to distinguish a timeout
from an implementation failure, proxy-divergence substitution, unsupported
readiness/correctness/ranking/source-faithful claims, review nonconvergence, or
any need to cross an unreviewed runtime/product/scientific/model-file boundary.

## Review Prompt Boundary

If a review bundle is sent to Claude, include only compact excerpts and artifact
summaries. Do not send whole files. If Claude is blocked by private
context-transfer policy, record the block and use a visible Codex substitute
review. Claude is read-only and cannot authorize crossing runtime, model-file,
funding, product-capability, public API, default-policy, or scientific-claim
boundaries.
