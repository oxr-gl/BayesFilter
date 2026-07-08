# P81 Phase 11 Result: Memory, Rank, And Compression Policy

status: BLOCK_PHASE11_NEEDS_COMPRESSED_OPERATOR_DERIVATION
date: 2026-06-21

## Phase Objective

Decide the next scientifically honest route for turning the parameterized local
transition tie-out into a computationally meaningful d=18 candidate, or write a
precise blocker if no route can be selected without a new derivation.

Phase 11 was read-only.  It did not run implementation edits, GPU/CUDA,
LEDH-PFPF-OT diagnostics, d=18 full-grid propagation, package installs, network
fetches, detached agents, destructive actions, or default changes.

## Skeptical Plan Audit

The audit blocks direct implementation because the tempting options would
mislead:

- relaxing the memory cap would change the claim class without reducing the
  algorithmic problem;
- tiny parameterized local-route tie-out does not establish d=18 readiness;
- the old P53 local/operator `R_eff` route is explicitly rejected as
  source-faithful rank evidence by P56/P57;
- LEDH-PFPF-OT comparison is not valid until a d=18 candidate full-history
  score route exists under a reviewed memory/runtime contract;
- no implemented TT-MPO/operator-compression route with theta-derivative
  semantics exists in the audited code.

## Read-Only Checks Run

```bash
rg -n "R_eff|rank-1 forecast|rank selection|memory_forecast|step_memory|TT-MPO|operator|compression|local-neighborhood|source-faithful|extension_or_invention" docs/plans bayesfilter/highdim tests/highdim -g '*.md' -g '*.py'
rg -n "rank_ceiling|step_memory_bytes|P53_RANK_SELECTION|LocalNeighborhoodScalingRouteConfig|P53_LOCAL_SCALING_ROUTE_ID|tt_mpo|operator" bayesfilter/highdim tests/highdim -g '*.py'
rg -n "source-route|retained object|TTSIRT|marginal|proposal correction|local/operator|R_eff" docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-result-2026-06-11.md
```

Outcome: the audit confirmed the existing P52/P53/P56/P57 split.  P53 provides
local-route lower-rung tie-out and admission for rank-selection entry, but P53
M5 blocks exact d=18 rank selection.  P56/P57 forbid using the local/operator
`R_eff` route as source-faithful rank evidence.

## Route-Policy Comparison

| Option | Phase 11 decision |
|---|---|
| Exact local route with larger cap | Block.  This is cap relaxation, not a scaling repair.  P53-M5 already shows rank 1 exceeds the 8 GiB step cap. |
| Smaller local approximation | Not selected yet.  It would introduce neighborhood truncation or approximation and needs a derivation, error contract, theta-gradient semantics, and lower-rung tests. |
| TT-MPO/operator compression | Best candidate for the deterministic diagnostic lane, but not implementable directly from current evidence.  A derivation/design phase is required first. |
| Hybrid local plus retained-TT contraction | Plausible, but the audited code has local factor primitives and dense/tiny tie-out, not a retained-TT contraction that avoids enumerating current/previous rows. |
| Source-route retained object | Correct direction for source-faithful claims, but it is a separate fixed TTSIRT/retained-object program with paper/source anchors and cannot be closed by P53 local/operator work. |
| Stop/block | Selected for Phase 11: block implementation and draft a derivation/design phase for compressed deterministic operator or contraction route. |

## Binding Memory And Source Facts

P53-M5 exact local-route blocker remains binding:

```text
R_eff = 2916
basis_order = 3
dimension = 18
candidate_ranks = {1, 2, 4, 8, 16, 32}
step_cap = 8 GiB
rank-1 forecast = 29,386,561,536 bytes
r_max = 0
```

The rank-budget formula in `bayesfilter/highdim/rank_budget.py` is:

```text
M_step = bytes * d * n * (R_eff * r)^2 * omega
```

P56 source audit also remains binding:

- `transition_route.py` and `rank_budget.py` are local/operator
  `extension_or_invention` for source-faithfulness;
- source-faithful SIR validation requires the fixed source-route retained
  object, source-style marginalization/KR/pdf semantics, proposal correction,
  sequential loop, and model parity ledgers;
- old local/operator `R_eff` evidence must not be promoted into source-faithful
  rank evidence.

## Decision Table

| Decision | Primary criterion status | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Block direct Phase 12 implementation; require compressed-route derivation/design | Met as blocker: no route can be implemented honestly without a new derivation/design artifact | Cap-relaxation veto, tiny-tieout-promotion veto, LEDH-jump veto, source-faithful-overclaim veto all avoided | Whether a TT-MPO/operator or hybrid retained-TT contraction can reduce effective rank while preserving theta derivatives | Draft Phase 12 as read-only compressed operator/contraction derivation and lower-rung test design | No d=18 full-history score route, no LEDH comparison, no source-faithfulness, no HMC/posterior/default readiness |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | Dirty worktree; no commit made |
| Commands | Three read-only `rg` audit commands from Phase 11 subplan |
| Environment | Local repo shell |
| CPU/GPU status | No GPU/CUDA command; read-only text audit |
| Data version | N/A |
| Random seeds | N/A |
| Wall time | Short text audit commands |
| Output artifacts | This result file and Phase 12 subplan |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase11-memory-rank-compression-subplan-2026-06-21.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase11-memory-rank-compression-result-2026-06-21.md` |

## Nonclaims

Phase 11 does not establish d=18 full-history likelihood correctness,
compressed-route correctness, LEDH-PFPF-OT agreement, HMC or NUTS readiness,
posterior validity, source-faithfulness, production readiness, or default
readiness.

## Next Handoff

Draft Phase 12 as a read-only compressed operator/contraction derivation phase.
It should decide whether the deterministic diagnostic lane should pursue
TT-MPO/operator compression, hybrid retained-TT contraction, or a precise
blocker.  It must specify:

- the represented transition object;
- exact versus approximate status;
- memory and rank formulas;
- theta-gradient propagation semantics;
- branch/replay identity;
- lower-rung value and theta-gradient tie-out tests;
- source-faithfulness nonclaim or source-anchor requirements.
