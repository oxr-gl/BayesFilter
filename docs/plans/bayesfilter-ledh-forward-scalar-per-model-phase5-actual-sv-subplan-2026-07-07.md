# Phase 5 Subplan: Actual-SV Forward Scalar Target Bridge

metadata_date: 2026-07-07
status: `DRAFT_AFTER_PHASE4`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 5

## Phase Objective

Build, admit, or explicitly block an executable same-target observed-data LEDH
forward scalar artifact for the actual stochastic-volatility row:

```text
zhao_cui_sv_actual_nongaussian_T1000
```

This phase is forward-scalar-only. It must not implement scores, admit scores,
or rebuild the leaderboard.

Target scalar: `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

The row target must be the transformed actual-SV target, not the KSC surrogate
and not an augmented-noise Gaussian-closure scalar.

## Entry Conditions Inherited From Previous Phase

- Phase 1 schema guard passed after theta-equality repair.
- Phase 2 LGSSM canonical artifact validates locally.
- Phase 3 fixed SIR canonical artifact validates locally under
  `sir_log_scale_theta`.
- Phase 4 predator-prey canonical artifact validates locally with
  `require_admitted=True`.
- Phase 4 local checks passed:
  `30 passed, 2 warnings`.
- Phase 4 did not admit actual-SV, generalized-SV, KSC, or any score.
- Phase 4 result and this subplan must pass read-only review before execution.

## Required Artifacts

- Phase 5 result or blocker result:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-result-2026-07-07.md`
- If admitted, canonical actual-SV executable schema artifact:
  `docs/plans/ledh-phase5-actual-sv-forward-scalar-artifact-2026-07-07.json`
- If admitted, optional markdown summary:
  `docs/plans/ledh-phase5-actual-sv-forward-scalar-artifact-2026-07-07.md`
- If admitted, mandatory actual-SV artifact replay test:
  `tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_artifact.py`
- Phase 6 generalized-SV subplan:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase6-generalized-sv-subplan-2026-07-07.md`
- Phase 5 review bundle:
  `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase5-review-bundle-2026-07-07.md`

## Required Checks/Tests/Reviews

If a canonical actual-SV artifact is produced, required local checks are:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_artifact.py -q
```

If the phase blocks before an artifact can be produced, required local checks
are the existing passed replay/guard set through Phase 4 plus any focused test
for the blocker guard that is added in this phase.

Required review:

- bounded read-only review of Phase 5 result/blocker and Phase 6 subplan before
  Phase 6 starts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the actual-SV row produce an executable same-target transformed observed-data log likelihood artifact under the shared schema? |
| Baseline/comparator | Corrected actual-SV single-target derivation note, `make_actual_sv_forward_contract(...)`, `StochasticVolatilitySSM`, existing `_dpf_sv_callbacks(...)`, any current LEDH runner code, and Phase 1 schema validator. |
| Primary criterion | A canonical actual-SV artifact validates with `require_admitted=True`, finite `log_likelihood_by_seed`, row id `zhao_cui_sv_actual_nongaussian_T1000`, theta coordinate `synthetic_unconstrained`, theta values `(0.2533471031357997,-0.916290731874155)`, full-row scale `T=1000,N=10000`, batch seeds `[81120,81121,81122,81123,81124]`, and a target observation policy matching the transformed actual-SV row contract. |
| Veto diagnostics | Raw-likelihood-corrected scalar admitted without reviewed transformed-target bridge; KSC surrogate borrowed as actual-SV evidence; augmented-noise Gaussian-closure scalar used as same-target evidence; missing `log_likelihood_by_seed`; wrong theta; target density not used for correction; metadata-only or callback-only evidence; score fields used as value evidence; runtime or finite output used without schema validation. |
| Explanatory diagnostics | Runtime, compile time, memory, ESS, tiny-prefix checks, raw-likelihood callback traces, constant-offset derivation notes, and non-LEDH references. |
| Not concluded | No score admission, score correctness, KSC admission, generalized-SV admission, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |
| Artifact | Phase 5 result/blocker, canonical actual-SV schema artifact if admitted, mandatory replay test if admitted, Phase 6 subplan. |

## Step-By-Step Plan

