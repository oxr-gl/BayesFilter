# Phase 1 Subplan: Predator-Prey T20 Zhao-Cui Evaluator And Analytical Score

Date: 2026-07-02

Status: `DRAFT_READY_AFTER_PHASE0`

Review status: `CONVERGED_AFTER_CLAUDE_ITERATION_3`

## Phase Objective

Build, or precisely block, the Zhao-Cui value and analytical/manual score
adapter for `zhao_cui_predator_prey_T20` under the real T20 source-scope target.

## Entry Conditions Inherited From Previous Phase

- Phase 0 baseline freeze passed:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase0-baseline-freeze-result-2026-07-02.md`.
- July 1 baseline shows `zhao_cui_predator_prey_T20` / Zhao-Cui as
  `blocked_or_status_only` with `P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED`.
- P47 two-observation lower-rung fixtures are diagnostic only and must not be
  reported as the T20 row.

## Required Artifacts

- Predator-prey T20 target contract: observations, theta coordinates,
  transition density, observation density, value scalar, and row identity.
- Source/route inventory separating reusable code from non-admissible lower
  rungs.
- Implementation or precise blocker result.
- Tests for target alignment, finite value, finite manual score if implemented,
  no autodiff/FD admission, and P47-not-T20 boundary.
- Regenerated leaderboard if status changes.
- Phase 1 result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-result-2026-07-02.md`
- Refreshed Phase 2 subplan.

## Required Checks, Tests, Reviews

- Local target-freeze check proving the row uses T20 observations, not P47.
- Finite value smoke if adapter is implemented.
- Manual analytical score checks if score is implemented.
- FD consistency diagnostic only, never admission evidence.
- Score-at-true calibration if simulator/truth binding is available.
- Route scan for admitted score provenance excluding `GradientTape`,
  `ForwardAccumulator`, `.gradient`, `jacobian`, and FD.
- Claude read-only review of material target contract/result.

## Concrete Inventory Anchors

Phase 1 must inspect and cite these local anchors before implementation or
blocker closeout:

| Anchor | Required check |
| --- | --- |
| `bayesfilter/highdim/models.py` / `PredatorPreySSM` | Freeze state dimension, observation dimension, theta coordinate order, parameter box, true parameters, RK4 transition mean, Gaussian transition density, Gaussian observation density, and T20 simulator binding. |
| `bayesfilter/highdim/models.py` / `p30_predator_prey_fixture_model` | Confirm the fixture used by prior blocker tests is the same predator-prey model contract, not a lower-rung two-observation row. |
| `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py` / `tf_predator_prey_to_fixed_sgqf_model` | Separate reusable value-model wiring from derivative helpers. Current derivative helpers using `tf.GradientTape` are diagnostic only and are not leaderboard-admissible analytical scores. |
| `tests/highdim/test_p45_target_registry.py` | Preserve P45 target-registry boundaries: RK4 closure is not native/paper-scale validation and same-target comparison remains blocked until all routes are reviewed. |
| `tests/highdim/test_p45_predator_prey_comparison_blocker.py` | Preserve the existing rejection that the current scalar Zhao-Cui route requires `state_dim == 1`; any Phase 1 repair must either replace this with a reviewed multistate/manual route or keep a precise blocker. |
| `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase4-predator-prey-comparison-result-2026-06-08.md` | Preserve the prior nonclaims: no P47/T20 promotion, no native predator-prey claim, no CUT4--Zhao-Cui equality claim, and no HMC readiness claim. |

## Exact Phase 1 Command Surface

