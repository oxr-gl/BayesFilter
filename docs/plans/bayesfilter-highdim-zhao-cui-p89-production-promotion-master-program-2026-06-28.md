# P89 Master Program: Zhao-Cui SIR d18 Production Promotion

Date: 2026-06-28

Status: `P89_MASTER_REVIEWED_AGREE`

## Objective

Start a successor program after P88 to promote the Zhao-Cui SIR d18 route from:

```text
selected_headline_label: D18_SOURCE_ROUTE_RANK_DEGREE_STABLE
```

to a production-ready implementation only through reviewed gates. P89 must not
treat P88 rank/degree evidence as correctness, analytical-gradient readiness,
HMC readiness, GPU readiness, or production readiness.

## Inherited P88 State

P88 reviewed closeout:

- `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase6-hmc-production-readiness-result-2026-06-27.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-stop-handoff-2026-06-27.md`

Inherited strongest honest label:

```text
D18_SOURCE_ROUTE_RANK_DEGREE_STABLE
```

Inherited blockers:

- `D18_CORRECTNESS_CANDIDATE` remains blocked by missing same-target
  source-backed reference bridge.
- Source-route full-history analytical derivative readiness remains blocked.
- HMC readiness, GPU readiness, production readiness, LEDH agreement, d50/d100
  scaling, posterior correctness, and default-policy readiness are not
  established.

## Governing Artifacts

- Runbook:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-visible-gated-overnight-execution-plan-2026-06-28.md`
- Execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-visible-execution-ledger-2026-06-28.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-claude-review-ledger-2026-06-28.md`
- Stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-visible-stop-handoff-2026-06-28.md`

## Phase Index

| Phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| 0 | Governance bootstrap and P88 inheritance | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase0-governance-inheritance-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase0-governance-inheritance-result-2026-06-28.md` |
| 1 | Target manifest and same-scalar branch contract | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase1-target-manifest-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase1-target-manifest-result-2026-06-28.md` |
| 2 | Same-target source-backed value bridge design | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase2-value-bridge-design-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase2-value-bridge-design-result-2026-06-28.md` |
| 3 | Value bridge implementation and validation ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase3-value-bridge-validation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase3-value-bridge-validation-result-2026-06-28.md` |
| 4 | Source-route analytical derivative design | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase4-derivative-design-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase4-derivative-design-result-2026-06-28.md` |
| 5 | Analytical derivative implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase5-derivative-implementation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase5-derivative-implementation-result-2026-06-28.md` |
| 6 | FD validation of same-scalar analytical gradient | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase6-fd-gradient-validation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase6-fd-gradient-validation-result-2026-06-28.md` |
| 7 | HMC readiness gate | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase7-hmc-readiness-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase7-hmc-readiness-result-2026-06-28.md` |
| 8 | GPU/XLA production execution gate | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase8-gpu-xla-production-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase8-gpu-xla-production-result-2026-06-28.md` |
| 9 | Training policy, packaging, CI, and docs gate | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase9-production-packaging-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase9-production-packaging-result-2026-06-28.md` |
| 10 | Final production promotion decision | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase10-final-production-decision-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase10-final-production-decision-result-2026-06-28.md` |

Dedicated subplans are created before each phase executes. A later phase cannot
start from this master alone.

Sequential gate rule: a phase that depends on an earlier gate may execute only
if the earlier gate's result artifact records a reviewed pass, unless the new
phase is explicitly labeled diagnostic-only and non-promotional in a reviewed
subplan. In particular:

- Phase 4 derivative design cannot promote readiness unless Phases 2-3 have
  produced a reviewed same-target value bridge pass.
- Phase 5 implementation cannot start unless Phase 4 records a reviewed design
  pass or a reviewed diagnostic-only exception.
- Phase 6 FD validation cannot start unless Phase 5 records a reviewed
  analytical-derivative implementation pass.
- Phase 7 HMC readiness cannot start unless Phases 3 and 6 record reviewed
  value and gradient passes.
