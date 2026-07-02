# SR-UKF Actual-SV Analytical Score Master Program

Date: 2026-07-01

Status: DRAFT_MASTER_PROGRAM

Supervisor/executor: Codex in the current conversation.

Reviewer: Claude Opus max effort, read-only and bounded. Claude is not an
execution authority and cannot authorize human, runtime, model-file, funding,
product-capability, default-policy, or scientific-claim boundaries.

## Objective

Build a production-admissible square-root UKF analytical score route for the
actual-SV leaderboard by separating two products:

1. a generic factor-propagating square-root UKF value/score backend that does
   not rely on strict-SPD principal-square-root derivatives; and
2. an augmented-noise actual-SV adapter that applies that backend to the correct
   pre-transition uncertainty law.

The program must first derive and document the algorithm in LaTeX, then audit
the derivation with MathDevMCP and bounded Claude review, then implement and
test the algorithm. Leaderboard admission is allowed only after the derivation,
implementation, and test gates pass.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter provide an analytical factor-propagating SR-UKF score for the actual-SV augmented-noise UKF diagnostic likelihood without the old autodiff, historical SVD, or strict-SPD principal-root derivative drift? |
| Baseline/comparator | Current actual-SV UKF value-only diagnostic route in `bayesfilter/highdim/sv_mixture_cut4.py`; current strict-SPD principal-square-root UKF score route for KSC source-scope diagnostics; Kalman affine parity fixtures for generic validation. |
| Primary pass criterion | A LaTeX-derived, MathDevMCP-audited, Claude-reviewed generic SR-UKF backend and actual-SV adapter are implemented in TensorFlow/TFP, pass focused analytical-score tests, and emit leaderboard rows only with analytical SR-UKF provenance. |
| Veto diagnostics | Any admitted score path uses `GradientTape`, historical SVD/eigenderivative score provenance, strict-SPD principal-root derivative as the claimed SR-UKF score, wrong actual-SV sigma-point law, missing stop conditions, failed MathDevMCP material obligation, failed Claude material review, failed factor reconstruction, failed same-scalar FD consistency, or failed score-at-true-parameter consistency. |
| Explanatory diagnostics | Runtime, CPU/GPU timing, UKF approximation error versus denser quadrature, FD sensitivity, and branch telemetry explain behavior but do not by themselves prove correctness or HMC readiness. |
| Not concluded | Passing this program does not prove exact actual-SV likelihood correctness, HMC convergence, statistical optimality, posterior validity, or superiority over SGQF/Zhao-Cui/particle methods. |
| Artifacts | This master program, phase subplans, visible runbook, execution ledger, Claude review ledger, stop handoff, patched LaTeX, MathDevMCP audit outputs, implementation diffs, tests, result notes, and regenerated leaderboard artifacts if admitted. |

## Skeptical Plan Audit

| Risk | Guard |
| --- | --- |
| Wrong baseline | Separate current diagnostic value route, KSC strict-SPD route, and new factor-propagating SR-UKF route. |
| Proxy metric promoted to pass | FD consistency is necessary only; score-at-true-parameter and factor reconstruction are separate gates. |
| Missing stop conditions | Every phase subplan has stop conditions and exact handoff conditions. |
| Unfair comparison | The actual-SV UKF score is compared to its own scalar SR-UKF objective for FD, not to an exact likelihood oracle. |
| Hidden assumption | The actual-SV adapter must state the augmented variable and parameterization before implementation. |
| Stale context | Phase 0 inventories current code/doc drift before derivation work. |
| Environment mismatch | GPU/XLA commands are not part of derivation phases; any later GPU command requires escalated trusted execution and a runtime subplan. |
| Artifact mismatch | Each phase must write a close/result record before handoff. |

The audit passes for Phase 0 launch because Phase 0 only inventories and
freezes boundaries; it does not implement, run long experiments, or make
scientific claims.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Drift Inventory | `docs/plans/bayesfilter-srukf-actual-sv-score-phase0-governance-inventory-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase0-governance-inventory-result-2026-07-01.md` |
| 1 | Generic SR-UKF Derivation | `docs/plans/bayesfilter-srukf-actual-sv-score-phase1-generic-derivation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase1-generic-derivation-result-2026-07-01.md` |
| 2 | Generic Derivation Audit | `docs/plans/bayesfilter-srukf-actual-sv-score-phase2-generic-audit-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase2-generic-audit-result-2026-07-01.md` |
| 3 | Augmented-Noise Adapter Derivation | `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-augmented-adapter-derivation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-augmented-adapter-derivation-result-2026-07-01.md` |
| 4 | Adapter Derivation Audit | `docs/plans/bayesfilter-srukf-actual-sv-score-phase4-adapter-audit-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase4-adapter-audit-result-2026-07-01.md` |
| 5 | Generic Backend Implementation | `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-result-2026-07-01.md` |
| 6 | Actual-SV Adapter Implementation | `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-result-2026-07-01.md` |
| 7 | Thorough Test Ladder | `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-result-2026-07-01.md` |
| 8 | Leaderboard Admission And Release Note | `docs/plans/bayesfilter-srukf-actual-sv-score-phase8-leaderboard-release-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase8-leaderboard-release-result-2026-07-01.md` |

## Repair Loop

For each material phase:

1. run a skeptical plan audit before execution;
2. execute the smallest visible action that answers the phase question;
3. run required local checks;
4. write the phase result or blocker close record;
5. draft or refresh the next phase subplan;
6. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
7. use Claude read-only review for material plans/results;
8. if Claude finds a fixable material issue, patch the same artifact visibly and
   rerun focused checks;
9. stop after five Claude review rounds for the same blocker;
10. stop after five focused MathDevMCP repair attempts for the same material
    formal-audit blocker.

## Claude Protocol

Use the bounded prompt shape from `AGENTS.md`:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a tiny read-only probe through the same worker.
If the probe responds, redesign the material prompt to be narrower. If the
probe does not respond in trusted execution, write a blocker result.

## Anticipated Approval Needs

The owner has requested launch. The following boundaries are anticipated:

- Claude Code usage for bounded read-only review through
  `bash scripts/claude_worker.sh` with escalated trusted permissions.
- CPU-only local checks for documentation and unit tests. These do not require
  GPU approval and must set `CUDA_VISIBLE_DEVICES=-1` when importing
  TensorFlow deliberately on CPU.
- Later GPU/XLA/HMC or long benchmark commands are not authorized by this
  launch unless their phase subplan states exact commands and trusted execution
  requirements. They require escalated trusted execution under the local GPU
  policy.
- No package installation, network data fetch, destructive filesystem action,
  model-file mutation, or default-policy change is authorized by this program
  without a human-required stop.

## Human-Required Stop Conditions

Stop if continuing would require changing the scientific target, changing
leaderboard admission criteria after seeing results, package installation,
network fetch, credentials, destructive git/filesystem action, model-file
mutation, detached agent launch, GPU/HMC runtime outside a reviewed subplan, or
continuing after five failed Claude convergence rounds.
