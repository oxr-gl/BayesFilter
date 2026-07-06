# LEDH Same-Target Forward Scalar And Score Master Program

Date: 2026-07-06

Status: `COMPLETE_PHASE6_LEDGER_REBUILT_WITH_TWO_ADMITTED_LEDHD_ROWS`

## Program Objective

Build the missing LEDH high-dimensional scores by first constructing and
admitting the correct same-target forward scalar for each model row.

The forward scalar is the row observed-data log likelihood

```text
log p_theta(y_1:T)
```

or the finite-`N`, fixed-randomness LEDH particle estimator of that exact
quantity. LEDH flow, transport, surrogate observations, linearizations, and
proposal diagnostics may affect the proposal mechanism, but the scalar whose
value and score enter the leaderboard must be the row likelihood estimator.

No LEDH score work may begin for a row until that row's same-target forward
scalar is admitted.

## Core Scientific Invariant

For each row:

1. the row target and free parameter vector must be frozen before code changes;
2. the executed LEDH value must be the row likelihood estimator, not a proposal
   objective;
3. the score must be the derivative of exactly that executed scalar;
4. no `GradientTape`, `ForwardAccumulator`, or hidden autodiff may be used as
   admitted leaderboard score evidence;
5. memory, runtime, compilation, finite values, or callback existence cannot
   replace same-target value or score evidence.

If the executed scalar is not the row likelihood estimator, the row is `wrong
relative to the stated target` and must not be scored or promoted.

## Inherited State

The previous row-score admission runbook closed as a blocker triage:

- admitted no-tape score-route evidence:
  - `benchmark_lgssm_exact_oracle_m3_T50`, compact LGSSM score;
  - `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`, scoped SIR
    component score;
- no additional full highdim LEDH score row was admitted;
- fixed spatial SIR, actual SV, KSC SV, predator-prey, and generalized SV
  remain blocked for full LEDH score admission at launch. By explicit human
  amendment on 2026-07-06, fixed spatial SIR is no longer blocked merely
  because of `no_free_theta`; it has the `sir_log_scale_theta` model-parameter
  surface and must pass the same-target value and no-tape score gates.

This program is a construction program, not another inventory run.

## Row Repair Targets

| Row | Target scalar | Free theta policy | Initial status |
| --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | LGSSM observed-data likelihood estimator | existing LGSSM theta | value and compact score evidence exists; keep as reference lane |
| `zhao_cui_spatial_sir_austria_j9_T20` | source-formula SIR observed-data likelihood estimator with free model log scales | `sir_log_scale_theta`, theta = `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`, truth theta `[0,0,0]` | full-row score blocked until same-target value and no-tape score gates pass |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | legacy/scoped component target only | three log-scale parameters | scoped diagnostic evidence only; not full observed-data evidence |
| `zhao_cui_sv_actual_nongaussian_T1000` | exact declared actual-SV row likelihood, raw or transformed as frozen in Phase 1 | declared actual-SV theta | same-target bridge missing |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | exact KSC finite-mixture surrogate likelihood | declared KSC theta | LEDH adapter missing |
| `zhao_cui_predator_prey_T20` | exact additive-Gaussian predator-prey state-space likelihood | declared predator-prey theta | current-route bridge unreviewed |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | exact frozen generalized-SV source-row likelihood | declared generalized-SV theta | source-row bridge unreviewed |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter build all LEDH highdim model scores by admitting the same-target forward log-likelihood scalar first and the no-tape score second? |
| Baseline/comparator | July 3 LEDH-inclusive leaderboard artifacts, July 5 score-memory suite, the prior row-score admission closeout, row target contracts, and current LEDH implementation surfaces. |
| Primary pass criterion | Every promoted row has a row-specific admitted same-target likelihood estimator, a no-tape score of that exact scalar, tiny correctness evidence, `N=10000` correctness/memory evidence, and integration evidence that value and score use the same algorithm. |
| Veto diagnostics | Score implementation before value admission; proposal scalar treated as likelihood; scoped SIR treated as fixed full-row SIR; callback existence treated as row admission; autodiff score promoted; memory/runtime success promoted as correctness; leaderboard rebuild before row gates pass. |
| Explanatory diagnostics | Compile time, GPU memory, runtime, callback traces, finite-difference diagnostics, and historical blocked evidence. |
| Not concluded at launch | No new row is admitted at launch. No HMC readiness, posterior correctness, or scientific superiority claim is made. |
| Artifacts | Master program, phase subplans, visible runbook, execution ledger, stop handoff, review bundles, phase results, implementation diffs, test results, and final leaderboard artifacts. |

