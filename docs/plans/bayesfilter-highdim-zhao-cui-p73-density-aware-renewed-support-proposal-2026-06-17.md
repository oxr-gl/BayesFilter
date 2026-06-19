# P73 Proposal: Density-Aware Renewed-Support Fixed Fit

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE
predecessor_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md
predecessor_json: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json

## Purpose

This proposal explains the next repair direction after the P72 real Phase 5
diagnostic blocked.  The P72 runner/reporting bug has been repaired and Claude
agreed the closeout is a valid blocked diagnostic.  The remaining problem is
algorithmic: the fixed square-root TT fit does not produce a stable density on
finite diagnostic support.

The proposed P73 direction is to treat the failure as stale finite-support
overfit of a density object.  The repair should combine conservative
sample-renewal, strict train/guard/audit separation, and density-aware fitting
terms.  It should not begin by increasing rank.

## Evidence From P72

The P72 bounded diagnostic executed two real rows.

`rank_candidate_1_2_fit36`:

- step 1 blocks on line and residual gates;
- step 1 relative RMS residual is approximately `1.577e5`;
- step 1 relative max residual is approximately `8.526e5`;
- step 2 blocks on line, residual, and condition/effective-rank gates;
- step 2 maximum condition number is approximately `3.479e11`, above the P72
  admission threshold `1e10`;
- normalizer gates pass, so this branch is admissible but inaccurate and
  off-support unstable.

`rank_stronger_1_3_fit36`:

- step 1 blocks on normalizer, line, condition, and residual gates;
- step 1 relative RMS residual is approximately `1.314e7`;
- step 1 relative max residual is approximately `7.873e7`;
- step 1 maximum condition number is approximately `4.146e14`;
- the normalizer gate records `NORMALIZER_FLOOR_EXCEEDED`;
- step 2 is correctly skipped because no admissible retained object exists.

This evidence rejects a simple "increase rank" repair.  Rank 3 is worse than
rank 2 under the current one-shot finite support construction.

## Mathematical Diagnosis

The current fixed fit is a supervised square-root regression on a small finite
cloud:

```text
min_theta sum_{i in F} w_i (h_theta(z_i) - y_i)^2,
```

where `y_i` is a shifted square-root target value.  But the sequential object
needed by the filter is the normalized density

```text
q_theta(z) = (h_theta(z)^2 + tau q_0(z)) / Z_theta,
Z_theta = int h_theta(u)^2 du + tau int q_0(u) du.
```

Small or moderate error on the finite fit cloud does not imply:

- admissible `Z_theta`;
- useful mass allocation by `q_theta`;
- stable line behavior between fit and diagnostic points;
- stable retained density for the next filtering step;
- well-conditioned local ALS systems.

The P72 failures are therefore consistent with stale finite-design overfit:
the fit cloud is too small and too static for the density task.  The fitted
square-root function can behave badly away from the original cloud and can
collapse as a density object.

## Relation To NeuTra Training

NeuTra-style flow training does not rely on one permanent finite cloud.  Its
Monte Carlo objective is evaluated on newly generated samples during training.
As heuristic motivation, that renewal is intended to reduce dependence on one
stale point set.  P73 does not claim this NeuTra behavior transfers without a
separate technical audit.

P73 should borrow this idea conservatively.  The TT/ALS fit need not draw
fresh points at every core update.  However, it should not certify a density
from one fixed tiny cloud.  It should use staged renewal:

```text
F_0 -> fit h_0 -> guard/audit/line diagnostics
F_1 = F_0 union selected guard/enrichment points union new target-relevant points
fit h_1 -> fresh untouched audit diagnostics
```

The binding rule is:

```text
Never certify on points just added to training.
```

Guard or line failures may be used to enrich a later training cloud, but a
fresh audit cloud must be kept out of coefficient selection.

## Proposed Repair Elements

### 1. Staged Sample Renewal

For renewal round `r`, maintain separate sets:

- `F_r`: points used for coefficient fitting;
- `G_r`: guard/enrichment points allowed to influence the next fit only after
  the current diagnostic is closed;
