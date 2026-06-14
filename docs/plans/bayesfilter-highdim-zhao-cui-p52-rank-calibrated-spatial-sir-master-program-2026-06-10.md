# P52 Master Program: Rank-Calibrated Factorized Zhao-Cui Spatial SIR Route

metadata_date: 2026-06-10
program: P52-rank-calibrated-factorized-spatial-sir
status: PLAN_REVIEW_CONVERGED
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Fix the rank-selection and calibration problem exposed by the P51 spatial SIR
dimension-18 blocker.  P52 replaces the current all-axes retained-grid
production idea with a reviewed path toward a fixed-rank, factorized,
HMC-facing deterministic approximation target.

The program has three required outcomes:

1. update the P30 Zhao-Cui LaTeX companion note with the motivation,
   mathematical detail, and implementation detail for rank selection,
   memory-bounded calibration, UKF scouting, and factorized transition
   application;
2. implement a rank-selection protocol that chooses a fixed rank before HMC
   from memory, smoothness, and calibration evidence rather than by adaptive
   branch decisions inside the likelihood call;
3. run spatial SIR feasibility and calibration ladders for dimensions 18, 50,
   and 100, with explicit limits on which rows may claim filtering evidence.

## Why P52 Exists

P51-M3 showed that the current spatial SIR production route materializes
pairwise transition evaluations over an all-axes retained grid.  For
`sites = 9`, `state_dim = 18`, and `order = 3`,

```text
grid_points = 3^(2*9) = 387420489
pairwise_transition_evaluations = grid_points^2 = 150094635296999121
```

This is a major production-design blocker.  The issue is not fixed design
itself.  Fixed design is desirable for HMC because it defines a deterministic
approximate target.  The issue is the dense all-pairs multistate route, which
destroys high-dimensional scalability.

## Scope

P52 is in scope for:

- fixed-rank deterministic TT or factorized approximation design;
- memory-bounded rank selection and rank-ladder stopping rules;
- UKF or block/local UKF scouting as an optional baseline and design guide;
- spatial SIR dimensions `d = 18`, `d = 50`, and `d = 100`;
- TensorFlow / TensorFlow Probability implementation paths;
- value and gradient evidence where a same-target or calibrated reference is
  available.

P52 is not in scope for:

- adaptive TT/SIRT source-faithful filtering inside HMC;
- rank changes during an HMC likelihood call;
- S&P 500 reproduction;
- claiming production HMC readiness;
- claiming exact spatial SIR posterior correctness from UKF, memory preflight,
  or rank self-convergence alone.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter replace the dense spatial SIR retained-grid route with a memory-bounded fixed-rank calibration protocol that makes high-dimensional Zhao-Cui filtering plausible without overclaiming correctness? |
| Baseline/comparator | P51-M3 route blocker; P50/P51 deterministic route contracts; existing spatial SIR lower-rung dense references; UKF scouting diagnostics; higher-rank fixed deterministic runs when feasible. |
| Primary pass criterion | Every phase has a reviewed subplan, pass/block token, result artifact target, and nonclaim boundary; the master program defines a concrete memory-bounded rank protocol and a dimension policy for d=18/50/100. |
| Veto diagnostics | Dense all-pairs grid retained as production route; UKF treated as truth; rank chosen adaptively inside HMC likelihood; d=50 or d=100 smoke promoted to correctness; memory cap ignored; finite gradients promoted to HMC readiness. |
| Explanatory diagnostics | UKF means/covariances, effective-dimension spectra, rank-ladder self-convergence, memory forecasts, wall time, TensorFlow/XLA placement, gradient finite checks, and lower-rung dense references. |
| Not concluded | This master plan alone does not conclude production spatial SIR readiness, HMC readiness, or correctness at d=50/d=100. |
| Artifacts | P52 master program, phase subplans, Claude review ledger, phase result artifacts, rank protocol manifest, dimension-ladder manifests, tests, and P30 LaTeX patch. |

