# P88 Phase 5 Result: Source-Route Derivative Design

Date: 2026-06-27

Status: `P88_PHASE5_REVIEWED_BLOCK_SOURCE_ROUTE_DERIVATIVE_READINESS_CLOSED`

Git commit: `97ad05d40676f3fd15a2a2b4d45034ebb657ed97`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 5 blocks source-route full-history analytical derivative readiness. P87 repaired local fixed-branch score plumbing, but the source-route retained-object loop still lacks source-backed same-branch derivative propagation through previous marginal density, transport/proposal correction, normalizer terms, and branch identities. |
| Primary criterion status | Not met. Every derivative component could be classified, but the classification shows missing connective wiring for a full source-route scalar derivative. |
| Veto diagnostic status | No JVP/ForwardAccumulator evidence is promoted. Local fixed-branch and tiny full-history evidence remain secondary. Phase 4 correctness blocker is preserved. |
| Main uncertainty | A future implementation phase could wire source-backed TTSIRT map/potential derivative operations and retained-object derivative propagation, but this Phase 5 design audit did not implement or certify it. |
| Next justified action | Review this result and the refreshed Phase 6 final readiness subplan. If both agree, Phase 6 may close P88 with the strongest honest label and unresolved blockers. |
| What is not being concluded | No implemented derivative correctness, source-route analytical-gradient readiness, `D18_CORRECTNESS_CANDIDATE`, HMC readiness, GPU readiness, production readiness, LEDH agreement, d50/d100 scaling, or default-policy readiness. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Is there a source-route full-history analytical derivative design that can be implemented without JVP/autodiff promotion? |
| Baseline/comparator | P87 JVP-free fixed-branch repair, P83/P87/P88 source-route boundaries, Phase 4 correctness blocker, and author paper/source anchors. |
| Primary criterion | Failed for readiness: components are classified below, but the full source-route derivative path is incomplete. |
| Veto diagnostics | Missing source-route derivative wiring remains active; JVP/ForwardAccumulator and local fixed-branch evidence are not promoted. |
| Explanatory diagnostics | P87 local SIR score hooks and tiny fixed-branch regression are useful implementation substrates only. |
| Not concluded | Implemented derivative correctness, correctness-candidate status, HMC readiness, production readiness, GPU readiness, LEDH agreement, or default-policy readiness. |
| Artifact | This Phase 5 result and refreshed Phase 6 final readiness subplan. |

## Component Classification

