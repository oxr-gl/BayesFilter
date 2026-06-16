# Batched Filtering Visible Execution Ledger

Date: 2026-06-14

## Status

`IN_PROGRESS`

## Ledger

### 2026-06-14 - Phase 0 - PREPLAN

Evidence contract:

- Question: Can the batched filtering promotion work be organized into visible
  gated phases with read-only Claude review and no hidden default changes?
- Baseline/comparator: Existing experimental batched Kalman/SVD-UKF artifacts
  and scalar production APIs named in the master program.
- Primary criterion: Master program, visible runbook, and Phase 0 subplan exist
  with explicit gates, artifacts, forbidden claims, and stop conditions.
- Veto diagnostics: Missing subplan fields; detached execution; Claude assigned
  execution authority; default-change authorization; GPU benchmark without
  JIT/trusted context.
- Non-claims: No production readiness, no default change, no CUT4 default
  path, no HMC/NeuTra posterior validity claim.

Skeptical audit:

- Wrong baseline: Mitigated by naming scalar production value+score APIs as
  the comparator, not prior batched artifacts alone.
- Proxy metric risk: Timings are explicitly explanatory until parity and
  downstream gates pass.
- Missing stop condition: Human/default/GPU/Claude nonconvergence stops are
  included in the runbook.
- Unfair comparison: Phase 4 requires scalar-loop, batched CPU, and batched GPU
  compiled comparators.
- Hidden assumption: CUT4 default exclusion is explicit.
- Stale context: Phase 0 must inventory current files before Phase 1.
- Environment mismatch: GPU phases require trusted execution; CPU phases hide
  GPU where relevant.
- Artifact adequacy: Every phase has subplan and result paths.

Actions:

- Created master program, runbook, ledger, and Phase 0 subplan.

Artifacts:

- `docs/plans/bayesfilter-batched-filtering-production-default-master-program-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-visible-gated-execution-runbook-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-visible-execution-ledger-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-0-inventory-boundary-subplan-2026-06-14.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run local plan-shape checks and Claude read-only review before Phase 0
  execution.

### 2026-06-14 - Phase 0 - ASSESS_GATE

Evidence contract:

- Question: Are the visible gated program, runbook, and Phase 0 execution
  boundary coherent enough to start correctness stabilization?
- Baseline/comparator: User instructions, current experimental artifacts,
  existing scalar production APIs, and repo scientific coding policy.
- Primary criterion: Local checks pass, Claude review returns `VERDICT:
  AGREE`, Phase 0 result records inventory/boundaries, and Phase 1 subplan is
  drafted and consistency-reviewed.
- Veto diagnostics: Missing headings, stale artifacts, environment mismatch,
  unresolved Python time loop, failed Kalman/SVD smoke, Claude nonconvergence,
  or attempted default change.
- Non-claims: No production readiness, no GPU speedup conclusion, no broad
  nonlinear correctness claim, no HMC/NeuTra integration claim.

Skeptical audit:

- Wrong baseline: Quantitative baseline artifacts were checked directly.
- Proxy metric risk: The no-loop grep is classified as a cheap proxy and paired
  with a live SVD smoke check.
- Missing stop condition: Environment, artifact, smoke, dirty-worktree, Claude,
  GPU, and default-change stops are explicit.
- Unfair comparison: Phase 4 now requires like-for-like scalar GPU comparators
  where feasible.
- Hidden assumption: NeuTra status must be audited before Phase 5 use.
- Stale context: Phase 0 result records current artifact values and dirty
  worktree boundary.
- Environment mismatch: tfgpu Python and TensorFlow `2.20.0` imported.
- Artifact adequacy: Phase 0 result and Claude review trail written.

Actions:

- Ran Phase 0 local checks.
- Ran Claude review round 1, patched fixable issues, then ran round 2.
- Wrote Phase 0 result.

Artifacts:

- `docs/plans/bayesfilter-batched-filtering-claude-review-round-01-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-claude-review-round-02-2026-06-14.md`
- `docs/benchmarks/experimental-batched-svd-ukf-phase0-smoke-b3-t5-n2-m2-2026-06-14.json`
- `docs/plans/bayesfilter-batched-filtering-phase-0-inventory-boundary-result-2026-06-14.md`

Gate status:

- `PASSED`

Next action:

- Draft and review Phase 1 subplan before editing tests.

### 2026-06-14 - Phase 1 - PRECHECK

Evidence contract:

- Question: Can the experimental batched Kalman and SVD sigma-point value+score
  paths be covered by small deterministic pytest correctness tests before
  production integration work?
- Baseline/comparator: Existing scalar production Kalman QR score and scalar
  SVD sigma-point score APIs row by row; existing Kalman tests; Phase 0
  artifact baseline.
- Primary criterion: Required Phase 1 tests pass and new SVD tests cover
  UKF/cubature scalar parity, singleton, row permutation, graph/XLA parity,
  shape mismatch, and CPU-only visibility.
- Veto diagnostics: Test failure not explained as unrelated, scalar parity
  mismatch, nonfinite output, tiny CPU XLA failure, GPU visible in CPU tests,
  production/default edits, or CUT4 default-promotion coverage.
- Non-claims: No production API readiness, no nonlinear branch coverage beyond
  affine fixture, no GPU performance claim, no CUT4 readiness, no HMC/NeuTra
  integration claim.

Skeptical audit:

- Wrong baseline: Phase 1 uses scalar production APIs row-by-row, not previous
  batched artifacts, as the correctness authority.
- Proxy metric risk: Tests are correctness gates; timing and warnings are
  explanatory only.
- Missing stop condition: Import failure, test failure, visible GPU,
  production edit need, and Claude nonconvergence are explicit stops.
- Unfair comparison: No performance comparison is made in this phase.
- Hidden assumption: Harness private helpers are used only after import safety
  check.
- Stale context: Phase 1 inherits Phase 0's validated artifact baseline.
- Environment mismatch: CPU-only TensorFlow environment will be checked via the
  test command and CPU visibility test.
- Artifact adequacy: New test file and Phase 1 result are required.

Actions:

- Drafted Phase 1 subplan.

Artifacts:

- `docs/plans/bayesfilter-batched-filtering-phase-1-test-stabilization-subplan-2026-06-14.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run subplan-shape checks and Claude read-only review before implementation.

