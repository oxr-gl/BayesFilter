# P86 Phase 5 Subplan: Budget-Compliant Fit

Date: 2026-06-24

Status: `REVIEWED_READY_FOR_PREAPPROVAL_PACKAGE_BLOCKED_BEFORE_FIT_APPROVAL`

## Phase Objective

Design, review, and either execute or block the first P86 budget-compliant
author-route fit. The route must be the P86 hard-wired author
`Lagrangep(4,8)` plus `AlgebraicMapping(1)` route, with an explicit sample
floor, exact command manifest, disjoint data clouds, and reviewed evidence
contract.

## Entry Conditions Inherited From Previous Phase

- Phase 4 passed as
  `PASS_P86_PHASE4_TINY_AUTHOR_ROUTE_FIT_SMOKE_REVIEWED`.
- Phase 4 evidence is mechanics-only. It may establish that the hard-wired
  route survives one tiny optimizer step, but it is not fit-quality,
  budget-compliance, correctness, HMC, LEDH, scale, or production evidence.
- P84 Phase 2 is precedent only. P86 Phase 5 owns the fit command, artifacts,
  interpretation, and stop conditions.
- Exact fit command, parameter-count calculation, sample count, seeds,
  training/holdout/audit clouds, runtime posture, artifact paths, and expected
  budget floor must be frozen before execution.
- Claude read-only bounded subplan review must return `VERDICT: AGREE` before
  any Phase 5 fit command is requested from the user.
- Explicit human approval of the exact command is required before any fit
  command.

## Required Artifacts

- Skeptical pre-execution audit recorded in this subplan or the Phase 5 result.
- Exact fit-command candidate manifest. It must include the command, expected
  output path, environment, CPU/GPU posture, random seeds, cloud labels, sample
  counts, rank/degree/basis/domain route, parameter-count calculation, budget
  floor, runtime cap, memory cap, `memory_diagnostic_source`,
  `planned_memory_envelope_status`, and nonclaims.
- Exact approved fit command manifest, if execution is approved. Before any
  approval request, the candidate manifest must pin the fit JSON path exactly;
  the reserved Phase 5 path is:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json`.
- Fit JSON manifest at the exact approved path. It must include the post-fit
  status table fields, including `runtime_status` and `memory_status`.
- Mandatory preflight JSON that validates route identity, sample/cloud
  separation, budget arithmetic, exact output paths, and command-fidelity
  fields without fitting. The reserved preflight path is:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-preflight-2026-06-24.json`.
- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-result-2026-06-24.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`
- Refreshed Phase 6 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-subplan-2026-06-24.md`

## Required Checks / Tests / Reviews

- Run a skeptical plan audit before drafting or approving any runtime command.
  The audit must check wrong baselines, proxy metrics as promotion criteria,
  missing stop conditions, unfair comparisons, hidden assumptions, stale P84
  ownership, environment mismatch, and whether the planned artifacts would
  answer the Phase 5 question.
- Confirm the budget floor:
  `minimum_training_samples = max(20 * P_theta, 5000)`.
- Compute and record `P_theta` for the exact P86 author route and fit rank.
- Confirm training, validation/holdout, replay if used, and audit clouds are
  disjoint before execution and in the result artifact.
- Confirm the route manifest is author `Lagrangep(4,8)` plus
  `AlgebraicMapping(1)`, not the legacy Legendre diagnostic route, not a
  local all-grid/operator route, and not a route-altering extension.
- Record CPU/GPU posture, seed, runtime, memory cap and observed memory
  diagnostic, environment, git status, and artifact paths.
- If CPU-only/GPU-hidden is chosen, use `CUDA_VISIBLE_DEVICES=-1` before
  framework import and record that it is a deliberate non-production runtime
  posture. If GPU is chosen, request escalated/trusted execution before running
  any GPU/CUDA probe or fit command.
- Run focused local checks for the command/preflight logic before requesting
  fit approval.
- Claude read-only bounded review of this subplan is mandatory before
  requesting exact human approval for the runtime command.
- Claude read-only bounded review of the Phase 5 result is mandatory after
  execution or blocker closeout.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the P86 author algebraic `Lagrangep` route produce a budget-compliant fixed-TTSIRT fit artifact without crossing correctness, HMC, LEDH, scale, or production boundaries? |
| Baseline/comparator | P84 Phase 2 budget contract as precedent, Phase 4 reviewed route mechanics smoke, Phase 3 route manifest, and P86 author source anchors. No weak or mismatched route may serve as a promotion baseline. |
| Primary criterion | Completed training samples meet `minimum_training_samples = max(20 * P_theta, 5000)` for the exact frozen route/rank; every required core status field is acceptable under the status contract below; finite fit and holdout residuals are recorded; clouds are disjoint; route manifest is correct; approved command and artifact path match exactly. |
| Veto diagnostics | Under-budget samples; wrong route; nonfinite target/loss/normalizer/residual; cloud overlap; audit cloud used for tuning; command drift; unapproved runtime; runtime/memory cap breach; hidden fallback to Legendre/local diagnostic route; interpreting training loss alone as fit quality. |
| Explanatory diagnostics | Fit residuals, holdout residuals, replay residuals if present, runtime, memory, branch hashes, warning log, optimizer trace, and CPU/GPU posture. |
| Not concluded | No correctness, convergence, KR closure, HMC readiness, LEDH comparison, scale, or production readiness. |
| Artifact | Fit manifest and Phase 5 result. |

## Core Status Contract

The phrase `core statuses are OK` is not free-form. The status contract is
split so the no-fit preflight artifact is not asked to certify post-fit facts.

