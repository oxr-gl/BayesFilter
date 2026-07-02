# Actual-SV Two-Lane Comparison

- JSON artifact: `/home/chakwong/BayesFilter/docs/benchmarks/actual_sv_two_lane_comparison_2026-06-27.json`
- Dims: `[1, 2, 3]`
- Include KSC surrogate rows: `True`
- Include control rows: `True`

## Nonclaims

- tiny deterministic comparison harness only
- not a production timing benchmark
- not HMC convergence evidence
- Lane A and Lane B are different declared scalars
- KSC surrogate rows are reported separately from actual-SV rows

## Actual-SV rows

- dim 1: Lane-A gap=0.014506, Lane-B SGQF gap=0.00019814, Lane-B UKF gap=0.748551, cross-lane gap=3.67795
- dim 2: Lane-A gap=0.0177579, Lane-B SGQF gap=0.000221254, Lane-B UKF gap=1.2142, cross-lane gap=7.72562
- dim 3: Lane-A gap=0.0182283, Lane-B SGQF gap=0.000226574, Lane-B UKF gap=1.57212, cross-lane gap=13.3313

## KSC surrogate rows

- dim 1: log-likelihood=-4.50548 (surrogate row only, not actual-SV evidence)
- dim 2: log-likelihood=-8.84722 (surrogate row only, not actual-SV evidence)
- dim 3: log-likelihood=-15.0925 (surrogate row only, not actual-SV evidence)

## Control rows

- model_b_nonlinear_accumulation / tf_svd_cubature: log-likelihood=-1.5598, score_relerr=1.63215e-10
- model_b_nonlinear_accumulation / tf_svd_ukf: log-likelihood=-1.55981, score_relerr=0.00131753
- model_b_nonlinear_accumulation / tf_svd_cut4: log-likelihood=-1.53728, score_relerr=1.61486e-10
- model_c_smooth_phase_growth / tf_svd_cubature: log-likelihood=-4.87143, score_relerr=2.59597e-09
- model_c_smooth_phase_growth / tf_svd_ukf: log-likelihood=-5.24273, score_relerr=0.00640924
- model_c_smooth_phase_growth / tf_svd_cut4: log-likelihood=-4.93794, score_relerr=1.10411e-09
