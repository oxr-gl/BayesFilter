# P90 Master Program: Zhao-Cui SIR d18 Source-Route Value Bridge And Derivative Repair

Date: 2026-06-28

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Program Objective

Repair the blockers preserved by P89 for Zhao-Cui SIR d18 by building the
missing same-target source-backed value bridge first, then designing and
implementing source-route analytical derivative carry for the exact same
scalar. Later FD, HMC, GPU/XLA, packaging, and default-readiness phases may
execute only after their upstream reviewed pass artifacts exist.

P90 is a successor repair program. It is not a production promotion at launch.

## Inherited State

P89 final decision:

```text
ZHAO_CUI_SIR_D18_NOT_PRODUCTION_READY_UNDER_P89
```

Strongest retained positive label:

```text
D18_SOURCE_ROUTE_RANK_DEGREE_STABLE
```

Binding blockers inherited from P89:

```text
BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING
NO_SOURCE_ROUTE_ANALYTICAL_DERIVATIVE_IMPLEMENTATION
SOURCE_ROUTE_FULL_HISTORY_ANALYTICAL_DERIVATIVE_READINESS_BLOCKED
FD_GRADIENT_VALIDATION_BLOCKED
HMC_READINESS_BLOCKED
GPU_XLA_PRODUCTION_READINESS_BLOCKED
PRODUCTION_PACKAGING_DEFAULT_READINESS_BLOCKED
```

Key inherited artifacts:

- P89 final decision:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase10-final-production-decision-result-2026-06-28.md`
- P89 reset memo:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-production-promotion-reset-memo-2026-06-28.md`
- P89 target manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-target-manifest-2026-06-28.md`
- P89 value-bridge blocker:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase2-value-bridge-design-result-2026-06-28.md`
- P89 derivative inventory:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase4-derivative-design-result-2026-06-28.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P90 close the missing same-target value bridge and source-route analytical derivative blockers for the exact Zhao-Cui SIR d18 scalar, then evaluate downstream production gates in sequence? |
| Baseline/comparator | P89 blocked closeout, P89 target manifest, author source anchors, and local source-route code. |
| Primary pass criterion | The whole program can promote only if each phase has a reviewed pass artifact in order: value bridge contract, value bridge implementation, value bridge execution, derivative-carry design, derivative implementation, same-scalar FD, HMC readiness, GPU/XLA readiness, packaging/default readiness, and final decision. |
| Veto diagnostics | Wrong scalar, wrong branch, proxy correctness, missing source anchors, missing tolerances, ALS training revival, audit-cloud tuning, FD before same-scalar derivative, HMC before value/gradient gates, GPU/XLA before HMC, packaging/default before production gates, unreviewed runtime crossing, or source-faithful claim without paper and author-source anchors. |
| Explanatory diagnostics | Rank/degree stability, holdout residuals, validation loss, ESS, replay diagnostics, compile/device evidence, and short smoke tests explain only unless a phase contract explicitly promotes them. |
| Not concluded at launch | No value correctness, source-route correctness, analytical-gradient correctness, FD validation, HMC readiness, GPU/XLA readiness, production readiness, packaging readiness, LEDH agreement, scale readiness, or default-policy change. |
| Artifacts | P90 master, runbook, subplans, ledgers, phase results, bridge manifest, derivative manifest, runtime manifests, review ledger, stop handoff. |

## Skeptical Plan Audit

| Risk Checked | P90 Control |
| --- | --- |
| Wrong baseline | P89 is a blocked baseline; `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` is rank/degree evidence only. |
| Proxy metrics promoted | Proxy metrics are explanatory only unless the phase evidence contract names them as primary criteria. |
| Missing stop conditions | Each subplan contains stop conditions and exact handoff criteria. |
| Unfair comparison | Value/gradient comparisons must bind same target, branch, retained objects, basis/rank/samples/schedules, parameterization, and tolerances. |
| Hidden assumptions | Phase 0 re-audits P89 inheritance, author/local source anchors, runtime boundaries, and dirty-worktree scope before any repair work. |
| Stale context | P90 must cite P89 closeout and target manifest before changing any target contract. |
| Environment mismatch | Runtime, GPU/CUDA, HMC, package/network, and release commands require exact reviewed subplans and escalated/trusted execution when applicable. |
| Useless artifacts | Each phase must write a result artifact whose decision directly answers that phase question. |

Audit status: passed for launch planning. Execution may begin only after local
checks and bounded Claude review converge for this master, the runbook, and the
Phase 0 subplan.

## Source-Anchor Gate

All Zhao-Cui source-route claims must satisfy the repository source-anchor
gate. A claim may be called `source_faithful` only when it cites the Zhao-Cui
paper/math claim and author source file/line anchors. Otherwise it must be
classified as `fixed_hmc_adaptation`, `implementation/setup choice`, or
`extension_or_invention`.

Any unanchored source-faithful claim blocks with:

```text
BLOCK_SOURCE_UNGROUNDED
```

## Training Boundary

- No ALS training revival.
- Training-base optimizer only.
- L1 weight tuning is the Zhao-Cui default training procedure.
- Zero-L1 is comparator-only.
- Audit clouds are never tuning clouds.
- Validation, holdout, and audit ledgers must remain separate.

## Sequential Gate Rule

