# P88 Phase 2 Subplan: Degree-Convergence Execution And Evaluation

Date: 2026-06-27

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Phase Objective

Execute exactly one P88-named CPU-hidden degree-comparator fit from the reviewed
P88 no-fit preflight manifest, then evaluate the frozen Phase 1
degree-convergence protocol. If the exact command passes all mechanical,
validation-shape, and interpretation gates, Phase 2 may promote
`D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`; otherwise the label remains blocked.

## Entry Conditions Inherited From Previous Phase

- Phase 1 froze the degree-convergence protocol and pass/fail thresholds.
- Phase 2A repaired the P86-path-bound runner guard by adding P88-named
  preflight/future-fit artifact identities.
- The P88 no-fit preflight exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json`
- The P88 future fit artifact does not exist before execution:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json`
- P87 baseline remains `D18_SOURCE_ROUTE_EXECUTION_ONLY`.
- Correctness, derivative, HMC, GPU, production, LEDH, and default-policy gates
  remain out of scope.

## Required Artifacts

- P88 preflight JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json`
- P88 fit JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json`
- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-result-2026-06-27.md`
- Refreshed Phase 3 subplan or blocker handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase3-same-target-bridge-design-subplan-2026-06-27.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-execution-ledger-2026-06-27.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-claude-review-ledger-2026-06-27.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-stop-handoff-2026-06-27.md`

## Required Checks/Tests/Reviews

Before Claude review:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json >/tmp/p88_phase2_degree_preflight_json_check.json
test ! -e docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json
rg -n "P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY_NOT_FIT|fit_executed|reserved_preflight_output_path_status|reserved_fit_output_path_status|reserved_not_created_in_p88_phase2|P88 Phase 2 degree comparator preflight|p88_phase2_degree_comparator_preflight.v1" docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p88*.md
```

Claude read-only bounded review of this subplan is required before the fit.

Exact fit command, authorized only after Claude review agrees:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json --target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 --training-sample-count 276000 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8303 --train-process-seed 8403 --holdout-prior-seed 9303 --holdout-process-seed 9403 --audit-prior-seed 9313 --audit-process-seed 9503 --output docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json
```

After execution:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json >/tmp/p88_phase2_degree_fit_json_check.json
rg -n "\"status\": \"P88_PHASE2_DEGREE_ORDER3_RANK4_CANDIDATE_TRAINING_BASE_COMPLETED\"|\"fit_executed\": true|\"output\": \"docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json\"|\"preflight_json\": \"docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json\"|\"preflight_status\": \"P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY_NOT_FIT\"|\"holdout_residual\"|\"fit_residual\"|\"finite_fit_residual_status\": \"ok\"|\"finite_holdout_residual_status\": \"ok\"|\"finite_normalizer_status\": \"ok\"|\"finite_sqrt_square_normalizer_status\": \"ok\"|\"trainable_component_active_status\": \"ok\"|\"trained_core_serialization\"|\"serialized_with_values\"|\"fallback_route_status\": \"not_used\"|\"audit_cloud_tuning_status\": \"not_used_for_tuning\"|\"als_training_status\": \"historical_buggy_stale_route_not_allowed_for_fixed_variant_zhao_cui_training\"|\"memory_status\": \"within_approved_envelope\"|\"runtime_status\": \"within_approved_envelope\"" docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p88*.md
```

The Phase 2 result must compute and record:

- reference holdout residual `0.0389400359426049`;
- candidate final holdout residual;
- candidate best validation holdout and step;
- final/best validation ratio;
- degree threshold `max(0.005, 0.05 * reference_holdout)`;
- degree decision: `favorable`, `stable_equivalent`, or `blocked`;
- all veto diagnostics from this subplan.

The degree decision mapping is binding:

```text
reference_holdout = 0.0389400359426049
threshold = max(0.005, 0.05 * reference_holdout)
delta = candidate_final_holdout - reference_holdout

if candidate_final_holdout < reference_holdout - threshold:
    degree_decision = "favorable"
elif abs(delta) <= threshold:
    degree_decision = "stable_equivalent"
else:
    degree_decision = "blocked"
