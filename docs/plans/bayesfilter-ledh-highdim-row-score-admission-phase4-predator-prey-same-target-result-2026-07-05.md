# Phase 4 Result: Predator-Prey Same-Target Adapter And Score

Date: 2026-07-06

Status: `BLOCK_PHASE4_PREDATOR_PREY_CURRENT_LEDH_BRIDGE_UNREVIEWED`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Do not admit the predator-prey LEDH value or score row yet. The repo does contain predator-prey LEDH code surfaces, but the remaining blocker is that none of them is yet reviewed and admitted as the current same-target GPU/XLA leaderboard route. |
| Primary criterion status | Passed by precise blocker: the row target is clear, the old "no code exists" story is false, and the remaining gap is now narrowed to an unreviewed bridge from existing predator-prey LEDH surfaces to the current admitted leaderboard lane. |
| Veto diagnostic status | Passed: no legacy callback existence was promoted to row admission, no diagnostic-only V2/autodiff evidence was promoted as current leaderboard evidence, and no score was admitted before value admission. |
| Main uncertainty | Whether the current admitted predator-prey LEDH lane should be bridged from the existing P8d callback/V2 contract surfaces, or whether a fresh GPU/XLA TF32 row-specific adapter should replace them explicitly. |
| Next justified action | Advance to Phase 5 with the clarified rule preserved: legacy or diagnostic LEDH surfaces are not enough for row admission without a reviewed current-route bridge. |
| What is not concluded | No admitted predator-prey LEDH value row, no admitted predator-prey LEDH score row, no no-tape score evidence, no GPU/XLA TF32 production admission, and no HMC readiness claim. |

## Question Answered

Phase 4 asked:

- Can the predator-prey T20 row be executed as a current same-target LEDH
  scalar with a no-tape total derivative, rather than as legacy or diagnostic
  evidence?

Answer:

- Not yet.

The important refinement is:

- the repo does contain predator-prey LEDH code paths;
- but the reviewed leaderboard artifacts still classify them as legacy or
  diagnostic only;
- and the runbook still lacks a reviewed bridge proving that one of those paths
  is the current same-target GPU/XLA TF32 leaderboard route.

So the correct Phase 4 close is:

- not `missing because no predator-prey code exists`;
- not `already admitted because a callback exists`;
- instead: `blocked because the current-route bridge is still unreviewed`.

## Evidence

Current row target is clear:

- The source-scope contract defines
  `zhao_cui_predator_prey_T20` as the source-scope additive-Gaussian
  predator-prey T20 row with horizon `20`, initial state `[50.0, 5.0]`,
  process covariance `4 * I_2`, observation covariance `4 * I_2`, and physical
  truth `(r, K, a, s, u, v) = (0.6, 114.0, 25.0, 0.3, 0.5, 0.5)`:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`

Current LEDH row-admission baseline still blocks the row:

- The July 3 LEDH row ledger keeps this row at
  `blocked_no_reviewed_current_gpu_xla_ledh_row_adapter` and says the only
  current adapter evidence is that
  `_dpf_predator_prey_callbacks` exists in the old numeric runner:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json`
- The July 3 LEDH closeout keeps the same row blocked with the same plain
  meaning:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md`
- The July 5 `N=10000` LEDH score/memory suite still treats predator-prey as
  blocked for exactly the same reason:
  `docs/plans/ledh-score-memory-test-suite-result-2026-07-05.md`

What the old numeric runner actually contains:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py` does define
  `_dpf_predator_prey_callbacks(...)` and `_dpf_route(...)` does include
  `PREDATOR_PREY_ROW`.
- That route uses
  `highdim.p30_predator_prey_fixture_model()`,
  direct state observation,
  direct Gaussian observation density,
  and calls `run_ledh_pfpf_alg1_ukf_tf(...)` with the raw T20 observations.
- So Phase 4 can now say plainly that a predator-prey LEDH callback route
  exists in the repo.

Why that still does not close the blocker:

- The July 3 row ledger already classifies that P8d callback surface as
  `legacy DPF callback route` evidence only, not as reviewed current
  leaderboard admission evidence.
- The current runbook baseline explicitly says:
  do not rely on legacy callback existence alone.

