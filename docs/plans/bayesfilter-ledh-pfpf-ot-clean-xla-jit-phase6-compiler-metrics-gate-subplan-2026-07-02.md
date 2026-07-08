# Phase 6 Subplan: Compiler Metrics Gate

Date: 2026-07-02

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Prove, on a tiny trusted GPU/XLA fixture, that the actual full manual route is
compiled with bounded TensorFlow/XLA loop representation rather than Python
unrolled Sinkhorn/RK4/time-scan graphs.

This phase must also prove route selection plainly: when the score target is
the total derivative, the compiled route must use `transport_ad_mode="full"`
and route through `_filterflow_manual_streaming_finite_transport_total_vjp`,
not through stopped-key partial-derivative helpers.

## Entry Conditions Inherited From Previous Phase

- Phase 2 tensorized fixed process noise.
- Phase 3 converted RK4 forward/reverse substeps to TensorFlow loop state.
- Phase 4 converted the live manual forward/reverse time scan to TensorFlow
  loop state.
- Phase 5 converted targeted streaming Sinkhorn step loops/state lists to
  TensorFlow loop state.
- Static audit still reports `FAIL_CURRENT_ROUTE` because stopped-key helper
  rows remain true: `SINK-STOPPED-VALUE-KEY` and `SINK-STOPPED-VJP-KEY`.
  Those helpers are partial-derivative helpers and must not be called scores.

## Required Artifacts

- A compiler-metrics script or focused test, scoped to one of:
  - `scripts/audit_ledh_clean_xla.py`;
  - `tests/test_audit_ledh_clean_xla.py`;
  - a new small script under `scripts/`;
  - a new focused test module under `tests/`.
- Phase 6 compiler metrics artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-2026-07-02.json`
- Phase 6 executed route/call-path artifact, either embedded in the compiler
  metrics JSON or written separately, recording actual observed calls or
  source-anchored static call-path evidence for the compiled fixture.
- Phase 6 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-gate-result-2026-07-02.md`
- Draft Phase 7 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-subplan-2026-07-02.md`
- Updated execution ledger and Claude review ledger.

## Required Checks, Tests, Reviews

Before implementation:

- Codex skeptical audit of this subplan.
- Claude read-only review of the Phase 5 result and this Phase 6 subplan.

After implementation:

- CPU-hidden local syntax/static checks for any new script or test.
- Trusted/escalated GPU/CUDA probe before any GPU/XLA run.
- Trusted/escalated tiny GPU/XLA compile/run of the full route with:
  - `transport_gradient_mode="manual_streaming_finite_sinkhorn_stopped_scale_keys"`;
  - `transport_ad_mode="full"`;
  - streaming transport;
  - small `N`, small `T`, and one seed;
  - `jit_compile=True`;
  - TF32 enabled for the GPU route unless an explicit reference arm disables it.
- HLO/compiler metrics recorded for that exact compiled function:
  - compile success;
  - device used;
  - HLO text/module length or stable proxy;
  - `while`/`While`/`WhileRegion` marker count when available;
  - absence of obvious per-time/per-Sinkhorn-step Python-unrolled graph
    expansion in the HLO/source-derived metrics;
  - cold compile plus first-call time;
  - warm-call time;
  - concrete function count or equivalent retrace/compile multiplicity proxy;
  - output finiteness.
- Route evidence recorded from source/static inspection and runtime metadata
  showing the full route uses the total-VJP transport helper.
- The Phase 6 result must include a run manifest and decision table.
- Existing Phase 5 static audit and focused tests still pass.
- Claude read-only review of Phase 6 result before Phase 7 execution.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the actual full manual route compile and execute under trusted GPU/XLA with bounded loop representation, and is the compiled route the total-derivative route rather than the stopped-key partial-derivative route? |
| Baseline/comparator | Phase 5 loop-state code and the same tiny full-route fixture in eager/non-HLO form for value/gradient finiteness and route metadata. |
| Primary pass criterion | Trusted GPU/XLA tiny full-route compile/run succeeds; artifact records finite outputs, `jit_compile=True`, GPU device evidence, actual call-path evidence for `transport_ad_mode="full"` through the total-VJP helper, bounded `while`/`While`/`WhileRegion` style representation when HLO text is available, no obvious HLO/source-derived graph expansion from Python unrolling, and no unexpected retrace/compile multiplicity between cold and warm same-signature calls. |
| Veto diagnostics | GPU not visible under trusted probe; compiled run falls back to CPU or non-XLA; compiled route uses stopped-key helpers for the score; actual call-path evidence is missing; output is nonfinite; HLO metrics cannot be obtained or recorded; HLO/source evidence shows Python-unrolled time/RK4/Sinkhorn step bodies; repeated calls retrace unexpectedly for the same signature; Phase 5 static/parity tests regress. |
| Explanatory diagnostics | Compile time, warm-call time, HLO text size, while marker count, concrete function count, memory if easy to collect, and exact command environment. |
| Not concluded | No FD correctness, no statistical validity, no HMC readiness, no posterior correctness, no broad production readiness, and no claim that stopped-key helpers compute scores. |
| Artifact | Phase 6 compiler metrics JSON and Phase 6 result markdown. |

## Implementation Details

Use the smallest fixture that exercises one transport step and the manual score
route. Prefer a small `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
entrypoint or a focused script that imports that module and wraps
`_manual_value_and_score_from_components` in `tf.function(jit_compile=True)`.

