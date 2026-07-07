# Phase 5 Repair Subplan: Exact Transformed Actual-SV Adapter Smoke

metadata_date: 2026-07-07
status: `DRAFT_PRE_REVIEW`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
parent_phase: 5

## Phase Objective

Implement and smoke-test a tiny executable LEDH adapter for the actual-SV row
before any full `N=10000,T=1000` run.

The adapter must target the exact transformed actual-SV observed-data scalar:

```text
z_t = log(y_t^2)
z_t - 2 log(beta) - h_t ~ log(chi_square_1)
```

The computed scalar is the observed-data log likelihood estimator reported as
`log_likelihood`. This repair subphase is forward-scalar-only and tiny-only. It
must not admit the full actual-SV row.

## Entry Conditions Inherited From Previous Phase

- Phase 1 executable schema guard exists and rejects metadata-only,
  callback-only, wrong-target, and actual-SV/KSC cross-use artifacts.
- Phase 2 LGSSM artifact validates locally.
- Phase 3 fixed SIR artifact validates locally.
- Phase 4 predator-prey artifact validates locally and passed read-only
  review.
- Phase 5 target bridge inventory found that legacy raw-Gaussian
  `_dpf_sv_callbacks` cannot be admitted for the declared actual-SV target.
- No full actual-SV `N=10000,T=1000` run has been launched.

## Required Artifacts

- This repair subplan:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-adapter-smoke-subplan-2026-07-07.md`
- Tiny runner:
  `docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py`
- Tiny executable artifact:
  `docs/plans/ledh-phase5-actual-sv-forward-scalar-tiny-smoke-artifact-2026-07-07.json`
- Tiny markdown summary:
  `docs/plans/ledh-phase5-actual-sv-forward-scalar-tiny-smoke-artifact-2026-07-07.md`
- Tiny artifact replay test:
  `tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_tiny_artifact.py`
- Repair result:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-adapter-smoke-result-2026-07-07.md`
- Plan/review bundle:
  `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-adapter-smoke-plan-review-bundle-2026-07-07.md`

## Required Checks/Tests/Reviews

Before code execution:

```text
bash ~/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/BayesFilter \
  --review-name ledh-phase5-actual-sv-adapter-smoke-plan \
  --bundle /home/chakwong/BayesFilter/docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-adapter-smoke-plan-review-bundle-2026-07-07.md \
  --probe-timeout 90 --timeout-seconds 180 --max-retries 1 --allow-bounded-fallback
```

After implementation:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile \
  docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py
```

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_tiny_artifact.py -q
```

Tiny trusted smoke run:

```text
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py \
  --time-steps 4 \
  --num-particles 128 \
  --batch-seeds 81120 \
  --transport-policy active-all \
  --sinkhorn-iterations 2 \
  --row-chunk-size 64 \
  --col-chunk-size 64 \
  --particle-chunk-size 64 \
  --history-mode full \
  --warmups 0 \
  --repeats 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/plans/ledh-phase5-actual-sv-forward-scalar-tiny-smoke-artifact-2026-07-07.json \
  --markdown-output docs/plans/ledh-phase5-actual-sv-forward-scalar-tiny-smoke-artifact-2026-07-07.md
```

The trusted smoke run must be escalated because it uses GPU/CUDA/XLA.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a tiny actual-SV LEDH adapter execute the exact transformed observed-data target correction before a full-row run? |
| Baseline/comparator | `make_actual_sv_forward_contract(...)`, `StochasticVolatilitySSM`, `ExactTransformedSVSSM`, `exact_transformed_sv_observations`, `exact_log_chi_square_log_density`, and Phase 1 validator. |
| Primary criterion | Tiny JSON artifact validates with `validate_ledh_forward_scalar_artifact(..., expected_row_id=ACTUAL_SV_ROW_ID)` and has `admission_status=tiny_executed_not_full_row`, finite `log_likelihood_by_seed`, row id `zhao_cui_sv_actual_nongaussian_T1000`, theta coordinate `synthetic_unconstrained`, theta values `[0.2533471031357997,-0.916290731874155]`, `target_observation_policy=transformed_actual_sv_log_y_square`, and `target_density_used_for_correction=true`. |
| Veto diagnostics | Any full-row admission claim; any full `N=10000,T=1000` run; raw Gaussian observation density used as the target correction; KSC finite-mixture density used as actual-SV evidence; augmented-noise Gaussian-closure target used; transform offset other than exact `0`; target density not used for correction; score fields used as value evidence; metadata-only or callback-only evidence. |
| Explanatory diagnostics | Runtime, compile time, memory, ESS, target-vs-flow policy names, tiny scale, and MC variability. |
| Not concluded | No actual-SV full-row admission, no score admission, no score correctness, no generalized-SV admission, no KSC admission, no HMC readiness, no posterior correctness, no scientific superiority, and no runtime ranking. |
| Artifact | Tiny JSON artifact, tiny replay test, repair result, and ledger entry. |

