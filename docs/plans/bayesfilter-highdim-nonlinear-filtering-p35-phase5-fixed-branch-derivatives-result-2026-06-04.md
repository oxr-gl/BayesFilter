# P35 Phase 5 Fixed-Branch Derivatives Result

metadata_date: 2026-06-04

phase: Phase 5 fixed-branch derivatives

git_commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`

## Pre-Implementation Skeptical Audit

status: `PASS_TO_PLAN_PHASE5_IMPLEMENTATION_ONLY`

The Phase 5 plan is valid only if the derivative path differentiates the same
fixed-branch scalar represented by the Phase 4 branch artifacts.  A direct
Kalman-score shortcut is useful as an exact baseline, but it cannot by itself
close Phase 5.  The implementation must expose explicit fixed-design least
squares derivative equations, TT evaluation/normalizer derivative equations, a
replay tape carrying branch hashes, and finite-difference rows that invalidate
branch mismatches.

Wrong-baseline risk: exact Kalman scores are a baseline, not sufficient proof
that the fitted fixed-branch TT derivative is correct.

Proxy-metric risk: finite-difference rows are valid evidence only when the
branch compatibility hash is unchanged.  Rows with changed branch hashes must
be invalidated, not averaged into error summaries.

Hidden-assumption risk: Phase 5 must keep bases, sample points, weights,
coordinate maps, ranks, sweep order, ridge, and branch-defining objects fixed.
Moving-basis and adaptive-branch derivatives remain unsupported.

Environment risk: authoritative Phase 5 tests are CPU-only TensorFlow tests
with `CUDA_VISIBLE_DEVICES=-1`; no GPU or DSGE readiness conclusion is made.

## Evidence Contract

scientific_or_engineering_question: Can BayesFilter compute and validate
fixed-branch derivatives for the deterministic scalar produced by the Phase 4
value path without differentiating adaptive branch selection?

exact_baseline_or_comparator:
- one-step scalar LGSSM prior-mean score;
- two-step scalar LGSSM transition-coefficient score;
- scalar nonlinear dense-quadrature score;
- centered finite differences with branch compatibility checks;
- direct fixed-design LS and TT derivative equations.

primary_pass_criterion:
- focused Phase 5 tests pass;
- full Phase 0--5 CPU validation passes;
- finite-difference table contains valid rows with expected tolerances;
- invalid branch rows are marked invalid and excluded;
- replay tape reproduces branch identity and records fixed-branch scope;
- Claude Code returns `PASS_TO_PHASE6`.

veto_diagnostics:
- exact score mismatch;
- `FINITE_DIFFERENCE_BRANCH_MISMATCH` treated as success rather than invalid
  evidence;
- moving-basis derivative silently enabled;
- stale replay environment not detected;
- nonfinite derivative values;
- hidden NumPy/JAX/PyTorch algorithmic differentiation path;
- Claude Code blocker not resolved after at most five rounds.

explanatory_only_diagnostics:
- condition-number warnings;
- finite-difference convergence trend outside valid rows;
- Kalman score baselines outside the TT derivative lane;
- dense nonlinear quadrature oracle stability.

what_will_not_be_concluded:
- adaptive Zhao--Cui branch differentiability;
- moving-basis or learned-basis derivative correctness;
- exact nonlinear likelihood gradients in general;
- HMC or DSGE readiness;
- large-scale performance.

artifact:
- this result ledger;
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-claude-review-ledger-2026-06-04.md`.

## Implementation Notes

Implemented a Phase 5 fixed-branch derivative component layer:

- `bayesfilter/highdim/derivatives.py`
  - `FixedBranchDerivativeConfig`;
  - `CoreDerivativeState`;
  - `SweepDerivativeDiagnostics`;
  - `FixedBranchReplayTape`;
  - `FiniteDifferenceRow`;
  - `FiniteDifferenceTable`;
  - `FixedDesignLSDerivativeResult`;
  - `FixedBranchScoreResult`;
  - fixed-branch compatibility hashing;
  - finite-difference row construction and branch-mismatch invalidation;
  - fixed-design weighted ridge least-squares derivative;
  - TT design-matrix derivative through sweep environments;
  - TT evaluation derivative;
  - squared-TT normalizer and log-normalizer derivatives;
  - retained-filter quotient derivative;
  - exact scalar LGSSM and dense nonlinear score fixtures.
- `bayesfilter/highdim/__init__.py`
  - subpackage-only Phase 5 exports.
- `tests/highdim/test_fixed_branch_derivatives.py`
  - required Phase 5 derivative, replay, exact-score, and failure-exit tests.
- `tests/highdim/test_phase0_contracts.py`
  - backend scan extended to `derivatives.py`.

The implementation is component-complete for the fixed-branch mathematical
obligations tested here.  It does not yet implement a full end-to-end
score method on `FixedBranchSquaredTTFilter` that propagates retained-filter
derivatives across all filtering times.  The current Phase 5 evidence is
therefore an explicit component derivative gate plus exact score fixture gate,
not a full production HMC score API.

## Commands Run

Focused Phase 5 validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_filtering_kalman_exact.py
```

First outcome: `1 failed, 28 passed, 2 warnings in 3.38s`.

Issue: retained-filter quotient finite-difference tolerance was too tight for a
centered difference at `h=1e-6`; maximum discrepancy was about `1.1e-10`.
Patch: adjusted that one component tolerance to `2e-10`.

Post-patch outcome: `29 passed, 2 warnings in 3.34s`.

Full Phase 0--5 CPU validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py tests/highdim/test_filtering_kalman_exact.py tests/highdim/test_fixed_branch_derivatives.py
```

