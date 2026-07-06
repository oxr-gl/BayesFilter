# Actual-SIR Nystrom Less-Intrusive Stability Master Program

Date: 2026-06-23

## Status

`DRAFT_FOR_P00_REVIEW`

## Supervisor Contract

Codex is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.  Claude may review bounded
paths and diffs, but may not edit files, run experiments, launch agents, change
state, authorize boundary crossings, or change evidence thresholds.

## Program Objective

Find whether the actual-SIR fixed-rank Nystrom route has a less-intrusive
stabilization than dense `positive_projected` that:

- keeps the known brittle row finite;
- keeps Nystrom residuals below the existing thresholds;
- preserves the predeclared paired log-likelihood thresholds against the
  compiled streaming TF32 comparator;
- produces artifacts sufficient to decide whether to continue repair,
  restrict policy to the already viable neighborhood, or stop.

This program is a repair and diagnostic program.  It is not a default-promotion
program.

## Prior Evidence

Closed source lane:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p07-closeout-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-stop-handoff-2026-06-23.md`

Relevant prior facts:

- Raw `rank=32,epsilon=0.25` passed at `T=2` and failed at `T=4`.
- Raw `rank=64,epsilon=0.3` passed at `T=2` and failed at `T=4`.
- Raw `rank=32,epsilon=0.5` control passed at `T=4` and `T=20`.
- `svd_truncated,rcond=1e-6` did not rescue the known failing rows.
- `positive_projected` made `rank=32,epsilon=0.25` finite and residual-valid,
  but failed paired max log-likelihood delta: observed `12.91107177734375`,
  threshold `10.0`.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can a less-intrusive Nystrom stabilization repair the brittle actual-SIR row without breaking paired comparability? |
| Candidate/mechanism | A single scoped stabilization family selected after diagnostic localization: preferably rescaled/log-stable low-rank Sinkhorn or similarly minimal factor/scaling repair. |
| Baseline/comparator | Compiled production-style streaming TF32 actual-SIR route; raw Nystrom brittle artifacts; positive projection as diagnostic-only rescue evidence. |
| Expected failure mode | The candidate may rescue finite/residual behavior but still alter paired likelihood too much, or may not rescue finite behavior at all. |
| Promotion criterion | For the repair candidate only: finite factors/particles, row/column residuals below existing threshold, and paired max/mean log-likelihood deltas within existing thresholds on `rank=32,epsilon=0.25`. |
| Promotion veto | Any nonfinite candidate output, Nystrom residual threshold failure, paired max delta above `10.0`, paired mean delta above `5.0`, missing GPU/TF32 evidence, or missing artifact. |
| Continuation veto | Harness invalidity, diagnostics unavailable before failure, criteria drift after observing results, Claude/Codex non-convergence after five rounds for the same material blocker, or human-required boundary crossing. |
| Repair trigger | Diagnostics indicate a local factor/scaling instability that can be addressed by one scoped algorithmic change without changing rank/epsilon thresholds. |
| Explanatory diagnostics | Kernel negativity, factor diagonal error, scaling ranges, denominator floor hits, runtime, projection floor hits, spectra, prefix behavior. |
| Must not conclude | No default readiness, no superiority/ranking, no posterior correctness, no dense Sinkhorn equivalence, no HMC readiness, no scalable high-N readiness, no broad robustness or unusability claim. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Program review and launch gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-program-review-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-program-review-result-2026-06-23.md` |
| P01 | Diagnostic adequacy and missing-instrumentation gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-diagnostic-adequacy-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-diagnostic-adequacy-result-2026-06-23.md` |
| P02 | Less-intrusive repair selection | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-repair-selection-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-repair-selection-result-2026-06-23.md` |
| P03 | Focused implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-result-2026-06-23.md` |
| P04 | Known brittle row repair gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-result-2026-06-23.md` |
| P05 | Neighborhood and control gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p05-neighborhood-control-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p05-neighborhood-control-result-2026-06-23.md` |
| P06 | Promotion-readiness decision gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-promotion-readiness-decision-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-promotion-readiness-decision-result-2026-06-23.md` |
| P07 | Closeout handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-result-2026-06-23.md` |

## Phase Flow

P00 reviews this master program and the visible runbook.  P01 checks whether
current diagnostics are enough for repair selection and implements only missing
diagnostics if needed.  P02 selects exactly one less-intrusive repair family.
P03 implements the selected opt-in repair.  P04 tests the first known brittle
row.  P05 tests the nearby brittle row and control.  P06 decides whether a
separate default-promotion program is justified or whether the lane should
close as fixed-policy or failed-repair evidence.  P07 writes final handoff.

The supervisor should advance automatically after each passed phase.  Stop only
for declared stop conditions or true blockers.

## Anticipated Approvals

The supervisor anticipates needing trusted/escalated approval for:

- Claude review through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh`;
- GPU preflight through `nvidia-smi`;
- TensorFlow/CUDA benchmark rows through
  `/home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`;
- CPU-hidden focused tests if the local sandbox blocks TensorFlow caches or
  device initialization.

No approval is requested for destructive filesystem operations, git reset,
package installation, network fetches, or default-policy changes.

## Forbidden Claims And Actions

- Do not claim default readiness in this program.
- Do not claim repair success from proxy diagnostics alone.
- Do not rank methods using descriptive-only metrics.
- Do not change paired thresholds after seeing results.
- Do not reopen the closed positive-projection P09/P10 program.
- Do not use dense `positive_projected` as a promotion repair in this lane.
- Do not detach execution or launch nested agents.
- Do not modify unrelated dirty worktree changes.
- Do not commit or push.

## Skeptical Plan Audit

Potential wrong baseline: comparing only against raw Nystrom would hide paired
semantic drift.  Mitigation: P04/P05 require paired streaming TF32 thresholds.

Potential proxy promotion: finite residuals alone could look like repair
success.  Mitigation: paired max and mean log-likelihood thresholds are hard
vetoes.

Potential unfair comparison: changing rank/epsilon while claiming repair would
turn the program into tuning.  Mitigation: P04 uses the same
`rank=32,epsilon=0.25` row and P05 separately tests neighborhood/control.

Potential stale context: previous program is closed.  Mitigation: this lane has
new paths, ledgers, and stop handoff, and references the prior lane only as
evidence.

Potential environment mismatch: GPU artifacts require trusted GPU evidence and
GPU1 preference with GPU0 fallback.

Potential artifact mismatch: each phase has a required result file and exact
handoff conditions.

Audit status: `PASS_FOR_P00_REVIEW`.  Execution begins only after P00 local
checks and Claude read-only review converge.