## Skeptical Plan Audit

Status: REVIEWED_BY_CODEX_PENDING_CLAUDE.

- Wrong-baseline risk: UKF is a scout and sanity baseline, not a promoted
  correctness comparator.  Low-dimensional dense references remain the
  correctness anchor where available.
- Proxy-metric risk: memory feasibility, finite values, finite gradients, and
  rank self-convergence do not imply HMC readiness or exact filtering
  correctness.
- Hidden-assumption risk: TT state storage is usually small; transition
  application and intermediate ranks are the real bottleneck.  The plan must
  model intermediate memory, not just core storage.
- Environment risk: GPU may help after factorization, but P52 begins CPU-only
  unless a trusted GPU plan is created.  CPU-only runs must set
  `CUDA_VISIBLE_DEVICES=-1`.
- Stop-condition risk: if `r <= r_max` cannot stabilize a row, do not keep
  growing rank indefinitely; record either a coordinate/factorization blocker or
  a model-complexity blocker.
- Artifact risk: d=100 is allowed as preflight/scout evidence first, not as an
  automatic filtering run.
- Documentation drift risk: implementation cannot close P52 if it differs from
  the P30 equations, memory model, or pseudocode without a documented P30
  amendment.

## Rank And Memory Policy

Ranks are fixed design parameters of the approximate likelihood.  They may be
calibrated offline, but they must not be adapted inside the HMC likelihood call.

Use a 32 GB practical machine ceiling with explicit reserves:

```text
physical memory cap:       32 GB
algorithm memory cap:      12-16 GB
single-step workspace cap:  4-8 GB
```

The first-order TT state storage estimate is

```text
M_state ~= bytes * d * n * r^2,
```

where `bytes = 8` for float64, `d` is state dimension, `n` is per-coordinate
grid/order, and `r` is the fixed TT rank cap.

The transition application estimate must include operator/intermediate rank:

```text
M_step ~= bytes * d * n * (R_eff * r)^2 * omega,
```

where `R_eff` is the effective transition-operator rank multiplier and `omega`
is the workspace multiplier for contraction, orthogonalization, autodiff, and
temporary tensors.

The protocol must compute a hard rank ceiling before execution:

```text
r_max = floor(sqrt(M_step_cap / (bytes * d * n * omega * R_eff^2))).
```

If `R_eff` is unknown, P52 must estimate it from lower-rung contractions,
operator cores, or conservative preflight diagnostics before running the row.

Initial candidate ranks are bounded:

```text
r in {2, 4, 8, 16, 32}
```

Rank `64` is not part of the first production ladder unless P52-M2 proves that
the single-step memory cap remains safe and P52-M4 proves that the factorized
transition route avoids dense all-pairs materialization.

## Rank-Ladder Stop Rules

Each filtering row must sort candidate ranks increasingly and remove ranks above
`r_max` before execution.  Let the remaining candidates be
`C = {r_1, ..., r_K}`.

The row must stop with `BLOCK_P52_RANK_BUDGET_EMPTY` if `K = 0`.

If a same-target dense or exact reference exists, select the smallest rank whose
diagnostics satisfy the phase tolerances.  If no rank satisfies the tolerances,
stop with `BLOCK_P52_RANK_REFERENCE_MISMATCH` rather than increasing rank
beyond `r_max`.

If no dense/exact reference exists, a self-convergence pass requires a feasible
higher-rank deterministic comparator `r_hi` in the same frozen route, with
`r_hi > r`.  The selected rank `r` must satisfy all declared adjacent-rank
tolerances against `r_hi`.  A row cannot pass self-convergence at the largest
available rank unless a separate reviewed comparator exists.

Default first-pass tolerances, unless a phase records stricter model-specific
values before execution, are:

