# 1D LGSSM T4 Residual Solver Ladder

## Decision

`one_d_lgssm_t4_residual_solver_ladder_residual_resolved`

## Evidence Contract

Comparator: current local patched FilterFlow executable. Primary
criterion: BayesFilter-vs-FilterFlow scalar, ledger, trigger, and AD
gradient agreement. Residual pass is a separate veto. Finite differences
remain explanatory only.

## Results

| Config | threshold | max iter | contract match | residual pass | max row residual | scalar delta | AD grad delta | BF iterations | BF FD | FF FD |
| --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_1e-6_iter200` | `1e-06` | `200` | `True` | `False` | `0.0005233287811279297` | `1.7313559519394062e-07` | `3.0408782158986014e-08` | `201.0` | `-1.9368130259955763` | `-1.9371509552001953` |
| `threshold_1e-7_iter200` | `1e-07` | `200` | `True` | `False` | `0.000523258831560458` | `1.680496284350852e-07` | `2.5057770214331754e-07` | `201.0` | `-1.9368126776886374` | `-1.9371509552001953` |
| `threshold_1e-6_iter500` | `1e-06` | `500` | `True` | `True` | `1.420476457947295e-05` | `5.981229511675679e-08` | `8.501654091830346e-07` | `333.0` | `-1.9375573807578483` | `-1.9383430480957031` |
| `threshold_1e-8_iter500` | `1e-08` | `500` | `True` | `True` | `4.76837158203125e-07` | `8.221198388724815e-09` | `1.1820381384808343e-07` | `501.0` | `-1.9374297627416937` | `-1.9383430480957031` |

## Interpretation

The residual veto can be cleared by solver settings on this fixture. Best observed config: `threshold_1e-8_iter500` with max row residual `4.76837158203125e-07`.

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
