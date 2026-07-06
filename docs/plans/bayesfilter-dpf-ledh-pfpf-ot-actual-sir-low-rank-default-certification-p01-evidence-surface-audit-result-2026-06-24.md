# P01 Evidence Inventory And Default-Surface Audit Result

Date: 2026-06-24

Status: `PASS_P01_READY_FOR_P02_IMPLEMENTATION_AUDIT`

## Phase Summary

P01 completed the local-check-only evidence inventory and default-surface audit
for the actual-SIR d18 low-rank LEDH default-certification lane.

The current low-rank default-certification candidate remains
`r16_eps0p25_alpha1em08_it120`: rank 16, assignment epsilon `0.25`, alpha
`1e-8`, max projection iterations `120`, convergence threshold `1e-6`,
denominator floor `1e-30`, TensorFlow/TFP, float32, GPU, TF32 enabled,
compiled-core timing.

P01 did not run a GPU benchmark, change defaults, change public API, change
algorithmic code, or make an HMC/scientific/default-readiness claim.

## Skeptical Plan Audit

| Audit item | P01 status |
| --- | --- |
| Wrong baseline | Guarded: the comparator remains paired streaming TF32 actual-SIR route evidence, not synthetic-only or unpaired timing. |
| Proxy metric promoted | Guarded: warm ratios remain descriptive and cannot certify default readiness. |
| Missing stop conditions | Guarded by P01 stop conditions; no stop condition fired. |
| Unfair comparison | Guarded: existing evidence rows preserve same seeds, shape, route request, dtype, TF32, GPU, and compiled-core timing contract. |
| Hidden assumptions | Guarded: P01 inventories gaps and does not cross default/API/GPU/HMC/science boundaries. |
| Stale context | Guarded by validating existing N3072 artifacts and reading current code/test surfaces. |
| Environment mismatch | Guarded: P01 did not initialize GPU runtime; GPU provenance is read from existing trusted artifacts. |
| Artifact mismatch | Guarded: required result, next subplan, and ledgers are named explicitly. |

Audit conclusion: P01 was safe to execute as local checks and source/artifact
inspection only.

## Evidence Inventory

Primary evidence anchor:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-replicated-evidence-resource-boundary-result-2026-06-23.md`

That anchor validated four N3072 actual-SIR d18 rows across two seed batches:

| Candidate | Epsilon | Seeds | Status | Warm ratio | Mean abs loglik delta | Max abs loglik delta |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | 0.25 | `81137,81138` | `PASS` | 10.344294680968009 | 0.097137451171875 | 0.1087646484375 |
| `r16_eps0p125_alpha1em08_it120` | 0.125 | `81137,81138` | `PASS` | 10.140608807393965 | 1.33868408203125 | 1.6871337890625 |
| `r16_eps0p25_alpha1em08_it120` | 0.25 | `81139,81140` | `PASS` | 9.829297316594772 | 0.050994873046875 | 0.08428955078125 |
| `r16_eps0p125_alpha1em08_it120` | 0.125 | `81139,81140` | `PASS` | 10.091529125979234 | 1.7257080078125 | 2.97552490234375 |

All four rows had no hard vetoes, passed paired comparability, passed
actual-SIR semantics, had complete low-rank provenance, had complete GPU/TF32
provenance, and preserved row JSON/Markdown/log artifacts. Both rank-16
candidates remain viable under that bounded screen. The epsilon `0.25`
candidate is the locked engineering candidate for the default-certification
program because it passed the completed screens and was descriptively closer to
the streaming comparator. That is not a statistically supported ranking.

## Default And Code Surface Inventory

Current production/default DPF transport policy surface:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  lines 33-45 define default dtype `tf.float32`, default TF32 mode `enabled`,
  precision policy `production_ledh_pfpf_ot_gpu_tf32`, execution target `gpu`,
  and algorithm target `ledh_pfpf_ot_tf32`.
- The same module's `precision_policy_metadata()` reports public API exposure
  as `separately_gated` and describes the current default route guidance as
  streaming fixed-branch GPU/TF32.
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  exposes the streaming value recursion with `transport_plan_mode="streaming"`
  as the default parameter.
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py` asserts the precision
  metadata and streaming-vs-dense behavior.

Low-rank candidate implementation surface:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
  is the candidate route used by the actual-SIR validation harness.
- The solver imports TensorFlow only for numeric implementation and returns
  low-rank factors with `transport_matrix` shape suffix `[0, 0]` rather than
  materializing an `N x N` transport matrix.
- The solver diagnostics still classify the route as a semantic replacement /
  extension-or-invention and explicitly retain nonclaims around dense Sinkhorn
  equivalence, speedup, ranking, production default, posterior correctness,
  HMC readiness, and public API readiness.
- `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py` calls
  `low_rank_coupling_solver_resample_tensors_tf(...)` inside the compiled
  low-rank route and wraps both streaming and low-rank route timing in
  `tf.function(jit_compile=args.jit_compile)`.
- The harness rejects non-compiled timing for the low-rank route and records
  route hard vetoes for route invocation mismatch, dense materialization,
  nonfinite tensors, factor invalidity, final logsumexp residual, ESS floor,
  and expected device mismatch.
- `tests/test_actual_sir_low_rank_route_validation.py` verifies actual-SIR d18
  semantics, compiled-core timing, route invocation, nonmaterialized low-rank
  transport factors, finite/nonnegative/positive factor diagnostics, and run
  manifest fields.
- `tests/test_actual_sir_low_rank_tuning_grid.py` verifies candidate/request
  matching, paired-comparability classification, GPU/TF32 provenance, and the
  no-NumPy/no-`.numpy()` barrier over the solver and compiled harness region.

