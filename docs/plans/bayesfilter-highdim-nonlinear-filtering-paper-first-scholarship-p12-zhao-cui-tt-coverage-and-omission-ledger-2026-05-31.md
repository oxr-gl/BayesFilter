# P12 Zhao-Cui TT Coverage And Omission Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.

what_is_not_concluded:
- No broad high-dimensional filtering literature completeness.
- No ranking/citation metadata claim.
- No omission-risk clearance for a future chapter-level survey.

## Scoped Coverage Rationale

P12 is a proof-expansion note for two local propositions, not a new survey
chapter.  The proof requires the Zhao-Cui sequential squared-TT construction,
the Cui-Dolgov squared inverse Rosenblatt transport substrate for context, and
project derivations for normalized approximate filtering and same-scalar
differentiation.

## Backward Snowball Status

| Referenced family | Role in Zhao-Cui/Cui-Dolgov | P12 action |
|---|---|---|
| Rosenblatt and Knothe KR rearrangement sources | Foundational naming and transport background | Classified as `BACKGROUND`; not theorem support for Proposition 1 or 2 |
| Oseledets tensor-train decomposition and TT-cross sources | Foundational TT representation/computation background | Classified as `BACKGROUND`; P12 defines the needed TT notation directly |
| Cui-Dolgov squared inverse Rosenblatt transport | Direct transport substrate for squared-TT conditional maps | Included as contextual source support |
| Particle-filter degeneracy and competing filters | Broad high-dimensional filtering context | Out of P12 proof scope; relevant to chapter integration, not to the two propositions |
| Zhao-Cui error-propagation theorems | Approximation-error theory | Not used as proof support; P12 proves only normalized approximate recursion and same-scalar derivative |

## Forward Snowball Status

Public metadata was used only to check source status for Zhao-Cui and
Cui-Dolgov on 2026-05-31.  A forward-citation survey was not required for the
two local propositions and was not used as truth evidence.  Future chapter
integration should revisit forward citations if it makes comparative or
state-of-the-art claims.

## Omission Risks

| Omitted source/family | Risk | Why it does not block P12 |
|---|---|---|
| Original Rosenblatt/Knothe papers | Reviewer may want historical KR provenance | P12 uses KR only as context; proofs do not depend on historical priority |
| Oseledets TT decomposition and TT-cross papers | Reviewer may want full TT background | P12 defines the algebra needed for the propositions; no TT approximation theorem is invoked |
| Zhao-Cui approximation-error theorems beyond the construction anchors | Reviewer may expect accuracy discussion | P12 explicitly does not prove posterior accuracy |
| Adaptive differentiable programming/autodiff through SVD/QR literature | Reviewer may ask about global adaptive gradients | P12 explicitly excludes adaptive-code global gradients |

Decision:
`SCOPED_COVERAGE_ACCEPTABLE_FOR_LOCAL_PROOF_NOTE`