- `A_r`: audit points never used for coefficient fitting in the same round;
- `L_r`: line-probe points used for diagnostics and possibly later
  enrichment only under recorded provenance.

The next training set may include old fit points, selected failed guard/line
points, and new independent target-relevant points:

```text
F_{r+1} = F_r union E_r union N_{r+1}.
```

Here `E_r` is a recorded enrichment subset and `N_{r+1}` is a genuinely new
sample cloud.  The next audit cloud `A_{r+1}` must be independent of
`F_{r+1}`.

### 2. Density-Aware Objective Terms

The fitting objective should continue to include square-root regression, but
it should also include a density-aware term that sees `q_theta`, not only
`h_theta`:

```text
L(theta) =
  sum_{i in F_r} w_i (h_theta(z_i) - y_i)^2
  + lambda_ce [ - sum_{j in C_r} alpha_j log q_theta(z_j) ]
  + lambda_line L_line(theta)
  + lambda_cond R_cond(theta).
```

`C_r` is a fitting or enrichment cloud, not the same-round audit cloud.  The
cross-entropy term may be read as an empirical forward-KL component when
`alpha_j` approximates target mass.  This term should be opt-in and reviewed
before becoming a default.

The log density uses

```text
log q_theta(z) =
  log(h_theta(z)^2 + tau q_0(z)) - log Z_theta.
```

This directly penalizes missing target-important points and normalizer
collapse.  It is closer to the density task than pointwise square-root
regression alone.

### 3. Guarded Certification

Promotion must not use training loss.  A renewed-support fit can only pass a
bounded lower gate if fresh heldout diagnostics pass:

- fit, guard, holdout, and replay residual gates;
- line-probe gates;
- normalizer gate, including `NORMALIZER_FLOOR_EXCEEDED`;
- condition/effective-rank gate;
- rank-activity gate;
- provenance gate proving audit exclusion.

### 4. Rank Policy

Do not increase rank first.  Use rank changes only after discriminating:

- stale-cloud overfit;
- sample adequacy;
- density-aware objective effect;
- conditioning and singular spectra;
- normalizer stability.

## Governance Classification

This proposal is not a source-faithful adaptive Zhao--Cui claim.

Preliminary classifications:

| Operation | Classification | Reason |
| --- | --- | --- |
| Broad squared TT/SIRT density route | `fixed_hmc_adaptation` | It preserves the broad existing fixed-variant route already documented in P72; any source-faithful subclaim still requires explicit paper and author-source anchors. |
| Staged sample renewal | `extension_or_invention` unless later anchored | It is inspired by NeuTra-style training discipline, not yet tied to Zhao--Cui source anchors. |
| Empirical cross-entropy / forward-KL fitting term | `extension_or_invention` | It changes the fixed-fit objective and must not be called source-faithful. |
| Guard/audit/line certification | `extension_or_invention` | P72 already classified these gates as fixed-variant stabilization additions. |
| Strict audit exclusion | fixed-variant safety requirement | It preserves claim discipline for differentiable fixed-HMC use. |

## Root-Cause Hypotheses To Test

P73 should test the following hypotheses in order:

1. Stale finite cloud overfit: new independent support reduces residual and
   line failures.
2. Sample inadequacy: larger fit/guard/audit counts stabilize rank 2 without
   increasing rank.
3. Density-object mismatch: a density-aware term reduces normalizer and line
   failures more than square-root regression alone.
4. Conditioning bottleneck: support renewal and density-aware terms improve or
   worsen singular spectra and effective ranks.
5. Rank/degree insufficiency: rank/degree changes only after the first four
   hypotheses are tested.

## Nonclaims

This proposal does not claim:

- that P72 is repaired;
- that P73 will pass the lower gate;
- d18 validation;
- HMC readiness;
- scaling;
- rank/degree promotion;
- source-faithful adaptive Zhao--Cui parity;
- that NeuTra results transfer automatically to TT/SIRT density fitting.

## Proposed Next Planning Step

Create a P73 master program that first reviews this proposal, then designs a
mathematical and implementation plan for staged renewed-support
density-aware fitting.  Implementation should not launch until the proposal,
master program, and visible runbook have passed read-only Claude review and
the user approves launch.
