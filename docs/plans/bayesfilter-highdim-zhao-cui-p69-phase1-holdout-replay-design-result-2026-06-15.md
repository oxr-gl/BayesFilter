# P69 Phase 1 Result: Holdout/Replay Diagnostic Design

metadata_date: 2026-06-15
status: P69_PHASE1_HOLDOUT_REPLAY_DESIGN_PASSED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 1 defines a diagnostic-only holdout and replay contract for the P59/P67/P68
Zhao--Cui SIR fixed-HMC adaptation lane.

The design deliberately does not use `FixedTTFitSampleBatch.holdout_points` for
the adjacent ladder rows in Phase 2.  In the current fitter, supplied holdout
points participate in the fit result status: a nonfinite or too-large holdout
residual can turn the fit into `NONFINITE_VALUE` or `HOLDOUT_RESIDUAL_VETO`.
That is useful for a different fitting contract, but it would change the row
status semantics of P67/P68.  P69 needs a diagnostic that says whether the
already fitted fixed branch generalizes and replays, without silently changing
the fitted cores, branch hashes, or ladder thresholds.

Phase 2 should therefore add post-fit diagnostics:

- an out-of-fit diagnostic set in the same local coordinate frame;
- a deterministic replay set that can be regenerated from manifest fields;
- residuals evaluated after fitting;
- hashes for fit points, diagnostic points, replay points, target values,
  weights, coordinate frame, fitted branch, and density branch;
- status fields that can make a ladder row unresolved, inconclusive, or blocked,
  but cannot by themselves prove filtering correctness.

## Source And Classification Ledger

| Design element | Classification | Anchors | Explanation |
| --- | --- | --- | --- |
| Sequential square-root TT density and normalizer route | source_faithful for the mathematical spine only | Zhao--Cui JMLR 2024 local PDF `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf`; source-support ledger `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-source-support-ledger-2026-06-01.md:20`; equation ledger `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-equation-by-equation-ledger-2026-06-01.md:40-42`; author source `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84-124`; `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:81-85` | The paper/source route supports the use of a fitted square-root TT, squaring/defensive mass, and normalizer update.  This does not make the fixed branch an adaptive reproduction. |
| Weighted recentering and local frame | fixed_hmc_adaptation of a source route operation | Author source `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:46-70`; `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47`; local code `bayesfilter/highdim/source_route.py:2354-2480`; `bayesfilter/highdim/source_route.py:6129-6201` | The source uses weighted pushed samples, `computeL`, resampling, and local coordinates.  BayesFilter freezes seeds and uses deterministic resampling for replayability. |
| Existing fit residual and condition diagnostics | fixed_hmc_adaptation | Local code `bayesfilter/highdim/fitting.py:268-291`; `bayesfilter/highdim/source_route.py:3078-3126`; P68 result | These diagnostics expose fit behavior of the fixed least-squares branch.  They are not Zhao--Cui adaptive stopping evidence. |
| Post-fit holdout/replay diagnostics | fixed_hmc_adaptation | Author source `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:95-98` splits local samples into `samples_debug` and `samples_init`; local fitter branch identities `bayesfilter/highdim/fitting.py:573-610`; current P67/P68 manifest path `scripts/p67_author_sir_adjacent_ladder_diagnostics.py:242-331` | The author code has a fitting/debug data split for the adaptive TTSIRT object, but P69's post-fit residuals are a BayesFilter fixed-branch diagnostic.  They must not be advertised as adaptive source-faithful validation. |

## Design Contract

### Diagnostic Sets

For each fixed-TTSIRT fit at step \(t\), Phase 2 should construct two
diagnostic batches after the fit data are constructed and before row results are
serialized.

1.  `diagnostic_holdout`:
    - same target dimension, source target order, coordinate frame, shifted
      target convention, and previous-retained object as the fitted branch;
    - deterministic construction recorded in the manifest;
    - not included in the ALS normal equations;
    - not passed to `FixedTTFitter.fit` as `holdout_points` for P67/P68 row
      comparisons;
    - evaluated against the fitted square-root TT after the fitted branch hash
      has been recorded.

2.  `replay`:
    - deterministic points in the same local frame;
    - preferably a small fixed subset or deterministic transform of the same
      source-route pushed/resampled local coordinate cloud;
    - used to verify that the target evaluator, fitted TT evaluator, density
      evaluator, and row manifest can be regenerated and compared;
    - not a new source of fitting information.

The safest Phase 2 starting rule is a deterministic even/odd split of the
source-route local fitting cloud before fitting:

- fitting points: the columns used by the current P67 row fit;
- diagnostic points: a disjoint deterministic subset generated by the same
  pushed-sample, recentering, resampling, clipping, target-shift, and previous
  retained-object route, with a separate recorded seed or index rule.

If Phase 2 cannot make the diagnostic subset disjoint without changing the fit
sample budget or prior retained object, it must stop with
`BLOCK_HOLDOUT_REPLAY_DESIGN_NEEDS_ROUTE_CHANGE`.

### Residuals

