# P47 Master Program: Remaining Zhao--Cui Filtering Completion

metadata_date: 2026-06-08
phase: P47
status: `DRAFT_FOR_CLAUDE_PLAN_REVIEW`

## Scope

P47 handles the remaining Zhao--Cui filtering work after P37/P45/P46:

- adaptive TT-cross/SIRT route candidate or a reviewed clean-room BayesFilter
  substitute with explicit deviation labels;
- paper-scale readiness and later model-specific filtering experiments,
  excluding S&P 500 real-data reproduction by user instruction;
- lower-rung spatial SIR and predator-prey reference/equality gates followed
  by separate production-filtering gates;
- same-target CUT4--Zhao--Cui value and gradient comparisons for generalized
  SV, spatial SIR, and predator-prey;
- stable production score/gradient API and HMC readiness gates.

Out of scope:

- S&P 500 real-data reproduction;
- copying or line-by-line translating MATLAB implementation code;
- weakening P42/P45/P46 target, baseline, tolerance, or nonclaim rules.

## Governing Sources

- P30 model-suite master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`
- P37 integration closeout:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase7-integration-closeout-result-2026-06-05.md`
- P42 likelihood/gradient validation rules:
  `docs/plans/bayesfilter-highdim-zhao-cui-p42-gradient-likelihood-validation-rules-2026-06-07.md`
- P45 comparison closeout:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-overnight-gated-self-recovery-execution-result-2026-06-08.md`
- P46 multistate adapter result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-result-2026-06-08.md`
- P46 resume-governance result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-resume-governance-result-2026-06-08.md`

## Evidence Contract

Question:

- Can BayesFilter complete the remaining Zhao--Cui filtering evidence, excluding
  S&P 500 real-data reproduction, while preserving source governance,
  same-target comparison discipline, and P42 gradient/HMC standards?

Baselines and comparators:

- Zhao--Cui paper equations and audited MATLAB behavior as source/reference
  material only;
- BayesFilter fixed-design TT and P46 multistate adapter as current
  implementation baselines;
- adaptive TT-cross/SIRT clean-room route candidate or explicitly reviewed
  documented-deviation substitute;
- exact Kalman, dense/refined tensor quadrature, or separately reviewed
  model-specific reference routes;
- CUT4 only where the declared target is additive-Gaussian or a reviewed
  transformed/closure target.

Primary promotion criteria:

- every promoted filtering row states target identity, parameterization,
  observation/state law, branch policy, reference route, tolerance, and
  nonclaims;
- adaptive or paper-scale feasibility evidence has resource manifests and lower
  rung guardrails, but production filtering correctness is promoted only by
  explicit production-filtering tokens;
- every promoted Zhao--Cui row carries the M1 route label: `adaptive route
  candidate` or `documented-deviation fixed-design substitute`;
- same-target value and gradient comparisons use the same data, parameters, and
  unconstrained parameterization for CUT4, Zhao--Cui, and reference routes;
- HMC readiness is claimed only after P42 Tier 1 local correctness, Tier 2
  statistical scale, and Tier 3 Hamiltonian/leapfrog diagnostics pass for the
  exact declared target.

Veto diagnostics:

- S&P 500 real-data reproduction is reintroduced;
- a diagnostic closure is presented as native-model correctness;
- CUT4 and Zhao--Cui evaluate different likelihood targets;
- gradients are compared in different parameterizations;
- adaptive branch decisions mutate during a fixed-branch score comparison;
- an adaptive route candidate is mislabeled as adaptive reproduction before
  later matched-target filtering evidence and closeout approval;
- generic Zhao--Cui wording hides a documented-deviation fixed-design
  substitute;
- fit residual, finite value, or finite gradient is promoted as correctness;
- paper-scale correctness is claimed from feasibility manifests or tiny value
  fixtures alone;
- MATLAB code structure, helper names, comments, or algorithms are copied
  rather than clean-room rederived.

Explanatory-only diagnostics:

- wall time, memory, point counts, TT ranks, basis sizes, condition numbers, fit
  residuals, holdout residuals, branch hashes, ESS-like summaries, trajectory
  plots, and proposal diagnostics.

What will not be concluded unless a later phase explicitly passes:

- no S&P 500 reproduction;
- no stable public score API;
- no HMC readiness;
- no adaptive MATLAB TT-cross/SIRT reproduction;
- no paper-scale model-suite completion;
- no CUT4--Zhao--Cui equality for generalized SV, spatial SIR, or predator-prey;
- no production-grade spatial SIR or predator-prey filtering unless the
  corresponding production-filtering token passes.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_WITH_STRICT_GATES`.

