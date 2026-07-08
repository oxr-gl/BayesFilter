# P86 Phase 5 Result: Budget-Compliant Fit Closeout

Date: 2026-06-24

Status: `PASS_P86_PHASE5_TRAINING_BASE_FULL_BUDGET_REVIEWED`

## Current Decision

Phase 5 now has an admissible full-budget CPU-hidden training-base fit artifact
for the P86 fixed-variant Zhao-Cui author `Lagrangep(4,8)` plus
`AlgebraicMapping(1)` route:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json
```

The current fit status is:

```text
P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE_COMPLETED
```

This supersedes the earlier stale ALS full-budget artifact for P86 Phase 5
admission. ALS training is now historical and buggy for the fixed-variant
Zhao-Cui route. Going forward, P86/P85 fixed-variant Zhao-Cui training must use
the training-base optimizer route (`TrainableFunctionalTT` /
`P75ObjectiveBatch` / Adam), not `FixedTTFitter` ALS.

This is a Phase 5 admission result only. It does not establish rank
convergence, posterior correctness, KR closure, HMC readiness, LEDH comparison,
d=50/d=100 scale, GPU performance, source-faithful author TT-cross training,
or production readiness.

## Training-Base Repair Summary

The repaired runner:

- removes `FixedTTFitter`, `FixedTTFitConfig`, and `FixedTTFitSampleBatch`
  from the P86 Phase 5 training path;
- routes fitting through `P75ObjectiveBatch`, `TrainableFunctionalTT`, and
  `make_adam_optimizer`;
- records `training_backend=training_base_optimizer`;
- records
  `historical_als_training_status=historical_buggy_stale_route_not_allowed_for_fixed_variant_zhao_cui_training`;
- feeds unclipped local algebraic coordinates to `ProductBasis`, so
  `AlgebraicMap.to_reference` is applied once inside basis evaluation;
- initializes all author `Lagrangep` nodal coefficients for the constant path,
  avoiding the old Legendre-shaped index-0-only initializer;
- rejects defensive-floor-only artifacts through
  `trainable_component_active_status`.

## Full-Budget Fit Evidence

| Field | Value |
|---|---|
| Fit JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json` |
| `status` | `P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE_COMPLETED` |
| `fit_executed` | `true` |
| `training_backend` | `training_base_optimizer` |
| Historical ALS status | `historical_buggy_stale_route_not_allowed_for_fixed_variant_zhao_cui_training` |
| Route | author `lagrangep` / `algebraic` |
| Target dimension / fit rank | `36` / `4` |
| `P_theta` / training samples | `18216` / `364320` |
| Optimizer | Adam, batch `4096`, train steps `89`, learning rate `0.001` |
| Completed train steps | `89` |
| Planned sample visits | `364544` |
| `normalizer` | `1.696098696075702e-06` |
| `sqrt_square_normalizer` | `1.686098696075702e-06` |
| `fit_residual` / `holdout_residual` | `0.22022907890919044` / `0.22090990401849483` |
| `runtime_seconds` | `56.53906785399886` |
| `peak_memory_mib` / cap | `2173.27734375` / `12288` |
| Core delta | finite and changed |

Post-fit required gates:

| Field | Value |
|---|---|
| `fit_status` | `completed` |
| `finite_target_status` | `ok` |
| `finite_loss_status` | `ok` |
| `finite_normalizer_status` | `ok` |
| `finite_sqrt_square_normalizer_status` | `ok` |
| `trainable_component_active_status` | `ok` |
| `finite_fit_residual_status` | `ok` |
| `finite_holdout_residual_status` | `ok` |
| `fallback_route_status` | `not_used` |
| `audit_cloud_tuning_status` | `not_used_for_tuning` |
| `als_training_status` | `historical_buggy_stale_route_not_allowed_for_fixed_variant_zhao_cui_training` |
| `training_backend_status` | `ok` |
| `runtime_status` | `within_approved_envelope` |
| `memory_status` | `within_approved_envelope` |

## Decision Table

