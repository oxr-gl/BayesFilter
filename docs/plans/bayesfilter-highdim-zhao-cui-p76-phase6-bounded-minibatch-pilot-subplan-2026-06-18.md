# P76 Phase 6 Subplan: Bounded UKF-Frame Mini-Batch Pilot

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_APPROVAL_REQUIRED_BEFORE_EXECUTION
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement the smallest opt-in author-SIR step-1 pilot that actually tests the
P76 hypothesis:

\[
  \hbox{UKF moments}
  \to
  \hbox{UKF local coordinate frame}
  \to
  h_0
  \to
  \hbox{fresh-batch density training}
  \to
  \hbox{audit-separated diagnostics}.
\]

Phase 6 must not compare another ladder of the failed P75 methods.  It tests
one live option: true UKF initialization plus fresh mini-batch training.

## Entry Conditions Inherited From Phase 5

Phase 6 may begin only if:

- Phase 4 smoke result is accepted by Claude;
- Phase 5 result exists and states that Phase 4 is mechanics evidence only;
- this Phase 6 subplan is reviewed and accepted by Claude;
- the user separately approves the Phase 6 implementation edits and bounded
  CPU-only pilot command;
- no GPU/CUDA, package installation, network, detached execution, default
  change, or destructive action is required.

## Required Artifacts

Phase 6 must produce, if executed:

- implementation edits, scoped to a new dedicated script:
  - `scripts/p76_bounded_ukf_minibatch_pilot.py`;
- focused tests, scoped to one or both of:
  - `tests/highdim/test_p76_ukf_initializer.py`;
  - a new dedicated P76 pilot-script test;
- pilot JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json`;
- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-result-2026-06-18.md`;
- Phase 7 decision subplan or stop handoff;
- updated execution, review, runbook, and stop-handoff records.

## Required Checks/Tests/Reviews

Pre-implementation checks:

```bash
rg -n "def spatial_sir_ukf_scout|class UKFScoutResult|P52_UKF_SCOUT_CLAIM" bayesfilter/highdim/ukf_scout.py
rg -n "def p76_build_ukf_initializer|P76_UKF_INITIALIZER_RULE|P76_ROUTE_CLASSIFICATION" bayesfilter/highdim/ukf_initializer.py
rg -n "def _p69_author_sir_source_diagnostic_data_for_step|class SourceRouteCoordinateFrame|def _target_pilot_payload_from_context" bayesfilter/highdim/source_route.py scripts/p75_stochastic_density_training_pilot.py
```

Implementation checks after edits:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p76_bounded_ukf_minibatch_pilot.py bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p75_stochastic_density_training.py
```

Do not edit `scripts/p75_stochastic_density_training_pilot.py` in Phase 6.
The dedicated P76 script is required so the P76 UKF-frame pilot cannot be
confused with the old P75 random/calibrated/source-prefit surface.

Pilot command, only after the user approves Phase 6 execution:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_bounded_ukf_minibatch_pilot.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json --degree 2 --rank 4 --batch-size 128 --batches 20 --max-seconds 600 --seed 7606
```

Local artifact checks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
rg -n "P76_PHASE6_BOUNDED_UKF_MINIBATCH_PILOT|ukf_frame|ukf_initializer|fresh_training_batches|audit_data_used|source_route_prefit_used|cpu_only|not lower-gate repair|not validation|not HMC readiness" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-result-2026-06-18.md
git diff --check -- scripts/p76_bounded_ukf_minibatch_pilot.py scripts/p75_stochastic_density_training_pilot.py tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p75_stochastic_density_training.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Review:

- Claude read-only review of implementation diff, pilot JSON/result, and
  Phase 7 handoff;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does a true UKF-frame initializer plus fresh mini-batch training show bounded pilot viability on the author-SIR step-1 target? |
| Exact baseline/comparator | Phase 4 mechanics smoke and historical P75 failures. No live failed-method ladder in Phase 6. |
| Primary pilot criterion | The operational UKF-frame bridge check passes, the pilot completes the declared CPU-only budget, training uses fresh non-audit batches, audit holdout/replay/line diagnostics are reported, and no veto fires. |
| Diagnostics that can veto | Coordinate-frame mismatch; all or near-all UKF-frame coordinates clipped; nonfinite target values; nonfinite loss/gradient/rho/normalizer/log-density; audit-data leakage; source-route prefit use; GPU use; default change; pilot exceeds declared budget. |
| Explanatory only | Loss trace, gradient norms, normalizer/rho ranges, clipping fractions below veto, audit residual magnitudes, runtime. |
| What will not be concluded | No lower-gate repair, no validation/HMC readiness, no source-faithfulness, no scaling, no final rank/sample policy. |
| Artifact preserving result | Pilot JSON, Phase 6 result, tests, ledgers, Claude review. |

## Required Implementation Details

The implementation must:

- build the author-SIR model with `zhao_cui_sir_austria_model()` and simulated
  observations with seed `5901`, matching the P75 target context;
- run `spatial_sir_ukf_scout(model, config=UKFScoutConfig(horizon=1),
  observations=observations[:2])` or an equivalent horizon-1 call with the
  same observation path used by the target;
- construct the P76 adjacent moments for `time_index=1`;
- convert the P76 UKF center and linear map into a
  `SourceRouteCoordinateFrame` with:
  \[
    r=m_A^U + L_U z ,
  \]
  where \(L_U\) is the P76 UKF local-map matrix;
