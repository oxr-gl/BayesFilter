# P76 Phase 6 Result: Bounded UKF-Frame Mini-Batch Pilot

metadata_date: 2026-06-18
status: CLAUDE_AGREE_PHASE6_CLOSED_READY_FOR_PHASE7
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-subplan-2026-06-18.md
pilot_json: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
phase: 6
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 6 implemented and ran the reviewed bounded CPU-only P76 pilot:

\[
  \hbox{UKF scout moments}
  \to
  \hbox{UKF local coordinate frame}
  \to
  h_0
  \to
  \hbox{fresh-batch density training}
  \to
  \hbox{audit-separated diagnostics}.
\]

This phase does not claim lower-gate repair, validation readiness, HMC
readiness, source-faithfulness, scaling, or final rank/sample policy.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does a true UKF-frame initializer plus fresh mini-batch training show bounded pilot viability on the author-SIR step-1 target? |
| Exact baseline/comparator | Phase 4 mechanics smoke and historical P75 failures. No live failed-method ladder. |
| Primary pilot criterion | UKF-frame bridge passes; pilot completes declared CPU-only budget; training uses fresh non-audit batches; audit holdout/replay/line diagnostics are reported; no nonfinite or boundary veto fires. |
| Veto diagnostics | Coordinate-frame mismatch; near-all clipping; nonfinite targets/loss/gradient/rho/normalizer/log-density; audit leakage; source-route prefit use; GPU use; default change; budget overrun. |
| Explanatory only | Loss trace, gradient norms, normalizer/rho ranges, clipping below veto, audit residual magnitudes, runtime. |
| Not concluded | No lower-gate repair, validation/HMC readiness, source-faithfulness, scaling, or final rank/sample policy. |

## Implementation

Implemented dedicated Phase 6 script:

- `scripts/p76_bounded_ukf_minibatch_pilot.py`

Added focused tests:

- `tests/highdim/test_p76_bounded_ukf_minibatch_pilot.py`

The script builds the author-SIR model and observations from the same seed as
the P75 target context, runs a horizon-1 UKF scout, builds the P76 local frame
\(r=m_U+L_U z\), constructs the P76 initializer cores in that same product
basis, and generates fresh training/audit batches through the same UKF frame.
It does not edit `scripts/p75_stochastic_density_training_pilot.py` and does
not expose the failed random, calibrated-constant, or source-route prefit
ladders as live repair options.

