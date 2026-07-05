# Manual Adjoint Phase 1 Subplan: Derivation And Chapter Contract

status: DRAFT_EXECUTABLE
date: 2026-06-22
phase: M1-DERIVATION

## Phase Objective

Write the derivation contract for a memory-disciplined LEDH-PFPF-OT
manual-adjoint/custom-gradient route before implementation.  The phase must
identify the exact finite computational scalar, the Sinkhorn/transport
primitive adjoints, the stopped/frozen quantities, and the primitive parity
tests required for M2.

This phase is documentation and derivation only.

## Entry Conditions

- M0 re-entry result is complete:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase0-reentry-result-2026-06-22.md`.
- P82 is blocked until a memory-disciplined LEDH actual-gradient route exists.
- Raw `transport_ad_mode=full` full-graph AD/JVP is forbidden as the governed
  N=10000 route.
- Existing entropic OT chapter exists:
  `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`.
- Current transport implementation paths are identified:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  and
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`.

## Required Artifacts

- Derivation note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-derivation-contract-2026-06-22.md`
- Phase 1 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-result-2026-06-22.md`
- Draft M2 primitive parity subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-subplan-2026-06-22.md`

Optional, only if the derivation is mature enough:

- chapter draft or chapter-insertion plan for
  `docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex`.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What exact finite LEDH-PFPF-OT transport scalar and primitive adjoints should the manual/custom-gradient route implement and test? |
| Baseline/comparator | Existing finite Sinkhorn/barycentric implementation and tiny dense TensorFlow autodiff references for later M2 tests. |
| Primary criterion | Derivation contract states the scalar, variables, adjoints, stopped/frozen quantities, supported modes, unsupported modes, and M2 parity tests without claiming implementation. |
| Veto diagnostics | Ambiguous scalar; conflating exact regularized OT with finite Sinkhorn; missing barycentric adjoint; missing potential/softmin adjoint; no stopped/frozen policy; claiming streaming memory or SIR d18 readiness; authorizing N10000 raw full AD. |
| Explanatory diagnostics | Code path anchors, equation labels, shape table, and list of reference tests needed. |
| Not concluded | No manual-adjoint correctness, code implementation, streaming memory improvement, P82 validation, HMC/default/posterior readiness. |
| Preserving artifact | Derivation contract and M1 result markdown. |

## Required Work

1. Read the relevant finite Sinkhorn and streaming LEDH transport code paths.
2. Read the existing entropic OT/Sinkhorn chapter section on differentiation
   contracts.
3. Draft a derivation contract that distinguishes:
   - exact regularized OT optimizer;
   - finite unrolled Sinkhorn computation;
   - scalar built from the finite computation.
4. Specify the first supported route narrowly:
   - dense, tiny/small primitive route;
   - fixed finite iteration count;
   - stabilized/stopped scale and key policy unless explicitly derived;
   - no streaming memory claim.
5. Define primitive M2 tests:
   - barycentric projection VJP;
   - dense log-domain softmin VJP;
   - finite Sinkhorn loop VJP/JVP on tiny dense cases;
   - scalar directional FD spot checks.

## Required Checks

Run after drafting the derivation contract and M2 subplan:

```bash
test -f docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-derivation-contract-2026-06-22.md
test -f docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-subplan-2026-06-22.md
rg -n "exact regularized OT|finite Sinkhorn|barycentric|softmin|stopped|unsupported|N=10000" docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-derivation-contract-2026-06-22.md
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*
```

No GPU command is authorized in M1.

## Review

Claude review is optional for M1 unless the derivation introduces a material
mathematical claim beyond the finite-computation contract.  If used, send only a
compact fact packet and ask whether the derivation contract is sufficient for
M2 primitive tests.  Claude cannot authorize implementation or downstream P82
validation.

## Forbidden Claims / Actions

- Do not implement manual VJP/custom-gradient code in M1.
- Do not launch TensorFlow GPU work.
- Do not claim the derivation proves the implementation.
- Do not claim streaming memory improvement.
- Do not claim SIR d18, HMC, posterior, or default readiness.
- Do not use raw `transport_ad_mode=full` N10000 AD/JVP as the target route.
- Do not modify unrelated dirty files.

## Next-Phase Handoff Conditions

M2 may proceed only if M1 result records:

- the exact primitive scalar(s) for parity tests;
- tensors and shapes for the dense primitive route;
- stopped/frozen quantities;
- unsupported modes;
- tolerances and reference comparators for primitive VJP/JVP tests;
- no unresolved derivation blocker.

## Stop Conditions

Stop and write a blocker result if:

- the finite computational scalar cannot be specified unambiguously;
- the required adjoint equations cannot be stated without changing the route;
- stopped/frozen policy is unclear;
- M2 tests would not actually check the manual adjoint;
- implementing safely would require changing public/default behavior first.