### 2026-06-14 - Phase 1 - ASSESS_GATE

Evidence contract:

- Question: Can the experimental batched Kalman and SVD sigma-point value+score
  paths be covered by small deterministic pytest correctness tests before
  production integration work?
- Baseline/comparator: Existing scalar production Kalman QR score and scalar
  SVD sigma-point score APIs row by row.
- Primary criterion: Required pytest command passes and new SVD tests cover
  UKF/cubature scalar parity, singleton, row permutation, graph/XLA parity,
  shape mismatch, and CPU-only visibility.
- Veto diagnostics: Test failure not explained as unrelated, nonfinite output,
  scalar parity mismatch, XLA compile failure, visible GPU in CPU-only tests,
  production/default edits, or CUT4 default-promotion coverage.
- Non-claims: No production API readiness, no nonlinear branch coverage beyond
  affine fixture, no GPU performance claim, no CUT4 readiness, no HMC/NeuTra
  integration claim.

Skeptical audit:

- Wrong baseline: Tests compare against scalar production authority row by row.
- Proxy metric risk: `rg` scan is audit-only; pytest is the correctness gate.
- Missing stop condition: Shape mismatch, visible GPU, import failure, and XLA
  failure were covered.
- Unfair comparison: No performance comparison made.
- Hidden assumption: Cubature authority import was checked.
- Stale context: Phase 1 result records repair and final command.
- Environment mismatch: Tests ran with `CUDA_VISIBLE_DEVICES=-1`.
- Artifact adequacy: New test file and Phase 1 result written.

Actions:

- Added `tests/test_experimental_batched_svd_sigma_point_tf.py`.
- Ran focused repair after one shape-mismatch test assertion failed.
- Ran final Phase 1 pytest command.

Artifacts:

- `tests/test_experimental_batched_svd_sigma_point_tf.py`
- `docs/plans/bayesfilter-batched-filtering-phase-1-test-stabilization-result-2026-06-14.md`

Gate status:

- `PASSED`

Next action:

- Draft and review Phase 2 subplan before nonlinear branch implementation.

### 2026-06-14 - Phase 2 - PRECHECK

Evidence contract:

- Question: Can the experimental batched SVD sigma-point value+score path
  preserve scalar authority parity and fail-closed branch behavior on a small
  non-affine nonlinear fixture?
- Baseline/comparator: Existing scalar production Model B SVD-UKF/cubature
  score APIs row by row; existing scalar nonlinear finite-difference tests;
  Phase 1 affine batched SVD tests.
