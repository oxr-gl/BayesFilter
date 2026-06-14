# P16 Zhao-Cui Backward-Snowball Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui JMLR 2024.

what_is_not_concluded:
- No exhaustive literature survey.
- No claim that every cited method has been technically audited in P16.

## Backward-Snowball Items Mentioned In Checked Sections

| Work family | Zhao--Cui context | P16 action |
|---|---|---|
| Kalman, extended Kalman, ensemble Kalman | Baselines for filtering | Context only; no theorem support. |
| Sequential Monte Carlo, bootstrap, auxiliary PF, resampling | Particle-filter comparators and bias correction context | Context only; not expanded. |
| Transport maps, KR rearrangements, Spantini et al. | Conceptual relation to conditional maps | Mentioned through derivation of KR maps; no broad survey claim. |
| Tensor trains: Hackbusch, Oseledets, Bigoni, Gorodetsky | TT background | Used as background; P16 derives needed TT formulas directly. |
| Cui--Dolgov squared inverse Rosenblatt transports | Squared-TT and KR support | Seed/support source; prior artifacts relied on it. |
| Beskos, Gelman--Meng, Herbst--Schorfheide, Kantas | Tempering bridge context | Context only for preconditioning. |

## Decision

`BACKWARD_SNOWBALL_CONTEXT_RECORDED_NOT_EXHAUSTIVE`
