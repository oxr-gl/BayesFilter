# P88 Phase 2 Result: Degree-Convergence Execution And Evaluation

Date: 2026-06-27

Status: `P88_PHASE2_REVIEWED_CLOSED_RANK_DEGREE_STABLE`

Git commit: `97ad05d40676f3fd15a2a2b4d45034ebb657ed97`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | The exact reviewed P88 Phase 2 order-3/rank-4 degree-comparator fit completed and locally passes the frozen Phase 1 degree gate. |
| Primary criterion status | Locally passed: exact command, P88 fit status, finite diagnostics, serialized cores, no fallback, no ALS, no audit tuning, runtime/memory envelope, validation-shape veto, and favorable degree decision all passed. |
| Veto diagnostic status | No local veto fired. |
| Main uncertainty | Claude has not yet reviewed this result or the refreshed Phase 3 handoff. |
| Next justified action | Send this result and refreshed Phase 3 subplan to bounded Claude review. If both agree, Phase 3 may start with `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` as a reviewed upstream fact. |
| What is not being concluded | No posterior correctness, `D18_CORRECTNESS_CANDIDATE`, analytical-gradient readiness, HMC readiness, GPU readiness, production readiness, LEDH agreement, d50/d100 scaling, or default-policy readiness. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the P88-named order-3/rank-4 degree-comparator fit satisfy the Phase 1 degree-convergence gate against the reviewed default-order rank-4 reference? |
| Baseline/comparator | Reference: P86 Phase 6W selected `Lagrangep(4,8)` rank-4 zero-L1 holdout `0.0389400359426049`; candidate: P88 `Lagrangep(3,8)` rank-4 zero-L1 fit. |
| Primary criterion | Locally passed. |
| Veto diagnostics | No command/path drift, nonfinite diagnostic, fallback route, ALS revival, audit tuning, runtime breach, memory breach, validation-shape failure, or unsupported claim was observed. |
| Explanatory diagnostics | Candidate/reference residuals, validation trace, LR drops, completed steps, runtime, memory, and parameter/sample counts are recorded below. |
| Not concluded | Correctness, HMC, GPU, production, LEDH, scale, and default-policy claims remain blocked. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json` |

## Exact Command Executed

Trusted/escalated sandbox permissions were used, with `CUDA_VISIBLE_DEVICES=-1`.
TensorFlow CUDA/cuInit startup logs appeared and are not GPU evidence.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json --target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 --training-sample-count 276000 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8303 --train-process-seed 8403 --holdout-prior-seed 9303 --holdout-process-seed 9403 --audit-prior-seed 9313 --audit-process-seed 9503 --output docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json
```

## Degree Decision

Binding Phase 1 rule:

```text
reference_holdout = 0.0389400359426049
threshold = max(0.005, 0.05 * reference_holdout) = 0.005
delta = candidate_final_holdout - reference_holdout

if candidate_final_holdout < reference_holdout - threshold:
    degree_decision = "favorable"
elif abs(delta) <= threshold:
    degree_decision = "stable_equivalent"
else:
    degree_decision = "blocked"
```

Observed:

| Metric | Value |
| --- | ---: |
| Reference holdout | `0.0389400359426049` |
| Candidate final holdout | `0.026216776647946836` |
| Candidate fit residual | `0.02642824660809709` |
| Threshold | `0.005` |
| Delta candidate-reference | `-0.012723259294658066` |
| Improvement reference-candidate | `0.012723259294658066` |
| Candidate/reference ratio | `0.6732602067083007` |
| Degree decision | `favorable` |

Reviewed interpretation: `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` is promoted as
a reviewed upstream fact for Phase 3. This is not a correctness claim.

## Gate Table

| Gate | Status | Evidence |
| --- | --- | --- |
| Exact preflight path | Pass | `preflight_json` is `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json`. |
| Exact output path | Pass | `output` is `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json`. |
| Exact preflight status | Pass | `P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY_NOT_FIT`. |
| Exact fit status | Pass | `P88_PHASE2_DEGREE_ORDER3_RANK4_CANDIDATE_TRAINING_BASE_COMPLETED`. |
| `fit_executed == true` | Pass | Fit JSON records `fit_executed: true`. |
| Finite fit residual | Pass | `finite_fit_residual_status: ok`; fit residual `0.02642824660809709`. |
| Finite holdout residual | Pass | `finite_holdout_residual_status: ok`; holdout residual `0.026216776647946836`. |
| Finite normalizer | Pass | `finite_normalizer_status: ok`; normalizer `4.554027196172014e-06`. |
| Finite sqrt-square normalizer | Pass | `finite_sqrt_square_normalizer_status: ok`; sqrt-square normalizer `4.544027196172014e-06`. |
| Active trainable component | Pass | `trainable_component_active_status: ok`. |
| Serialized trained cores | Pass | `serialized_with_values`; `core_count: 36`; `total_values: 13800`. |
| Fallback route not used | Pass | `fallback_route_status: not_used`. |
| ALS not revived | Pass | `historical_buggy_stale_route_not_allowed_for_fixed_variant_zhao_cui_training`. |
| Audit cloud not used for tuning | Pass | `audit_cloud_tuning_status: not_used_for_tuning`. |
| Runtime envelope | Pass | `193.63000839803135` seconds under `7200` seconds. |
| Memory envelope | Pass | `1837.390625` MiB under `12288` MiB. |
| Validation-shape veto | Pass | Best validation holdout `0.021793931728010047` at step `16`; final/best ratio `1.2029392848951825`, below the `2x` veto. |
| Basis classification | Pass | Candidate `Lagrangep(3,8)` remains `extension_or_invention`; reference `Lagrangep(4,8)` remains source-faithful author default. |
| Degree decision | Pass | `favorable` under frozen Phase 1 rule. |