- Primary criterion: Required pytest commands pass and new nonlinear batched
  tests cover UKF/cubature scalar parity, row permutation, graph/XLA parity, and
  fail-closed branch diagnostics.
- Veto diagnostics: Scalar nonlinear parity mismatch, nonfinite output, tiny
  CPU XLA failure, branch diagnostics not raised, visible GPU in CPU-only tests,
  production edits needed, or CUT4 default-promotion scope creep.
- Non-claims: No production API readiness, no broad nonlinear accuracy claim,
  no GPU performance claim, no CUT4 readiness, no HMC/NeuTra integration claim.

Skeptical audit:

- Wrong baseline: Scalar production Model B score APIs remain authority.
- Proxy metric risk: Source scan is audit-only, not a correctness gate.
- Missing stop condition: Import failure, wrapper infeasibility, parity failure,
  XLA failure, diagnostic failure, visible GPU, and Claude nonconvergence are
  explicit stops.
- Unfair comparison: No performance comparison is made.
- Hidden assumption: Batch-native Model B wrapper is treated as the risky
  implementation point and must stop if it needs production edits.
- Stale context: Phase 2 inherits Phase 1 passing tests.
- Environment mismatch: CPU-only checks and GPU visibility tests are required.
- Artifact adequacy: New nonlinear test file and Phase 2 result are required.

Actions:

- Drafted Phase 2 subplan.

Artifacts:

- `docs/plans/bayesfilter-batched-filtering-phase-2-nonlinear-branch-coverage-subplan-2026-06-14.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run Phase 2 subplan checks and Claude read-only review before implementation.

### 2026-06-14 - Phase 2 - ASSESS_GATE

Evidence contract:

- Question: Can the experimental batched SVD sigma-point value+score path
  preserve scalar authority parity and fail-closed branch behavior on a small
  non-affine nonlinear fixture?
- Baseline/comparator: Existing scalar production Model B SVD-UKF/cubature
  score APIs row by row; existing scalar nonlinear finite-difference tests;
  Phase 1 affine batched SVD tests.
- Primary criterion: Required pytest commands pass and new nonlinear batched
  tests cover UKF/cubature eager scalar parity, row permutation, and fail-closed
  branch diagnostics.
- Veto diagnostics: Scalar nonlinear parity mismatch, nonfinite output, branch
  diagnostics not raised, visible GPU, production edits needed, fixture
  mismatch, or CUT4 default-scope creep.
- Non-claims: No production API readiness, no broad nonlinear accuracy claim,
  no GPU performance claim, no CUT4 readiness, no HMC/NeuTra integration claim.

Skeptical audit:

- Wrong baseline: Scalar production Model B APIs used as row-by-row authority.
- Proxy metric risk: Source scan is audit-only.
- Missing stop condition: Wrapper infeasibility, parity, branch diagnostics,
  visible GPU, and dirty worktree stops covered.
- Unfair comparison: No performance comparison made.
- Hidden assumption: Fixture constants recorded and tested.
- Stale context: Phase 1 tests rerun with Phase 2 tests.
- Environment mismatch: Tests run with `CUDA_VISIBLE_DEVICES=-1`.
- Artifact adequacy: New nonlinear test file and Phase 2 result written.

Actions:

- Added `tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`.
- Ran Phase 2 required tests.
- Drafted Phase 3 subplan.

Artifacts:

- `tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`
- `docs/plans/bayesfilter-batched-filtering-phase-2-nonlinear-branch-coverage-result-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-subplan-2026-06-14.md`

Gate status:

- `PASSED`

Next action:

- Run Phase 3 subplan checks and Claude read-only review before implementation.

### 2026-06-14 - Phase 3 - ASSESS_GATE

Evidence contract:

- Question: Can a non-default, opt-in batched value+score interface candidate
  be exposed without changing public defaults or weakening scalar fallback
  semantics?
- Baseline/comparator: Existing experimental batched Kalman and SVD
  sigma-point kernels, Phase 1-2 tests, public API tests, and explicit scalar
  callback fallback behavior.
- Primary criterion: Required tests pass; wrappers match underlying kernels;
  scalar callback fallback stacks value/score rows in order; unsupported
  backend fails closed; metadata records experimental status and nonclaims;
  public exports remain unchanged.
- Veto diagnostics: Public export/default edit, wrapper mismatch, unsafe scalar
  fallback inference, wrong stacked fallback order/shape, unsupported backend
  accepted, metadata omits nonclaims, or Phase 1-2 regression.
- Non-claims: No production readiness, no default policy, no GPU performance
  claim, no HMC/NeuTra integration claim.

Skeptical audit:

- Wrong baseline: Tests compare wrappers to underlying experimental kernels and
  keep scalar fallback explicit.
- Proxy metric risk: The public export scan is an audit-only guard; pytest and
  public API tests are the gate.
- Missing stop condition: Export/default edits, wrapper mismatch, fallback
  inference, earlier-test regression, and Claude nonconvergence were covered.
- Unfair comparison: No performance comparison made in Phase 3.
- Hidden assumption: A top-level explicit experimental module path is allowed
  only as non-default and non-reexported.
- Stale context: Phase 1-2 tests were rerun with the new interface tests.
- Environment mismatch: Tests ran CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Artifact adequacy: New module, tests, and Phase 3 result were written.

Actions:

- Added `bayesfilter/experimental_batched_value_score.py`.
- Added `tests/test_experimental_batched_value_score_interface.py`.
- Repaired one public-export boundary test that used `hasattr` on an already
  imported submodule instead of the repo's `__all__` and `_EXPORT_MODULES`
  public export maps.
- Ran Phase 3 required tests and public API guard.

Artifacts:

- `bayesfilter/experimental_batched_value_score.py`
- `tests/test_experimental_batched_value_score_interface.py`
- `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-result-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-subplan-2026-06-14.md`

Gate status:

- `PASSED`

Next action:

- Run Phase 4 subplan checks and Claude read-only review before benchmark
  harness repair.

### 2026-06-14 - Phase 4 - PRECHECK

Evidence contract:

- Question: For realistic filtering dimensions, what is the compiled CPU/GPU
  behavior of experimental batched Kalman and SVD-UKF value+score relative to
  scalar-loop comparators where feasible?
- Baseline/comparator: Scalar-loop production authority paths over the same
  deterministic fixture rows; batched compiled CPU; batched compiled GPU;
  previous parity tests.
- Primary criterion: Harness repairs and tests pass; all GPU performance
  commands use JIT/XLA compiled paths in trusted context; benchmark JSON
  artifacts record compile time, warm timing, finite outputs, shapes, and
  device placement; scalar-loop comparator timing or infeasibility artifacts
  are recorded.
- Veto diagnostics: GPU benchmark run without JIT, wrong device placement,
  nonfinite outputs, required JSON missing/malformed, Phase 1-3 regression,
  public export/default edit, scalar parity failure in existing tests, or
  unsupported broad speedup/default claim.
- Non-claims: No production default readiness, no downstream HMC/NeuTra
  throughput claim, no sampler convergence/posterior quality claim, no CUT4
  readiness, no broad GPU superiority beyond this fixture and these batch
  sizes.

Skeptical audit:

- Wrong baseline: Subplan now requires scalar-loop comparator artifacts or
  explicit infeasibility artifacts.
- Proxy metric risk: Timing is descriptive; correctness and device placement
  are veto gates.
- Missing stop condition: Trusted GPU, JIT-only GPU, local tests, public API,
  nonfinite output, and Claude nonconvergence stops are explicit.
- Unfair comparison: Batched GPU cannot be presented as broad speedup against
  scalar CPU if scalar GPU is infeasible.
- Hidden assumption: The Kalman harness lacks compiled timing and must be
  repaired before GPU comparison.
- Stale context: Phase 3 result and public API status are recorded.
- Environment mismatch: CPU commands hide GPU; GPU commands require trusted
  execution.
- Artifact adequacy: Batched and scalar-loop artifacts are named for CPU/GPU
  and `B=20,256,4096`.

Actions:

- Drafted Phase 4 subplan.
- Patched subplan after local audit to add explicit scalar-loop artifacts and
  infeasibility handling.
- Ran heading, public-export, and benchmark-plan source scans.

Artifacts:

- `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-subplan-2026-06-14.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Send Phase 4 subplan to Claude read-only review.

### 2026-06-14 - Phase 4 - ASSESS_GATE

Evidence contract:

- Question: For realistic filtering dimensions, what is the compiled CPU/GPU
  behavior of experimental batched Kalman and SVD-UKF value+score relative to
  scalar-loop comparators where feasible?
- Baseline/comparator: Scalar-loop production authority paths where XLA
  feasible, batched compiled CPU, batched compiled GPU, and previous parity
  tests.
