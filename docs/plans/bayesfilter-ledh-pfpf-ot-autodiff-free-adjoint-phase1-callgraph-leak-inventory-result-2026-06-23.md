# Phase 1 Result: Callgraph Leak Inventory

date: 2026-06-23
phase: P1-CALLGRAPH-LEAK-INVENTORY
decision: PASSED

## Phase Objective And Question

Objective: build an exact production callgraph from the SIR actual-gradient
harness to LEDH-PFPF-OT transport and classify autodiff usage as production
leak, custom-gradient boundary, diagnostic/test-only, unreachable, or explicit
P2 blocker.

Question: where does autodiff enter the current LEDH production gradient path?

## Inherited Entry Conditions

- P0 contract passed.
- Inherited state remains `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED`.
- No GPU/FD run was authorized or launched in P1.
- Production-vs-diagnostic boundary is fixed by the P0 contract.
- No production LEDH-PFPF-OT gradient artifact counts without a future
  no-autodiff audit bound to the exact same route manifest.

## Evidence Produced

- Leak ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-autodiff-leak-ledger-2026-06-23.md`
- P1 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-subplan-2026-06-23.md`
- P2 subplan to refresh/review next:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-subplan-2026-06-23.md`

## Local Commands Actually Run

```text
rg -n "SIR|sir|actual-gradient|actual_gradient|LEDH|PFPF|transport_ad_mode|no-autodiff|autodiff_free|manual_vjp|custom_gradient" experiments docs scripts src tests -g '*.py' -g '*.md' -g '*.tex'

rg --files | rg '(sir|SIR|ledh|pfpf|transport|gradient|actual|dpf)'

find . -maxdepth 3 -type d | sort | sed -n '1,220p'

rg -n "def main|ArgumentParser|transport_ad_mode|actual_gradient|actual-gradient|gradient_mode|manual_streaming|BatchedLEDH|run_actual|N10000|particles" docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py

rg -n "tf\\.GradientTape|GradientTape\\(|\\.gradient\\(|\\.jacobian\\(|\\.batch_jacobian\\(|tf\\.gradients|ForwardAccumulator|tf\\.custom_gradient|@tf\\.custom_gradient|gradient_override_map|RegisterGradient|custom_gradient|watch\\(" docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py tests/highdim/test_p81_analytical_sir_score.py

rg -n "S7R|phase7r|N2500|N10000|actual-gradient|benchmark_p8p|regression_fd|manual_streaming|blockwise|transport_ad_mode|gradient_mode|command" docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7r-metadata-remediation-result-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-stop-handoff-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-result-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md

rg -n "def _filterflow_manual_streaming_finite_transport_stopped_scale_keys|def _filterflow_manual_streaming_blockwise_vjp_finite_transport_stopped_scale_keys|tf\\.custom_gradient|@tf\\.custom_gradient|tf\\.GradientTape|GradientTape\\(|tf\\.autodiff\\.ForwardAccumulator|\\.gradient\\(|\\.jacobian\\(|\\.batch_jacobian\\(|tf\\.gradients|gradient_override_map|RegisterGradient|watch\\(" experiments/dpf_implementation/tf_tfp/resampling experiments/dpf_implementation/tf_tfp/filters -g '*.py'

rg -n "tf\\.GradientTape|GradientTape\\(|\\.gradient\\(|\\.jacobian\\(|\\.batch_jacobian\\(|tf\\.gradients|tf\\.autodiff\\.ForwardAccumulator|ForwardAccumulator\\(|tf\\.custom_gradient|@tf\\.custom_gradient|gradient_override_map|RegisterGradient|custom_gradient|watch\\(" docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/highdim/test_p82_regression_fd_harness_protocol.py tests/highdim/test_p81_analytical_sir_score.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py

git rev-parse HEAD
```

The first broad `rg` included a non-existent `src` root and produced noisy,
truncated output.  It was used only as exploratory context and not as promotion
evidence.  The narrowed scans above are the evidence basis for the ledger.

No GPU, FD, implementation, or TensorFlow execution command was run.

## Skeptical Plan Audit Outcome

Passed with caveat.

- Wrong baseline check: P1 uses the reviewed S7R/P82 blocker route, not
  Zhao-Cui or FD as comparator.
- Proxy metric check: raw search hits are not treated as reachability proof;
  the ledger separates callgraph-reachable leaks from diagnostic/test-only and
  unreachable hits.
- Stop-condition check: route binding was pinned to the reviewed command and
  exact call chain; no GPU/FD work was launched.
- Environment check: P1 is source inspection only.
- Artifact-answer check: the leak ledger gives P2 exact audit payloads rather
  than claiming the route is fixed.

Caveat: the initial broad search was too noisy.  The result relies on narrowed
exact-path scans and line-anchored inspection.

## Evidence Contract Outcome

Primary criterion passed for inventory only.

The leak ledger contains:

- exact route binding and reviewed command path;
- path/line-anchored production callgraph;
- explicit scope ledger;
- forbidden API/pattern classifications;
- per-finding P2 audit payload.

## Compact Inventory Closure Summary

Exact bound route:

- command path:
  `python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`;
- reviewed route provenance:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md:68`;
- route flags:
  `--ad-evaluation-mode reverse-gradient`, `--fd-mode ad-only`,
  `--transport-plan-mode streaming`,
  `--transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys`,
  `--transport-ad-mode stabilized`, `--dtype float32`,
  `--tf32-mode enabled`, and five seeds `81120,81121,81122,81123,81124`;
