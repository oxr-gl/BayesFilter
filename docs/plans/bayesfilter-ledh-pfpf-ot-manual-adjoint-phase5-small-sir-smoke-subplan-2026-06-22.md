# Manual Adjoint Phase 5 Subplan: Opt-In Integration And Small SIR Smoke

status: DRAFT_READY_AFTER_M4_REVIEW
date: 2026-06-22
phase: M5-SMALL-SIR-SMOKE

## Phase Objective

Implement the first opt-in filter-loop integration of the private
manual/custom-gradient route and run small bounded SIR/LEDH mechanics tests.
Raw AD may be used only on tiny cases where it is cheap enough to serve as a
local comparator.

## Entry Conditions

- M4 integration design result is complete and reviewed.
- M4 records exact integration points, retained/replay policy, and smoke test
  commands.
- M3 private dense route remains passing.
- M4 design states the default replay contract:
  recompute `C(x, stop_gradient(x))` under the same stopped-key rule.
- M4 design pins canonical M5 comparators, tolerances, branch ownership,
  mask/log-weight ownership, and halt rules.

## Required Artifacts

- Opt-in integration diff and focused tests.
- Small-smoke JSON or markdown diagnostics.
- Phase 5 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase5-small-sir-smoke-result-2026-06-22.md`
- Refreshed M6 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

- Unit tests for opt-in routing and unsupported/default-route rejection.
- Unit tests proving defaults remain unchanged and existing public route names
  remain available.
- Unit tests rejecting unsupported manual-route combinations:
  streaming, warmstart, vector `epsilon`, unsupported `transport_ad_mode`, and
  any governed N10000 validation launcher added in M5.
- Transport-matrix value parity against the M3 value helper for the same
  stopped-key scalar.
- Transport-matrix gradient parity for particles/log weights against tiny raw
  TensorFlow autodiff of that same M3 value helper.
- Mixed active/inactive mask test proving inactive rows keep identity
  transport/original log weights and active rows use manual transport/uniform
  log weights.
- Tiny SIR mechanics smoke, CPU-only if sufficient for shape/value tests.
- Trusted GPU smoke only if the subplan/result needs GPU placement evidence.
- Raw AD comparison only for tiny cases with an explicit bounded command.
- `python -m py_compile` for edited Python files.
- `git diff --check`.
- Claude read-only implementation/test review.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the private manual/custom-gradient route be invoked through an opt-in filter-loop path on small bounded SIR cases without changing defaults? |
| Baseline/comparator | M3 stopped-key value helper for transport values; tiny raw AD of the same stopped-key value helper for transport gradients; tiny fixed-branch value/score smoke for integration. |
| Primary criterion | Opt-in tests pass; defaults remain unchanged; tiny smoke has finite value/gradient and expected route metadata. |
| Veto diagnostics | Default route changed; unsupported modes accepted; nonfinite values; raw full-AD N10000 launched; route metadata missing; tiny raw AD mismatch beyond M5 tolerance. |
| Explanatory diagnostics | Device placement, runtime, memory if available, tiny raw-AD delta, route metadata, and seed manifest. |
| Not concluded | No N10000 feasibility, no streaming memory improvement, no P82 FD agreement, no HMC/default/posterior readiness. |

Initial M5 tolerances unless patched before execution:

- transport value max absolute error: `1e-10`;
- transport gradient max absolute error: `1e-8`;
- tiny value/score graph/eager parity: `1e-10`;
- finite value/score/gradient: required.

## Forbidden Claims / Actions

- Do not promote the opt-in path to default.
- Do not run N10000 actual-gradient or N1000 FD validation.
- Do not treat tiny raw AD comparison as large-scale correctness evidence.
- Do not claim HMC readiness.

## Next-Phase Handoff Conditions

M6 may proceed only if M5 records:

- opt-in route name and metadata;
- passing tests and tiny smoke diagnostics;
- default-route non-mutation evidence;
- exact manual-route unsupported combinations;
- remaining memory bottleneck and streaming/chunked design question.

## Stop Conditions

Stop if opt-in integration cannot be isolated, if default behavior changes, if
tiny values/gradients are nonfinite, if tiny raw-AD parity fails materially, or
if GPU/trusted execution is required but unavailable.

Also stop if unsupported-combination rejection fails, mixed-mask behavior
fails, tiny transport value parity fails, tiny transport gradient parity fails,
or graph/eager parity fails when graph mode is claimed.  Do not advance to M6
after such a failure without a visible repair loop and focused rerun.