```text
absolute log-likelihood difference per observation <= 1e-3
relative score/gradient error, when a reference score exists <= 5e-2
directional gradient cosine, when scores are compared >= 0.995
filtered mean scaled RMSE <= 5e-2
filtered covariance relative Frobenius error <= 1e-1
deterministic replay residual == 0 within dtype-stable serialization
```

Early-stop blockers:

- two consecutive candidate ranks produce nonfinite values, nonfinite
  gradients, or memory preflight failures;
- a higher-rank comparator cannot run under the memory cap;
- diagnostics worsen by more than a factor of two for two consecutive rank
  increases without a model-invariant explanation;
- the implementation path differs from the documented P30 route.

These blockers must be recorded as rank, coordinate/factorization, or reference
strategy blockers.  They are not failures of Zhao-Cui as a mathematical idea
unless a later reviewed scientific test says so.

## Reference Hierarchy

P52 uses this ordered comparator hierarchy:

1. exact or dense same-target reference on a lower-dimensional row;
2. same-target dense reference for the tested row, if feasible;
3. same frozen factorized route at a strictly higher rank under the same memory
   contract;
4. UKF scout as sanity and scale baseline only;
5. memory and route preflight only.

Rows using only levels 4 or 5 cannot claim filtering correctness.  Rows using
level 3 can claim rank self-convergence only, not exactness.  A phase must
block with `BLOCK_P52_REFERENCE_STRATEGY_MISSING` if it needs correctness
evidence but only levels 4 or 5 are available.

## UKF Scouting Policy

UKF may be used to choose centers, scales, covariance structure, and initial
rank expectations.  UKF diagnostics may include:

- filtered means and covariances;
- covariance eigenvalue decay and effective dimension;
- local site-neighborhood correlation strength;
- state-scale and positivity diagnostics;
- likelihood scale sanity checks.

UKF does not certify the Zhao-Cui filter.  It can veto nonsense, guide grids,
and propose rank ranges, but it cannot replace lower-dimensional exact/dense
references or rank-convergence evidence.

## Dimension Policy

Spatial SIR has `d = 2J`, where `J` is the number of sites.

| Dimension | Sites | P52 role | Reasonable first claim |
| --- | --- | --- | --- |
| `d = 18` | `J = 9` | first production-like spatial SIR target after route repair | filtering/calibration candidate if factorized route, memory cap, and lower-rung checks pass |
| `d = 50` | `J = 25` | high-dimensional stress target | performance/scaling and rank self-convergence candidate; correctness only if reviewed reference strategy exists |
| `d = 100` | `J = 50` | scout and preflight target first | UKF plus memory preflight by default; actual filtering only after d=18 and d=50 pass and memory predictor clears |

