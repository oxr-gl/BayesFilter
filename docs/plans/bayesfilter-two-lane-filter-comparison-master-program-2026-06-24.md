# Master Program: Two-Lane SGQF / UKF / Zhao-Cui Comparison Governance

metadata_date: 2026-06-24
program_id: two-lane-filter-comparison
status: PROGRAM_ACTIVE_TWO_LANE_COMPARISON_GOVERNANCE

## Date

2026-06-24

## Status

`PROGRAM_ACTIVE_TWO_LANE_COMPARISON_GOVERNANCE`

## Purpose

This program governs a **new** comparison effort for `fixed_sgqf`, `ukf`, and
`zhao_cui_scalar_or_multistate`, with `cut4` included **only** where the row is
low-dimensional and same-target.

This is **not** a continuation of the completed fixed-SGQF promotion-governance
program. That program is already closed. This program reuses the existing
benchmark governance backbone to express a new comparison contract with explicit
lane boundaries, stop rules, and nonclaims.

The program must:

1. split the comparison into a **low-dimensional same-target lane** and a
   **high-dimensional / source-scope lane**;
2. keep `cut4` confined to the low-dimensional lane;
3. keep **actual transformed SV** and **KSC surrogate SV** in separate target
   identities and separate ranking tables;
4. preserve the rule that **SGQF autodiff is diagnostic-only** for promoted
   score claims;
5. preserve the rule that blocked SGQF families remain blocked unless a new
   reviewed same-target route is actually added;
6. keep preflight and runner matrices as **governance/status artifacts**, not
   performance evidence.

## Governing Artifacts

### Immediate policy and reset lineage
- `docs/plans/bayesfilter-fixed-sgqf-promotion-closeout-and-two-lane-comparison-reset-memo-2026-06-23.md`
- `/home/chakwong/.claude/plans/partitioned-questing-valley.md`

### Benchmark governance backbone to extend
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gradient-semantics-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json`

### Comparator-honesty template
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-cut4-statistical-comparator-master-plan-2026-06-06.md`

## Lane Contract

### Lane A — low-dimensional same-target comparison

Allowed algorithms:
- `fixed_sgqf`
- `ukf`
- `cut4`
- `zhao_cui_scalar_or_multistate`

Representative rankable rows:
- `lgssm_exact_kalman_dim_1_2_3`
- `p44_cubic_additive_gaussian_dim_1_2_3`
- `p44_quadratic_observation_dim_1_2_3`
- `p44_nonlinear_transition_h2_dim_1_2_3`
- `sv_ksc_gaussian_mixture_surrogate_dim_1_2_3`

Diagnostic-only low-dimensional row:
- `p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3`

Status-only / blocked low-dimensional rows remain explicit and must not silently
vanish.

### Lane B — high-dimensional / source-scope comparison

Allowed algorithms:
- `fixed_sgqf`
- `ukf`
- `zhao_cui_scalar_or_multistate`

Explicitly excluded from this lane:
- `cut4`

Representative governed rows:
- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
- `zhao_cui_spatial_sir_austria_j9_T20`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

## Hard Constraints

1. **CUT4 remains low-dimensional only.**
   No high-dimensional comparison table may include `cut4`.

2. **Actual transformed SV and KSC surrogate SV remain separate.**
   They may share truth values or source lineage, but they must not be merged
   into one ranking table or one generic “SV overall” cell family.

3. **SGQF autodiff remains diagnostic-only.**
   Promoted SGQF score claims still require explicit analytical routes.

4. **Blocked SGQF families stay blocked by default.**
   Under the current lane, actual transformed SV, spatial SIR, predator-prey,
   and generalized SV do not become SGQF comparison-ready without a new reviewed
   same-target route.

5. **No silent holes.**
   Unsupported or blocked cells must emit structured statuses rather than being
   omitted.

6. **Governance artifacts are not performance evidence.**
   Preflight and runner matrices remain status/governance surfaces even after the
   lane split.

## Implementation Surface

### New artifact
- this master program

### Existing machine-readable artifacts to refresh
- target registry
- source-paper scope contract
- gradient semantics
- deterministic filter coverage
- preflight matrix
- P8 runner matrices

### Tests that should guard the contract
- `tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`

## Skeptical Plan Audit

Status: `PASS_TO_GOVERNANCE_IMPLEMENTATION`

- **Wrong baseline risk:** avoided if the existing registry / source-scope /
  preflight / P8 stack remains the baseline.
- **Proxy promotion risk:** avoided only if preflight and runner artifacts keep
  their explicit `not_performance_evidence` semantics.
- **Hidden assumption risk:** current artifacts still expose global rosters; the
  lane split must therefore be encoded as machine-readable lane metadata rather
  than prose alone.
- **Unfair comparison risk:** avoided only if same-target row eligibility is
  explicit before any lane is interpreted as rankable.
- **SV target-mixing risk:** actual transformed and surrogate SV must be tagged
  separately in both low-dimensional and high-dimensional surfaces.
- **SGQF overpromotion risk:** any SGQF score admission via autodiff-only
  provenance remains vetoed.

## Verification

Focused CPU-only governance checks:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py \
  tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py \
  tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py \
  tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py \
  tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py
```

Row-specific regression checks:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

Static sanity checks:

```bash
python -m compileall -q scripts tests/highdim
```