Before approval can be requested, the candidate/preflight manifest must report
all of these required fields with these exact acceptable values:

| Field | Acceptable value |
|---|---|
| `route_manifest_ok` | `true` |
| `basis_family` | `lagrangep` |
| `basis_order` | `4` |
| `basis_num_elems` | `8` |
| `domain_map` | `algebraic` |
| `domain_scale` | `1.0` |
| `basis_dim_per_dimension` | `33` |
| `route_changing_cli` | `false` |
| `parameter_count_status` | `ok` |
| `sample_budget_status` | `ok` |
| `cloud_separation_status` | `ok` |
| `command_fidelity_status` | `ok` |
| `reserved_preflight_output_path_status` | `ok` |
| `reserved_fit_output_path_status` | `ok` |
| `planned_runtime_envelope_status` | `ok` |
| `planned_memory_envelope_status` | `ok` |
| `memory_diagnostic_source_status` | `ok` |

After execution, the fit manifest must preserve the preflight-required fields
above and also report all of these post-fit required fields with these exact
acceptable values:

| Field | Acceptable value |
|---|---|
| `fit_status` | `completed` |
| `finite_target_status` | `ok` |
| `finite_loss_status` | `ok` |
| `finite_normalizer_status` | `ok` |
| `finite_fit_residual_status` | `ok` |
| `finite_holdout_residual_status` | `ok` |
| `fallback_route_status` | `not_used` |
| `audit_cloud_tuning_status` | `not_used_for_tuning` |
| `runtime_status` | `within_approved_envelope` |
| `memory_status` | `within_approved_envelope` |

Any missing required field or other value blocks Phase 5 unless the Phase 5
result records a blocker instead of a pass.

## Skeptical Plan Audit Before Execution

Status: `PASS_FOR_SUBPLAN_REVIEW_BLOCKED_BEFORE_RUNTIME_COMMAND`

- Wrong baseline check: P84 Phase 2 is only a precedent for the budget
  contract. The P86 route, artifacts, and interpretation are owned here.
- Proxy-promotion check: Phase 4 one-step smoke, training loss, validation
  residuals, and replay residuals cannot promote correctness, HMC readiness,
  LEDH comparison, scale, or production readiness.
- Missing stop-condition check: this subplan stops on missing exact approval,
  unresolved Claude material revisions, ambiguous parameter-count/sample-floor
  arithmetic, wrong route, cloud overlap, nonfinite diagnostics, runtime cap
  breach, or unavailable trusted GPU/CUDA context if GPU is needed.
- Unfair-comparison check: no cross-route or weak Legendre/local diagnostic
  baseline can be used as a Phase 5 pass criterion.
- Hidden-assumption check: parameter count, rank, basis/domain route, data
  clouds, runtime posture, seeds, and artifact paths must be frozen in the
  command manifest before execution.
- Environment-mismatch check: CPU-only/GPU-hidden is allowed only as an
  explicit non-production posture; GPU/CUDA execution requires trusted/elevated
  approval before any probe or fit command.
- Artifact-answer check: the planned fit manifest and result must answer the
  Phase 5 budget-compliance question; if they cannot record budget arithmetic,
  route identity, cloud separation, finite diagnostics, and exact command
  fidelity, the phase blocks instead of running.
- Artifact-completeness check: the preflight JSON and fit JSON paths are now
  reserved and must be carried into the exact approval package before any
  runtime request.
- Memory-cap check: if memory cap breach is retained as a veto, the exact
  memory cap, diagnostic source, and `planned_memory_envelope_status` must be
  present in the candidate/preflight manifest before approval, and
  `memory_status` must be present in the fit manifest after execution. If a
  reliable memory diagnostic cannot be specified, Phase 5 must remove memory
  cap breach from the pass/fail veto list before approval review rather than
  leave it implicit.

## Forbidden Claims / Actions

- Do not run without exact approval.
- Do not treat training loss alone as correctness.
- Do not treat Phase 4 one-step smoke evidence as budget, fit-quality,
  scientific, correctness, HMC, LEDH, scale, or production evidence.
- Do not use audit data for tuning.
- Do not compare against a weak or mismatched baseline.
- Do not silently change basis, domain map, rank, sample floor, clouds, runtime
  posture, or output path after review.
- Do not claim source-faithfulness without preserving paper/source/local
  anchors.
- Do not claim production readiness.
- Do not execute GPU/CUDA/NVIDIA or model-training commands in a non-escalated
  context.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- at least one budget-compliant author-route fit artifact exists, or Phase 5
  blocks and Phase 6 is explicitly reframed as blocked;
- same-route stronger comparator commands are drafted with disjoint clouds and
  approval requirements;
- Phase 5 result includes a decision table, run manifest, veto diagnostic
  statuses, nonclaim boundaries, and Claude result review outcome;
- Phase 6 subplan has been refreshed to inherit the exact Phase 5 outcome.

## Stop Conditions

Stop if:

- exact approval is not available;
- Claude subplan review returns `VERDICT: REVISE` for a material issue that
  cannot be patched within five loops;
- fit budget, route identity, cloud separation, or finite diagnostics fail;
- parameter-count or sample-floor arithmetic is ambiguous;
- no exact command can be stated without unsupported assumptions;
- runtime or memory exceeds the approved envelope;
- GPU/CUDA runtime is needed but trusted/elevated approval is unavailable;
- Claude and Codex do not converge after five review rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 5 result / close record;
3. draft or refresh the Phase 6 subplan;
4. review the Phase 6 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