Outcome: `98 passed, 2 warnings in 5.88s`.

Whitespace check:

```bash
git diff --check -- bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-result-2026-06-04.md
```

Outcome: passed.

Backend/source scan:

```bash
rg -n "^\s*(import|from)\s+(numpy|jax|torch)\b|matlab|octave|tensor-ssm-paper-demo|zhao_cui_tensor_ssm_p10" bayesfilter/highdim tests/highdim
```

Outcome: no matches.

## Fixtures And Obligations Checked

target_derivative_unit:
- test: `test_target_derivative_matches_finite_difference`;
- status: pass.

environment_derivative:
- test: `test_environment_derivatives_match_finite_difference`;
- status: pass.

design_matrix_derivative:
- test: `test_design_matrix_dotA_matches_finite_difference`;
- status: pass.

normal_equation_derivative:
- test: `test_normal_equation_dotN_dotd_dotc_matches_finite_difference`;
- status: pass.

tt_evaluation_derivative:
- test: `test_tt_evaluation_derivative_matches_finite_difference`;
- status: pass.

squared_tt_log_normalizer_derivative:
- test: `test_log_normalizer_derivative_matches_finite_difference`;
- status: pass.

retained_filter_quotient_derivative:
- test: `test_retained_filter_quotient_derivative_matches_finite_difference`;
- tolerance used: `2e-10`;
- status: pass.

replay_tape:
- tests:
  - `test_replay_tape_reconstructs_pre_and_post_update_core_states`;
  - `test_reverse_sweep_uses_post_update_right_environment`;
  - `test_replay_environment_cache_invalidation_is_enforced`;
- status: pass.

exact_score_fixtures:
- one-step scalar LGSSM prior mean score:
  - expected log evidence: `-0.980376005178410`;
  - expected score: `0.183486238532110`;
  - tolerance: `2e-10`;
  - status: pass.
- two-step scalar LGSSM transition coefficient score:
  - expected score: `-0.241250978551728`;
  - tolerance: `2e-10`;
  - status: pass.
- scalar nonlinear dense quadrature score:
  - expected log evidence: `-0.373000101795619`;
  - expected score: `-0.608378439103854`;
  - tolerance: `5e-10`;
  - status: pass.

failure_exit_status:
- branch mismatch invalidates finite-difference row;
- adaptive branch change invalidates finite-difference row;
- moving-basis derivative returns
  `UNSUPPORTED_MOVING_BASIS_DERIVATIVE`;
- derivative solve failure returns `DERIVATIVE_SOLVE_FAILURE`;
- replay branch mismatch raises `REPLAY_TAPE_MISMATCH`.

## Required Addendum Fields

files_changed:
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/derivatives.py`
- `tests/highdim/test_fixed_branch_derivatives.py`
- `tests/highdim/test_phase0_contracts.py`
- this result ledger

clean_room_inputs:
- P35 Phase 5 subplan;
- P36 Phase 5 addendum;
- local Phase 0--4 highdim contracts.

third_party_code_consulted: none during implementation.

clean_room_attestation: no MATLAB/Octave/P10 source was ported, translated, or
used as an implementation template for Phase 5.

backend_status: TensorFlow/TensorFlow Probability only in
`bayesfilter/highdim` Phase 5 production code; no NumPy/JAX/PyTorch imports.

measure_convention_status: Phase 5 derivative functions operate on
`ProductBasis`, `FunctionalTT`, `SquaredTTDensity`, and fixed-branch objects
that already carry `MeasureConvention`; moving-basis derivatives remain
unsupported.

branch_manifest_status: replay tape is bound to a pre-existing branch identity;
finite-difference rows require branch compatibility hashes; mismatch rows are
invalid evidence.

manifest_version:
- `fixed_branch_fd_compatibility.v1`
- `fixed_branch_replay_tape.v1`
- `fixed_branch_score_fixture.v1`

branch_hash: generated deterministically by `BranchManifest`; replay test
checks branch/tape separation and branch mismatch rejection.

replay_tape_hash_when_applicable: generated by `FixedBranchReplayTape.sha256()`;
exact score container stores the replay tape hash.

exact_reference_status: pass for pinned scalar LGSSM and dense nonlinear score
fixtures.

exact_reference_metrics: see `Fixtures And Obligations Checked`.

primary_pass_criterion_status: pass for Phase 5 component gate.  Internal tests
pass for component fixed-branch derivative equations, branch mismatch
invalidation, replay tape containers, and exact score fixtures.  Claude iter3
returned `PASS_TO_PHASE6` with a score-API constraint.

veto_diagnostics_status:
- exact score mismatch: not triggered;
- finite-difference branch mismatch treated as success: not triggered;
- moving-basis derivative silently enabled: not triggered;
- stale replay environment undetected: not triggered in replay mismatch test;
- nonfinite derivative values: not triggered;
- forbidden backend/source scan: no matches.

termination_reason: Phase 5 component implementation and internal validation
completed; Claude iter3 passed the Phase 5 gate with a constraint that Phase 6
must not claim end-to-end score API validation.

stop_condition_triggered: none internally.

decision: `PASS_TO_PHASE6_WITH_SCORE_API_CONSTRAINT`
