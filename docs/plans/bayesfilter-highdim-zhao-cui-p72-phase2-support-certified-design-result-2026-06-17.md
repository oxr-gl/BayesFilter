# P72 Phase 2 Result: Support-Certified Design Contract

metadata_date: 2026-06-17
status: PHASE2_PASSED_CLAUDE_R3_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | What exact finite guard/audit/line/conditioning contract should the fixed-variant repair implement and diagnose? |
| Baseline/comparator | P70 Phase 6h failed evidence, P72 repair note, Phase 1 classification ledger, and P70/P71 diagnostic vocabulary remapped through Phase 1 classifications. |
| Primary criterion | Freeze finite cloud rules, observables, thresholds, scaling/effective-rank conventions, classification labels, and pass/block semantics before implementation or repaired diagnostic output. |
| Veto diagnostics | Vague thresholds; fit residual used as sole pass criterion; low/high branch closeness as a criterion; guard additions called source-faithful; downstream validation authorized; unclassified P70/P71 observables admitted; optional shape/stable-LS candidates made mandatory. |
| Explanatory only | Support-distance summaries, clipping summaries below block thresholds, expected runtime, optional future stable-LS/Christoffel literature directions, and continuum-support theory. |
| Not concluded | No implementation, no repaired diagnostic pass, no continuum support theorem, no d18 validation, no HMC readiness, no source-faithfulness closure for guard/stability additions, no original Zhao--Cui failure claim. |
| Artifact preserving result | This Phase 2 result, execution ledger, review ledger, and Phase 3 subplan. |

## Skeptical Plan Audit

Phase 2 survives the skeptical audit.  The baseline is the actual P70 Phase 6h
failure: row A has off-cloud line values up to `2.053e10` and raw
holdout/replay residuals up to `4.827e11`; row B has a scaled augmented
condition `1.305e14 > 1e14`.  This result does not promote fit residual,
validation accuracy, low/high closeness, timing, or downstream filtering
metrics.  It freezes finite observables and thresholds before any repaired
implementation or repaired diagnostic output is seen.

## Imported-Observable Admission Table

| Observable or candidate | Phase 1 classification row | Admitted Phase 2 role | Mandatory? |
| --- | --- | --- | --- |
| Fit cloud `Z_fit` and same scalar target | fixed ranks/bases/domains/samples/seeds and broad TT/SIRT route | Define the original fixed regression cloud and target scale. | yes |
| Guard cloud `Z_guard` | guard/audit/line/max gates are `extension_or_invention` | Enter the repaired finite fit objective and gate. | yes |
| Audit cloud `Z_audit` | guard/audit/line/max gates are `extension_or_invention` | Decide admission without coefficient selection. | yes |
| Holdout/replay residuals | guard/audit/holdout/replay gates are `extension_or_invention` | Veto finite off-cloud failure. | yes |
| Line-probe absolute values and growth | line-probe gates are `extension_or_invention` | Veto the Phase 6h off-cloud growth pattern. | yes |
| Column-scaled augmented ridge condition observable | current stable solve is `fixed_hmc_adaptation` | Record the inherited fixed-solver singular spectrum and scaled condition. | yes |
| P72 condition/effective-rank admission gate | conditioning admission is `extension_or_invention` | Veto near-null declared local directions and stricter-than-P70 fixed lower-gate conditioning. | yes |
| Rank-direction activity | rank-direction activity gates are `extension_or_invention` | Prevent aggregate residuals from hiding inactive rank channels. | yes |
| Squared-density normalizer and defensive mass | squared TT/normalizer role is source-anchored; finite gate is fixed-variant stabilization | Preserve noncollapsed finite density evidence. | yes |
| Support distance and clipping summaries | support-distance gates are `extension_or_invention` | Record coverage risk and block only nonfinite/all-clipped clouds. | diagnostic plus finite-data block |
| Shape penalties, derivative penalties, line-growth objective penalties | `extension_or_invention` plus literature/source gap | Quarantined optional future candidates. | no |
| Christoffel/leverage/oversampling/stable-LS theorem claims | `SOURCE_GAP_BLOCKER` for theorem-level support | Quarantined optional future literature lane. | no |

No P70/P71 diagnostic vocabulary is admitted merely because it appeared in an
earlier artifact.  The table above is the only Phase 2 admission route.

## Frozen Cloud Definitions

