# P39 Claim-Support Ledger: SV Gaussian-Mixture CUT4

metadata_date: 2026-06-06

| Claim | Support class | Support anchor | Boundary |
|---|---|---|---|
| Native scalar SV observation is heteroskedastic. | PRIMARY_TECHNICAL_SUPPORT / PROJECT_DERIVATION | P30 SV equations; `StochasticVolatilitySSM.observation_log_density` | Does not imply current CUT4 handles native SV. |
| The transform `z_t = log(y_t^2 + c)` gives additive observation noise. | PROJECT_DERIVATION | P39 LaTeX derivation | Offset `c` is a numerical/domain device; exact algebra is for `c=0`, `y_t != 0`. |
| `eta_t = log(epsilon_t^2)` is non-Gaussian. | PRIMARY_TECHNICAL_SUPPORT / PROJECT_DERIVATION | KSC transform/moment paragraph; P39 derivation | Requires mixture, correction, or direct non-Gaussian quadrature for approximation. |
| The seven-component shifted table is the P39 implementation fixture. | PRIMARY_TECHNICAL_SUPPORT / IMPLEMENTATION_EVIDENCE / PROJECT_DERIVATION | KSC Table 4 and component law \(z_t\mid s_t=i\sim N(m_i-1.2704,v_i^2)\); `eq:bf-hd-sv-ksc-pinned-table`; `ksc_1998_log_chi_square_mixture`; P39 moment test | It is pinned for BayesFilter diagnostics; P39 does not implement KSC importance reweighting or the full KSC sampler. |
| Conditional on mixture component, transformed SV has an additive Gaussian observation. | PRIMARY_TECHNICAL_SUPPORT / PROJECT_DERIVATION | KSC component law; P39 derivation from finite mixture approximation | Exact only for the approximating mixture law. |
| Mixture-CUT4 can reuse additive-Gaussian CUT4 component updates. | IMPLEMENTATION_EVIDENCE / PROJECT_DERIVATION | `bayesfilter/highdim/sv_mixture_cut4.py`; P39 tests; CUT4 definition paragraph | In current scalar SV fixtures the conditional observation is linear Gaussian, so this validates reduction/bookkeeping, not nonlinear CUT4 accuracy. |
| P39 mixture-CUT4 matches dense transformed-mixture reference on tiny fixtures. | IMPLEMENTATION_EVIDENCE | `tests/highdim/test_p39_sv_mixture_cut4.py` | Local scalar evidence only; not a native SV likelihood, nonlinear CUT4 accuracy, or publication-scale result. |
| Same-target TT comparison is available. | SOURCE_GAP_BLOCKER | No transformed-mixture TT lane with same offset, table, horizon, parameters, and observations | Existing native SV TT lane is explanatory only. |
| P39 validates native SV or generalized SV production inference. | SOURCE_GAP_BLOCKER | Not implemented | Forbidden claim. |
