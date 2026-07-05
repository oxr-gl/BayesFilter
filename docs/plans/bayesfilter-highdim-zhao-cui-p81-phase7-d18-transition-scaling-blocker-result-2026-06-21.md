# P81 Phase 7 Result: d=18 Transition Scaling Blocker Audit

status: PHASE7_AUDIT_RECOMMENDS_PHASE8_STREAMED_ALL_PAIRS_PROTOTYPE_REVIEW_PENDING
date: 2026-06-21
supervisor_executor: Codex
readonly_reviewer: Claude Opus

## Skeptical Audit Before Execution

Pass.  Phase 7 executed only read-only local source/document searches and
source inspection.  It did not run LEDH/P8p diagnostics, SIR d=18 diagnostics,
TensorFlow tests, GPU/CUDA commands, package installs, network fetches,
detached agents, default changes, or destructive filesystem/git actions.

The audit question was narrow: identify whether the Phase 6 d=18 all-grid
transition blocker can be handled by a bounded route before any comparator
phase.  The answer is: peak memory can be bounded by streaming, but total
transition work remains enormous; therefore Phase 8 may only be a bounded
streaming prototype/smoke, not LEDH comparison or production readiness.

## Decision Table

| Field | Status |
|---|---|
| Decision | Recommend `PHASE8_STREAMED_ALL_PAIRS_IMPLEMENTATION` as a bounded prototype only, with strict runtime/memory caps and fail-fast guards. |
| Primary criterion | Passed: identified a concrete bounded peak-memory route and a test plan, while preserving the blocker for unbounded all-pairs materialization. |
| Veto diagnostic status | No veto triggered in Phase 7.  LEDH/P8p was not run and the complexity gate remains required. |
| Main uncertainty | Streaming controls peak memory but does not reduce the `O(N_current N_previous d)` transition-evaluation count; d=18 degree-0 two-row may still be too slow for a useful smoke. |
| Next justified action | Draft/review Phase 8 for a streaming logsumexp derivative prototype, with tiny d=2 parity first and an optional d=18 smoke only under a timeout/budget. |
| Not concluded | No d=18 full-history score correctness, no LEDH/P8p agreement, no HMC readiness, no posterior/scientific validity, no source-faithfulness, no scaling/default readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` |
| Worktree status | Dirty; includes P81 edits plus unrelated/non-P81 modified and untracked files already present in the workspace. |
| Commands | Phase 7 `rg` audit checks; targeted `sed` reads of `filtering.py`, `models.py`, and P51 preflight tests. |
| Environment | Local shell in `/home/chakwong/BayesFilter`. |
| CPU/GPU status | N/A: no framework execution or GPU/CUDA command in Phase 7. |
| Random seeds | N/A: read-only audit only. |
| Output artifact paths | This result; Phase 8 subplan; updated P81 runbook/ledgers/handoff. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase7-d18-transition-scaling-blocker-subplan-2026-06-21.md` |
| Reviewer status | Phase 7 subplan was patched per Claude execution-review guardrails; Phase 7 result/Phase 8 review pending. |

## Audit Findings

Current code:

- `_multistate_grid_predictive_log_density_from_retained(...)` materializes
  `transition_log` for all current-reference grid points against all previous
  retained grid points, then applies `tf.reduce_logsumexp(..., axis=1)`.
- `_multistate_grid_predictive_log_density_and_derivative_from_retained(...)`
  materializes both transition log density and transition derivative matrices.
- `_check_pairwise_transition_tensor_budget(...)` now blocks unchunked
  allocation using
  `current_count * previous_count * state_dim * sizeof(float64)`.

Prior project evidence:

- P51 already identified the current route as
  `P46/P47 all-axes multistate retained-grid fixed-design TT route`.
- P51 already recorded the missing component as
  `streamed_or_factorized_transition_application`.
- P51 required avoiding materializing all `grid_points^2` transition pairs.

## Quantitative Route Table

