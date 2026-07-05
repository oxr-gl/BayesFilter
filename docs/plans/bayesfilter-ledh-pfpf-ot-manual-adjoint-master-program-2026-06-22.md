# LEDH-PFPF-OT Manual Adjoint / Custom Gradient Master Program

status: COMPLETE_LOCAL_ROUTE_PASSED_P82_P5_WIRED
date: 2026-06-22
supervisor_executor: Codex
readonly_reviewer: Claude Opus, bounded fact-packet review only when material

## Objective

Design, verify, and integrate a memory-disciplined manual-adjoint/custom-gradient
route for LEDH-PFPF-OT transport gradients so that SIR d=18 and related
high-dimensional filtering tests can obtain usable gradients without raw
autodiff through the full retained Sinkhorn/transport solve.

This program exists because the raw `transport_ad_mode=full` route has already
been shown infeasible for governed `N=10000` evidence on this hardware/harness.

## Standing Evidence Contract

| Field | Contract |
|---|---|
| Scientific/engineering question | Can we implement a memory-disciplined LEDH-PFPF-OT transport-gradient route whose primitive VJPs/JVPs match checked references before using it in SIR d=18 FD consistency tests? |
| Baseline/comparator | For primitive tests: TensorFlow autodiff on tiny dense problems and finite differences where appropriate.  For later SIR validation: same-scalar 13-point regression FD. |
| Primary promotion criterion | Each phase must pass its stated primitive parity, shape, finite-value, memory, and documentation checks before the route is used by downstream P82 validation. |
| Veto diagnostics | Unbounded raw full-AD at `N=10000`; missing primitive parity; nonfinite adjoints; shape/broadcast mismatches; undocumented stopped/frozen quantities; memory growth inconsistent with the route claim; unsupported HMC/default/posterior/scientific-superiority claims. |
| Explanatory diagnostics | Runtime, peak memory where available, TensorFlow device placement, residuals from linear solves, finite-difference residuals, gradient relative error, dense-vs-streaming differences, and code-doc audit notes. |
| Not concluded | HMC/NUTS readiness, posterior correctness, exact likelihood correctness, default-gradient readiness, production readiness, scientific superiority, or P82 FD agreement until the corresponding downstream gates pass. |
| Preserving artifacts | This master program, phase subplans/results, primitive test artifacts, implementation diffs, code-doc audit notes, and the final handoff back to P82. |

## Forbidden Claims And Actions

- Do not use `transport_ad_mode=full` raw TensorFlow autodiff/JVP as the
  governed `N=10000` actual-gradient route.
- Do not rerun the known-bad `N=10000`, five-seed, full-transport AD/JVP
  route except as a tiny/small primitive diagnostic explicitly bounded by a
  phase subplan.
- Do not claim streaming memory improvement until a streaming/chunked route is
  implemented and measured.
- Do not claim manual-adjoint correctness from a chapter or derivation alone.
- Do not expose a public/default route before private primitive parity tests
  and opt-in integration checks pass.
- Do not change BayesFilter default gradient policy or HMC-facing defaults in
  this program.
- Do not revert unrelated dirty worktree changes.

## Required Inputs

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-reset-memo-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-inventory-result-2026-06-22.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-transport-fd-result-2026-06-19.md`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`

## Phase Ladder

| Phase | Objective | Subplan | Required result |
|---|---|---|---|
| M0 | Re-entry governance: verify reset/inventory state, lock boundaries, and make the known-bad full-AD route non-executable for governed N10000 validation. | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase0-reentry-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase0-reentry-result-2026-06-22.md` |
| M1 | Derivation and chapter plan: define the exact scalar, stopped/frozen objects, Sinkhorn/OT adjoint equations, and notation before implementation. | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-result-2026-06-22.md` |
| M2 | Primitive dense Sinkhorn VJP tests: private helper only, tiny dense problems, compare manual VJP/JVP to TensorFlow autodiff and FD. | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-result-2026-06-22.md` |
| M3 | Stabilized dense transport custom-gradient prototype: opt-in private path, finite-value and shape checks, no streaming claim. | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase3-dense-custom-gradient-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase3-dense-custom-gradient-result-2026-06-22.md` |
| M4 | Loop-adjoint filtering integration design: decide retained quantities, replay policy, seed/fixed-randomness policy, and gradient contract for LEDH-PFPF-OT. | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase4-loop-adjoint-integration-design-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase4-loop-adjoint-integration-design-result-2026-06-22.md` |
| M5 | Opt-in integration and small SIR smoke: use the manual/custom route on small bounded cases, compare to raw AD only where raw AD is cheap. | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase5-small-sir-smoke-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase5-small-sir-smoke-result-2026-06-22.md` |
| M6 | Streaming/chunked memory route: implement or reject a streaming adjoint based on measured memory/runtime evidence. | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-result-2026-06-22.md` |
| M7 | Return-to-P82 validation handoff: prepare `N=10000` manual/custom-adjoint actual-gradient gate and `N=1000` 13-point regression-FD comparator gate. | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-result-2026-06-22.md` |
| M8 | Closeout and code-doc consistency audit: document limitations, supported modes, unsupported modes, and downstream claims still blocked. | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-result-2026-06-22.md` |

## Subplan Contract

Every phase subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each executed phase, Codex must:

1. run required local checks;
2. write a phase result or blocker result;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.

## Review Loop

Claude may be used as a read-only reviewer for material derivation,
implementation, and handoff gates.  Claude is not an execution authority and
cannot authorize crossing human, runtime, model-file, funding,
product-capability, GPU, or scientific-claim boundaries.

Use compact fact packets, not whole-file prompts, unless a narrow source/code
anchor audit requires direct inspection.  If Claude stalls, run:

```text
READ-ONLY PROBE. Reply exactly PROBE_OK.
```

If the probe works, redesign the prompt.  If review finds a fixable problem,
patch the same subplan or artifact visibly and rerun focused checks.  Stop
after five review rounds for the same blocker and write a blocker result.

## Return-To-P82 Gate

P82 FD-only validation may resume only after this program produces a reviewed
handoff stating:

- which manual/custom-adjoint route is supported;
- which transport modes are supported and unsupported;
- what data/randomness is fixed, replayed, or differentiated;
- primitive parity results and tolerances;
- memory/runtime evidence for the intended `N=10000` actual-gradient gate;
- exact commands for the downstream `N=10000` five-seed gradient and `N=1000`
  five-seed 13-point regression-FD comparison.

Until then, P82 status remains:

```text
BLOCKED_WAITING_FOR_MEMORY_DISCIPLINED_LEDHPFPFOT_GRADIENT_ROUTE
```
