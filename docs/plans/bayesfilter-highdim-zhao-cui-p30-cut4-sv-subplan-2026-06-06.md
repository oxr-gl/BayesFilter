# P38-C1 Subplan: Stochastic-Volatility CUT4 Comparator Boundary

metadata_date: 2026-06-06
phase: P38-C1

Question: should native P30 stochastic volatility be compared directly against
the current CUT4 filter?

Comparator:

- direct `tf_svd_cut4_filter` is `COMPARATOR_NOT_APPLICABLE` for the native P30
  stochastic-volatility likelihood because the current CUT4 value path assumes
  an additive-Gaussian observation closure, while P30 SV uses a
  heteroskedastic observation density `y_t | x_t ~ N(0, beta^2 exp(x_t))`.

Audit design:

- record a manifest row for the current scalar dense and scalar TT SV lanes;
- preserve dense quadrature as the active comparator for existing SV value
  tests;
- block CUT4 equivalence claims until a separately reviewed heteroskedastic
  Gaussian-closure comparator is introduced.

Equivalence criterion:

- none in this phase; status must be `COMPARATOR_NOT_APPLICABLE`.

Vetoes:

- using an additive-Gaussian CUT4 model as if it were the P30 SV likelihood;
- treating scalar dense-grid agreement as CUT4 agreement;
- paper-scale `T=1000`, S&P 500, adaptive TT-cross/SIRT, GPU, HMC, or DSGE
  claims.

Non-claims:

- no CUT4 statistical-equivalence evidence for native SV;
- no production SV CUT4 comparator;
- no paper-scale SV validation.

Artifact:

- manifest tests in `tests/highdim/test_p30_cut4_statistical_comparators.py`.

