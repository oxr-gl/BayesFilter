# LEDH Forward Scalar Per-Model Master Program

Date: 2026-07-07

Status: `DRAFT_LAUNCH_GATE`

Source amendment:

- `docs/plans/bayesfilter-ledh-same-target-forward-scalar-per-model-amendment-plan-2026-07-06.md`

## Objective

Repair the LEDH high-dimensional leaderboard value layer by admitting the
same-target forward scalar one model row at a time. This program is
forward-scalar-only. It must not implement, admit, or promote scores.

The target scalar is the row observed-data log likelihood estimator:

```text
observed_data_log_likelihood_estimator
```

The reported tensor field is:

```text
log_likelihood
```

The LEDH correction identity is:

```text
transition_log_density
+ observation_log_density
- pre_flow_log_density
+ forward_log_det
```

Metadata, callback existence, runtime, memory, finite output, or proposal/flow
objectives are not admission evidence.

## Inherited State

The previous same-target forward/score program closed with only two LEDH rows
value-admitted:

- `benchmark_lgssm_exact_oracle_m3_T50`;
- `zhao_cui_spatial_sir_austria_j9_T20`.

The following rows remain blocked for LEDH value and score admission:

- `zhao_cui_predator_prey_T20`;
- `zhao_cui_sv_actual_nongaussian_T1000`;
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`;
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`.

The prior planning error was bundling all model forward-scalar admission work
into one broad phase. This program repairs that by giving every model row its
own phase and by making scalar admission a hard prerequisite for any later
score work.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can each intended high-dimensional LEDH row produce an executable same-target observed-data log likelihood estimator artifact? |
| Baseline/comparator | July 6 Phase 3 admitted/blocked result, the July 6 per-model amendment plan, current forward contract metadata, row datasets, and row-specific reference checks where available. |
| Primary pass criterion | A row is value-admitted only when a validated executable artifact reports finite `log_likelihood` values from the row target correction, at the required row scale for admission. |
| Veto diagnostics | Metadata-only admission; callback-only admission; proposal/flow objective used as likelihood; wrong row target; actual-SV/KSC artifact borrowing; score implementation before scalar admission; runtime/memory/finite output promoted as correctness. |
| Explanatory diagnostics | Runtime, compile time, memory, ESS, Monte Carlo standard error, tiny-prefix checks, old blocked evidence, and non-LEDH references. |
| Not concluded | Score correctness, score admission, HMC readiness, posterior correctness, scientific superiority, and fair runtime ranking. |
| Artifacts | Master program, visible runbook, execution ledger, stop handoff, phase subplans, phase results, review bundles, local check logs, and final value leaderboard artifacts. |

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Phase 0 must restate exactly which rows are already admitted and blocked from the July 6 result. |
| Proxy metrics | Runtime, memory, compile, and finite output are explanatory unless target identity also passes. |
| Missing stop conditions | Every phase has row-specific stop conditions and cannot promote on ambiguity. |
| Unfair comparison | References are diagnostic unless they compare the same frozen row target. |
| Hidden assumptions | Each model phase freezes observations, theta, target density, and flow policy before execution. |
| Stale context | Phase 0 rechecks current files and artifacts before implementation begins. |
| Environment mismatch | GPU/CUDA/XLA commands require trusted execution; CPU-only checks must declare device hiding. |
| Useless artifacts | A phase result must answer whether a row has executable same-target scalar evidence, not merely whether code ran. |

Launch audit status: passed for creating the gated launch package. Phase 0 must
repeat a focused audit before execution.

## Phase Index

| Phase | Name | Purpose | Subplan | Required result artifact |
| --- | --- | --- | --- | --- |
| 0 | Baseline and admission guard | Freeze admitted/blocked baseline and enforce metadata-vs-execution distinction. | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase0-baseline-guard-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase0-baseline-guard-result-2026-07-07.md` |
| 1 | Shared runner schema | Standardize executable forward-scalar artifact schema and validator. | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase1-runner-schema-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase1-runner-schema-result-2026-07-07.md` |
| 2 | LGSSM | Reconfirm the exact linear-Gaussian golden row under the shared schema. | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase2-lgssm-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase2-lgssm-result-2026-07-07.md` |
| 3 | Fixed SIR | Reconfirm amended fixed SIR with `sir_log_scale_theta`. | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-result-2026-07-07.md` |
| 4 | Predator-prey | Build/admit additive-Gaussian predator-prey scalar. | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-result-2026-07-07.md` |
| 5 | Actual SV | Build/admit raw-target, log-square-flow actual SV scalar. | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-result-2026-07-07.md` |
| 6 | Generalized SV | Build/admit raw-target, log-square-flow generalized SV scalar. | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase6-generalized-sv-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase6-generalized-sv-result-2026-07-07.md` |
| 7 | KSC SV | Build/admit KSC finite-mixture surrogate scalar with a KSC-specific LEDH route. | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase7-ksc-sv-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase7-ksc-sv-result-2026-07-07.md` |
| 8 | Value integration | Rebuild LEDH value leaderboard from admitted scalar artifacts only. | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase8-integration-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase8-integration-result-2026-07-07.md` |

## Phase Discipline

Each phase must have a dedicated subplan before execution. Each subplan must
state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each phase:

1. run required local checks;
2. write a phase result or blocker result;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Review Policy

Claude may be used as read-only reviewer for material subplans, phase results,
and repair decisions. Claude has no edit, execution, approval, policy,
scientific-claim, funding, product-capability, model-file, or boundary
authority. Codex remains supervisor and executor.

Review bundles must be bounded and fixed-path. Do not send the whole repo to
Claude. If Claude does not respond, run a tiny probe. If the probe succeeds,
narrow or rewrite the prompt and retry. If Claude is unavailable or
policy-blocked, replace Claude review with a fresh Codex read-only review.

Loop Claude review only for material issues, stopping after five rounds for
the same blocker.

## Human Approval Boundaries

Stop for human approval before:

- changing a row target definition;
- changing pass/fail criteria after seeing results;
- using package/network/data fetches;
- destructive git or filesystem actions;
- crossing model-file, funding, product-capability, public-release, or
  scientific-claim boundaries.

Trusted GPU/CUDA/XLA runs and bounded Claude read-only reviews have standing
approval from the user in this thread.

## Nonclaims

- This master program does not admit any new row.
- This master program does not implement or admit any score.
- This master program does not establish HMC readiness, posterior correctness,
  runtime ranking, or scientific superiority.
