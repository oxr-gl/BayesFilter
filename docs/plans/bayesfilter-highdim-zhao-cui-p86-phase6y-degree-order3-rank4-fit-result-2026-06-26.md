# P86 Phase 6Y Result: Order-3 Degree Comparator Fit

Date: 2026-06-26

Status: `P86_PHASE6Y_DEGREE_ORDER3_RANK4_FIT_COMPLETED_REVIEWED`

## Current Decision

The exact frozen Phase 6Y CPU-hidden order-3/rank-4 degree-comparator fit
command executed and wrote:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json`

The fit artifact status is:

```text
P86_PHASE6Y_DEGREE_ORDER3_RANK4_CANDIDATE_TRAINING_BASE_COMPLETED
```

The candidate is the non-default `Lagrangep(3,8)` setup comparator, classified
as `extension_or_invention`. The reviewed default-order reference remains the
Phase 6W selected `Lagrangep(4,8)` rank-4 zero-L1 artifact.

Mechanically, the fit passed: finite residuals and normalizers, no fallback
route, no audit tuning, no ALS revival, runtime/memory within envelope,
training-base optimizer, and serialized trained cores.

Numerically, the order-3 comparator final holdout residual is lower than the
default-order reference:

```text
reference Lagrangep(4,8) holdout: 0.0389400359426049
candidate Lagrangep(3,8) holdout: 0.026216776647946836
absolute improvement:             0.012723259294658066
candidate/reference ratio:         0.6732602067083007
```

This is favorable degree-comparator evidence, and bounded Claude review agreed
the note is boundary-safe. It is not by itself a production, HMC,
posterior-correctness, KR, LEDH, scale, or source-faithful author TT-cross
claim, and it does not establish degree convergence or Phase 7 readiness.

## Exact Command Executed

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-2026-06-26.json --target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 --training-sample-count 276000 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8303 --train-process-seed 8403 --holdout-prior-seed 9303 --holdout-process-seed 9403 --audit-prior-seed 9313 --audit-process-seed 9503 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json
```

## Decision Table

| Field | Status |
|---|---|
| Decision | Order-3/rank-4 degree-comparator fit completed mechanically and passed bounded Claude review; it gives favorable holdout evidence versus the reviewed default-order reference. |
| Primary criterion status | Passed for fit execution and boundary-safe review: exact command/path, basis setup, sample budget, scheduler, seeds, serialization, finite diagnostics, runtime/memory envelope, no audit tuning, and the reviewed comparator boundary all match the frozen preflight. |
| Veto diagnostic status | Passed mechanically and in review: no fallback route, no ALS revival, finite fit/holdout residuals, finite normalizers, active trainable component, trained cores serialized, runtime/memory within envelope. Interpretation veto remains: no standalone degree-convergence or Phase 7 claim. |
| Main uncertainty | The candidate final holdout is lower than the reference, but best validation was at step `16` and the saved final artifact stopped at step `272` after four LR drops. This is still favorable versus the reference, but it should be reviewed as degree evidence rather than silently promoted. |
| Next justified action | Refresh the degree convergence handoff/evaluation with the reviewed comparator evidence; keep Phase 7 blocked until the broader gate is explicitly reopened. |
| What is not being concluded | No posterior correctness, KR closure, HMC readiness, LEDH comparison, GPU performance, d50/d100 scale, production readiness, or source-faithful author TT-cross training claim. |

## Evidence Contract Check

| Field | Result |
|---|---|
| Question | Can the reviewed configurable-basis runner execute the frozen lower-degree `Lagrangep(3,8)` rank-4 comparator and produce replayable evidence against the Phase 6W selected default-order `Lagrangep(4,8)` rank-4 reference? |
| Baseline/comparator | Reference: `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-0-fit-2026-06-25.json`; candidate: `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json`. |
| Primary criterion | Passed for the executed fit and bounded review: exact frozen command, finite diagnostics, serialized cores, audit cloud reserved, candidate holdout below the default-order reference, and boundary-safe comparator framing. |
| Veto diagnostics | No command drift, nonfinite diagnostic, fallback route, audit tuning, ALS training, runtime breach, memory breach, or unsupported claim was observed. |
| Explanatory diagnostics | Candidate/reference residuals, scheduler events, best/final validation behavior, normalizers, runtime, memory, and parameter/sample budget. |
| Not concluded | This result does not prove posterior correctness or production readiness, and the non-default basis remains classified as `extension_or_invention`. |
| Artifact | Fit JSON, this result, refreshed degree handoff, visible execution ledger, and Claude review ledger. |

