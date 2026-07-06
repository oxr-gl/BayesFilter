# BayesFilter LEDH Compact Sensitivity Score Master Program

Date: 2026-07-05

## Objective

Replace the current full-history LEDH-PFPF-OT score route with a memory-light,
no-tape, forward-sensitivity score route for the same finite scalar value used
by the LEDH leaderboard row.  The admitted score must be the total derivative
of the executed finite LEDH + finite Sinkhorn scalar with respect to the fixed
parameter vector under fixed base random numbers and a fixed resampling mask.

## Skeptical Plan Audit

This plan should not run implementation or leaderboard commands unless the
following risks are handled.

| Risk | Audit result | Required response |
| --- | --- | --- |
| Wrong baseline | The current admitted diagnostic route is a full-history reverse scan. It is a useful reference but not a memory-light production default. | Treat it as a diagnostic comparator only. |
| Proxy metric promoted as proof | A no-OOM smoke test would not prove score correctness. | Require same-scalar finite-difference checks and tiny-route parity checks. |
| Missing stop condition | A large leaderboard run can fail for runtime or GPU memory reasons. | Stop at the smallest failing artifact and record a blocker rather than claiming admission. |
| Hidden autodiff | Existing generic value-and-score helpers use `GradientTape`; that is not allowed for admitted LEDH score computation. | Add source/runtime no-autodiff tests for the admitted score route. |
| Value/score route mismatch | The value route currently calls the streaming value core, while score uses a separate manual route. | The new score route must execute the same finite LEDH and Sinkhorn formulas as the value route for the tested scalar. |
| Dense transport fallback | Dense transport can mask the intended memory fix. | Default admitted route must use streaming/chunked Sinkhorn JVP, with dense use allowed only in tiny diagnostic references. |
| Unfair leaderboard comparison | Frozen non-LEDH rows are not rerun under the same runtime harness. | Keep runtime cross-ranking forbidden unless a separate plan reruns all arms under one harness. |

Audit decision: pass for Phase 0/1 documentation and local tiny checks.  Full
leaderboard execution is gated on unit and integration tests passing.

## Evidence Contract

Scientific/engineering question: Does the new LEDH score route compute
\(\nabla_\theta \widehat\ell_T(\theta)\) for the same finite scalar
\(\widehat\ell_T\) produced by the fixed-randomness LEDH-PFPF-OT computation,
while avoiding storage of the full filter history?

Baseline/comparators:
- Tiny exact comparator: centered finite differences of the same finite scalar.
- Diagnostic implementation comparator: existing full-history manual reverse
  route on very small `T,N`.
- Runtime/memory comparator: previous full-history route is diagnostic only;
  the production criterion is that the new route carries current sensitivities,
  not all time-step flow history.

Primary pass/fail criteria:
- Same-scalar FD max absolute or relative error meets the stated test threshold
  on tiny deterministic fixtures.
- New compact route agrees with the old manual reverse diagnostic on tiny
  fixtures where the old route is feasible.
- Source and runtime sentinels find no `GradientTape`, `ForwardAccumulator`, or
  outer autodiff score path in the admitted route.
- The admitted default route reports matching value and score route ids.

Veto diagnostics:
- Any score route using tape/autodiff for admitted score computation.
- Any default route using the old full-history `TensorArray` reverse scan.
- Any leaderboard artifact that claims LEDH score admission without same-scalar
  FD evidence.
- Any route that changes the scalar target without a visible new target label.

Explanatory diagnostics only:
- Warm-call timing, GPU memory snapshots, row/column Sinkhorn residuals, ESS,
  and value error versus Kalman.  These diagnose behavior but do not by
  themselves prove score correctness.

Nonclaims:
- This does not prove exact Kalman likelihood correctness.
- This does not prove posterior correctness or HMC readiness.
- This does not rank LEDH runtime against frozen non-LEDH rows.
- This does not certify nonlinear rows until model-specific sensitivities are
  implemented and tested.

Artifact preservation:
- Plan: this file.
- Math documentation: `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`.
- Code: `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
  and, if needed, `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- Tests: targeted `tests/test_*ledh*compact*sensitivity*` modules plus updated
  audit tests.
- Results: JSON/Markdown under `docs/plans` or `docs/benchmarks`.

## Master Phases

### Phase 1: Mathematical Documentation

Objective: Add a complete LaTeX derivation for the compact LEDH sensitivity
score recursion and finite Sinkhorn JVP.

Entry conditions: Existing score mismatch root cause is understood as missing
total derivatives and full-history reverse memory pressure.

Required artifacts:
- LaTeX section with labeled equations for LEDH forward step, sensitivity
  recursion, finite softmin JVP, finite Sinkhorn JVP, transport application JVP,
  score accumulation, and memory complexity.

