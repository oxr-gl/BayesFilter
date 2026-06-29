# P86 Phase 6V Result: L1 Selection And Convergence Reentry

Date: 2026-06-25

Status: `P86_PHASE6V_L1_SELECTION_CONVERGENCE_REVIEWED`

## Current Decision

Phase 6V fitting execution completed after exact human approval of the three
new CPU-hidden candidate commands. The reviewed Phase 6T `l1_weight=1e-9`
artifact was reused as the fourth arm after manifest/protocol equivalence.

All four rank-5 arms completed mechanically, used the training-base optimizer,
kept the audit cloud reserved, avoided the historical ALS route, serialized
trained cores, and stayed within the approved runtime/memory envelope.

Selection result:

```text
selected Phase 6V candidate: l1_weight=0.0 zero-L1 comparator
best observed holdout arm:   l1_weight=3e-9
positive-L1 margin status:   not cleared
```

The best positive-L1 arm, `l1_weight=3e-9`, improved over the zero-L1
comparator by `0.00171902146079247`, below the reviewed deterministic margin
of `0.005`. Under the reviewed Phase 6V rule, the zero-L1 comparator is
therefore selected as the Phase 6V candidate.

This does not revoke L1 tuning as the Zhao-Cui default procedure. It means this
reviewed Phase 6V grid did not earn a positive-L1 scalar selection by the
predeclared margin. Phase 7 remains blocked until a later reviewed same-policy
rank/degree convergence gate passes or is explicitly reframed with owner
approval.

Ledger artifact:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-ledger-2026-06-25.json`

## Decision Table

| Field | Status |
|---|---|
| Decision | Select the `l1_weight=0.0` comparator as the Phase 6V candidate under the reviewed tie policy. |
| Primary criterion status | Passed for Phase 6V selection: all arms completed, the selected arm is finite and below the holdout threshold `0.11045495200924742`, and no veto fired. |
| Veto diagnostic status | Passed: no fallback route, no audit tuning, no ALS revival, finite residuals/normalizers, runtime/memory within envelope, selected final/best validation ratio below `2x`, and no Phase 7/production/HMC claim. |
| Main uncertainty | Phase 6V selects a rank-5 candidate but does not establish same-policy rank convergence; a same-policy rank-4 lower rung must still be generated or otherwise justified in Phase 6W. |
| Next justified action | Draft/review Phase 6W same-policy rank/degree convergence reentry. |
| What is not being concluded | No rank convergence, no degree convergence, no posterior correctness, no KR closure, no HMC readiness, no LEDH comparison, no GPU performance, no d50/d100 scale, no production readiness, and no source-faithful author TT-cross training claim. |

## Candidate Table

| Arm | Source | Holdout residual | Improvement over zero-L1 | Margin pass | Selection role |
|---|---|---:|---:|---|---|
| `l1=0.0` | New Phase 6V fit | `0.04130816233046943` | `N/A` | `N/A` | Selected by tie policy |
| `l1=3e-10` | New Phase 6V fit | `0.04196951154098494` | `-0.0006613492105155095` | No | Rejected |
| `l1=1e-9` | Reviewed Phase 6T reuse | `0.03973471699747935` | `0.0015734453329900808` | No | Rejected by margin |
| `l1=3e-9` | New Phase 6V fit | `0.03958914086967696` | `0.00171902146079247` | No | Best observed, rejected by margin |

Margin:

```text
max(0.005, 0.05 * 0.04130816233046943) = 0.005
```

## Evidence Contract Check

| Field | Result |
|---|---|
| Question | Under the reviewed Zhao-Cui L1-tuning default procedure, is rank-5 training stable enough to reopen Phase 6 rank/degree convergence work? |
| Baseline/comparator | Reviewed Phase 6S rank-5 failure, reviewed Phase 6T `l1_weight=1e-9` diagnostic, and new same-LR rank-5 arms at `l1=0.0`, `3e-10`, and `3e-9`. |
| Primary criterion | Passed for Phase 6V candidate selection: the selected zero-L1 comparator has holdout `0.04130816233046943`, below `0.11045495200924742`, with finite diagnostics and no veto. |
| Veto diagnostics | Passed for Phase 6V: exact approved commands used for new arms; reuse arm validated by protocol equivalence; no audit tuning; no fallback route; no runtime/memory breach; no unsupported claim. |
| Explanatory diagnostics | All arms stopped via the adaptive plateau LR-drop limit at 272 completed train steps. Best validation was at step 16 for all arms, and final holdout worsened but stayed below the selected-arm `2x` veto threshold. |
| Not concluded | Phase 6V does not establish rank convergence because no same-policy rank-4 lower rung has been compared to the selected rank-5 candidate. |
| Artifact | Phase 6V ledger JSON, four fit artifacts, this result, execution ledger, and Claude review ledger. |

## Run Manifest

| Field | Value |
|---|---|
| Runtime posture | CPU-only/GPU-hidden non-production fits |
| GPU status | `CUDA_VISIBLE_DEVICES=-1`; TensorFlow CUDA/cuInit startup noise is not GPU evidence |
| Target route | Author SIR `Lagrangep(4,8)` plus `AlgebraicMapping(1)` setup surface |
| Target dimension | `36` |
| Rank | `5` |
| Parameters | `28380` |
| Training samples | `567600` |
| Holdout samples | `65536` |
| Audit samples | `65536`, reserved and not used for tuning |
| Optimizer | training-base Adam |
| Learning rate | `0.0003` |
| Scheduler | validation check every `16`, plateau patience `4`, LR factor `0.5`, stop after `4` LR drops |
| L2 / logZ | `1e-8` / `0.0` |
| Seeds | train `8301/8401`, holdout `9301/9401`, audit `9311/9501` |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-subplan-2026-06-25.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-result-2026-06-25.md` |

