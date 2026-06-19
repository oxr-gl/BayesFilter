# P73 Phase 2 Result: Density-Aware Renewal Design Contract

metadata_date: 2026-06-17
status: PHASE2_PASSED_CLAUDE_R2_AGREE_READY_FOR_PHASE3_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-subplan-2026-06-17.md

## Evidence Contract

| Field | Result |
| --- | --- |
| Scientific/engineering question | What exact mathematical contract should P73 implement for a renewed-support fixed fit, and how should the optional density-aware term be treated before diagnostics? |
| Exact baseline/comparator | P72 real Phase 5 blocked diagnostic, its JSON artifact, and the Phase 1 classification ledger: `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md`, `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json`, and `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md`. |
| Primary pass/fail criterion | This result must freeze renewal sets, objective terms, objective weights, audit exclusion, gates, thresholds, provenance predicates, and next-phase handoff without implementation or diagnostic execution. |
| Veto diagnostics | Same-round audit points admitted to coefficient selection; certification on points just added to training; source-faithfulness overclaim; vague thresholds; training loss promoted to success; density-aware objective made default; rank promotion before renewal/objective hypotheses are tested. |
| Explanatory only | Training loss, cross-entropy loss, fit-cloud residuals, support distances, singular spectra, runtime estimates, and NeuTra analogy. |
| What will not be concluded | No implementation correctness, no P73 lower-gate pass, no validation, no HMC readiness, no scaling claim, no rank promotion, and no adaptive Zhao--Cui source-faithfulness parity. |
| Artifact preserving result | This Phase 2 result, the Phase 3 subplan, the execution ledger, and the Claude review ledger. |

## Skeptical Plan Audit

Phase 2 passes the skeptical audit for a design-only execution.  The baseline is
the actual P72 Phase 5 blocked diagnostic, not a smoke result or schema
artifact.  The primary criterion is a frozen mathematical contract, not a proxy
metric such as training loss.  The plan forbids implementation, Python
diagnostics, GPU work, validation, HMC, scaling, and rank promotion.  It also
keeps the density-aware term opt-in and evidence-bound rather than converting
it into a default policy.

The main hidden-assumption risk is that a new support cloud can be mistaken for
a proof of continuum accuracy.  The contract below prevents that mistake:
finite clouds may nominate or veto a branch, but only the stated fresh-audit
gates decide the lower-gate result.

## Imported Boundary From Phase 1

The Phase 1 classification ledger is binding here.

| Design element | Classification used in P73 | Phase 2 consequence |
| --- | --- | --- |
| Broad squared TT/SIRT density route and positive normalizer role | `fixed_hmc_adaptation` of the source route | P73 may retain \(h_\theta^2\), the defensive component, and normalizer diagnostics, but this does not make P73 renewal source-faithful. |
| Author random/adaptive sampling and enrichment machinery | `source_faithful` route context only | It motivates the concern that one stale finite cloud is not the author route, but it does not anchor the P73 four-set protocol. |
| Renewal sets \(F_r,G_r,A_r,L_r\) | `extension_or_invention` | They are admitted as BayesFilter fixed-variant repair machinery with strict provenance. |
| Empirical cross-entropy / forward-KL objective | `extension_or_invention` | It may be included only as an opt-in diagnostic arm with frozen weight and no source-faithfulness claim. |
| Guard/audit/line certification and strict audit exclusion | `extension_or_invention` | They are mandatory evidence safeguards for P73. |
| Normalizer and defensive-mass gates | `fixed_hmc_adaptation` for the broad retained-density role; P73 finite thresholds are `extension_or_invention` | The normalizer semantics are inherited, but the exact admission thresholds remain fixed-variant gates. |
| Conditioning, effective-rank, and rank-activity gates | `extension_or_invention` | They remain veto gates because P72 failed them, not because Zhao--Cui proves these thresholds. |
| NeuTra analogy | `extension_or_invention` and survey context only | It may motivate sample renewal but supplies no theorem for P73. |
| UKF scouting | `fixed_hmc_adaptation` if used | It may guide fixed branch construction, but it is not a truth oracle and is not added by Phase 2. |

No row in this table authorizes the phrase "source-faithful P73 repair."

## P72 Comparator Facts To Preserve

The P72 diagnostic is the comparator for Phase 5.