All TensorFlow checks in this phase are CPU-only and must hide GPU devices
before framework import:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_predator_prey_comparison_blocker.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/models.py bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_predator_prey_comparison_blocker.py
```

Baseline row extraction:

```bash
python -c "import json; p='docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json'; d=json.load(open(p)); rows=[r for r in d['rows'] if r['row_id']=='zhao_cui_predator_prey_T20']; print(json.dumps(rows, indent=2, sort_keys=True))"
```

Route/provenance scans:

```bash
rg -n "GradientTape|ForwardAccumulator|\\.gradient|jacobian|finite.?diff|FD|fd" bayesfilter/highdim bayesfilter/nonlinear tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_predator_prey_comparison_blocker.py
```

If Phase 1 introduces any implementation or test file for the admitted
predator-prey T20 route, append every new path to this route scan before
admission. The admitted route fails if any newly introduced score path depends
on `GradientTape`, `ForwardAccumulator`, `.gradient`, `jacobian`, or FD.

```bash
rg -n "zhao_cui_predator_prey_T20|predator_prey|P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED|blocked_autodiff_not_admitted|P47" docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md docs/plans/bayesfilter-highdim-zhao-cui-p45-phase4-predator-prey-comparison-result-2026-06-08.md
```

Post-repair target-freeze and admission tests, required only if Phase 1
implements or changes the predator-prey T20 route:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py
```

The test module above must include all of these assertions before any row can
move from blocker to admitted status:

- `zhao_cui_predator_prey_T20` uses exactly 20 observations, not the P47
  two-observation lower rung.
- theta coordinates are exactly `(r, K, a, s, u, v)`.
- finite value smoke runs on the admitted Zhao-Cui route.
- finite analytical/manual score smoke runs on the admitted Zhao-Cui route.
- the emitted score provenance string contains `manual` or `analytical` and
  does not contain `autodiff`, `GradientTape`, `ForwardAccumulator`, `fd`, or
  `finite_difference`.
- any FD consistency check is labeled diagnostic/non-admission in the result
  artifact.

Post-repair compile/test bundle:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim bayesfilter/nonlinear docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py tests/test_two_lane_highdim_leaderboard_analytical_scores.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_predator_prey_comparison_blocker.py tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py tests/test_two_lane_highdim_leaderboard_analytical_scores.py
```

Leaderboard regeneration dry run if status changes, writing only `/tmp`
artifacts until the result is reviewed:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output /tmp/bayesfilter-phase1-predator-prey-leaderboard.json --markdown-output /tmp/bayesfilter-phase1-predator-prey-leaderboard.md
```

Regenerated predator-prey row extraction:

```bash
python -c "import json; p='/tmp/bayesfilter-phase1-predator-prey-leaderboard.json'; d=json.load(open(p)); rows=[r for r in d['rows'] if r['row_id']=='zhao_cui_predator_prey_T20']; print(json.dumps(rows, indent=2, sort_keys=True))"
```

If the route remains blocked, the exact post-repair tests may be absent, but
the Phase 1 result must explicitly state that no admitted-route test module was
created because the phase closed as a precise blocker rather than an
implementation repair.

FD diagnostic command, allowed only after finite manual-score smoke and labeled
non-admission:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py -k "fd_diagnostic"
```

Score-at-true calibration command, allowed only if the simulator/truth binding
is explicitly wired in the admitted test module:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py -k "score_at_true"
```