- Primary criterion: Harness repairs and tests pass; all GPU performance
  commands use JIT/XLA compiled paths in trusted context; benchmark JSON
  artifacts record compile time, warm timing, finite outputs, shapes, and
  device placement; scalar-loop comparator timing or infeasibility artifacts
  are recorded.
- Veto diagnostics: Eager GPU benchmark, wrong device placement, nonfinite
  output, missing artifact without capacity/infeasibility record, Phase 1-3
  regression, public export/default edit, or unsupported broad speedup/default
  claim.
- Non-claims: No production default readiness, no downstream HMC/NeuTra
  throughput claim, no sampler convergence/posterior quality claim, no CUT4
  readiness, no broad GPU superiority beyond this fixture and these batch
  sizes.

Skeptical audit:

- Wrong baseline: Scalar-loop comparators were recorded where feasible; scalar
  SVD comparator infeasibility was preserved rather than ignored.
- Proxy metric risk: Timings are descriptive; correctness/device placement are
  veto gates.
- Missing stop condition: Capacity timeouts, scalar comparator infeasibility,
  trusted GPU, and no-default boundaries were applied.
- Unfair comparison: Batched GPU timings are not presented as broad speedup
  against scalar CPU when scalar GPU comparator is missing.
- Hidden assumption: Kalman scalar-loop comparator is a benchmark comparator
  only, not an HMC-jittable production path.
- Stale context: Phase 4 inherited and reran Phase 1-3 tests.
- Environment mismatch: CPU runs hid GPU; GPU runs used trusted
  `CUDA_VISIBLE_DEVICES=1` and verified GPU device placement.
- Artifact adequacy: Timing, timeout, and infeasibility artifacts were written
  for all planned Phase 4 slots.

Actions:

- Patched benchmark harnesses for Kalman compiled timing and scalar-loop
  comparator modes.
- Added benchmark harness tests.
- Ran CPU compiled benchmark ladder and trusted GPU compiled benchmark ladder.
- Wrote capacity/infeasibility artifacts for bounded non-completions.
- Wrote Phase 4 result and Phase 5 subplan.

Artifacts:

- `docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py`
- `docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py`
- `tests/test_experimental_batched_benchmark_harness.py`
- `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-result-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-subplan-2026-06-14.md`
- Phase 4 benchmark JSON artifacts listed in the Phase 4 result.

Gate status:

- `PASSED_WITH_CAPACITY_AND_FEASIBILITY_LIMITS`

Next action:

- Run Phase 5 subplan checks and Claude read-only review before downstream
  harness implementation.

### 2026-06-14T15:04:00+08:00 - Phase 5 - ASSESS_GATE

Evidence contract:

- Question: Can the experimental batched value+score interface be consumed at a
  named existing downstream target/harness boundary while preserving HMC-style
  value/score shapes and explicit experimental metadata?
- Baseline/comparator: Phase 3 interface contract, existing value+score adapter
  conventions, scalar fallback callback semantics, and Phase 1-3 correctness
  artifacts. Phase 4 timing is context only.
- Primary criterion: Required tests pass against a named existing downstream
  boundary; the boundary receives `[B]` values and `[B, p]` scores; finite
  outputs and row order are preserved; no export/default edit occurs; HMC/NeuTra
  gate status is audited before any downstream claim.
- Veto diagnostics: Shape mismatch, nonfinite output, row-order failure,
  implicit scalar fallback, missing experimental metadata, public
  export/default edit, or stale/missing HMC/NeuTra gate status used as readiness
  evidence.
- Non-claims: No sampler convergence, no posterior quality, no HMC/NeuTra
  production readiness, no default policy, no broad speedup claim.

Skeptical audit:

- Wrong baseline: The gate used the named value/score boundary
  `bayesfilter.inference.hmc.static_unroll_chain_value_and_score`, not a generic
  synthetic callback as sufficient downstream evidence.
- Proxy metric risk: Phase 4 timing remained contextual and was not used as a
  downstream readiness criterion.
- Missing stop condition: Shape, finite output, row-order, explicit fallback,
  export/default, and stale HMC/NeuTra gate misuse vetoes were applied.
- Unfair comparison: No sampler or NeuTra training result was inferred from a
  value/score boundary test.
- Hidden assumption: Existing HMC/NeuTra gate status was audited before naming
  the boundary as engineering evidence.