| Row | P72 status | Binding lesson |
| --- | --- | --- |
| `rank_candidate_1_2_fit36`, step 1 | Residual and line gates failed; relative RMS approximately `1.577e5`; relative max approximately `8.526e5`; normalizer and condition passed | Rank 2 is admissible but inaccurate and unstable away from the fitted support. |
| `rank_candidate_1_2_fit36`, step 2 | Residual, line, and condition gates failed; max condition approximately `3.479e11 > 1e10` | A branch that passes step 1 normalizer can still produce an unusable next-step fit. |
| `rank_stronger_1_3_fit36`, step 1 | Residual, line, condition, and normalizer gates failed; `NORMALIZER_FLOOR_EXCEEDED`; condition approximately `4.146e14` | Increasing rank first worsened the finite fixed variant. |
| `rank_stronger_1_3_fit36`, step 2 | Skipped because no retained object was admissible | A downstream step must not pretend that a blocked retained object exists. |

Therefore the first P73 diagnostic must keep rank fixed at the P72 candidate
rank and test renewal/objective hypotheses before any rank promotion.

## Fixed Target And Density Object

Let \(\pi(z)\) denote the unnormalized frozen-branch target density in the
local coordinate frame for the current filtering step.  Let \(c\) be the fixed
stability shift already associated with that branch.  The square-root target is

```text
y(z) = exp(-0.5 * ( -log pi(z) - c )).
```

The fitted square-root tensor is \(h_\theta(z)\).  Let \(q_0(z)\) be the fixed
defensive reference density and let \(\tau>0\) be the fixed defensive weight.
With respect to the branch measure \(\mu\), define

```text
q_\theta(z) = (h_\theta(z)^2 + tau * q_0(z)) / Z_\theta,
Z_\theta = int (h_\theta(u)^2 + tau * q_0(u)) dmu(u).
```

The log density used by the optional density-aware arm is

```text
log q_\theta(z)
  = log(max(h_\theta(z)^2 + tau * q_0(z), eps_log))
    - log(max(Z_\theta, eps_log)),
eps_log = 1e-300.
```

The `eps_log` floor is a numerical guard only.  It does not rescue a branch
from the normalizer gate: if \(Z_\theta\), the square-root-square normalizer,
or the defensive normalizer fails a frozen gate, the branch blocks.

## Renewal Sets

P73 uses finite renewal rounds \(r=0,1,\ldots,R\).  The first bounded
diagnostic uses exactly one renewal, \(R=1\).  Additional renewals are
`deferred` until Phase 5 reports whether one renewal discriminates the P72
failure mechanism.

For each row and time step, define:

| Set | Meaning | Coefficient-selection role | Certification role |
| --- | --- | --- | --- |
| \(F_r\) | Fit cloud for renewal round \(r\). | Used for coefficient selection in round \(r\). | Never by itself certifies success. |
| \(G_r\) | Guard/enrichment cloud generated for round \(r\). | Not used for same-round coefficient selection unless its points have first entered a later \(F_{r+1}\). | Diagnostic only in round \(r\). |
| \(A_r\) | Fresh audit cloud for round \(r\). | Never used for coefficient selection in round \(r\), and never used to tune thresholds. | Required certification cloud. |
| \(L_r\) | Line probes for round \(r\), split into guard-line and audit-line channels. | Guard-line failures may enter a later enrichment set; audit-line points remain audit-only. | Required line diagnostic. |
| \(E_r\) | Enrichment subset selected after round \(r\) is closed. | May enter \(F_{r+1}\). | Does not certify the round in which it was selected. |
| \(N_{r+1}\) | New independent target-relevant support for the next round. | May enter \(F_{r+1}\). | Does not certify the same round in which it first enters training. |

The renewal recursion is

```text
F_{r+1} = F_r union E_r union N_{r+1}.
```

The first certifiable P73 fit is the fit produced from \(F_1\), not the
intermediate round-0 fit.  \(A_1\) must be generated independently of
\(F_1\), \(E_0\), and \(N_1\).  \(L_1\) must include audit-line probes from
\(F_1\) to \(A_1\) endpoints.

Never certify on points just added to training.  In particular, \(E_0\) and
\(N_1\) may help fit \(h_{\theta,1}\), but certification of \(h_{\theta,1}\)
must use \(A_1\) and audit-line probes that are not in \(F_1\).

## Enrichment Rule

The round-\(r\) enrichment set \(E_r\) may contain only points from guard
channels, not audit channels:

```text
E_r subset G_r union L_r^guard.
```

A point may be selected for \(E_r\) only if, using the frozen P72 gates, it
belongs to one of these failure classes:

1. guard residual exceeds the RMS or max residual gate;
2. guard-line absolute value or guard-line residual exceeds the line gate;
3. the point is one of the nearest, median-distance, or farthest guard
   endpoints used to form a failed guard-line channel.

Audit points and audit-line points are excluded:

```text
E_r cap A_r = empty,
E_r cap L_r^audit = empty.
```

This rule lets P73 learn from guard failures while preserving an untouched
fresh audit.  It is `extension_or_invention`; it is not a Zhao--Cui
source-faithful rule.

## Objective Arms

P73 defines two implementation arms.  Both are opt-in relative to the broader
BayesFilter package, and neither changes the default filtering policy.

### P73-A: Renewal-Only Square-Root Regression

P73-A is the mandatory first implementation target.  It solves

```text
L_A(theta; r)
  = sum_{z_i in F_r} w_i * (h_theta(z_i) - y(z_i))^2
    + ridge * ||theta||_2^2
```

using the existing scaled-ridge convention inherited from P72.  Frozen values:

| Quantity | Value |
| --- | --- |
| `ridge` | `1e-10`, inherited from P72 |
| renewal count for first diagnostic | `R = 1` |
| first diagnostic rank/degree row | `rank_candidate_1_2_fit36` only |
| rank promotion | `deferred` |

P73-A asks whether renewed finite support alone reduces the P72 residual,
line, condition, and normalizer blockers.

### P73-B: Density-Aware Opt-In Diagnostic Arm

`DENSITY_AWARE_OBJECTIVE_STATUS: included_as_opt_in_diagnostic_arm`.

P73-B is included for Phase 3/4 planning as an opt-in diagnostic arm, not as a
default policy and not as a source-faithful Zhao--Cui claim.  It solves

```text
L_B(theta; r)
  = L_A(theta; r) + lambda_ce * L_ce(theta; r).
```

The empirical cross-entropy term is

```text
L_ce(theta; r) = - sum_{z_j in C_r} alpha_j * log q_\theta(z_j).
```

For the first P73 diagnostic,

```text
C_r = F_r,
alpha_j =
  w_j * (y(z_j)^2 + tau * q_0(z_j))
  / sum_{z_k in F_r} w_k * (y(z_k)^2 + tau * q_0(z_k)).
```

This is a finite empirical surrogate for a forward-KL density fit.  It is not
a theorem-level KL approximation in Phase 2.  Its purpose is to test whether
the fitted density \(q_\theta\), not merely the pointwise square root
\(h_\theta\), is improved on a renewed support.

Frozen values:

| Quantity | Value |
| --- | --- |
| `lambda_ce` | `0.1` |
| `eps_log` | `1e-300` |
| `lambda_line` | `0.0`; line penalties are `deferred` |
| `lambda_cond` | `0.0`; conditioning penalties are `deferred` |
| shape, derivative, Christoffel, leverage, and adaptive oversampling penalties | `quarantined` pending separate literature/source audit |

P73-B can only be called a candidate improvement if the fresh-audit downstream
gates pass.  A lower \(L_ce\), lower training loss, or prettier fit cloud is
explanatory only.

## Gates And Thresholds

P73 inherits the P72 lower-gate thresholds unless explicitly stated here.  No
threshold may be changed in Phase 4 or Phase 5 after seeing P73 outputs.

There are two different uses of guard information:

1. In round \(0\), guard and guard-line failures are enrichment signals.  They
   nominate \(E_0\) and do not certify or block the final renewed fit by
   themselves.
2. In round \(1\), a fresh guard cloud \(G_1\) and fresh guard-line probes are
   mandatory lower-gate checks alongside \(A_1\).  A round-1 guard residual,
   guard maximum residual, guard-line value, guard-line growth, or guard-line
   residual failure blocks the P73 row.

| Gate | Frozen P73 rule |
| --- | --- |
| Fit RMS residual | `fit_rms / s_y <= 10.0`; mandatory lower-gate requirement, but not sufficient for promotion |
| Fresh guard RMS residual | `guard_rms / s_y <= 10.0`; mandatory for round-1 lower-gate admission |
| Fresh audit RMS residual | `audit_rms / s_y <= 10.0` |
| Guard maximum residual | `max_guard_abs_residual <= 1e3 * s_y` |
| Fresh audit maximum residual | `max_audit_abs_residual <= 1e3 * s_y` |
| Guard-line absolute value, endpoint growth, and residual | P72 line gates; mandatory for round-1 guard-line probes, enrichment-only for round-0 guard-line probes |
| Audit-line absolute value, endpoint growth, and residual | P72 line gates; mandatory for round-1 audit-line probes |
| Mixture normalizer | finite and strictly positive |
| Square-root-square normalizer | present, finite, and `> 1e-14` |
| Defensive `tau` and defensive normalizer | present, finite, and strictly positive |
| Fit mass fraction | `sqrt_square_normalizer / mixture_normalizer >= 1e-6` |
| Log transport normalizer | finite and `abs(log_transport_normalizer) <= 1e6` |
| Condition number | `kappa(A_bar) <= 1e10` |
| Effective rank | `r_eff = 1.0` under P72 tolerance |
| Rank activity | P72 deterministic rank-channel activity predicate |
| Provenance | `NO_AUDIT_COEFFICIENT_SELECTION` must pass |