## Pilot Command

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_bounded_ukf_minibatch_pilot.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json --degree 2 --rank 4 --batch-size 128 --batches 20 --max-seconds 600 --seed 7606
```

TensorFlow emitted CUDA plugin/cuInit startup messages even with
`CUDA_VISIBLE_DEVICES=-1`.  The run manifest records `cpu_only: true` and
`cuda_visible_devices: "-1"`.

## Main Findings

The UKF-frame bridge passed.

- target/frame/product/initializer dimension: `36`;
- frame hashes matched for all training and audit batches;
- reconstruction max error: `6.22052119162378e-15`, below `1e-10`;
- target tieout error: `0.0`, below `1e-10`;
- target tieout source:
  `actual_batch_target_values_vs_independent_direct_physical_density`;
- training clip fraction max: `0.00043402777777777775`, below `0.25`;
- audit clip fraction max: `0.00021701388888888888`, below `0.25`;
- target finite flags all true;
- nonfinite target count: `0`.

The bounded training run completed.

- requested batches: `20`;
- completed batches: `20`;
- batch size: `128`;
- total fresh training draws seen: `2560`;
- raw TT core parameters for degree-2/rank-4/36D: `1656`;
- final loss finite: true;
- final gradient finite: true, gradient norm `2.772741812474346`;
- final normalizer finite: true, normalizer `0.0834454786826895`;
- final rho finite: true, rho range `[21.70185175917391, 6062301548.959457]`;
- stop reason: `max_batches_completed`.

The audit-separated residual diagnostics were extremely poor.

- holdout square-root residual:
  - rms relative: `51258.899375658155`;
  - max relative: `207553.42039112293`;
- replay square-root residual:
  - rms relative: `177661.9261096955`;
  - max relative: `521917.21005986683`;
- line diagnostic status: `block`, with absolute value, max residual, and
  rms residual reasons.

Per the reviewed Phase 6 evidence contract, these audit residual magnitudes
are explanatory only, not a Phase 6 execution veto.  They are nevertheless
strong evidence that this small pilot did not produce a usable approximation
under the inherited square-root residual diagnostic.

## Important Diagnostic Caveat

The inherited audit residual compares the square-root TT \(h_\theta(z)\)
directly with shifted square-root target values.  The training objective,
however, optimizes a normalized density objective through

\[
  \rho_\theta(z)=h_\theta(z)^2+\tau q_0(z),
  \qquad
  p_\theta(z)=\rho_\theta(z)/Z_\theta .
\]

Therefore the enormous audit residuals may reflect one or both of:

- a genuinely poor density approximation;
- a mismatch between the density objective and a square-root-amplitude
  residual diagnostic that is not invariant to sign or normalization.

Phase 7 should diagnose this before interpreting the residuals as purely a
capacity or optimizer failure.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Treat Phase 6 as a completed bounded pilot with negative fit-quality evidence | Passed: bridge passed, CPU-only run completed 20 fresh batches, finite training quantities were reported, and audit diagnostics were separated | No Phase 6 veto fired after correcting audit residuals to explanatory-only status | Whether the large audit residuals mean poor density fit, diagnostic mismatch, insufficient capacity/samples, optimizer instability, or some combination | Draft Phase 7 to separate density-space diagnostics from square-root residual diagnostics and quantify capacity/sample/objective issues | No lower-gate repair, no validation/HMC readiness, no final rank/sample policy, no evidence against the UKF idea at larger or better-tuned budgets |

## Local Checks

Pre-implementation checks:

```bash
rg -n "def spatial_sir_ukf_scout|class UKFScoutResult|P52_UKF_SCOUT_CLAIM" bayesfilter/highdim/ukf_scout.py
rg -n "def p76_build_ukf_initializer|P76_UKF_INITIALIZER_RULE|P76_ROUTE_CLASSIFICATION|def p76_local_frame_from_moments|def p76_adjacent_moments_from_scout" bayesfilter/highdim/ukf_initializer.py
rg -n "def _p69_author_sir_source_diagnostic_data_for_step|class SourceRouteCoordinateFrame|def _target_pilot_payload_from_context|def _target_components|def _target_batch_from_data|def _weighted_residual|frame_hash" bayesfilter/highdim/source_route.py scripts/p75_stochastic_density_training_pilot.py
```

Implementation checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p76_bounded_ukf_minibatch_pilot.py bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p76_bounded_ukf_minibatch_pilot.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p76_bounded_ukf_minibatch_pilot.py tests/highdim/test_p75_stochastic_density_training.py
```

Result:

- `31 passed, 2 warnings`;
- warnings were TensorFlow Probability `distutils` deprecation warnings.

