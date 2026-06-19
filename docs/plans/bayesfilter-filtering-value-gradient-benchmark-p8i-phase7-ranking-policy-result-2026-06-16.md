# P8i Phase 7 Result: Scope, Ranking, And Default-Policy Decision

Date: 2026-06-16

Status: `PASS_NO_RANKING_NO_DEFAULT_POLICY_REVIEWED`

## Phase Objective

Decide what, if anything, the reviewed P8i artifacts support about filter
ranking, generic high-dimensional LEDH readiness, and default sampler policy.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Do the collected reviewed P8i artifacts justify any ranking, high-dimensional readiness, or default-policy change? |
| Baseline/comparator | Reviewed P8i results and blockers, including Phase 6; P8h is used only through artifacts explicitly inherited or re-tested by P8i. |
| Primary criterion | A conservative decision table either justifies a narrow claim or preserves the nonclaim with explicit missing evidence. |
| Veto diagnostics | Ranking without comparable baselines; default-policy change from diagnostic-only evidence; generic high-dimensional readiness from scalar-SV evidence; production-HMC, posterior, NUTS, exact-likelihood, or stochastic-gradient claims revived after Phase 6 blocked them. |
| Explanatory diagnostics | Artifact coverage matrix and remaining blocker table. |
| Not concluded | Filter ranking, generic high-dimensional LEDH readiness, default sampler policy, or any Phase 6 blocked claim. |

## Skeptical Audit

- Wrong-baseline check: P8h is not treated as a live comparator or proof of
  broader readiness; only P8i-inherited or P8i-retested artifacts count.
- Proxy-metric check: finite values, finite gradients, runtime, and tiny HMC
  execution are not promotion criteria for ranking or default policy.
- Stop-condition check: any ranking or policy claim would require new
  comparative experiments or code-default changes, both outside this phase.
- Artifact-fit check: a decision artifact answers the phase question; no new
  numerical run is needed.

## Artifact Coverage Matrix

| Artifact | Coverage | Boundary |
|---|---|---|
| Phase 0 gap ledger | Maps P8h nonclaims to P8i gates. | Governance only; no scientific or runtime claim. |
| Phase 1 value/count ladder | Selects diagnostic `N=5` for horizons `16,32` under finite/trusted-GPU/transport/runtime/MCSE/adjacent-rung gates. | Not full-horizon adequacy, ranking, or policy. |
| Phase 2 gradient ladder | Shows finite connected fixed-seed relaxed-OT AD gradients at horizons `16,32`, `N=5`, with FD residuals below `1e-5`. | Not exact stochastic PF marginal-gradient correctness. |
| Phase 3 GPU profile | Shows selected route/count is practically executable for a bounded Tier-1 HMC diagnostic. | Not full GPU scaling law or HMC readiness. |
| Phase 4 fixed-kernel HMC diagnostic | Shows a tiny fixed-kernel HMC execution at H32, `N=5`, with finite trusted-GPU traces within budget. | Not posterior convergence, valid tuning, production HMC readiness, or NUTS readiness. |
| Phase 5 NUTS decision | Blocks NUTS because no command path, adaptation budget, or diagnostics exist. | No NUTS readiness or sampler recommendation. |
| Phase 6 claim boundary | Classifies relaxed-OT AD gradient evidence as diagnostic and blocks exact stochastic-gradient/exact-likelihood claims. | No exact likelihood, stochastic marginal score, ranking, or default policy. |

## Remaining Blocker Table

| Claim | Decision | Missing evidence |
|---|---|---|
| Filter ranking | Blocked / not concluded. | Comparable value, gradient, runtime, likelihood, and sampler diagnostics across candidate filters. |
| Generic high-dimensional LEDH readiness | Blocked / not concluded. | Evidence beyond scalar-SV prefixes, with reviewed high-dimensional model scope and route-specific diagnostics. |
| Default sampler policy change | Blocked / not concluded. | Production-grade sampler evidence, convergence/tuning diagnostics, runtime budgets, and code-policy review. |
| NUTS readiness | Blocked / not concluded. | NUTS command path, adaptation budget, diagnostics, and reviewed subplan after stronger HMC evidence. |
| Production HMC readiness | Blocked / not concluded. | Real HMC tuning, multi-chain diagnostics, convergence evidence, and posterior/reference checks. |
| Exact nonlinear likelihood correctness | Blocked / not concluded. | Exact-likelihood tieout or derivation for the nonlinear model. |
| Stochastic PF marginal-gradient correctness | Blocked / not concluded. | Derivation or estimator contract tying the AD graph to the stochastic PF marginal score. |

## Checks

```bash
rg -n "no filter ranking|not a filter ranking|default sampler policy|generic high-dimensional LEDH readiness|production HMC readiness|posterior convergence|NUTS readiness|exact nonlinear likelihood correctness|stochastic PF marginal-gradient correctness" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Results:

- Boundary/nonclaim search: passed.
- `git diff --check`: passed.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Preserve no ranking, no generic high-dimensional readiness, and no default sampler policy, pending review. | The conservative decision table is complete and includes artifact coverage plus missing evidence. | No ranking/default-policy veto fired because no such claim is made. | The scalar-SV diagnostic route may still be useful, but the current evidence is too narrow for policy promotion. | Refresh Phase 8 closeout with artifact index, reset memo, and repo boundary manifest. | No filter ranking, generic high-dimensional LEDH readiness, default sampler policy, NUTS readiness, production HMC readiness, posterior convergence, exact likelihood correctness, or stochastic PF marginal-gradient correctness. |

## Post-Run Red-Team Note

Strongest alternative explanation: the route may eventually rank well or become
a useful default after broader evidence, but P8i has not run the comparative
or convergence diagnostics required for that conclusion.

What would overturn this result: a reviewed comparison ladder with comparable
baselines, full diagnostic coverage, and a separate policy-change review.

Weakest part of the evidence: P8i is intentionally a remaining-gap closure
program for one inherited scalar-SV route, not a full method comparison.

## Handoff

Read-only review accepted this decision after a focused Phase 8 entry/stop
condition repair. Phase 8 must preserve all blockers and must not commit,
push, or mix unrelated Zhao-Cui/monograph/P8h dirty work without a fresh
explicit request.
