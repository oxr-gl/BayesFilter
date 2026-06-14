# P25 Zhao--Cui Source-Support Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P24 Zhao--Cui human-facing companion note.

what_is_not_concluded:
- No claim that the literature survey is complete.
- No claim that citation counts or venue status prove correctness.
- No production implementation claim.

## Source Support

P25 inherits the P24 source-support discipline and adds no new scholarly
sources.  The new sections are project derivations built from the same source
base:

| Source | P25 use | Allowed claims | Forbidden claims |
|---|---|---|---|
| Zhao and Cui JMLR 2024 | Source-order filtering, squared-TT, KR, smoothing, and preconditioning reconstruction | Algorithmic and equation-level reconstruction for Sections 1--3 and 5 | Exact posterior accuracy, production readiness, global adaptive differentiability |
| Oseledets 2011 | Tensor-train representation background | TT as rank-linked tensor representation | Filtering correctness or derivative claims |
| Rosenblatt 1952 | Triangular transformation background | KR/triangular map terminology | Tensor-train or filtering claims |
| Cui and Dolgov | Squared inverse Rosenblatt transport background delegated through Zhao--Cui | Background for squared/KR transport context | New theorem-level claims beyond Zhao--Cui anchors or P25 derivations |

Local artifact paths and version/retraction blockers are recorded in the P24
source-support ledger.  P25 does not claim fresh live database retraction or
erratum checks.

Decision: `SOURCE_SUPPORT_INHERITED_AND_SCOPED`.