Important exclusion:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_transport_tf.py`
  is an older transport-object fixture route. It contains eager `.numpy()`
  diagnostics and is not the locked default-certification candidate surface.
  P02 must keep this distinction explicit so fixture/reporting code is not
  mistaken for the compiled candidate implementation path.

## NumPy / XLA Surface Status

Targeted scan status:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
  has no `import numpy`, no `np.`, and no `.numpy(` occurrences.
- The compiled harness region from `_streaming_value_core` through
  `_run_streaming_compiled_core_timed` is protected by an existing test against
  `.numpy(`.
- Benchmark/reporting code uses `.numpy()` to materialize tensors into JSON and
  Markdown after compiled calls return. That is reporting/serialization, not
  BayesFilter-owned algorithmic implementation.
- Tests use NumPy assertions and `.numpy()` conversions as comparison fixtures.
  That is allowed under the repository policy.

P01 does not fully certify the no-NumPy default path. It establishes that a
focused P02 implementation-path audit is both necessary and feasible.

## Remaining Gaps

The remaining gaps before low-rank can be certified as the bounded engineering
default for actual-SIR d18 LEDH are:

1. P02 implementation-path audit: prove the active candidate/default-switch path
   is TensorFlow/TFP, GPU/XLA-compatible, no NumPy implementation backend, and
   not accidentally using the eager fixture route.
2. P03 end-to-end benchmark gate: produce approved trusted-GPU actual-SIR d18
   evidence with end-to-end wall time, compiled-core timing, paired
   comparability, and hard-veto screens for the locked candidate versus the
   streaming comparator.
3. P04 resource-boundary gate: either N4096 feasibility evidence or a reviewed
   resource-boundary blocker with no automatic runtime escalation.
4. P05 default-route implementation gate: only after human approval, implement
   any default-route/config/API-surface change and focused tests.
5. P06 optional HMC/autodiff mechanics: only if the default claim includes HMC
   or differentiable-use readiness.
6. P07 final decision: decide bounded engineering default, optional route only,
   or blocked/repair-required without upgrading descriptive evidence into
   statistical or scientific claims.

## Required Checks

Completed checks:

- Existing N3072 evidence anchor read and inventoried.
- Local artifact row-lock validator over three N3072 aggregate JSONs:
  - Result: pass, `errors=[]`, four expected candidate/seed rows present.
  - Note: a first quick print formatter did not resolve nested row artifact
    fields cleanly; the artifact existence and metrics above are anchored to
    the validated N3072 closeout and direct aggregate schema inspection.
- Focused default/code-surface audit:
  - `rg` over default policy, streaming route, low-rank route, timing source,
    and transport plan mode.
  - `rg` over NumPy/`.numpy()` surfaces in solver, fixture, benchmarks, and
    focused tests.
- Source anchors read:
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  - `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
  - `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_transport_tf.py`
  - `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
  - `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
  - `tests/test_actual_sir_low_rank_route_validation.py`
  - `tests/test_actual_sir_low_rank_tuning_grid.py`
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `18 passed`.

Claude was not rerun for P01 because P00/P01 subplans already converged under
Claude Opus/max review and P01 found no new material ambiguity that required a
review loop before drafting P02. P02 will be reviewed under its own gate if the
local subplan review finds material boundary or feasibility ambiguity.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P01 passes and may hand off to P02 implementation/no-NumPy audit |
| Primary criterion status | Passed: P01 inventories existing evidence, default surface, low-rank implementation surface, NumPy/XLA gap, and next required gates |
| Veto diagnostic status | No missing evidence anchor, candidate-lock failure, failed focused tests, unidentified default surface, unsupported claim, or unapproved GPU/default/API/HMC/science boundary was found |
| Main uncertainty | P01 is an inventory phase; it does not certify no-NumPy default path, end-to-end performance, N4096 feasibility, default implementation readiness, HMC, or scientific validity |
| Next justified action | Execute P02 local implementation-path/no-NumPy audit subplan |
| What is not being concluded | No low-rank default readiness, speedup, statistical ranking, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API readiness, N4096 feasibility, formal memory scaling, production readiness, or scientific validity |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Existing N3072 hard-veto screen remains passed for four fixed rows; P01 local checks passed |
| Statistically supported ranking | None |
| Descriptive-only differences | Warm ratios and paired deltas descriptively favor epsilon `0.25`, but do not rank candidates statistically |
| Default-readiness | Not certified; P01 identifies the remaining gates |
| Next evidence needed | P02 implementation-path audit, then reviewed/approved P03/P04 trusted-GPU gates |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Commands | Focused artifact validator; targeted `rg` scans; source reads; `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`; `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q` |
| Environment | Local repository environment |
| CPU/GPU status | P01 did not initialize or use GPU benchmark runtime |
| Data version | Existing actual-SIR d18 synthetic harness artifacts from 2026-06-23 |
| Random seeds | Existing evidence seeds `81137,81138` and `81139,81140` |
| Wall time | Local-check-only audit; N/A for new runtime |
| Output artifact paths | This P01 result, updated execution ledger, P02 subplan |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p01-evidence-surface-audit-subplan-2026-06-24.md` |
| Result file | This file |

## Post-Run Red-Team Note

The strongest alternative explanation is that P01 validates the bookkeeping and
code surfaces, not the default itself. The actual low-rank candidate still
carries semantic-replacement and extension-or-invention nonclaims. Existing
timing evidence is promising but descriptive, not sufficient to prove default
readiness or statistical superiority. The weakest part of the current evidence
is that no new approved end-to-end trusted-GPU default-certification benchmark
or N4096 resource-boundary gate has been run under this master program.

## Handoff

Proceed to P02:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p02-implementation-audit-subplan-2026-06-24.md`
