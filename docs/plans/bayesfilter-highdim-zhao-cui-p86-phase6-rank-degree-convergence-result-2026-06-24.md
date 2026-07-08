# P86 Phase 6 Result: Rank And Degree Convergence

Date: 2026-06-24

Status: `BLOCK_P86_PHASE6_RANK_DEGREE_CONVERGENCE_NOT_ESTABLISHED_REVIEWED`

## Current Decision

Phase 6 has an admissible same-route rank-5 comparator fit artifact, but rank
convergence is not established and degree convergence remains blocked.

The rank-5 comparator fit JSON reports:

```text
P86_PHASE6_RANK5_COMPARATOR_TRAINING_BASE_COMPLETED
```

That completion is an artifact-admissibility result only. It does not pass the
Phase 6 rank/degree convergence gate, because the comparator residuals are much
worse than the reviewed rank-4 lower rung and the available artifacts are
summary-only rather than serialized trained TT cores suitable for a reviewed
functional-delta convergence test.

Degree convergence is still blocked because the current P86 runner is
hard-wired to author `Lagrangep(4,8)` plus `AlgebraicMapping(1)`. Any
degree/order/element comparison needs a reviewed configurable-basis execution
path and exact command approval before fitting.

## Comparator Fit Status

| Field | Rank 4 lower rung | Rank 5 comparator |
|---|---:|---:|
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank5-comparator-fit-2026-06-24.json` |
| Status | `P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE_COMPLETED` | `P86_PHASE6_RANK5_COMPARATOR_TRAINING_BASE_COMPLETED` |
| Backend | `training_base_optimizer` | `training_base_optimizer` |
| Fit rank | `4` | `5` |
| `P_theta` | `18216` | `28380` |
| Training samples | `364320` | `567600` |
| Completed train steps | `89` | `139` |
| Planned sample visits | `364544` | `569344` |
| `normalizer` | `1.696098696075702e-06` | `3.9049342442131245e-08` |
| `sqrt_square_normalizer` | `1.686098696075702e-06` | `2.904934244213124e-08` |
| `fit_residual` | `0.22022907890919044` | `21.67632778142163` |
| `holdout_residual` | `0.22090990401849483` | `21.41256396525755` |
| Runtime seconds | `56.53906785399886` | `98.29290339001454` |
| Peak memory MiB / cap | `2173.27734375` / `12288` | `3080.56640625` / `12288` |

Rank-5 post-fit status fields are acceptable for comparator artifact
admissibility: finite target/loss/normalizers/residuals, active trainable
component, no fallback route, no audit-cloud tuning, runtime within envelope,
memory within envelope, and `training_backend_status=ok`.

## Return-Code Repair

The approved rank-5 command produced a completed JSON artifact but exited with
code `1` because the CLI success predicate still accepted only the Phase 5
completed status. The runner has now been patched so fit mode exits
successfully for both:

```text
P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE_COMPLETED
P86_PHASE6_RANK5_COMPARATOR_TRAINING_BASE_COMPLETED
```

Focused test coverage was added for that predicate. The rank-5 fit was not
rerun for this code-only return-classification repair.

## Decision Table

| Field | Status |
|---|---|
| Decision | Phase 6 is blocked: rank-5 comparator artifact is admissible, but rank convergence is not established; degree convergence is blocked pending reviewed configurable-basis execution. |
| Primary criterion status | Not passed. Same-route comparator exists, but there is no reviewed positive convergence ledger: rank-5 fit and holdout residuals are about `98.42x` and `96.93x` the rank-4 residuals, and trained TT core payloads are not serialized for functional-delta evaluation. |
| Veto diagnostic status | No artifact-admissibility veto for the rank-5 comparator. Convergence promotion is vetoed by insufficient reviewed convergence evidence and adverse residual diagnostics. Historical ALS remains excluded. |
| Main uncertainty | This is one CPU-hidden training-base rank comparison. It may reflect optimizer/tuning limitations, rank-5 initialization/training dynamics, or target approximation behavior; it is not evidence against the mathematical idea by itself. |
| Next justified action | Refresh Phase 7 as a blocker or tightly reframed bridge note. Do not run correctness, KR, HMC, LEDH, scale, or production-promotion phases as passes while Phase 6 remains unresolved. |
| What is not concluded | No rank convergence, degree convergence, posterior correctness, KR closure, HMC readiness, LEDH comparison, d=50/d=100 scale, GPU performance, source-faithful author TT-cross training, or production readiness. |

## Evidence Contract Check

| Contract item | Result |
|---|---|
| Question | Adjacent same-route rank stability is not established; degree convergence is not executable in the current hard-wired runner. |
| Baseline/comparator | Baseline is the reviewed rank-4 training-base lower rung. Comparator is the approved rank-5 training-base artifact. |
| Primary criterion | Not met. Comparator artifact exists, but reviewed convergence evidence is insufficient and residual diagnostics are adverse. |
| Veto diagnostics | ALS was not used; route/backend match; comparator budget and clouds are frozen; no audit tuning; no runtime or memory breach; no unapproved command beyond the user-approved rank-5 fit. |
| Explanatory diagnostics | Residuals, normalizers, optimizer trace, runtime, and memory are preserved in the JSON artifacts and convergence ledger. |
| Not concluded | All correctness, HMC, LEDH, scale, GPU, and production claims remain forbidden. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-ledger-2026-06-24.json` |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Git worktree | Dirty; unrelated dirty files were preserved. |
| Exact approved rank-5 command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-convergence-preflight-2026-06-24.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 139 --learning-rate 0.001 --max-seconds 14400 --memory-cap-mib 12288 --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank5-comparator-fit-2026-06-24.json` |
| Environment / conda env | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` for runner/test commands. |
| CPU/GPU status | CPU-only / GPU-hidden by intentional `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence is claimed. |
| Data version | Source-pushed author SIR clouds generated by the runner from frozen seeds. |
| Rank-5 seeds | Fit seed `8606`; train prior/process seeds `8301`/`8401`; holdout prior/process seeds `9301`/`9401`; audit-reserved seeds `9311`/`9501` were not used for tuning. |
| Output artifacts | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-convergence-preflight-2026-06-24.json`; `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank5-comparator-fit-2026-06-24.json`; `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-ledger-2026-06-24.json` |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-subplan-2026-06-24.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-result-2026-06-24.md` |

## Local Checks

Commands run after the return-code repair and rank-5 artifact validation:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY' ... P86_PHASE6_RANK5_COMPARATOR_JSON_VALIDATED ... PY
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
```