## Implementation Plan

1. Implement `docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py` as
   a tiny-capable row runner.
2. Load the raw actual-SV dataset from `_sv_dataset(81101)`.
3. Transform observations exactly with `exact_transformed_sv_observations`; do
   not use `log(y^2 + offset)`.
4. Freeze theta to the Phase 1 contract:
   `[0.2533471031357997, -0.916290731874155]`.
5. Generate initial particles from the stationary actual-SV prior using the
   batch seed list.
6. In the row-specific value core, use a time-dependent Gaussian proposal:
   - at `t=0`, proposal mean `0` and covariance
     `sigma^2/(1-gamma^2)`;
   - at `t>0`, proposal mean `gamma*x_{t-1}` and covariance `sigma^2`.
7. Use LEDH flow only as a proposal surface:
   - flow observation function `x -> x + 2 log(beta)`;
   - Jacobian `1`;
   - residual `z_t - (x + 2 log(beta))`;
   - Gaussianized flow observation covariance fixed by argument.
8. Correct with the exact target density:
   - at `t=0`, `initial_log_density(theta, x_0)`;
   - at `t>0`, `transition_log_density(theta, x_{t-1}, x_t)`;
   - all `t`, `exact_log_chi_square_log_density(z_t - 2log(beta) - x_t)`.
9. Use streaming/chunked OT through `batched_annealed_transport_core_tf`, not a
   dense materialized transport matrix.
10. Emit a tiny executable artifact with `admission_status` exactly
    `tiny_executed_not_full_row`.
11. Add a replay test that reads the tiny JSON artifact and validates it
    without `require_admitted=True`; the test must also assert that
    `require_admitted=True` rejects the tiny artifact.
12. Run the tiny GPU smoke, replay tests, and write the repair result.

## Forbidden Claims/Actions

- Do not run the full actual-SV `N=10000,T=1000` row in this subphase.
- Do not set `admission_status=n10000_same_target_value_admitted`.
- Do not use raw Gaussian observation likelihood as target correction.
- Do not use KSC finite-mixture likelihood as actual-SV target evidence.
- Do not use augmented-noise Gaussian-closure evidence.
- Do not use a positive log-square transform offset.
- Do not implement or admit scores.
- Do not rebuild the leaderboard.
- Do not claim HMC readiness, posterior correctness, scientific superiority,
  or runtime ranking.

## Exact Next-Phase Handoff Conditions

This repair subphase may hand back to Phase 5 full-row planning only if:

- the tiny runner exists and compiles;
- the tiny GPU smoke artifact validates under Phase 1 schema without
  admission;
- the tiny replay test passes and confirms `require_admitted=True` rejects the
  tiny artifact;
- the repair result records the exact target bridge and the no-full-row
  boundary;
- read-only review of the implementation/result agrees or a documented
  fallback review is used only after Claude is unavailable or policy-blocked.

## Stop Conditions

Stop and write a blocker result if:

- the exact transformed target cannot be represented without an offset;
- the adapter cannot use target density in the correction;
- the only executable path is the legacy raw-Gaussian target correction;
- the tiny artifact is nonfinite or fails schema validation;
- the implementation would require score work;
- a full-row run is needed to answer the adapter-smoke question;
- a human approval boundary is reached.

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | The plan binds to `ExactTransformedSVSSM`/exact log-chi-square rather than `_dpf_sv_callbacks` raw Gaussian likelihood. |
| Proxy metrics | Tiny runtime and finite output cannot admit the row; schema validation plus tiny rejection under `require_admitted=True` is required. |
| Missing stop condition | The plan stops on missing exact target bridge, raw/KSC/augmented substitution, nonfinite artifact, score creep, or accidental full-row need. |
| Hidden assumption | The time-0 proposal/target distinction is explicit: initial prior at `t=0`, transition density only for `t>0`. |
| Artifact mismatch | Output is a tiny smoke artifact and repair result, not a full-row admission artifact. |
| Environment mismatch | GPU smoke must run trusted/escalated; CPU-only compile/tests hide GPU intentionally. |

Audit status: passed for pre-review. Execution may start only after bounded
read-only review agrees or a documented Claude-unavailable fallback review is
completed.