Pilot artifact checks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
rg -n "overall_status|audit_status_not_phase6_veto|audit_residual_magnitudes_explanatory_only|blockers|status|completed_batches|ukf_frame_bridge|training_clip_fraction_max|audit_clip_fraction_max|rms_relative|max_relative|cpu_only|cuda_visible_devices" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
```

Observed:

- JSON parses;
- `gate_summary.overall_status` is `pass`;
- `ukf_frame_bridge.status` is `pass`;
- `fresh_audit.status` is `block`, but recorded as
  `audit_status_not_phase6_veto: true`;
- `source_route_prefit_used: false`;
- `cpu_only: true`.

## Claude R1 Review And Repair

Claude R1 returned `VERDICT: REVISE/BLOCK`.

Claude agreed:

- the script uses one shared UKF-derived frame for the initializer, product
  basis, fresh training batches, target values, and audit diagnostics;
- the failed P75 random, calibrated-constant, and source-route prefit ladders
  are not revived as live repair options;
- under the reviewed Phase 6 evidence contract, large audit residual
  magnitudes are explanatory fit-quality evidence, not a Phase 6 veto;
- the Phase 7 fit-diagnostic subplan is a bounded and logical next step;
- there is no Zhao-Cui source-faithfulness boundary violation because this
  lane is consistently classified as `extension_or_invention` /
  not source-faithful.

Claude blocked on three concrete implementation/provenance issues:

1. the original target tieout compared the direct evaluator to itself, so it
   was not independent;
2. nonfinite training quantities were checked after the loop rather than
   fail-closed during the loop;
3. `run_manifest.elapsed_seconds` was captured at manifest construction time,
   not after the run completed.

Repairs applied:

- bridge target tieout now compares actual batch `target_values` from the
  training/audit target-generation path against an independent direct
  physical-density evaluation at the same local points;
- bridge JSON now records
  `target_tieout_source:
  actual_batch_target_values_vs_independent_direct_physical_density`;
- training now has a fail-closed per-step finite veto and emits
  `P76_PHASE6_BLOCKED_TRAINING_VETO` if a train step raises or nonfinite loss,
  gradient, rho, normalizer, or log-density is detected;
- final wall time is now written after the run completes as
  `run_manifest.elapsed_seconds` and `wall_time_seconds`.
- focused tests now include a guard that the bridge records the actual-batch
  target tieout source and that bridge-blocker payloads mark tieout as
  unevaluated.

## Claude R2 Review And Repair

Claude R2 returned `VERDICT: REVISE/BLOCK`.

Claude agreed the R1 code/artifact repairs were substantively present:

- the bridge target tieout is no longer vacuous;
- the implementation has an in-loop fail-closed path for train-step
  exceptions and nonfinite quantities;
- final wall time is written after completion;
- prior shared-frame, failed-ladder, audit-interpretation, and Phase 7
  boundedness conclusions still hold.

Claude blocked because the repaired fail-closed training-veto path and final
wall-time rewrite were not pinned by focused tests, and the docs could
therefore overstate test coverage.

R2 repairs applied:

- added a focused test for `_training_blocked_payload`, asserting
  `status == P76_PHASE6_BLOCKED_TRAINING_VETO`, blocker propagation,
  stop-reason propagation, and wall-time consistency;
- added a focused test for `_terms_have_nonfinite_veto`, asserting a nonfinite
  loss is detected before any density calls are needed;
- added a focused test for `_with_final_wall_time`, asserting the manifest
  elapsed time is overwritten after completion and mirrored in
  `wall_time_seconds`;
- reran focused CPU-only compile/tests with result `31 passed, 2 warnings`.

## Claude R3 Review

Claude R3 returned `VERDICT: AGREE`.

Claude verified:

- focused tests now cover `_training_blocked_payload`,
  `_terms_have_nonfinite_veto`, and `_with_final_wall_time`;
- the script implements non-vacuous batch-target tieout, in-loop fail-closed
  training vetoes, and final wall-time rewrite;
- the Phase 6 JSON matches repaired artifact claims;
- docs/ledgers describe actual focused test coverage and the local check
  result `31 passed, 2 warnings`;
- prior shared-frame, failed-ladder, audit-interpretation, and Phase 7
  boundedness points still hold.

Phase 6 is closed.  Phase 7 may begin under its reviewed diagnostic subplan.

Repaired pilot summary:

- `target_tieout_max_abs_error`: `0.0`;
- `target_tieout_source`:
  `actual_batch_target_values_vs_independent_direct_physical_density`;
- `run_manifest.elapsed_seconds`: `5.866`;
- `wall_time_seconds`: `5.866`;
- `completed_batches`: `20`;
- `gate_summary.overall_status`: `pass`;
- audit square-root residuals remain extremely poor and explanatory.

## Phase 7 Handoff

Phase 7 should not enlarge the pilot yet.  It should first diagnose what the
Phase 6 negative fit-quality evidence means:

- density-space vs square-root-space diagnostic mismatch;
- train-vs-audit residual separation;
- raw parameter count, effective sample count, and number of optimizer steps;
- target-value dynamic range and weight concentration;
- whether the current degree/rank/batch schedule is obviously underpowered.

Phase 7 remains bounded and must not launch a large mini-batch pilot, change
defaults, use GPU/CUDA, install packages, fetch network resources, or claim
algorithmic repair.
