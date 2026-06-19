# Zhao-Cui Fixed Variant: Mathematical Fitting Correction

metadata_date: 2026-06-19
status: MATHEMATICAL_HANDOFF_FOR_DOCUMENTATION
scope: mathematical explanation, not coding governance
related_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
phase8_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-result-2026-06-18.md
phase9_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md

## Purpose

This note records the mathematical correction to the Zhao-Cui fixed-variant
fitting lane.  It is intended for the documentation agent.  It explains what
was wrong in the earlier fitting/evaluation logic, what density objective we
should use, how UKF warm-started mini-batch fitting now fits into the story,
and what Phases 8 and 9 actually established.

This note is not a claim that the Zhao-Cui paper algorithm has been faithfully
implemented.  The fixed variant remains an extension/invention unless a later
source-anchored document proves otherwise.  This note also does not claim
lower-gate repair, validation readiness, HMC readiness, scaling, or final
fit-quality success.

## Density Model

The fixed variant represents a nonnegative unnormalized density by

\[
  q_\theta(z)=h_\theta(z)^2+\tau q_0(z),
\]

where:

- \(h_\theta\) is the trainable square-root TT function;
- \(q_0\) is a defensive reference density;
- \(\tau>0\) is a small defensive mixture weight;
- \(z\) denotes the local/reference coordinate used by the fixed variant.

The normalizing constant is

\[
  Z_\theta=\int q_\theta(z)\,dz,
\]

and the normalized model density is

\[
  p_\theta(z)=\frac{q_\theta(z)}{Z_\theta}.
\]

The target object in the fixed variant is a density proportional to the square
of a target square-root value \(s(z)\):

\[
  p_\star(z)\propto s(z)^2.
\]

Therefore the primary mathematical fitting and evaluation target is a density
objective, not an ordinary square-root regression objective.

## Correct Density Objective

The natural cross-entropy objective against the target density is

\[
  \mathcal L(\theta)
  =
  -\mathbb E_{p_\star}\bigl[\log p_\theta(z)\bigr].
\]

Using \(p_\theta(z)=q_\theta(z)/Z_\theta\), this becomes

\[
  \mathcal L(\theta)
  =
  -\mathbb E_{p_\star}\bigl[\log q_\theta(z)\bigr]
  + \log Z_\theta .
\]

For a quadrature or Monte Carlo batch

\[
  B=\{(z_i,w_i,s_i)\}_{i=1}^n,
\]

where \(w_i\) are integration or empirical weights and \(s_i=s(z_i)\), the
target-only empirical measure should be

\[
  \alpha_i^\star
  =
  \frac{w_i s_i^2}{\sum_j w_j s_j^2}.
\]

The corresponding empirical density cross-entropy is

\[
  \widehat{\mathcal L}_B(\theta)
  =
  -\sum_i \alpha_i^\star \log q_\theta(z_i)
  + \log Z_\theta .
\]

This is the corrected heldout metric implemented in Phase 8 and smoke-tested
in Phase 9.

## What Was Wrong Before

The earlier fitting/evaluation logic mixed together three mathematically
different objects.

### Square-Root Regression Was Treated Too Seriously

The old diagnostics often treated

\[
  h_\theta(z_i)\approx s_i
\]

as if it were the primary success criterion.

That is not the correct density criterion.  The model density depends on

\[
  h_\theta(z)^2+\tau q_0(z),
\]

so sign, scale, and local amplitude errors in \(h_\theta\) do not translate
cleanly into density quality.  A square-root residual may be large while the
density shape is less damaged, or a square-root residual may look acceptable
while the normalized density is poor.  Square-root residuals are therefore
secondary diagnostics only.

### The Old Helper Mixed The Target With The Defensive Density

The historical helper used weights of the form

\[
  \alpha_i^{\rm old}
  \propto
  w_i\bigl(s_i^2+\tau q_0(z_i)\bigr).
\]

This includes the defensive component \(\tau q_0\) inside the empirical target
weights.  That may be useful as an internal training-support convention, but
it is not the scientific heldout target.  The heldout target should be based
on \(s_i^2\) alone:

\[
  \alpha_i^{\rm hold}
  =
  \frac{w_i s_i^2}{\sum_j w_j s_j^2}.
\]

Thus the old helper can remain as historical training behavior, but it must
not be used as the primary heldout metric.

### Failed Initializations Were Revisited As If They Were Live Baselines

Several earlier ladders revisited initialization routes that had already
failed for this fixed-variant fitting problem:

\[
  \text{random},\qquad
  \text{calibrated constant},\qquad
  \text{source-route prefit}.
\]

These did not solve the high-dimensional geometry problem.  The fixed variant
needs an initialization that places mass in a meaningful local region before
mini-batch density fitting can be interpreted.  The remaining hypothesis is a
UKF-guided warm start.

## Current Mathematical Fitting Picture

The current intended fitting and testing picture has four parts.

### 1. UKF As A Geometric Scout

The UKF is not treated as truth.  It is used as a geometric scout.  It provides
approximate local Gaussian information,

\[
  m,\Sigma,
\]

which defines a local coordinate frame.  Schematically, one may write a local
coordinate relation as

\[
  z = A^{-1}(x-m),
\]

where \(A\) is derived from the covariance information.  The point is to build
and initialize the fixed-variant TT representation in a coordinate system that
is adapted to the likely mass region.

### 2. UKF-Guided Initialization Of \(h_\theta\)