## Skeptical Plan Audit

| Risk checked | Control |
| --- | --- |
| Wrong baseline | Program starts from the July 3/July 5 LEDH artifacts and the completed blocker-triage runbook. |
| Proxy metric promoted | Runtime, memory, compile, callback existence, and finite outputs are explanatory only. |
| Score before scalar | Phase order makes same-target forward scalar admission a hard prerequisite for score work. |
| Surrogate confusion | The plan separates proposal/flow observations from target likelihood correction in every adapter. |
| Scoped SIR confusion | Fixed SIR now has `sir_log_scale_theta`; the legacy parameterized scoped row is not full observed-data evidence. |
| Hidden assumption | Phase 1 must freeze row target and theta before Phase 2 can edit shared APIs. |
| Environment mismatch | GPU/CUDA/XLA and Claude commands require trusted execution. CPU-only checks must state GPU hiding. |
| Useless artifacts | Each phase has a result artifact that must answer one narrow construction or admission question. |

Audit status: passed for launch planning only. Execution begins with Phase 0
after local checks and read-only review.

## Program Order

| Phase | Name | Purpose | Subplan | Required result artifact |
| --- | --- | --- | --- | --- |
| 0 | Launch and invariant freeze | Freeze the corrected construction plan and prevent another inventory-only run. | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase0-launch-invariant-freeze-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase0-launch-invariant-freeze-result-2026-07-06.md` |
| 1 | Row target and theta freeze | Freeze each row likelihood target, free theta, allowed transforms, and nonempty-score status. | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-result-2026-07-06.md` |
| 2 | Common forward likelihood API | Build or standardize adapter interfaces that separate proposal surfaces from target likelihood densities. | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-result-2026-07-06.md` |
| 3 | Model forward scalar admission | Admit same-target finite-`N` LEDH likelihood estimators model by model. | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-model-forward-admission-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-model-forward-admission-result-2026-07-06.md` |
| 4 | Manual no-tape score implementation | Implement analytical/manual total-VJP scores only for rows admitted in Phase 3. | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase4-manual-score-implementation-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase4-manual-score-implementation-result-2026-07-06.md` |
| 5 | Per-model score and memory tests | Add one correctness/memory score test per model and run tiny then `N=10000` gates. | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase5-per-model-score-tests-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase5-per-model-score-tests-result-2026-07-06.md` |
| 6 | Integration and leaderboard rebuild | Add all-model integration tests and rebuild the leaderboard only with rows that passed row gates. | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase6-integration-leaderboard-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase6-integration-leaderboard-result-2026-07-06.md` |

## Phase Invariants

- Every phase must state the claimed target and computed quantity separately.
- Any mismatch must be called `wrong relative to the stated target`.
- Any unsupported bridge must be called `unsupported` or `not checked`.
- The word `surrogate` must identify a proposal mechanism only, unless the row
  target itself is explicitly a surrogate likelihood such as KSC.
- No score phase may open for a row lacking a Phase 3 same-target value pass.
- No leaderboard rebuild may occur before Phase 5 tests pass for admitted rows.

## Review Protocol

Claude is a read-only reviewer only. If Claude review stalls or returns no
verdict:

1. run a tiny probe;
2. if the probe passes, narrow or rewrite the review bundle and retry;
3. if the probe fails in trusted execution, replace that review with a fresh
   Codex read-only review packet;
4. do not treat silence, timeout, or fallback agreement as proof.

Stop after five review rounds for the same blocker.

## Anticipated Approval Boundaries

Already approved by the user in this thread:

- trusted GPU/CUDA/XLA TensorFlow runs, including `N=10000`;
- trusted long-running benchmark/test commands that touch XLA/GPU;
- bounded Claude read-only review commands for `/home/chakwong/BayesFilter`;
- sending bounded BayesFilter repo artifacts to Claude for read-only review.

Still human-required before execution:

- changing pass/fail criteria after seeing results;
- installing packages or fetching network data;
- destructive git or filesystem actions;
- changing the fixed SIR row into a new full observed-data parameterized row
  without an explicit row-contract decision;
- publishing claims beyond the reviewed artifacts.
