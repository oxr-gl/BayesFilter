# P81 Phase 3 Result: Fixed-Branch/JVP-Backed SIR d=18 Horizon-0 Smoke

status: PHASE3_FIXED_BRANCH_JVP_SIR_D18_SMOKE_PASSED_CLAUDE_R3_AGREE
date: 2026-06-21

## Question

Can the fixed-branch/JVP-backed Zhao-Cui candidate execute a finite,
branch-stable d=18 horizon-0 SIR score smoke under the P8p/P79 theta
convention?

## Decision

Yes for the bounded Phase 3 question.  The d=18 horizon-0 score path now runs
to completion on CPU-hidden TensorFlow, returns finite log likelihood and score,
and its fixed-branch finite-difference rows preserve the same branch hash.
This establishes only horizon-0, one-row, observation-term engineering wiring
under same-branch finite-difference stability; it does not establish
multistate transition score correctness, full-likelihood gradients, HMC
readiness, LEDH/P8p parity, scientific validity, or production readiness.

## Implementation Repairs During Phase 3

1. The P81 smoke originally hit `COMPLEXITY_GATE` because the d=18 degree-0
   grid has `2^18 = 262144` points and rank-1 TT evaluation estimates about
   151 MB.  The test-local `dense_matrix_byte_budget` was raised from 40 MB to
   192 MB.  This is a local smoke budget only; no default budget changed.
2. After the budget repair, TensorFlow failed in `tape.jacobian` pfor
   vectorization on the 262144-row batch.  The local model-log-density
   derivative helper now uses `tf.autodiff.ForwardAccumulator` for the single
   requested parameter direction.  This remains TensorFlow autodiff over model
   log-density terms; it is not a closed-form hand derivative.
3. Diagnostic strings were updated from
   `tensorflow_gradient_tape_for_model_log_density` to
   `tensorflow_forward_accumulator_for_model_log_density`.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` |
| Python | `3.11.14`, executable `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| TensorFlow / TFP | TensorFlow `2.19.1`, TensorFlow Probability `0.25.0` |
| CPU/GPU status | Deliberate CPU-hidden Phase 3 runs with `CUDA_VISIBLE_DEVICES=-1`; visible TensorFlow device list was CPU-only. |
| Data version | N/A; deterministic local model/test fixtures only. |
| Random seeds | Deterministic fixture ids and branch seeds from `tests/highdim/test_p81_analytical_sir_score.py` and `tests/highdim/test_fixed_branch_derivatives.py`; no stochastic sampler run. |
| Wall time | Focused P81 smoke approximately 54 s; combined focused rerun approximately 87 s. |
| Output artifacts | This result file and `docs/plans/bayesfilter-highdim-zhao-cui-p81-visible-execution-ledger-2026-06-21.md`; terminal logs were summarized rather than separately persisted. |
| Plan files | Master, runbook, Phase 3 subplan, and Phase 4 draft under `docs/plans/bayesfilter-highdim-zhao-cui-p81-*2026-06-21.md`. |
| Branch-hash evidence | Test assertions in `tests/highdim/test_p81_analytical_sir_score.py` and `tests/highdim/test_fixed_branch_derivatives.py` require `branch_hash_plus == branch_hash_base` and `branch_hash_minus == branch_hash_base` for valid finite-difference rows. |

## Checks Run

All checks were deliberate CPU-hidden runs with `CUDA_VISIBLE_DEVICES=-1`.

| Check | Result |
|---|---|
| `python -m py_compile bayesfilter/highdim/filtering.py bayesfilter/highdim/__init__.py bayesfilter/highdim/models.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py` | passed |
| `pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate_fixed_design_tt_score_path or scalar_fixed_design_tt_score_path"` | 2 passed, 17 deselected, 2 TFP deprecation warnings |
| `pytest -q tests/highdim/test_p81_analytical_sir_score.py` | 3 passed, 2 TFP deprecation warnings |
| `pytest -q tests/highdim/test_p46_multistate_zhaocui_adapter.py tests/highdim/test_p47_spatial_sir_filtering.py` | 10 passed, 2 TFP deprecation warnings |
| Combined focused rerun after backend-label cleanup | 5 passed, 17 deselected, 2 TFP deprecation warnings |

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Primary criterion | Passed: focused Phase 3 tests pass, d=18 horizon-0 smoke returns finite log likelihood/score, and finite-difference branch hashes match. |
| Veto diagnostics | No nonfinite values, branch-hash drift, parameter convention mismatch, global default change, or horizon-0 overclaim in the test contract. |
| Explanatory diagnostics | Budget repair was resource-gate only; JVP repair avoids TensorFlow pfor failure for single-direction local derivatives. |
| Main uncertainty | Full transition/filter likelihood correctness remains untested by this horizon-0 smoke. |
| Next justified action | Draft and review Phase 4 tiny GPU/TF32 smoke for the same candidate route. |
| Not concluded | Multistate transition score correctness, full d=18 filtering likelihood correctness, LEDH-PFPF-OT agreement, source-faithfulness, HMC readiness, posterior validity, scientific validity, GPU scaling, or default readiness. |

## Handoff

Claude Round 3 agreed that this Phase 3 result and the Phase 4 subplan preserve
the horizon-0 boundary and do not promote proxy evidence into full likelihood
correctness.  Phase 4 may begin with trusted/escalated GPU preflight only.
