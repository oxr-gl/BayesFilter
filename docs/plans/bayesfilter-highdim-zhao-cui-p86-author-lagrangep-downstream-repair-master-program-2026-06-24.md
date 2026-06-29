# P86 Zhao-Cui Author Lagrangep Downstream Repair Master Program

Date: 2026-06-24

Status: `BLOCK_P86_ZHAO_CUI_SIR_NOT_PRODUCTION_PROMOTED_REVIEWED`

## Objective

Close, or precisely block, the remaining Zhao-Cui SIR production gaps that P85
left after repairing the setup surface. P86 starts from the reviewed P85 state:

```text
The author SIR setup can be declared as Lagrangep(4,8) plus
AlgebraicMapping(1), but the author algebraic Lagrangep route cannot yet be fit
or promoted because mass, integral, measure, downstream, fitting, convergence,
correctness, KR, derivative, HMC, comparator, scale, and production gates remain
open.
```

P86 is a visible gated program. Codex is supervisor and executor. Claude Opus
max effort may be used only as a read-only reviewer of bounded one-path prompts.

## Governing Inputs

- `docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-stop-handoff-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p85-configurable-basis-domain-reset-memo-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p84-production-promotion-master-program-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase2-budget-compliant-fitting-subplan-2026-06-23.md`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:43-55`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/LagrangeRef.m:1-67`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Piecewise.m:1-67`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Lagrangep.m:12-52`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Domains/AlgebraicMapping.m:5-43`
- `bayesfilter/highdim/bases.py`
- `bayesfilter/highdim/tt.py`
- `bayesfilter/highdim/squared_tt.py`
- `bayesfilter/highdim/stochastic_density_training.py`
- `bayesfilter/highdim/derivatives.py`
- `bayesfilter/highdim/ukf_initializer.py`
- `tests/highdim/test_p85_configurable_basis_domain.py`

## Source-Anchor Premise

The only source-faithful setup claims allowed at P86 launch are:

| Claim | Anchor | Classification |
|---|---|---|
| The author SIR script builds `ApproxBases(Lagrangep(4,8), AlgebraicMapping(1), d + 2*m)` and solves with it. | `eg3_sir/mainscript.m:43-55` | `source_faithful_setup_surface` |
| `LagrangeRef` defines the local `[0,1]` interpolation nodes, barycentric weights, local mass, and local integral weights. | `LagrangeRef.m:1-67` | `source_faithful_local_basis_rule` |
| `Piecewise` fixes the default piecewise domain `[-1,1]`, element grid, and constant reference measure. | `Piecewise.m:1-67` | `source_faithful_reference_domain_rule` |
| `Lagrangep` assembles global nodes, local-to-global mapping, unweighted mass, integral weights, and normalized mass/int weights. | `Lagrangep.m:12-52` | `source_faithful_mass_integral_rule` |
| `AlgebraicMapping(1)` maps physical values to reference values and exposes both Jacobian log-density directions. | `AlgebraicMapping.m:5-43` | `source_faithful_domain_map_formula` |
| P85 BayesFilter currently represents the author setup but raises `NotImplementedError` for Lagrangep mass/integral. | `bayesfilter/highdim/bases.py` and `tests/highdim/test_p85_configurable_basis_domain.py` | `local_gap` |

Any use of "faithful", "source-faithful", "author-route", or equivalent in P86
must cite both an author paper/source anchor and a local implementation/result
anchor. If a later phase freezes or changes randomness, ranks, bases, schedules,
or samples for differentiability or HMC, classify that as
`fixed_hmc_adaptation`. If a route is not in the author source, classify it as
`extension_or_invention`.

## Whole-Program Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the Zhao-Cui SIR lane move from P85 setup-only author configuration to a reviewed author algebraic Lagrangep route whose remaining production gaps are each closed or blocked by evidence? |
| Baseline/comparator | P85 setup-only author config, P84 production-promotion gates, Zhao-Cui author source anchors, and current BayesFilter TensorFlow/TFP highdim implementation. |
| Primary pass criterion | Every P86 phase has a result with either passing artifacts and review trail or a precise blocker. Production promotion requires all mandatory gates plus explicit owner approval; P86 planning alone cannot promote. |
| Veto diagnostics | Missing paper/source/local anchors; treating P85 setup as fitting/correctness evidence; treating local Legendre diagnostic route as author parity; using proxy metrics as promotion criteria; unapproved fitting/GPU/HMC/LEDH/d50/d100/long commands; XLA dynamic basis switching inside hot paths; changing default policy without owner approval. |
| Explanatory diagnostics | Source inventories, exact 1D mass/integral checks, measure-convention ledgers, CPU-hidden unit/smoke tests, fit residuals, holdout/replay rows, rank/degree deltas, reference-bridge residuals, KR diagnostics, derivative checks, HMC diagnostics, LEDH summaries, scale telemetry. |
| Not concluded | No posterior correctness, HMC readiness, LEDH superiority, d=50/d=100 scaling, production readiness, default-policy change, or broad scientific claim until the corresponding phase gate passes. |
| Artifacts | This master program, visible runbook, execution ledger, Claude review ledger, subplans/results, JSON manifests, blocker notes, stop handoff, and final reset memo. |

## Skeptical Plan Audit

Pre-execution audit result:

- Wrong baseline risk is high. P86 must start from P85 setup-only status and
  P84 production gates, not from any execution-only or smoke result.
- Proxy-promotion risk is high. Mass/integral unit tests, tiny fits, validation
  loss, finite replay, ESS, finite derivatives, short chains, and local smokes
  can nominate, explain, or veto only under the phase evidence contract.
- Hidden-assumption risk is highest at the algebraic measure boundary. P86
  separates exact reference-domain Lagrangep mass/integral from algebraic
  physical-domain density/Jacobian conventions before fitting.
- XLA risk is controlled by keeping basis family, order, element count, domain
  map family, scale, dimension, and dtype setup-static. Changing those choices
  may retrace/recompile; P86 must not implement runtime tensor switching.
- Artifact risk is controlled by requiring every phase to produce a result or
  blocker, refresh the next subplan, and review material gates.
- Environment risk is controlled by exact approval gates. GPU/CUDA/NVIDIA,
  HMC/MCMC, LEDH, d=50/d=100, long, fitting, network, model-file, and detached
  commands are not authorized by this master program.

P86 may launch Phase 0 because it is a governance/document phase and does not
run fitting, GPU, HMC, LEDH, MCMC, d=50/d=100, long, or production commands.

## Phase Ladder

Phase 0 owns creation and first review of these whole-program artifacts:

- visible runbook:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-gated-execution-runbook-2026-06-24.md`;
- execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`;
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`;
- stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-stop-handoff-2026-06-24.md`.

Phase 11 owns the final reset memo and final handoff refresh if P86 reaches the
production-decision phase. Earlier phases own only their listed result
artifacts and any phase-local manifests explicitly named in their subplans.

| Phase | Name | Subplan | Required result |
|---|---|---|---|
| P86-0 | Scope, source, approval, and XLA freeze | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase0-scope-source-xla-freeze-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase0-scope-source-xla-freeze-result-2026-06-24.md` |
| P86-1 | Lagrangep mass and integral implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase1-lagrangep-mass-integral-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase1-lagrangep-mass-integral-result-2026-06-24.md` |
| P86-2 | Algebraic measure convention contract | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase2-algebraic-measure-contract-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase2-algebraic-measure-contract-result-2026-06-24.md` |
| P86-3 | Downstream squared-density, normalizer, marginal, quadrature, and transport wiring | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase3-downstream-author-route-wiring-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase3-downstream-author-route-wiring-result-2026-06-24.md` |
| P86-4 | Tiny author-route fit smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-result-2026-06-24.md` |
| P86-5 | Budget-compliant P84 Phase 2 fit | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-result-2026-06-24.md` |
| P86-6 | Rank and degree convergence | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-result-2026-06-24.md` |
| P86-7 | Correctness bridge | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase7-correctness-bridge-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase7-correctness-bridge-result-2026-06-24.md` |
| P86-8 | KR and transport closure | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase8-kr-transport-closure-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase8-kr-transport-closure-result-2026-06-24.md` |
| P86-9 | Derivative and HMC readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase9-derivative-hmc-readiness-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase9-derivative-hmc-readiness-result-2026-06-24.md` |
| P86-10 | LEDH comparator and scale stress | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase10-ledh-scale-stress-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase10-ledh-scale-stress-result-2026-06-24.md` |
| P86-11 | Production promotion decision and reset memo | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase11-production-decision-reset-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase11-production-decision-reset-result-2026-06-24.md` |

## Approval Gates To Anticipate

- Claude read-only review through the trusted wrapper requires escalated
  permissions and model access.
- CPU-hidden TensorFlow tests may run only with `CUDA_VISIBLE_DEVICES=-1`
  recorded in the artifact.
- Any GPU/CUDA/NVIDIA detection, initialization, benchmark, XLA-GPU, GPU smoke,
  or GPU ML command requires escalated permissions and exact approval.
- Any fitting command, including the tiny author-route smoke if it trains or
  optimizes parameters, requires explicit exact-command approval before
  execution.
- Any HMC/MCMC/NUTS command requires exact-command human approval before
  execution.
- Any LEDH/PFPF/OT comparator command requires exact-command human approval
  before execution.
- Any d=50/d=100, long-running, detached, overnight worker, package install,
  network fetch, remote, funding, model-file, default-policy, or production
  promotion action requires explicit owner approval.
- Git add/commit/push is outside P86 unless separately requested.

## Per-Phase Protocol

Every phase must use its dedicated subplan. At the end of each phase:

1. run the required local checks;
2. write a phase result or blocker;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, boundary safety, stop conditions, and approval needs;
5. use Claude read-only review for material subplans/results/blockers;
6. repair visibly and rerun focused checks when fixable;
7. stop after five Claude review rounds for the same blocker.

Claude is not an execution authority. A `VERDICT: AGREE` can support plan
consistency only; it cannot authorize human, runtime, model-file, funding,
product-capability, default-policy, or scientific-claim boundaries.

## Production Promotion Rule

`PASS_P86_ZHAO_CUI_SIR_PRODUCTION_PROMOTION_REVIEWED` is allowed only if all
mandatory gates pass and the owner explicitly approves promotion:

- source-anchored author Lagrangep mass/integral;
- algebraic measure convention;
- downstream squared-density/normalizer/marginal/quadrature/transport wiring;
- approved fitting artifact satisfying the budget floor;
- same-route rank/degree convergence;
- same-target correctness bridge;
- KR/transport closure or explicitly scoped product limitation;
- derivative readiness when gradient use is in scope;
- HMC readiness when HMC is in scope;
- fair LEDH comparator when used in the production claim;
- scale/stress and uncertainty accounting for any d=50/d=100 claim;
- final review and owner approval.

Until those gates pass, the strongest allowed P86 conclusion is a narrower
phase result or a precise blocker.
