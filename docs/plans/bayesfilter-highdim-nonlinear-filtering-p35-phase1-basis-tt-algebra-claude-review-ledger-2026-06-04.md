# P35 Phase 1 Zhao--Cui Highdim Basis And TT Algebra Claude Review Ledger

metadata_date: 2026-06-04

phase: Phase 1 basis, mass, and TT algebra

review_scope:
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/bases.py`
- `bayesfilter/highdim/tt.py`
- `tests/highdim/test_bases.py`
- `tests/highdim/test_tt_algebra.py`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-result-2026-06-04.md`

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`

what_is_not_concluded:
- Claude review does not certify mathematical correctness beyond Phase 1
  contracts.
- This ledger does not approve Phase 2.
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
iterations, Phase 1 acceptance is blocked.

## Iteration 1

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase1-impl-review-iter1 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `FAIL`.

Codex classification summary:

```text
ACCEPT: 5
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| BLOCKER | Complexity gate was not enforced on actual dense-materializing Phase 1 paths: `FunctionalTT.evaluate()`, `integrate_all()`, and `contract_axes()` could allocate without a budget. | ACCEPT | Added a declared `complexity_budget` to `FunctionalTT`; dense paths now validate either the supplied budget or the TT's declared budget before work and raise `COMPLEXITY_GATE` on failure. Added `test_evaluate_and_contraction_enforce_complexity_budget_before_work`. |
| MAJOR | `FunctionalTT` could be constructed with a measure convention that disagreed with its `ProductBasis`. | ACCEPT | Added construction-time equality check between `measure_convention` and `product_basis.convention`. Added `test_functional_tt_rejects_product_basis_measure_mismatch`. |
| MAJOR | `contract_axes()` returned the source TT's branch identity rather than an identity for the contracted object. | ACCEPT | Added `TTContractedRepresentation.manifest_payload()` and `manifest()`; `contract_axes()` now hashes kept axes, integrated axes, retained cores, scalar value if applicable, diagnostics, and measure convention. Added `test_contracted_branch_identity_hashes_contracted_payload`. |
| MAJOR | Full-axis contraction fabricated a synthetic `[1,1,1]` retained core despite `kept_axes == ()`. | ACCEPT | Added explicit scalar contracted representation via `scalar_value`; full contraction now returns `cores == ()` and `diagnostics["representation"] == "scalar"`. Added `test_full_axis_contraction_records_scalar_without_fake_core`. |
| MINOR | Basis objects/manifests did not carry every field stated in the Phase 1 subplan. | ACCEPT | Added `LegendreBasis1D.dtype` and `reference_measure` properties and included basis dtype and reference-measure family in the TT manifest payload. |

Post-patch local validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_tt_algebra.py tests/highdim/test_bases.py
```

Outcome: `19 passed, 2 warnings in 3.05s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py
```

Outcome: `33 passed, 2 warnings in 3.55s`.

No disputed findings remain after iteration 1.

## Iteration 2

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase1-impl-review-iter2 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `FAIL`.

Codex classification summary:

```text
ACCEPT: 4
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| MAJOR | `TTContractedRepresentation.manifest_payload()` omitted retained basis semantics, allowing the same retained cores on different retained domains to hash identically. | ACCEPT | Added `retained_bases` to `TTContractedRepresentation`; `contract_axes()` now records retained basis family, domain, dtype, reference-measure family, degree, and normalization in the contracted manifest. Added `test_contracted_branch_hash_changes_with_retained_basis_domain`. |
| MAJOR | The contraction complexity estimate did not account for retained-rank growth in `contract_axes()`, so a budget could pass before allocating a much larger retained core. | ACCEPT | Added `_estimated_axis_contraction_elements()` that simulates the pending-rank flow used by `contract_axes()` and gates against that estimate. Added `test_contract_axes_complexity_accounts_for_retained_rank_growth`. |
| MAJOR | Durable artifacts still recorded placeholder Phase 1 closure state. | ACCEPT | Kept final status pending until a passing re-review, but updated result and review ledgers with iteration-2 failure, accepted findings, patches, and post-patch validation evidence. |
| MINOR | Regression suite did not pin the two remaining holes. | ACCEPT | Added the retained-basis hash-sensitivity and retained-rank-growth complexity tests listed above. |

Post-patch local validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_tt_algebra.py tests/highdim/test_bases.py
```

Outcome: `21 passed, 2 warnings in 5.73s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py
```

Outcome: `35 passed, 2 warnings in 3.29s`.

No disputed findings remain after iteration 2.

## Iteration 3

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase1-impl-review-iter3 \
  --model sonnet \
  --effort high \
  "<prompt>"
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
| TOOL | Broad iteration-3 review process remained live and silent for more than 20 minutes. | N/A | Terminated only the stalled Claude process with `pkill -f highdim-zhao-cui-phase1-impl-review-iter3`; reran a narrower iteration-3b review focused on iteration-2 fixes and closure. |

## Iteration 3b

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase1-impl-review-iter3b \
  --model sonnet \
  --effort high \
  "<narrow prompt>"
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
| NONE | Claude found no remaining blocker or major issue in the requested Phase 1 closure scope. | N/A | No patch required. |

Claude PASS evidence:
- Contracted manifest includes retained basis metadata before hashing.
- `contract_axes()` gates retained-rank growth before retained-core allocation.
- Full-axis contraction remains scalar with `cores == ()`.
- `FunctionalTT` rejects product-basis/TT measure-convention mismatch.
- Dense Phase 1 paths are budget-gated before work.
- Regression tests pin the above cases.
- Result and review ledgers accurately record iteration-1/2 failures, accepted
  patches, current local gates, and pending-to-final closure.

## Final Status

Final Claude status: `PASS`.

Open blockers: `NONE`.

Final Codex supervisor decision: `ACCEPT_PHASE1`.
