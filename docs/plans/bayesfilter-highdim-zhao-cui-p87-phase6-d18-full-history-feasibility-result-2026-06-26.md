# P87 Phase 6 Result: d18 Full-History Feasibility Gate

Date: 2026-06-27

Status: `P87_PHASE6_D18_FEASIBILITY_SELECTS_SOURCE_ROUTE_RANK_DEGREE_GATE_REVIEWED_CLOSED`

## Decision

Phase 6 selects the source-route rank/degree lane as the only admissible
non-all-pairs SIR d18 full-history lane to carry into Phase 7.

This is a route-feasibility handoff only. It does not establish SIR d18
full-history value correctness, analytical-gradient correctness, source-route
correctness, HMC readiness, production readiness, GPU readiness, LEDH
comparison, training readiness, or default-policy readiness.

Dense all-pairs, streamed all-pairs, and local/operator routes are not selected
as d18 full-history feasibility routes.

## Route Feasibility Table

| Route name | Claim class | Source/provenance anchor | Derivative semantics | Replay identity | Memory bound | Rank/sample contract | Blocker reason | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Current dense multistate retained-grid pairwise route | `blocked_all_pairs` | `bayesfilter/highdim/filtering.py:4205`; `bayesfilter/highdim/filtering.py:4206`; `bayesfilter/highdim/transition_route.py:128` | Pairwise value and score helpers exist, but they are attached to the forbidden all-pairs route. | Dense current-by-previous grid matrix. | Fails `COMPLEXITY_GATE` for d18 scale; pair tensor is quadratic. | None admissible for d18 full history. | Dense all-pairs route materializes/treats every current/previous pair; increasing memory is not a new route. | Not selected. |
| Streamed all-pairs fallback | `blocked_all_pairs` | `bayesfilter/highdim/filtering.py:3502`; `bayesfilter/highdim/filtering.py:3576`; `bayesfilter/highdim/filtering.py:3597`; `bayesfilter/highdim/filtering.py:3649` | Streaming derivative helper exists for tiny parity, but semantics remain all-previous-row summation. | Current chunks by previous chunks with streaming logsumexp over all previous rows. | Chunk budget limits per block, but total route is still quadratic and gated by chunk product. | None admissible for d18 full history. | P81 Phase 9 already records streamed all-pairs as not sufficient for d18 full-history routing. | Not selected. |
| P53 local-neighborhood/operator route | `extension_or_invention` | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase9-representation-scaling-result-2026-06-21.md:50`; `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase9-representation-scaling-result-2026-06-21.md:92`; `bayesfilter/highdim/transition_route.py:496` | Useful for deterministic local/operator diagnostics, but not a source-route analytical-gradient closure. | Local-neighborhood branch metadata. | P81 records P53-M5 d18 memory blocker: `R_eff=2916`, rank-1 forecast `29,386,561,536` bytes, `r_max=0`. | No admissible d18 rank-selection contract yet. | Local/operator lane is extension/invention for source-faithfulness and remains too wide under existing memory/rank policy. | Not selected for P87 d18 full-history feasibility. |
| Fixed-TTSIRT source-route retained-object lane | `fixed_hmc_adaptation` for P87 fixed/replay use; source-route evidence lane, not correctness | `bayesfilter/highdim/source_route.py:8042`; `bayesfilter/highdim/source_route.py:8086`; `bayesfilter/highdim/source_route.py:8180`; `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md:102` | No promoted full-history analytical-gradient claim. The admissible derivative boundary is explicit: Phase 7 may audit source-route rank/degree evidence only; analytical-gradient correctness remains outside this selection. | Retained-object branch identity and sequential fixed-HMC replay carry. | Non-all-pairs sample/transport lane; memory is governed by source-route fit/rank/sample artifacts, not retained-grid pair tensors. | P86 training-base/L1 evidence supplies rank passed and degree-comparator artifacts, with degree still needing Phase 7 audit. | Not a correctness proof; rank/degree evidence must be audited without promoting proxy metrics. | Selected for Phase 7 rank/degree gate only. |

## Evidence Contract Check

| Field | Result |
| --- | --- |
| Question | Is there a feasible non-all-pairs SIR d18 full-history route with derivative semantics and memory/rank contract? |
| Primary criterion status | Met only in the narrow source-route handoff sense: a non-all-pairs source-route lane exists with replay identity and rank/sample artifacts to audit in Phase 7. Full-history analytical-gradient semantics are not promoted. |
| Veto diagnostic status | Dense all-pairs, streamed all-pairs, memory-budget-only all-pairs variants, and local/operator source-faithfulness overclaims are blocked. Proxy metrics are not promoted to correctness. |
| Main uncertainty | Whether P86/P83 artifacts support a same-route rank/degree-stable source-route label remains for Phase 7; correctness and analytical-gradient readiness remain unproven. |
| Next justified action | Execute reviewed Phase 7 as a local artifact audit of source-route rank/degree evidence. |
| What is not concluded | No SIR d18 correctness, no source-route correctness, no full-history analytical-gradient correctness, no HMC/production/GPU/LEDH/training/default readiness. |

## Run/Check Manifest

| Field | Value |
| --- | --- |
| Git commit | `97ad05d` |
| Repository root | `/home/chakwong/BayesFilter` |
| Execution target | Local route audit only |
| CPU/GPU status | No GPU/CUDA command. No TensorFlow numerical command was run for Phase 6. |
| TensorFlow command avoided | Yes; Phase 6 used text/code route audit only. |
| Commands actually run | Required P87 `rg` route inventory, required `COMPLEXITY_GATE`/streaming helper grep, `git diff --check`, narrowed anchor scans over P81/P83/P86/P87 and route files, and targeted `nl -ba ... | sed ...` anchor reads. |
| Broad grep note | The first broad route-inventory grep produced a very large truncated inventory, so Phase 6 used narrower anchor scans for the auditable result table. |
| Reviewed artifacts consulted | P81 Phase 9 result; P83 Phase 7 source-route validation subplan; P86 Phase 6U/6V/6W/6X/6Y results; `filtering.py`; `transition_route.py`; `source_route.py`. |
| Wall time | Short local text/code audit; exact wall time not recorded. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-subplan-2026-06-26.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-result-2026-06-26.md` |

