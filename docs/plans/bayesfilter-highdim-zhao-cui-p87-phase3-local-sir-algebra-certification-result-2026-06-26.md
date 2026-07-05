# P87 Phase 3 Result: Local SIR Algebra Certification

Date: 2026-06-27

Status: `P87_PHASE3_LOCAL_SIR_ALGEBRA_PASS_REVIEWED_CLOSED`

## Decision

Phase 3 passed the local SIR algebra certification gate under CPU-hidden
execution.

The local `ParameterizedZhaoCuiSIRSSM` algebra now has focused evidence for:

- theta convention and parameter order;
- intended transition and observation sensitivity;
- transition mean parameter Jacobian against diagnostic `GradientTape`;
- transition log-density parameter score against diagnostic `GradientTape`;
- observation log-density parameter score against diagnostic `GradientTape`;
- infectious-coordinate VJP scatter;
- explicit initial log-density zero score contract inherited from Phase 2.

This certifies local SIR model algebra only. It does not prove filter-level
value/gradient correctness, horizon-0 d18 value/gradient readiness,
full-history d18 feasibility, Zhao-Cui source-route correctness, HMC readiness,
production readiness, LEDH/GPU readiness, or any default-policy change.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `97ad05d` |
| Repository root | `/home/chakwong/BayesFilter` |
| Python | `3.11.14` |
| TensorFlow | `2.19.1` |
| Execution target | CPU-only local check |
| CPU-only enforcement | `CUDA_VISIBLE_DEVICES=-1` on Python/pytest commands |
| Tensor dtype | `tf.float64` |
| GPU status | Intentionally hidden; `tf.config.list_physical_devices('GPU')` reported `[]` in the manifest probe |
| Network/model access | None for local checks; Claude review was external/read-only before execution |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-subplan-2026-06-26.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-result-2026-06-26.md` |

## Checks Run

```bash
env CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py
```

Result: passed.

```bash
env CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "parameterized_sir or zhao_cui_sir"
```

Result: passed, `5 passed, 2 deselected, 2 warnings`.

```bash
rg -n "transition_mean_parameter_jacobian|transition_log_density_parameter_score|observation_log_density_parameter_score|initial_log_density_parameter_score|infectious_components_vjp" bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py
```

Result: passed with expected model/test anchors for the SIR local algebra
helpers and tests.

```bash
git diff --check -- bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Result: passed.

## Evidence Table

| Evidence item | Status | Notes |
| --- | --- | --- |
| Parameter convention | Passed | Test checks three-parameter P8p/P79 scaling and parameter order. |
| Intended sensitivity | Passed | Test checks transition sensitivity for kappa/nu scales and observation sensitivity for observation-noise scale. |
| Transition mean Jacobian | Passed | Hand-coded Jacobian matches diagnostic `GradientTape` to tight float64 tolerances. |
| Transition score | Passed | Hand-coded transition score matches diagnostic `GradientTape` to tight float64 tolerances. |
| Observation score | Passed | Hand-coded observation score matches diagnostic `GradientTape` to tight float64 tolerances. |
| Initial score | Passed as explicit zero contract | Phase 2 added `initial_log_density_parameter_score`; the wrapped SIR initial density is parameter-independent. |
| Infectious VJP scatter | Passed | Test verifies infectious cotangent scatters into odd SIR coordinates and zeros susceptible coordinates. |

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Local SIR algebra certification passes. |
| Primary criterion | Met for local algebra under CPU-hidden execution. |
| Veto diagnostics | No silent zero for intended sensitive parameters; parameter order verified; no nonfinite local derivative evidence; no diagnostic promoted to filter/source proof. |
| Main uncertainty | Filter-level horizon-0 value/gradient evidence and all later full-history/source/production gates remain open. |
| Next justified action | Execute reviewed Phase 4 horizon-0 d18 value/gradient gate. |
| What is not concluded | Filter-level correctness, full-history d18 feasibility, source-route correctness, HMC/production readiness, LEDH/GPU/training readiness. |

## Phase 4 Handoff

Phase 4 may proceed because its refreshed subplan received Claude
`VERDICT: AGREE`. Phase 4 must remain a horizon-0 d18 value/gradient gate and
must preserve
`BLOCK_HORIZON0_OVERCLAIM`: horizon-0 evidence cannot validate full-history
d18 filtering.

The refreshed handoff artifact is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase4-horizon0-d18-value-gradient-subplan-2026-06-26.md`