All clouds are constructed inside the same fixed branch, same coordinate
frame, same shift convention, same model observations, same ranks, same
degree, same sweep order, same ridge, and same branch identity rules as the
P70 row under diagnosis.  Cloud construction is deterministic and recorded by
hash before fitting.

### Fitting Cloud

`Z_fit` is the source-route fixed branch fitting cloud already used by the
row.  Its target is the frozen-branch square-root target

```text
y_fit(z) = exp(-0.5 * shifted_negative_log_target(z))
```

using the fitted coordinate frame and shift constant.  Fit weights are the
existing source-route fit weights, normalized to sum one for reporting.
The same direct target-evaluation rule is mandatory for every guard, audit,
and line-probe point in P72; no line residual is optional because every
line-probe point lies in the fixed local coordinate frame and has the same
frozen target definition.

### Guard Cloud

`Z_guard` is created before the fit is solved.  It is used for coefficient
selection by augmenting the fixed least-squares data, but it is not an adaptive
post-output selection.

For the P70/P72 bounded SIR diagnostic, use the same deterministic diagnostic
data constructor as P69/P70 with new guard-only seeds:

| Time step | Guard construction | Seeds |
| --- | --- | --- |
| 1 | `p72_step1_guard_distinct_diagnostic_seed` | prior `7321`, process noise `7601` |
| 2 | `p72_step2_guard_distinct_diagnostic_seed` | previous retained object from step 1, process noise `7602` |

The base guard count equals the fixed row fit count.  Guard base points are
augmented with line points from nearest fit points to selected guard endpoints:
nearest, median-distance, and farthest guard point relative to `Z_fit`, with
duplicates removed.  The finite fractions are

```text
S = (0.0, 0.25, 0.5, 0.75, 1.0).
```

Only guard endpoints and guard-line points enter the repaired objective.  The
guard target at every point is the same frozen-branch target as `Z_fit`,
evaluated directly in the fixed coordinate frame.  No surrogate target is
authorized in P72.

Guard weights are normalized so the total guard mass is one.  The guard
objective multiplier is frozen as

```text
alpha_guard = 1.0.
```

This means `Z_fit` and `Z_guard` have equal set-level weight in the augmented
least-squares objective, independent of their row counts.

### Audit Cloud

`Z_audit` is not used for coefficient selection.  It contains the existing
P69/P70 holdout and replay diagnostic clouds so the repaired path is tested
against the same failure scale:

| Time step | Audit channel | Construction | Seeds |
| --- | --- | --- | --- |
| 1 | holdout | `p69_step1_holdout_distinct_diagnostic_seed` | prior `7301`, process noise `7401` |
| 1 | replay | `p69_step1_replay_distinct_diagnostic_seed` | prior `7311`, process noise `7501` |
| 2 | holdout | `p69_step2_holdout_distinct_diagnostic_seed` | previous retained object, process noise `7402` |
| 2 | replay | `p69_step2_replay_distinct_diagnostic_seed` | previous retained object, process noise `7502` |

Audit line probes use nearest, median-distance, and farthest endpoints for
both holdout and replay channels, with duplicates removed, and the same
fractions `S`.  Audit endpoints and audit-line points are never appended to
the fit objective.

## Frozen Objective

Phase 4 may implement only this objective for the support-certified lane:

```text
min_theta
    sum_{z in Z_fit} w_fit(z) (h_theta(z) - y_fit(z))^2
  + alpha_guard * sum_{u in Z_guard} w_guard(u) (h_theta(u) - y_guard(u))^2
  + ridge * ||theta||_2^2 in the existing scaled-ridge coordinate convention.
```

Frozen values:

| Quantity | Value |
| --- | --- |
| `alpha_guard` | `1.0` |
| `ridge` | existing P70 value `1e-10` |
| shape penalty `rho` | `0.0` |
| derivative-energy penalty | not authorized |
| line-growth objective penalty | not authorized |
| Christoffel/leverage/oversampling weighting | not authorized |

The line probes affect the objective only through guard-line points.  Audit
line probes are admission diagnostics only.

## Frozen Scales And Thresholds

Let

```text
s_y = max(weighted_rms(y_fit on Z_fit), 1e-300)
s_fit_endpoint = max(max_abs(h_theta at the selected line-start fit endpoints), 1e-300)
```

