# Fixed-SGQF Predator-Prey Dense Score Result

metadata_date: 2026-06-17
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-predator-prey-dense-score-plan-2026-06-17.md`
status: EXECUTION_COMPLETE

## Question

On the same predator-prey lower-rung target, how far are fixed-SGQF and UKF in
both value and score from the same-target dense lower-rung reference?

## Implemented changes

Updated:
- `tests/highdim/test_p47_predator_prey_filtering.py`

Added:
1. `_dense_value_and_score(...)`
   - same-target dense predator-prey lower-rung scalar differentiated by
     `tf.GradientTape()`.
2. fixed-SGQF score gap to dense score check.
3. UKF score gap to dense score check.
4. fixed-SGQF vs UKF score-gap finiteness check.

This pass intentionally keeps the dense score work local to the predator-prey
lower-rung test file. It does not automatically upgrade the broader benchmark
registry’s predator-prey gradient exposure policy.

## Verification run

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_predator_prey_filtering.py \
  tests/highdim/test_p44_predator_prey_diagnostic.py \
  tests/highdim/test_p51_predator_prey_production_tuning.py
```

Observed:
- `30 passed, 2 warnings`

## What this establishes

### Dense score oracle now exists locally
The predator-prey lower-rung file now contains a same-target dense value-and-
score helper, so we can finally talk about:
- fixed-SGQF score vs dense score,
- UKF score vs dense score,
not just each route’s FD-vs-own-scalar agreement.

### Current dense score gaps
Current predator-prey lower-rung same-target dense score values are:
- dense score = `[63.2629826921, 0.4320242887, 0.0296691107, -6.4331684236, -1.2031391144, 1.7386637941]`
- fixed-SGQF score = `[-228.5586021961, -1.7897008287, -0.1500241149, 32.1717015428, 7.3157370606, -10.3772332137]`
- UKF score = `[-228.5460136536, -1.7895814737, -0.1500173639, 32.1706547783, 7.3131302703, -10.3738390828]`

Componentwise score gaps versus the dense score:

| Parameter | Dense score | SGQF score | UKF score | SGQF abs gap | UKF abs gap | SGQF rel gap | UKF rel gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `r` | `63.2629826921` | `-228.5586021961` | `-228.5460136536` | `291.8215848881` | `291.8089963457` | `4.6128331683` | `4.6126341808` |
| `K` | `0.4320242887` | `-1.7897008287` | `-1.7895814737` | `2.2217251174` | `2.2216057624` | `2.2217251174` | `2.2216057624` |
| `a` | `0.0296691107` | `-0.1500241149` | `-0.1500173639` | `0.1796932255` | `0.1796864746` | `0.1796932255` | `0.1796864746` |
| `s` | `-6.4331684236` | `32.1717015428` | `32.1706547783` | `38.6048699664` | `38.6038232019` | `6.0009108148` | `6.0007481011` |
| `u` | `-1.2031391144` | `7.3157370606` | `7.3131302703` | `8.5188761751` | `8.5162693848` | `7.0805412880` | `7.0783746306` |
| `v` | `1.7386637941` | `-10.3772332137` | `-10.3738390828` | `12.1158970078` | `12.1125028768` | `6.9685105591` | `6.9665584100` |

Normwise score gaps versus the dense score:

| Comparator | Absolute norm gap | Relative norm gap |
| --- | ---: | ---: |
| Fixed-SGQF vs dense score | `294.7448183692` | `4.6324697146` |
| UKF vs dense score | `294.7320018316` | `4.6322682786` |

Interpretation:
- fixed-SGQF and UKF scores are extremely close to **each other** on this tested
  lower-rung predator-prey closure,
- but both are very far from the dense same-target score,
- so the current result is not a dense-gradient success for either Gaussian
  closure route.

### Scope remains careful
This pass does **not** yet promote the predator-prey gradient to benchmark-grade
reference-gradient status in the broader registry stack. It establishes that the
local dense score comparison is computationally available and finite under the
same lower-rung target.

## Supported claims
1. Predator-prey now has a same-target dense lower-rung score oracle in the test
   suite.
2. Fixed-SGQF and UKF can both be compared to that dense score locally.
3. The repo can now distinguish:
   - SGQF internal FD consistency,
   - UKF local route gradient behavior,
   - and each method’s gap to the dense same-target score.

## Not supported by this pass
1. No benchmark-grade predator-prey reference-gradient promotion in the broader
   registry stack.
2. No production or HMC claim.
3. No broader family admission claim.

## Interpretation

This closes an important evidence gap: until now, SGQF and UKF predator-prey
scores could only be judged against their own internal FD consistency. After
this pass, a same-target dense lower-rung score oracle exists and can be used to
measure how far each route’s score is from the dense target.

That makes the next discussion about “why SGQF differs from Zhao-Cui” much more
concrete on the gradient side.