## Comparator Table

| Field | Default-order reference | Order-3 candidate |
|---|---:|---:|
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-0-fit-2026-06-25.json` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json` |
| Basis | `Lagrangep(4,8)` | `Lagrangep(3,8)` |
| Classification | source-faithful author default | `extension_or_invention` |
| Basis dimension | `33` | `25` |
| Rank | `4` | `4` |
| Parameters | `18216` | `13800` |
| Training samples | `364320` | `276000` |
| Fit residual | `0.03945179703997934` | `0.02642824660809709` |
| Holdout residual | `0.0389400359426049` | `0.026216776647946836` |
| Normalizer | N/A in this result note | `4.554027196172014e-06` |
| Runtime seconds | N/A in this result note | `206.15538929699687` |
| Peak memory MiB | N/A in this result note | `1836.1484375` |

## Training Diagnostics

The adaptive scheduler stopped the candidate after plateau/LR-drop exhaustion:

```text
completed train steps: 272
requested train steps: 512
stop reason: early_stop_after_plateau_lr_drop_limit
LR drops: 4
final learning rate: 1.875e-05
best validation holdout: 0.021793931728010047 at step 16
final holdout residual: 0.026216776647946836 at step 272
serialized cores: 36
serialized values: 13800
```

The best validation point was earlier than the final saved artifact, so this
result should be interpreted with that validation-shape caveat. The final
artifact nevertheless remains favorable against the default-order reference.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Runtime posture | CPU-only/GPU-hidden non-production fit |
| GPU status | `CUDA_VISIBLE_DEVICES=-1`; TensorFlow CUDA/cuInit startup noise is not GPU evidence |
| Python | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` recorded in fit JSON |
| Target route | Zhao-Cui SIR Austria d18 fixed source route, setup-static Lagrangep basis comparator |
| Candidate basis | `Lagrangep(3,8)`, `extension_or_invention` |
| Reference basis | `Lagrangep(4,8)`, source-faithful author default |
| Target dimension / rank | `36` / `4` |
| Parameters / training samples | `13800` / `276000` |
| Holdout samples | `65536` |
| Audit samples | `65536`, reserved and not used for tuning |
| Optimizer | training-base Adam |
| Learning rate | `0.0003` |
| Scheduler | validation check every `16`, plateau patience `4`, LR factor `0.5`, stop after `4` LR drops |
| L1 / L2 / logZ | `0.0` / `1e-8` / `0.0` |
| Seeds | run `8608`, train `8303/8403`, holdout `9303/9403`, audit `9313/9503` |
| Runtime/memory envelope | `7200` seconds, `12288` MiB |
| Actual runtime/peak memory | `206.15538929699687` seconds, `1836.1484375` MiB |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-subplan-2026-06-26.md` |
| Preflight | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-2026-06-26.json` |
| Fit JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-fit-result-2026-06-26.md` |

## Local Checks

Commands:

```text
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-fit-result-2026-06-26.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-degree-convergence-handoff-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md
```

Results:

```text
json.tool passed
git diff --check passed
```

## Boundary Notes

- The order-3 candidate is classified as `extension_or_invention`, not a
  source-faithful author-default route.
- The reference `Lagrangep(4,8)` route remains the source-faithful author
  default.
- L1 tuning remains the Zhao-Cui training-base default procedure.
- The zero-L1 arm here is a comparator arm, not a global scalar default.
- Audit data were not used for fitting or tuning.
- ALS training remains historical, buggy/stale, and not revived.
- Phase 7 remains blocked until the broader same-policy rank/degree gate is
  satisfied or the owner reframes the gate.

## Next Handoff

Claude agreed. Refresh the degree convergence handoff/evaluation so the
runbook carries forward the reviewed comparator evidence without widening it
into Phase 7 readiness.

## Claude Review Status

`VERDICT: AGREE`
