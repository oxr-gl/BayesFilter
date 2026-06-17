# Visible Gated Overnight Execution Plan: Batched LEDH-PFPF-OT

Date: 2026-06-15

## Status

`REVIEWED_PHASE_0_LAUNCH_READY`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This plan is deliberately not a detached overnight launcher. It follows the
visible-gated runbook pattern in the current dialogue. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, detached `tmux`, or backgrounded phase runners;
- copied-workspace execution.

If the user later wants detached unattended execution, stop and write a separate
detached-supervisor plan for explicit human approval.

## Governing Program

Master program:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-master-program-2026-06-15.md`

Visible runbook:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-visible-gated-execution-runbook-2026-06-15.md`

Claude review trail:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-claude-review-round-01-2026-06-15.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-visible-execution-ledger-2026-06-15.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-visible-stop-handoff-2026-06-15.md`

## Launch Decision

Launch starts only after Claude plan review converges with `VERDICT: AGREE` or
Codex patches fixable issues and reruns focused checks. Once launched, Phase 0
begins visibly in this conversation and continues phase-by-phase until a gate
passes, a real stop condition fires, or human approval is required.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the LEDH-PFPF-OT relaxed objective be made batch-native across parameter rows with deterministic parity and later value+score support? |
| Baseline/comparator | Existing scalar LEDH-PFPF-OT TensorFlow path and scalar-stack parity using identical noise/contracts. |
| Primary pass criterion | Every old scalar-relevant behavior used as baseline is inventoried, every new batched phase has parity/finite checks, and no unsupported categorical PF or production claim is made. |
| Veto diagnostics | Scalar parity failure; row cross-talk; nondeterministic RNG in core; `.numpy()`/Python control flow in compiled core; uncompiled GPU benchmark; missing phase result; Claude nonconvergence after five rounds. |
| Explanatory diagnostics | ESS, transport residuals, log-det ranges, score finite-difference gaps, compile time, warm-call time, memory notes. |
| Not concluded | No production default, categorical PF gradient, posterior correctness, HMC/NeuTra readiness, or GPU speedup before Phase 5. |
| Artifacts | Phase results, pytest output summaries, benchmark JSON/MD when reached, ledger, Claude review artifacts, final closeout. |

## Phase Order

| Phase | Gate |
| --- | --- |
| P0 | Inventory current scalar LEDH-PFPF-OT, determinism gaps, graph blockers, and file boundaries. |
| P1 | Define batch callback/shape contract and deterministic fixture scaffolding. |
| P2 | Implement batched LEDH flow and transport core. |
| P3 | Implement value recursion and prove B=1/B=20 scalar-stack parity. |
| P4 | Implement value+score and finite-difference checks for relaxed objective. |
| P5 | Run JIT-only CPU/GPU benchmark ladder when trusted GPU approval is available. |
| P6 | Closeout experimental-readiness and production-boundary decision. |

## Repair Loop

For each phase:

1. Run a local skeptical phase audit.
2. Execute the smallest visible diagnostic or implementation needed.
3. Write the phase result and machine-readable artifact when applicable.
4. Draft or refresh the next subplan.
5. Review the next subplan locally for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
6. Send material result/subplan material to Claude Opus max effort as read-only
   reviewer.
7. If Claude returns `VERDICT: REVISE`, audit the finding, repair the artifact
   or implementation, rerun focused checks, and repeat.
8. Stop only after `VERDICT: AGREE`, max five review loops, or a real
   human-required stop condition.

Finite-only numerical output is not a promotion criterion. Promotion requires
predeclared parity, row-independence, gradient, and compilation checks.

## Claude Probe Fallback

If a Claude review call produces no useful response:

1. Run a small read-only probe through
   `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh` asking for
   exactly `PROBE_OK`.
2. If the probe fails, classify as a Claude availability/tooling blocker and
   write a visible stop handoff.
3. If the probe succeeds, treat the prior review prompt as the problem,
   shorten and redesign the review prompt, then retry the same review
   iteration without counting it as a substantive Claude disagreement.

## Anticipated Approval Needs

- Trusted Claude Code review calls through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.
- Deliberate CPU-only TensorFlow/PyTest runs with `CUDA_VISIBLE_DEVICES=-1`.
- Trusted GPU/CUDA commands only in Phase 5, and only after all correctness
  gates pass.
- Non-destructive writes under `docs/plans`, `tests`, and
  `experiments/dpf_implementation/tf_tfp` for this experimental path.

Destructive git/filesystem operations, package installation, network fetches,
credential changes, detached execution, default-policy changes, and production
API changes remain human-required stop conditions unless separately approved.

## Initial Skeptical Execution Audit

| Risk | Status | Control |
| --- | --- | --- |
| Wrong baseline | Passed with guard | Phase 0 must inventory scalar LEDH-PFPF-OT and deterministic parity requirements before implementation. |
| Proxy promotion | Passed with guard | RMSE, finite values, and speed are explanatory unless paired with declared parity/gradient gates. |
| Missing stop condition | Passed | Human-required stops and five-round Claude cap are explicit. |
| Unfair comparison | Passed with guard | Scalar-stack parity must use identical noise and transport parameters. |
| Hidden assumption | Passed with guard | Relaxed objective is named; categorical PF gradient is forbidden. |
| Stale context | Passed with guard | Phase 0 inventories current files and tests. |
| Environment mismatch | Passed with guard | TensorFlow import and CPU-only smoke are Phase 0 checks. |
| Artifact mismatch | Passed | Every phase has result and review artifacts. |

## Launch State

Claude review round 01 converged with `VERDICT: AGREE` after the runbook
nonresponse protocol was used.

Next visible action: start Phase 0 `PRECHECK`, write ledger entry, and run
Phase 0 inventory/local checks.