- Stale context: Phase 5 used current-code-relevant local canary documentation
  and preserved its nonclaims.
- Environment mismatch: Tests intentionally hid GPU with
  `CUDA_VISIBLE_DEVICES=-1`; no GPU inference was made.
- Artifact adequacy: The Phase 5 result records the named boundary, tests,
  Claude review trail, and handoff to Phase 6.

Actions:

- Patched the Phase 5 subplan after Claude round 1 required a named existing
  downstream boundary.
- Added `tests/test_experimental_batched_downstream_value_score_harness.py`.
- Ran downstream/interface/benchmark, experimental correctness, public API, and
  export-scan checks.
- Wrote the Phase 5 result and drafted the Phase 6 subplan.

Artifacts:

- `tests/test_experimental_batched_downstream_value_score_harness.py`
- `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-result-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-5-claude-review-round-01-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-5-claude-review-round-02-2026-06-14.md`

Gate status:

- `PASSED_AS_NAMED_DOWNSTREAM_VALUE_SCORE_BOUNDARY`

Next action:

- Run Phase 6 pre-decision checks and Claude read-only review of the Phase 6
  default-readiness subplan.

### 2026-06-14T15:26:35+08:00 - Phase 6 - ASSESS_GATE

Evidence contract:

- Question: Is the batched filtering value+score work ready to become a
  production default, an optional experimental path, a conditional production
  candidate, or blocked?
- Baseline/comparator: Phase 0-5 result files, scalar authority parity tests,
  public API guard, JIT-only benchmark artifacts, and the named Kalman
  downstream boundary.
- Primary criterion: A decision table and inference-status table explicitly
  separate Kalman evidence, SVD-UKF evidence, downstream-boundary coverage,
  trusted/JIT performance provenance, default-policy blockers, required human
  approvals, and nonclaims.
- Veto diagnostics: Missing phase result, scalar parity failure, nonfinite
  output, wrong GPU placement, missing trusted GPU provenance, eager GPU timing
  used as speed evidence, public export/default change, unsupported HMC/NeuTra
  or posterior claim, or unsupported SVD-UKF downstream claim from Kalman-only
  evidence.
- Non-claims: No production default change, no sampler convergence, no posterior
  quality, no CUT4 readiness, no broad model coverage, no statistically
  supported speed ranking.

Skeptical audit:

- Wrong baseline: Phase 6 used the prior phase result set and scalar authority
  parity, not benchmark timings alone.
- Proxy metric risk: Phase 4 timing remained descriptive and was not used as a
  default-promotion criterion.
- Missing stop condition: Public API/import failure, trusted GPU provenance,
  SVD downstream gap, and human-default approval stops were applied.
- Unfair comparison: SVD scalar compiled-loop infeasibility and CPU capacity
  limits were preserved rather than converted into broad GPU superiority
  claims.
- Hidden assumption: Phase 5 downstream evidence was scoped to Kalman only.
- Stale context: Current live checks found a new public inference import blocker
  from dirty `generic_hmc_tuning` export drift; the result was revised to
  include it.
- Environment mismatch: Phase 6 local checks were CPU-only; Phase 4 GPU evidence
  was used only because its artifacts record trusted JIT/GPU provenance.
- Artifact adequacy: The Phase 6 result includes pre-checks, end-of-phase local
  checks, blocker assessment, decision tables, inference status, and a handoff.

Actions:

- Patched Phase 6 subplan after Claude round 1 identified Kalman-only
  downstream, snapshot-scope, trusted-GPU, and primary-criterion gaps.
- Claude round 2 agreed the Phase 6 subplan converged.
- Wrote the Phase 6 default-readiness result.
- Ran focused batched implementation/interface tests: `40 passed`.
- Attempted downstream/public API gates; both failed due the live
  `generic_hmc_tuning` public inference import blocker.
- Retried Claude result review after a broad prompt nonresponse and successful
  probe; the narrower round 2 review agreed.

Artifacts:

- `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-result-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-6-claude-review-round-01-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-6-claude-review-round-02-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-6-result-claude-review-round-01-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-6-result-claude-review-round-02-2026-06-14.md`

Gate status:

- `DEFAULT_NOT_READY_EXPERIMENTAL_OPTIONAL_PATH_SUPPORTED_WITH_LIVE_PUBLIC_API_BLOCKER`

Next action:

- Write the final visible stop handoff and stop for human direction on whether
  to repair dirty public inference/export drift and/or authorize a new
  productionization program.