1. Inventory actual-SV target sources:
   - `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`;
   - `bayesfilter/highdim/ledh_forward_contract.py::make_actual_sv_forward_contract`;
   - `bayesfilter/highdim/models.py::StochasticVolatilitySSM`;
   - `bayesfilter/highdim/sv_mixture_cut4.py::transformed_sv_observations`;
   - `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py::_dpf_sv_callbacks`.
2. Freeze the row contract before execution:
   - row id `zhao_cui_sv_actual_nongaussian_T1000`;
   - theta coordinate `synthetic_unconstrained`;
   - theta values `[0.2533471031357997, -0.916290731874155]`;
   - horizon `1000`;
   - particle count `10000`;
   - batch seeds `[81120,81121,81122,81123,81124]`;
   - target observation policy `transformed_actual_sv_log_y_square`.
3. Decide and document the target bridge before any full-row run:
   - admissible path A: implement an LEDH value adapter whose correction
     evaluates the exact transformed actual-SV observation law for
     `z_t = log(y_t^2)` under the Phase 1 contract;
   - admissible path B: write and locally review a constant-offset bridge that
     proves the executed raw-likelihood-corrected scalar is the same declared
     transformed target up to an explicitly handled parameter-independent
     constant;
   - if neither path is explicit, write a blocker result and do not run the
     full row.
4. If an executable candidate path exists, run a tiny smoke artifact first:
   - small `T`, small `N`, one seed;
   - status must be `tiny_executed_not_full_row`;
   - no admission claim.
5. If the tiny path validates and no target-bridge veto remains, run the
   trusted GPU/XLA full-row N=10000 artifact.
6. Validate the canonical artifact with:
   - `validate_ledh_forward_scalar_artifact(..., expected_row_id=ACTUAL_SV_ROW_ID, require_admitted=True)`.
7. Add a mandatory replay test that reads the actual Phase 5 canonical JSON
   artifact from disk and validates it with `require_admitted=True`.
8. If full-row canonical artifact cannot be produced, write a blocker result
   instead of admitting actual-SV.
9. Draft Phase 6 generalized-SV subplan.
10. Run required local checks.
11. Send Phase 5 result/blocker and Phase 6 subplan for bounded read-only
    review.

## Forbidden Claims/Actions

- Do not use KSC surrogate evidence as actual-SV evidence.
- Do not admit raw-likelihood-corrected LEDH output as the transformed row
  target without a reviewed bridge written before the full-row run.
- Do not admit the augmented-noise Gaussian-closure scalar as same-target
  actual-SV evidence.
- Do not change actual-SV row target, theta, seed list, horizon, or particle
  count after seeing results.
- Do not implement or admit scores.
- Do not rebuild the leaderboard.
- Do not claim HMC readiness, posterior correctness, scientific superiority,
  or runtime ranking.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- either the canonical actual-SV artifact validates with
  `require_admitted=True`, or a blocker result explains why it cannot yet be
  produced;
- any admitted artifact has an automated replay test reading the actual Phase 5
  canonical JSON artifact from disk;
- Phase 5 result records the target bridge or blocker explicitly;
- Phase 5 local checks pass or the blocker result explains why artifact replay
  checks cannot apply;
- Phase 6 generalized-SV subplan is drafted;
- read-only review agrees, or a documented fallback Codex review accepts the
  boundary.

## Stop Conditions

Stop and update the visible stop handoff if:

- the phase cannot explicitly bind the executed scalar to the transformed
  actual-SV row target;
- KSC or augmented-noise Gaussian-closure evidence is the only available
  executable evidence;
- the target-density correction is absent or ambiguous;
- `log_likelihood_by_seed` is missing or nonfinite;
- theta values differ from `[0.2533471031357997, -0.916290731874155]`;
- the canonical artifact fails Phase 1 validation;
- the phase would need score work;
- a human approval boundary is reached.

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Phase starts by freezing the transformed actual-SV target and the prior raw-vs-transformed bridge blocker. |
| Proxy metrics | Runtime, memory, and finite output cannot pass without target bridge plus schema validation. |
| Missing stop conditions | Stop conditions cover missing target bridge, surrogate borrowing, wrong theta, missing correction, failed validation, and score creep. |
| Hidden assumptions | Target bridge must be decided before full-row execution. |
| Artifact mismatch | Required output is a canonical schema artifact or blocker result, not a leaderboard rebuild. |

Audit status: passed for Phase 5 subplan draft.
