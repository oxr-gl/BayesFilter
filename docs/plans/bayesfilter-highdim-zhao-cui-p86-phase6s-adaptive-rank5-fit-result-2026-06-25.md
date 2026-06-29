# P86 Phase 6S Result: Adaptive Rank-5 Fit

Date: 2026-06-25

Status: `BLOCK_P86_PHASE6S_ADAPTIVE_RANK5_CONVERGENCE_NOT_ESTABLISHED_REVIEWED`

## Current Decision

The exact approved Phase 6S CPU-hidden adaptive rank-5 fit command executed and
wrote:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json`

The raw JSON status is:

```text
BLOCK_P86_PHASE6S_ADAPTIVE_RANK5_COMPARATOR_TRAINING_BASE
```

Post-run validation found this raw block was caused by a narrow runner
classifier bug: the fit-status classifier treated any run that stopped before
the max-step ceiling as `incomplete_optimizer_steps`, even when adaptive
training stopped by the approved scheduler plateau/LR-drop rule. The code now
classifies `scheduler_stopped_after_plateau` as a completed adaptive protocol
outcome while preserving fixed-budget max-step exhaustion as non-converged.

No long rerun was performed after this classifier repair. The saved artifact is
therefore interpreted as mechanically admissible after classifier repair, but
it does not establish rank convergence. Its holdout residual is much worse
than the Phase 5 rank-4 lower rung.

## Exact Command Executed

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 1024 --learning-rate 0.001 --max-seconds 14400 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json
```

## Decision Table

| Field | Status |
|---|---|
| Decision | Adaptive rank-5 fit executed and produced a replayable artifact, but rank convergence is not established. |
| Primary criterion status | Mixed: command/artifact/training mechanics passed after classifier repair; numerical convergence versus rank 4 fails. |
| Veto diagnostic status | No fallback, no ALS, no audit tuning, finite diagnostics, runtime/memory within envelope, validation trace present, trained cores serialized. Convergence veto: rank-5 holdout residual is far worse than rank 4. |
| Main uncertainty | Whether the poor rank-5 result is optimizer/objective pathology, overfitting/normalizer collapse, initialization issue, or evidence against this fixed training-base route. |
| Next justified action | Write a convergence ledger comparing rank 4 against the repaired rank-5 artifact, then stop or plan a smaller discriminating diagnostic. |
| What is not being concluded | No rank convergence, degree convergence, posterior correctness, KR closure, HMC readiness, LEDH comparison, scale, GPU performance, source-faithful TT-cross training, production readiness, or default-policy change. |

## Evidence Contract Check

| Contract item | Result |
|---|---|
| Question | Does the same-route rank-5 comparator train under the repaired adaptive scheduler without fixed-budget exhaustion and with replayable trained cores? |
| Baseline/comparator | Baseline is the Phase 5 rank-4 training-base artifact; diagnostic predecessor is the old fixed-budget rank-5 artifact. |
| Primary criterion | Mechanically passed after classifier repair: exact command, adaptive scheduler stop, validation trace, serialized trained cores, finite diagnostics, no fallback/audit tuning. Scientifically failed for rank convergence versus rank 4. |
| Veto diagnostics | Raw artifact status was blocked by the classifier bug. After repair, remaining engineering vetoes pass. Rank-convergence veto remains because holdout residual worsened from `0.22090990401849483` at rank 4 to `9.553783177487691` at rank 5. |
| Explanatory diagnostics | LR events, validation residual trajectory, fit/holdout residuals, normalizers, runtime, memory, and core hashes. |
| Not concluded | No rank convergence and no production promotion. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json` |

## Artifact Validation Summary

Post-run validator facts:

- raw status:
  `BLOCK_P86_PHASE6S_ADAPTIVE_RANK5_COMPARATOR_TRAINING_BASE`
- repaired classification:
  `P86_PHASE6S_ADAPTIVE_RANK5_COMPARATOR_TRAINING_BASE_ADMISSIBLE_AFTER_CLASSIFIER_REPAIR`
- `fit_executed`: `true`
- `training_backend`: `training_base_optimizer`
- completed train steps: `272`
- requested max train steps: `1024`
- stop reason: `early_stop_after_plateau_lr_drop_limit`
- training convergence status: `scheduler_stopped_after_plateau`
- validation trace length: `17`
- trained-core serialization status: `serialized_with_values`
- serialized values: `28380`
- runtime: `250.7143890260195` seconds
- peak memory: `3082.3125` MiB
- memory cap: `12288` MiB

Post-fit statuses:

- fallback route: `not_used`
- audit-cloud tuning: `not_used_for_tuning`
- finite loss: `ok`
- finite normalizer: `ok`
- finite sqrt-square normalizer: `ok`
- trainable component active: `ok`
- finite fit residual: `ok`
- finite holdout residual: `ok`
- runtime: `within_approved_envelope`
- memory: `within_approved_envelope`

Rank-5 numerical diagnostics:

- fit residual: `9.625018868846658`
- holdout residual: `9.553783177487691`
- normalizer: `4.038658791921966e-08`
- sqrt-square normalizer: `3.038658791921966e-08`
- best validation monitor value: `0.030539674365849725` at step `16`
- final validation monitor value: `9.553783177487691` at step `272`
- LR drops: `4`
- final learning rate: `0.0000625`

Rank-4 lower-rung diagnostics from Phase 5:

- fit residual: `0.22022907890919044`
- holdout residual: `0.22090990401849483`
- normalizer: `1.696098696075702e-06`
- sqrt-square normalizer: `1.686098696075702e-06`

Interpretation: adaptive rank 5 is mechanically admissible as a repaired
artifact, but it is not a rank-converged improvement. The validation trajectory
worsened after the first validation check even as the training loss continued
to improve, which is consistent with overfitting or objective/normalizer
pathology and must be treated as a convergence veto.

## Classifier Repair

Changed `scripts/p86_author_lagrangep_phase5_budget_fit.py`:

- added `_training_protocol_completed`;
- classified `scheduler_stopped_after_plateau` as completed adaptive protocol;
- preserved strict fixed-budget completion for non-adaptive runs.

Changed `tests/highdim/test_p86_phase5_budget_preflight.py`:

- added success-status coverage for Phase 6S;
- added protocol-completion tests distinguishing scheduler plateau stop from
  incomplete non-scheduler interruption.

This repair changes future classification behavior. It does not rewrite or
rerun the saved Phase 6S fit artifact.

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

Write a Phase 6S convergence ledger that compares the Phase 5 rank-4 artifact
against the repaired Phase 6S rank-5 artifact. The expected decision is a
reviewed rank-convergence blocker unless a material validation error is found.

Do not proceed to Phase 7 correctness/HMC/production claims from this result.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-fit-result-2026-06-25.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6S adaptive rank-5 fit result safely record the approved run, correctly distinguish the raw blocked JSON status from the classifier-repaired mechanical admissibility, preserve that rank convergence is not established because rank-5 holdout residual is much worse than rank 4, avoid production/HMC/source-faithful TT-cross claims, and hand off safely to a convergence ledger rather than Phase 7? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed the note records the approved run and exact artifact/command.
- Claude agreed it separates raw blocked artifact status from
  classifier-repaired mechanical admissibility.
- Claude agreed rank convergence is not established because rank 5 is
  materially worse than rank 4.
- Claude agreed no production, HMC, or source-faithful TT-cross claim leaks.
- Claude agreed the handoff is to a convergence ledger, not Phase 7.

Verdict:

```text
VERDICT: AGREE
```