```

The Phase 2 result must include a gate table with explicit rows for:

- exact preflight path;
- exact output path;
- exact preflight status;
- exact fit status;
- `fit_executed == true`;
- finite fit residual;
- finite holdout residual;
- finite normalizer;
- finite sqrt-square normalizer;
- active trainable component;
- serialized trained cores;
- fallback route not used;
- ALS not revived;
- audit cloud not used for tuning;
- runtime envelope;
- memory envelope;
- validation-shape veto;
- basis classification;
- degree decision.

Claude read-only bounded review of the Phase 2 result and refreshed Phase 3
subplan is required before Phase 2 closes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the P88-named order-3/rank-4 degree-comparator fit satisfy the Phase 1 degree-convergence gate against the reviewed default-order rank-4 reference? |
| Baseline/comparator | Reference: P86 Phase 6W selected `Lagrangep(4,8)` rank-4 zero-L1 holdout `0.0389400359426049`; candidate: P88 `Lagrangep(3,8)` rank-4 zero-L1 fit from the exact command above. |
| Primary criterion | Exact command succeeds; fit JSON status is P88 Phase 2 completed; finite diagnostics, no fallback, no ALS, no audit tuning, runtime/memory envelope, serialized cores, and validation-shape veto pass; candidate/reference decision is favorable or stable under the Phase 1 threshold. |
| Veto diagnostics | Command/path drift; wrong preflight status; future fit output mismatch; nonfinite residual/normalizer; fallback route; ALS revival; audit tuning; runtime/memory breach; max-step exhaustion without plateau/LR-drop explanation; final holdout greater than `2x` best validation holdout; non-default basis called source-faithful; proxy correctness/HMC/production/GPU/default-policy claims. |
| Explanatory diagnostics | Fit/holdout residuals, validation trace, LR drops, completed steps, final/best ratio, runtime, memory, parameter/sample counts. |
| Not concluded | Posterior correctness, `D18_CORRECTNESS_CANDIDATE`, analytical-gradient readiness, HMC readiness, GPU readiness, production readiness, LEDH agreement, d50/d100 scaling, or default-policy readiness. |
| Artifact | P88 fit JSON, Phase 2 result, refreshed Phase 3 subplan, ledgers, and stop handoff. |

## Skeptical Audit Before Execution

| Risk | Phase 2 control |
| --- | --- |
| Wrong baseline | Baseline is fixed to P87 execution-only, P86 Phase 6W rank-4 default-order reference holdout `0.0389400359426049`, and Phase 1 frozen thresholds. |
| Proxy metric promoted | Validation/holdout residuals may pass or veto only the degree gate; they cannot establish correctness, HMC, production, or posterior validity. |
| Missing stop condition | Stop conditions include preflight drift, pre-existing output, nonzero command exit, malformed/wrong-status fit JSON, veto diagnostics, and post-result criterion changes. |
| Unfair comparison | Candidate and reference use the same target identity and rank; the non-default candidate basis remains `extension_or_invention`; sample count follows the same 20x parameter-count rule. |
| Hidden assumptions | The exact command is copied from the P88 no-fit preflight manifest; no hyperparameter, seed, sample, basis, or path edits are allowed after review. |
| Stale context | Pre-review checks revalidate the P88 preflight JSON status/path identity and absence of the future fit artifact. |
| Environment mismatch | The command is CPU-hidden with `CUDA_VISIBLE_DEVICES=-1` and must run in a trusted/escalated context because TensorFlow imports CUDA-capable libraries; GPU logs are not GPU evidence. |
| Artifact mismatch | The required output path is the P88 Phase 2 fit JSON; P86 artifacts cannot satisfy fresh P88 execution. |

The Phase 2 result and execution ledger must explicitly record that the exact
fit command was run with trusted/escalated sandbox permissions, with
`CUDA_VISIBLE_DEVICES=-1`, and that TensorFlow CUDA startup logs are not GPU
evidence.

## Pre-Mortem

- The run could pass mechanically but mislead if a favorable lower-degree
  holdout is treated as correctness; Phase 2 explicitly limits the claim to the
  degree gate.
- The run could fail because of transient TensorFlow/import/environment issues
  rather than the scientific idea; any nonzero exit must be recorded separately
  from evidence against degree convergence.
- The run could overfit despite a good final holdout; the final/best validation
  ratio and LR-drop/early-stop trace are veto diagnostics.
- The run could recreate P86 evidence under a P88 name by path drift; exact
  preflight status, preflight path, output path, and candidate command checks
  are mandatory.
- The run could tempt post-hoc threshold changes; Phase 1 thresholds are frozen
  and cannot be changed after seeing the P88 result.

## Forbidden Claims/Actions

- Do not run any command other than the exact fit command above for Phase 2
  execution.
- Do not tune after seeing fit results.
- Do not use the audit cloud for tuning.
- Do not revive ALS.
- Do not change basis, rank, sample counts, seeds, L1/L2/logZ weights,
  scheduler settings, runtime budget, or output paths.
- Do not call the order-3 non-default basis source-faithful.
- Do not promote correctness, HMC readiness, GPU readiness, production
  readiness, LEDH readiness, d50/d100 scaling, or default-policy readiness.
- Do not run GPU, HMC, production benchmark, package-install, network-fetch, or
  destructive git/filesystem commands.
- Do not omit trusted/escalated execution status, path identity, normalizer,
  serialized-core, ALS, audit-tuning, validation-shape, runtime, or memory rows
  from the Phase 2 result gate table.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only after Phase 2 writes a reviewed result.

If Phase 2 passes:

- hand off `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` as a reviewed upstream fact;
- refresh Phase 3 to design the same-target source-backed correctness bridge;
- preserve that `D18_CORRECTNESS_CANDIDATE` remains unproved until Phase 4.

If Phase 2 fails or is blocked:

- keep `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` blocked;
- refresh Phase 3 only as a blocker-aware design handoff that cannot bypass
  unresolved degree convergence.

## Stop Conditions

- Claude review does not converge after five rounds.
- Preflight JSON is missing, malformed, wrong-status, or path-drifted.
- The future fit artifact already exists before execution.
- The exact command exits nonzero.
- Fit JSON is missing, malformed, wrong-status, or path-drifted.
- Any veto diagnostic fires.
- Result interpretation would require changing pass/fail criteria after seeing
  results.

## End-Of-Phase Requirements

1. Run pre-review local checks.
2. Send this subplan to bounded Claude read-only review.
3. If review revises, patch this subplan visibly, rerun focused checks, and
   retry review up to five rounds.
4. If review agrees, run exactly the fit command above.
5. Run post-execution local checks and compute the Phase 1 criteria.
6. Write the Phase 2 result and refresh Phase 3 subplan, ledgers, and stop
   handoff before final checks.
7. Run final diff hygiene over touched code, tests, and P88 artifacts.
8. Send the Phase 2 result and refreshed Phase 3 subplan to bounded Claude
   read-only review.
9. Advance only if reviews agree; otherwise patch the relevant artifact and
   repeat focused checks/review within the five-round cap, or write a blocker
   result and stop.