- run the operational UKF-frame bridge check before any training;
- use the same frame to generate fresh training batches by calling the
  source-route diagnostic-data generator with training-only seeds;
- use distinct audit holdout/replay seeds only after training;
- build `P76UKFInitializerConfig` with a product basis in the same UKF frame;
- initialize `TrainableFunctionalTT` from the P76 initializer cores;
- run only the declared number of mini-batches;
- record runtime provenance with `sys.executable`, `sys.argv`, CPU-only
  environment snapshot, git state if available, seeds, degree, rank,
  batch-size, batch count, and wall time.

The pilot JSON must include at least:

- `status`;
- `schema_version`;
- `run_manifest`;
- `ukf_frame_manifest`;
- `initializer_manifest`;
- `training_seed_policy`;
- `fresh_training_batches: true`;
- `audit_data_used: false`;
- `source_route_prefit_used: false`;
- `default_behavior_changed: false`;
- `cpu_only: true`;
- `degree`, `rank`, `batch_size`, `requested_batches`,
  `completed_batches`;
- clipping fractions for training and audit data;
- finite flags for loss, gradient, rho, normalizer, and log-density;
- audit holdout/replay residuals and line diagnostics;
- `ukf_frame_bridge`;
- nonclaims.

## Operational UKF-Frame Bridge Check

Before training, the dedicated Phase 6 script must build and record a
`ukf_frame_bridge` block.  The block must include:

- `status`;
- `target_dimension`;
- `frame_dimension`;
- `product_basis_dimension`;
- `initializer_dimension`;
- `dimension_match`;
- `frame_hash`;
- `training_frame_hashes`;
- `audit_frame_hashes`;
- `reconstruction_max_abs_error`;
- `target_tieout_max_abs_error`;
- `training_clip_fraction_max`;
- `audit_clip_fraction_max`;
- `bridge_target_values_finite`;
- `training_target_values_finite`;
- `audit_target_values_finite`;
- `nonfinite_target_value_count`;
- `thresholds`;
- `blockers`.

The bridge check passes only if all of the following hold:

- `frame_dimension == product_basis_dimension == initializer_dimension ==
  target_dimension`;
- every training and audit batch records the same `frame_hash`;
- for deterministic probe points \(z_j\in[-1,1]^D\),
  \[
    \max_j \left\|z_j
    - L_U^{-1}\left((m_A^U+L_Uz_j)-m_A^U\right)\right\|_\infty
    \le 10^{-10};
  \]
- for the same probe points, the target values produced through the Phase 6
  UKF-frame batch path agree with a direct physical-density evaluation using
  the same shift and Jacobian convention to absolute error at most \(10^{-10}\);
- `training_clip_fraction_max <= 0.25`;
- `audit_clip_fraction_max <= 0.25`;
- `bridge_target_values_finite`, `training_target_values_finite`, and
  `audit_target_values_finite` are all true;
- `nonfinite_target_value_count == 0`.

If the bridge check fails, Phase 6 must write a blocker result and stop before
optimizer construction or training.  A bridge failure is not evidence against
the UKF idea unless the failure is classified after checking whether it is an
implementation, frame-support, or target-evaluation problem.

## Approval Boundary

This subplan itself does not authorize running the Phase 6 pilot command.
Before executing Phase 6 implementation edits or the pilot command, ask the
user for explicit approval.  A suitable approval sentence is:

`I approve P76 Phase 6 implementation edits and the bounded CPU-only pilot
command exactly as reviewed, with no GPU/CUDA, no package installs, no network,
no detached execution, no default changes, and no large-pilot escalation.`

If the user approval excludes implementation edits or pilot execution, obey
the narrower approval.

## Forbidden Claims/Actions

- Do not use GPU/CUDA.
- Do not run a large mini-batch pilot.
- Do not change defaults.
- Do not install or fetch packages.
- Do not use network.
- Do not launch detached agents.
- Do not use audit samples for initialization, training, stopping, or
  hyperparameter selection.
- Do not use source-route prefit.
- Do not compare random, calibrated constant, or source-route prefit as live
  repair ladders.
- Do not claim lower-gate repair, validation readiness, HMC readiness,
  source-faithfulness, scaling, or final rank/sample policy.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only if:

- Phase 6 result exists;
- pilot JSON exists and parses, or a precise blocker result exists;
- implementation checks pass, or failures are classified as implementation,
  tuning, evidence-against-UKF, or environment blockers;
- Claude agrees Phase 6 interpretation and the Phase 7 subplan are bounded;
- any next pilot or larger budget has a new reviewed subplan and user
  approval.

## Stop Conditions

Stop if:

- the UKF frame cannot be tied to the source-route target coordinates;
- the pilot would require using the old source-route recentered frame while
  claiming to test the UKF frame;
- the `ukf_frame_bridge.status` is not pass;
- all or near-all generated local coordinates clip in the UKF frame;
- target values, losses, gradients, normalizers, rho, or log-density become
  nonfinite;
- audit separation cannot be preserved;
- the only possible next action is a large pilot or GPU run without separate
  approval;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

The main risk is a coordinate-frame false positive: a pilot could appear to
train while the P76 initializer and the target batches use different local
coordinates.  Phase 6 therefore makes the UKF-frame bridge a hard gate before
training, with explicit reconstruction, target tieout, frame-hash, and
clipping thresholds.  A second risk is proxy promotion: even a passing pilot
remains bounded diagnostic evidence only and cannot establish lower-gate
repair or HMC readiness.
