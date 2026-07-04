# BayesFilter General NeuTra SSM Interface Master Program

Date: 2026-07-03

Status: `DRAFT_UNDER_REVIEW`

## Objective

Design and execute a BayesFilter-owned interface that makes NeuTra usable for
Bayesian estimation of nonlinear state-space models through any BayesFilter
filter that satisfies a reviewed HMC target contract.

The intended composition is:

```text
Bayesian SSM problem
+ parameter chart
+ prior
+ BayesFilter filter program
-> batch-native posterior value/score adapter in unconstrained coordinates
-> optional frozen or trainable NeuTra transport
-> BayesFilter-owned HMC runtime, tuning, diagnostics, and artifacts
```

## Role Contract

Codex is the supervisor and executor.

Claude Opus at max effort is a read-only reviewer only. Claude may review
bounded plan paths, result paths, or exact line ranges. Claude must not edit,
run commands, launch agents, authorize boundary crossings, or change state.

Human approval remains required for project-direction changes, package
installation, network fetches, destructive git/filesystem operations, detached
execution, GPU/accelerator research runs, serious NeuTra training, serious HMC
validation, default-policy changes, or scientific claims.

## Current Design Baseline

Existing reusable BayesFilter surfaces:

- `bayesfilter.inference.posterior_adapter`: value/score authority,
  nonlinear SSM static metadata, stable target signatures.
- `bayesfilter.inference.batched_value_score`: batch-native custom-gradient
  target wrappers and the current frozen transport value/score adapter.
- `bayesfilter.inference.hmc`, `hmc_tuning`, and `hmc_budget_ladder`: HMC
  runtime and diagnostic surfaces.
- `bayesfilter.nonlinear`, `bayesfilter.linear`, and `bayesfilter.highdim`:
  existing filter implementations and target-specific evidence patterns.

Existing NeuTra evidence from `~/python` should be reused as frozen artifacts
when signatures and hashes match. It must not trigger automatic retraining.

## Design Boundary

BayesFilter owns:

- generic SSM target contracts;
- filter-program capability declarations;
- posterior value/score adapter construction;
- frozen transport wrapper semantics;
- HMC target construction, tuning policy, diagnostics, and manifests;
- artifact signature checks and fail-closed reuse decisions.

External model packages own:

- model equations;
- data preparation;
- parameter names and parameter transforms;
- priors;
- target-specific source evidence;
- frozen training-state payload storage when generated artifacts are too large
  for git.

NeuTra training is a later optional phase. It must use trusted GPU execution by
default. CPU hiding is allowed only for small contract tests, loader checks,
debug-only reducer replays, or explicitly CPU-only HMC workers.

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | Governance, scope, and artifact boundary | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-result-2026-07-03.md` |
| 1 | Generic SSM contract scaffold | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-result-2026-07-03.md` |
| 2 | Posterior target builder and toy nonlinear fixture | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-result-2026-07-03.md` |
| 3 | Filter-program registry and capability gates | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-result-2026-07-03.md` |
| 4 | Frozen NeuTra transport artifact loader | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-result-2026-07-03.md` |
| 5 | Fixed-transport HMC runtime binding | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-result-2026-07-03.md` |
| 6 | Existing NeuTra artifact reuse bridge | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-reuse-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-reuse-result-2026-07-03.md` |
| 7 | Validation ladder and closeout | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase7-validation-closeout-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase7-validation-closeout-result-2026-07-03.md` |

## Shared Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter expose a generic Bayesian nonlinear SSM posterior value/score target that can be filtered by any admissible BayesFilter filter and optionally transformed by NeuTra? |
| Baseline/comparator | Existing BayesFilter posterior adapter and HMC authority contracts; existing DSGE NeuTra artifact evidence is reuse input, not the generic design baseline. |
| Primary pass criterion | Each phase writes its required artifact, local checks pass, material next-phase subplans receive read-only review convergence or a documented blocker, and no phase crosses its declared boundary. |
| Veto diagnostics | Missing subplan fields, unstable signatures, hidden scalar row loops in batch-native paths, stochastic particle likelihoods without deterministic artifact state, fallback value/score authority promoted into XLA HMC, CPU-hidden NeuTra training, stale artifact reuse, unsupported claims, or Claude/Codex nonconvergence after five rounds. |
| Explanatory diagnostics | Code coverage, fixture likelihood values, speed, acceptance, R-hat, ESS, training losses, and artifact availability unless explicitly promoted by a phase evidence contract. |
| Not concluded | No posterior correctness, no NeuTra superiority, no default sampler change, no all-filter HMC readiness, no production readiness for every nonlinear SSM, no scientific claim about DSGE models. |
| Artifacts | Master program, phase subplans/results, visible runbook, execution ledger, Claude review ledger, stop handoff, focused tests, and any generated JSON manifests. |

## Required Subplan Shape

Every phase subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each phase execution Codex must:

1. run required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude read-only review for material subplans or boundary decisions.

## Repair Loop

For each material blocker:

1. classify the blocker as plan, implementation, evidence, artifact,
   environment, or human-boundary;
2. patch the same subplan or source visibly if the issue is fixable within the
   approved phase boundary;
3. rerun the focused local checks that address the blocker;
4. rerun Claude review only on the bounded path or exact line range needed;
5. stop after five Claude review rounds for the same blocker and write a
   blocker result.

Claude review cannot authorize crossing human, runtime, model-file, funding,
product-capability, default-policy, or scientific-claim boundaries.

## Claude Review Protocol

Use the smallest prompt surface that can answer the gate. Do not paste whole
files into prompts. The default prompt shape is one exact path:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <path>. Do not edit,
run commands, launch agents, or review the whole repo. Question: <gate>.
End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude gives no output or times out, run a health probe:

```text
Return exactly CLAUDE_PROBE_OK.
```

If the health probe passes, shrink or redesign the review prompt.

## Approvals Anticipated

Expected approvals during this visible program:

- Escalated/trusted Claude Code usage for each read-only review or probe.
- Escalated/trusted GPU probes or GPU jobs only if a later phase explicitly
  reaches NeuTra training or GPU HMC validation.

Not expected during Phase 0:

- package installation;
- network fetch;
- destructive git operation;
- detached execution;
- serious GPU training;
- serious stochastic comparison.

## Skeptical Plan Audit

Initial audit status: `PASSED_WITH_BOUNDARIES`.

Checked risks:

- Wrong baseline: avoided by using existing BayesFilter contracts as the design
  baseline and DSGE artifacts only as reuse inputs.
- Proxy metrics promoted to pass criteria: forbidden by phase contracts.
- Missing stop conditions: each phase subplan includes stop conditions.
- Unfair comparisons: no method ranking is part of this master program.
- Hidden assumptions: GPU default, deterministic HMC targets, and artifact
  signature matching are explicit.
- Stale context: Phase 0 includes artifact inventory and signature boundary.
- Environment mismatch: GPU and Claude commands require trusted execution.
- Artifacts not answering the question: each phase has required result
  artifacts and next-phase handoff conditions.

## Current Launch Decision

Proceed only with Phase 0 after this master program, Phase 0 subplan, Phase 1
subplan, and visible runbook pass local consistency checks and read-only review
or produce a documented blocker.

