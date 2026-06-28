# Actual-SIR Nystrom Threshold Calibration Master Program

Date: 2026-06-24

Status: `P07_CLOSEOUT_READY_FOR_NEXT_MODEL_SUITE_OR_DEFAULT_GAP_PLAN`

## Objective

Replace the inherited actual-SIR Nystrom paired log-likelihood threshold with a
principled, reviewed threshold-calibration workflow.  The master program must
separate deterministic validity vetoes from stochastic paired-comparator
diagnostics, choose any practical threshold before validation outcomes are
interpreted, and avoid rejection or promotion unless the result is statistically
meaningful for the declared scope.

Codex is supervisor and executor.  Claude Opus/max-effort may be used only as a
read-only reviewer.  Claude cannot edit files, run commands, authorize default
promotion, choose product scope, approve scientific claims, or cross human,
runtime, model-file, funding, or product-capability boundaries.

## Governing Inputs

- Statistical testing amendment:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-statistical-testing-amendment-2026-06-24.md`
- Threshold calibration plan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-plan-2026-06-24.md`
- Existing compiled-redo benchmark harness:
  `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
- Visible gated runbook template:
  `/home/ubuntu/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | What paired log-likelihood threshold is principled for the actual-SIR Nystrom fixed-policy value route, and can validation evidence support it statistically? |
| Candidate under test | Compiled TF32 actual-SIR Nystrom route, initially fixed policy `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`. |
| Comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Intended scope for this program | Bounded value-route diagnostic/default-candidate evidence only.  HMC/posterior readiness is out of scope. |
| Deterministic vetoes | Nonfinite outputs, malformed artifacts, wrong route/policy metadata, residual invariant failure, comparator failure, trusted GPU/TF32 mismatch, invalid harness, or missing required artifacts. |
| Stochastic evidence | Normalized paired log-likelihood error per observed component, seed-panel uncertainty, exceedance probability, and confidence bounds relative to a frozen `tau_component`. |
| Promotion criterion | No default promotion in this program.  A later default packet may use this program only if deterministic validity passes and statistical validation supports the frozen threshold. |
| Rejection criterion | Reject only if deterministic validity fails, or a predeclared statistical test rejects the acceptable-error model after threshold freeze. |
| Continuation veto | Claude/Codex review nonconvergence after five rounds for the same material blocker, inability to justify/freeze `tau_component`, invalid artifacts, trusted GPU unavailable for GPU phases, or human approval required. |
| What must not be concluded | No posterior correctness, no HMC readiness, no statistical superiority, no default readiness, no broad Nystrom rejection, and no threshold claim derived from legacy `5.0` alone. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the actual-SIR Nystrom paired-delta threshold be calibrated and then tested under a statistically meaningful rule? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route; existing artifacts for artifact-only phases; new trusted GPU artifacts only after threshold freeze. |
| Primary pass criterion | Each phase writes required artifacts, passes local checks, converges under read-only review when material, and either advances to the exact next phase or writes a blocker. |
| Veto diagnostics | Wrong baseline, proxy threshold promoted to criterion, missing stop condition, unfair comparison, hidden assumptions, stale context, environment mismatch, unsupported claim, artifact mismatch, or post-hoc threshold change. |
| Explanatory diagnostics | Runtime, ESS, residual magnitudes below deterministic thresholds, factor/scaling diagnostics, descriptive seed-panel SD. |
| Not concluded | Default readiness, posterior correctness, HMC readiness, statistical superiority, or threshold validity beyond the declared scope. |
| Artifacts | Master program, phase subplans/results, visible runbook, ledger, stop handoff, Claude review ledger, logs, JSON/Markdown benchmark outputs if GPU phases run. |

## Skeptical Plan Audit

