# P91 Phase 7 Subplan: HMC Readiness Smoke

Date: 2026-06-29

Status: `REFRESHED_PENDING_PHASE6_RESULT_REVIEW`

## Phase Objective

Run a short HMC-facing smoke test to verify the compiled Zhao-Cui target is
usable by an HMC/NUTS-style caller: finite values/gradients, no immediate
implementation-level divergence pathology, and acceptable runtime/memory. This
is not posterior correctness or scientific posterior validation.

## Entry Conditions Inherited From Previous Phase

- Phase 6 performance benchmark reviewed pass.
- Phase 5 GPU/XLA JIT capability reviewed pass.
- Phase 3 limited-FD diagnostic owner-accepted for continuation with caveats;
  not a full FD pass.
- Phase 4 local complete-data component-score identity reviewed pass.
- This Phase 7 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Exact-command Phase 7 runtime refresh:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-exact-command-refresh-2026-06-29.md`
- HMC smoke manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-2026-06-29.json`
- Phase 7 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md`
- Refreshed Phase 8 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

This refreshed Phase 7 subplan is a planning handoff only. HMC/GPU commands
require a further exact-command refresh and trusted execution before runtime.
Claude review is required for the exact-command refresh, Phase 7 result, and
Phase 8 subplan.

Allowed pre-refresh check:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

The exact-command refresh must state the runtime command, target scope,
sampler/kernel settings, trusted GPU/XLA status, stop conditions, manifest
schema, and forbidden claims before HMC runtime. The manifest/result must
preserve at minimum: git commit, dirty-worktree note, exact command actually
run, Python executable, conda environment, trusted-vs-untrusted GPU status,
TensorFlow/TFP versions, device visibility, XLA status, random seeds, chain
count, step count, warmup/burn-in count if any, target value/gradient finiteness,
divergence/pathology counts, runtime/wall time, artifact paths, decision/veto
status, Phase 3 limited-FD caveat, and nonclaims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the HMC-relevant local complete-data Zhao-Cui target component survive a short implementation smoke test under reviewed exact commands? |
| Baseline/comparator | Phase 5 compiled local complete-data value/autodiff-score path and Phase 6 model-specific execution evidence. |
| Primary criterion | Short HMC/NUTS smoke runs with finite values/gradients and no immediate implementation-level pathology under reviewed settings. |
| Veto diagnostics | Posterior correctness claim, ESS/speed ranking despite divergences, NaN/Inf, target compile failure, untrusted GPU evidence, HMC used to override Phase 3 caveats/full-source-route blockers, or HMC smoke treated as production readiness. |
| Explanatory diagnostics | Divergence count, finite gradient check, short-chain traces, runtime/memory. |
| Not concluded | No posterior correctness, convergence, statistical superiority, exact likelihood correctness, or production readiness by itself. |
| Artifact | HMC smoke manifest, Phase 7 result, refreshed Phase 8 subplan. |

## Forbidden Claims/Actions

- Do not claim posterior correctness or convergence from smoke.
- Do not rank samplers if veto diagnostics fail.
- Do not treat Phase 3 as a full FD pass.
- Do not claim full observed-data/filtering HMC target readiness unless an
  exact-command refresh explicitly implements and tests that scope.
- Do not run package/release/CI/default commands.
- Do not change defaults.

## Exact Next-Phase Handoff Conditions

Phase 8 may start only if:

- Phase 7 result receives Claude `VERDICT: AGREE`;
- Phase 8 subplan receives Claude `VERDICT: AGREE`;
- HMC smoke passes or Phase 8 is blocker-only.

## Stop Conditions

- HMC target fails finite value/gradient smoke.
- Divergence/pathology requires implementation repair.
- Local checks fail and cannot be repaired.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required HMC smoke commands authorized by reviewed Phase 7 refresh.
2. Write Phase 7 result / close record.
3. Draft or refresh Phase 8 subplan.
4. Review Phase 7 result and Phase 8 subplan.