## Local Checks

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-ledger-2026-06-25.json
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-ledger-2026-06-25.json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-result-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-subplan-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md
```

Results:

```text
py_compile passed
31 passed, 2 warnings
json.tool passed
git diff --check passed
```

## Boundary Notes

- `DEFAULT_L1_WEIGHT` remains `0.0`.
- `l1_weight=0.0` remains an allowed comparator arm inside the default
  Zhao-Cui L1 tuning procedure.
- L1 tuning remains the default Zhao-Cui training-base procedure.
- The selected zero-L1 arm is a Phase 6V candidate, not a universal scalar
  default.
- Audit data were not used for tuning.
- ALS training remains historical, buggy/stale, and not revived.
- Phase 7 remains blocked.

## Next Handoff

Draft/review:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-subplan-2026-06-25.md`

Phase 6W should reopen rank/degree convergence only by same-policy evidence. In
particular, the existing Phase 5 rank-4 artifact is historical context but is
not a same-policy lower rung for the Phase 6V selected rank-5 candidate because
the optimizer schedule and L1-selection procedure differ.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-result-2026-06-25.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6V result correctly record the approved L1-selection fit execution, reuse the reviewed Phase 6T l1_weight=1e-9 artifact by protocol equivalence, apply the reviewed deterministic margin rule so zero-L1 is selected despite l1=3e-9 having the best observed holdout, preserve that L1 tuning remains the Zhao-Cui default procedure and DEFAULT_L1_WEIGHT remains 0.0, avoid Phase-7/rank-convergence/production/HMC/source-faithful TT-cross claim leakage, and hand off safely to Phase 6W same-policy rank/degree reentry? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed the approved Phase 6V execution is recorded correctly.
- Claude agreed the deterministic margin rule is applied correctly: `l1=3e-9`
  has the best observed holdout but does not clear the `0.005` margin over
  zero-L1, so zero-L1 is selected.
- Claude agreed the Zhao-Cui default-procedure boundary is preserved:
  `DEFAULT_L1_WEIGHT` remains `0.0`, and L1 tuning remains the default
  procedure.
- Claude agreed rank-convergence, Phase-7, production, HMC, and
  source-faithful TT-cross claim leakage is avoided.
- Claude agreed the Phase 6W same-policy rank/degree handoff is safe.
- Claude noted a non-blocking wording nuance: the phrase "tie policy" could be
  more precisely called a deterministic margin rule, but the substantive rule
  is stated correctly.

Verdict:

```text
VERDICT: AGREE
```
