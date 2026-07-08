# Reset Memo: Geometry-Scaled HMC Budget/Timing Policy

Date: 2026-07-07

BayesFilter HMC tuning now has a central serious/default policy,
`HMCGeometryScaledBudgetTimingPolicy`, for sample budgets, bootstrap screen
counts, and emergency staged timeout caps.  The policy uses parameter dimension,
condition number, effective dimension/anisotropy, and regularization pressure.
Emergency caps are safety rails only; meaningful progress is a separate monitor
concept.

The promoted HMC algorithm remains fixed-trajectory HMC:

1. mass matrix from posterior/pilot covariance;
2. SPD/diagonal regularization;
3. grid over `L`;
4. tune epsilon for each `L`;
5. select `(L, epsilon)` using finite, acceptance, trajectory-window, and veto checks;
6. repair `L` grid if edge-hit;
7. final local `L` grid;
8. freeze `(L, epsilon)`, update mass moderately, and repeat only while meaningful repair progress exists.

NUTS is not used for CCMA/TensorFlow tuning.  NUTS remains reference/diagnostic
only in documentation.

Important repair from review: public final handoffs are non-replayable and must
not expose `step_size`, `num_leapfrog_steps`, trajectory length, mass arrays,
raw samples, final states, candidate grids, or private paths.  Private BayesFilter
loop payloads may still contain the mechanics needed for BayesFilter-owned frozen
kernel replay.

CCMA integration now requires BayesFilter `HMCGeometryScaledBudgetTimingPolicy`
for the `phase4y` staged timeout path.  MacroFinance no longer constructs a
local fallback staged-timeout policy for that promoted path.

Do not claim CCMA tuning success, posterior convergence, sampler superiority,
GPU readiness, scientific validity, or default readiness from this repair.  The
next justified action is a small public-path CCMA smoke that verifies policy use
and artifact redaction on the actual target before any long tuning run.
