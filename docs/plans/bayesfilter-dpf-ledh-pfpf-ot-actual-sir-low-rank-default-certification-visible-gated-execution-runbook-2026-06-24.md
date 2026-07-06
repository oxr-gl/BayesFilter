# Actual-SIR Low-Rank LEDH Default-Certification Visible Gated Execution Runbook

Date: 2026-06-24

## Status

`COMPLETE_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus/max is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Execution is visible and recoverable inside the current conversation.

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content. For TensorFlow, CUDA,
benchmark, long test, and Claude review commands:

1. Predeclare log and structured artifact paths in the phase subplan or ledger.
2. Redirect full stdout/stderr to a log file when output may be large.
3. Prefer commands that write JSON/Markdown artifacts directly.
4. After a command, print only exit status, artifact paths, pass/fail fields,
   and at most the last 20-40 log lines on failure.
5. Poll bounded status commands rather than streaming full output.
6. Treat excessive stdout/stderr as an execution-flow defect.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-master-program-2026-06-24.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-claude-review-ledger-2026-06-24.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-visible-execution-ledger-2026-06-24.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-visible-stop-handoff-2026-06-24.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| ---: | --- | --- | --- |
| P00 | Governance, scope lock, and program review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p00-governance-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p00-governance-result-2026-06-24.md` |
| P01 | Evidence inventory and default-surface audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p01-evidence-surface-audit-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p01-evidence-surface-audit-result-2026-06-24.md` |
| P02 | Reference, no-NumPy, and implementation-path audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p02-implementation-audit-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p02-implementation-audit-result-2026-06-24.md` |
| P03 | End-to-end actual-SIR benchmark harness/gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-result-2026-06-24.md` |
| P04 | N4096 resource-boundary feasibility | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-result-2026-06-24.md` |
| P05 | Default-route implementation and focused tests | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-result-2026-06-24.md` |
| P06 | Optional HMC/autodiff mechanics branch | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p06-hmc-autodiff-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p06-hmc-autodiff-result-2026-06-24.md` |
| P07 | Final default-readiness decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p07-closeout-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-result-2026-06-24.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the locked low-rank route become the bounded engineering default for actual-SIR d18 GPU/TF32 LEDH-PFPF-OT? |
| Baseline/comparator | Existing paired streaming TF32 actual-SIR route under the same model, seeds, shape, dtype, TF32, GPU, and timing contract. |
| Primary pass criterion | Every executed phase writes required artifacts and passes hard validity, provenance, comparability, no-NumPy/default-path, and review gates. |
| Veto diagnostics | Missing actual-SIR semantics; nonfinite outputs; route mismatch; dense transport materialization; low-rank factor invalidity; logsumexp/ESS failure; paired comparability failure; failed end-to-end gate; GPU/TF32 mismatch; default/API change without approval; unsupported claim. |
| Explanatory diagnostics | Warm ratios, first-call times, wall times, memory snapshots, residual magnitudes below thresholds, ESS above threshold, and filename lengths. |
| Not concluded | Posterior correctness, HMC readiness, dense Sinkhorn equivalence, statistical superiority, scientific validity, formal memory scaling, or public API readiness unless a separate phase explicitly gates the claim. |
| Artifacts | Master program, runbook, review ledger, execution ledger, phase subplans/results, benchmark JSON/Markdown/logs. |

## Approvals And Trusted Commands

Already requested by the user for this visible launch:

- Claude Code read-only review through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh` with
  `--model opus --effort max`.

Future approvals expected before crossing later gates:

- trusted GPU prechecks and GPU benchmark execution for P03/P04;
- human approval before any default-code, public API, or product-capability
  change in P05;
- human approval before any HMC-readiness claim or HMC-specific runtime in P06;
- human approval before any final default-policy switch if P05 changes code
  rather than only writing a readiness result.

No package installs, network fetches, destructive git commands, or dependency
changes are authorized by this runbook.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Candidate `r16_eps0p25_alpha1em08_it120` | N3072 replicated closeout | Passed all completed screens and had descriptively smaller paired deltas than epsilon `0.125` | Descriptive selection may not generalize | P01 evidence audit, P03 end-to-end gate | hypothesis |
| Streaming comparator | Existing validation harness | Current baseline route for actual-SIR d18 LEDH/PFPF-OT | Unfair comparison if seeds/GPU/timing differ | Artifact validator checks request signatures | baseline |
| GPU/TF32 default target | Project AGENTS policy | Owner-directed default execution target | Trusted GPU unavailable or mixed GPU | trusted `nvidia-smi` and row manifests | reviewed |
| Default-readiness scope | This master program | Separates engineering default from scientific/HMC/API claims | Claim overreach | Claude review and boundary scan | reviewed |

## Skeptical Plan Audit

Before executing any phase, Codex records a skeptical audit in the execution
ledger. The audit must check wrong baselines, proxy metrics promoted to pass
criteria, missing stop conditions, unfair comparisons, hidden assumptions,
stale context, environment mismatch, and artifacts that would not answer the
phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`: read the subplan, confirm prerequisites, restate the evidence
   contract, and append a ledger entry.
2. `EXECUTE_MINIMAL`: run only the visible commands required by the phase.
3. `ASSESS_GATE`: compare outputs against the primary criterion and vetoes.
4. `PASS_REVIEW`: send material plans/results to Claude as read-only review.
5. `REPAIR_LOOP`: patch fixable issues visibly, rerun focused checks, and stop
   after five review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current gate passes, otherwise
   write a blocker or stop handoff.

## Claude Read-Only Review Template

Use Claude only as reviewer. Prompts must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the named paths only.

Check wrong baseline, proxy metric promotion, missing stop condition, unfair
comparison, hidden assumption, stale context, environment mismatch,
unsupported claim, artifact mismatch, and boundary safety.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing would require:

- default-policy/code change not already approved by the user;
- public API change;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- modifying unrelated dirty user work;
- interpreting GPU results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

When execution completes or stops, write final phase reached, final status,
result artifacts, Claude review trail, tests/benchmarks actually run,
unresolved blockers, nonclaims, and safest next human decision.
