# P86 Phase 6 Result: Rank Comparator Preflight

Date: 2026-06-24

Status: `PREFLIGHT_READY_REVIEWED_BLOCKED_BEFORE_COMPARATOR_FIT_APPROVAL`

## Decision

The Phase 6 rank-convergence comparator preflight package has been generated
without fitting. It freezes a same-route rank-5 training-base comparator
candidate against the reviewed Phase 5 rank-4 lower rung.

Preflight artifact:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-convergence-preflight-2026-06-24.json
```

Preflight status:

```text
P86_PHASE6_RANK_CONVERGENCE_PREFLIGHT_READY_NOT_FIT
```

This is not approval to run the comparator fit and is not rank-convergence
evidence.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can Phase 6 freeze a same-route rank-5 comparator package after the reviewed Phase 5 training-base pass without executing the fit or making convergence claims? |
| Baseline/comparator | Lower rung: reviewed Phase 5 rank-4 artifact. Candidate comparator: same-route rank-5 author `Lagrangep(4,8)` plus `AlgebraicMapping(1)` training-base fit. |
| Primary criterion | Preflight JSON reports route identity, rank/sample budget, disjoint clouds/seeds, command/path fidelity, runtime/memory plan, lower-rung admissibility, and exact human-approval requirement before fitting. |
| Veto diagnostics | Historical ALS lower rung; route/backend mismatch; under-budget rank-5 sample floor; command/path drift; cloud overlap; audit tuning; missing exact output path; implicit degree-convergence execution; rank-convergence claim from preflight. |
| Explanatory diagnostics | Planned memory/runtime, sample visits, lower-rung summary metrics, and the known summary-only lower-rung core serialization gap. |
| Not concluded | No rank convergence, degree convergence, posterior correctness, KR closure, HMC readiness, LEDH comparison, GPU performance, source-faithful author TT-cross training, or production readiness. |
| Artifact | Phase 6 rank preflight JSON and this result note. |

## Frozen Candidate Fit Command

The candidate rank-5 comparator command is frozen but not approved:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-convergence-preflight-2026-06-24.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 139 --learning-rate 0.001 --max-seconds 14400 --memory-cap-mib 12288 --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank5-comparator-fit-2026-06-24.json
```

Exact human approval is required before running this command.

## Preflight Evidence

| Field | Value |
|---|---|
| `status` | `P86_PHASE6_RANK_CONVERGENCE_PREFLIGHT_READY_NOT_FIT` |
| `fit_executed` | `false` |
| `training_backend` | `training_base_optimizer` |
| Lower rung status | `P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE_COMPLETED` |
| Lower rung fit rank / `P_theta` | `4` / `18216` |
| Comparator fit rank / `P_theta` | `5` / `28380` |
| Minimum comparator samples | `567600` |
| Comparator training samples | `567600` |
| Optimizer batch / train steps | `4096` / `139` |
| Planned sample visits | `569344` |
| Planned peak memory | `1211.2377014160156 MiB` |
| Memory cap | `12288 MiB` |
| Degree convergence status | `blocked_pending_reviewed_configurable_basis_path` |
| Convergence interpretation status | `preflight_only_no_rank_convergence_claim` |
| Lower-rung core serialization status | `summary_only_no_tt_core_payload_for_functional_delta` |

## Known Gap

The reviewed Phase 5 lower-rung JSON is summary-only and does not serialize
trained TT cores. This is not a blocker for freezing a rank-5 comparator
preflight, but it is a blocker for claiming functional rank convergence from
the current artifacts alone. Final Phase 6 interpretation needs a reviewed
convergence ledger/evaluation artifact after any approved comparator fit.

## Local Checks

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p86_phase5_budget_preflight.py tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py
python - <<'PY' ... P86_PHASE6_RANK_PREFLIGHT_JSON_VALIDATED ... PY
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-convergence-preflight-2026-06-24.json
```

Results:

```text
30 passed, 2 warnings
P86_PHASE6_RANK_PREFLIGHT_JSON_VALIDATED
```

## Next Gate

Claude read-only bounded review returned `VERDICT: AGREE`.

Review summary:

- Claude agreed the note freezes a no-fit Phase 6 rank-5 comparator package
  after the reviewed Phase 5 training-base pass.
- Claude agreed the exact-command approval gate is intact before any fit.
- Claude agreed budget/path/runtime/memory evidence is recorded, with
  disjoint train/holdout/audit seeds visible in the frozen command.
- Claude agreed degree convergence remains blocked pending configurable-basis
  support and unsupported rank-convergence/correctness/HMC/GPU/production
  claims are avoided.

Verdict:

```text
VERDICT: AGREE
```

The next action is to request exact human approval for the frozen rank-5
comparator command or stop before fitting.