Results:

```text
31 passed, 2 warnings
P86_PHASE6_RANK5_COMPARATOR_JSON_VALIDATED
```

The first JSON validator attempt used the wrong local key name
`train_process_noise_seed`; the artifact schema uses `train_process_seed` and
`holdout_process_seed`. The validator was corrected to match the actual P86
manifest schema and then passed.

## Phase 7 Handoff

Phase 7 should inherit this final Phase 6 state:

```text
Phase 6 produced an admissible same-route rank-5 comparator artifact, but rank
convergence is not established and degree convergence remains blocked pending a
reviewed configurable-basis execution path.
```

Therefore Phase 7 may not proceed as a normal correctness-bridge pass path. It
may only write a precise correctness-bridge blocker or a reviewed reframing note
that preserves the Phase 6 blocker and does not claim posterior correctness,
HMC readiness, KR closure, LEDH comparison, scale, or production readiness.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-result-2026-06-24.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6 result correctly record that the rank-5 comparator artifact is admissible while rank convergence is not established, degree convergence is blocked pending reviewed configurable-basis execution, the CLI return-code bug was patched without rerunning the fit, local checks are adequate, nonclaim boundaries are preserved, and Phase 7 handoff is safe? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed the result correctly separates rank-5 artifact admissibility
  from rank-convergence promotion.
- Claude agreed degree convergence remains blocked pending reviewed
  configurable-basis execution.
- Claude agreed the CLI return-code repair is recorded as a code-only
  classification fix without rerunning the rank-5 fit.
- Claude agreed local checks are adequate for the narrow claim made.
- Claude agreed nonclaim boundaries and the Phase 7 blocker/reframing handoff
  are safe.

Verdict:

```text
VERDICT: AGREE
```
