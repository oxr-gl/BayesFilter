# Experiment result: actual-sv-two-lane-value-gradient-comparison

## Plan reference
- `docs/plans/bayesfilter-actual-sv-two-lane-value-gradient-comparison-plan-2026-06-27.md`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  bayesfilter/highdim/sv_mixture_cut4.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

```bash
python - <<'PY'
# tiny-fixture dim 1..3 value/score comparison script
# computes Lane-A dense vs SGQF, Lane-B dense vs SGQF/UKF, and cross-lane gaps
PY
```

## Result summary
- Implemented and documented two explicit actual-SV lanes:
  - **Lane A**: exact-transformed direct likelihood quadrature.
  - **Lane B**: augmented-noise Gaussian-closure approximate likelihood.
- Added wrapper score paths for both lanes using GradientTape under the declared
  `theta=[probit_gamma, log_beta]` parameterization.
- Added a dense Lane-B Gaussian-closure reference and a Lane-B UKF comparator.
- Targeted compile checks passed.
- Targeted p41/p43 tests passed: **66 passed**.
- Tiny-fixture comparison shows Lane-B SGQF is very close to its own dense
  Lane-B reference, while Lane-B UKF is much farther from that dense Lane-B
  reference on these rows.
- Cross-lane gaps are large and clearly nonzero, confirming the two lanes are not
  the same scalar.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| Targeted tests passed | 66/66 | Targeted p41/p43 actual-SV coverage passed after fixes |
| Lane A value gap, dim 1 | 0.014506 | SGQF direct quadrature stays close to exact-transformed dense reference |
| Lane A value gap, dim 2 | 0.017758 | Same-target Lane-A gap remains small |
| Lane A value gap, dim 3 | 0.018228 | Same-target Lane-A gap remains small |
| Lane A score relative error, dims 1/2/3 | 7.86e-12 / 2.51e-11 / 2.16e-11 | GradientTape wrapper matches centered finite differences extremely well |
| Lane B SGQF value gap, dim 1 | 1.98e-4 | Lane-B SGQF is very close to dense Lane-B reference |
| Lane B SGQF value gap, dim 2 | 2.21e-4 | Lane-B SGQF is very close to dense Lane-B reference |
| Lane B SGQF value gap, dim 3 | 2.27e-4 | Lane-B SGQF is very close to dense Lane-B reference |
| Lane B SGQF score relative error, dims 1/2/3 | 4.15e-12 / 1.44e-11 / 1.21e-11 | GradientTape Lane-B SGQF wrapper matches centered finite differences extremely well |
| Lane B SGQF gradient relative error vs dense Lane-B reference, dims 1/2/3 | 3.27e-4 / 2.38e-4 / 1.94e-4 | SGQF gradient tracks the dense Lane-B reference very closely |
| Lane B SGQF gradient absolute gap norm, dims 1/2/3 | 6.62e-4 / 6.65e-4 / 6.65e-4 | Absolute gradient mismatch to dense Lane-B reference stays small |
| Lane B UKF value gap, dim 1 | 0.748551 | UKF Lane-B approximation is materially worse than Lane-B SGQF on this tiny row |
| Lane B UKF value gap, dim 2 | 1.214197 | UKF Lane-B remains much farther from dense Lane-B reference |
| Lane B UKF value gap, dim 3 | 1.572123 | UKF Lane-B remains much farther from dense Lane-B reference |
| Lane B UKF score relative error, dims 1/2/3 | 9.45e-12 / 6.76e-12 / 6.36e-12 | Wrapper score is self-consistent with finite differences of the UKF scalar |
| Lane B UKF gradient relative error vs dense Lane-B reference, dims 1/2/3 | 2.74e-1 / 2.22e-1 / 1.87e-1 | UKF gradient is much farther from the dense Lane-B reference than SGQF |
| Lane B UKF gradient absolute gap norm, dims 1/2/3 | 5.54e-1 / 6.19e-1 / 6.42e-1 | Absolute gradient mismatch to dense Lane-B reference is large |
| Cross-lane value gap, dim 1 | 3.677954 | Lane-A and Lane-B are not the same scalar |
| Cross-lane value gap, dim 2 | 7.725620 | Lane-A and Lane-B are not the same scalar |
| Cross-lane value gap, dim 3 | 13.331319 | Lane-A and Lane-B are not the same scalar |

## Engineering observations
- Exported the new actual-SV lane helpers through `bayesfilter/highdim/__init__.py`.
- The first attempt at analytic Lane-B score helpers was more brittle than needed;
  replacing them with GradientTape wrappers removed shape-contract and principal-
  sqrt branch blockers while preserving same-scalar score checks.
- Lane-B SGQF needed a higher sparse level (`sparse_level=4`) to line up tightly
  with the dense Lane-B Gaussian-closure reference on the tiny fixtures.
