# 1D LGSSM Horizon Ladder

## Decision

`one_d_lgssm_horizon_ladder_agreement_residual_veto`

| Scenario | T | Flags | Scalar delta | Ledger match | Residuals pass | Max row residual | BF AD | FF AD | BF FD | FF FD |
| --- | ---: | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `T2_anchor` | `2` | `[False, True]` | `6.201557778418021e-08` | `True` | `True` | `3.77402173978858e-06` | `-1.7820385507243621` | `-1.7820383310317993` | `-1.6753548204218038` | `-1.6754865646362305` |
| `T4_extension` | `4` | `[False, True, True, True]` | `1.7313559519394062e-07` | `True` | `False` | `0.0005233287811279297` | `-2.2461719817027275` | `-2.2461719512939453` | `-1.9368130259955763` | `-1.9371509552001953` |

## Interpretation

This is a fixed scalar-state forward-ledger ladder. Gradient diagnostics
remain non-promotional.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No DSGE/NAWM validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- No gradient correctness beyond this fixed 1D scalar fixture is concluded.
