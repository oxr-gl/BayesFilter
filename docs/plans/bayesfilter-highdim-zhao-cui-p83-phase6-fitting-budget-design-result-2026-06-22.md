# P83 Phase 6 Result: Source-Route Fitting Budget Design

Date: 2026-06-22

Status: `PASS_P83_PHASE6_FITTING_BUDGET_DESIGN`

## Decision

Phase 6 defines the fixed-TTSIRT source-route fitting budget discipline before
any fitting ladder or SIR d=18 validation run.

This phase is design-only.  No fitting run, d=18 validation, GPU job, LEDH
comparison, HMC/MCMC run, or production source-route correctness claim was
launched or authorized.

The Phase 4 analytical derivative blocker remains active:
`BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS`.

## Skeptical Audit

The Phase 6 plan passes for design-only execution.

- Wrong-baseline risk is controlled by using local `FixedTTFitter` budget
  mechanics and author source settings as budget inputs, not as correctness
  evidence.
- Proxy-promotion risk is controlled: training residual, holdout residual,
  replay diagnostics, finite values, ESS, validation CE, and audit clouds may
  veto or explain only under their declared roles.
- Stop conditions are explicit: any fitting, d=18, GPU, LEDH, HMC, production
  KR, or derivative-readiness need blocks this phase.
- Environment mismatch is avoided because Phase 6 runs only read-only searches
  and markdown hygiene checks.
- The artifacts answer the stated budget question and do not attempt to answer
  source-route numerical validity.

## Evidence Contract Result

| Field | Result |
|---|---|
| Question | What source-route fixed-TTSIRT fitting budget, rank/degree ladder, sample minimum, and diagnostics are required before any d=18 validation attempt? |
| Baseline/comparator | Phase 4 blocker, Phase 5 mechanics smoke, local `FixedTTFitConfig`/`FixedTTFitter`, P58/P66/P77 budget discipline, and Zhao-Cui author SIR/TTSIRT source anchors. |
| Primary criterion status | PASS: parameter-count formula, sample minimum, candidate ladder, fit/holdout gates, heldout/audit clouds, and stop conditions are stated below; local checks and Claude boundary review passed. |
| Veto diagnostic status | PASS for design scope: no fitting, d=18 validation, GPU, LEDH, HMC, derivative-readiness claim, production KR closure, or source-route correctness claim is made. |
| Explanatory diagnostics | Read-only code/source inventory and budget tables. |
| Not concluded | No fit quality, no d=18 correctness, no derivative readiness, no LEDH readiness, no HMC readiness, no production source-route correctness. |

## Anchors Used

Local fitter anchors:

- `bayesfilter/highdim/fitting.py:39-107`: `FixedTTFitConfig` declares ranks,
  sweep order, row/column budgets, byte budgets, condition gates, holdout
  tolerance, float64 dtype, and solver/stabilization policy.
- `bayesfilter/highdim/fitting.py:111-152`: `FixedTTFitSampleBatch` separates
  training samples from optional holdout samples.
- `bayesfilter/highdim/fitting.py:224-348`: `FixedTTFitter.fit` records core
  update statuses, fit residual, holdout residual, and holdout veto.
- `bayesfilter/highdim/fitting.py:350-390`: `build_core_update_system`
  exposes the core design matrix and diagnostics.
- `bayesfilter/highdim/fitting.py:544-598`: `_check_design_budget` computes
  rows, columns, dense matrix bytes, normal matrix bytes, and budget gates.

Local readiness/launch guard anchors:

- `bayesfilter/highdim/source_route.py:1316-1363`: P58/P59 M9 readiness
  payload and nonclaims.
- `bayesfilter/highdim/source_route.py:1507-1560`: P58/P59 source-route launch
  readiness fails closed on missing d=18 source-route assembly or drift.
- `bayesfilter/highdim/source_route.py:6540-6665`: P59 runner manifest consumes
  assembly artifacts and records fit sample counts/row adequacy before the
  validation ladder.
- `bayesfilter/highdim/source_route.py:6726-6860`: P59 validation ladder has an
  execution-only tier and blocks higher correctness/rank-convergence tiers.

