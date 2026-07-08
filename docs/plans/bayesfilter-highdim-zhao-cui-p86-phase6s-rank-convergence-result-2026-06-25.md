# P86 Phase 6S Result: Rank Convergence Ledger

Date: 2026-06-25

Status: `BLOCK_P86_PHASE6S_RANK_CONVERGENCE_NOT_ESTABLISHED_REVIEWED`

## Current Decision

Rank convergence is not established.

The Phase 6S adaptive rank-5 artifact is mechanically admissible after the
classifier repair, but its holdout residual is materially worse than the Phase
5 rank-4 lower rung. The comparison blocks Phase 7 correctness/HMC/production
handoff.

Ledger artifact:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank-convergence-ledger-2026-06-25.json`

## Decision Table

| Field | Status |
|---|---|
| Decision | Block rank convergence. |
| Primary criterion status | Failed: adaptive rank-5 holdout residual is `43.24741898709909x` the rank-4 holdout residual. |
| Veto diagnostic status | Mechanical admissibility gates pass after classifier repair; convergence veto fails. Degree convergence remains blocked pending reviewed configurable-basis execution. |
| Main uncertainty | Whether the rank-5 failure is optimizer/objective pathology, overfitting, normalizer collapse, initialization sensitivity, or evidence against this fixed training-base route. |
| Next justified action | Stop the production-promotion path; if continuing, plan a smaller discriminating diagnostic around objective/normalizer/validation behavior. |
| What is not being concluded | No production readiness, no posterior correctness failure theorem, no rejection of the Zhao-Cui paper, no HMC readiness, no LEDH comparison, no GPU scale claim, and no source-faithful TT-cross training claim. |

## Comparator Table

| Field | Rank 4 lower rung | Adaptive rank 5 comparator |
|---|---:|---:|
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json` |
| Status | `P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE_COMPLETED` | raw `BLOCK_P86_PHASE6S_ADAPTIVE_RANK5_COMPARATOR_TRAINING_BASE`; mechanically admissible after classifier repair |
| Rank | `4` | `5` |
| Parameters | `18216` | `28380` |
| Training samples | `364320` | `567600` |
| Fit residual | `0.22022907890919044` | `9.625018868846658` |
| Holdout residual | `0.22090990401849483` | `9.553783177487691` |
| Normalizer | `1.696098696075702e-06` | `4.038658791921966e-08` |
| Runtime seconds | `56.53906785399886` | `250.7143890260195` |
| Peak memory MiB | `2173.27734375` | `3082.3125` |

## Deltas

- fit residual delta: `9.404789789937467`
- holdout residual delta: `9.332873273469196`
- fit residual ratio: `43.70457400406282`
- holdout residual ratio: `43.24741898709909`
- normalizer ratio: `0.023811460983225788`
- sqrt-square normalizer ratio: `0.018021834686389565`

## Evidence Contract Check

| Contract item | Result |
|---|---|
| Question | Are adjacent same-route rank rungs stable enough to pass the Phase 6 rank-convergence gate after adaptive rank-5 repair? |
| Baseline/comparator | Rank 4 Phase 5 training-base artifact versus Phase 6S adaptive rank-5 artifact. |
| Primary criterion | Failed: rank-5 fit/holdout residuals are much worse than rank 4. |
| Veto diagnostics | Rank-5 mechanical admissibility passes after classifier repair, but rank-convergence veto fails. |
| Explanatory diagnostics | Validation trace worsened after step 16 while training loss continued improving; normalizer is much smaller at rank 5. |
| Not concluded | This does not prove the Zhao-Cui paper is wrong and does not establish posterior correctness failure. It blocks this fixed training-base production promotion path. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank-convergence-ledger-2026-06-25.json` |

## Interpretation

The original rank-5 failure was not a fair final convergence failure because it
used a fixed-step optimizer with no plateau scheduler. Phase 6S fixed that
protocol issue enough to produce a replayable adaptive rank-5 artifact.

The repaired rank-5 artifact still fails the convergence gate. The failure is
now a meaningful training-route diagnostic: validation residual was best at the
first validation check and worsened steadily despite continued training-loss
improvement. That pattern points to overfitting, objective/normalizer pathology,
or initialization sensitivity, not to a simple "rank 5 needed more epochs"
story.

## Local Checks

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py
```

Result:

```text
41 passed, 2 warnings
```

## Next Handoff

Do not proceed to Phase 7 correctness/HMC/production promotion from this
evidence. If continuing, draft a new reviewed diagnostic subplan focused on the
smallest discriminating question among:

- validation/overfitting behavior;
- objective-vs-holdout mismatch;
- normalizer collapse;
- initialization sensitivity;
- whether an author-source-faithful TT-cross route is needed rather than the
  fixed training-base adaptation.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank-convergence-result-2026-06-25.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6S rank-convergence result correctly block rank convergence after comparing rank 4 and adaptive rank 5, preserve that the adaptive rank-5 artifact is mechanically admissible after classifier repair but numerically much worse, avoid production/HMC/source-faithful TT-cross/paper-rejection claims, and hand off safely to a new smaller diagnostic subplan rather than Phase 7? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed rank convergence is correctly blocked.
- Claude agreed the result preserves the repaired-artifact distinction:
  adaptive rank 5 is mechanically admissible after classifier repair but
  numerically much worse.
- Claude agreed forbidden production, HMC, source-faithful TT-cross, posterior
  correctness failure, and Zhao-Cui paper rejection claims are avoided.
- Claude agreed the handoff is to a new smaller diagnostic subplan rather than
  Phase 7.
- Claude noted only a minor nuance: the interpretation language is appropriately
  tentative.

Verdict:

```text
VERDICT: AGREE
```