No phase may execute as promotional work unless all prior promotional gates
have reviewed pass artifacts. If an upstream gate is blocked, downstream phases
may only write no-runtime blocker closeouts or a final blocked decision.

Runtime commands, GPU/CUDA commands, HMC/sampler commands, package/network
commands, release/CI commands, production benchmarks, and default-policy
changes require the exact phase subplan to be reviewed ready first.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance bootstrap and blocker inheritance | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase0-governance-bootstrap-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase0-governance-bootstrap-result-2026-06-28.md` |
| 1 | Same-target value bridge contract | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase1-value-bridge-contract-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase1-value-bridge-contract-result-2026-06-28.md` |
| 2 | Value bridge implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase2-value-bridge-implementation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase2-value-bridge-implementation-result-2026-06-28.md` |
| 3 | Value bridge execution and correctness candidate | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-result-2026-06-28.md` |
| 4 | Source-route derivative-carry design | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-result-2026-06-28.md` |
| 5 | Source-route derivative implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-result-2026-06-28.md` |
| 6 | Same-scalar FD gradient validation | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase6-fd-gradient-validation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase6-fd-gradient-validation-result-2026-06-28.md` |
| 7 | HMC readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase7-hmc-readiness-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase7-hmc-readiness-result-2026-06-28.md` |
| 8 | GPU/XLA production readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase8-gpu-xla-production-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase8-gpu-xla-production-result-2026-06-28.md` |
| 9 | Packaging, CI, and default-readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase9-packaging-default-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase9-packaging-default-result-2026-06-28.md` |
| 10 | Final production decision | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase10-final-decision-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase10-final-decision-result-2026-06-28.md` |

## Phase Objectives And Handoff Gates

| Phase | Objective | Entry condition | Pass/handoff condition |
| --- | --- | --- | --- |
| 0 | Confirm P89 inheritance, P90 artifacts, source-anchor rules, and runtime boundaries. | P89 final closeout exists. | Reviewed governance result and Phase 1 subplan ready. |
| 1 | Build a same-target value bridge contract with source anchors, branch identity, retained-object identity, and tolerances. | Phase 0 reviewed closed. | Bridge manifest reviewed ready, or blocker `P90_BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_CONTRACT_MISSING`. |
| 2 | Implement the reviewed value bridge and fail-closed tests. | Phase 1 bridge manifest reviewed pass. | Bridge code/tests reviewed pass, or implementation blocker. |
| 3 | Execute the bridge on deterministic same-scalar cases and decide whether `D18_CORRECTNESS_CANDIDATE` may be nominated. | Phase 2 implementation reviewed pass. | Value match within pinned tolerances and no veto, or value blocker. |
| 4 | Design derivative-carry data structures for the same scalar/branch. | Phase 3 value bridge reviewed pass. | Derivative manifest reviewed ready, or derivative-design blocker. |
| 5 | Implement source-route analytical derivative for the exact same scalar. | Phase 4 derivative manifest reviewed pass. | Same-scalar analytical derivative implementation reviewed pass, or implementation blocker. |
| 6 | Validate analytical derivative against same-scalar FD with fixed branch/retained objects. | Phase 5 derivative implementation reviewed pass. | FD match within pinned tolerances and no veto, or FD blocker. |
| 7 | Evaluate HMC readiness only after value and gradient gates pass. | Phase 6 FD reviewed pass. | HMC readiness pass under reviewed diagnostics, or HMC blocker. |
| 8 | Evaluate GPU/XLA production readiness only after HMC pass. | Phase 7 HMC reviewed pass. | GPU/XLA readiness pass, or GPU/XLA blocker. |
| 9 | Evaluate packaging, CI, release, and default-readiness only after GPU/XLA pass. | Phase 8 GPU/XLA reviewed pass. | Packaging/default readiness pass, or packaging/default blocker. |
| 10 | Make final production decision from reviewed evidence only. | Phase 9 reviewed closed. | Final reviewed decision; no promotion unless all upstream gates passed. |

## Claude Review Protocol

Claude is read-only reviewer only. Claude cannot authorize human, runtime,
model-file, funding, product-capability, default-policy, or scientific-claim
boundaries. Every Claude prompt must be one-path bounded by default:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

For each material blocker, Codex may patch and rerun focused checks, then loop
Claude review up to five rounds for the same blocker. If convergence fails,
write a blocker result and stop.

## Launch Approval Needs

The launch phase needs permission to:

- create and edit P90 planning artifacts under `docs/plans`;
- run local read-only/focused checks such as `rg`, `sed`, and
  `git diff --check`;
- run bounded Claude Opus read-only review via the approved Claude worker with
  escalated/trusted permissions.

Later runtime/GPU/HMC/package/release/default-policy phases require their exact
reviewed subplan to authorize the narrower action before execution.

## Initial Stop Conditions

- P89 artifacts are missing or contradict the inherited blocker chain.
- The P90 master, runbook, or Phase 0 subplan fails local checks and cannot be
  repaired in document scope.
- Claude review does not converge after five rounds for the same blocker.
- Continuing would require runtime, GPU/CUDA, HMC, package/network, release,
  default-policy, destructive git/filesystem, or unrelated dirty-worktree
  changes before a reviewed phase subplan authorizes them.