The trainable square-root TT \(h_\theta\) should be initialized using the
UKF-guided shape and frame.  The initialization should not be random, constant,
or source-prefit unless a new reviewed mathematical reason is given.  The goal
is only to start the density model in a reasonable geometric region:

\[
  q_\theta(z)=h_\theta(z)^2+\tau q_0(z).
\]

This does not by itself prove fit quality.

### 3. Mini-Batch Density Fitting

Training should use mini-batches rather than a tiny fixed sample.  For a
mini-batch \(B_t\), the density objective has the form

\[
  \widehat{\mathcal L}_{B_t}(\theta)
  =
  -\sum_{i\in B_t}\alpha_{i,t}\log q_\theta(z_{i,t})
  +\log Z_\theta .
\]

The empirical target weights should be derived from the target square-root
values:

\[
  \alpha_{i,t}
  =
  \frac{w_{i,t}s_{i,t}^2}{\sum_{j\in B_t}w_{j,t}s_{j,t}^2}.
\]

The practical reason for mini-batches is also important.  The fixed variant
has hundreds of free TT parameters even in moderate settings.  A tiny fixed
sample cannot adequately determine a high-dimensional density.  Fresh or
rotating mini-batches are needed to reduce overfitting to a small point set and
to expose the optimizer to enough target geometry.

### 4. Corrected Heldout Testing

Heldout or audit testing should use the target-only density cross-entropy:

\[
  \widehat{\mathcal L}_{\rm hold}(\theta)
  =
  -\sum_i \alpha_i^{\rm hold}\log q_\theta(z_i)
  +\log Z_\theta,
\]

with

\[
  \alpha_i^{\rm hold}
  =
  \frac{w_i s_i^2}{\sum_j w_j s_j^2}.
\]

This is separated from the historical helper

\[
  \alpha_i^{\rm old}
  \propto
  w_i\bigl(s_i^2+\tau q_0(z_i)\bigr).
\]

The old helper is a boundary comparator or internal training-support object,
not the heldout target.

## What Phase 8 Established

Phase 8 implemented the corrected heldout metric surface.

Mathematically, it added an opt-in way to compute

\[
  \alpha_i^{\rm hold}
  =
  \frac{w_i s_i^2}{\sum_j w_j s_j^2}
\]

and

\[
  \widehat{\mathcal L}_{\rm hold}(\theta)
  =
  -\sum_i\alpha_i^{\rm hold}\log q_\theta(z_i)
  + \log Z_\theta .
\]

The implementation deliberately separates the heldout metric batch from the
training batch.  It also records metric role and provenance.  This separation
matters mathematically because a heldout empirical target measure should not
silently become a training batch or a stopping/tuning batch.

Phase 8 did not prove that a fitted model is good.  It only established that
the corrected heldout metric surface exists and is mechanically tested.

## What Phase 9 Established

Phase 9 tested the corrected metric on a deterministic manual fixture.  The
fixture used four points, target square-root values

\[
  s=(0,0.5,1,2),
\]

weights

\[
  w=(1,2,1.5,0.5),
\]

and \(\tau=2.5\) with \(q_0(z_i)=1\).

The corrected target-only weights are

\[
  w_i s_i^2=(0,0.5,1.5,2),
\]

so

\[
  \alpha^{\rm hold}=(0,0.125,0.375,0.5).
\]

The historical helper boundary-only weights are

\[
  w_i(s_i^2+\tau q_0(z_i))
  =
  (2.5,5.5,5.25,3.25),
\]

so

\[
  \alpha^{\rm old}
  =
  (2.5,5.5,5.25,3.25)/16.5.
\]

The smoke verified that these two alpha vectors are different, and that the
corrected metric is using the target-only vector.  It also verified that the
heldout cross-entropy reconstructed exactly from the JSON artifact:

\[
  \widehat{\mathcal L}_{\rm hold}
  =
  -\sum_i\alpha_i^{\rm hold}\log q_\theta(z_i)
  +\log Z_\theta .
\]

The Phase 9 smoke is therefore evidence that the corrected metric wiring and
artifact reporting are right.  It is not evidence that the real fitted density
is accurate.

## Remaining Mathematical Question

The remaining question is no longer whether the heldout metric is the old
\(\tau q_0\)-smoothed helper.  That has been separated.

The next mathematical question is:

Can UKF-warm-started mini-batch training reduce the corrected heldout density
cross-entropy on genuine generated heldout samples?

Answering that requires a new reviewed phase with:

- generated train/validation/heldout samples;
- enough samples relative to TT parameter count;
- predeclared learning rate and optimizer settings;
- predeclared stopping and tuning rules;
- no audit leakage;
- corrected heldout density cross-entropy as the primary evaluation metric;
- square-root residuals as secondary diagnostics only.

Until such a phase succeeds, the current state should be described as a
mathematical evaluation-surface repair, not a completed fitting success.

## Documentation Guidance

When this is moved into the mathematical document, the safe narrative is:

1. The fixed variant models a density through
   \(q_\theta=h_\theta^2+\tau q_0\).
2. The target density is proportional to \(s^2\), so heldout testing should use
   \(\alpha_i\propto w_i s_i^2\).
3. The previous \(\alpha_i\propto w_i(s_i^2+\tau q_0)\) helper is not the
   heldout target.
4. Square-root residuals are not the primary density metric.
5. UKF information is used as a geometric warm start, not as truth.
6. Phases 8 and 9 repaired and smoke-tested the metric surface.
7. Real fitting success remains to be demonstrated by a later mini-batch
   training and corrected-heldout evaluation phase.
