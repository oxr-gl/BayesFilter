# P02 Reference, No-NumPy, And Implementation-Path Audit Subplan

Date: 2026-06-24

Status: `COMPLETE_P02_PASSED`

## Phase Objective

Run a local-check-only implementation-path audit for the locked low-rank
actual-SIR d18 candidate. P02 must prove, from current source and focused
tests, whether the candidate path that could later be defaulted is TensorFlow /
TensorFlow Probability oriented, GPU/XLA-compatible, free of NumPy and
`.numpy()` implementation barriers, nonmaterializing, and separate from older
fixture/reporting paths.

P02 does not run GPU benchmarks, change defaults, change public API, change
algorithmic code unless a fixable local-check bug is explicitly approved in a
repair note, or certify low-rank as default.

## Entry Conditions Inherited From Previous Phase

- P00 governance result exists and passes.
- P01 evidence/default-surface audit result exists and passes.
- Candidate lock is `r16_eps0p25_alpha1em08_it120`.
- Current comparator remains the streaming GPU/TF32 actual-SIR route.
- Existing evidence anchor remains the N3072 replicated closeout from
  2026-06-23.
- No approval is inherited for GPU benchmark runtime, default-code changes,
  public API changes, package installs, network fetches, destructive git
  operations, HMC readiness claims, or scientific claims.

## Required Artifacts