The scale \(s_y\) is inherited from P72:

```text
s_y = max(weighted_rms(y on the relevant fit cloud), 1e-300).
```

Training loss, \(L_ce\), and fit-cloud cross-entropy are never promotion
criteria.  Nonfinite values in these quantities may veto the arm that produced
them.

## Provenance Predicate

Each point admitted to any P73 cloud must carry:

```text
point_id,
cloud_hash,
role in {fit, guard, guard_line, audit, audit_line, enrichment, fresh},
created_round,
entered_training_round,
audit_round,
source_channel,
parent_point_ids,
seed_or_constructor_label.
```

Define `NO_AUDIT_COEFFICIENT_SELECTION(r)` to hold if and only if:

1. every point in the coefficient matrix for round \(r\) has
   `entered_training_round <= r`;
2. no point in the coefficient matrix has `role` equal to `audit` or
   `audit_line`;
3. no point in the coefficient matrix has `audit_round <= r`;
4. the coefficient-selection cloud hashes are disjoint from the same-round
   audit and audit-line cloud hashes;
5. every enrichment point records a guard or guard-line source channel, never
   an audit source channel.

If this predicate fails, the branch blocks with a provenance failure even if
all numerical residuals look good.

## Pass/Block Semantics

A P73 row and time step passes the lower gate only if all of the following hold
for the first renewed fit \(h_{\theta,1}\):

1. branch identity, shift, frame, rank, degree, basis, and retained-object
   identity are recorded;
2. \(F_1\), \(G_1\), \(A_1\), and \(L_1\) hashes are recorded and finite;
3. `NO_AUDIT_COEFFICIENT_SELECTION(1)` passes;
4. all fit, fresh-guard, fresh-audit, guard-line, and audit-line values are
   finite;
5. fit RMS residual passes;
6. fresh-guard RMS and maximum residual gates pass;
7. fresh-audit RMS and maximum residual gates pass;
8. guard-line gates pass on round-1 guard-line probes;
9. audit-line gates pass on round-1 audit-line probes;
10. normalizer and defensive-mass gates pass;
11. condition and effective-rank gates pass;
12. rank-activity gates pass;
13. no threshold was changed after P72 or P73 outputs.

If any item fails, the row blocks.  A P73 block is not evidence against the
adaptive Zhao--Cui algorithm; it is evidence about this fixed-variant repair.

## Initial Phase 5 Comparison Set

The first P73 bounded diagnostic must compare only against the P72 candidate
rank-2 row:

| Arm | Row | Role |
| --- | --- | --- |
| P72 comparator | `rank_candidate_1_2_fit36` | Historical blocked baseline. |
| P73-A | `rank_candidate_1_2_fit36`, one renewal, square-root objective | Mandatory renewal-only test. |
| P73-B | `rank_candidate_1_2_fit36`, one renewal, density-aware objective | Included opt-in diagnostic arm. |

The P72 rank-3 row remains a blocked comparator.  Retrying rank 3 in P73 is
`deferred` until the renewal-only and density-aware rank-2 hypotheses have
fresh-audit evidence.

## Phase 3 Handoff

Phase 3 receives this design contract and may only map it to implementation
surfaces and tests.  It may not edit production implementation code.

Phase 3 must preserve:

- P73-A as the mandatory first implementation target;
- P73-B as `included_as_opt_in_diagnostic_arm`, not default policy;
- `lambda_ce = 0.1`;
- `lambda_line = 0.0` and `lambda_cond = 0.0`;
- inherited P72 residual, line, normalizer, condition, effective-rank,
  rank-activity, and provenance thresholds;
- no rank promotion;
- no validation, HMC, scaling, or downstream filtering claims.

Phase 3 must write an implementation-surface map, a focused test plan, and a
Phase 4 implementation subplan before any code edits.