- Phase 8 route manifest status:
  `ROUTE_MANIFEST_NOT_YET_CREATED_P1`.

Compact path/line callgraph:

1. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:1039`
   enters `main`.
2. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:1047`
   selects reverse-gradient diagnostics.
3. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:477`
   opens the route-reachable outer `tf.GradientTape`.
4. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:480`
   calls `p8p._objective_from_components`.
5. `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:535`
   enters `_objective_from_components`.
6. `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:507`
   calls `streaming_batched_ledh_pfpf_ot_value_core_tf`.
7. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:256`
   enters the streaming value recursion.
8. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:440`
   calls `batched_annealed_transport_core_tf`.
9. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:814`
   selects the manual streaming finite transport route.
10. `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1942`
    defines the reached custom-gradient transport primitive.

Scope summary:

- included production route: P8p regression harness, P8p parameterized SIR
  harness, P8j actual-SIR callback adapter, P8d SIR callbacks/observations,
  streaming LEDH-PFPF-OT value core, batched transport core, and annealed
  transport primitives;
- included adjacent validation: P82 harness protocol tests, analytical SIR
  score tests, and LEDH-PFPF-OT transport tests;
- excluded as unreachable for this command route: third-party/vendor MATLAB
  trees, unrelated plan artifacts, `.claude`, `.git`, cache, and worktree
  infrastructure.

Classification summary:

| Class | IDs | Count | Meaning |
|---|---:|---:|---|
| `production_leak` | P1-L001, P1-L002, P1-L003, P1-L013, P1-L014, P1-L015 | 6 | Route-reachable forbidden autodiff. |
| `custom_gradient_boundary` | P1-L012, P1-L016, P1-L020 | 3 | Must inspect `grad` body; not an automatic pass. |
| `production_leak_or_boundary_unknown` | P1-L004, P1-L005, P1-L006, P1-L007, P1-L008, P1-L021, P1-L022, P1-L023, P1-L024, P1-L026, P1-L027, P1-L028 | 12 | Must be blocked or carried into exact audit/whitelist decisions. |
| `diagnostic_or_test_only` | P1-L009, P1-L010, P1-L011, P1-L029, P1-L030 | 5 | Exact diagnostic/test whitelist candidates only. |
| `unreachable_or_irrelevant` | P1-L017, P1-L018, P1-L019, P1-L025 | 4 | Not selected by reviewed route; production manifests must not select these modes. |

P2 payload summary:

- P1-L001/P1-L003 require P2 static/runtime audit to fail the current outer
  `GradientTape` route.
- P1-L013/P1-L015 require P2 static audit to fail the current manual streaming
  finite transport route because its custom-gradient `grad` body opens
  autodiff.
- P1-L016 requires P2/P6 `grad`-body inspection before the blockwise manual VJP
  route can be a candidate.
- P1-L004/P1-L005 through P1-L008 and P1-L021 through P1-L028 require exact
  route exclusion, production blocking, or diagnostic-only whitelist decisions.
- P1-L009/P1-L011 and P1-L029/P1-L030 may be exact diagnostic/test whitelist
  entries only.

## Veto Diagnostics Status

- Broad whitelist: PASS; no whitelist was created in P1.
- Missing P0 route binding: PASS.
- Missing callgraph section: PASS.
- Missing forbidden scan pattern: PASS.
- Missing route anchor: PASS.
- Ignoring callbacks: PASS; callback files are included and anchored.
- Classifying production code as diagnostic without evidence: PASS.
- Ambiguous occurrence not carried as blocker: PASS; ambiguous production
  helpers are carried as P2 blockers.
- GPU/FD launched in P1: PASS; none launched.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `8eca1559c9508527a8d61d4ca348d8cee632db42` |
| Commands | Source-search and line-inspection commands recorded above; `git rev-parse HEAD`. |
| Environment | Local shell in `/home/chakwong/BayesFilter`. |
| CPU/GPU status | GPU not used; no CUDA/TensorFlow command ran. |
| Data version | N/A. |
| Seeds | N/A; no experiment run. |
| Wall time | N/A. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-result-2026-06-23.md` |

## Unresolved Blockers Or Leaks Carried Forward

- Current reviewed actual-gradient route opens outer autodiff in
  `benchmark_p8p_regression_fd_reparameterization.py`.
- Current `manual_streaming_finite_sinkhorn_stopped_scale_keys` transport route
  opens autodiff inside a custom-gradient `grad` body.
- Score helper functions in production modules contain autodiff and must be
  blocked from production no-autodiff routes or exact-whitelisted as
  diagnostic-only.
- `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys` has a
  custom-gradient boundary that still requires a no-autodiff `grad`-body audit.
- No audit tool exists yet.
- No implementation repair has been made.
- No route is certified no-autodiff.
- No valid N10000 actual-gradient artifact exists.
- FD remains prohibited.

## What Is Not Concluded

P1 does not conclude leak repair, no-autodiff certification, GPU feasibility,
FD agreement, posterior correctness, HMC readiness, production readiness,
default-policy promotion, Zhao-Cui source-faithfulness, or scientific
superiority.

## Exact Next Gate And Handoff Conditions

Next gate: Phase 2 audit tooling.

P2 may start only after:

- P1 leak ledger/result pass bounded review;
- P2 subplan is refreshed to consume P1-L001 through P1-L030;
- no implementation, GPU, or FD action is launched before the reviewed P2
  subplan authorizes it.
