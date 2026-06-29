# P86 Phase 6W Result: Same-Policy Rank And Degree Convergence

Date: 2026-06-26

Status: `P86_PHASE6W_RANK_CONVERGENCE_PASSED_DEGREE_BLOCKED_REVIEWED`

## Current Decision

The four approved Phase 6W same-policy rank-4 candidate fits completed
mechanically. All used the training-base optimizer, kept the audit cloud
reserved, avoided the historical ALS route, serialized trained cores, and
stayed within the approved runtime/memory envelope.

Rank convergence passes under the reviewed same-policy holdout-stability rule.
Degree convergence remains blocked pending a reviewed configurable-basis
execution path.

Selection result:

```text
selected Phase 6W rank-4 candidate: l1_weight=0.0 zero-L1 comparator
best observed rank-4 holdout arm:   l1_weight=3e-9
positive-L1 margin status:          not cleared
rank-stability status:              passed
degree-convergence status:          blocked
```

The best positive-L1 rank-4 arm, `l1_weight=3e-9`, improved over the rank-4
zero-L1 comparator by `0.003753457322467067`, below the reviewed deterministic
margin of `0.005`. Under the reviewed Phase 6W rule, the rank-4 zero-L1
comparator is therefore selected as the lower rung.

The selected rank-4 zero-L1 holdout residual is `0.0389400359426049`. The
reviewed Phase 6V selected rank-5 zero-L1 holdout residual is
`0.04130816233046943`. The absolute delta is `0.0023681263878645293`, below
the rank-stability threshold `0.005`, so same-policy adjacent rank convergence
passes.

This does not revoke L1 tuning as the Zhao-Cui default procedure. It also does
not open Phase 7 by itself because degree convergence is still blocked.

Ledger artifact:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-ledger-2026-06-26.json`

## Decision Table

| Field | Status |
|---|---|
| Decision | Rank convergence passes; degree convergence remains blocked. |
| Primary criterion status | Rank passed: all Phase 6W rank-4 arms completed, rank-4 selected zero-L1 by the reviewed margin rule, Phase 6V rank-5 reuse was validated by the no-fit preflight, and adjacent holdout stability passed. Degree did not pass because no reviewed configurable-basis execution path has run. |
| Veto diagnostic status | Passed for rank: no fallback route, no audit tuning, no ALS revival, finite residuals/normalizers, runtime/memory within envelope, serialized cores, and no Phase 7/production/HMC/source-faithful TT-cross claim. Degree gate remains a blocker. |
| Main uncertainty | Degree convergence is unresolved; the current evidence establishes same-policy adjacent rank stability only for this fixed rank-4/rank-5 L1-tuning procedure and CPU-hidden runtime posture. |
| Next justified action | Review this Phase 6W result. If agreed, either plan a reviewed configurable-basis/degree convergence path or keep Phase 7 blocked until the owner explicitly reframes the degree gate. |
| What is not being concluded | No degree convergence, no Phase 7 correctness bridge, no posterior correctness, no KR closure, no HMC readiness, no LEDH comparison, no GPU performance, no d50/d100 scale, no production readiness, and no source-faithful author TT-cross training claim. |

## Rank-4 Candidate Table

| Arm | Holdout residual | Improvement over zero-L1 | Margin pass | Selection role |
|---|---:|---:|---|---|
| `l1=0.0` | `0.0389400359426049` | `N/A` | `N/A` | Selected by margin rule |
| `l1=3e-10` | `0.0388761810154267` | `0.00006385492717819795` | No | Rejected by margin |
| `l1=1e-9` | `0.03811385374150144` | `0.0008261822011034617` | No | Rejected by margin |
| `l1=3e-9` | `0.03518657862013783` | `0.003753457322467067` | No | Best observed, rejected by margin |

Positive-L1 margin:

```text
max(0.005, 0.05 * 0.0389400359426049) = 0.005
```

## Rank-Stability Table

| Field | Value |
|---|---:|
| Selected rank-4 holdout | `0.0389400359426049` |
| Selected rank-5 holdout | `0.04130816233046943` |
| Absolute delta | `0.0023681263878645293` |
| Stability threshold | `0.005` |
| Rank-stability decision | Pass |

Stability rule:

```text
abs(rank5_selected_holdout - rank4_selected_holdout)
  <= max(0.005, 0.05 * rank4_selected_holdout)
```

## Run Manifest

| Field | Value |
|---|---|
| Runtime posture | CPU-only/GPU-hidden non-production fits |
| GPU status | `CUDA_VISIBLE_DEVICES=-1`; TensorFlow CUDA/cuInit startup noise is not GPU evidence |
| Target route | Author SIR `Lagrangep(4,8)` plus `AlgebraicMapping(1)` setup surface |
| Target dimension | `36` |
| Rank | `4` |
| Parameters | `18216` |
| Training samples | `364320` |
| Holdout samples | `65536` |
| Audit samples | `65536`, reserved and not used for tuning |
| Optimizer | training-base Adam |
| Learning rate | `0.0003` |
| Scheduler | validation check every `16`, plateau patience `4`, LR factor `0.5`, stop after `4` LR drops |
| L2 / logZ | `1e-8` / `0.0` |
| Seeds | train `8301/8401`, holdout `9301/9401`, audit `9311/9501` |
| Approval request | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-approval-request-2026-06-25.md` |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-subplan-2026-06-25.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-result-2026-06-26.md` |

## Local Checks

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-ledger-2026-06-26.json
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-ledger-2026-06-26.json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-result-2026-06-26.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-degree-convergence-handoff-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase7-correctness-bridge-subplan-2026-06-24.md docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md
```

Results:

```text
py_compile passed
37 passed, 2 warnings
json.tool passed
git diff --check passed
```

## Boundary Notes

- `DEFAULT_L1_WEIGHT` remains `0.0`.
- `l1_weight=0.0` remains an allowed comparator arm inside the default
  Zhao-Cui L1 tuning procedure.
- L1 tuning remains the default Zhao-Cui training-base procedure.
- The selected zero-L1 arms are procedure-local selections, not universal
  scalar defaults.
- Audit data were not used for tuning.
- ALS training remains historical, buggy/stale, and not revived.
- Phase 7 remains blocked while degree convergence is unresolved unless the
  owner explicitly reframes the gate.

## Next Handoff

Claude has reviewed this Phase 6W result. Next, either:

- create a dedicated configurable-basis/degree convergence subplan before any
  degree runtime command; or
- keep Phase 7 as a blocker/deferral path until the owner explicitly reframes
  the unresolved degree gate.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-result-2026-06-26.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6W result correctly record the approved same-policy rank-4 fit execution, apply the reviewed L1 margin rule so rank-4 zero-L1 is selected despite l1=3e-9 having best observed holdout, compare the selected rank-4 and reviewed Phase 6V selected rank-5 under the predeclared adjacent-rank stability rule, preserve that rank convergence passes but degree convergence remains blocked, avoid Phase-7/production/HMC/source-faithful TT-cross claim leakage, and hand off safely? End with VERDICT: AGREE or VERDICT: REVISE.
```

Claude response:

```text
Yes - it records the approved same-policy rank-4 execution, applies the margin
rule to select zero-L1 over the better observed l1=3e-9 arm, compares rank-4
vs Phase 6V rank-5 under the stated stability rule, keeps rank convergence
passed / degree blocked, and avoids the listed claim leakage.

VERDICT: AGREE
```
