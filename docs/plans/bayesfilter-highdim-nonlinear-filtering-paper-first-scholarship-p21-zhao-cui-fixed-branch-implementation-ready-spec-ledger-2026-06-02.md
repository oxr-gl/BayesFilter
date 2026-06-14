# P21 Zhao--Cui Fixed-Branch Implementation-Ready Specification Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No executable prototype claim.
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross/rank/pivot/domain
  choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No full adaptive Zhao--Cui implementation claim.

## Decision

Decision: `IMPLEMENTATION_READY_MATH_SPECIFICATION_CREATED`.

P21 specifies the minimal fixed-branch \(T=2\), one-dimensional nonlinear
state-space example as derivation, pseudocode, array shapes, branch manifest,
derivative recursions, and finite-difference protocol.  It does not write
executable code.

## Fixed Branch

Declared branch:

| Object | Specification |
|---|---|
| horizon | \(T=2\) |
| coordinates | \(z=(z_t,z_{t-1})\in[-1,1]^2\) |
| basis | normalized Legendre basis |
| basis count | \(p\), declared before fitting |
| fitting points | fixed deterministic table \(Z_{\rm fit}\in[-1,1]^{N\times2}\) |
| ranks | \(R_0=R_2=1,\ R_1=R\) |
| cores | \(C_1:(1,p,R),\ C_2:(R,p,1)\) |
| carried numerator | \(Q_t:(p,p)\), \(\dot Q_t:(p,p)\) |
| carried filter | \(P_t:(p,p)\), \(\dot P_t:(p,p)\); query evaluator outputs \((M,)\) |
| ridge | fixed \(\rho>0\) |
| shift | fixed \(c_t\) per time step |
| defensive term | fixed \(\tau_t\lambda_t\) |
| sweeps | fixed deterministic order and count |

## Required Mathematical Blocks

| Block | P21 anchor | Status |
|---|---|---|
| reference-coordinate targets | P21-6--P21-7 | `SPECIFIED` |
| shifted square-root fit | P21-8 | `SPECIFIED` |
| squared-TT density and normalizer | P21-9--P21-10 | `SPECIFIED` |
| carried reference filter | P21-11 | `SPECIFIED` |
| normalizer derivative | P21-13--P21-21 | `SPECIFIED` |
| squared-density derivative | P21-24--P21-30 | `SPECIFIED` |
| mass contraction derivative | P21-31--P21-39 | `SPECIFIED` |
| fixed ridge-solve derivative | P21-40--P21-50 | `SPECIFIED` |
| carried-filter quotient derivative | P21-51--P21-57i | `SPECIFIED` |
| next-step target derivative | P21-58--P21-63 | `SPECIFIED` |
| shapes and branch manifest | P21-64--P21-66 | `SPECIFIED` |
| model derivatives | P21-67--P21-71 | `SPECIFIED` |
| basis and fitting table | P21-72--P21-75 | `SPECIFIED` |
| core-fitting pseudocode | P21-76--P21-78 | `SPECIFIED` |
| forward/derivative pass pseudocode | P21-79--P21-80 | `SPECIFIED` |
| diagnostics | P21-81 | `SPECIFIED` |
| same-branch finite differences | P21-82--P21-87 | `SPECIFIED` |

## Implementation-Readiness Limits

- Shape contracts are for a minimal two-coordinate fixed branch.
- Adaptive TT-cross and rank-changing operations are not specified.
- No runtime, finite-difference numerical output, or software dependency check
  is produced.
- A later coding phase must convert the pseudocode into tests before claiming
  engineering correctness.
