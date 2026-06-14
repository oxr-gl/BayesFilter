# P48 Source-Code Discrepancy Ledger: Zhao--Cui Source Route Vs BayesFilter

metadata_date: 2026-06-09
program: P48-source-code-discrepancy-and-rewrite
status: EXECUTED_STATIC_AUDIT
supervisor: Codex
reviewer: Claude Code read-only

## Scope

This ledger compares material implementation choices in the Zhao--Cui companion
MATLAB code against the current BayesFilter high-dimensional implementation.
It treats P10/P34 as certified source-understanding artifacts only.  Those
audits did not certify that BayesFilter's fixed-branch route implements the
same adaptive TT/SIRT algorithm.

No source MATLAB code is copied into `bayesfilter/`.  Any source-faithful
rewrite must be a clean-room TensorFlow / TensorFlow Probability
implementation unless a separate reviewed exception is approved.

Analytical gradients are a legitimate reason to maintain a separate
deterministic gradient lane.  They are not a reason to relabel an unfaithful or
ad hoc route as source-faithful Zhao--Cui.  Gradient-bearing adaptations must
be named, tested, and bounded as adaptations.

## Surfaces Inspected

Source surfaces:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTFun/cross.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m`
- `third_party/audit/tensor-ssm-paper-demo/eg3_sir/mainscript.m`
- `third_party/audit/tensor-ssm-paper-demo/eg4_predatorprey/mainscript.m`
- P10/P34 source audit artifacts.

BayesFilter surfaces:

- `bayesfilter/highdim/fitting.py`
- `bayesfilter/highdim/filtering.py`
- `bayesfilter/highdim/squared_tt.py`
- `bayesfilter/highdim/transport.py`
- `bayesfilter/highdim/models.py`
- P30--P47 highdim tests and result artifacts.

## Discrepancy Ledger

| ID | Topic | Source anchor | BayesFilter anchor | Difference | Severity | Decision | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D01 | TT fitting route | `@TTFun/cross.m` lines 8--29, 81--169; examples use `TTOption('tt_method','random', ...)` | `fitting.py` lines 1--37, 182--292, 333--434, 555--626 | Source uses adaptive TT cross/ALS with random enrichment, rank truncation, local error, and debug/init samples. BayesFilter uses deterministic fixed-rank weighted ridge ALS on declared fixed designs with replayable branch manifests and condition-number gates. | Critical for source-faithful filtering; beneficial divergence for gradient lane. | `split_lanes` | Build a clean-room adaptive TT/SIRT filtering lane; keep fixed branch as deterministic gradient/HMC lane with explicit non-equivalence label. |
| D02 | Time-step retained object | `full_sol.m` lines 13--18, 33--43, 105--129; `pre_sol.m` lines 10--13, 205--213, 241--260 | `filtering.py` lines 186--231, 346--518, 775--983, 997--1214, 2359--2602 | Source retains SIRT/TTSIRT transport objects plus affine maps `L, mu` and samples/weights. BayesFilter retains dense or TT grid payloads over all retained axes, with reference/physical points and weights. | Critical for high-dimensional scaling and M4b. | `source_wins` | Rewrite source-faithful lane to retain transport/density objects and samples, not all-axes tensor-product grids. |
| D03 | Transition propagation | `full_sol.m` lines 21--43, 46--66, 76--98; `pre_sol.m` lines 17--31, 33--103 | `filtering.py` lines 2201--2348, 2628--2673; P47 M4b result | Source propagates samples through model dynamics, uses weights/ESS, and reapproximates in a local coordinate system. BayesFilter multistate route computes pairwise transition density between retained grids, giving quadratic grid-pair complexity. | Critical; directly explains M4b failure. | `source_wins` | Replace paper-scale multistate propagation with sample/ESS-driven proposal and reapproximation before claiming source-faithful Zhao--Cui filtering. |
| D04 | ESS and particle correction | `full_sol.m` lines 21--43, 49--66; `pre_sol.m` lines 17--31, 35--103, 245--256 | `filtering.py` fixed branch value paths; `fitting.py` deterministic residual/holdout gates | Source has particle-style proposal correction, ESS diagnostics, resampling, and enhanced sampling when ESS collapses. BayesFilter fixed branch has deterministic quadrature/fitting gates but no source-style particle correction. | High. | `source_wins` | Add ESS/correction mechanics to source-faithful lane; keep fixed branch gates as engineering diagnostics only. |
| D05 | Coordinate maps and recentering | `full_sol.m` lines 63--98; `pre_sol.m` lines 103--213 | `filtering.py` config coordinate windows and retained grid maps; `transport.py` grid CDF KR map | Source computes weighted `mu, L`, expands by `epd`, shifts target by random sampled minimum, and builds in those coordinates. Preconditioned source additionally composes maps `Tu2x`, `Tx2u`. BayesFilter uses fixed coordinate windows / affine maps and grid-based conditional CDF helpers. | High. | `split_lanes` | Source-faithful lane should implement sample-derived recentering and preconditioner maps. Fixed branch should keep declared windows for differentiable replay. |
| D06 | Preconditioned algorithm | `pre_sol.m` lines 1--14, 33--213, 241--260, 276--394 | P30/P47 preconditioning artifacts; `models.py` diagnostic flags | Source implements five preconditioner/residual variants (`pifg`, `fg`, `fgeta`, `g`, `geta`) and two-stage SIRT construction. BayesFilter has limited diagnostic fixtures and no complete source-faithful preconditioned residual solver. | Critical for predator-prey and difficult nonlinear rows. | `source_wins` | P49+ should implement a clean-room preconditioned lane before retrying M5b production. |
| D07 | Smoothing and backward conditionals | `full_sol.m` lines 139--205; `pre_sol.m` lines 276--394 | `transport.py`; `squared_tt.py` marginal helpers; no full source-style smoother in highdim filtering | Source uses inverse/conditional Rosenblatt maps and backward smoothing weights. BayesFilter currently focuses on filtering value paths and limited marginal/transport helpers. | Medium for filtering likelihood; high for smoothing claims. | `documentation_only` | Do not claim source-style smoothing. Add tests only when smoothing is in scope. |
| D08 | Squared density normalizer and marginalization | `@TTSIRT/marginalise.m` lines 1--85; P10 crosswalk | `squared_tt.py` lines 183--283; P30 phase2p6b result | Source has recursive TTSIRT marginalization and stores `obj.z = obj.fun_z + obj.tau`. BayesFilter has squared density normalization and conditional helpers but explicitly lacks generic integrated-axis retained density evaluation outside validated cases. | Medium-high. | `test_required` | Scientific tests should compare marginal normalizers and conditionals on low-dimensional analytic densities before using them in source-faithful route. |
| D09 | Random/adaptive route differentiability | Source random enrichment, data-dependent ESS, resampling, SVD rank truncation, adaptive branches | `fitting.py` branch identity and deterministic fixed branch; P42/P43 gradient validation rules | Source route is not a stable differentiable scalar program for HMC gradients. BayesFilter fixed branch was intentionally designed for deterministic replay and gradient-bearing experiments. This is a valid reason for a separate gradient lane, not a justification for calling a changed route source-faithful. | Critical for HMC interpretation. | `split_lanes` | Keep current fixed branch for HMC/gradient lane; label it as a gradient-bearing fixed-branch adaptation, not adaptive source reproduction. |
| D10 | Model contract: spatial SIR | `eg3_sir/mainscript.m` lines 12--20, 32--55: `d=0`, `m=18`, `T=20`, `N=5e3`, random TT, `max_rank=40` | P47 M4b result; `models.py` `SpatialSIRSSM` | Source paper-scale SIR uses adaptive/random TT/SIRT on augmented dimension `d+2m=36`, not all-grid pairwise propagation. BayesFilter M4b all-grid route explodes: J=9 order=3 gives about `1.5e17` pairwise evaluations. | Critical. | `source_wins` | Do not retry M4b with all-grid route. Rewrite propagation/retention architecture first. |
| D11 | Model contract: predator-prey | `eg4_predatorprey/mainscript.m` lines 64--77: random TT, `max_rank=20`, bounded and preconditioned solvers | P47 M5b result; `models.py` predator-prey fixture | Source uses full/preconditioned TT/SIRT with random adaptive fitting. BayesFilter fixed-design candidate ran finitely but missed production tolerances by large log-likelihood/moment gaps. | Critical for production claim. | `test_required` | Preconditioned clean-room lane is the leading repair; scientific ladder must separate tuning failure from route-architecture failure. |
| D12 | Model contract: stochastic volatility/generalized SV | Source `eg2_sv`; P39--P43 artifacts; transformed Kalman/mixture discussion | `models.py` SV fixtures; P40--P43 tests | SV has useful exact/mixture/Kalman comparison ladders in transformed coordinates, but these do not certify multistate source-faithful TT/SIRT behavior. Generalized SV needs careful target equality and non-Gaussian observation tests. | Medium-high. | `test_required` | Use SV as a low-dimensional calibration ladder for values and gradients; do not promote it to proof of SIR/predator-prey scalability. |
| D13 | License and backend boundary | P10/P34 license findings: LGPL/GPL-family MATLAB reference | AGENTS.md TensorFlow/TFP backend rule; `bayesfilter/highdim/*` | Source MATLAB can guide a clean-room implementation but cannot be copied into production. BayesFilter algorithmic implementation must default to TF/TFP. | Critical governance. | `bayesfilter_wins` | Any rewrite plan must state clean-room translation and backend compliance. |
| D14 | Diagnostics and pass-token governance | Source examples are scripts and plotting oriented; P34 says not production-ready | P30--P47 artifacts and tests | BayesFilter has strong artifact/review discipline, but some prior labels risk overstating equivalence. Source has real algorithmic path but fewer automated regression gates. | High. | `split_lanes` | Preserve BayesFilter governance; patch claims to distinguish source audit, fixed branch, and source-faithful implementation. |

## Immediate Corrections To Claims

- The P10/P34 audit remains valid as evidence that the Zhao--Cui source code
  implements the paper method family.
- P46/P47 do not certify that BayesFilter implements the same adaptive
  source route.  They certify bounded fixed-design adapters and blockers.
- M4b and M5b should remain blocked until a source-faithful route amendment is
  implemented and tested.
- The current BayesFilter fixed branch should be described as
  "Zhao--Cui-inspired deterministic fixed-branch TT/SIRT experiments" unless a
  future plan proves route equivalence.

## Rewrite Direction

The clean split is:

1. Source-faithful filtering lane: sample propagation, ESS/reapproximation,
   source-style recentering, TT/SIRT transport objects, proposal correction,
   and preconditioner/residual maps.
2. Deterministic gradient lane: current fixed-branch route, replayable branch
   manifests, TensorFlow gradients, and fixed-design tests.

The source-faithful lane can be statistically strong for filtering while still
being unsuitable as the default differentiable HMC likelihood.

Conversely, the deterministic gradient lane can be useful for HMC while still
being unsuitable as evidence of source-faithful Zhao--Cui filtering.  Necessity
of analytical gradients and fidelity to the source algorithm are separate
claims with separate evidence contracts.
