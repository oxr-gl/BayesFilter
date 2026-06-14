# P6 Result: Particle-Count And Seed Ladder

Date: 2026-05-29

## Decision

`STRUCTURED_BLOCKER_PARTICLE_COUNT_CALIBRATION_NOT_RUN`

## Evidence Contract Result

The first nonlinear-SSM ladder produced bounded seed rows for SV and structural
MLE smoke tests, but did not yet run a broader particle-count sweep.  Because
the structural phase showed a visible DPF-vs-CUT4 grid-MLE and gradient
difference, P6 is a structured blocker for estimator-equivalence claims.

## Calibration Evidence

| Phase | Parameter | Comparator grid MLE | DPF seed grid MLEs | SE-scaled median distance |
| --- | --- | ---: | --- | ---: |
| SV | `mu` | -1.0 | `[-1.0, -1.0, -1.0]` | 0.0 |
| Structural AR(1) | `b` | 0.65 | `[0.35, 0.5, 0.35]` | 1.196399784219709 |

## Calibration Implication

The SV smoke has seed-stable coarse-grid MLE agreement.  The structural smoke
has larger DPF-vs-CUT4 discrepancy and seed variability, so it should be the
first target for a real particle-count ladder before any stronger equivalence
language is used.

## Structured Blocker

No universal threshold is set.  The P4/P5 smoke ladder is too small to decide
final acceptance bands.  The next phase should add particle counts such as
`[48, 96, 192]`, preserve common random numbers, and estimate whether the
structural MLE distance shrinks with particle count.

## Verification

- JSON parse checks are recorded in P7.
- P4/P5 validate and reproducibility commands passed.

## Caveats

One-seed or small-grid behavior is not final equivalence.  No posterior
correctness, production readiness, DSGE/NAWM validation, or monograph claim is
concluded.
