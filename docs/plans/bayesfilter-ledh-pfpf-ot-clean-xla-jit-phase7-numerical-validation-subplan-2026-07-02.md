# Phase 7 Subplan: Numerical Validation

Date: 2026-07-02

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Rerun bounded numerical validation for the actual full route after the loop
hygiene and compiler-metrics repairs. The goal is to check that the tiny
GPU/XLA full route remains numerically connected and directionally consistent;
it is not to prove HMC readiness or exact nonlinear likelihood correctness.

## Entry Conditions Inherited From Previous Phase

- Phase 5 fixed targeted Sinkhorn loop/state mechanics with zero focused
  pre-edit parity difference.
- Phase 6 tiny full-route GPU/XLA compiler metrics passed with finite outputs,
  one concrete function, warm-call reuse, and source-anchored total-VJP route
  evidence.
- Phase 6 also exposed a residual scaling risk: large HLO text even for a tiny
  fixture.
- Static audit still reports stopped-key helper findings. Those helpers remain
  partial-derivative helpers and must not be called scores.

## Required Artifacts

- Phase 7 numerical validation JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-2026-07-02.json`
- Runtime route manifest for the exact executed scalar, either embedded in the
  validation JSON or written separately, showing the selected helper path for
  the full-route transport step.
- Phase 7 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-result-2026-07-02.md`
- Draft Phase 8 closeout subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase8-closeout-subplan-2026-07-02.md`
- Updated execution ledger and Claude review ledger.

## Required Checks, Tests, Reviews

Before execution:

- Codex skeptical audit of this subplan.
- Claude read-only review of the Phase 6 result and this Phase 7 subplan.

During execution:

- Trusted/escalated GPU/CUDA probe before GPU validation.
- A bounded GPU/XLA full-route run using:
  - `transport_plan_mode="streaming"`;
  - `transport_gradient_mode="manual_streaming_finite_sinkhorn_stopped_scale_keys"`;
  - `transport_ad_mode="full"`;
  - `manual-reverse` score route;
  - small but nontrivial `T`, `N`, and seeds;
  - TF32 enabled and float32 route unless a reference arm explicitly disables it.
- Same-scalar FD sentinel for the exact executed scalar, route, seeds, theta,
  fixed mask, fixed randomness, and transport settings.
- Predeclared FD sentinel acceptance rule:
  - statistic: directional derivative of the exact executed scalar along each
    tested basis or diagnostic direction;
  - analytic value: dot product between the reported full-route mean score and
    the tested direction;
  - FD value: central finite difference using the same compiled scalar, same
    fixed observations, same fixed seeds, same fixed transport random keys, and
    same route settings;
  - step adjudication: at least one of the predeclared FD steps must pass and
    no larger-neighborhood step may show the opposite derivative sign when the
    analytic directional magnitude is at least `1.0e-4`;
  - tolerance: pass if absolute error is at most `2 * fd_mcse` when an FD MCSE
    is emitted, or at most `1.0e-3 + 0.02 * max(1, abs(fd_value))` when no FD
    MCSE is emitted;
  - multiple directions: all tested directions must pass this rule.
- Finite objective, per-seed log likelihood, mean gradient, and per-seed
  gradients.
- Repeated same-signature run determinism with explicit pass tolerance:
  objective, log-likelihood, mean gradient, and per-seed gradient max absolute
  repeat deltas must be at most `1.0e-5` for the TF32/float32 GPU route. This
  determinism check is same-process warm-call determinism: build the fixed
  observations, masks, seeds, transport keys, theta, and scalar inputs once;
  call the compiled function twice with the same concrete signature; compare
  outputs from those two calls. Fresh-process reproducibility is explanatory
  only in Phase 7 unless a later reviewed subplan promotes it.
- Runtime route manifest proves the exact executed scalar selected the
  total-VJP full-route helper path; stopped-key helper evidence is not accepted
  as score evidence.
- Phase 5 static/parity checks still pass.

After execution:

- Write the Phase 7 result with a decision table, run manifest, primary
  criterion status, veto status, runtime route manifest summary, and nonclaims.
- Claude read-only review of Phase 7 result before Phase 8.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After clean-loop repairs, does the actual full GPU/XLA route produce finite, connected, same-scalar directional gradients on a bounded fixture? |
| Baseline/comparator | Same scalar central-difference sentinel on the exact executed full route and fixed-randomness fixture. Phase 6 compiler metrics are compiler evidence only, not the numerical comparator. |
| Primary pass criterion | Full-route GPU/XLA run is finite and connected; same-scalar FD sentinel passes the predeclared directional rule in this subplan; same-process warm-call repeat determinism passes with max absolute objective/log-likelihood/mean-gradient/per-seed-gradient deltas at most `1.0e-5`; runtime route manifest confirms the exact executed scalar selected the total-VJP full-route helper path. |
| Veto diagnostics | GPU unavailable under trusted probe; runtime route manifest is missing; route falls back to stopped-key partial derivatives for score evidence; nonfinite objective/gradient; repeat deltas exceed `1.0e-5`; FD sentinel fails; compile/HLO watchpoint exceeds the concrete Phase 7 bound stated below; Phase 5 static/parity checks regress. |
| Explanatory diagnostics | MCSE, relative errors, FD step ladder values, compile/warm timing if available, HLO-size watchpoint values, and per-parameter gradient magnitudes. |
| Not concluded | No exact nonlinear likelihood proof, no posterior correctness, no HMC readiness, no all-model validation, no broad production readiness, and no claim that stopped-key helpers compute scores. |
| Artifact | Phase 7 numerical validation JSON and Phase 7 result markdown. |

## Implementation Details

Prefer an existing P8p runner if it can execute the full route with
`transport_ad_mode="full"` and same-scalar FD sentinel. If the existing runner
cannot record the necessary route metadata or compiler watchpoint, add the
smallest wrapper or output augmentation needed for this phase.

The runtime route manifest must be emitted from the exact validation command
and must include:

- `transport_ad_mode="full"`;
- the selected full-route helper name;
- whether any stopped-key helper was selected for score evidence;
- source anchors or runtime counters sufficient to identify the selected
  helper path;
- the exact scalar route and FD route settings.

The repeat determinism pass rule is tolerance-based, not bitwise: in a single
Python process, construct all fixed inputs once, invoke the same compiled
function twice after compilation/warmup, and require the maximum absolute repeat
delta for objective, log-likelihood, mean gradient, and per-seed gradient to be
at most `1.0e-5` under TF32/float32 GPU execution.

The compile/HLO watchpoint is a veto only under this concrete rule: stop Phase
7 if the bounded validation fixture cannot produce a compiled full-route result
within 10 minutes, or if the emitted HLO text size exceeds the Phase 6 tiny
fixture JSON field `hlo_text_length = 27766809` by more than a factor of 4 for
a fixture that has the same `T`, `N`, and Sinkhorn iteration count. For larger
validation fixtures, HLO size and compile time are explanatory unless a
separate reviewed subplan sets a bound before execution.

Use a bounded fixture first. Do not jump to large `N` or long `T` before the
tiny/full route passes. Suggested first run:

- one or two seeds;
- `T=1` or `T=2`;
- `N=16` or `N=64`;
- two or three FD steps around the current theta;
- small Sinkhorn iteration count if the objective is compiler/numerical
  connectivity, with a later result allowed to recommend a larger validation
  rung.

The result must say plainly whether the derivative being checked is the
derivative of the executed scalar. If not, the run fails the score-validation
target.

The result markdown must include:

- decision table;
- run manifest with commit/dirty state, command, environment, CPU/GPU status,
  seeds, wall time, output paths, plan/result paths, and route config;
- runtime route manifest summary;
- primary criterion and veto status;
- nonclaims.

## Forbidden Claims And Actions

- Do not call a partial derivative a score.
- Do not promote FD, MCSE, or HLO metrics beyond the stated primary criterion.
- Do not run HMC or long validation ladders in Phase 7.
- Do not change FD acceptance rules after seeing results.
- Do not use CPU-only evidence as GPU/XLA evidence.
- Do not claim broad clean-XLA readiness if only the tiny fixture passes.

## Exact Next-Phase Handoff Conditions

Phase 7 may hand off to Phase 8 only if:

- bounded full-route GPU/XLA numerical validation artifact exists;
- primary criterion and veto status are plainly recorded;
- route evidence confirms total-derivative route selection;
- stopped-key helper findings remain correctly classified as partial
  derivatives;
- Phase 7 result and Phase 8 subplan exist;
- Claude read-only review returns `VERDICT: AGREE`, or fixable findings are
  patched and rereviewed.

## Stop Conditions

Stop and write a blocker result if:

- trusted GPU probe fails;
- the full route cannot run under GPU/XLA for the bounded fixture;
- route metadata shows stopped-key partial derivatives are used as score
  evidence;
- runtime route manifest is missing;
- FD sentinel fails under the stated acceptance criterion;
- output is nonfinite;
- repeat deltas exceed `1.0e-5`;
- validation requires changing the scientific target or acceptance criterion;
- Claude and Codex do not converge after five rounds.

## Skeptical Pre-Execution Audit

Result: `PASS_PENDING_CLAUDE_REVIEW`

- Wrong baseline: avoided by requiring same-scalar FD on the exact executed
  full route.
- Proxy promotion: avoided because HLO/compile metrics are explanatory/veto
  watchpoints, not numerical correctness evidence.
- Missing stop conditions: explicit above.
- Unfair comparison: validation must use fixed seeds, fixed randomness, same
  scalar, same theta, and same route.
- Hidden assumption: stopped-key helper findings remain real and must not be
  used as score evidence.
- Environment mismatch: GPU/XLA evidence requires trusted/escalated execution.
- Artifact mismatch: result JSON and markdown are required before Phase 8.