Subplan/result hygiene check:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-subplan-2026-07-02.md docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-claude-review-ledger-2026-07-02.md docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md
```

Longer benchmarks, GPU/XLA, HMC, package/network access, and leaderboard
admission rewrites are outside Phase 1.

## Expected Failure Modes And Repair Triggers

| Failure mode | Repair trigger | Required response |
| --- | --- | --- |
| T20 observations or row identity cannot be recovered from the baseline/current fixtures | Baseline extraction lacks `zhao_cui_predator_prey_T20`, or only a P47/two-observation route is executable | Stop and write a precise target-alignment blocker; do not implement. |
| Value route exists only through a lower-rung P47 diagnostic | Any executable value command uses two observations or lower-rung fixture evidence | Stop row admission; record P47 as diagnostic only. |
| Existing derivative helper uses autodiff | Route scan finds `GradientTape`, `ForwardAccumulator`, `.gradient`, `jacobian`, or FD in the admitted score route | Do not admit score; either implement manual derivatives with tests or write `blocked_autodiff_not_admitted`. |
| Zhao-Cui scalar route rejects two-state predator-prey | Tests raise `scalar nonlinear dense value path requires state_dim == 1` | Repair only if a reviewed multistate/manual evaluator can be wired without changing the target; otherwise keep a precise model-specific blocker. |
| Manual derivative is algebraically ambiguous | RK4 transition sensitivity or density-score terms cannot be written in the phase result with theta coordinates | Stop and write derivative blocker; do not substitute autodiff/FD. |
| Finite value/score is nonfinite at true theta | Smoke emits NaN/Inf | Stop row admission and isolate value vs score failure. |
| Review finds claim-boundary drift | Claude/Codex flags P47 promotion, autodiff admission, source-faithfulness without anchors, or HMC/GPU overclaim | Patch the same subplan/result and rerun focused checks; stop after five rounds for the same blocker. |

## Phase 1 Skeptical Audit / Pre-Mortem

Material risks before execution:

- Wrong baseline: using a P47 or two-observation lower-rung fixture would answer
  a different question than the T20 leaderboard row.
- Proxy metric drift: FD residuals, score norm, runtime, and score-at-true
  diagnostics can explain behavior but cannot admit a score route.
- Hidden implementation assumption: the current predator-prey SGQF adapter can
  build derivative helpers, but those helpers use `GradientTape` and therefore
  are not analytical leaderboard evidence.
- Environment mismatch: Phase 1 is CPU-only; GPU/XLA/HMC performance belongs
  to Phase 5 after row admission or precise blocker classification.
- Unfair comparison: a value-only UKF row or blocked SGQF row cannot be ranked
  as if it had an admitted analytical score.
- Stale context: P45 established closure/blocker/nonclaim boundaries on
  2026-06-08; Phase 1 may supersede the blocker only with new reviewed code
  and tests, not by rewording the old result.

Audit status for launch: `PASSED_AFTER_REVISION` only if the exact command
surface above passes and Claude returns `VERDICT: AGREE` on this revised
subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the predator-prey T20 Zhao-Cui row execute under its real T20 target with admitted analytical/manual score, or must it remain precisely blocked? |
| Baseline/comparator | July 1 blocked Zhao-Cui predator-prey row; T20 source-scope target; P47 only as diagnostic non-admission context. |
| Primary criterion | `executed_value_score` with finite value, finite manual score, theta coordinates, and no autodiff/FD provenance; or precise blocker separating missing target, value evaluator, and score derivative. |
| Veto diagnostics | P47 lower-rung reported as T20; autodiff/FD score admitted; no theta coordinates; nonfinite value/score; target mismatch. |
| Explanatory diagnostics | FD residual, score norm, runtime, score-at-true calibration. |
| Not concluded | No HMC convergence, production GPU readiness, or source-faithful adaptive Zhao-Cui reproduction. |
| Artifact | Phase 1 result and regenerated leaderboard if changed. |

## Forbidden Claims And Actions

- Do not report P47 lower-rung values as `zhao_cui_predator_prey_T20`.
- Do not admit autodiff/FD as analytical score.
- Do not claim source-faithfulness without paper/source anchors.
- Do not run GPU/XLA/HMC in this phase.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 if predator-prey has either:

- an admitted finite value/manual-score Zhao-Cui row with tests and
  regenerated leaderboard; or
- a precise blocker that states the target, theta, value scalar, missing
  evaluator/derivative, and why no score is admitted.

## Stop Conditions

Stop if:

- T20 target identity cannot be established;
- the only executable route is P47 lower-rung diagnostic;
- manual score route would require an unapproved invention;
- Claude/Codex review does not converge after five rounds for the same blocker.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 1 result / close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
