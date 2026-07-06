# BayesFilter General NeuTra SSM Interface Visible Gated Execution Runbook

Date: 2026-07-03

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is an overnight-capable gated plan in the sense that every phase has a
visible stop/restart ledger. It is not a detached overnight supervisor.

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content. For commands with large
output:

1. predeclare log and structured artifact paths;
2. redirect full output to logs;
3. print only bounded summaries;
4. preserve artifacts and paths in the phase result;
5. poll bounded status rather than streaming long output.

## Program

Master program:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-master-program-2026-07-03.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-claude-review-ledger-2026-07-03.md`

Execution ledger:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-execution-ledger-2026-07-03.md`

Stop handoff:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, scope, and artifact boundary | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-result-2026-07-03.md` |
| 1 | Generic SSM contract scaffold | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-result-2026-07-03.md` |
| 2 | Posterior target builder and toy nonlinear fixture | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-result-2026-07-03.md` |
| 3 | Filter-program registry and capability gates | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-result-2026-07-03.md` |
| 4 | Frozen NeuTra transport artifact loader | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-result-2026-07-03.md` |
| 5 | Fixed-transport HMC runtime binding | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-result-2026-07-03.md` |
| 6 | Existing NeuTra artifact reuse bridge | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-reuse-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-reuse-result-2026-07-03.md` |
| 7 | Validation ladder and closeout | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase7-validation-closeout-subplan-2026-07-03.md` | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase7-validation-closeout-result-2026-07-03.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generic NeuTra SSM interface be implemented through visible gated phases without crossing scientific, runtime, or artifact boundaries? |
| Baseline/comparator | Master program and existing BayesFilter inference contracts. |
| Primary pass criterion | Every crossed phase has a passing result artifact, required local checks, next-subplan review, and no unresolved stop condition. |
| Veto diagnostics | Missing subplan field, failed required test, Claude/Codex nonconvergence after five review rounds, hidden GPU/CPU policy drift, unsupported claims, artifact mismatch, or unauthorized boundary crossing. |
| Explanatory diagnostics | Review count, test count, fixture values, loader hashes, tiny HMC smoke metrics. |
| Not concluded | No posterior correctness, no NeuTra superiority, no default sampler change, no all-filter HMC readiness. |
| Artifacts | Master program, subplans/results, ledgers, logs, focused tests, structured JSON outputs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow/TFP backend | BayesFilter governance | Existing default implementation backend | Accidental NumPy/JAX/PyTorch algorithmic path | Focused tests and source review | Reviewed policy |
| GPU default for NeuTra training | BayesFilter governance and user correction | Neural transport training should not hide GPU | CPU-only artifact misrepresented as training evidence | Run manifests must label device policy | Reviewed policy |
| Frozen transport before training | Existing successful NeuTra artifacts | Reuse avoids waste and preserves evidence | Missing or mismatched artifact reused | Phase 6 signature/hash inventory | Hypothesis |
| Claude read-only review | User request and local policy | Independent plan-boundary review | Claude treated as authority or prompt hangs | Bounded prompt and probe ladder | Reviewed protocol |

## Skeptical Plan Audit

Before each phase Codex must record a skeptical audit in chat and the ledger:

- wrong baselines;
- proxy metrics treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the question.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the evidence contract.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in this conversation.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result.
4. `PASS_REVIEW`
   - Send material phase results or next subplans to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - Patch fixable blockers visibly.
   - Rerun focused checks.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Invocation Pattern

Use the supervised wrapper with escalated/trusted execution. Do not paste whole
files into the prompt.

Example:

```bash
timeout 600 bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name general-neutra-phase0-review-r1 \
  --model opus \
  --effort max \
  "READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-subplan-2026-07-03.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this subplan satisfy the requested phase-subplan fields, evidence contract, repair loop, stop conditions, and boundary safety? End with VERDICT: AGREE or VERDICT: REVISE."
```

If no output or timeout occurs, run:

```bash
timeout 120 bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name general-neutra-claude-probe \
  --model opus \
  --effort max \
  "Return exactly CLAUDE_PROBE_OK."
```

If the probe succeeds, redesign the prompt and retry the bounded review.

## Human-Required Stop Conditions

Stop if continuing would require:

- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- detached execution;
- serious GPU/NeuTra/HMC run without reviewed plan and trusted-context approval;
- changing pass/fail criteria after seeing results;
- default-policy change;
- modifying unrelated dirty user work;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

At completion or stop, update the stop handoff with:

- current phase and state;
- completed artifacts;
- unresolved blockers;
- commands run and where logs live;
- next exact action.
