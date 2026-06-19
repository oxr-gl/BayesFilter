# Fixed-SGQF Broader Nonlinear Comparison Closeout

metadata_date: 2026-06-16
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-master-program-2026-06-16.md`
status: EXECUTION_COMPLETE

## Question

Where does the repaired fixed-SGQF lane fit into the broader repo-wide nonlinear
comparison ecosystem, and which model families can it enter honestly under the
current lane semantics?

## Executive summary

The broader repo-wide nonlinear comparison ecosystem is much wider than the
narrow A/B/C benchmark harness. For eventual literature-facing leaderboard
studies, the governing scope is the repo's **source-paper scope contract**, not
the older 12-row diagnostic roster.

Under the **current additive-state fixed-SGQF lane**, fixed SGQF fits honestly
into only a subset of that broader literature-backed ecosystem.

### Literature-backed families kept in final leaderboard scope
- **benchmark_lgssm_exact_oracle_m3_T50**
- **zhao_cui_sv_actual_nongaussian_T1000**
- **zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000**
- **zhao_cui_spatial_sir_austria_j9_T20**
- **zhao_cui_predator_prey_T20**
- **zhao_cui_generalized_sv_synthetic_from_estimated_values**

### Engineering/debugging-only rows excluded from final leaderboard scope
- `p44_cubic_additive_gaussian_dim_1_2_3`
- `p44_quadratic_observation_dim_1_2_3`
- `p44_nonlinear_transition_h2_dim_1_2_3`
- `p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3`

### Admitted now
- **LGSSM / affine exact-reference rows**
- **Model A / affine benchmark rows** in the narrow harness
- **Model C / autonomous nonlinear growth** through the new exact-gated
  structural adapter in the narrow harness

### Not yet admitted repo-wide
- most broader literature-backed nonlinear families remain blocked under the
  current lane semantics, including generalized SV native rows, spatial SIR
  scaling/source-route rows, predator-prey production rows, and DPF/range-
  bearing comparison streams.

So fixed SGQF is now better placed than before, but it is **not** yet a full
repo-wide deterministic family peer across the whole literature-backed nonlinear
comparison backbone.

## Family-level admission summary

| Family / row class | Current fixed-SGQF status | Scope role | Reason |
| --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` / LGSSM-affine exact rows | `admit_exact` | final literature-backed scope | fixed SGQF already matches exact Kalman on tested affine Gaussian rows |
| narrow-harness Model A affine oracle | `admit_exact` | local anchor that supports the broader affine admission | already integrated and benchmarked |
| narrow-harness Model C autonomous nonlinear growth | `admit_exact` within current narrow adapter scope | local engineering proof of one non-affine exact-gated admission | admitted by the new structural adapter and semidefinite state-covariance handling |
| narrow-harness Model B nonlinear accumulation | `blocked_not_same_target` | local engineering blocker | innovation enters deterministic block through nonlinear completion; not exact under current additive-state SGQF lane |
| `zhao_cui_sv_actual_nongaussian_T1000` | `blocked_not_same_target` | final literature-backed scope | current fixed SGQF lane is not yet an admitted same-target route for actual non-Gaussian SV |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `diagnostic_or_adapter_required` | final literature-backed scope | current fixed SGQF lane is not yet admitted in the surrogate route stack |
| `zhao_cui_spatial_sir_austria_j9_T20` | `blocked_not_same_target` | final literature-backed scope | current SGQF lane is not in the admitted source-route / scaling ladder |
| `zhao_cui_predator_prey_T20` | `blocked_not_same_target` | final literature-backed scope | no current same-target SGQF production route is defined there |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked_not_same_target` | final literature-backed scope | current fixed SGQF lane is not yet the admitted same-target route for this family |
| P44 debugging rows | `engineering_debug_only` | excluded from final literature-backed scope | BayesFilter-only debugging fixtures, not standard literature leaderboard rows |
| DPF / range-bearing external comparison streams | `blocked_not_same_target` | outside final literature-backed deterministic SGQF scope | comparison stream is different in purpose and target semantics |

## Admitted anchor families

### 1. LGSSM / affine exact anchor
This is the strongest current broader admission.

Supporting evidence:
- repaired fixed-SGQF affine exact rows already established in:
  - `docs/plans/bayesfilter-fixed-sgqf-p4-affine-kalman-ladder-result-2026-06-14.md`
  - `docs/plans/bayesfilter-fixed-sgqf-p8-closeout-and-claim-audit-result-2026-06-14.md`
- benchmark admission in the narrow nonlinear harness also exists.

Interpretation:
- fixed SGQF is already a legitimate deterministic algorithm lane for affine
  exact-reference rows.

### 2. Model C exact-gated narrow admission
This is a new exact-gated admission in the narrow harness only.

Supporting evidence:
- `docs/plans/bayesfilter-fixed-sgqf-structural-adapter-result-2026-06-16.md`

Interpretation:
- Model C proves the current lane can be extended beyond affine rows when the
  structural model is exactly compatible with the additive-state fixed-SGQF form.
- This does **not** automatically admit the whole broader repo-wide nonlinear
  family roster.

## Blocked-family ledger

### Model B nonlinear accumulation
Status: `blocked_not_same_target`

Reason:
- innovation enters the deterministic block through `k_next = alpha * k_prev + beta * tanh(m_next)`.
- this is not a constant additive-Gaussian full-state lane under the current
  fixed-SGQF assumptions.

### Native generalized SV rows
Status: `blocked_not_same_target`

Reason:
- the broader registry already uses declared native dense or transformed/surrogate
  routes there.
- current fixed SGQF does not yet have an admitted same-target route in that
  family.

### Spatial SIR scaling/source-route rows
Status: `blocked_not_same_target`

Reason:
- the current SIR ecosystem is governed by source-route/scaling ladders where
  fixed SGQF is not an admitted lane.
- current additive-state fixed SGQF is not the same-target structural route.

### Predator-prey production rows
Status: `blocked_not_same_target`

Reason:
- these rows are tuned and admitted under different route assumptions.
- no current fixed-SGQF same-target production route is defined there.

### DPF / range-bearing comparison streams
Status: `blocked_not_same_target`

Reason:
- these are separate comparison ecosystems with different algorithm classes and
  target semantics.

## Broader comparison claim boundaries

### Supported now
1. Fixed SGQF has a legitimate place in the repo-wide nonlinear ecosystem as an
   admitted deterministic lane for affine exact-reference rows.
2. Fixed SGQF can also admit at least one non-affine structural family (Model C)
   under an exact-gated adapter in the narrow benchmark harness.
3. The broader comparison program can now state honestly where fixed SGQF is
   admitted and where it is blocked within the **literature-backed source-paper
   scope**, rather than treating all nonlinear families as interchangeable.
4. The three P44 debugging families are explicitly excluded from eventual final
   literature-facing fixed-SGQF leaderboard studies while being preserved as
   local engineering/debugging evidence.

### Not supported now
1. No claim that fixed SGQF is admitted repo-wide across all literature-backed
   nonlinear families.
2. No claim that the broader SV, SIR, predator-prey, or DPF/range-bearing
   families are all current same-target SGQF rows.
3. No repo-wide score-lane admission claim.
4. No universal ranking claim across the broader nonlinear ecosystem.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| close the broader admission scan as a truthful placement pass | satisfied | no blocked family was admitted without justification | which broader low-dimensional deterministic P44 rows can be admitted next | pursue family-by-family deterministic admissions rather than blanket promotion | no repo-wide full nonlinear admission claim |

## Recommended next step
The next justified expansion is **not** “admit everything.”
It is:

1. keep the final literature-facing leaderboard scope restricted to the
   literature-backed source-paper rows,
2. preserve the P44 rows only as engineering/debugging evidence,
3. choose one admitted literature-backed family beyond the affine anchor,
4. test exact same-target compatibility against the current fixed-SGQF lane,
5. admit it only if the semantics line up cleanly,
6. otherwise keep it blocked explicitly.

In other words, the repo-wide expansion path should be:
- affine anchor first,
- then one literature-backed family at a time,
- while keeping generalized SV, SIR, predator-prey, and DPF/range-bearing rows
  blocked until a richer SGQF lane exists.