| Component | Local anchors | Source anchors | Classification | Phase 5 decision |
| --- | --- | --- | --- | --- |
| Local SIR model theta score hooks | `bayesfilter/highdim/models.py:753-885`; P87 Phase 2/3 results | Model algebra is local clean-room, not author TTSIRT retained-object derivative code | fixed-HMC/local implementation substrate | Useful and JVP-free, but not full source-route derivative readiness. |
| Fixed-branch target derivative dispatch | `bayesfilter/highdim/filtering.py:2404-2416`, `:2490-2498`, `:2555-2567`, `:2628-2652`, `:4118-4126`, `:4146-4154`, `:4181-4189`, `:4319-4435` | No direct author retained-object full-scalar derivative anchor | fixed-branch/local substrate; reverse-mode fallback is diagnostic only | Cannot be promoted as source-route derivative path. |
| Fixed LS/TT algebra derivatives | `bayesfilter/highdim/derivatives.py:521-654` | General TT/normalizer algebra relates to source mass terms but is not full retained-object source loop | reusable analytical primitive | Needs source-route dot targets, dot transports, dot retained marginals, and branch manifest before readiness. |
| Source-route retained-object loop | `bayesfilter/highdim/source_route.py:7715-7813`, `:7837-7891`, `:7894-8039`, `:8086-8138` | Author retained-object/push/marginalization lineage from P83/P57/P61 anchors | source-route mechanics without derivative carry | Missing derivative propagation through previous retained marginal, target, proposal correction, and normalizer. |
| Author TTSIRT inverse/potential/gradient operations | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_irt_reference.m:1-188`; `ApproxFun.m:30-38`, `:114-123` | Same | source-backed derivative-capable map/potential operations exist upstream | Not locally wired into source-route scalar derivative. |
| Author TTSIRT map Jacobian | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_rt_jac_reference.m:1-208`; `AbstractIRT.m:275-294` | Same | source-backed map-Jacobian operation exists upstream | Candidate future anchor for transport derivative, not current readiness. |
| Author marginalization and normalizer | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:1-87`; `AbstractIRT.m:299-307` | Same | source-backed retained marginal / pdf normalizer operations | Local value route uses these semantics, but derivative of retained marginal and normalizer carry is not wired. |
| P87 local tiny full-history regression | P87 Phase 5 result | N/A for source-route retained-object TTSIRT derivative | diagnostic/local fixed-branch evidence | Does not close source-route full-history derivative readiness. |

## Required Future Design Before Readiness

A future implementation phase would need all of the following before any
source-route analytical-gradient readiness claim:

- a same-branch manifest tying value and derivative to the same retained
  objects, ranks, bases, samples, schedules, and branch identities;
- derivative of the source-route physical target terms in retained-object
  ordering `[theta, x_t, x_{t-1}]`;
- derivative propagation through `source_route_previous_marginal_log_density`,
  including the marginal transport and affine prefix determinant;
- derivative propagation through `source_route_generate_retained_samples`,
  including proposal log density, target log density, correction weights,
  normalized correction, and normalizer contribution;
- source-backed TTSIRT map/potential/Jacobian wiring rather than numerical
  grid-CDF or local fixed-branch substitutes for the promoted route;
- focused tests that use FD/JVP/autodiff only as diagnostics and explicitly
  fail if the promoted path depends on them;
- a clear separation between local SIR model score algebra and full filter-level
  source-route derivative correctness.

## Local Checks

Commands:

```bash
rg -n "ForwardAccumulator|tensorflow_forward_accumulator_for_model_log_density|target_derivative_backend|model_parameter_score_or_reverse_mode_gradient_tape|source_route_previous_marginal_log_density|source_route_sequential_negative_log_physical_density|source_route_run_sequential_fixed_hmc|squared_tt_normalizer_derivative|fixed_design_lsq_derivative" bayesfilter/highdim docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-result-2026-06-22.md docs/plans/bayesfilter-highdim-zhao-cui-p87-phase2-analytical-route-repair-result-2026-06-26.md docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-result-2026-06-26.md docs/plans/bayesfilter-highdim-zhao-cui-p88*.md -g '*.py' -g '*.md'
rg -n "eval_rt_jac_reference|eval_irt_reference|grad_reference|marginalise|eval_pdf|ApproxFun|AbstractIRT" third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-result-2026-06-22.md docs/plans/bayesfilter-highdim-zhao-cui-p88*.md -g '*.m' -g '*.md'
rg -n "P88_PHASE5_LOCAL_BLOCK_SOURCE_ROUTE_DERIVATIVE_READINESS|D18_CORRECTNESS_CANDIDATE.*blocked|source-route full-history analytical derivative readiness|Do not run HMC/GPU/production" docs/plans/bayesfilter-highdim-zhao-cui-p88-phase5-source-route-derivative-design-result-2026-06-27.md docs/plans/bayesfilter-highdim-zhao-cui-p88-phase6-hmc-production-readiness-subplan-2026-06-27.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p88*.md
```

Outcomes:

- Local derivative surfaces and prior blocker/repair artifacts were found and classified.
- Author TTSIRT inverse, potential/gradient, Jacobian, marginalization, and pdf anchors were found.
- P88 Phase 5/6 blocker and handoff anchors passed after patch.
- Diff hygiene passed.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Execution target | Local document/code/source audit only. |
| CPU/GPU status | No TensorFlow numerical command and no GPU/CUDA command were run. |
| Runtime/HMC status | No derivative implementation, bridge, HMC, sampler, production benchmark, package, network, or default-policy command was run. |
| Phase 4 upstream fact | `D18_CORRECTNESS_CANDIDATE` remains blocked by missing same-target source-backed bridge. |
| Derivative status | Source-route full-history analytical derivative readiness blocked. |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase5-source-route-derivative-design-subplan-2026-06-27.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase5-source-route-derivative-design-result-2026-06-27.md` |

## Boundary Notes

- P87 repaired a JVP-free local fixed-branch route, but this does not establish source-route retained-object derivative readiness.
- P87 local SIR algebra and tiny full-history regression remain useful implementation evidence only.
- The source-route value mechanics are present, but derivative propagation through retained objects and source-backed transport operations is not wired.
- Correctness remains blocked independently by Phase 4. Even a future derivative repair would not by itself create `D18_CORRECTNESS_CANDIDATE`.

## Phase 6 Handoff

The refreshed Phase 6 subplan is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase6-hmc-production-readiness-subplan-2026-06-27.md`

Phase 6 may start only after this Phase 5 result and the refreshed Phase 6
subplan receive bounded review. Phase 6 must preserve both blockers:

- `D18_CORRECTNESS_CANDIDATE` remains blocked by missing same-target bridge.
- Source-route full-history analytical derivative readiness remains blocked.

## Claude Review Status

Reviewed by bounded read-only Claude review on 2026-06-28 HKT.

Reviewer summary:

- The result correctly blocks source-route full-history analytical derivative
  readiness.
- P87 local fixed-branch evidence is preserved as secondary implementation or
  diagnostic evidence only.
- JVP/autodiff/fixed-branch evidence is not promoted.
- Correctness, HMC, GPU, production, LEDH, scale, and default-policy overclaims
  are avoided.

Verdict:

```text
VERDICT: AGREE
```