For a diagnostic batch \((z_i,y_i,\omega_i)_{i=1}^M\) in local coordinates,
record
\[
  R_{\rm rms}
  =
  \left(
    \frac{\sum_{i=1}^M \omega_i
      \left(\widehat\phi_t(z_i)-y_i\right)^2}
    {\sum_{i=1}^M \omega_i}
  \right)^{1/2}.
\]
Here \(\widehat\phi_t\) is the fitted square-root TT value, and \(y_i\) is the
same shifted square-root target value used for the fit.  This residual is a
diagnostic of local square-root fit generalization, not a proof of filtering
correctness.

For density replay, also record finite/nonfinite status and optional log-density
differences between
\[
  \log\bigl(\widehat\phi_t(z_i)^2+\tau_t\lambda(z_i)\bigr)
\]
and the shifted target density quantity when both are available in the same
measure convention.  These log-density diagnostics are explanatory unless a
later reviewed phase declares thresholds before seeing the replay values.

### Branch Identity Invariant

Phase 2 must record the following invariant for each step:

- `fit_branch_hash_before_diagnostic`;
- `fit_branch_hash_after_diagnostic`;
- `density_branch_hash_before_diagnostic`;
- `density_branch_hash_after_diagnostic`;
- `branch_identity_unchanged_by_diagnostics`.

The invariant passes only if the before/after hashes match exactly.  A mismatch
is a hard blocker: `BLOCK_BRANCH_IDENTITY_DRIFT`.

### Manifest Fields

Phase 2 should add these fields under each step-level fit-quality record or a
new sibling `holdout_replay_diagnostics_by_step` record:

- `diagnostic_role`: `post_fit_diagnostic_only`;
- `diagnostic_classification`: `fixed_hmc_adaptation`;
- `fit_point_count`;
- `fit_point_hash`;
- `fit_target_hash`;
- `fit_weight_hash`;
- `coordinate_frame_hash`;
- `holdout_available`;
- `holdout_status`;
- `holdout_point_count`;
- `holdout_point_hash`;
- `holdout_target_hash`;
- `holdout_weight_hash`;
- `holdout_construction`;
- `holdout_disjoint_from_fit`;
- `holdout_residual`;
- `holdout_residual_available`;
- `holdout_nonfinite`;
- `holdout_threshold_role`: `diagnostic_only_unless_predeclared`;
- `replay_available`;
- `replay_status`;
- `replay_identity`;
- `replay_point_count`;
- `replay_point_hash`;
- `replay_target_hash`;
- `replay_weight_hash`;
- `replay_residual`;
- `replay_residual_available`;
- `replay_nonfinite`;
- `fit_branch_hash_before_diagnostic`;
- `fit_branch_hash_after_diagnostic`;
- `density_branch_hash_before_diagnostic`;
- `density_branch_hash_after_diagnostic`;
- `branch_identity_unchanged_by_diagnostics`;
- `source_route_invariants`;
- `fixed_branch_adaptation_class`;
- `nonclaims`.

The P67 row-level payload should also expose summarized fields:

- `holdout_replay_diagnostics_by_step`;
- `holdout_unavailable_steps`;
- `holdout_nonfinite_steps`;
- `replay_unavailable_steps`;
- `replay_nonfinite_steps`;
- `branch_identity_drift_steps`;
- `diagnostic_only_steps`;
- `holdout_replay_resolution_status`.

### Status Taxonomy

Use these statuses in Phase 2 and Phase 3:

- `PASS_HOLDOUT_REPLAY_DIAGNOSTICS_AVAILABLE`;
- `WARN_HOLDOUT_REPLAY_DIAGNOSTIC_ONLY`;
- `BLOCK_HOLDOUT_REPLAY_DIAGNOSTICS_MISSING`;
- `BLOCK_HOLDOUT_REPLAY_NONFINITE`;
- `BLOCK_HOLDOUT_REPLAY_ROUTE_MISMATCH`;
- `BLOCK_BRANCH_IDENTITY_DRIFT`;
- `BLOCK_HOLDOUT_REPLAY_DESIGN_NEEDS_ROUTE_CHANGE`;
- `BLOCK_HOLDOUT_REPLAY_THRESHOLD_EXCEEDED`, only if Phase 3 predeclares a
  numerical threshold before rerun;
- `INCONCLUSIVE_HOLDOUT_REPLAY_UNTHRESHOLDED`, when finite diagnostics exist
  but no reviewed threshold permits promotion.

### Interpretation Rules

- A missing diagnostic keeps the row unresolved.
- A nonfinite diagnostic blocks the row.
- A branch-identity drift blocks the row.
- A finite diagnostic with no predeclared threshold is explanatory only.
- A finite diagnostic below a predeclared threshold may remove the
  holdout/replay-unavailable blocker, but it still does not prove filtering
  correctness.
- Rank-ladder zero delta cannot be promoted until rank-channel activity is
  checked in Phase 4.
- Degree-ladder threshold failures remain blockers unless a later reviewed
  phase changes the branch or route before rerun.  Thresholds must not be
  changed after seeing new data.

## Phase 2 Implementation Scope

