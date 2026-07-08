# P85 Zhao-Cui Configurable Basis/Domain Repair Master Program

Date: 2026-06-23

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Objective

Repair the P84 Phase 1 blocker by making the Zhao-Cui basis and domain mapping
an explicit setup parameter in the BayesFilter source-route lane.

P85 is allowed to replace the current fixed Legendre-only diagnostic surface
with a reviewed configuration surface that can distinguish:

- the current BayesFilter Legendre bounded diagnostic route;
- the author SIR route using `Lagrangep(4,8)` with `AlgebraicMapping(1)`;
- any future route as either `source_faithful`, `fixed_hmc_adaptation`, or
  `extension_or_invention`.

P85 does not run production fitting and does not promote Zhao-Cui to production.
It only repairs or precisely blocks the P84 author-basis/domain parity break.

## Governing Inputs

- `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase1-author-basis-domain-parity-result-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p84-visible-stop-handoff-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p83-final-reset-memo-2026-06-23.md`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/README.md:28-41`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:39-55`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/ApproxBases.m:1-12`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/ApproxBases.m:70-119`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Lagrangep.m:12-52`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Domains/AlgebraicMapping.m:5-43`
- `bayesfilter/highdim/bases.py:55-143`
- `bayesfilter/highdim/source_route.py:2262-2269`
- `bayesfilter/highdim/source_route.py:3421-3427`

## Source-Anchor Premise

The P85 repair is source-backed only to the following extent:

| Claim | Anchor | Classification |
|---|---|---|
| Basis/domain are user-selectable setup choices in the author code. | `source/README.md:28-41` | `source_faithful_setup_surface` |
| SIR author script constructs both bounded and algebraic-mapped `Lagrangep(4,8)` bases. | `eg3_sir/mainscript.m:43-45` | `source_faithful_sir_config` |
| The SIR solve uses the algebraic-mapped basis. | `eg3_sir/mainscript.m:53-56` | `source_faithful_sir_config` |
| `ApproxBases` repeats a one-dimensional basis/domain mapping across dimensions. | `ApproxBases.m:70-119` | `source_faithful_replication_semantics` |
| Current BayesFilter hard-codes bounded Legendre product bases. | `bases.py:55-143`, `source_route.py:2262-2269`, `source_route.py:3421-3427` | `local_gap` |

Any claim beyond these anchors requires a phase result, local tests, and review.

## Role Contract

Codex is the visible supervisor and executor.

Claude Opus max effort may be used only as a read-only reviewer of compact,
bounded one-path prompts. Claude is not an execution authority and cannot
authorize crossing human, runtime, GPU, model-file, funding, product-capability,
default-policy, or scientific-claim boundaries.

## Whole-Program Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the P84 Phase 1 basis/domain blocker be repaired by making basis family and domain mapping explicit setup parameters without weakening source-anchor, XLA, or production-claim boundaries? |
| Baseline/comparator | P84 Phase 1 blocker, author README/SIR/source basis anchors, and current local Legendre-only source-route code. |
| Primary pass criterion | A reviewed implementation and manifest/test surface can represent the author `Lagrangep(4,8)` plus `AlgebraicMapping(1)` route and the existing Legendre diagnostic route as distinct setup configurations, with source classification preserved. |
| Veto diagnostics | Missing author anchors; treating Legendre as author parity; treating configurable setup as fit/correctness/scaling evidence; Python/runtime basis switching inside XLA hot paths; copying third-party code without review; running fitting/GPU/HMC/LEDH/long commands without exact approval. |
| Explanatory diagnostics | Basis cardinality, local evaluation shapes, domain-map formulas, manifest identity fields, CPU-hidden unit tests, static `tf.function` trace behavior. |
| Not concluded | No fit quality, posterior correctness, KR closure, HMC readiness, LEDH agreement, d=50/d=100 scaling, default-policy change, or production readiness. |
| Artifacts | This master program, visible runbook, execution ledger, Claude review ledger, phase subplans/results, optional implementation diff, stop handoff, and final reset memo. |

## Skeptical Plan Audit

Pre-execution audit result:

- Wrong baseline risk is controlled by starting from the P84 blocker. P85 must
  compare against author basis/domain anchors and local hard-coded Legendre
  anchors, not against P83 execution-only status.
- Proxy-promotion risk is controlled by forbidding fit/correctness/scaling
  claims. Unit tests can support implementation behavior only.
- Hidden-assumption risk is material. Phase 1 must inventory `Lagrangep`,
  `ApproxBases`, and `AlgebraicMapping` semantics before interface design.
- XLA risk is material. Basis family, basis cardinality, degree/order, element
  count, domain-map family, scale, and dimension must be setup/static choices
  for a compiled run. Changing any of those may retrace/recompile and is not a
  runtime tensor switch.
- Artifact risk is controlled by requiring every phase to produce a result or
  blocker and by reviewing material phases with bounded Claude prompts.

P85 may begin with Phase 0 because it is a governance/document phase and does
not run fitting, GPU, LEDH, HMC, MCMC, d=50/d=100, long, or production commands.

## Phase Ladder

| Phase | Name | Subplan | Required result |
|---|---|---|---|
| P85-0 | Governance, scope, and XLA boundary freeze | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase0-governance-xla-freeze-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase0-governance-xla-freeze-result-2026-06-23.md` |
| P85-1 | Author basis/domain semantics inventory | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase1-author-basis-domain-inventory-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase1-author-basis-domain-inventory-result-2026-06-23.md` |
| P85-2 | Config interface and XLA contract design | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase2-config-interface-xla-contract-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase2-config-interface-xla-contract-result-2026-06-23.md` |
| P85-3 | Implementation and test matrix review | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase3-implementation-test-matrix-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase3-implementation-test-matrix-result-2026-06-23.md` |
| P85-4 | Minimal configurable basis/domain implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md` |
| P85-5 | Manifest classification and regression checks | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-result-2026-06-23.md` |
| P85-6 | P84 handoff and reset memo | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-result-2026-06-23.md` |

## Approval Gates To Anticipate

- Claude read-only review through the trusted wrapper requires escalated
  permissions.
- CPU-hidden TensorFlow unit tests may be run only with `CUDA_VISIBLE_DEVICES=-1`
  recorded in the result artifact.
- Any GPU/CUDA/NVIDIA probe or run requires escalated permissions.
- Any fitting, validation ladder, LEDH comparison, HMC/MCMC, d=50/d=100,
  long-running command, or production claim requires exact-command human
  approval outside P85.
- Any default-policy or production-promotion decision requires explicit owner
  approval.
- Git add/commit/push is outside P85 unless the user requests it after review.

## Per-Phase Protocol

Every phase must use its dedicated subplan. At the end of each phase:

1. run required local checks;
2. write a phase result or blocker;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, boundary safety, stop conditions, and approval needs;
5. use Claude read-only review for material subplans or material blockers;
6. repair visibly and rerun focused checks when fixable;
7. stop after five Claude review rounds for the same blocker.

## Final Repair Rule

`PASS_P85_P84_PHASE1_BASIS_DOMAIN_REPAIR` is allowed only if P85 shows that the
BayesFilter source-route lane can represent the author SIR basis/domain setup
and the legacy Legendre diagnostic route as distinct, reviewed configurations.

That status may unblock P84 Phase 1 only. P84 Phase 2 fitting and all later
production-promotion gaps remain blocked until their own reviewed gates pass.
