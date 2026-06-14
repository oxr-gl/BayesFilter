# P15 MathDevMCP Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," FoCM 2022.
- P10-P14 BayesFilter Zhao-Cui TT artifacts.

what_is_not_concluded:
- No posterior accuracy claim.
- No global derivative claim for adaptive TT-cross or rank-changing code.
- No HMC convergence claim.
- No production BayesFilter implementation.
- No default-method recommendation.
- No numerical validation on the target high-dimensional model.

## Status Before Tool Calls

Planned narrow checks:
- affine product change-of-variables identity;
- log-normalizer derivative;
- linear solve derivative;
- normalized-density derivative.

Tool results will be appended after MathDevMCP calls.

## Tool Results

| Obligation | Status | Evidence |
|---|---|---|
| derivative notation forms submitted directly with `diff(...)` | `MCP_TOOL_LIMIT` | SymPy encoder reported `'Symbol' object is not callable`; not used as certification |
| normalized-density algebra `(qdot*z-q*zdot)/z^2 = qdot/z - q*zdot/z^2` | `MCP_VERIFIED` | SymPy simplified difference to zero |
| defensive marginal mass `tau*2^{-D}*2^O = tau*2^{-(D-O)}` | `MCP_VERIFIED` | SymPy simplified difference to zero |
| log-normalizer with assumptions `taudot=0`, `cdot=0` | `MCP_UNVERIFIED` | tool did not substitute equality assumptions; human derivation retained |
| linear solve derivative symbolic assumption form | `MCP_UNVERIFIED` | tool did not substitute equality assumptions; human derivation retained |

Overall decision: `NARROW_IDENTITIES_PARTLY_VERIFIED_BROAD_TT_PROOF_HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`.