## Checks Run

```bash
rg -n "all-pairs|pairwise|streaming|LocalNeighborhoodScalingRouteConfig|factorized|source-route|retained" bayesfilter/highdim docs/plans tests/highdim -g '*.py' -g '*.md'
```

Result: ran, but output was too broad/truncated for direct result evidence.
Narrowed anchor scans were used for the table above.

```bash
rg -n "COMPLEXITY_GATE|_check_pairwise_transition_tensor_budget_conservative|_multistate_grid_predictive_log_density_from_retained_streaming" bayesfilter/highdim/filtering.py tests/highdim/test_p81_analytical_sir_score.py
```

Result: passed as route inventory evidence. It found the expected d18
`COMPLEXITY_GATE`, streaming fallback, and conservative budget anchors.

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Result: passed before the result/subplan patch.

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py
```

Result: passed after the Phase 6 result and Phase 7 subplan patch.

## Boundary Notes

- `BLOCK_D18_ALL_PAIRS_DRIFT` remains active for dense and streamed all-pairs.
- `BLOCK_PROXY_PROMOTION` remains active: rank/degree, finite execution, fit
  loss, holdout residual, replay identity, and tiny parity do not prove
  correctness.
- `BLOCK_SOURCE_CLAIM_UNGROUNDED` remains active for local/operator routes and
  non-default basis choices.
- The selected source-route lane may support Phase 7 artifact audit only. It is
  not a full-history analytical-gradient route.

## Phase 7 Handoff

Phase 7 may proceed because this result and the refreshed Phase 7 subplan
received read-only review. Phase 7 must remain a local artifact audit of
source-route rank/degree evidence and must not run new fits, GPU commands,
HMC, LEDH, production promotion, or default-policy changes.

The refreshed handoff artifact is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase7-source-route-rank-degree-gate-subplan-2026-06-26.md`
