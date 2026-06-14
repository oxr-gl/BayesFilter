# P18 Zhao--Cui Backward Snowball Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This ledger does not claim a complete literature survey.
- P18 is an annotation of Zhao--Cui Sections 1--3 and 5, not a survey chapter.

## Relevant Backward References From Zhao--Cui

| Reference family | Zhao--Cui context | P18 action |
|---|---|---|
| State-space/filtering reviews: Kantas et al., Särkkä, Reich and Cotter, Evensen et al. | Introduces sequential learning problems. | Context only; not used for theorem support. |
| Particle filters/SMC: Gordon et al., Doucet and Johansen, Pitt and Shephard, Chopin et al. | Motivates particle degeneracy and parameter-learning baselines. | Context only; P18 focuses on Zhao--Cui algorithm. |
| Transport/KR maps: Knothe, Rosenblatt, Spantini et al. | Supports KR rearrangement terminology and conditional maps. | Used as conceptual background; P18 derives local triangular identities directly. |
| Tensor trains: Oseledets, Hackbusch, Bigoni et al., Gorodetsky et al. | Supports functional TT representation and fitting. | Background; P18 derives the local TT algebra used in the note. |
| Squared inverse Rosenblatt transports: Cui and Dolgov 2022 | Source for Lemma 1 and Proposition 2. | Direct delegated support where Zhao--Cui explicitly cites it. |
| Preconditioning/tempering: Beskos et al., Gelman and Meng, Herbst and Schorfheide, Kantas et al. | Supports bridge/tempering motivation. | Context only; P18 reconstructs Zhao--Cui Section 5 formulas. |

Decision: `BACKWARD_SNOWBALL_RECORDED_FOR_ANNOTATION_SCOPE`.