Author source anchors:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`:
  SIR uses `d=0`, `m=18`, `T=20`, so the fixed route target dimension is
  `D = d + 2*m = 36`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:39-55`:
  author SIR declares `N=5e3`, `sqr=1`, `Lagrangep(4,8)` on
  `AlgebraicMapping(1)`, `TTOption` main/low settings, and calls `full_sol`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`:
  source route pushes samples, reapproximates, samples via `eval_irt`, maps
  through `L`/`mu`, and corrects with `eval_pdf`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:64-98`:
  source fit data uses `computeL`, weighted resampling, `epd` scaling, and
  split unweighted local samples into init/debug clouds.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Options/TTOption.m:61-91`:
  author TT options include `max_als`, `init_rank`, `kick_rank`, `max_rank`,
  local/CDF tolerances, and `random`/`amen`/`fix_rank`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:185-188`:
  executable TTSIRT default defensive `tau` is `1E-8`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTFun/TTFun.m:176-204`:
  author TTFun sample-size heuristic is
  `(init_rank + kick_rank * (1 + max_als)) * ndims`.

## Parameter Count Contract

For fixed TT ranks `ranks = (r_0, ..., r_D)` and per-axis basis dimensions
`b_axis`, with `r_0 = r_D = 1`, the fixed parameter count is:

```text
P_theta = sum_axis ranks[axis] * b_axis * ranks[axis + 1]
```

For a uniform interior rank `R` and uniform basis dimension `b` over the
author SIR target dimension `D=36`, this becomes:

```text
P_theta = b * (2 * R + 34 * R^2)
```

The hard source-route fitting evidence minimum is:

```text
minimum_training_samples = max(20 * P_theta, author_source_sample_floor)
author_source_sample_floor = 5000 for the SIR d=18 author route
```

The `20 * P_theta` term is binding for every candidate in the ladder below.
The author `N=5000` floor prevents tiny fixed-branch diagnostics from being
mistaken for author-scale source-route evidence.

## Basis And Rank Ladder

Author SIR uses `Lagrangep(4,8)`.  The source cardinality implied by the
author polynomial construction is:

```text
author_basis_dim = num_elems * order + 1 = 8 * 4 + 1 = 33
```

The current BayesFilter fixed fitter supports local `LegendreBasis1D`, where:

```text
local_basis_dim = max_degree + 1
```

Therefore the ladder has two lanes:

- Local fixed-HMC diagnostic lane: useful for implementation and budget
  discipline, but not author-basis parity.
- Author-basis lane: required before paper-scale source-route claims, and
  blocked until a source-backed basis/domain route is implemented or a reviewed
  fixed adaptation explicitly authorizes the substitute.

| Lane | Basis dimension | Rank pattern | `P_theta` | Minimum training samples | Role |
|---|---:|---|---:|---:|---|
| Local diagnostic rung A | `2` | `(1,2,...,2,1)` | `280` | `5600` | plumbing only |
| Local diagnostic rung B | `3` | `(1,4,...,4,1)` | `1656` | `33120` | first serious local budget diagnostic |
| Local stronger rung C | `4` | `(1,8,...,8,1)` | `8768` | `175360` | stronger local fixed-rank diagnostic |
| Local degree-richer rung D | `5` | `(1,8,...,8,1)` | `10960` | `219200` | degree sensitivity diagnostic |
| Local rank-richer rung E | `4` | `(1,12,...,12,1)` | `19680` | `393600` | rank sensitivity diagnostic |
| Author-basis rung F | `33` | `(1,4,...,4,1)` | `18216` | `364320` | author-basis feasibility rung |
| Author-basis rung G | `33` | `(1,8,...,8,1)` | `72336` | `1446720` | author-basis stronger rung |
| Author option envelope | `33` | effective rank `20` envelope | `450120` | `9002400` | not launchable without a separate long-run plan |

The author-option envelope is not a required immediate execution target.  It is
recorded to show that full author-rank-scale fitting would be a large,
separately approved run.

## Required Fit Gate For Any Later Fitting Run

A later fitting phase may not pass unless its result manifest records all of
the following:

- `evidence_run=true` or an equally explicit source-route fit-evidence marker;
- `target_id="zhao_cui_sir_austria_d18"`;
- `target_dimension=36`;
- `route_class="fixed_ttsirt_source_route"`;
- exact rank tuple, basis dimensions, basis/domain route, branch seed, fit data
  mode, defensive tau, and source anchors;
- `P_theta` and `minimum_training_samples` computed before execution;
- completed training samples greater than or equal to the declared minimum;
- no overlap between training, holdout, replay, validation, and audit seeds or
  sample identifiers;
- every core update status is OK;
- no row/column/dense-byte/normal-byte/condition-number gate trips;
- fit residual is finite;
- holdout residual is finite and not above the predeclared holdout tolerance;
- holdout is not used for final audit claims;
- production KR closure remains false unless a later reviewed source-backed KR
  replacement changes that status.

Fit residual alone is explanatory.  A finite/improved training loss cannot by
itself establish source-route correctness, d=18 correctness, derivative
readiness, HMC readiness, or production readiness.

## Heldout, Replay, Validation, And Audit Clouds

All clouds must be source-route local-coordinate clouds, not arbitrary
model-generated substitutes.

| Cloud | Source | Role | May select/tune? | May veto? | Nonclaim |
|---|---|---|---|---|---|
| Training | source-pushed `computeL`/weighted-resampled fit data in local coordinates | fit TT cores | yes, only within predeclared fit algorithm | yes, for nonfinite target/weights or budget failure | no correctness claim |
| Holdout | disjoint source-pushed local cloud with target values and weights | fit-quality veto and early failure detection | no rank/degree selection unless predeclared | yes, for nonfinite or tolerance violation | no final audit claim |
| Replay | frozen retained/source-route points across steps | branch replay, retained carry, proposal correction diagnostics | no | yes, for provenance/finite/reconstruction failures | no selection claim |
| Validation | disjoint cloud declared before candidate comparison | choose between predeclared rank/degree candidates if Phase 7 authorizes it | yes, only for declared candidate comparison | yes | no posterior/HMC claim |
| Audit | final-only disjoint source-route cloud | report final selected-candidate diagnostics | no | yes, for invalid final evidence construction | no correctness by itself |

The audit cloud must remain unused for fitting, stopping, rank/degree tuning,
threshold changes, or rescue after validation failure.

## Phase 7 Handoff

Phase 7 may be drafted, but it is not executable until all of the following are
true:

- Phase 6 local checks pass;
- Claude read-only review agrees the Phase 6 design and Phase 7 handoff are
  safe;
- a reviewed Phase 7 subplan freezes exact command(s), runtime/GPU posture,
  seeds, fit artifacts, comparator tier, pass/fail criteria, and vetoes;
- the required fit artifacts and manifests exist or the Phase 7 subplan is
  explicitly an implementation/fitting phase rather than a validation run;
- Phase 4 derivative readiness is either still declared blocked and out of
  scope, or a separate reviewed derivative repair has passed;
- the user explicitly approves any long, GPU, d=18 validation, LEDH, fitting,
  HMC, or MCMC command before execution.

## Decision Table

| Decision | Primary criterion status | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Pass Phase 6 fitting-budget design. | Passed: design is written, local doc checks passed, and Claude boundary review agreed. | No prohibited run or production/scientific claim made. | Real fit quality, author-basis feasibility, and derivative readiness remain unresolved. | Keep Phase 7 as blocked draft until exact commands/artifacts and human approval are available. | No fit quality, d=18 correctness, derivative readiness, LEDH readiness, HMC readiness, or production source-route correctness. |

## Local Checks

Passed:

```text
rg -n "FixedTTFitConfig|FixedTTFitter|ranks|degree|parameter_count|sample_count|row adequacy|20 \\*|fit_sample|training|heldout|audit|condition|rank" \
  bayesfilter/highdim \
  tests/highdim \
  docs/plans/bayesfilter-highdim-zhao-cui-p6*.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p7*.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p8*.md -S

rg -n "fit|approximate|TTSIRT|SIRT|tau|sample|computeL|mainscript|full_sol|setup" \
  third_party/audit/zhao_cui_tensor_ssm_p10/source/models \
  third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src -S

git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md
```

The `rg` checks returned matches and the `git diff --check` command returned
cleanly.

## Claude Review

- `p83-p6-budget-p7-handoff-review-r1`: stalled with no usable output and was
  interrupted.
- `p83-p6-claude-probe`: returned `PROBE_OK`.
- `p83-p6-budget-p7-handoff-review-r2`: `VERDICT: AGREE`.
