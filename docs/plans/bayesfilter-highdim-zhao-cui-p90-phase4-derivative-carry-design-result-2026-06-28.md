# P90 Phase 4 Result: Source-Route Derivative-Carry Design

Date: 2026-06-28

Status: `P90_PHASE4_DERIVATIVE_CARRY_DESIGN_LOCAL_READY_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 4 locally designed derivative-carry ownership for the same scalar and branch that passed the Phase 3 value bridge. |
| Primary criterion status | Met locally pending review: every scalar component has a derivative owner/classification, carry fields, branch binding, and Phase 5 test plan. |
| Veto diagnostic status | Passed locally: no derivative implementation, no FD/HMC/GPU/production/default-policy command, no fixed-branch/JVP/autodiff promotion, and no weakening of the Phase 3 value-bridge boundary. |
| Main uncertainty | Fixed TTSIRT proposal/transport derivative surfaces remain design/blocker rows until Phase 5 either implements a source-backed derivative surface or explicitly blocks readiness. |
| Next justified action | Claude review of derivative manifest, this result, and refreshed Phase 5 subplan. If all agree, Phase 5 may implement only the reviewed deterministic derivative-carry surface. |
| What is not being concluded | No source-route analytical-gradient readiness, FD validation, HMC readiness, GPU/XLA readiness, production readiness, packaging readiness, or default-policy change. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What derivative objects and source-backed operations are required to differentiate the exact same scalar that passed Phase 3? |
| Baseline/comparator | Phase 3 passed value bridge, P89 derivative inventory, local source-route code, and author TTSIRT derivative anchors. |
| Primary criterion | Passed locally pending review: the manifest names derivative owners/classification, carry fields, branch identity binding, and Phase 5 test plan for each scalar component. |
| Veto diagnostics | Passed locally: previous-marginal, proposal-correction, normalizer, branch identity, and transport derivative ownership are explicit and not promoted beyond design. |
| Explanatory diagnostics | Required source-anchor inventory and component ownership table. |
| Not concluded | No derivative implementation or gradient correctness. |
| Artifact | Derivative manifest, this Phase 4 result, and refreshed Phase 5 subplan. |

## Local Checks

Commands:

```bash
rg -n "source_route_previous_marginal_log_density|source_route_generate_retained_samples|source_route_sequential_negative_log_physical_density|eval_irt_reference|eval_rt_jac_reference|marginalise|AbstractIRT|normalizer|branch" docs/plans/bayesfilter-highdim-zhao-cui-p89*.md docs/plans/bayesfilter-highdim-zhao-cui-p90*.md bayesfilter/highdim/source_route.py third_party/audit/zhao_cui_tensor_ssm_p10/source -g '*.md' -g '*.py' -g '*.m'
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Outcomes:

- Source-route scalar, previous marginal, retained sampling, proposal
  correction, normalizer, branch identity, and author TTSIRT derivative anchors
  were found.
- P90 docs diff hygiene passed before result writing.

## Manifest Summary

Manifest:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p90-derivative-carry-manifest-2026-06-28.md
```

Core design decisions:

- Bind derivative work to the Phase 3 value-bridge binding hash and branch
  hashes.
- Treat transition, likelihood, and prior parameter scores as local
  parameterized SIR derivative components over the source formula.
- Treat previous retained marginal derivative as source-backed marginal
  semantics plus local fixed-HMC adaptation until fixed TTSIRT derivative
  surfaces are implemented.
- Treat proposal correction, normalizer, and transport inverse/eval/Jacobian
  as explicit carry owners; do not promote them to readiness without
  implementation evidence.
- Require Phase 5 drift-veto tests before derivative comparison.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Execution target | Design/document/source-anchor inventory only. |
| CPU/GPU status | No TensorFlow numerical command and no GPU/CUDA command were run in Phase 4. |
| Runtime/HMC status | No FD, derivative implementation, HMC, sampler, GPU/XLA, package/network, production benchmark, release, CI, or default-policy command was run. |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-subplan-2026-06-28.md` |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p90-derivative-carry-manifest-2026-06-28.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-result-2026-06-28.md` |

## Phase 5 Handoff

Phase 5 may start only after Claude `VERDICT: AGREE` for:

- derivative manifest;
- this Phase 4 result;
- `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-subplan-2026-06-28.md`.

Phase 5 must implement only the reviewed deterministic derivative-carry surface
and must not run FD validation, HMC, GPU/CUDA, production, packaging, CI,
release, or default-policy commands.