- Wrong-baseline risk: CUT4 is not ground truth.  P47 requires exact,
  dense/refined, or separately reviewed references before equality promotion.
- Proxy-metric risk: fit residuals and finite gradients may veto or explain,
  but cannot promote filtering correctness or HMC readiness.
- Hidden-assumption risk: P46 retains all axes on tiny tensor grids.  P47 must
  not infer high-dimensional scalability from that adapter.
- Target-mismatch risk: native SV, transformed SV, KSC mixture SV, generalized
  SV, SIR closures, and predator-prey closures are distinct targets.
- Environment risk: GPU or long runs require separate trusted execution plans.
- Scope creep risk: S&P 500 is explicitly excluded even if paper-scale
  synthetic/model-suite filtering is pursued.

## Phase Map

| Phase | Subplan | Purpose | Required pass token |
| --- | --- | --- | --- |
| P47-M0 | `bayesfilter-highdim-zhao-cui-p47-phase0-governance-freeze-subplan-2026-06-08.md` | freeze target registry, claim classes, and S&P 500 exclusion | `PASS_P47_M0_GOVERNANCE` |
| P47-M1 | `bayesfilter-highdim-zhao-cui-p47-phase1-adaptive-tt-sirt-route-subplan-2026-06-08.md` | decide and validate clean-room adaptive route candidate or documented substitute label | `PASS_P47_M1_ADAPTIVE_ROUTE` |
| P47-M2 | `bayesfilter-highdim-zhao-cui-p47-phase2-paper-scale-filtering-subplan-2026-06-08.md` | paper-scale readiness, resource caps, and feasibility manifests excluding S&P 500; no correctness promotion | `PASS_P47_M2_PAPER_SCALE_READINESS` |
| P47-M3 | `bayesfilter-highdim-zhao-cui-p47-phase3-generalized-sv-equality-subplan-2026-06-08.md` | generalized SV same-target CUT4--Zhao--Cui value/gradient gate | `PASS_P47_M3_GENERALIZED_SV_EQUALITY` |
| P47-M4 | `bayesfilter-highdim-zhao-cui-p47-phase4-spatial-sir-filtering-subplan-2026-06-08.md` | spatial SIR lower-rung reference/equality gate, then separate production-filtering gate | `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY` and `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING` |
| P47-M5 | `bayesfilter-highdim-zhao-cui-p47-phase5-predator-prey-filtering-subplan-2026-06-08.md` | predator-prey lower-rung filtering/preconditioning gate, then separate production-filtering gate | `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING` and `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING` |
| P47-M6 | `bayesfilter-highdim-zhao-cui-p47-phase6-score-hmc-readiness-subplan-2026-06-08.md` | stable score/gradient API and HMC readiness gate with per-target evidence-class dependencies | `PASS_P47_M6_SCORE_HMC_READINESS` |
| P47-M7 | `bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-subplan-2026-06-08.md` | claim ledger, documentation alignment, and final nonclaims | `PASS_P47_M7_CLOSEOUT` |

Required order:

```text
M0 -> M1 -> M2 -> M3 -> M4 -> M5 -> M6 -> M7
```

M3--M5 may prepare target notes after M0.  M2 may prepare paper-scale resource
manifests after M1, but may not promote model-specific filtering correctness.
No equality, production filtering, score API, or HMC claim may promote before
M1 and the relevant model-specific reference gate pass.  Production spatial SIR
and predator-prey claims require both M2 readiness and the corresponding
production-filtering token.

## Review And Repair Loop

- Codex remains supervisor and executor.
- Claude is read-only reviewer only.
- Review the master program plus all subplans as a bounded plan packet.
- Loop until convergence or maximum five Claude iterations.
- Accepted Claude blockers must be patched before execution.
- If Claude and Codex do not converge after five iterations, stop with a
  blocker artifact; do not weaken target identity, baseline, tolerance, or
  nonclaim rules.

Review ledger:

`docs/plans/bayesfilter-highdim-zhao-cui-p47-remaining-filtering-completion-claude-review-ledger-2026-06-08.md`

## Planned Execution Policy

This master program creates the plan only.  Execution requires a separate
reviewed gated runbook.  The current executable runbook gate is
`PASS_P47_OVERNIGHT_RUNBOOK`, which supersedes the earlier blocked
`PASS_P47_PLAN_GOVERNANCE` packet by reviewing the repaired master and all
M0--M7 subplans together.

Default checks are CPU-only unless a phase-specific trusted GPU plan is
approved:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim
git diff --check -- bayesfilter/highdim tests/highdim docs/plans
```
