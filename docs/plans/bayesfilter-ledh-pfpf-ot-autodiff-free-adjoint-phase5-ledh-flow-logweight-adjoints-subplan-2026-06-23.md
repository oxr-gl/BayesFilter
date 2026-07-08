# Phase 5 Subplan: LEDH Flow And Log-Weight Adjoints

status: REFRESHED_AFTER_P4_DRAFT_READY_FOR_REVIEW
date: 2026-06-23
phase: P5-LEDH-FLOW-LOGWEIGHT-ADJOINTS

## Phase Objective

Implement manual adjoints for LEDH affine flow, observation residual terms,
transition/observation log densities, log-weight normalization, and likelihood
increment accumulation, as assigned by the P3 derivation contract.

## Entry Conditions

- P4 analytical SIR derivative gate passed.
- P3 derivation contract assigns primitive adjoint responsibilities.
- P5 inherits the P4 SIR derivative interface and may not introduce a hidden
  autodiff fallback for any SIR/model callback cotangent.
- P4 provides model-level analytical SIR methods for theta scaling,
  transition-mean parameter Jacobian, transition log-density parameter score,
  observation log-density parameter score, and infectious-component VJP.
- Transport repair, filter-level route certification, GPU, FD, and
  actual-gradient validation remain forbidden in P5.

## Required Artifacts

- Implementation diffs.
- Primitive adjoint tests.
- P5 result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-result-2026-06-23.md`.
- Refreshed P6 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-subplan-2026-06-23.md`.
- Primitive adjoint interface note or in-result section for Gaussian
  log-density, log-normalization, floor-mask handling, LEDH flow matrix
  primitives, and theta-score accumulation boundaries.

## Required Checks/Tests/Reviews

- CPU-hidden primitive tests.
- Tiny diagnostic autodiff comparisons in tests only.
- No finite-difference checks in P5.
- P2 audit run must still fail only for known later unimplemented phases, not
  new P5 production leaks.
- Static scan must show P5 production primitives do not open
  `tf.GradientTape`, `ForwardAccumulator`, or tape `.gradient`/`.jacobian`.
- Bounded Claude review.

Exact local commands expected before P5 close:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile <touched-python-files>

CUDA_VISIBLE_DEVICES=-1 python -m pytest <focused-p5-test-files> -q

python scripts/audit_ledh_no_autodiff.py --manifest docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json --whitelist docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-current-route-audit-result-2026-06-23.json --expect-decision FAIL_CURRENT_ROUTE

rg -n 'GradientTape|ForwardAccumulator|tape\.gradient|tape\.jacobian|tf\.gradients' <touched-production-files> <focused-p5-test-files>

git diff --check -- <touched-files-and-p5-artifacts>
```

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are non-transport filter primitives manually differentiable without production autodiff? |
| Baseline/comparator | P3/P4 contracts and tiny diagnostic autodiff parity checks in tests only; no finite differences in P5. |
| Primary criterion | Primitive adjoint tests pass for transition log-density adjoints, observation log-density adjoints, Gaussian covariance/state residual terms, log-normalization, likelihood-increment accumulation, floor-mask handling, LEDH flow interfaces, and no new production autodiff leak. |
| Veto diagnostics | Hidden tape in primitive; missing shape contract; transition or observation log-density adjoint absent; likelihood-increment adjoint absent; log-normalization adjoint absent; floor-mask derivative silently delegated to TensorFlow; LEDH flow matrix primitive VJP missing; finite differences used in P5. |
| Explanatory only | Tiny autodiff parity residuals. |
| Not concluded | Full route certification or GPU feasibility. |
| Preserved artifact | P5 result artifact path listed above. |

## Forbidden Claims/Actions

- Do not promote tiny parity to full correctness.
- Do not run GPU ladder or FD.
- Do not change defaults.
- Do not run finite differences in P5.
- Do not repair transport custom-gradient bodies except to keep P5 tests from
  selecting an unauthorized transport route.
- Do not claim that P5 closes P1-L013/P1-L015; those remain P6 transport leaks.

## Exact Next-Phase Handoff Conditions

Advance to P6 only if transport no-autodiff audit can compose with P5 adjoints.
The P6 subplan must inherit P5 cotangent shapes for `post_flow`,
`normalized_logw`, and transport inputs, and must keep P1-L013/P1-L015 as
open until the transport `grad` body is audited and repaired.

## Stop Conditions

- Primitive adjoint cannot be derived or tested.
- Audit fails with unexplained production leak.
- Any LEDH flow/log-density/log-weight primitive still needs production
  autodiff.
- Transition or observation log-density, likelihood-increment accumulation, or
  floor-mask obligations are missing.
- Any P5 check would require finite differences.
- P5 would require transport repair, GPU, FD, or actual-gradient evidence to
  pass.
