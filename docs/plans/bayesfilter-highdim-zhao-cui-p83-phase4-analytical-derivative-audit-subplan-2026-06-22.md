# P83 Phase 4 Subplan: Analytical Fixed-Branch Derivative Audit

Date: 2026-06-22

Status: `READY_AFTER_PHASE3_REVIEW`

## Phase Objective

Audit whether the current Zhao-Cui fixed-TTSIRT source route has a
source-backed same-branch analytical derivative path suitable for later
validation work.

Phase 4 must distinguish:

- source-backed analytical derivative route;
- fixed-HMC adaptation that preserves the author's route while freezing branch
  choices;
- diagnostic-only FD/JVP/ForwardAccumulator evidence;
- extension or invention.

If only FD/JVP/ForwardAccumulator evidence exists, Phase 4 must write a blocker
or a follow-up design, not claim analytical derivative readiness.

## Entry Conditions Inherited From Previous Phase

P83-4 may begin only after P83-3 passes local checks and read-only review.

Inherited boundaries:

- `FixedTTSIRTTransport` metadata says the current numerical CDF-grid route is
  not production KR closure;
- P83 readiness requires positive defensive mass and `eval_pdf` proposal
  correction;
- P83-3 did not validate d=18, LEDH agreement, HMC readiness, posterior
  correctness, or production source-route correctness;
- FD/JVP/ForwardAccumulator remain diagnostic-only until Phase 4 finds or wires
  a source-backed same-branch analytical route;
- unrelated dirty worktree changes must be preserved.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-result-2026-06-22.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`
- Draft/refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase5-mechanics-smoke-subplan-2026-06-22.md`
- If Phase 4 blocks, blocker handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md`

## Required Checks / Tests / Reviews

Skeptical audit before any code edits.

Read-only inventory checks:

```bash
rg -n "ForwardAccumulator|GradientTape|finite difference|finite_difference|JVP|jvp|derivative|score|custom_gradient|analytical|fixed branch|branch" \
  bayesfilter/highdim \
  tests/highdim \
  docs/plans/bayesfilter-highdim-zhao-cui-p8*.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p7*.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p6*.md -S

rg -n "eval_.*jac|jac|grad|deriv|cdf|irt|rt|cirt|potential|marginal" \
  third_party/audit/zhao_cui_tensor_ssm_p10/source -S
```

If no code edits are made:

```bash
git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase5-mechanics-smoke-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md
```

If code or tests are changed, add focused compile/test checks for touched files
before writing the Phase 4 result.

Review:

- Claude Opus max-effort read-only review of a compact derivative-audit fact
  packet and Phase 5 handoff if Phase 4 is material.
- Repair loop up to five rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there a source-backed same-branch analytical derivative route for the fixed-TTSIRT source-route mechanics, or must derivative readiness remain blocked? |
| Baseline/comparator | P83-3 metadata/tests, P81/P82 derivative-route corrections, P50/P56/P57 source-route anchors, local derivative code, and Zhao-Cui author derivative/Jacobian source anchors. |
| Primary pass criterion | Phase 4 produces an anchored classification table for every candidate derivative route and either identifies a source-backed analytical route with local wiring evidence or records a blocker/design gap. |
| Veto diagnostics | FD/JVP/ForwardAccumulator promoted as analytical source route; derivative path changes the route rather than freezing it; branch randomness or rank/basis adaptation not frozen; missing paper/source anchors; d=18/LEDH/HMC readiness claims. |
| Explanatory diagnostics | `rg` inventories, code/source anchor table, focused tests if code changes, Claude review notes. |
| Not concluded | No derivative correctness unless anchored and tested; no d=18 validation; no posterior correctness; no production KR closure; no HMC readiness. |
| Artifact preserving result | Phase 4 result and, if needed, blocker handoff. |

## Forbidden Claims / Actions

- Do not run GPU, LEDH, d=18, fitting ladders, MCMC, HMC, or validation jobs.
- Do not claim that FD, replay residuals, JVP, or ForwardAccumulator establish
  analytical derivative correctness.
- Do not change default numerical policy.
- Do not implement broad KR replacement.
- Do not make PyTorch/JAX/NumPy a BayesFilter-owned gradient backend.
- Do not claim production source-faithfulness without paper and author-source
  file/line anchors.

## Exact Next-Phase Handoff Conditions

P83-5 may begin only if:

- Phase 4 result either identifies a source-backed same-branch analytical route
  or explicitly scopes Phase 5 as mechanics-only without derivative-readiness
  claims;
- all Phase 4 local checks pass;
- Claude review agrees or non-material comments are resolved;
- Phase 5 subplan exists and states whether derivative readiness is available,
  blocked, or out of scope;
- Phase 5 remains a tiny mechanics smoke and does not become d=18, LEDH, GPU,
  HMC, or production-validation work.

## Stop Conditions

Stop with a Phase 4 blocker result if:

- no source-backed same-branch analytical derivative route can be found;
- only FD/JVP/ForwardAccumulator evidence is available;
- local code changes would require broad transport/KR refactors;
- source anchors cannot be inspected or cited;
- a derivative route would alter the author route rather than freeze it;
- Claude and Codex do not converge after five rounds for the same blocker.
