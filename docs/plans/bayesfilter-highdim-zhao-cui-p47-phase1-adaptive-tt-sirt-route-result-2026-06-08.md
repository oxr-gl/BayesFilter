# P47-M1 Result: Adaptive TT-Cross/SIRT Route Label

metadata_date: 2026-06-08
phase: P47-M1
status: `PASS_P47_M1_ADAPTIVE_ROUTE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | P47 adopts `documented-deviation fixed-design substitute` as the M1 route label. |
| Primary criterion status | Local M1 gates passed; Claude read-only review passed at Iteration 2. |
| Veto diagnostic status | No adaptive MATLAB TT-cross/SIRT reproduction claim is emitted; P46 is used only as bounded fixed-design multistate adapter evidence. |
| Main uncertainty | Later phases must preserve the documented-deviation wording in every promoted row. |
| Next justified action | Proceed to P47-M2 paper-scale readiness. |
| Not concluded | No adaptive TT-cross/SIRT reproduction, no paper-scale Zhao--Cui reproduction, no filtering correctness, no HMC readiness. |

## Evidence Contract

Question: which source-governed Zhao--Cui route label may downstream P47
phases use?

Baseline/comparator:

- P46 bounded multistate fixed-design TT adapter result.
- P47-M0 registry and tests.

Primary promotion criterion:

- The registry carries a single M1 route decision.
- Every P47 row carries the conservative route label.
- The route-label row forbids adaptive MATLAB TT-cross/SIRT reproduction.

Outcome:

- Selected label: `documented-deviation fixed-design substitute`.
- Source evidence: P46 passed bounded multistate fixed-design TT adapter
  governance, but explicitly did not claim adaptive TT-cross/SIRT reproduction.

## Artifacts

- Registry:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json`
- Focused tests:
  `tests/highdim/test_p47_adaptive_route.py`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase1-adaptive-tt-sirt-route-claude-review-ledger-2026-06-08.md`

## Local Evidence

| Command | Result |
| --- | --- |
| `python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json` | passed |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_adaptive_route.py` | 9 passed |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_adaptive_route.py` | passed |
| `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_adaptive_route.py docs/plans/bayesfilter-highdim-zhao-cui-p47-*2026-06-08.md` | passed |

## Gate Markers

p47_m1_route_label: `documented-deviation fixed-design substitute`
p47_m1_local_evidence_run: `COMPLETE`
p47_m1_evidence_audit: `COMPLETE`
p47_m1_result_note_substance: `COMPLETE`
p47_m1_claude_review: `PASS_P47_M1_ADAPTIVE_ROUTE`
p47_m1_long_run_used: `false`