All residuals must be finite.  Weighted RMS residuals use the normalized
weights for their own cloud.  Maximum residuals are pointwise absolute
residuals.  Line targets are evaluated directly at every line point.  Line
absolute values are checked against the fixed target scale `s_y`; line growth
is checked against each selected line-start fit prediction.  Therefore the
line ceiling cannot relax merely because unrelated on-fit predictions become
large.

| Gate | Frozen formula | Role |
| --- | --- | --- |
| Fit RMS residual | `fit_rms / s_y <= 10.0` | explanatory plus lower-gate requirement, not sufficient alone |
| Guard RMS residual | `guard_rms / s_y <= 10.0` | finite guard aggregate gate |
| Guard max residual | `max_guard_abs_residual <= R_max`, `R_max = 1e3 * s_y` | finite spike veto |
| Audit holdout RMS residual | `holdout_rms / s_y <= 10.0` | existing P70 normalized residual gate |
| Audit replay RMS residual | `replay_rms / s_y <= 10.0` | existing P70 normalized residual gate |
| Audit max residual | `max_audit_abs_residual <= R_max`, `R_max = 1e3 * s_y` | finite spike veto |
| Line absolute value | `max_abs_line_value <= G_max`, `G_max = 1e3 * s_y` | off-cloud growth veto that cannot loosen with fitted predictor blow-up |
| Line endpoint growth | for each pair, `max_abs_line_value <= 1e3 * max(abs(h_theta(z_start)), s_y, 1e-300)` | pairwise growth veto from fit endpoint toward guard/audit endpoint |
| Line residual | `max_line_abs_residual <= R_max` with direct target evaluation at every line point | off-cloud target mismatch veto |

The values `10.0`, `1e3`, and `1e-300` are frozen here.  The `10.0` value
inherits the P70 holdout/replay normalized residual gate.  The `1e3` max and
line ceilings are deliberately below the Phase 6h `1e6` off-cloud-growth
signature.  The line absolute-value ceiling is tied to the fixed target scale,
and the pairwise growth ceiling is tied only to the selected line-start fit
endpoint, so the observed failure pattern cannot pass by averaging or by
inflating unrelated fit predictions.

## Normalizer And Defensive-Mass Gates

Every admitted step must pass all finite normalizer checks:

| Quantity | Frozen gate |
| --- | --- |
| mixture normalizer | finite and strictly positive |
| square-root-square normalizer | present, finite, and `> 1e-14` |
| defensive `tau` | present, finite, and strictly positive |
| defensive normalizer | present, finite, and strictly positive |
| fit mass fraction | `sqrt_square_normalizer / mixture_normalizer >= 1e-6`; absence of either quantity blocks |
| log transport normalizer | finite and `abs(log_transport_normalizer) <= 1e6` |

These gates reuse the P70 normalizer vocabulary but do not claim a
source-faithful theorem about the repaired guard design.

## Conditioning And Effective-Rank Gates

The local solver keeps the current objective-preserving scaled augmented ridge
convention:

```text
column_norm_j = sqrt(sum_i weight_i * A_ij^2)
scale_floor = max(sqrt(float64_eps) * max_j column_norm_j, column_scale_floor)
D_jj = max(column_norm_j, scale_floor)
A_bar = [sqrt(W) A D^{-1}; sqrt(ridge) I D^{-1}]
```

with `column_scale_floor = float64_eps` and the existing
`tensorflow.linalg.lstsq(fast=False)` backend.

Let singular values of `A_bar` be `sigma_1 >= ... >= sigma_p`.  The frozen
effective-rank convention is:

```text
rank_tol = max(1e-12 * sigma_1, 1e-300)
r_eff = count_j(sigma_j > rank_tol) / p
```

Admission requires:

```text
all singular values finite,
sigma_p > 0,
kappa(A_bar) = sigma_1 / sigma_p <= kappa_max,
kappa_max = 1e10,
r_eff = 1.0.
```

The old P70 `1e14` condition is retained only as a hard solver-veto reference
for compatibility and failure capture.  The P72 lower gate is stricter:
conditions in `(1e10, 1e14]` are not admitted even if the old solver would
have continued.

## Rank-Direction Activity Gate

The stored deterministic gauge activity check is frozen as the P70 channel
activity predicate:

```text
a_ref = max score of channel 0 across bonds
activity_threshold = max(1e-12, 1e-8 * a_ref)
minimum_active_bonds = ceil(0.25 * (target_dim - 1))
```