The route must set:

- `transport_plan_mode="streaming"`;
- `transport_gradient_mode=core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE`;
- `transport_ad_mode="full"`;
- small `time_steps`, `num_particles`, and chunk sizes.

Record the exact command and environment. GPU/CUDA/XLA commands must run with
trusted/escalated permissions. CPU-only helper checks must set
`CUDA_VISIBLE_DEVICES=-1` before TensorFlow import and must be labeled CPU-only.

The metrics artifact must include:

- git commit or explicit dirty-worktree note;
- exact command;
- environment/conda executable when available;
- CPU/GPU status and GPU probe result;
- random seeds;
- wall time;
- output paths;
- plan and result paths;
- route config;
- actual call-path evidence, with either source line anchors or lightweight
  runtime counters proving the total-VJP helper path was used by the compiled
  fixture;
- HLO/compiler metrics and retrace proxy;
- nonclaims.

The result markdown must include a decision table and run manifest. A Phase 6
pass means only: the tiny trusted GPU/XLA full-route fixture compiled and ran
with bounded loop representation. It does not establish broad clean-XLA
readiness, numerical superiority, HMC suitability, or default-policy promotion.

Do not use the stopped-key stabilized route as score-route compiler evidence.
The stopped-key route may be mentioned only as a partial-derivative route or a
negative/control route.

## Forbidden Claims And Actions

- Do not claim final clean-XLA if route evidence is from
  `transport_ad_mode="stabilized"` or any stopped-key helper path.
- Do not call stopped-key partial derivatives scores.
- Do not use CPU-only compile evidence as GPU/XLA evidence.
- Do not run long validation ladders, FD sweeps, or HMC in Phase 6.
- Do not change numerical pass/fail thresholds after seeing compiler metrics.
- Do not edit finite Sinkhorn equations, derivative targets, or Phase 5 helper
  semantics in Phase 6 unless a compiler failure has a narrowly documented
  implementation bug.

## Exact Next-Phase Handoff Conditions

Phase 6 may hand off to Phase 7 only if:

- tiny full-route GPU/XLA compile/run succeeds under trusted execution;
- route metadata/source evidence confirms total-derivative route selection;
- HLO/compiler metrics artifact exists and is interpreted as compiler evidence
  only;
- Phase 5 static/parity checks still pass;
- Phase 6 result and Phase 7 subplan exist;
- Claude read-only review returns `VERDICT: AGREE`, or fixable findings are
  patched and rereviewed.

## Stop Conditions

Stop and write a blocker result if:

- trusted GPU/CUDA probe fails;
- trusted GPU/CUDA probe fails, in which case Phase 6 must stop immediately and
  classify the result as environment-blocked, not as route evidence;
- the full route does not compile with XLA;
- compiled execution is CPU-only, non-XLA, or nonfinite;
- route evidence shows stopped-key helpers are used for the score route;
- HLO/compiler metrics cannot be collected with a bounded command;
- metrics show clear Python unrolling remains;
- Phase 5 static/parity checks regress;
- Claude and Codex do not converge after five rounds.

## Skeptical Pre-Execution Audit

Result: `PASS_PENDING_CLAUDE_REVIEW`

- Wrong baseline: avoided by testing the Phase 5 code and exact full-route
  tiny fixture.
- Proxy promotion: avoided because compiler/HLO metrics are not scientific
  correctness evidence.
- Missing stop conditions: explicit above.
- Unfair comparison: route must use the same fixture and same compiled
  signature for cold and warm calls.
- Hidden assumption: stopped-key helper findings remain real; Phase 6 must
  target `transport_ad_mode="full"` for score-route evidence.
- Environment mismatch: GPU/XLA evidence requires trusted/escalated execution.
- Artifact mismatch: Phase 6 must write JSON metrics and a result markdown
  before any next phase.
