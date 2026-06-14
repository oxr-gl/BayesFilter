# Visible Gated Overnight Execution Plan: Algorithm 1 UKF Rerun Of LEDH-PFPF-OT Tests

Date: 2026-06-10

## Status

`LAUNCH_READY_VISIBLE_EXECUTION`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This plan is deliberately not a detached overnight launcher.  It follows the
visible-gated runbook pattern in the current dialogue.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, detached `tmux`, or backgrounded phase runners;
- copied-workspace execution.

## Governing Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-master-program-2026-06-10.md`

Reviewed visible runbook:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-visible-gated-execution-runbook-2026-06-10.md`

Claude plan review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-claude-review-ledger-2026-06-10.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-visible-execution-ledger-2026-06-10.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-visible-stop-handoff-2026-06-10.md`

## Launch Decision

The master program and subplans were reviewed by Claude Opus max effort until
convergence:

- iteration 1: `VERDICT: REVISE`;
- iteration 2: `VERDICT: AGREE`.

This execution plan therefore launches P0 and continues phase-by-phase until
the program completes, reaches a real stop condition, or requires a human
decision under the runbook.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the old LEDH-PFPF-OT-related tests be redone visibly with Algorithm 1 UKF, or classified without overclaiming? |
| Baseline/comparator | Old LEDH-PFPF-OT tests define coverage only.  Current comparators are exact or valid approximation routes declared per model. |
| Primary pass criterion | All old LEDH-PFPF-OT lanes receive a reviewed new status and no old row remains usable as Algorithm 1 evidence. |
| Veto diagnostics | Old implementation used as current evidence; missing Algorithm 1 route ids; unsupported model/filter pair ranked; missing MC uncertainty; nonfinite numerics; hidden detached execution. |
| Explanatory diagnostics | Runtime, ESS, value and gradient errors, covariance spectra, determinant ranges, old-vs-new deltas. |
| Not concluded | No production default, HMC readiness, universal superiority, or OT-as-source-Algorithm-1 claim. |
| Artifacts | Phase results, JSON/Markdown reports, visible ledger, Claude review ledger, closeout. |

## Phase Order

| Phase | Gate |
| --- | --- |
| P0 | Inventory registry, thresholds, route fields, and Algorithm 1 guardrail pytest |
| P1 | Direct LGSSM/range-bearing/stress/gradient replacement or precise blockers |
| P2 | V2 Algorithm 1 contract replacement |
| P3 | V2 Algorithm 1 value replacement |
| P4 | V2 Algorithm 1 gradient replacement |
| P5 | Filter-oracle statistical-closeness replacement |
| P6 | Cross-filter calibration replacement |
| P7 | P44/P8 blocker-closure replacement |
| P8 | FilterFlow, annealed, and historical-regression classification |
| P9 | Final closeout and supersession ledger |

## Repair Loop

For each phase:

1. Run a local skeptical phase audit.
2. Execute the smallest visible diagnostic or implementation needed.
3. Write the phase result and machine-readable artifact when applicable.
4. Send the result to Claude Opus max effort as read-only reviewer.
5. If Claude returns `VERDICT: REVISE`, audit the finding, repair the artifact
   or implementation, rerun focused checks, and repeat.
6. Stop only after `VERDICT: AGREE`, max five review loops, or a real
   human-required stop condition.

Finite-only numerical output is not a promotion criterion.  Promotion requires
predeclared P0/P2 thresholds, uncertainty, route identifiers, and clear veto
diagnostics.

## Claude Probe Fallback

If a Claude review call produces no useful response:

1. Run a small read-only probe:

   ```bash
   bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name claude-probe --model claude-opus-4-7 --effort max --permission-mode dontAsk 'READ-ONLY PROBE. Reply with exactly: PROBE_OK'
   ```

2. If the probe fails, classify as a Claude availability/tooling blocker and
   write a visible stop handoff.
3. If the probe succeeds, treat the prior review prompt as the problem,
   shorten and redesign the review prompt, then retry the same review
   iteration without counting it as a substantive Claude disagreement.

## Anticipated Approval Needs

The user has asked for smooth continuous execution.  The following command
families are anticipated:

- trusted Claude Code review calls through
  `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`;
- deliberate CPU-only TensorFlow/PyTest runs with
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp ...`;
- read-only inventory commands such as `rg`, `sed`, `git status`, and
  `git rev-parse`;
- non-destructive file writes under `docs/plans` and
  `experiments/dpf_implementation/reports`;
- focused implementation edits under `experiments/dpf_implementation/tf_tfp`
  only when a reviewed phase requires replacement runners or adapters.

Destructive git/filesystem operations, package installation, network fetches,
credential changes, default-policy changes, and GPU/CUDA execution remain
human-required stop conditions unless separately approved.

## Initial Skeptical Execution Audit

| Risk | Status | Control |
| --- | --- | --- |
| Wrong baseline | Passed | Old LEDH-PFPF-OT is coverage history only; Algorithm 1 UKF is the replacement route. |
| Proxy promotion | Passed | P0 registry must predeclare thresholds before P1-P9 promote rows. |
| Missing stop condition | Passed | Runbook stop conditions, max-five review loop, and Claude probe fallback are explicit. |
| Unfair comparison | Passed | Stochastic rows require paired seeds, particle ladders, and uncertainty. |
| Hidden assumption | Passed | Core Algorithm 1 and BayesFilter OT/annealed extensions are separated by required row fields. |
| Stale context | Passed | P0 reruns repo-wide inventory before later phases. |
| Artifact mismatch | Passed | Every phase has required result artifacts and JSON/Markdown outputs where applicable. |
| Environment mismatch | Passed | CPU-only commands hide CUDA before TensorFlow import; GPU/CUDA commands are not part of this launch. |

## Launch State

Next visible action: start P0 `PRECHECK`, then write the execution ledger entry
and P0 inventory registry.

