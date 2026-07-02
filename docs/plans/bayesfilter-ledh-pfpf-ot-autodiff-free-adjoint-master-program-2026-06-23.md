# LEDH-PFPF-OT Autodiff-Free Adjoint Master Program

date: 2026-06-23
status: REVIEWED_READY_FOR_EXECUTION
program: LEDH-PFPF-OT-AUTODIFF-FREE-ADJOINT

## Objective

Eliminate autodiff from the production LEDH-PFPF-OT gradient route.  The
program exists because prior attempts reduced memory in isolated pieces but
left an outer `tf.GradientTape` around the filter value.  That is plan drift.
The new binary invariant is:

```text
No production LEDH-PFPF-OT gradient artifact may count unless the selected
route passes an explicit no-autodiff audit.
```

## Current Entry State

The inherited reviewed state is:

- `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED`;
- remediated N100 and N1000 actual-gradient artifacts validated;
- N2500 failed with trusted GPU `RESOURCE_EXHAUSTED`;
- no valid N10000 actual-gradient artifact exists;
- S8/P82 FD remains prohibited.

Source handoff:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-stop-handoff-2026-06-23.md
```

Reviewed blocker:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7r-metadata-remediation-result-2026-06-23.md
```

## Autodiff-Free Definition

For the production LEDH-PFPF-OT gradient route, forbidden APIs include:

- `tf.GradientTape`;
- `tf.autodiff.ForwardAccumulator`;
- `.gradient(` on a tape;
- `.jacobian(` or `.batch_jacobian(` on a tape;
- `tf.gradients`;
- any custom-gradient `grad` body that opens autodiff;
- hidden callback routes whose gradient depends on TensorFlow autodiff.

Allowed:

- `tf.custom_gradient` only as a boundary whose `grad` body is manually coded;
- TensorFlow tensor math in forward and manual backward code;
- tiny diagnostic or test-only autodiff comparisons, under explicit whitelist;
- static source audits and runtime sentinels that prove forbidden APIs are not
  reached on the production route.

## Route Manifest Binding

Phase 8 certification and Phase 9 GPU ladder must use one exact route
manifest.  The manifest is a required artifact before Phase 8 can pass and
must be embedded or referenced by every Phase 9 rung JSON.

Minimum route identity fields:

- git commit;
- production entrypoint;
- route name;
- exact command flags;
- `transport_ad_mode`;
- transport gradient mode;
- transport plan mode;
- dtype and TF32 policy;
- row/column/particle chunk settings;
- seed policy and seed list;
- audit tool path;
- audit tool version or hash;
- whitelist artifact path and hash;
- no-autodiff audit result path.

Any mismatch between the Phase 8 audited route manifest and a Phase 9 rung
artifact is a hard veto.  A metadata flag such as `autodiff_free_audit=pass`
does not count unless it points to the same route manifest and audit artifact.

## Whitelist Governance

The no-autodiff audit whitelist is zero-default.

Whitelist entries must be:

- exact-path or exact-symbol entries;
- diagnostic/test-only;
- justified in a written whitelist artifact;
- reviewed when added or changed.

Production modules are never whitelistable for forbidden autodiff APIs.  A
production-path forbidden API occurrence is a blocker, not a whitelist
candidate.

## Required Phase Result Schema

Every phase result must include:

- phase objective and question;
- inherited entry conditions;
- decision: `PASSED`, `BLOCKED`, or `FAILED`;
- evidence produced, with exact paths;
- local commands actually run;
- skeptical plan audit outcome;
- phase evidence contract outcome;
- veto diagnostics status;
- unresolved blockers/leaks carried forward;
- run manifest when commands or experiments ran;
- what is not concluded;
- exact next gate and handoff conditions.

If a phase partially succeeds, the result must say which gate remains blocked
and must not advance the program.

## Phase Index

| Phase | Name | Main output |
|---|---|---|
| 0 | Contract Freeze | No-autodiff contract and inherited stop-state lock |
| 1 | Callgraph Leak Inventory | Exact production callgraph and autodiff leak ledger |
| 2 | Audit Tooling | Static and runtime no-autodiff audit harness |
| 3 | Derivation Contract | Full filter-level adjoint derivation contract |
| 4 | SIR Analytical Derivatives | Analytical SIR derivative wiring plan and tests |
| 5 | LEDH Flow And Log-Weight Adjoints | Manual primitive adjoints for flow/log weights |
| 6 | Transport No-Autodiff Audit/Repair | Transport custom-gradient audit and repairs |
| 7 | Filter-Level Custom Gradient | Production no-autodiff route implementation |
| 8 | Certification Tests | Audit-enforced tiny and SIR smoke tests |
| 9 | Trusted GPU Ladder | N100 through N10000 only after audit passes |
| 10 | Closeout And FD Handoff | Final audit closeout and conditional FD handoff |

