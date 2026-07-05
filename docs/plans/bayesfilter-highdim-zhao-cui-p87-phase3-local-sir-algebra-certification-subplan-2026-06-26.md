# P87 Phase 3 Subplan: Local SIR Algebra Certification

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE3_EXECUTION`

## Phase Objective

Certify local d18 SIR model derivative algebra for the parameterized Zhao-Cui
Austria target before using it as analytical score evidence in filter tests.

## Entry Conditions Inherited From Previous Phase

- Phase 2 locally repaired the candidate filter score route so the repair
  scope no longer contains `ForwardAccumulator` or
  `tensorflow_forward_accumulator_for_model_log_density`.
- Phase 2 result received Claude read-only `VERDICT: AGREE`.
- The SIR route uses model-level score hooks for initial, transition, and
  observation log-density derivatives.
- Parameter order and claim class are frozen.
- Phase 3 is promotion-track only for local SIR algebra certification; it is
  not a full filter correctness gate.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-result-2026-06-26.md`
  - The result must record the CPU-only execution choice and exact local
    command manifest, including `CUDA_VISIBLE_DEVICES=-1` for Python/pytest
    commands.
- Focused tests in `tests/highdim/test_p81_analytical_sir_score.py`.
- Updated Phase 4 subplan.

## Required Checks/Tests/Reviews

Execution environment:

- Repository root: `/home/chakwong/BayesFilter`.
- Execution target: local CPU-only scientific check; no GPU/CUDA command is
  required or allowed in Phase 3.
- CPU-only enforcement: every Python/pytest command below must be launched with
  `CUDA_VISIBLE_DEVICES=-1` before TensorFlow imports.
- Python environment: current active repository Python environment used by the
  Phase 2 focused checks.
- Tensor dtype: float64 for the SIR derivative comparisons.
- Network/model access: none during local checks; Claude is read-only review
  only.

```text
env CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py
env CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "parameterized_sir or zhao_cui_sir"
rg -n "transition_mean_parameter_jacobian|transition_log_density_parameter_score|observation_log_density_parameter_score|initial_log_density_parameter_score|infectious_components_vjp" bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py
git diff --check -- bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Claude review is required if tests or model code are changed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do local SIR initial, transition, and observation score formulas match diagnostic autodiff/FD for all three parameters where sensitivity is expected, with explicit zero only where the model is parameter-independent? |
| Baseline/comparator | Hand-coded SIR model methods vs `GradientTape` and centered FD diagnostics. |
| Primary criterion | Tight float64 local agreement for all parameters, batch size >1 where applicable, perturbed states, explicit initial-zero justification, and VJP scatter coverage. |
| Veto diagnostics | Silent zero score for intended sensitive parameter, parameter-order mismatch, nonfinite derivative, diagnostic used as filter/source promotion, missing initial-zero justification. |
| Explanatory diagnostics | `GradientTape` and FD residuals. |
| Not concluded | Filter score correctness, full-history d18 feasibility, source-route correctness. |
| Artifact | Phase 3 result and tests, with CPU-only command manifest recorded. |

## Forbidden Claims/Actions

- Do not claim filter-level analytical-gradient correctness.
- Do not use local model agreement as source-route validation.
- Do not run GPU/long numerical work.
- Do not treat the generic reverse-mode fallback in `filtering.py` as SIR
  analytical-promotion evidence.
- Do not revive ALS training, training-base sweeps, rank/degree claims, or
  production/default-policy claims in Phase 3.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if:

- Phase 2 receives Claude `VERDICT: AGREE`;
- local algebra tests pass;
- Phase 3 result records explicit score coverage and nonclaim boundaries;
- Phase 4 states that its filter route is JVP-free in the Phase 2 repair
  scope but still not full-history/source/production certified.

## Stop Conditions

- Local analytical score mismatch.
- Parameter order cannot be verified.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 3 result/close record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