- This subplan.
- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p02-implementation-audit-result-2026-06-24.md`
- Updated execution ledger.
- Updated Claude review ledger if Claude is used.
- P03 draft subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-subplan-2026-06-24.md`
- Implementation-path inventory over:
  - `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
  - `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
  - `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
  - `tests/test_actual_sir_low_rank_route_validation.py`
  - `tests/test_actual_sir_low_rank_tuning_grid.py`
  - current default streaming surface:
    `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
    and
    `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- Explicit fixture exclusion note for
  `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_transport_tf.py`.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Source AST/text audit for the solver path:
  - no `import numpy`;
  - no `np.`;
  - no `.numpy(`;
  - low-rank route implementation uses TensorFlow tensors and TensorFlow ops;
  - no dense `N x N` transport matrix is returned in active route outputs.
- Harness compiled-path audit:
  - low-rank route is called through
    `low_rank_coupling_solver_resample_tensors_tf(...)`;
  - route timing source is restricted to `compiled_core`;
  - low-rank compiled route is wrapped in `tf.function(jit_compile=args.jit_compile)`
    and the harness/tests enforce `args.jit_compile is True` for active
    default-candidate evidence;
  - `.numpy()` materialization is confined to timing/reporting/JSON conversion
    after compiled outputs return.
- Default-surface audit:
  - current default policy remains streaming GPU/TF32;
  - no default switch is performed in P02;
  - later P05 switch target is identifiable.
- Focused tests:
  `python -m pytest tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Local syntax check:
  `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Boundary scan over P02 result and P03 draft.
- Claude read-only review if the audit finds a material ambiguity about
  implementation-path cleanliness, fixture exclusion, default-surface identity,
  or boundary safety.

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: P02 compares the candidate implementation path against the current streaming GPU/TF32 actual-SIR route and does not introduce a new comparator. |
| Proxy metric promoted | Guarded: P02 audits source/path cleanliness only; timing and warm ratios remain out of scope. |
| Missing stop conditions | Guarded: P02 stops on active-path NumPy/`.numpy()`, fixture confusion, dense materialization, failed checks, unsupported claims, or unapproved boundary crossing. |
| Unfair comparison | Guarded: P02 does not run a comparison; later P03 must preserve paired seeds, shape, dtype, TF32 mode, GPU, and timing contract. |
| Hidden assumptions | Guarded: P02 distinguishes active solver path, fixture/reporting paths, and tests; it does not assume reporting conversions are implementation backend. |
| Stale context | Guarded: P02 starts from the P01 close result and rereads current source/test surfaces. |
| Environment mismatch | Guarded: P02 does not initialize GPU runtime; GPU checks are deferred to P03/P04. |
| Artifact mismatch | Guarded: P02 names the result, ledger updates, and P03 draft subplan artifact before execution. |

Audit conclusion: P02 may proceed as local source scans, syntax checks, and
focused tests only. GPU benchmark runtime, default/API/code changes, HMC work,
and scientific/default-readiness claims remain blocked.

## Evidence Contract

- Question: is the locked low-rank candidate implementation path clean enough
  to justify moving to an approved trusted-GPU end-to-end benchmark gate?
- Baseline/comparator: current streaming GPU/TF32 implementation path and the
  actual-SIR low-rank validation harness identified in P01.
- Primary pass criterion: P02 produces a source-anchored implementation-path
  inventory showing the candidate route is TensorFlow/XLA oriented, has no
  NumPy or `.numpy()` implementation barriers in the active solver path, keeps
  reporting conversions outside the compiled implementation path, and leaves
  defaults/API untouched.
- Veto diagnostics: NumPy import or `np.` in the active solver path; `.numpy()`
  inside the active solver path; use of the eager fixture route as the default
  candidate; dense transport matrix materialization in active route outputs;
  inability to identify default switch surface; failed focused tests; or
  unsupported default/performance/scientific/HMC claim.
- Explanatory diagnostics: source anchors, scan outputs, test names, reporting
  conversions, fixture exclusions, and default-surface anchors.
- What will not be concluded: default readiness, speedup, statistical ranking,
  posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API
  readiness, N4096 feasibility, production readiness, or scientific validity.
- Artifact preserving result: P02 result and updated ledgers.

## Forbidden Claims And Actions

- Do not run GPU benchmarks.
- Do not change defaults, public exports, API, package metadata, dependencies,
  model files, or algorithmic code.
- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not treat benchmark/reporting `.numpy()` conversions as implementation
  backend when they occur after compiled tensors return.
- Do not treat tests' NumPy assertions as production implementation.
- Do not treat the older transport-object fixture as the candidate route.
- Do not claim low-rank default readiness, speedup, HMC readiness, posterior
  correctness, dense Sinkhorn equivalence, or scientific validity.
- Do not treat Claude as execution authority.

## Exact Next-Phase Handoff Conditions

- If P02 passes, draft or refresh P03 end-to-end actual-SIR benchmark subplan
  with trusted-GPU approval requirements, path-length gates, exact commands,
  stop conditions, and artifact contracts.
- If P02 finds an implementation-path blocker that is fixable without changing
  the research question, write a repair note and ask for explicit approval
  before code changes.
- If P02 finds that the candidate path uses NumPy/`.numpy()` in the active
  algorithmic implementation, write a blocker result and stop.
- If P02 cannot identify the later default switch surface, write a blocker
  result and stop for human direction.
- If local tests fail, write a blocker result and stop for focused repair.

## Stop Conditions

- Active solver path contains `import numpy`, `np.`, or `.numpy(`.
- Active candidate path cannot be distinguished from eager fixture/reporting
  paths.
- Dense `N x N` materialization is required by the active low-rank route.
- Required local checks fail.
- Boundary scan finds unsupported claims.
- Any action would require GPU benchmark runtime, default-code change, public
  API change, package/network access, destructive git operation, or
  scientific/HMC claim.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the P02 result or blocker result.
3. Draft or refresh the P03 subplan.
4. Review P03 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.

## Subplan Self-Review

- Consistency: follows P01 and remains local-check-only.
- Correctness: audits the active solver path separately from fixture/reporting
  paths.
- Feasibility: source scans, syntax checks, and focused tests are local.
- Artifact coverage: result, ledgers, implementation-path inventory, and P03
  draft are required.
- Boundary safety: blocks GPU benchmark runtime, default/API changes, and
  unsupported scientific/HMC/default-readiness claims.