## Phase Artifacts

| Phase | Subplan | Result |
|---|---|---|
| 0 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase0-contract-freeze-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase0-contract-freeze-result-2026-06-23.md` |
| 1 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-result-2026-06-23.md` |
| 2 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-result-2026-06-23.md` |
| 3 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-result-2026-06-23.md` |
| 4 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-result-2026-06-23.md` |
| 5 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-result-2026-06-23.md` |
| 6 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-result-2026-06-23.md` |
| 7 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-filter-custom-gradient-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-filter-custom-gradient-result-2026-06-23.md` |
| 8 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-certification-tests-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-certification-tests-result-2026-06-23.md` |
| 9 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-ladder-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-ladder-result-2026-06-23.md` |
| 10 | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase10-closeout-fd-handoff-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase10-closeout-fd-handoff-result-2026-06-23.md` |

## Global Evidence Contract

| Field | Contract |
|---|---|
| Question | Can BayesFilter produce LEDH-PFPF-OT SIR gradients through the production route with no autodiff in the production gradient path? |
| Baseline/comparator | Reviewed S7R blocker: partial manual transport VJP with outer `GradientTape`, valid N100/N1000, N2500 GPU OOM. |
| Primary pass criterion | Phase 8 no-autodiff audit passes for the exact route manifest, then Phase 9 writes a valid N10000 actual-gradient JSON bound to that same route manifest and audit artifact. |
| Veto diagnostics | Any production path uses forbidden autodiff; Phase 8/9 route manifest mismatch; audit whitelist too broad; custom-gradient `grad` body opens autodiff; diagnostic autodiff is used as promotion criterion; route defaults change; `transport_ad_mode=full`; GPU ladder launched before audit pass; any Phase 9 higher rung launched after the first non-`PASSED` rung; FD launched before valid N10000 artifact. |
| Explanatory only | Tiny autodiff parity, runtime trends, memory allocator warnings, N100/N1000 finite gradients, local FD diagnostics. |
| Not concluded | No posterior correctness, HMC readiness, production default promotion, scientific superiority, Zhao-Cui source-faithfulness, or FD agreement unless separately gated. |
| Artifacts | Master program, subplans/results, audit script/results, implementation diffs, ledgers, Claude review ledger, stop handoff, GPU JSONs. |

## Global Forbidden Claims And Actions

- Do not call a route autodiff-free unless the Phase 8 audit passes.
- Do not carry an audit pass to a different route manifest.
- Do not treat `tf.custom_gradient` as sufficient; its `grad` body must be
  manually audited.
- Do not hide autodiff behind callbacks, wrappers, helper functions, or tests.
- Do not launch S8/P82 FD before a valid audited N10000 actual-gradient
  artifact exists.
- Do not use Zhao-Cui as comparator for LEDH FD consistency.
- Do not use `transport_ad_mode="full"`.
- Do not rerun or tune GPU ladders after a blocker without a reviewed
  remediation subplan.
- In Phase 9, stop at the first non-`PASSED` rung, including either `BLOCKED`
  or `FAILED`; do not launch higher rungs until a reviewed remediation plan
  exists and passes.
- The Phase 9 result must include an ordered rung ledger recording each rung
  attempted, each rung decision, the first non-`PASSED` rung if any, and
  confirmation that no higher rung was launched after that point.
- Do not change default route, public API exposure, HMC policy, model-file
  boundaries, funding boundaries, or scientific pass/fail criteria.

## Review And Repair Loop

Claude is read-only reviewer only.  Reviews must use exact path prompts and no
large artifact bundles.  Claude cannot authorize crossing human, runtime,
model-file, funding, product-capability, default-policy, or scientific-claim
boundaries.

If Claude returns `VERDICT: REVISE`, patch the same artifact visibly and rerun
focused local checks.  Stop after five review rounds for the same blocker and
write a blocker result.

## Initial Approvals Anticipated

The program anticipates needing:

- trusted Claude Code exact-path review commands;
- trusted GPU commands in Phase 9 only: `nvidia-smi`, TensorFlow GPU probe, and
  GPU ladder rungs;
- no package installs, no network fetches, no detached agents, no destructive
  git operations.

## Final Handoff Conditions

Phase 10 can close only if:

- no-autodiff audit passed on the exact production route;
- GPU ladder result passed through N10000;
- bounded Claude review agreed the audit/result artifacts are sufficient;
- FD handoff is refreshed with the exact audited N10000 artifact path.

Otherwise Phase 10 must record a blocker and keep FD prohibited.
