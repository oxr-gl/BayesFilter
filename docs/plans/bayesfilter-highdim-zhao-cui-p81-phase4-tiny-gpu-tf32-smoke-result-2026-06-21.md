# P81 Phase 4 Result: Tiny GPU/TF32 Fixed-Branch/JVP-Backed Smoke

status: PHASE4_TRUSTED_GPU_VISIBLE_BACKEND_FEASIBILITY_SMOKE_PASSED_CLAUDE_AGREE
date: 2026-06-21

## Question

Does the Phase 3 fixed-branch/JVP-backed candidate route execute under
GPU-visible TensorFlow conditions on the bounded horizon-0 SIR d=18 smoke?

## Decision

Yes for the Phase 4 backend-feasibility question.  Trusted GPU preflight passed,
TensorFlow saw a GPU under escalated permissions, the tiny model-level
GPU-visible smoke passed, and the d=18 one-row horizon-0 observation-term score
smoke passed under GPU-visible TensorFlow.

This remains a one-row, horizon-0 engineering smoke.  It does not establish
full transition/filter likelihood correctness, LEDH-PFPF-OT agreement, HMC
readiness, posterior validity, scientific validity, production readiness, or
GPU scaling.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Primary criterion | Passed: GPU-visible tiny smoke and d=18 horizon-0 score smoke passed. |
| Veto diagnostics | No OOM, backend/device failure, nonfinite output, branch instability, tolerance failure, default change, or one-row overgeneralization was observed. |
| Comparator | Phase 3 CPU-hidden passing checks; Phase 4 is backend feasibility only, not numerical superiority. |
| Main uncertainty | Whether the candidate agrees with a stochastic LEDH-PFPF-OT comparator on full SIR d=18 value/gradient remains untested. |
| Next justified action | Draft Phase 5 small SIR d=18 value/gradient diagnostic with predeclared budget, seeds, candidate route, LEDH comparator boundary, and pass/veto criteria. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` |
| Python / TensorFlow | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python`, TensorFlow `2.19.1`; TFP warnings reported by pytest. |
| CPU/GPU status | GPU-visible trusted/escalated Phase 4 commands; no `CUDA_VISIBLE_DEVICES=-1` hiding. |
| GPU preflight | `nvidia-smi` saw NVIDIA GeForce RTX 4080-class GPU, driver `591.86`, CUDA `13.1`, 16376 MiB memory, no running processes listed. |
| TensorFlow device probe | TensorFlow saw `[CPU:0, GPU:0]` and `[GPU:0]` under trusted/escalated permissions; plugin-registration warnings appeared but did not veto. |
| Data version | N/A; deterministic local model/test fixtures only. |
| Seeds | Deterministic fixture ids and branch seeds inside `tests/highdim/test_p81_analytical_sir_score.py`; no stochastic sampler run. |
| Wall time | Tiny model-level smoke about 4.9 s pytest time; d=18 horizon-0 smoke about 52.4 s pytest time. |
| Result artifact | This file plus P81 execution ledger and Claude review ledger. |

## Commands Run

Trusted/escalated preflight:

```bash
nvidia-smi
MPLCONFIGDIR=/tmp python -c "import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices()); print(tf.config.list_physical_devices('GPU'))"
```

Trusted/escalated tiny model-level smoke:

```bash
MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "parameterized_zhao_cui_sir_matches_p8p_p79_theta_convention or parameterized_zhao_cui_sir_terms_are_sensitive"
```

Result: `2 passed, 1 deselected, 2 TFP deprecation warnings`.

Trusted/escalated d=18 horizon-0 score smoke:

```bash
MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "multistate_fixed_design_tt_score_path_runs_on_sir_d18_horizon0_observation_term"
```

Result: `1 passed, 2 deselected, 2 TFP deprecation warnings`.

## Branch-Stability Evidence

The d=18 smoke asserts finite log likelihood, finite score, valid
finite-difference rows, and equality of plus/minus/base fixed-branch hashes at
`tests/highdim/test_p81_analytical_sir_score.py:154`.  The tiny multistate
fixture regression asserts the same branch-hash stability at
`tests/highdim/test_fixed_branch_derivatives.py:662`.

## Non-Claims

Phase 4 does not claim full d=18 filtering likelihood correctness, transition
score correctness, LEDH-PFPF-OT value/gradient agreement, HMC readiness,
posterior validity, scientific validity, source-faithfulness, performance
scaling, TensorFlow environment health beyond these trusted commands, or
production default readiness.

Observed plugin-registration warnings in the TensorFlow probe and TFP
deprecation warnings in pytest were non-vetoing for this backend-feasibility
question only.  They were not adjudicated as globally harmless.

## Claude Review

Claude Phase 4 execution review returned `VERDICT: AGREE`, with guardrails:
keep the result scoped to trusted GPU-visible backend feasibility for the Phase
3 candidate at one-row horizon-0; preserve all non-claims; cite the GPU result
only because `nvidia-smi`, TensorFlow GPU probe, and both pytests were
trusted/escalated; keep horizon wording tight; and treat Phase 5 as drafting a
new reviewed subplan only.

## Handoff

Phase 5 should not run from this result alone.  It needs a dedicated reviewed
subplan that predeclares the small SIR d=18 value/gradient diagnostic budget,
GPU settings, random seeds, candidate route, LEDH-PFPF-OT comparator boundary,
primary pass/fail criteria, veto diagnostics, and artifact schema.
