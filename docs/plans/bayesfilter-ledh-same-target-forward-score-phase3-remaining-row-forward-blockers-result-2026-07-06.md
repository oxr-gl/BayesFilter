# Phase 3 Row Result: Remaining Forward Value Blockers

metadata_date: 2026-07-06
status: BLOCKED_ROWS_RECORDED_WITH_VALID_TARGET_CONTRACTS
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 3

## Question

Can the remaining high-dimensional LEDH rows be admitted for same-target
observed-data likelihood value in Phase 3?

## Decision

Not yet. The Phase 1 target contracts are now representable through the Phase 2
forward contract API, but there is no reviewed current LEDH-PFPF-OT runner
artifact that admits these rows.

The rows remain blocked for value and score:

- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

## Contract Status

The new Phase 2 contract factories validate these target identities:

| Row | Theta coordinate | Parameter order | Target policy |
| --- | --- | --- | --- |
| `zhao_cui_sv_actual_nongaussian_T1000` | `synthetic_unconstrained` | `(gamma_unconstrained, log_beta)` | transformed actual-SV row target |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `synthetic_unconstrained` | `(gamma_unconstrained, log_beta)` | KSC finite-mixture surrogate likelihood |
| `zhao_cui_predator_prey_T20` | `physical` | `(r, K, a, s, u, v)` | additive-Gaussian predator-prey likelihood |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `source_route_active_transformed_prior_mean` | `(gamma_unconstrained, log_tau, mu)` | frozen generalized-SV source-row likelihood |

## Blockers By Row

### Actual SV

Current evidence:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:_dpf_sv_callbacks`
  has a legacy DPF callback.
- The callback uses transformed observations for the LEDH flow and raw SV
  observation density for correction.
- Prior P8D status recorded LEDH Algorithm 1 failure:
  `FloatingPointError: Algorithm 1 corrected log weights are non-finite`.

Blocker:

- No reviewed current GPU/XLA streaming LEDH-PFPF-OT row adapter proves that
  the executed scalar is the Phase 1 actual-SV target.

### KSC SV

Current evidence:

- deterministic KSC mixture value routes exist for non-LEDH algorithms.
- the P8D DPF callback registry does not expose a KSC-specific LEDH row route.

Blocker:

- No reviewed LEDH adapter exists for the KSC finite-mixture surrogate target.
  Actual-SV callbacks must not be reused as KSC evidence.

### Predator-Prey

Current evidence:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:_dpf_predator_prey_callbacks`
  has a legacy DPF callback.
- P8D has small five-seed Algorithm 1 value-only evidence.

Blocker:

- No reviewed current streaming LEDH-PFPF-OT row adapter proves same-target
  predator-prey T20 execution under the Phase 2 contract.
- Legacy callback existence and UKF value status are not enough.

### Generalized SV

Current evidence:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:_dpf_generalized_sv_callbacks`
  has a legacy DPF callback.
- The callback labels its LEDH observation adapter as a BayesFilter extension
  for non-Gaussian generalized-SV flow and not same-target transformed-SV
  evidence.
- Prior P8D status recorded LEDH Algorithm 1 failure:
  `FloatingPointError: Algorithm 1 corrected log weights are non-finite`.

Blocker:

- No reviewed current streaming LEDH-PFPF-OT row adapter proves the requested
  generalized-SV source-row target. Native-oracle, actual-SV, KSC, or auxiliary
  evidence cannot substitute.

## Local Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py -q
```

Result: `12 passed, 2 warnings`.

```text
python -m py_compile \
  bayesfilter/highdim/ledh_forward_contract.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_ledh_phase3_forward_admission.py
```

Result: passed.

## Nonclaims

- No value admission for these four rows.
- No score admission for these four rows.
- No HMC readiness, posterior correctness, scientific superiority, or runtime
  ranking claim.
- No claim that legacy Algorithm 1 DPF callback existence is equivalent to a
  current streaming LEDH-PFPF-OT same-target value adapter.

## Repair Handoff

To admit any of these rows later, create a row-specific adapter/runner that
emits the Phase 2 forward contract, runs a tiny fixed-randomness value check,
and then runs trusted GPU/XLA value evidence for the production row. Only after
that may Phase 4 score implementation begin for the row.
