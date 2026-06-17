# Fixed-SGQF Predator-Prey Budget Ladder Result

metadata_date: 2026-06-17
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-predator-prey-budget-ladder-plan-2026-06-17.md`
status: EXECUTION_COMPLETE

## Question

For the fixed predator-prey lower-rung same target, does increasing SGQF budget
(sparse level) improve value and score agreement against the same-target dense
reference?

## Verification run

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_predator_prey_filtering.py \
  tests/highdim/test_p44_predator_prey_diagnostic.py \
  tests/highdim/test_p51_predator_prey_production_tuning.py
```

Observed:
- `32 passed, 2 warnings`

## Fixed ladder settings

Held fixed across the ladder:
- `predictive_epsilon = 1e-10`
- `innovation_epsilon = 1e-10`
- `merge_tolerance = 1e-12`
- `zero_weight_tolerance = 1e-14`
- same observations
- same theta `(r, K, a, s, u, v)`
- same dense lower-rung reference order `7`

Varied:
- `sparse_level ∈ {1, 2, 3, 4}`

## Dense reference anchor

- dense total log-likelihood = `-16.4158538691`
- dense score L2 norm = `63.6258489595`

## SGQF budget ladder table

| Sparse level | Cloud point count | Total abs gap vs dense | Total rel gap vs dense | Step-0 abs gap | Step-0 rel gap | Score L2 gap vs dense |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | `151.7962931146` | `9.2469325279` | `104.2181659846` | `11.3685540781` | `645.8712844138` |
| 2 | 5 | `48.6954153653` | `2.9663650611` | `44.9596413994` | `4.9043860037` | `294.7448183692` |
| 3 | 17 | `48.6954536897` | `2.9663673957` | `44.9596777496` | `4.9043899689` | `294.7437096298` |
| 4 | 45 | `48.6954536901` | `2.9663673957` | `44.9596777498` | `4.9043899689` | `294.7437096319` |

## Interpretation

### What improves
The major improvement is from level 1 to level 2:
- total value gap drops substantially,
- first-step value gap drops substantially,
- score L2 gap drops substantially.

So increasing SGQF budget from the minimal one-point rule to level 2 clearly
improves the lower-rung predator-prey approximation.

### What does not continue to improve meaningfully
From level 2 to level 3 and level 4:
- value gaps are essentially unchanged,
- score gaps are essentially unchanged,
- higher point counts (5 → 17 → 45) do not buy materially better agreement with
  the dense same-target target on this fixed predator-prey row.

That means the current predator-prey mismatch is **not** just a “budget too
small” problem once SGQF reaches level 2. The evidence is consistent with the
method-class mismatch identified in the earlier audit: the Gaussian
assumed-density closure is the main limitation, not simply insufficient sparse
level.

## Supported claims
1. Increasing SGQF budget from level 1 to level 2 improves both value and score
   agreement against the dense same-target predator-prey lower-rung reference.
2. Increasing SGQF budget further from level 2 to levels 3 and 4 does not
   materially reduce the observed predator-prey value and score gaps on this
   fixed lower-rung target.
3. The current predator-prey SGQF gap is therefore not well explained by “just
   raise the sparse level” once level 2 is reached.

## Not supported by this pass
1. No universal monotonicity claim for SGQF budget ladders.
2. No runtime-efficiency or production-readiness claim.
3. No claim that higher sparse levels will never help on other models or other
   predator-prey fixtures.
4. No claim that SGQF is competitive with the dense lower-rung reference on this
   target just because the ladder improves from level 1 to level 2.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| close the predator-prey SGQF budget ladder as a successful local characterization | satisfied | no branch/tolerance/confound veto triggered | whether other predator-prey fixtures or a richer SGQF lane would respond differently | use this as the governing local interpretation for predator-prey SGQF tuning: level 2 is the real step-up; level 3/4 do not rescue the remaining gap | no general SGQF budget theorem |

## Practical conclusion

For this predator-prey lower-rung same-target row:
- **more SGQF budget helps from level 1 to level 2**,
- but **more budget beyond level 2 does not fix the problem**.

So the current value/score gap to dense appears to be dominated by the SGQF
closure class rather than by an under-tuned sparse-level budget once level 2 is
used.
