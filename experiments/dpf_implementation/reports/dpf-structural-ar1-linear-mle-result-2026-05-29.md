# DPF Structural AR(1) Linear MLE Result

## Decision

`DPF_STRUCTURAL_AR1_LINEAR_MLE_ESTIMATION_CALIBRATION_WARNING`

| Check | Kalman | DPF | Role |
| --- | ---: | ---: | --- |
| value at true b | `7.099395` | `7.693165` | same-scalar smoke |
| gradient at true b | `-0.350863` | `-4.042359` | gradient smoke |
| grid MLE b | `0.650000` | `0.800000` | estimation smoke |
| SE-scaled MLE distance | `0.628773` | `0.628773` | calibration |
| max deterministic residual | `0.000e+00` | `0.000e+00` | veto |

This is an exact-Kalman comparison only for the `c=d=0` linear structural toy
fixture.  It does not validate the nonlinear `c,d != 0` case or DSGE/NAWM.