## Training Diagnostics

| Field | Value |
| --- | --- |
| Completed train steps | `272` |
| Requested train steps | `512` |
| Stop reason | `early_stop_after_plateau_lr_drop_limit` |
| Validation check every | `16` |
| Plateau patience | `4` |
| LR drops | `4` |
| Final learning rate | `1.875e-05` |
| Best validation holdout | `0.021793931728010047` at step `16` |
| Final validation/final holdout | `0.026216776647946836` at step `272` |

The run stopped by the reviewed adaptive plateau/LR-drop policy, not by an
unexplained max-step hit.

## Local Checks

Commands:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json >/tmp/p88_phase2_degree_fit_json_check.json
rg -n "\"status\": \"P88_PHASE2_DEGREE_ORDER3_RANK4_CANDIDATE_TRAINING_BASE_COMPLETED\"|\"fit_executed\": true|\"output\": \"docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json\"|\"preflight_json\": \"docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json\"|\"preflight_status\": \"P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY_NOT_FIT\"|\"holdout_residual\"|\"fit_residual\"|\"finite_fit_residual_status\": \"ok\"|\"finite_holdout_residual_status\": \"ok\"|\"finite_normalizer_status\": \"ok\"|\"finite_sqrt_square_normalizer_status\": \"ok\"|\"trainable_component_active_status\": \"ok\"|\"trained_core_serialization\"|\"serialized_with_values\"|\"fallback_route_status\": \"not_used\"|\"audit_cloud_tuning_status\": \"not_used_for_tuning\"|\"als_training_status\": \"historical_buggy_stale_route_not_allowed_for_fixed_variant_zhao_cui_training\"|\"memory_status\": \"within_approved_envelope\"|\"runtime_status\": \"within_approved_envelope\"" docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p88*.md
```

Outcomes:

- Fit JSON validation passed.
- Required gate grep passed.
- Diff hygiene passed.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Command | Exact command above. |
| Sandbox/trust | Ran with trusted/escalated sandbox permissions. |
| Runtime posture | CPU-hidden non-production fit. |
| GPU status | `CUDA_VISIBLE_DEVICES=-1`; TensorFlow CUDA/cuInit startup logs are not GPU evidence. |
| Python | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` recorded in preflight/fit context. |
| Target route | Zhao-Cui SIR Austria d18 fixed source route, setup-static lower-degree Lagrangep comparator. |
| Candidate basis | `Lagrangep(3,8)`, `extension_or_invention`. |
| Reference basis | `Lagrangep(4,8)`, source-faithful author default. |
| Target dimension / rank | `36` / `4`. |
| Parameters / training samples | `13800` / `276000`. |
| Holdout samples | `65536`. |
| Audit samples | `65536`, reserved and not used for tuning. |
| Optimizer | training-base Adam. |
| Learning rate | `0.0003`. |
| Scheduler | validation check every `16`, plateau patience `4`, LR factor `0.5`, stop after `4` LR drops. |
| L1 / L2 / logZ | `0.0` / `1e-8` / `0.0`. |
| Seeds | run `8608`, train `8303/8403`, holdout `9303/9403`, audit `9313/9503`. |
| Runtime/memory envelope | `7200` seconds, `12288` MiB. |
| Actual runtime/peak memory | `193.63000839803135` seconds, `1837.390625` MiB. |
| Preflight | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json` |
| Fit JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json` |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-subplan-2026-06-27.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-result-2026-06-27.md` |

## Boundary Notes

- The lower-degree comparator is `extension_or_invention`, not source-faithful
  author default.
- Favorable degree evidence does not establish posterior correctness.
- `D18_CORRECTNESS_CANDIDATE` remains blocked until a same-target source-backed
  bridge is designed and executed under later reviewed phases.
- L1 tuning remains the Zhao-Cui training-base default procedure; zero-L1 here
  is an allowed comparator arm, not a universal scalar default.
- Audit data were not used for fitting or tuning.
- ALS training remains historical, buggy/stale, and not revived.

## Next Handoff

Refresh and review:

`docs/plans/bayesfilter-highdim-zhao-cui-p88-phase3-same-target-bridge-design-subplan-2026-06-27.md`

Claude agreed with this result and Phase 3 handoff. Phase 3 may start with
`D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` as a reviewed upstream fact. Phase 3 must
not treat this as correctness evidence.

## Claude Review Status

`VERDICT: AGREE`