The reasonable maximum first full filtering test is `d = 50`.  Dimension `100`
is reasonable for UKF scouting and memory preflight, and it may become a
bounded-horizon filtering stress row only after P52-M2 through P52-M6 pass
without increasing the rank ceiling beyond the 32 GB contract.

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required token |
| --- | --- | --- | --- | --- |
| P52-M0 | Governance, Target Lock, And Claim Boundaries | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m0-governance-target-lock-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m0-governance-target-lock-result-2026-06-10.md` | `PASS_P52_M0_GOVERNANCE_TARGET_LOCK` or `BLOCK_P52_M0_GOVERNANCE_TARGET_LOCK` |
| P52-M1 | P30 LaTeX Rank-Calibrated Route Update | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m1-p30-latex-rank-calibration-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m1-p30-latex-rank-calibration-result-2026-06-10.md` | `PASS_P52_M1_P30_LATEX_RANK_CALIBRATION` or `BLOCK_P52_M1_P30_LATEX_RANK_CALIBRATION` |
| P52-M2 | Memory-Bounded Rank Ceiling Protocol | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m2-memory-rank-ceiling-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m2-memory-rank-ceiling-result-2026-06-10.md` | `PASS_P52_M2_MEMORY_RANK_CEILING` or `BLOCK_P52_M2_MEMORY_RANK_CEILING` |
| P52-M3 | UKF Scouting And Centering Protocol | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m3-ukf-scouting-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m3-ukf-scouting-result-2026-06-10.md` | `PASS_P52_M3_UKF_SCOUTING` or `BLOCK_P52_M3_UKF_SCOUTING` |
| P52-M4 | Factorized Transition Route Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m4-factorized-transition-route-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m4-factorized-transition-route-result-2026-06-10.md` | `PASS_P52_M4_FACTORIZED_TRANSITION_ROUTE` or `BLOCK_P52_M4_FACTORIZED_TRANSITION_ROUTE` |
| P52-M5 | Rank Selection Implementation And Tests | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m5-rank-selection-implementation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m5-rank-selection-implementation-result-2026-06-10.md` | `PASS_P52_M5_RANK_SELECTION_IMPLEMENTATION` or `BLOCK_P52_M5_RANK_SELECTION_IMPLEMENTATION` |
| P52-M6 | Spatial SIR d=18 Calibration Row | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m6-spatial-sir-d18-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m6-spatial-sir-d18-result-2026-06-10.md` | `PASS_P52_M6_SPATIAL_SIR_D18` or `BLOCK_P52_M6_SPATIAL_SIR_D18` |
| P52-M7 | Spatial SIR d=50/d=100 Scaling Policy | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m7-spatial-sir-d50-d100-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m7-spatial-sir-d50-d100-result-2026-06-10.md` | `PASS_P52_M7_SPATIAL_SIR_D50_D100` or `BLOCK_P52_M7_SPATIAL_SIR_D50_D100` |
| P52-M8 | Integration Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m8-integration-closeout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m8-integration-closeout-result-2026-06-10.md` | `PASS_P52_M8_INTEGRATION_CLOSEOUT` or `BLOCK_P52_M8_INTEGRATION_CLOSEOUT` |

## P30 Consistency Gate

P52 cannot close unless M8 confirms one of:

- implementation, rank protocol, UKF scouting role, memory model, and dimension
  policy match the P30 LaTeX update from M1; or
- every deviation is documented in a reviewed P30 amendment before closeout.

The closeout must fail with `BLOCK_P52_P30_IMPLEMENTATION_DRIFT` if code,
tests, or result artifacts implement a route that is not described by the P30
mathematical and pseudocode contract.

## Repair Loop

Codex must handle fixable issues instead of stopping for no valid reason.

Fixable issues include:

- local test failures with a clear code or artifact repair path;
- stale claim language that promotes UKF, memory preflight, or rank
  self-convergence beyond its evidence;
- missing result tokens, manifests, nonclaims, commands, or memory fields;
- Claude `REVISE` findings that identify concrete plan defects;
- implementation bugs in rank-ceiling arithmetic, static route checks, or
  deterministic replay.

Human-required blockers include:

- changing the default backend away from TensorFlow/TFP;
- package installation, network fetch, credentials, or external runtime setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- GPU claims or GPU execution without trusted-context approval;
- d=100 promoted to filtering correctness without a reviewed reference and
  memory contract;
- non-convergence with Claude after five review iterations for the same major
  issue.

## Claude Review Loop

Claude is read-only reviewer only.  Use up to five iterations.  Stop early on:

```text
VERDICT: AGREE
```

If Claude returns `VERDICT: REVISE`, Codex patches the plan and resubmits,
unless the finding is a human-required blocker.  At iteration 5, accept only if
there is no major blocker; otherwise record
`BLOCKED_P52_PLAN_REVIEW_MAJOR_ISSUE`.

## Anticipated Approval Needs For Execution

The plan phase review needs escalated/trusted Claude Code use through the local
Claude worker wrapper.  Future implementation phases may need:

1. CPU-only focused `pytest` and `python -m compileall` commands with
   `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`;
2. static inspection commands such as `rg`, `sed`, and `git diff --check`;
3. no network, package installation, GPU execution, or destructive git actions
   unless separately approved.
