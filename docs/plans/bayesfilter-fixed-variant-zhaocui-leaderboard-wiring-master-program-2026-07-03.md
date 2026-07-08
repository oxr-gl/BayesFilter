# Fixed-Variant Zhao-Cui Leaderboard Wiring Master Program

Date: 2026-07-03

Status: `CLAUDE_REVIEW_AGREE_PHASE0_LAUNCHED`

## Objective

Wire the Zhao-Cui SIR leaderboard row to the fixed-variant Zhao-Cui source-route
evidence path, demote the generic all-axes retained-grid route to
diagnostic/historical evidence, regenerate the affected leaderboard artifacts,
and preserve explicit scope boundaries.

Codex is supervisor and executor. Claude is read-only reviewer only and cannot
authorize crossing human, runtime, model-file, funding, product-capability, or
scientific-claim boundaries.

## Owner Directives

- The generic multistate retained-grid route is diagnostic/historical only.
- The production-admissible Zhao-Cui direction is the fixed-variant source
  route.
- Analytical/manual gradients are required for leaderboard gradient rows.
- Autodiff and finite differences are diagnostics only.
- The existing P91 fixed-variant SIR evidence is local complete-data/component
  evidence unless this program explicitly closes the full observed-data
  filtering derivative gap.

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | Launch Boundary Freeze | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase0-launch-boundary-freeze-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase0-launch-boundary-freeze-result-2026-07-03.md` |
| 1 | Fixed-Variant Entry Point Inventory | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase1-entrypoint-inventory-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase1-entrypoint-inventory-result-2026-07-03.md` |
| 2 | Row Scope And Evidence Contract | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase2-row-scope-contract-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase2-row-scope-contract-result-2026-07-03.md` |
| 3 | Runner Wiring And Guards | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase3-runner-wiring-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase3-runner-wiring-result-2026-07-03.md` |
| 4 | Regeneration And Validation | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase4-regeneration-validation-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase4-regeneration-validation-result-2026-07-03.md` |
| 5 | Closeout And Handoff | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase5-closeout-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase5-closeout-result-2026-07-03.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the highdim leaderboard report the Zhao-Cui SIR fixed-variant route without using or repairing the demoted retained-grid route and without overclaiming full observed-data filtering readiness? |
| Baseline/comparator | Current July highdim leaderboard artifacts, P91 fixed-variant SIR artifacts, and the owner directive demoting retained-grid production use. |
| Primary pass criterion | The affected Zhao-Cui SIR row is regenerated with fixed-variant route metadata, analytical/manual score provenance if a score is emitted, retained-grid exclusion metadata, and explicit scope/nonclaim fields. |
| Veto diagnostics | Retained-grid route selected for production; autodiff/FD score admitted; full observed-data filtering score identity claimed without closing preserved blockers; stale fixed/no-free-theta row treated as the parameterized score row; nonfinite value/score; missing result artifacts; Claude review `VERDICT: REVISE` not resolved within five rounds. |
| Explanatory diagnostics | Runtime, sidecar P91 GPU/XLA timing, P91 score-at-true tables, row summary readiness, and leaderboard markdown formatting. |
| Not concluded | No exact likelihood proof, no posterior correctness, no convergence claim, no universal GPU speed superiority, no production default change beyond route admission metadata, and no source-faithful claim without paper/source anchors. |
| Artifacts | Master program, phase subplans/results, visible runbook, execution ledger, review ledger, regenerated leaderboard JSON/MD, and stop handoff. |

## Skeptical Plan Audit

| Risk | Audit Result |
| --- | --- |
| Wrong baseline | The baseline is the current highdim leaderboard plus P91 fixed-variant artifacts, not the historical retained-grid route. |
| Proxy promoted to pass | P91 local complete-data evidence may support only the declared local/component scope unless a phase closes full filtering derivative blockers. |
| Missing stop condition | Each phase has explicit stop conditions and a five-round Claude review cap for material blockers. |
| Unfair comparison | Rows must state whether they are main leaderboard rows or scoped sidecar evidence before ranking/timing fields are interpreted. |
| Hidden assumption | The plan treats fixed-variant wiring as target-scope work first; it does not assume a full observed-data value/score is already available. |
| Stale context | Phase 0 must reread current runner, leaderboard JSON/MD, route demotion constants, and P91 artifacts before edits. |
| Environment mismatch | CPU-only runner checks hide GPU. GPU/XLA evidence can only be cited from trusted P91 artifacts unless a later phase explicitly runs trusted GPU commands. |
| Artifact mismatch | Every phase result must name the commands run and the artifacts that answer that phase question. |

Audit status: `PASS_MASTER_PROGRAM_SKEPTICAL_AUDIT_CLAUDE_AGREE`.

## Claude Review Loop

Claude review must use bounded prompts. First review attempts must point to one
path only. If Claude does not respond, Codex must run a small probe:

```text
Return exactly CLAUDE_PROBE_OK.
```

If the probe responds, the failed review prompt is treated as too broad or
malformed and must be redesigned. Claude review stops after five rounds for the
same blocker.

## Stop Conditions

- Human direction is needed to redefine the leaderboard scientific target.
- New GPU execution is required but trusted GPU escalation is unavailable.
- The fixed-variant route cannot emit the claimed quantity under the declared
  scope.
- Claude and Codex do not converge after five review rounds for the same
  material issue.
- Continuing would require package installation, network fetch, credentials,
  destructive git operations, or reverting unrelated user changes.