| Field | Status |
|---|---|
| Decision | Phase 5 budget-compliant fit admission passes on the repaired training-base route. Phase 6 may proceed to a refreshed/reviewed rank-convergence subplan and exact comparator-command approval gates. |
| Primary criterion status | Passed: full-budget sample count meets `max(20 * P_theta, 5000)`, exact author route and command/path are preserved, training backend is `training_base_optimizer`, post-fit status fields are acceptable, fit/holdout residuals are finite, active trainable normalizer is positive, memory/runtime are within approved envelope, and audit data were not used for tuning. |
| Veto diagnostic status | No Phase 5 veto remains for the repaired training-base artifact. Historical ALS vetoes are retained only as stale-route provenance. |
| Main uncertainty | This is one CPU-hidden fit with a fixed rank/basis schedule. It does not establish same-route rank/degree convergence or downstream correctness. |
| Next justified action | Refresh and review Phase 6. Rank convergence can be planned from this lower-rung artifact; degree convergence needs a reviewed configurable-basis execution path or must be recorded as out of scope/blocked for the current runner. |
| What is not concluded | No author SIR posterior correctness, KR closure, HMC readiness, LEDH comparison, d=50/d=100 scale, GPU performance, source-faithful author TT-cross training, or production readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Git worktree | Dirty; unrelated dirty files were preserved. |
| Exact preflight command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --preflight-only --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-preflight-2026-06-24.json` |
| Exact approved fit command actually run | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-preflight-2026-06-24.json --target-dimension 36 --fit-rank 4 --training-sample-count 364320 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8605 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 89 --learning-rate 0.001 --max-seconds 14400 --memory-cap-mib 12288 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json` |
| Environment / conda env | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` for runner/test commands. |
| CPU/GPU status | CPU-only / GPU-hidden by intentional `CUDA_VISIBLE_DEVICES=-1`. TensorFlow emitted CUDA/cuInit import noise under GPU hiding; no GPU evidence is claimed. |
| Data version | Source-pushed author SIR clouds generated by the runner from frozen seeds; fit data are summarized in the fit JSON. |
| Random seed | Fit seed `8605`; training cloud prior/process seeds `6301`/`6401`; holdout cloud seeds `7301`/`7401`; audit-reserved seeds `7311`/`7501` were not used for tuning. |
| Output artifacts | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-preflight-2026-06-24.json`; `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json` |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-subplan-2026-06-24.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-result-2026-06-24.md` |

## Local Checks

Commands run after the training-base full-budget artifact was regenerated:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p86_phase5_budget_preflight.py tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py
python - <<'PY' ... P86_PHASE5_TRAINING_BASE_FULL_BUDGET_JSON_VALIDATED ... PY
```

Results:

```text
28 passed, 2 warnings
P86_PHASE5_TRAINING_BASE_FULL_BUDGET_JSON_VALIDATED
```

## Historical ALS Provenance

The earlier full-budget Phase 5 artifact used stale ALS wiring through
`FixedTTFitter`. It produced a blocked result with
`finite_normalizer_status=block`, `sqrt_square_normalizer=0.0`, and
`memory_status=memory_cap_breached`. That artifact is no longer admissible as a
Phase 5 lower rung and must not be used as evidence against the repaired
training-base route.

The historical ALS result remains useful only as provenance for why ALS
training was demoted.

## Phase 6 Handoff

Phase 6 should inherit this final Phase 5 state:

```text
Phase 5 training-base full-budget fit passed local admission on the hard-wired
author Lagrangep(4,8) plus AlgebraicMapping(1) route. The historical ALS block
is stale-route provenance only.
```

Phase 6 may not claim rank/degree convergence from this single artifact. It may
draft/review exact same-route comparator commands. Any fitting command still
requires exact human approval. Degree convergence must not be executed unless a
reviewed configurable-basis runner/subplan exists; otherwise it remains an
explicit Phase 6 limitation or blocker.

## Claude Review Status

Claude read-only bounded review of this refreshed pass closeout returned
`VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-result-2026-06-24.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this refreshed Phase 5 closeout coherently record the repaired training-base full-budget pass, demote ALS as historical stale-route provenance, preserve local checks/evidence/nonclaim boundaries, and hand off safely to Phase 6 without claiming rank convergence, correctness, HMC, GPU, source-faithful author TT-cross training, or production readiness? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed the closeout records the repaired training-base full-budget
  pass, demotes ALS to stale-route provenance, preserves local checks and
  nonclaim boundaries, and hands off safely to Phase 6.
- Claude specifically agreed that the file does not claim rank convergence,
  correctness, HMC readiness, GPU performance, source-faithful author TT-cross
  training, or production readiness.

Verdict:

```text
VERDICT: AGREE
```
