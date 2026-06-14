# P35 Phase 3 Zhao--Cui Highdim Fixed-Branch Fitting Result

metadata_date: 2026-06-04

phase: Phase 3 fixed-branch fitting

git_commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`

## Pre-Implementation Skeptical Audit

status: `PASS_TO_IMPLEMENT`

The Phase 3 plan has a valid fixed-branch target: declared ranks, declared
sample batch, declared ridge, declared sweep order, and no adaptive branch
choice during fitting.  The main hazards are overclaiming and hidden branch
mutation.  This implementation will therefore restrict itself to deterministic
fixed-rank weighted ridge ALS; it will not claim adaptive TT-cross, rank
adaptation, filtering, or derivative correctness.  Complexity gates must run
before dense design or normal matrices are allocated, and each accepted core
update must rebuild environments from the current cores.

Wrong-baseline risk: low-dimensional analytic TT targets are correctness
fixtures, not evidence for large-scale filtering performance.

Proxy-metric risk: training residual is not a promotion metric when a holdout
batch is supplied; holdout residual above tolerance is a veto.

Environment risk: authoritative tests are CPU-only TensorFlow tests with
`CUDA_VISIBLE_DEVICES=-1`; no GPU performance conclusion is made.

## Evidence Contract

scientific_or_engineering_question: Can BayesFilter fit supplied fixed-rank TT
cores to supplied target values by deterministic weighted ridge ALS while
recording a replayable full branch manifest and deterministic failure exits?

exact_baseline_or_comparator:
- analytic rank-one separable TT target;
- analytic rank-two bivariate TT target;
- direct dense normal-equation solve for one core;
- deterministic replay of the same branch-defining payload.

primary_pass_criterion:
- Phase 0--3 CPU-only tests pass;
- exact fixed-rank fixtures fit within stated tolerance;
- replay produces identical branch hash and fitted values;
- over-budget, ill-conditioned, and holdout-failing cases return deterministic
  veto statuses.

veto_diagnostics:
- `COMPLEXITY_GATE`;
- `CONDITION_NUMBER_VETO`;
- `HOLDOUT_RESIDUAL_VETO`;
- `NONFINITE_VALUE`;
- `MEASURE_MISMATCH`;
- public API regression;
- forbidden backend/source scan failure;
- `git diff --check` failure;
- Claude Code blocker not accepted or resolved after at most five rounds.

explanatory_only_diagnostics:
- training residual when holdout is present;
- condition-number warning below veto;
- TensorFlow Probability deprecation warnings from unrelated imports.

what_will_not_be_concluded:
- adaptive Zhao--Cui TT-cross correctness;
- rank-selection validity;
- sequential filtering correctness;
- fixed-branch derivative correctness;
- large-scale memory/performance readiness;
- DSGE readiness.

artifact:
- this result ledger;
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-claude-review-ledger-2026-06-04.md`.

## Implementation Notes

files_changed:
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/diagnostics.py`
- `bayesfilter/highdim/fitting.py`
- `tests/highdim/test_fixed_branch_fit.py`
- `tests/highdim/test_failure_exits.py`
- `tests/highdim/test_phase0_contracts.py`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-result-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-claude-review-ledger-2026-06-04.md`

implemented_api:
- `FixedTTFitConfig`
- `FixedTTFitSampleBatch`
- `FixedTTFitResult`
- `FixedTTFitter.fit(...)`
- `FixedTTFitter.build_core_update_system(...)` for deterministic reference
  tests.

solver_equation_status: `PASS`

The implemented design matrix uses
`A[i, ((a * p_j) + l) * r_{j+1} + b] =
L[i,a] * psi_j,l(z_i,j) * R[i,b]`.  The normal equation is
`(A^T W A + ridge I)c = A^T W y`, solved with `tf.linalg.solve`.

environment_rebuild_status: `PASS`

The fitter rebuilds core matrices and left/right environments from the current
core list at every core update.  Tests assert that the pre-update core hash
changes after an accepted update and that the rebuild count matches the number
of updates.

branch_manifest_status: `PASS`

The realized manifest records product basis, measure convention, full sample
payload, sample/target/weight/holdout hashes, ranks, ridge, dtype, sweep order,
coordinate order, max sweeps, initial core hash, update statuses, condition
estimates, stabilization choice, complexity budgets, solver backend,
deterministic seed, residuals, termination reason, and explicit fixed-branch
scope.

failure_exit_status: `PASS`

Tests cover `COMPLEXITY_GATE`, `CONDITION_NUMBER_VETO`,
`HOLDOUT_RESIDUAL_VETO`, `NONFINITE_VALUE`, and `MEASURE_MISMATCH` paths.

commands_run:
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py`
- `git diff --check -- bayesfilter/highdim/__init__.py bayesfilter/highdim/diagnostics.py bayesfilter/highdim/fitting.py bayesfilter/highdim/fixed_branch.py bayesfilter/highdim/validation.py bayesfilter/highdim/bases.py bayesfilter/highdim/tt.py bayesfilter/highdim/squared_tt.py bayesfilter/highdim/transport.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-result-2026-06-04.md docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-claude-review-ledger-2026-06-04.md`
- `rg -n "import numpy|from numpy|import jax|from jax|import torch|from torch|matlab|octave|tensor-ssm-paper-demo|zhao_cui_tensor_ssm_p10" bayesfilter/highdim tests/highdim`
- Claude review iterations recorded in the Phase 3 Claude review ledger.

test_outcome:
- Final focused Phase 3 gate:
  `20 passed, 2 warnings in 3.45s`.
- Final authoritative Phase 0--3 gate:
  `69 passed, 2 warnings in 5.87s`.
- Warnings were TensorFlow Probability deprecation warnings about
  `distutils.version`.

backend_status: `PASS`

Production highdim Phase 3 code uses TensorFlow tensors and `tf.float64`.
Backend/source scan was clean except for intentional no-NumPy assertion strings
in `tests/highdim/test_phase0_contracts.py`.

claude_review_status: `PASS`

Claude iteration 1 and 1b stalled and were recorded as tool stalls.  Claude
iteration 1c returned two accepted findings about direct test-file coverage for
complexity and condition-number vetoes.  Both were patched.  Claude iteration 2
returned `PASS`.

termination_reason: `phase3_tests_and_claude_review_passed`

stop_condition_triggered: `none`

decision: `PASS`
