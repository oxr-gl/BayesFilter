# P35 Phase 3 Zhao--Cui Highdim Fixed-Branch Fitting Claude Review Ledger

metadata_date: 2026-06-04

phase: Phase 3 fixed-branch fitting

review_scope:
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/diagnostics.py`
- `bayesfilter/highdim/fitting.py`
- `tests/highdim/test_fixed_branch_fit.py`
- `tests/highdim/test_failure_exits.py`
- `tests/highdim/test_phase0_contracts.py`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-result-2026-06-04.md`

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`

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
iterations, Phase 3 acceptance is blocked.

## Pre-Review Local Validation

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py
```

Outcome: `16 passed, 2 warnings in 3.58s`.

After pre-review self-hardening added explicit manifest-field and coupled
coordinate/sweep-order diagnostics, focused outcome:
`18 passed, 2 warnings in 3.76s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py
```

Outcome: `65 passed, 2 warnings in 6.24s`.

After pre-review self-hardening, authoritative Phase 0--3 outcome:
`67 passed, 2 warnings in 5.79s`.

```bash
git diff --check -- bayesfilter/highdim/__init__.py bayesfilter/highdim/diagnostics.py bayesfilter/highdim/fitting.py bayesfilter/highdim/fixed_branch.py bayesfilter/highdim/validation.py bayesfilter/highdim/bases.py bayesfilter/highdim/tt.py bayesfilter/highdim/squared_tt.py bayesfilter/highdim/transport.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-result-2026-06-04.md
```

Outcome: `PASS`.

Backend/source scan:

```bash
rg -n "import numpy|from numpy|import jax|from jax|import torch|from torch|matlab|octave|tensor-ssm-paper-demo|zhao_cui_tensor_ssm_p10" bayesfilter/highdim tests/highdim
```

Outcome: clean except the intentional no-NumPy assertion strings in
`tests/highdim/test_phase0_contracts.py`.

## Iteration 1

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase3-impl-review-iter1 \
  --model sonnet \
  --effort high \
  "<broad hostile review prompt>"
```

Claude verdict: `TOOL_STALLED`.

Codex classification summary:

```text
ACCEPT: 0
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| TOOL | Broad iteration-1 review remained live and silent beyond the practical review window. | N/A | Terminated only the named stalled Claude worker with `pkill -f highdim-zhao-cui-phase3-impl-review-iter1`; running a narrower iteration-1b review. |

Pre-iteration-1b self-hardening:
- Added explicit branch-manifest field coverage test.
- Added coupled trivariate coordinate/sweep-order diagnostic test.
- Cleaned invalid-shape gate termination diagnostics so they are not mislabeled
  as a complexity gate.

## Iteration 1b

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase3-impl-review-iter1b \
  --model sonnet \
  --effort high \
  "<narrow review prompt>"
```

Claude verdict: `TOOL_STALLED`.

Codex classification summary:

```text
ACCEPT: 0
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| TOOL | Narrow iteration-1b review remained live and silent beyond the practical review window. | N/A | Terminated only the named stalled Claude worker with `pkill -f highdim-zhao-cui-phase3-impl-review-iter1b`; running a minimal iteration-1c review. |

## Iteration 1c

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase3-impl-review-iter1c \
  --model sonnet \
  --effort medium \
  "<minimal review prompt>"
```

Claude verdict: `FAIL`.

Codex classification summary:

```text
ACCEPT: 2
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| MAJOR | `tests/highdim/test_fixed_branch_fit.py` lacked direct complexity-gate coverage in the fixed-fit test file. | ACCEPT | Added `test_fixed_fit_complexity_gate_is_covered_in_fit_file`, asserting `COMPLEXITY_GATE` and matching stop condition. |
| MAJOR | `tests/highdim/test_fixed_branch_fit.py` lacked direct condition-number-veto coverage in the fixed-fit test file. | ACCEPT | Added `test_fixed_fit_condition_number_veto_is_covered_in_fit_file`, asserting `CONDITION_NUMBER_VETO` and matching stop condition. |

Post-patch validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py
```

Outcome: `20 passed, 2 warnings in 3.45s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py
```

Outcome: `69 passed, 2 warnings in 5.87s`.

## Iteration 2

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase3-impl-review-iter2 \
  --model sonnet \
  --effort medium \
  "<closure review prompt>"
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
| NONE | Claude found the two prior findings resolved and no new blocker/major issue in the touched closure scope. | N/A | No patch required. |

## Final Status

Final Claude status: `PASS`.

Open blockers: `NONE`.

Final Codex supervisor decision: `ACCEPT_PHASE3`.