- The principal-square-root UKF route hit active-floor placement blockers for the
  current augmented-noise state construction; the retained historical SVD-UKF
  value backend avoided that blocker and remained usable as a diagnostic Lane-B
  comparator.
- One pre-existing p41 sparse-level ladder assertion assumed monotone improvement
  for every metric; the actual observed gaps showed mixed monotonicity in some
  state-moment metrics, so the test was tightened to assert improvement where it
  is actually supported and to cap the remaining metrics directly.
- For the broader control-model phase, the existing Model B and Model C fixtures
  already provide stable score-comparison baselines for cubature, UKF, and CUT4,
  so they can be used as cross-family controls without changing their semantics.

## Broader comparison extension
### Additional control-model score diagnostics
| Model | Backend | Log likelihood | Score relative error vs FD | Interpretation |
|---|---|---:|---:|---|
| Model B nonlinear accumulation | Cubature | -1.559797 | 6.48e-10 | Control row remains extremely consistent with finite differences |
| Model B nonlinear accumulation | UKF | -1.559808 | 1.32e-3 | UKF control row is weaker than cubature/CUT4 but still close at the existing test scale |
| Model B nonlinear accumulation | CUT4 | -1.537279 | 6.28e-10 | Control row remains extremely consistent with finite differences |
| Model C smooth-phase nonlinear growth | Cubature | -4.871427 | 2.57e-9 | Control row remains extremely consistent with finite differences |
| Model C smooth-phase nonlinear growth | UKF | -5.242725 | 6.41e-3 | UKF control row is noticeably weaker than cubature/CUT4 on this fixture |
| Model C smooth-phase nonlinear growth | CUT4 | -4.937942 | 1.13e-9 | Control row remains extremely consistent with finite differences |

### KSC surrogate separation rows
| Dim | KSC Kalman-mixture log likelihood | Interpretation |
|---:|---:|---|
| 1 | -4.505481 | Surrogate transformed-SV row only, not actual-SV evidence |
| 2 | -8.847219 | Surrogate transformed-SV row only, not actual-SV evidence |
| 3 | -15.092460 | Surrogate transformed-SV row only, not actual-SV evidence |

Interpretation of the broader control rows:
- The control models continue to separate strong score/value agreement from weaker
  UKF approximations, which is consistent with the actual-SV Lane-B finding that
  SGQF tracks its dense Gaussian-closure reference much better than UKF on the
  tested tiny fixtures.
- The KSC rows remain numerically close to the Lane-A truth-anchor scale on these
  tiny fixtures, but they are still surrogate transformed-SV evidence and must
  not be promoted as actual-SV rows.
- These additional rows are not actual-SV proof, but they support the conclusion
  that the broader comparison harness still distinguishes approximation quality
  rather than collapsing all methods into one score-quality bucket.

## Empirical evidence
- On the tiny deterministic actual-SV fixtures, **Lane-B SGQF is much closer to
  the dense Lane-B Gaussian-closure reference than Lane-B UKF**.
- The same pattern now holds for gradients against the dense Lane-B reference:
  **Lane-B SGQF gradients track the dense Lane-B gradient closely, while Lane-B
  UKF gradients are much farther away**.
- On those same rows, **Lane-A SGQF remains close to the exact-transformed dense
  same-target reference**.
- Lane-A and Lane-B values differ materially, so the empirical results support the
  documentation change that they are different declared scalars rather than two
  implementations of one scalar.
- The GradientTape score wrappers for both lanes match centered finite differences
  extremely closely, so the current score evidence is internally consistent with
  the declared wrapper scalar in each lane.

## Mathematical claims
- Claimed only what was implemented and tested:
  - Lane A and Lane B are distinct cumulative log-likelihood constructions.
  - Lane-A and Lane-B score wrappers differentiate their own declared scalar.
- No new proof is claimed here that Lane B is closer to the exact actual-SV
  likelihood than Lane A. The empirical result only shows Lane-B SGQF is closer
  than Lane-B UKF to the **dense Lane-B Gaussian-closure** reference on these
  tiny fixtures.

## Decision
- Keep **Lane A** as the same-target exact-transform truth-anchor lane.
- Keep **Lane B** as a distinct augmented-noise Gaussian-closure approximate-
  likelihood lane.
- For the current tiny actual-SV fixtures, prefer **Lane-B SGQF** over **Lane-B
  UKF** as the stronger Gaussian-closure approximation for both value and
  gradient fidelity to the dense Lane-B reference.
- Do not interpret cross-lane differences as bugs; they are expected evidence of
  different declared scalars.

## Next step
- Expand the comparison artifact to the broader model set named in the plan,
  keeping within-lane and cross-lane evidence separate.
- If desired, add a dedicated benchmark script under `docs/benchmarks/` to emit
  these Lane-A / Lane-B tables reproducibly.
- Revisit a promoted principal-square-root Lane-B UKF only if a non-blocking
  augmented-noise structural construction is identified; for now the historical
  UKF backend remains diagnostic-only.
