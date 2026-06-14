# P16 Zhao-Cui BayesFilter Translation Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui JMLR 2024.

what_is_not_concluded:
- No production API mapping.
- No code implementation in `bayesfilter/`.

## Translation Choices

| Zhao--Cui notation | P16 BayesFilter notation | Reason |
|---|---|---|
| \(\theta\) as unknown parameter | \(\alpha\) in annotated reconstruction | Matches parameter-learning density while avoiding later derivative ambiguity. |
| External derivative parameter | \(\beta\) in fixed-branch section | Separates HMC-style likelihood argument from posterior random coordinate. |
| \(\pi,\widehat\pi\) | unnormalized exact/approximate densities | Preserved when useful. |
| \(q_t\) | propagated pointwise target | Preserved and rewritten in BayesFilter density notation. |
| \(F^l,F^u\) | lower/upper conditional KR maps | Preserved with conditional density derivation. |

## Decision

`TRANSLATION_PASS_WITH_BETA_ALPHA_SEPARATION`