Phase 2 may edit only:

- `bayesfilter/highdim/source_route.py`;
- `scripts/p67_author_sir_adjacent_ladder_diagnostics.py`;
- focused tests under `tests/highdim/`;
- P69 plan/result ledgers.

Phase 2 should not:

- change P67 ladder thresholds;
- rerun the full adjacent ladder;
- introduce GPU/HMC execution;
- change default backends away from TensorFlow/TensorFlow Probability;
- change `FixedTTFitter.fit` status semantics unless a separate reviewed
  subplan is written.

The smallest acceptable implementation is:

1. Add a helper that computes a post-fit weighted RMS residual for a fitted
   `FunctionalTT` on diagnostic local points.
2. Add deterministic diagnostic point construction and hashing to the P59/P67
   SIR fixed branch.
3. Expose the manifest fields above.
4. Update P67 budget diagnostics so finite post-fit holdout/replay fields remove
   only the `holdout_unavailable_steps` unresolved marker.
5. Add focused tests with small sample counts and a fake-diagnostic unit test
   for the P67 budget logic.

## Required Phase 2 Checks

Phase 2 must run these local checks before review:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim/test_p59_author_sir_step_spec_assembly.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

If a new dedicated test file is added, include it in the focused pytest command.

## Skeptical Plan Audit

| Audit item | Phase 1 result |
| --- | --- |
| Wrong baseline | Controlled: P68 is the immediate predecessor; P67/P66/P65 are supporting context. |
| Proxy metric promoted to pass criterion | Controlled: residuals are diagnostic/veto evidence only unless later thresholds are predeclared. |
| Missing stop condition | Controlled: route-change, branch-drift, nonfinite, missing diagnostic, and review-convergence stops are explicit. |
| Unfair comparison | Controlled: Phase 2 must preserve row thresholds and comparison invariants. |
| Hidden assumption | Controlled: current lane is fixed-HMC adaptation; adaptive reproduction is not claimed. |
| Stale context | Controlled: Phase 1 read P68, P67 runner, `source_route.py`, `fitting.py`, source-support ledgers, and author source anchors. |
| Environment mismatch | Controlled: Phase 1 is design-only; Phase 2 checks are CPU-only. |
| Artifact does not answer question | Controlled: this result gives the concrete manifest, status, invariant, and Phase 2 test contract needed before implementation. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What holdout/replay diagnostics should be added so adjacent-ladder rows can be interpreted without silently changing the fixed branch or thresholds? |
| Primary criterion status | Passed: this result specifies diagnostic construction, manifest fields, status taxonomy, checks, and Phase 2 scope; Claude R3 returned `VERDICT: AGREE`. |
| Veto diagnostic status | No threshold change, no validation claim, no adaptive parity claim, no use of holdout residual as correctness, and no fit-branch mutation is allowed. |
| Main uncertainty | Whether Phase 2 can construct a truly disjoint diagnostic set without changing the row route; if not, Phase 2 must stop. |
| Next justified action | Refresh and review the Phase 2 implementation subplan, then implement only if Claude returns `VERDICT: AGREE`. |
| Not concluded | No implementation, no ladder rerun, no d18 correctness, no d50/d100 scaling, no HMC readiness, no adaptive Zhao--Cui reproduction. |

## Local Checks

Planned after writing this result:

```bash
rg -n "post_fit_diagnostic_only|BLOCK_BRANCH_IDENTITY_DRIFT|diagnostic_only_unless_predeclared|fixed_hmc_adaptation|no d18 correctness|no HMC readiness" docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-holdout-replay-design-result-2026-06-15.md docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-subplan-2026-06-15.md
rg -n "thresholds changed|source-faithful adaptive|d18 correctness claim|HMC readiness claim" docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-holdout-replay-design-result-2026-06-15.md docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-subplan-2026-06-15.md
```

The second command is expected to return no matches except quoted forbidden
phrases in explicit nonclaim/forbidden-action contexts.

Observed result:

- Positive-marker text check found the required diagnostic-role,
  branch-drift, threshold-role, and `fixed_hmc_adaptation` markers.
- Forbidden-phrase text check found only explicit veto/nonclaim contexts.

## Claude Review

- R1 returned `VERDICT: REVISE`.
  - Required repair: make replay symmetric with holdout in Phase 2 gates.
  - Required repair: add an explicit diagnostic-cloud feasibility checkpoint
    before broader Phase 2 edits.
- R2 returned `VERDICT: REVISE`.
  - Required repair: ensure the required pytest command includes the exact
    touched holdout/replay/P67-focused tests, even if assertions are added to an
    existing file.
- R3 returned `VERDICT: AGREE`.

Review ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p69-claude-review-ledger-2026-06-15.md`

## Handoff To Phase 2

Phase 2 may begin only after:

- this result passes local text checks;
- the Phase 2 subplan is refreshed from this design;
- Claude read-only review returns `VERDICT: AGREE`.

These conditions are satisfied.  Phase 2 must begin with Task 0, the
diagnostic-cloud feasibility checkpoint, before implementation edits.
