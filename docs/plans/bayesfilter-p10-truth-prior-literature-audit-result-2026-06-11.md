# P10 Truth-Prior Literature Audit Result

metadata_date: 2026-06-11
status: FIRST_PASS_SOURCE_GROUNDED_LEDGER_P44_DIAGNOSTICS_REMOVED
owner: Codex
skill: scholarly-literature-audit

## Decision

Use Zhao--Cui 2024 Section 6 and the local author-code mirror as the primary
source for the SV, SIR, predator-prey, generalized-SV, and linear-Kalman
benchmark-prior anchors where applicable.  P44 cubic, quadratic, and tanh
diagnostic rows are removed from this literature-prior ledger because they are
BayesFilter project fixtures rather than author-paper model rows.

This file is a prior/source ledger.  It does not freeze the final P10 truth
prior and does not run the benchmark.

## Sources Inspected

| Source | Local path | Status | Inspected anchors |
| --- | --- | --- | --- |
| Zhao and Cui, 2024, *Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models* | `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf` | primary full text inspected | Section 6.1 linear Kalman, Section 6.2 stochastic volatility, Section 6.3 SIR, Section 6.4 predator-prey |
| Kim, Shephard, and Chib, 1998 | bibliography entry only | source gap for this task | Candidate source for SV priors/mixture approximations; full text not inspected in this pass |
| Chib, Nardari, and Shephard, 2002 | bibliography entry only; bib entry appears malformed | source gap for this task | Candidate source for SV Bayesian priors; full text not inspected |
| Li, Wang, Yau, and Zhang, 2019 | `.local_sources/highdim_nonlinear_filtering/li_wang_yau_zhang_tt_nonlinear_filtering_1908.04010.pdf` | primary full text inspected lightly | Contains QTT nonlinear-filtering examples, but not the P8 parameter-prior ladder |
| van der Merwe, 2003 | `docs/Sigma-Point Kalman Filters for Probabilistic Inference in Dynamic State-Space Models Merwe(03).pdf` | background only | Sigma-point parameter choices, not model truth priors |
| P1 target registry | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json` | reviewed project fixture | Current row theta/tested values |

## Excluded Rows

The following P8 rows are excluded from this literature-prior ledger by scope
decision because no inspected author paper/code source uses them as benchmark
models; they are BayesFilter dense-reference diagnostic fixtures:

- `p44_cubic_additive_gaussian_dim_1_2_3`
- `p44_quadratic_observation_dim_1_2_3`
- `p44_nonlinear_transition_h2_dim_1_2_3`
- `p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3`

## Row-By-Row Prior And Tested-Value Ledger

| P8 model row | Literature support status | Prior/tested values found | Current project values | P10 recommendation |
| --- | --- | --- | --- | --- |
| `lgssm_exact_kalman_dim_1_2_3` | `PAPER_PRIOR_FOUND`, but paper row differs from project row | Zhao--Cui Section 6.1 uses a linear Kalman model with reduced parameters `(a,d)`, prior `uniform([0.4,1]^2)`, synthetic truth `a=0.8`, `d=0.5`, `T=50`, `m=n=3`. | P1 row uses `(rho_raw, log_transition_variance_base, log_observation_variance_base, raw_initial_mean_scale) = (0.25, log(0.18), log(0.12), 0.04)`. | Do not directly transplant `(a,d)` prior.  Use it as an LGSSM literature anchor and design a project-coordinate prior around the P1 transform, with stability/variance bounds explicitly mapped to Zhao--Cui's stationary low-noise regime. |
| `sv_exact_transformed_actual_nongaussian_dim_1_2_3` | `PAPER_PRIOR_FOUND` and `PAPER_TESTED_VALUE_FOUND` | Zhao--Cui Section 6.2 synthetic SV fixes `sigma=1`, estimates `(gamma,beta)`, uses truth `gamma=0.6`, `beta=0.4`, prior `uniform([0.1,0.9]^2)`, and initial prior `x0|theta ~ N(0, 1/(1-gamma^2))`.  Real-data SV prior: `(gamma+1)/2 ~ Beta(20,1.5)`, `sigma^2 ~ IG(1,0.005)` under their parameterization, `log(beta)|sigma ~ N(0, sigma^2/0.8)`, and `x0|gamma,sigma ~ N(0, sigma^2/(1-gamma^2))`. | P1 row uses per-dimension `physical_gamma=[0.60,0.52,0.47]`, `physical_beta=[0.40,0.35,0.45]`, `fixed_sigma=[1.00,0.85,0.75]`, coordinates `(probit_gamma, log_beta)`. | For core prior, use Zhao--Cui synthetic SV: independent `gamma_j ~ Uniform(0.1,0.9)`, `beta_j ~ Uniform(0.1,0.9)` in physical coordinates, transformed to `(probit_gamma, log_beta)`, with `sigma_j` fixed by row.  Use P1 values as deterministic centers/checkpoints. |
| `sv_ksc_gaussian_mixture_surrogate_dim_1_2_3` | `PAPER_PRIOR_FOUND` via SV source, `SOURCE_GAP` for KSC mixture details | Same SV prior/tested values as above for `(gamma,beta)`.  Kim--Shephard--Chib 1998 is a candidate source for the Gaussian-mixture observation approximation, but full text was not inspected in this pass. | Same `gamma`, `beta`, `sigma` fixture as transformed actual SV row; mixture table fixed. | Use the same SV truth prior as the actual transformed SV row, but label target as Gaussian-mixture surrogate.  Inspect KSC 1998 before freezing mixture-specific source claims. |
| `native_generalized_sv_dense_lower_rung_dim_2` | `PROJECT_FIXTURE_ONLY`, `SOURCE_GAP` for generalized-SV literature prior | No local paper prior found for this native generalized SV row. | Physical values: `rho_s=0.25`, `rho_h=0.55`, `sigma_s=0.70`, `sigma_h=0.45`, `beta=0.35`; coordinates `(atanh(rho_s), atanh(rho_h), log(sigma_s), log(sigma_h), log(beta))`. | Use fixture as temporary core-prior center.  Candidate prior: bounded/stationary `rho_s,rho_h` away from ±1 and lognormal/box priors for positive scales, but this must be labeled project-designed until source search is expanded. |
| `spatial_sir_lower_rung_j1_dim_2` | `PAPER_FIXED_PARAMETER_FOUND` | Zhao--Cui Section 6.3 fixes `kappa_j=0.1`, `nu_j=18`, `delta=0.02`, RK4 internal step `0.005`, process noise `N(0,I_{2J})`, observation noise `N(0,100 I_J)`, initial states `S_j(0)=485+j`, `I_j(0)=15-j`, and prior `x0 ~ N(mu0,I_{18})` for `J=9`. | P1 lower-rung `J=1` uses `kappa=[0.1]`, `nu=[18.0]`, `initial_mean=[486,14]`, same noise/covariance conventions. | No parameter prior exists because rates are fixed and theta dimension is 0.  For P10, vary only data/truth seeds for this row unless a new parameterized SIR row is explicitly introduced. |
| `spatial_sir_scaling_route_admitted_rank_selection_blocked_d18` | `PAPER_FIXED_PARAMETER_FOUND`, value route blocked | Same Zhao--Cui SIR settings with `J=9`, Austrian adjacency, `T=20`, fixed `kappa_j=0.1`, `nu_j=18`, `mu0=(S_1(0),I_1(0),...,S_9(0),I_9(0))`. | P1 production row matches fixed `J=9` parameters and covariance conventions but is blocked before filtering by rank-selection route. | Keep out of numeric performance tables until value route unblocks.  If unblocked, no theta prior is needed unless a parameter-estimation SIR row is added. |
| `predator_prey_lower_rung_dim_2` | `PAPER_PRIOR_FOUND` and `PAPER_TESTED_VALUE_FOUND` | Zhao--Cui Section 6.4 uses truth `theta=(0.6,114,25,0.3,0.5,0.5)`, `x0=(50,5)`, `T=20`, process and observation noise `N(0,4I_2)`, initial prior `x0 ~ N((50,5),I_2)`, and parameter prior uniform on box `a=(0.1,110,20,0.1,0,0)`, `b=(1.1,130,30,1.1,1,1)` for `(r,K,a,s,u,v)`. | P1 lower-rung row uses the same physical truth vector. | Use Zhao--Cui uniform box as the core prior in physical coordinates.  Convert to any canonical benchmark coordinates with a reviewed transform before score/Hessian comparison. |
| `predator_prey_production_tuned_h25_dim_2` | `PAPER_PRIOR_FOUND` and `PAPER_TESTED_VALUE_FOUND`, horizon differs | Same Zhao--Cui predator-prey prior and truth as above, with paper terminal time `T=20`. | P1 production-tuned row uses same truth vector but horizon 25 deterministic path. | Use Zhao--Cui uniform box as prior source; record horizon mismatch as project benchmark design.  Stress lane may include edge boxes, but main prior should stay inside paper box. |

## Recommended P10 Prior-Lane Design

Use two lanes, as required by the P8 contract:

- `core_prior`: source-supported or project-centered draws that avoid
  explosive, unidentified, or degenerate regions.
- `stress_prior`: boundary or difficult regimes used only for robustness and
  failure-rate reporting, not ordinary-case ranking.

Concrete first-pass recommendations:

| Model group | Core prior candidate | Source status |
| --- | --- | --- |
| Zhao--Cui synthetic SV rows | `gamma_j ~ Uniform(0.1,0.9)`, `beta_j ~ Uniform(0.1,0.9)`, fixed row `sigma_j`; transform to `(probit_gamma, log_beta)`. | paper prior |
| Predator-prey rows | Uniform box on `(r,K,a,s,u,v)` with lower `(0.1,110,20,0.1,0,0)` and upper `(1.1,130,30,1.1,1,1)`. | paper prior |
| Spatial SIR rows | No theta prior; fixed rates `kappa=0.1`, `nu=18`; data/state variation only. | paper fixed parameter |
| LGSSM row | Design project prior in current P1 coordinates; use Zhao--Cui linear Kalman `uniform([0.4,1]^2)` on `(a,d)` as context, not direct row prior. | partial paper prior, coordinate mismatch |
| Native generalized SV | Project prior around fixture values, stationary `rho` bounds and positive scale bounds. | project fixture only/source gap |

## Claim-Support Ledger

| Claim | Support |
| --- | --- |
| Zhao--Cui synthetic SV uses `sigma=1`, truth `(gamma,beta)=(0.6,0.4)`, and `Uniform([0.1,0.9]^2)` prior. | `PRIMARY_TECHNICAL_SUPPORT`: Zhao--Cui 2024 Section 6.2 inspected in local full text. |
| Zhao--Cui real-data SV uses Beta/IG/normal priors for `(gamma,sigma,beta)`. | `PRIMARY_TECHNICAL_SUPPORT`: Zhao--Cui 2024 Section 6.2 inspected.  Need original econometric sources before adopting as benchmark prior. |
| Zhao--Cui SIR fixes `kappa=0.1`, `nu=18`, with Gaussian initial-state prior and no theta prior. | `PRIMARY_TECHNICAL_SUPPORT`: Zhao--Cui 2024 Section 6.3 inspected. |
| Zhao--Cui predator-prey uses the listed truth and uniform parameter box. | `PRIMARY_TECHNICAL_SUPPORT`: Zhao--Cui 2024 Section 6.4 inspected. |
| Native generalized SV row has literature priors. | `SOURCE_GAP_BLOCKER`: no local primary source found in this pass. |

## Omission And Reviewer-Risk Register

| Risk | Why it matters | Next action |
| --- | --- | --- |
| Kim--Shephard--Chib 1998 not inspected | It is central for stochastic-volatility likelihood and Gaussian-mixture approximations. | Locate local/full text or fetch with approval; inspect priors and mixture table details before freezing KSC surrogate claims. |
| Chib--Nardari--Shephard 2002 not inspected | It is a direct Bayesian SV prior source. | Fix malformed bibliography entry if needed and inspect full text. |
| Native generalized SV source missing | Current fixture values may be arbitrary without literature context. | Search generalized SV/Box-Cox SV sources referenced by Zhao--Cui, especially Zhang--Maxwell and Yu et al. |
| LGSSM coordinate mismatch | Zhao--Cui prior is for `(a,d)`, while P1 uses transformed variance/rho coordinates. | Write a small mapping note or choose a project prior with stability and variance bounds. |

## Next Required Actions

1. Decide whether P10 should use paper priors only where available and
   separately carry BayesFilter diagnostic rows outside this literature-prior
   plan.
2. Inspect Kim--Shephard--Chib 1998 and Chib--Nardari--Shephard 2002 before
   freezing SV mixture-surrogate prior claims.
3. For non-P44 project-only rows, write explicit benchmark-prior boxes in
   canonical `phi` coordinates and get Claude review before sampling truth
   draws.
4. Keep fixed-parameter SIR rows out of theta-prior sampling unless a new
   parameter-estimation row is created.

## What Is Not Concluded

- Final P10 truth priors are not frozen.
- No truth draws were sampled.
- No synthetic data were generated.
- No benchmark likelihood, score, or curvature values were computed.
- Excluded P44 project fixture values are not literature priors.
