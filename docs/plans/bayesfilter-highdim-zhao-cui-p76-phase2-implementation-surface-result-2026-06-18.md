# P76 Phase 2 Result: Implementation Surface And Test Plan

metadata_date: 2026-06-18
status: PHASE2_PASSED_CLAUDE_AGREE_READY_FOR_PHASE3
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase1-mathematical-ukf-initializer-result-2026-06-18.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 2 names the concrete implementation and test surface for the Phase 1
initializer:

`ukf_whitened_gaussian_sqrt_projection_v1`.

No implementation code is edited in Phase 2.  No training diagnostic, GPU run,
large mini-batch pilot, default change, or source-faithfulness claim is made.

## Skeptical Audit

The Phase 2 plan survives the skeptical audit with the following controls.

| Risk checked | Phase 2 control |
| --- | --- |
| Wrong baseline | The live implementation target is the Phase 1 UKF-whitened initializer, not P75 source-route prefit. |
| Proxy metric promoted to gate | Phase 2 runs no empirical metric.  Phase 3 tests are shape/finite/contract tests only. |
| Missing stop condition | Phase 3 blocks on missing UKF moments, invalid covariance, degree guard failure, audit leakage, NumPy-backend drift, or source-prefit substitution. |
| Unfair comparison | No ladder or method comparison is run. |
| Hidden assumption | The first implementation supports the Phase 1 block-diagonal adjacent covariance and uniform internal TT rank only. |
| Stale context | Phase 2 reads Phase 1, `ukf_scout.py`, `bases.py`, `stochastic_density_training.py`, and P70 seeded-channel design. |
| Environment mismatch | Phase 3 tests are CPU-only with `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA interpretation is allowed. |
| Artifact mismatch | Required artifacts are a surface result and an implementation subplan, not a successful initializer run. |

## Implementation Surface Decision

Create a new opt-in module:

- `bayesfilter/highdim/ukf_initializer.py`

Do not export it from `bayesfilter/highdim/__init__.py` in Phase 3.  The
module is imported explicitly by tests and future P76 scripts.  This avoids
presenting the initializer as a default highdim API and keeps it separate from
P75 source-prefit helpers.

Create focused tests:

- `tests/highdim/test_p76_ukf_initializer.py`

The implementation may import the existing TensorFlow objects:

- `ProductBasis`, `LegendreBasis1D`, and `BoundedInterval` from
  `bayesfilter.highdim.bases`;
- `TTCore` from `bayesfilter.highdim.tt`;
- `UKFScoutResult` and `P52_UKF_SCOUT_CLAIM` from
  `bayesfilter.highdim.ukf_scout`;
- `TrainableFunctionalTT` and `P75TrainableTTConfig` only in tests or optional
  helper checks, not as a required coupling.

Phase 3 may reuse the TensorFlow Gauss--Legendre construction already present
in `bayesfilter/highdim/filtering.py`, or implement the same Golub--Welsch
construction locally in the new module.  It must not use NumPy as the
BayesFilter implementation backend.

## Exact Public Surface Inside The Opt-In Module

Phase 3 should implement the following names.

### Constants

- `P76_UKF_INITIALIZER_RULE =
  "ukf_whitened_gaussian_sqrt_projection_v1"`
- `P76_ROUTE_CLASSIFICATION = "extension_or_invention"`
- `P76_SCHEMA_VERSION = "p76_ukf_initializer.v1"`
- `P76_NONCLAIMS`, including:
  - `"scout_not_truth"`;
  - `"not source-faithful Zhao-Cui"`;
  - `"not lower-gate repair evidence"`;
  - `"not validation evidence"`;
  - `"not HMC readiness evidence"`;
  - `"not large-pilot evidence"`.

### Dataclasses

- `P76UKFInitializerConfig`
  - `product_basis: ProductBasis`
  - `ranks: tuple[int, ...]`
  - `time_index: int = 1`
  - `gamma: float = 4.0`
  - `covariance_abs_floor: float = 1e-9`
  - `covariance_rel_floor: float = 1e-8`
  - `quadrature_order: int = 32`
  - `seed_epsilon: float = 1e-6`
  - `require_curvature_degree: bool = True`

- `P76AdjacentUKFMoments`
  - `center: tf.Tensor`
  - `covariance: tf.Tensor`
  - `time_index: int`
  - `previous_time_index: int`
  - `claim_class: str`

- `P76StabilizedCovariance`
  - `covariance: tf.Tensor`
  - `eigenvectors: tf.Tensor`
  - `raw_eigenvalues: tf.Tensor`
  - `floored_eigenvalues: tf.Tensor`
  - `eigen_floor: tf.Tensor`

- `P76UKFInitializerResult`
  - `cores: tuple[TTCore, ...]`
  - `center: tf.Tensor`
  - `linear_map: tf.Tensor`
  - `stabilized_covariance: tf.Tensor`
  - `raw_eigenvalues: tf.Tensor`
  - `floored_eigenvalues: tf.Tensor`
  - `projection_coefficients: tuple[tf.Tensor, ...]`
  - `manifest: Mapping[str, object]`
  - `status: str`
  - `nonclaims: tuple[str, ...]`

### Functions

- `p76_adjacent_moments_from_scout(scout: UKFScoutResult, *, time_index: int)`
  - Builds \(m_A^U\) and block-diagonal \(P_A^U\).
  - For `time_index == 1`, uses `mean_path[0]` and `covariance_path[0]` for
    the previous block.
  - Blocks if moments are absent, nonfinite, or not `scout_not_truth`.

- `p76_stabilize_covariance(covariance, *, abs_floor, rel_floor)`
  - Symmetrizes covariance.
  - Floors eigenvalues by
    \(\max\{\epsilon_{\rm abs},\epsilon_{\rm rel}\max_i|\lambda_i|\}\).
  - Returns finite SPD covariance diagnostics.

- `p76_local_frame_from_moments(moments, config)`
  - Builds \(L_U=\gamma V\operatorname{diag}(\sqrt{\bar\lambda_i})\).
  - Returns the physical center and linear map.

- `p76_gaussian_sqrt_projection_coefficients(product_basis, *, gamma, quadrature_order)`
  - Computes one-dimensional \(L^2\) projection coefficients of
    \(\exp(-\gamma^2z^2/4)\) under each basis's active reference/mass
    convention using TensorFlow quadrature.

- `p76_rank_one_ukf_sqrt_cores(product_basis, *, gamma, quadrature_order)`
  - Builds rank-one TT cores from the one-dimensional projection coefficients.

- `p76_embed_rank_one_with_seeded_channels(rank_one_coefficients, *, ranks, seed_epsilon)`
  - Embeds the rank-one projection in channel 0.
  - Adds deterministic small extra-channel paths following the P70
    `fixed_hmc_seeded_channel_paths_v1` idea.
  - Supports the first P76 target: uniform internal rank tuple
    \((1,R,\ldots,R,1)\).  Nonuniform ranks are a reviewed extension.

- `p76_build_ukf_initializer(scout, config)`
  - Runs all steps and returns `P76UKFInitializerResult`.

- `p76_initializer_manifest_payload(result_or_inputs)`
  - Produces a JSON-friendly manifest summary.

## Validation Rules For Phase 3

Phase 3 implementation must validate:

- `config.product_basis` is a `ProductBasis`;
- `ranks` length equals `dimension + 1`;
- `ranks[0] == ranks[-1] == 1`;
- internal ranks are positive and uniform for the first implementation;
- if `require_curvature_degree` is true, every basis has `max_degree >= 2`;
- `gamma`, covariance floors, quadrature order, and seed epsilon are positive;
- `quadrature_order >= max(8, 2 * max_degree + 4)`;
- UKF claim class is exactly `scout_not_truth`;
- no input record has audit role because the initializer accepts no sample
  cloud;
- output cores are finite `tf.float64` tensors of shape
  `[ranks[k], basis_dim[k], ranks[k+1]]`.

## Manifest Fields

The result manifest must include:

- schema version;
- initializer rule;
- route classification;
- status;
- `scout_not_truth` claim class and nonclaims;
- time index and previous time index;
- dimension and basis dimensions;
- rank tuple;
- gamma;
- covariance floors and eigenvalue floor used;
- raw and floored eigenvalue ranges;
- center dimension;
- linear-map shape and finite/SPD status;
- quadrature order;
- seed epsilon;
- degree guard status;
- `source_route_prefit_used: false`;
- `audit_data_used: false`;
- `default_behavior_changed: false`.

## Focused Tests For Phase 3

`tests/highdim/test_p76_ukf_initializer.py` must include at least:

1. synthetic `UKFScoutResult` adjacent moment extraction builds the expected
   center and block-diagonal covariance from `mean_path[time_index]`,
   `covariance_path[time_index]`, `mean_path[time_index-1]`, and
   `covariance_path[time_index-1]`; for `time_index == 1`, the test must
   explicitly assert that the previous block is `mean_path[0]` and
   `covariance_path[0]`;
2. covariance stabilization floors a negative or tiny eigenvalue and returns
   finite SPD covariance;
3. degree-one `ProductBasis` raises when `require_curvature_degree=True`;
4. degree-two rank-one initializer returns one core per dimension with finite
   shape `[1, 3, 1]`;
5. degree-two rank-four initializer returns finite embedded cores with shapes
   `[1,3,4]`, internal `[4,3,4]`, and `[4,3,1]`;
6. manifest records `source_route_prefit_used: false`,
   `audit_data_used: false`, `scout_not_truth`, and the initializer rule;
7. initialized cores can instantiate `TrainableFunctionalTT` and produce finite
   `rho_theta`, `normalizer`, and `log_density` on a tiny CPU-only point set;
8. a `P75ObjectiveBatch` with audit records is still rejected before any
   train step, preserving audit separation at the downstream training surface;
9. a static check or targeted assertion ensures the initializer module does not
   call `square_root_prefit_step`, `square_root_prefit_objective`, or
   `source_guided_prefit`.

## Phase 3 CPU-Only Commands

Phase 3 must run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p75_stochastic_density_training.py
rg -n "square_root_prefit|source_guided_prefit|source-route prefit" bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py
git diff --check -- bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md
```

The `rg` command is expected to return no implementation hits in
`ukf_initializer.py`.  If it returns a docstring/nonclaim hit, Phase 3 must
record why the hit is not a call path; otherwise block.

## Phase 3 Handoff

Phase 3 may edit only:

- `bayesfilter/highdim/ukf_initializer.py`;
- `tests/highdim/test_p76_ukf_initializer.py`;
- P76 result/subplan/ledger/runbook artifacts under `docs/plans`.

Phase 3 must not edit:

- `bayesfilter/highdim/__init__.py`;
- P75 source-prefit code;
- default training or filtering behavior;
- unrelated dirty files.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Proceed to Phase 3 implementation | Satisfied by named module, API, tests, commands, and boundaries | No Phase 2 veto identified locally | Projection helper details and test exactness remain implementation questions | Review this result and Phase 3 subplan with Claude, then implement if agreed | No empirical success, no lower-gate repair, no validation/HMC readiness, no large pilot |
