# P4 Derivation Obligation Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U source ledgers, P2R chapter rewrite result, P3
industrial defect synthesis result, and edited `ch33`--`ch37`.

what_is_not_concluded: This ledger does not certify the chapters as formal
theorem files, paper-length proofs, production validation, NAWM readiness,
posterior accuracy, HMC convergence, tensor validation, transport validation,
GPU/XLA readiness, or exhaustive literature coverage.

## Status Classes

- `FULL_DERIVATION_READY`: the chapter now contains a stepwise monograph
  derivation under stated assumptions.
- `PROJECT_DERIVATION`: the claim is supported by derivation in project
  notation, not by a single source theorem.
- `PRIMARY_TECHNICAL_SUPPORT`: checked source anchors support the source-local
  technical claim.
- `SOURCE_THEOREM_ONLY`: the text points to a checked theorem but does not
  reproduce a full proof.
- `MCP_UNVERIFIED`: MathDevMCP did not certify the broad obligation.
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`: the text is human-audited but not
  machine-certified.
- `REMOVE_OR_WEAKEN`: unsupported theorem-level language must be weakened or
  removed.

## Obligation Table

| obligation_id | chapter | label_or_location | claim | support_status | classification | assumptions_needed | text_status | mcp_status | source_anchor | remaining_gap |
|---|---|---|---|---|---|---|---|---|---|---|
| `P4-33-1` | `ch33` | `eq:bf-hd-prediction`, `eq:bf-hd-update` | prediction/update recursion follows from dominated state-space model and Bayes formula | `PROJECT_DERIVATION` | `FULL_DERIVATION_READY` | dominated densities, finite positive normalizer | expanded joint-density and normalization derivation added | not machine-checked | standard filtering recursion, local derivation | no machine certification |
| `P4-33-2` | `ch33` | `eq:bf-hd-likelihood-factor` | likelihood factors as product of one-step normalizers | `PROJECT_DERIVATION` | `FULL_DERIVATION_READY` | chain rule, finite normalizers | expanded derivation added | log-product check attempted only as small algebra and unverified by SymPy simplification | local derivation | no formal measure-theoretic certification |
| `P4-33-3` | `ch33` | `prop:bf-hd-score` | predictive score equals filtering expectation of the log-integrand score | `PROJECT_DERIVATION` | `FULL_DERIVATION_READY` | dominated differentiation, positive integrand on support | proof expanded step by step | `MCP_UNVERIFIED` for broad label; human-reviewed | local derivation under Assumption `ass:bf-hd-dominated` | tool parsing cannot certify integral identity |
| `P4-33-4` | `ch33` | `sec:bf-hd-zakai-dmz`, `sec:bf-hd-pathwise-dmz` | Zakai/KS/DMZ and robust-DMZ statements are source-local PDE formulations | `PRIMARY_TECHNICAL_SUPPORT` | `SOURCE_THEOREM_ONLY` | source-specific regularity, ellipticity, weak-solution, boundary assumptions | unchanged source-local caution plus defects section | not attempted as broad PDE proof | van Handel, Davis, Yau, Meng source anchors | no independent PDE proof; no historical-priority proof |
| `P4-33-5` | `ch33` | `sec:bf-hd-foundations-defects` | exact target, approximate target, density semantics, and PDE assumptions are passed to synthesis as gates | `PROJECT_DERIVATION` | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | exact/approximate likelihood distinction | new section added | not machine-checkable | local derivation plus cited source boundaries | industrial contract, not theorem |
| `P4-34-1` | `ch34` | `prop:bf-hd-affine-projection` | affine MMSE estimator has gain `C S^{-1}` and covariance `P - C S^{-1} C^T` | `PROJECT_DERIVATION` | `FULL_DERIVATION_READY` | finite second moments, nonsingular innovation covariance, conformable dimensions | proof expanded with trace objective and residual covariance | scalar algebra verified; typed label diagnostic needs assumptions due parser limits | local derivation | matrix theorem remains human-reviewed |
| `P4-34-2` | `ch34` | one-dimensional `Y=X^2+V` example | Gaussian projection can be moment-correct while missing nonlinear posterior structure | `PROJECT_DERIVATION` | `FULL_DERIVATION_READY` | symmetric zero-mean Gaussian predictor | example added | not machine-checked | local moment calculation | illustrative, not a general theorem |
| `P4-34-3` | `ch34` | `prop:bf-hd-exactness-not-accuracy` | polynomial exactness does not imply posterior accuracy | `PROJECT_DERIVATION` plus source-local quadrature support | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | polynomial projection/remainder split, Gaussian projection step | existing proof retained; defects section added | not machine-checked | Julier, Arasaratnam, Jia, Singh | exactness theorem source-local to checked papers |
| `P4-34-4` | `ch34` | `sec:bf-hd-gq-defects` | projection, quadrature, PSD/factor, active-dimension, and scalar-diagnostic defects feed synthesis | `PROJECT_DERIVATION` | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | block dimension and diagnostic thresholds declared in later work | new section added | not machine-checkable | local synthesis | not production policy |
| `P4-35-1` | `ch35` | `prop:bf-hd-pf-collapse` | log-weight variance produces exponential variance inflation warning | `PROJECT_DERIVATION` plus primary particle-collapse support | `FULL_DERIVATION_READY` | weakly dependent log-likelihood blocks, lognormal heuristic for displayed calculation | proof expanded | lognormal moment ratio `MCP_VERIFIED`; broad collapse theorem not certified | Bengtsson, Snyder; local calculation | exact asymptotics remain source-specific |
| `P4-35-2` | `ch35` | `prop:bf-hd-transport-correction` | transport/guided proposal requires density-ratio correction and support coverage | `PROJECT_DERIVATION` | `FULL_DERIVATION_READY` | proposal positive on target support, integrability | support-veto paragraph added | not machine-certified | change-of-variables/importance identity, Parno/Papamakarios context | broad transport filtering remains source-specific |
| `P4-35-3` | `ch35` | `prop:bf-hd-factor-gate` | covariance compression requires PSD or factor gate | `PROJECT_DERIVATION` plus TN square-root caution | `FULL_DERIVATION_READY` | covariance object used in Gaussian update | two-by-two PSD counterexample added | PSD algebra identity `MCP_VERIFIED` locally | Menzen, square-root logic, local counterexample | finite-precision analysis not exhaustive |
| `P4-35-4` | `ch35` | `sec:bf-hd-ptt-defects` | particle, correction/support, map, TT density, and TN PSD defects feed synthesis | `PROJECT_DERIVATION` | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | declared diagnostics | new section added | not machine-checkable | source-local chapter claims | not validation of TT/transport methods |
| `P4-36-1` | `ch36` | `prop:bf-hd-same-scalar` | HMC target requires gradient and Metropolis scalar to correspond to same Hamiltonian | `PROJECT_DERIVATION` plus Neal source support | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | reversible volume-preserving integrator framework, finite scalar and gradient | scalar parity diagnostic added | not machine-certified | Neal, local diagnostic | no convergence proof |
| `P4-36-2` | `ch36` | `prop:bf-hd-jacobian-target` | transport-preconditioned HMC requires Jacobian-corrected transformed potential | `PROJECT_DERIVATION` | `FULL_DERIVATION_READY` | differentiable bijection, finite determinant, support validity | sign derivation added | typed diagnostic `consistent`, not formal proof | change of variables; Parno/Hoffman/Cui/Zhao context | no proof for learned-map quality |
| `P4-36-3` | `ch36` | `sec:bf-hd-hmc-defects` | target validity, scalar parity, Jacobian/support, diagnostics, and acceleration limits feed synthesis | `PROJECT_DERIVATION` | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | declared target and diagnostics | new section added | not machine-checkable | HMC source family plus local contract | no HMC convergence or backend claim |
| `P4-37-1` | `ch37` | `prop:bf-hd-particle-collapse-calculus` | particle collapse defect scales through log-weight variance | `PROJECT_DERIVATION` plus particle-collapse support | `FULL_DERIVATION_READY` | lognormal heuristic, effective-dimension variance | retained and cross-supported by `ch35` | lognormal moment ratio `MCP_VERIFIED`; broad proposition not certified | Bengtsson, Snyder | heuristic constant `c` source/model dependent |
| `P4-37-2` | `ch37` | `prop:bf-hd-local-cubature-diagnostic` | sparse-grid/high-degree cubature is first a local diagnostic | `PROJECT_DERIVATION` plus quadrature sources | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | bounded block dimension and smoothness | retained; stronger architecture proposition added | not machine-certified | Jia/Julier/Arasaratnam/Singh | no global sparse-grid theorem |
| `P4-37-3` | `ch37` | `prop:bf-hd-tensor-viability` | tensor viability requires rank stability plus semantic checks | `PROJECT_DERIVATION` plus TT/TN sources | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | stable ranks and object-specific diagnostics | retained | broad label previously unverified; local PSD algebra verified | Oseledets, Zhao--Cui, Menzen | no general TT rank guarantee |
| `P4-37-4` | `ch37` | `prop:bf-hd-transport-auditability` | transport usefulness requires correction/Jacobian/support auditability | `PROJECT_DERIVATION` plus transport sources | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | differentiability or source-specific map contract, support | retained | broad label previously unverified | Rosenblatt, Parno, Hoffman, Reich, Spantini 2022 | quarantined Spantini 2016 unused |
| `P4-37-5` | `ch37` | `prop:bf-hd-hmc-downstream` | HMC is downstream of same-scalar filter target | `PROJECT_DERIVATION` plus HMC sources | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | finite scalar and gradient, valid transform | retained and supported by `ch36` parity diagnostic | broad label previously unverified | Neal, Hoffman, Betancourt, Girolami, Hoffman NeuTra | no convergence proof |
| `P4-37-6` | `ch37` | `sec:bf-hd-synthesis-architecture` | method composition is a sequence of audited handoffs | `PROJECT_DERIVATION` | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | observable defect diagnostics and thresholds | new architecture section added | not machine-checkable | local synthesis | industrial contract, not theorem |
| `P4-37-7` | `ch37` | `prop:bf-hd-sparse-grid-promotion` | sparse-grid promotion requires bounded active dimension | `PROJECT_DERIVATION` plus source-local sparse-grid support | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | smooth local block, point budget, omitted-interaction residual | new proposition added | not machine-certified | Jia 2012/2013, Singh 2018 | Smolyak/Genz/Stroud originals remain blocked |
| `P4-37-8` | `ch37` | `prop:bf-hd-performance-after-veto` | performance comparison is conditional on validity gates | `PROJECT_DERIVATION` | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | validity event declared by component | new proposition added | typed diagnostic `consistent`, no formal proof | local synthesis | not an empirical benchmark |
| `P4-37-9` | `ch37` | `prop:bf-hd-block-scaffold-first` | block Gaussian scaffold comes before exotic methods as diagnostic baseline | `PROJECT_DERIVATION` | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | finite moments, block partition, factor diagnostics | retained | not machine-checkable | Gaussian projection derivation | not accuracy claim |
| `P4-37-10` | `ch37` | `prop:bf-hd-useful-not-novel` | useful non-novel synthesis is acceptable when every handoff exports diagnostics | `PROJECT_DERIVATION` | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | observable residual handoff | retained | not machine-checkable | local synthesis | not academic novelty claim |

## Claim-Support Summary

All new major claims were kept in either `PROJECT_DERIVATION`,
`PRIMARY_TECHNICAL_SUPPORT`, or `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` status.
No new claim uses citation counts, venue rank, abstracts, introductions,
conclusions, metadata, blocked originals, or quarantined papers as theorem
support.

The Spantini et al. 2016 decomposable-transport workshop paper remains
`QUARANTINED` and supports no claim.