| Risk | Audit Result |
| --- | --- |
| Wrong baseline | The operational comparator is the compiled streaming TF32 actual-SIR route.  It is not a truth oracle. |
| Proxy metric as promotion criterion | Legacy `5.0`, runtime, ESS, and descriptive deltas cannot promote or reject without a frozen threshold and uncertainty rule. |
| Missing stop conditions | Every phase below requires explicit stop conditions and a close record. |
| Unfair comparison | New GPU validation must use the same model, observations, seed policy, dtype, TF32 mode, transport policy, fixed Nystrom policy, and trusted GPU provenance. |
| Hidden assumption | The threshold must be tied to intended use.  This program covers value-route evidence only, not HMC/posterior use. |
| Stale context | Earlier zero-failure G5 interpretation is superseded by the statistical amendment. |
| Environment mismatch | GPU phases require trusted `nvidia-smi`; use physical GPU1 if available and suitable, otherwise GPU0. |
| Artifact mismatch | A phase cannot pass unless artifacts parse and support the phase evidence contract. |

Audit status: `PASS_FOR_P0_REVIEW`.  Execution may start only through the phase
subplans and visible runbook.

## Phase Index

| Phase | Name | Status | Subplan | Required result |
| --- | --- | --- | --- | --- |
| P0 | Governance/runbook lock | `PASSED` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p00-governance-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p00-governance-result-2026-06-24.md` |
| P1 | Existing-artifact scale extraction | `PASSED_LOCAL` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p01-artifact-scale-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p01-artifact-scale-result-2026-06-24.md` |
| P2 | Threshold principle and freeze | `PASSED` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p02-threshold-freeze-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p02-threshold-freeze-result-2026-06-24.md` |
| P3 | Frozen-threshold statistical validation and extension | `P3_INCONCLUSIVE_STOP_THRESHOLD_UNSUPPORTED_BY_PANEL` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-subplan-2026-06-24.md`; `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-extension-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-result-2026-06-24.md` |
| P4 | Threshold-support failure repair selection | `P04_HANDOFF_POLICY_TUNING` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p04-repair-selection-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p04-repair-selection-result-2026-06-24.md` |
| P5 | SVD core-solver focused tuning | `P05_NOMINATE_SVD_TO_P06` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-result-2026-06-24.md` |
| P6 | SVD fresh validation | `P06_PASS_TO_P07_EVIDENCE_PACKAGE` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-result-2026-06-24.md` |
| P7 | Evidence package closeout | `P07_CLOSEOUT_READY_FOR_NEXT_MODEL_SUITE_OR_DEFAULT_GAP_PLAN` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-result-2026-06-24.md` |

## Phase Requirements

Every phase subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each phase:

1. run required local checks;
2. write a phase result or close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude Opus/max-effort as read-only reviewer for material subplans or
   boundary decisions, with at most five repair-review rounds for the same
   blocker.

## Repair Loop

If local or Claude review finds a fixable issue:

1. patch the same subplan visibly;
2. rerun focused local checks;
3. rerun Claude review only for material issues;
4. record each round in the review ledger;
5. continue after `VERDICT: AGREE`;
6. stop after five rounds for the same blocker and write a blocker result.

Blocker identity rule: a blocker is the same blocker when it concerns the same
phase, artifact set, evidence-contract field, or boundary condition, even if a
later review phrases it differently.  Renaming, splitting, or rewording a
materially unchanged issue does not reset the five-round limit.

## Calibration/Validation Split Rule

P1 may use the existing artifact seed panel only for descriptive scale
extraction and P2 threshold-freeze design.  Any P3 statistical validation seed
panel must be disjoint from the P1 calibration/extraction seeds unless a later
reviewed subplan explicitly classifies the result as resubstitution-only and
forbids validation/pass claims.  Validation seeds and artifact paths must be
declared before P3 execution.

## Anticipated Approval Needs

The visible execution may need:

- escalated/trusted Claude Code wrapper calls:
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh ...`;
- escalated/trusted GPU preflight:
  `nvidia-smi`;
- escalated/trusted GPU benchmark commands if P3 runs validation seeds;
- no package installs, network fetches, destructive git operations, model-file
  changes, or default-policy changes are authorized by this plan.

## Immediate Next Action

Launch P0 visibly:

1. run local file/section checks for this master program, P0 subplan, runbook,
   ledger, stop handoff, and P1 subplan;
2. send bounded excerpts to Claude Opus/max-effort read-only review;
3. patch if review finds material issues;
4. write P0 result;
5. continue to P1 if converged.
