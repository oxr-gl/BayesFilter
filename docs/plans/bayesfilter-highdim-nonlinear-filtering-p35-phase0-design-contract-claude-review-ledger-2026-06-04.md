# P35 Phase 0 Zhao--Cui Highdim Design Contract Claude Review Ledger

metadata_date: 2026-06-04

phase: Phase 0 design contract and non-public skeleton

review_scope:
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/diagnostics.py`
- `bayesfilter/highdim/fixed_branch.py`
- `bayesfilter/highdim/validation.py`
- `tests/highdim/test_phase0_contracts.py`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-result-2026-06-04.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports," Foundations of Computational Mathematics, 2022.

what_is_not_concluded:
- Claude review does not certify mathematical correctness beyond Phase 0
  contracts.
- This ledger does not approve Phase 1.
- This ledger does not approve public API exposure.
- This ledger does not approve adaptive Zhao--Cui derivatives.

## Review Rules

Codex is supervisor and final authority.  Claude Code is a bounded hostile
reviewer.  For each finding, Codex classifies:

```text
ACCEPT
PARTIAL
DISPUTE
CLARIFY
```

Accepted or partially accepted findings require patches.  Disputed findings
require concise rebuttals.  If unresolved blockers remain after five
iterations, Phase 0 acceptance is blocked.

## Iteration 1

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase0-impl-review-iter1 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `FAIL`.

Codex classification summary:

```text
ACCEPT: 1
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| MAJOR | Result ledger claimed `INVALID_SHAPE` failure-exit coverage, but tests did not exercise `assert_shape`. | ACCEPT | Added `test_assert_shape_rejects_rank_mismatch` to `tests/highdim/test_phase0_contracts.py`; reran CPU-only Phase 0 validation with `CUDA_VISIBLE_DEVICES=-1`, now `14 passed, 2 warnings in 3.76s`; updated result ledger fixture coverage and test outcome. |

No disputed findings remain after iteration 1.

## Iteration 2

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase0-impl-review-iter2 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `FAIL_ON_DOCUMENTATION_CLOSURE`.

Codex classification summary:

```text
ACCEPT: 2
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| MAJOR | Phase 0 result ledger omitted the serious-run run manifest required by project governance. | ACCEPT | Added `run_manifest` with git commit, exact commands, conda environment, CPU-only status, data version, random seeds, wall time, output artifact paths, plan file, hardening addendum, and result file. |
| MINOR | Review and result ledgers still said pending. | ACCEPT | Updated Phase 0 result decision to `PASS`; closing this review ledger after final narrow confirmation. |

## Iteration 3

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase0-impl-review-iter3 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `PASS`.

Codex classification summary:

```text
ACCEPT: 0
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| NONE | Claude found no remaining blocker or major issue. | N/A | No patch required. |

## Final Status

Final Claude status: `PASS`.

Open blockers: `NONE`.

Final Codex supervisor decision: `ACCEPT_PHASE0`.
