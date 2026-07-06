# Low-Rank Gradient Nonfinite Diagnostic

- Status: `FAIL`
- Phase: `LOW_RANK_GRADIENT_REPAIR_DIAGNOSTIC`
- Evidence class: `owner_designated_managed_session_visible_gpu_trusted`
- Hard vetoes: `['91002:qr_plus:loglik_gradient_nonfinite', '91002:qr_plus:loglik_gradient_disconnected', '91002:qr_plus:final_particles_gradient_disconnected', '91003:center:loglik_gradient_nonfinite', '91003:center:loglik_gradient_disconnected', '91003:center:final_particles_gradient_disconnected', '91003:q_plus:loglik_gradient_nonfinite', '91003:q_plus:loglik_gradient_disconnected', '91003:q_plus:final_particles_gradient_disconnected', '91003:q_minus:loglik_gradient_nonfinite', '91003:q_minus:loglik_gradient_disconnected', '91003:q_minus:final_particles_gradient_disconnected', '91003:r_plus:loglik_gradient_nonfinite', '91003:r_plus:loglik_gradient_disconnected', '91003:r_plus:final_particles_gradient_disconnected', '91003:r_minus:loglik_gradient_nonfinite', '91003:r_minus:loglik_gradient_disconnected', '91003:r_minus:final_particles_gradient_disconnected', '91003:qr_plus:loglik_gradient_nonfinite', '91003:qr_plus:loglik_gradient_disconnected', '91003:qr_plus:final_particles_gradient_disconnected']`
- JSON artifact: `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.json`

## Rows

| Seed | Probe | Value finite | Loglik grad finite | Prior grad finite | Final-particle grad finite | Route outputs finite | Factor residual | Row residual | Col residual | Iterations |
| ---: | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| 91002 | `qr_plus` | `True` | `False` | `True` | `False` | `True` | 0.004857312887907028 | 0.8265491724014282 | 0.01540684700012207 | 120 |
| 91003 | `center` | `True` | `False` | `True` | `False` | `True` | 0.006653338670730591 | 0.753667950630188 | 0.0033339262008666992 | 120 |
| 91003 | `q_plus` | `True` | `False` | `True` | `False` | `True` | 0.006098220124840736 | 0.7775169014930725 | 0.0030513405799865723 | 120 |
| 91003 | `q_minus` | `True` | `False` | `True` | `False` | `True` | 3.474997356534004e-08 | 3.534555435180664e-05 | 4.649162292480469e-06 | 34 |
| 91003 | `r_plus` | `True` | `False` | `True` | `False` | `True` | 3.39350663125515e-08 | 3.4749507904052734e-05 | 5.0067901611328125e-06 | 27 |
| 91003 | `r_minus` | `True` | `False` | `True` | `False` | `True` | 3.8708094507455826e-08 | 3.9637088775634766e-05 | 4.76837158203125e-06 | 33 |
| 91003 | `qr_plus` | `True` | `False` | `True` | `False` | `True` | 3.527384251356125e-08 | 3.600120544433594e-05 | 5.841255187988281e-06 | 36 |

## Non-Claims

- focused repair diagnostic only
- no calibrated residual threshold claim
- no holdout validation claim
- no posterior correctness claim
- no HMC readiness claim
- no default/package/public API readiness claim
- no statistical superiority claim
- no scientific validity claim
