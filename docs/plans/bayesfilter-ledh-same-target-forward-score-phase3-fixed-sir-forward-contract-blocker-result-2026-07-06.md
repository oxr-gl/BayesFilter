# Phase 3 Row Result: Fixed SIR Forward Contract Blocker

metadata_date: 2026-07-06
status: BLOCKED_FIXABLE_NEEDS_RUNNER_CONTRACT_PATCH
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 3
row_id: zhao_cui_spatial_sir_austria_j9_T20

## Question

Can the fixed spatial SIR row be admitted for same-target LEDH observed-data
likelihood value under the amended 3D `sir_log_scale_theta` contract?

## Finding

Not yet. The available July 3 fixed-SIR GPU artifact demonstrates a finite
N=10000 SIR LEDH execution with target-density correction, but it was produced
by the older fixed-parameter diagnostic runner and does not emit the Phase 2
forward contract or amended theta contract.

Artifact inspected:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.json`

Relevant fields:

- `schema_version = filter_bench.p8j_tf32_batched_actual_sir_probe.v1`
- `primary_pass_5x_runtime_gate = true`
- `finite_output = true`
- `sir_semantics.row_id = zhao_cui_spatial_sir_austria_j9_T20`
- `sir_semantics.target_density_used_for_correction = true`
- nonclaim includes `not exact likelihood correctness`
- no `forward_contract`
- no `theta_contract`

## Veto Triggered

The Phase 3 admission criterion requires row-specific same-target evidence
under the Phase 1/Phase 2 contract. The old artifact cannot by itself prove the
amended 3D free-theta target because it does not state:

- `target_scalar = observed_data_log_likelihood_estimator`
- `theta_coordinate_system = sir_log_scale_theta`
- `theta_dimension = 3`
- parameter order `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`
- truth theta `[0,0,0]`

## Fixable Repair

Patch the fixed-SIR value runner `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`
so it emits the Phase 2 `make_fixed_sir_logscale_forward_contract(...)`
manifest and explicit target scalar fields.

Then run a tiny CPU-hidden fixed-SIR metadata/value smoke. If that passes,
write a row-specific fixed-SIR forward value result that distinguishes:

- old N=10000 GPU runtime/value feasibility evidence;
- current amended theta/forward-contract metadata evidence;
- unresolved exact nonlinear likelihood correctness and score gates.

## Local Check

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py -q
```

Result: `10 passed, 2 warnings`.

## Nonclaims

- No fixed-SIR value admission yet.
- No fixed-SIR score admission.
- No exact nonlinear likelihood correctness claim.
- No Zhao-Cui TT/SIRT source-faithfulness claim for the log-scale inference
  theta extension.
- No HMC readiness or posterior correctness claim.
