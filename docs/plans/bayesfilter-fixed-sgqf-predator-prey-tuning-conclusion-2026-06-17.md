# Fixed-SGQF Predator-Prey Tuning Conclusion

metadata_date: 2026-06-17
status: EXECUTION_COMPLETE

## Scope

This note ties together the current lower-rung predator-prey same-target
comparison evidence for:
- fixed SGQF vs dense reference,
- UKF vs dense reference,
- fixed SGQF vs UKF,
- and the fixed-SGQF sparse-level budget ladder.

It is a compact local conclusion note, not a production or literature-promotion
artifact.

## Core findings

### 1. SGQF and UKF are both far from the dense same-target reference on predator-prey
On the tested lower-rung predator-prey T20 row, both Gaussian closure routes are
far from the dense same-target target in both value and score.

Current dense-anchored value gaps:
- SGQF total log-likelihood abs gap: `48.6954153653`
- UKF total log-likelihood abs gap: `48.6929022242`

Current dense-anchored score gaps:
- SGQF score L2 gap: `294.7448183692`
- UKF score L2 gap: `294.7320018316`

### 2. SGQF and UKF are extremely close to each other
Despite both being far from the dense reference, they are extremely close to one
another on the same target.

This strongly suggests the dominant limitation is shared by the Gaussian closure
class rather than being a uniquely SGQF-specific failure.

### 3. SGQF’s internal gradient is still very strong
The SGQF analytic score remains highly consistent with centered finite
differences of the same SGQF scalar on the accepted branch.

So the gradient code appears internally correct for the SGQF surrogate objective,
even though that surrogate objective is not close to the dense target.

### 4. Increasing SGQF budget helps only from level 1 to level 2
Predator-prey SGQF sparse-level ladder summary:
- level 1 is much worse,
- level 2 is substantially better,
- levels 3 and 4 do not materially reduce the value or score gap further.

So for this target:
- more SGQF budget helps at the very low end,
- but after level 2, increasing sparse level does not rescue the mismatch.

## Practical interpretation

The current predator-prey evidence supports the following local conclusion:

> On the literature-backed predator-prey lower-rung same target, fixed SGQF is a
> valid deterministic Gaussian closure route with internally consistent
> fixed-branch gradients, but its remaining value/score gap to the dense target is
> not primarily a sparse-level budget problem once level 2 is reached. The gap is
> more plausibly dominated by the Gaussian assumed-density closure itself, and UKF
> exhibits essentially the same limitation on this row.

## What this does not conclude
- no production predator-prey SGQF claim,
- no universal SGQF vs UKF ranking claim,
- no general sparse-level theorem,
- no HMC readiness claim,
- no broader family generalization.

## Most useful next step
If future work continues on fixed SGQF for literature-backed nonlinear rows, the
most useful next direction is not to raise sparse level again on this predator-
prey target. Instead, it is to:
- test another literature-backed family,
- or change approximation class / target representation rather than just cloud
  budget.
