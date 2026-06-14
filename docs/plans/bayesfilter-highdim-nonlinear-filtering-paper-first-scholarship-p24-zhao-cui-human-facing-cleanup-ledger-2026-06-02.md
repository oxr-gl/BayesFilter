# P24 Zhao--Cui Human-Facing Cleanup Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross or rank-changing
  decisions.
- No production implementation claim.
- No empirical validation claim.

## Cleanup Controls

| Control | P24 location | Status |
|---|---|---|
| Human-facing abstract replaces planning/process abstract. | Main note abstract | `DONE` |
| Opening process equations removed. | Section "Notation And Reading Convention" | `DONE` |
| Displayed audit tags replaced by hidden labels and normal equation numbers. | All displayed equations | `DONE` |
| Bibliography added with `\cite{...}` source references. | Main note preamble and end matter | `DONE` |
| "Source Coverage Summary" renamed and moved to reader-facing scope note. | Appendix | `DONE` |
| Banned process strings scanned before build. | Validation step | `PENDING_FINAL_SCAN` |

