# P91 Phase 0 Result: Production Contract Reframe

Date: 2026-06-29

Status: `P91_PHASE0_PRODUCTION_CONTRACT_LOCAL_READY_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 0 locally freezes the revised P91 production contract as a document-only artifact. The contract records score identity as primary scientific gate, FD as necessary engineering consistency but not oracle, GPU/XLA as HMC capability requirement, CPU/GPU speed as model-specific, and batched APIs as required. |
| Primary criterion status | Met locally: required owner decisions, non-claims, runtime boundaries, required gates, and next-phase handoff are explicit. |
| Veto diagnostic status | Passed locally: no production-ready claim, no exact-likelihood claim, no FD-oracle claim, no universal-GPU-speed claim, no root-solving/Hessian requirement, no default-policy change, and no runtime/GPU/HMC/FD/package command. |
| Main uncertainty | Implementation and validation gates remain ahead: score contract details, batched API, FD, score identity, GPU/XLA, benchmarks, HMC smoke, packaging, and final decision. |
| Next justified action | Review the production contract, this Phase 0 result, and refreshed Phase 1 score-contract subplan with Claude. |
| What is not being concluded | No score correctness, FD pass, score-identity pass, GPU/XLA readiness, HMC readiness, benchmark pass, packaging readiness, production readiness, exact likelihood correctness, posterior correctness, universal GPU superiority, release readiness, or default-policy change. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Is the P91 production contract safely reframed from P90 without treating score identity as exact likelihood proof, FD as oracle, or GPU as universally fastest? |
| Baseline/comparator | P90 final blocked decision and user P91 owner amendments. |
| Primary criterion | Passed locally: production contract states required gates, non-claims, owner decisions, runtime boundaries, and next-phase handoff. |
| Veto diagnostics | Passed locally: no exact-likelihood claim, FD oracle claim, root-solving requirement, Hessian requirement, universal GPU-speed claim, missing batched route requirement, or default-policy change. |
| Explanatory diagnostics | Local grep coverage and artifact hygiene. |
| Not concluded | No score correctness, FD pass, GPU/XLA readiness, HMC readiness, benchmark result, production readiness, or default-policy change. |
| Artifact | Production contract, this Phase 0 result, refreshed Phase 1 subplan. |

## Local Checks

Commands:

```bash
test -f docs/plans/bayesfilter-highdim-zhao-cui-p90-phase10-final-decision-result-2026-06-28.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p90-production-repair-reset-memo-2026-06-28.md
rg -n "score identity|FD|GPU/XLA|batched|HMC|default|production|oracle|likelihood" docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

Outcome:

- P90 final decision anchor exists.
- P90 reset memo anchor exists.
- P91 keyword coverage returned the expected production-contract, Phase 0
  result, and Phase 1 subplan references.
- P91 docs diff hygiene passed before result writing.

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: P90 final decision and reset memo are exact Phase 0 anchors. |
| Proxy metric promoted | Avoided: score identity, FD, GPU/XLA, benchmarks, and HMC smoke are separate gates with explicit non-claims. |
| Missing stop condition | Avoided: Phase 0 subplan stops on missing anchors, overclaim, failed local checks, non-convergent review, or runtime/default boundaries. |
| Unfair comparison | Avoided: CPU/GPU speed is model-specific and deferred to Phase 6. |
| Hidden assumption | Avoided: root solving and Hessian/information checks are optional/advisory. |
| Stale context | Avoided: P90 closeout and 2026-06-29 owner amendments are the current baseline. |
| Environment mismatch | Avoided: no runtime/GPU command was authorized or run. |
| Artifact mismatch | Avoided locally: production contract, result, and Phase 1 subplan are exact artifacts and require review. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Execution target | Document-only production-contract reframe. |
| CPU/GPU status | No TensorFlow numerical command and no GPU/CUDA command were run in Phase 0. |
| Runtime status | No FD, score-identity runtime, HMC, GPU/XLA, package/network, release, CI, production benchmark, or default-policy command was run. |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-subplan-2026-06-29.md` |
| Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p91-production-contract-2026-06-29.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-result-2026-06-29.md` |
| Refreshed Phase 1 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-subplan-2026-06-29.md` |

## Phase 1 Handoff

Phase 1 may start only after Claude review agrees on:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-production-contract-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-subplan-2026-06-29.md`

Phase 1 must freeze the score contract and must not run FD, score-identity,
GPU/XLA, HMC, benchmark, package/release/CI, production, or default-policy
commands.