For the degree-0 d=18 smoke, the reference tensor grid has
`N_current = N_previous = 2^18 = 262144` points.

| Route | Peak bytes estimate | Chunk size | Chunk count | Asymptotic runtime | Guard preserved | Phase 8 suitability |
|---|---:|---:|---:|---|---|---|
| Unchunked all-pairs | `262144 * 262144 * 18 * 8` = about 9.9 TB just for tiled point tensors; transition/log matrices add more. | N/A | 1 | `O(N^2 d)` | Yes, current `COMPLEXITY_GATE` | Must remain blocked. |
| Chunk current only | `current_chunk * 262144 * 18 * 8`; with `current_chunk=64`, about 2.4 GB just for point tensors. | 64 current rows | 4096 | `O(N^2 d)` | Needs per-chunk guard | Still too memory-heavy unless chunk is tiny. |
| Chunk previous only with streaming logsumexp | `262144 * previous_chunk * 18 * 8`; with `previous_chunk=16`, about 604 MB just for point tensors. | 16 previous rows | 16384 | `O(N^2 d)` | Needs per-chunk guard | Maybe CPU/GPU feasible only as a carefully timed prototype, not default. |
| Double chunk with streaming accumulators | `current_chunk * previous_chunk * 18 * 8`; with `current_chunk=512`, `previous_chunk=64`, about 4.7 MB for point tensors plus transition arrays. | 512 x 64 | 512 * 4096 chunk products | `O(N^2 d)` | Yes, explicit per-chunk formula | Best bounded prototype route, but total work remains huge. |
| Reduced retained grid smoke | Peak and total work drop with retained order; e.g. a deliberately smaller retained grid changes the branch. | TBD | TBD | Reduced | Needs separate branch contract | Useful only as engineering smoke, not same candidate evidence. |
| Factorized/analytic transition application | Potentially avoids `N^2`; would exploit Gaussian transition structure or TT contraction. | TBD | TBD | Potentially subquadratic | Needs new derivation/tests | Likely required for serious d=18 full-history evidence. |

## Recommended Phase 8 Direction

Proceed with `PHASE8_STREAMED_ALL_PAIRS_IMPLEMENTATION` only as a bounded
prototype:

- implement streaming value and derivative logsumexp helpers that do not
  materialize full all-pairs tensors;
- preserve the current unbounded-route `COMPLEXITY_GATE`;
- test exact parity against dense all-pairs on the tiny d=2 fixture;
- keep the tiny d=2 two-row finite-difference regression passing;
- define a d=18 smoke as optional and budget-vetoed by timeout/chunk count;
- if d=18 smoke remains too slow, close with
  `BLOCK_REPRESENTATION_CHANGE_REQUIRED` rather than comparing to LEDH/P8p.

The most plausible streaming recurrence for each current block is:

1. maintain per-current `m = max(log_terms)` and `s = sum(exp(log_terms - m))`;
2. for each previous block, update `m`/`s` with stable logsumexp;
3. for derivative, also maintain
   `q = sum(exp(log_terms - m) * dot_log_terms)` under the same rescaling;
4. return `log_predictive = m + log(s)` and `dot_predictive = q / s`.

This preserves the target but not the total computational cost.

## Phase 8 Readiness Test Plan

Required tests for Phase 8:

- unbounded d=18 all-grid route still fails fast with `COMPLEXITY_GATE`;
- tiny d=2 dense-vs-streaming transition predictive log density parity;
- tiny d=2 dense-vs-streaming transition predictive derivative parity;
- tiny d=2 two-observation multistate score finite-difference regression still
  passes;
- any d=18 two-row smoke must use chunk budgets and must not materialize all
  current-previous pairs.

## Next Handoff

Review and then execute Phase 8 only if the subplan converges:
`docs/plans/bayesfilter-highdim-zhao-cui-p81-phase8-streamed-transition-prototype-subplan-2026-06-21.md`.

No LEDH/P8p comparison is justified yet.