Required checks/reviews:
- `rg` label/reference check.
- MathDevMCP derivation audit on the new label.
- Claude read-only review if available; otherwise a fresh Codex review packet.

Evidence contract: The derivation must distinguish an exact score, a finite
executed scalar score, and unproved nonlinear/model extensions.

Forbidden claims/actions:
- Do not claim HMC readiness.
- Do not claim exact likelihood correctness.
- Do not say the old route is fixed merely because the derivation exists.

Next-phase handoff conditions: Documentation has a named algorithm and enough
equations to implement a no-tape compact sensitivity route.

Stop conditions: MathDevMCP or reviewer finds an unresolved mathematical
blocker in the recurrence or target definition.

### Phase 2: Transport JVP Primitive

Objective: Implement no-tape streaming forward-mode JVP helpers for the finite
Sinkhorn transport map used by LEDH.

Entry conditions: Phase 1 derivation accepted or patched.

Required artifacts:
- Softmin JVP helper.
- Finite Sinkhorn potential JVP helper.
- Transport-from-potentials JVP helper.
- Total transport JVP helper that includes scale and epsilon-start derivatives.

Required checks/reviews:
- Unit tests against TensorFlow autodiff on tiny fixtures for the local value
  helper only.  Autodiff is allowed as a test oracle, not as admitted score code.
- Unit tests against centered FD directional derivatives.
- Source audit that helper code contains no `GradientTape` or `ForwardAccumulator`.

Evidence contract: Passing tests certify the local finite transport JVP on tiny
fixtures only.

Forbidden claims/actions:
- Do not use dense transport as the default admitted route.
- Do not use autodiff inside the production JVP helper.

Next-phase handoff conditions: JVP helper returns finite tangents and matches
tiny oracles.

Stop conditions: JVP helper cannot match FD/tape oracle within tolerance.

### Phase 3: Compact LGSSM LEDH Sensitivity Route

Objective: Implement a memory-light LGSSM LEDH value-and-score route that
carries current particles, log weights, and their parameter sensitivities.

Entry conditions: Phase 2 transport JVP passes local checks.

Required artifacts:
- New compact route id.
- New value-and-score function.
- Old full-history reverse route renamed or reported as historical diagnostic.

Required checks/reviews:
- Tiny compact-vs-full-history manual reverse parity.
- Tiny compact-vs-centered-FD same-scalar check.
- No-autodiff runtime/source sentinels.
- Value/score same-route metadata checks.

Evidence contract: Passing tests admit the compact route for the LGSSM LEDH
row only.

Forbidden claims/actions:
- Do not use the old reverse route as default.
- Do not claim nonlinear-row score support from LGSSM-only code.

Next-phase handoff conditions: `--score-mode compact-sensitivity` or the
default admitted score path works on small fixtures.

Stop conditions: Compact route fails same-scalar FD or route metadata tests.

### Phase 4: Default Wiring And Demotion

Objective: Make compact sensitivity the default admitted LEDH score route and
demote full-history reverse to historical/diagnostic.

Entry conditions: Phase 3 tests pass.

Required artifacts:
- CLI/default metadata updates.
- Audit tests rejecting old full-history admission.
- Leaderboard builder updated to consume the compact score artifact.

Required checks/reviews:
- Targeted tests for CLI arguments and metadata.
- Claude/fresh-Codex read-only review of default/demotion diff.

Evidence contract: Default wiring is an engineering policy change, not a new
scientific claim.

Forbidden claims/actions:
- Do not delete the historical diagnostic unless tests require only demotion.
- Do not admit score artifacts without FD evidence.

Next-phase handoff conditions: The runner emits compact-route score metadata
and the old route cannot be mistaken for current production default.

Stop conditions: Tests show old route remains default/admitted.

### Phase 5: Leaderboard Rerun

Objective: Rerun the LEDH-inclusive high-dimensional leaderboard using the new
compact score route where supported.

Entry conditions: Phase 4 checks pass.

Required artifacts:
- GPU run command and manifest.
- JSON and Markdown leaderboard outputs.
- Result note with decision table.

Required checks/reviews:
- GPU commands run with escalated permissions.
- Output finite checks.
- Same-scalar score status in artifact.
- No runtime cross-ranking claim against frozen rows unless separately rerun.

Evidence contract: The leaderboard can report LEDH LGSSM compact-score
admission if gates pass; it cannot generalize to unsupported nonlinear rows.

Forbidden claims/actions:
- Do not call partial or unsupported nonlinear LEDH scores admitted.
- Do not rank runtime against frozen rows.

Stop conditions: GPU/XLA/OOM/runtime failure, failed score gate, or missing
artifact.  Record blocker with the smallest failing command.