For every extra rank channel, the channel must be active on at least
`minimum_active_bonds`.  This is a fixed-variant guardrail, not a
gauge-invariant theorem and not a Zhao--Cui source-faithfulness claim.

## Support-Coverage Diagnostics

Support diagnostics are recorded for fit, guard, holdout, and replay clouds:
nearest-neighbor distances to `Z_fit`, fit leave-one-out distances, clipping
or coordinate-saturation fractions, point-any-saturated fractions, local
maximum absolute coordinate, and effective support of weights.

Admission blocks only if target construction fails, values are nonfinite, all
entries are clipped, or a required cloud is missing.  Clipping fraction
`>= 0.25`, large nearest-neighbor distance, or zero fit leave-one-out median is
recorded as a coverage warning, not by itself as proof of failure.  This keeps
Phase 6h's unresolved support/effective-support mechanism from becoming an
unsupported theorem.

## Phase 5 Pass/Block Semantics

The repaired lower gate passes only if all required rows and time steps satisfy
all mandatory gates:

1. branch identity is unchanged by diagnostics;
2. target hashes, frame hashes, shift constants, and cloud hashes are recorded;
3. fit, guard, holdout, replay, and line values are finite;
4. fit and guard RMS residual gates pass;
5. guard and audit maximum residual gates pass;
6. holdout and replay normalized residual gates pass;
7. line absolute value, growth, and residual gates pass;
8. normalizer and defensive-mass gates pass;
9. conditioning and effective-rank gates pass;
10. rank-direction activity gate passes;
11. no audit cloud is accidentally included in coefficient selection.

If any item fails, Phase 5 must report a blocked lower gate.  A blocked lower
gate is not evidence against Zhao--Cui's adaptive algorithm and is not a
downstream validation result.

## Threshold Freeze

The following are frozen before Phase 4 implementation and Phase 5 diagnostic
execution:

```text
guard seeds: step1 prior 7321, step1 process 7601, step2 process 7602
audit seeds: step1 holdout 7301/7401, step1 replay 7311/7501,
             step2 holdout 7402, step2 replay 7502
line fractions: (0.0, 0.25, 0.5, 0.75, 1.0)
line pair rule: nearest, median-distance, farthest, duplicates removed
line target rule: direct frozen-branch target evaluation at every line point
line absolute-value scale: s_y only
line pairwise growth scale: max(abs(start prediction), s_y, 1e-300)
alpha_guard: 1.0
ridge: 1e-10
rho_shape: 0.0
R_rms_rel: 10.0
R_max_rel: 1e3
G_max_rel: 1e3
normalizer sqrt-square floor: 1e-14
fit mass fraction floor: 1e-6
log normalizer absolute bound: 1e6
kappa_max: 1e10
hard compatibility condition-veto reference: 1e14
effective-rank relative tolerance: 1e-12
effective-rank floor: 1.0
support clipping warning threshold: 0.25
column scale floor: float64 eps
```

These values may not be changed in Phase 4 or Phase 5 after seeing repaired
outputs.  A later phase may propose a new threshold policy only by writing a
new reviewed plan and treating the old P72 result as not comparable.

## Source-Governance Labels

| Design element | Label |
| --- | --- |
| Broad TT/SIRT square-root route and normalizer role | `source_faithful` for broad route only, citing Phase 1 anchors |
| Frozen branch identity, ranks, bases, seeds, frame, and same scalar | `fixed_hmc_adaptation` |
| Column-scaled augmented ridge solve | `fixed_hmc_adaptation` |
| Guard cloud, guard objective, audit cloud, line probes, max residual gates | `extension_or_invention` |
| Rank-direction activity gate | `extension_or_invention` |
| P72 lower-gate pass/block table | `extension_or_invention` |
| Shape/stable-LS/Christoffel/leverage candidates | quarantined `SOURCE_GAP_BLOCKER` unless separately audited |

## Phase 3 Handoff

Phase 3 receives a design-only contract.  It may map this contract to code
surfaces and tests, but it may not edit production code.  Phase 3 must produce
an implementation-surface map and a Phase 4 implementation subplan.  Phase 4
may implement only surfaces authorized by Phase 3 and must preserve TensorFlow
/ TensorFlow Probability as the BayesFilter algorithmic backend.
