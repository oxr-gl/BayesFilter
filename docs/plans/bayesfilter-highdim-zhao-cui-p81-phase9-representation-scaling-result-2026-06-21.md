# P81 Phase 9 Result: Representation Scaling Route

status: PASS_PHASE9_SELECT_PARAMETERIZED_LOCAL_ROUTE_TIEOUT
date: 2026-06-21

## Phase Objective

Decide the next representation or transition-application step after Phase 8
showed that streamed all-pairs transition propagation is still quadratic and
therefore not a meaningful route to the SIR d=18 full-history fixed-branch
score.

Phase 9 was read-only audit/design.  It did not run LEDH-PFPF-OT diagnostics,
GPU benchmarks, d=18 full-grid transition propagation, or implementation
edits.

## Skeptical Plan Audit

The plan passed only under a narrowed interpretation:

- wrong baseline avoided: the baseline is the current all-grid dense/streamed
  retained route and prior P52/P53 scaling artifacts, not LEDH-PFPF-OT;
- proxy metric avoided: tiny d=2 dense-vs-streaming parity remains
  implementation evidence only;
- stale context checked: P52/P53 already contain a local-neighborhood scaling
  route, but P53-M5 blocks exact d=18 rank selection under the 8 GiB step cap;
- source boundary preserved: P56 classifies the local/operator route as
  `extension_or_invention` for source-faithfulness claims;
- artifact usefulness checked: Phase 9 can select a next implementable tie-out
  step, but cannot authorize d=18 correctness or stochastic comparison.

## Read-Only Checks Run

```bash
rg -n "streamed_or_factorized_transition_application|dense all-pairs|factorized_transition|scaling_route|R_eff" docs/plans bayesfilter/highdim tests/highdim -g '*.md' -g '*.py'
rg -n "class .*Transition|factorized|local|neighborhood|LowerRungStreamingRouteConfig|LocalNeighborhoodScalingRouteConfig|transition" bayesfilter/highdim/transition_route.py tests/highdim/test_p52_factorized_transition_route.py tests/highdim/test_p53_m4*.py
rg -n "_multistate_grid_predictive_log_density_from_retained_streaming|_check_pairwise_transition_tensor_budget_conservative|_validate_streaming_transition_inputs" bayesfilter/highdim/filtering.py
```

Outcome: the audit confirmed that P52 names the all-grid pairwise route as the
forbidden scaling blocker, P53 implements a local-neighborhood TensorFlow route
and lower-rung tie-out, and Phase 8 added streamed helpers plus conservative
chunk guards.  The grep output is large because historical dirty-worktree
artifacts are present, but the relevant paths were inspected directly.

## Route Comparison

| Option | Phase 9 conclusion |
|---|---|
| Keep streamed all-pairs with subsets | Not sufficient.  It is useful for tiny parity and integration coverage only.  It still sums over all current/previous retained rows and cannot be the d=18 full-history route. |
| Factorized Gaussian transition application | Mathematically relevant because the transition covariance is diagonal and the log-density factorizes by coordinate.  P53 already implements this as a local-neighborhood primitive for `SpatialSIRSSM`. |
| TT contraction / low-rank transition operator | Still plausible as a later route, but Phase 9 found no ready implementation with theta-derivative semantics and memory/rank contract. |
| Local/neighborhood route | Smallest implementable next step for deterministic fixed-gradient diagnostics.  It already has P53 lower-rung value/current-gradient tie-out, but it currently assumes `SpatialSIRSSM` and discards `theta`. |
| Source-route sample/ESS propagation | Required for source-faithful Zhao-Cui claims, but separate from this deterministic fixed-branch diagnostic lane.  P56 says local/operator routes cannot close source-faithfulness gaps. |

## Selected Next Route

Phase 9 selects a Phase 10 parameterized local-route tie-out:

```text
route: P53 local-neighborhood transition factorization
scope: deterministic fixed-gradient diagnostic lane only
model target: ParameterizedZhaoCuiSIRSSM
claim class: extension_or_invention for source-faithfulness
next evidence: tiny value and theta-derivative tie-out against dense transition
```

The concrete implementation gap is:

```text
spatial_sir_local_coordinate_log_factor(...)
```

currently discards `theta` and calls:

```text
model.transition_mean(previous)
```

That is correct for `SpatialSIRSSM`, but not for
`ParameterizedZhaoCuiSIRSSM`, whose transition mean is:

```text
model.transition_mean(theta, previous)
```

Phase 10 should add a narrow TensorFlow helper/API adaptation so the local route
uses the same theta convention as the P81 fixed branch and the LEDH-PFPF-OT
lane.  It should then test tiny dense-vs-local value and theta-gradient/JVP
parity before any d=18 attempt.

## P53-M5 Memory Blocker

P53-M5 remains binding for d=18 exact local-route admission:

```text
R_eff = 2916
basis_order = 3
dimension = 18
step_cap = 8 GiB
rank-1 forecast = 29,386,561,536 bytes
r_max = 0
```

Therefore Phase 10 must not claim that the local route solves d=18 scaling.  It
only repairs the parameterized semantics and derivative tie-out needed before a
later memory/rank-policy or compressed-operator phase.

## Decision Table

| Decision | Primary criterion status | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Pass Phase 9 and draft Phase 10 | Met: selected parameterized P53 local-route tie-out as the smallest implementable next step | No LEDH comparison; no d=18 full-grid run; no source-faithful claim; no dense all-pairs promotion | Exact local route is still too wide for d=18 under P53-M5; compressed/operator or source-route path remains open | Implement parameterized local route support and tiny value/theta-derivative tie-out | No d=18 full-history correctness, no LEDH agreement, no HMC readiness, no posterior validity, no source-faithfulness, no default readiness |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | Dirty worktree; no commit made |
| Command | Three read-only `rg` audit commands from Phase 9 subplan |
| Environment | Local Python/repo shell |
| CPU/GPU status | No GPU/CUDA command; read-only text audit |
| Data version | N/A |
| Random seeds | N/A |
| Wall time | Short text audit commands |
| Output artifacts | This result file and Phase 10 subplan |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase9-representation-scaling-subplan-2026-06-21.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase9-representation-scaling-result-2026-06-21.md` |

## Nonclaims

This result does not establish d=18 full-history likelihood correctness,
stochastic comparator agreement, LEDH-PFPF-OT value/gradient agreement, HMC or
NUTS readiness, posterior validity, source-faithfulness, production readiness,
or default-readiness.

## Next Handoff

Proceed to Phase 10 only after Claude reviews this result and the Phase 10
subplan.  Phase 10 is allowed to edit only the parameterized local-route support
and focused tests described in its subplan.