What the newer V2 surfaces say:

- `experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_ot_contracts_tf.py`
  names a predator-prey route with:
  - direct noisy-state observation;
  - target transition density
    `highdim.PredatorPreySSM.transition_log_density(...)`;
  - observation density
    `highdim.PredatorPreySSM.observation_log_density(...)`;
  - `value_phase_readiness = READY_FOR_P6`.
- `experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_alg1_ukf_values_tf.py`
  and
  `experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_ot_values_tf.py`
  also contain predator-prey Algorithm 1 / LEDH value surfaces.

Why those newer surfaces still do not close the blocker:

- The June 10 V2 gradient report classifies `predator_prey_rk4` as
  `RERUN_ALG1_DIAGNOSTIC_ONLY` with
  `diagnostic_finite_difference_only_no_exact_gradient_oracle`:
  `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-alg1-ukf-gradients-2026-06-10.md`
- The June 10 rerun closeout likewise keeps predator-prey under
  `RERUN_ALG1_DIAGNOSTIC_ONLY`:
  `experiments/dpf_implementation/reports/dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-closeout-2026-06-10.md`
- So Phase 4 cannot honestly promote the V2 surfaces as already admitted
  current leaderboard evidence. They remain diagnostic or replacement-context
  surfaces, not a reviewed row-admission bridge.

Score status is still blocked after value:

- No no-tape predator-prey LEDH score route is admitted anywhere in the current
  highdim leaderboard stack.
- Available predator-prey gradient evidence in the LEDH lane is diagnostic only
  and not a promotion gate.

## Plain Scientific Classification

Predator-prey is not blocked because the row target is unclear.

Predator-prey is not blocked because no LEDH code exists.

Predator-prey is blocked because:

1. the row target is clear;
2. the repo contains predator-prey LEDH callback/contract surfaces;
3. the currently reviewed leaderboard artifacts still classify those surfaces as
   legacy or diagnostic only;
4. no reviewed bridge yet proves that one of those surfaces is the current
   same-target GPU/XLA TF32 leaderboard route.

Therefore:

- current predator-prey LEDH row admission: blocked;
- reason: current-route bridge unreviewed;
- not because the repo is missing predator-prey LEDH code entirely.

## Required Checks Run

```bash
rg -n "predator_prey|blocked_no_reviewed_current_gpu_xla_ledh_row_adapter|blocked_target_alignment|same-target|diagnostic-only" docs/plans docs/benchmarks bayesfilter tests
```

Result: passed; the row contract, blocker ledger, score-memory blocker, and
diagnostic-only policy language were all located.

```bash
git diff --check -- docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase4-predator-prey-same-target-result-2026-07-05.md docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase5-generalized-sv-same-target-subplan-2026-07-05.md docs/plans/bayesfilter-ledh-highdim-row-score-admission-visible-execution-ledger-2026-07-05.md docs/reviews/ledh-highdim-row-score-admission-phase4-review-bundle-2026-07-06.md
```

Result: pending until this phase close patch is complete, then rerun.

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Answered directly: predator-prey LEDH code surfaces exist, but no reviewed bridge yet admits one as the current same-target GPU/XLA leaderboard route. |
| Baseline/comparator | Passed: row contract, July 3 row ledger/closeout, July 5 score-memory blocker, P8d callback trace, V2 contract/value surfaces, and June 10 diagnostic-only reports agree with this narrower classification. |
| Primary criterion | Passed by blocker: the blocker is now exact and no longer falsely states that the repo lacks predator-prey code. |
| Veto diagnostics | Passed: no legacy or diagnostic-only surface was promoted as admitted leaderboard evidence. |
| Explanatory diagnostics | The P8d callback trace and V2 contract surfaces remain useful bridge material for a later adapter-admission phase, but they are not admission evidence yet. |
| Not concluded | No predator-prey LEDH promotion and no score repair yet. |

## Next-Phase Handoff

Phase 5 should proceed with this preserved boundary:

- generalized SV remains its own target-admission problem;
- existence of a callback or diagnostic surface is not enough for row
  admission;
- if a candidate route is the wrong scalar, say so directly;
- if a candidate route may be right but the bridge is unreviewed, say that
  directly too.