- Phase 8 GPU/XLA production readiness cannot start unless Phase 7 records a
  reviewed HMC readiness pass.
- Phases 9-10 cannot start unless all prior production-promotional gates pass
  or the subplan explicitly narrows them to non-promotional closeout.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Zhao-Cui SIR d18 be promoted from rank/degree-stable source-route evidence to production-ready implementation without repeating prior testing mistakes? |
| Baseline/comparator | P88 reviewed closeout, same-target source-backed reference bridge once built, central FD of the exact same scalar, and later HMC/GPU production diagnostics only after correctness and derivative gates pass. |
| Primary pass criterion | Production readiness is allowed only if same-target value correctness, source-route analytical-gradient correctness, FD same-scalar validation, HMC readiness, GPU/XLA production readiness, and packaging/CI/docs gates all pass with reviewed artifacts. |
| Veto diagnostics | Rank/degree evidence treated as correctness; FD of the wrong scalar; gradient validated before value bridge; local fixed-branch evidence promoted to source-route retained-object readiness; JVP/autodiff promoted as analytical route; missing same-branch manifest; stale ALS route; audit tuning; missing L1 tuning; HMC/GPU/production run before reviewed protocol; default-policy change without reviewed gate. |
| Explanatory diagnostics | Value residuals, FD step-size ladders, gradient residuals, sampler diagnostics, runtime/memory, XLA compile cache behavior, CPU/GPU parity, validation/holdout/audit curves. |
| Not concluded | Production readiness, HMC readiness, posterior correctness, source-route correctness, full-history analytical-gradient correctness, GPU readiness, LEDH agreement, d50/d100 scaling, or default-policy change until the relevant phase explicitly passes. |
| Artifacts | P89 master, runbook, subplans/results, ledgers, target manifests, bridge manifests, derivative manifests, runtime manifests, final stop handoff. |

## Claim Ladder

| Claim | Current status | P89 gate |
| --- | --- | --- |
| `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` | Passed/reviewed in P88 | Inherited baseline only. |
| Exact same-scalar target manifest | Not established | Phase 1. |
| `D18_CORRECTNESS_CANDIDATE` | Blocked by missing same-target source-backed bridge | Phases 2-3. |
| Source-route full-history analytical-gradient readiness | Blocked by missing retained-object derivative propagation | Phases 4-6. |
| HMC readiness | Not established | Phase 7, only after value and gradient gates pass. |
| GPU/XLA production readiness | Not established | Phase 8, only after the Phase 7 HMC readiness gate records a reviewed pass. |
| Production-ready Zhao-Cui SIR d18 | Not established | Phases 9-10 after all earlier gates pass. |

## Mandatory Lessons Carried Forward

- Value bridge comes before gradient validation.
- FD validates the analytical gradient of the exact same scalar only; it is not
  a source-faithfulness proof by itself.
- Same target, same branch, same retained objects, same basis/rank/samples/
  schedules, and same parameterization must be manifest-bound before comparing
  value or gradient.
- Training-base optimizer only.
- L1 weight tuning is the default Zhao-Cui training procedure.
- Zero-L1 is a comparator arm only.
- No ALS training revival.
- Validation/holdout/audit clouds remain separate.
- Audit cloud is never used for tuning.
- Plateau LR scheduling and stop-after-no-benefit rules are required for new
  training evidence.
- Sample budget must scale with parameter count.
- Basis/order/rank are setup-static choices for XLA; changing them can require
  a new compile and a new manifest.

## Review Protocol

Claude is read-only reviewer only. Codex is supervisor and executor. Material
subplans/results use bounded one-path prompts and stop after five review rounds
for the same blocker. Claude cannot authorize crossing human, runtime,
model-file, funding, product-capability, default-policy, or scientific-claim
boundaries.

## Launch Rule

P89 may launch Phase 0 only after this master, the visible runbook, and the
Phase 0 subplan pass local artifact checks and bounded Claude Opus max-effort
read-only review.
