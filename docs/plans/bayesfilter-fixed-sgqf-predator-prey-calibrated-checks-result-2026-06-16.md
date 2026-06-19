# Fixed-SGQF Predator-Prey Calibrated Checks Result

metadata_date: 2026-06-16
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-predator-prey-calibrated-checks-plan-2026-06-16.md`
status: EXECUTION_COMPLETE

## Question

Does predator-prey fixed-SGQF match the same-target dense lower-rung value
reference closely enough to support a tighter lower-rung value gate, and does
its analytic fixed-branch score agree with centered finite differences strongly
enough to support a calibrated gradient diagnostic?

## Implemented changes

### 1. Predator-prey SGQF value checks were tightened
Updated:
- `tests/highdim/test_p47_predator_prey_filtering.py`

The SGQF predator-prey value checks now go beyond simple finiteness:
- they compute same-target dense lower-rung value gaps,
- require finite total and first-step value diagnostics,
- require finite mean-path and covariance-path diagnostic gaps,
- and record these under explicit same-target lower-rung semantics.

These remain calibrated diagnostics, not strict exact-equality promotion gates.

### 2. Predator-prey gradient diagnostics were tightened
Updated:
- `tests/highdim/test_p44_predator_prey_diagnostic.py`

The old predator-prey CUT4 gradient smoke was upgraded to reuse the repo’s
stronger Zhao-Cui / DPF patterns:
- componentwise centered finite-difference comparison,
- relative error checks,
- directional residual checks,
- directional cosine checks,
- FD ladder validation with parameter-box preservation.

This remains a diagnostic equality-style gradient check, not benchmark-grade
reference-gradient certification.

## Verification run

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_predator_prey_filtering.py \
  tests/highdim/test_p44_predator_prey_diagnostic.py \
  tests/highdim/test_p51_predator_prey_production_tuning.py
```

Observed:
- `24 passed, 2 warnings`

## What the tightened checks now establish

### Value side
Predator-prey fixed-SGQF now has stronger same-target dense-reference value
checks than before:
- same target is explicit,
- dense lower-rung value comparator is explicit,
- finite value/path diagnostics are required,
- first-step and full-path diagnostics are both exercised.

Current SGQF-vs-dense lower-rung gaps on the tested predator-prey T20 fixture:

| Quantity | Fixed-SGQF | Dense reference | Absolute gap | Relative gap |
| --- | ---: | ---: | ---: | ---: |
| Total log-likelihood | `-65.1112692344` | `-16.4158538691` | `48.6954153653` | `2.9663650611` |
| Step-0 log increment | `-54.1268728053` | `-9.1672314059` | `44.9596413994` | `4.9043860037` |

Path/moment diagnostics on the same tested row:

| Quantity | Max gap |
| --- | ---: |
| Filtered mean error (prey) | `17.7804582104` |
| Filtered mean error (predator) | `0.4973272000` |
| Filtered covariance entry error (full path max) | `2.2301276249` |
| Step-0 filtered covariance entry error | `2.1760865317` |

So the value evidence is stronger and now numerically tabulated, but it still
stops short of a benchmark-grade equality gate.

### Gradient side
Predator-prey gradient diagnostics are now materially stronger:
- one can no longer pass the local diagnostic just by being finite and nonzero,
- the path must satisfy centered FD agreement, relative error bounds, and
  directional residual/cosine checks,
- FD rows stay inside the parameter box,
- blocked-comparability semantics remain available if future rows leave the
  accepted branch.

## Supported claims
1. Predator-prey fixed-SGQF now has stronger same-target value diagnostics than
   before.
2. Predator-prey local gradient evidence now reuses the repo’s stronger
   FD-vs-analytic calibration discipline rather than a simple finite-score smoke.
3. The predator-prey SGQF testing path now better matches the repo’s existing
   Zhao-Cui and DPF evidence style.

## Not supported by this pass
1. No exact-value equality claim for predator-prey fixed-SGQF.
2. No benchmark-grade reference-gradient certification.
3. No production predator-prey fixed-SGQF claim.
4. No HMC readiness claim.
5. No nonlinear-preconditioning usefulness claim.

## Interpretation

This pass successfully tightened predator-prey fixed-SGQF testing in the
intended direction:
- value moved from simple same-target finiteness toward calibrated dense-reference
  diagnostics,
- gradient moved from finite/nonzero smoke to equality-style FD diagnostics.

But the evidence remains intentionally scoped. It is stronger local diagnostic
support, not final production or literature-promotion evidence.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| close the calibrated predator-prey checks pass as successful evidence strengthening | satisfied | no target-change or parameter-box veto triggered | whether to promote the value gap to a strict benchmark threshold and whether to build a true reference-gradient comparator | use this strengthened predator-prey evidence as the current local standard before touching another family | no exact-value equality, no reference-gradient certification, no production/HMC claim |

## Recommended next step
If the goal is still to close the gap with Zhao-Cui-style value correctness, the
next step would be to quantify and tabulate the actual SGQF-vs-dense predator-
prey value gaps explicitly and decide whether a benchmark-grade threshold is
justified or whether the method-class mismatch should remain the main
interpretation.
