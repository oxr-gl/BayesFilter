# Actual-SIR Nystrom N8192 Paired-Drift Diagnostic Master Program

Date: 2026-06-23

Status: `DRAFT_FOR_P00_REVIEW`

## Supervisor Contract

Codex is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only. Claude may review bounded
paths and concise excerpts, but may not edit files, run experiments, launch
agents, change state, authorize boundary crossings, or change evidence
thresholds.

## Program Objective

Diagnose the paired mean log-likelihood drift that caused the fixed-policy
promotion-stress lane to fail at `N=8192,T=20`, seed `82921`, without silently
retuning or converting a hard-screen failure into a default-promotion claim.

The starting failed policy is:

- `rank=32`;
- `epsilon=0.5`;
- `kernel_mode=raw`;
- `scaling_normalization=none`;
- `core_solver=cholesky`;
- `float32`, TF32 enabled, JIT compiled.

## Prior Evidence

Immediate predecessor:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-result-2026-06-23.md`

Relevant facts:

- Required P01 rows passed:
  - `N=2048,T=20`, seeds `82921,82922,82923`;
  - `N=4096,T=20`, seeds `82921,82922,82923`.
- Launched optional P01 row failed:
  - `N=8192,T=20`, seed `82921`;
  - per-route outputs finite and residuals valid;
  - paired mean/max log-likelihood delta `6.96771240234375`;
  - paired mean threshold `5.0`, max threshold `10.0`.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Is the `N=8192` paired mean drift a reproducible fixed-policy failure, a one-seed stochastic tail, a harness/comparator artifact, or a repairable tuning issue? |
| Candidate/mechanism | Fixed Nystrom policy first; only later, predeclared repair candidates may be tested if replication shows a reproducible issue. |
| Baseline/comparator | Compiled streaming TF32 actual-SIR route in the same paired artifact. |
| Expected failure mode | Replayed/nearby `N=8192` rows may fail paired mean threshold while remaining finite/residual-valid, suggesting approximation drift rather than numerical blow-up. |
| Promotion criterion | None. This is a diagnostic/repair lane, not a default-promotion lane. |
| Promotion veto | Any default-readiness, superiority, posterior-correctness, HMC-readiness, broad robustness, or product default claim. |
| Continuation veto | Invalid/missing artifact, trusted GPU unavailable for GPU phases, fixed-policy metadata drift in P01, criteria drift after results, hard GPU/runtime failure, or Claude/Codex non-convergence after five review rounds. |
| Repair trigger | Reproducible paired-drift failure across replay/nearby `N=8192` seeds with finite route outputs and valid residuals. |
| Explanatory diagnostics | Paired deltas by seed, route log likelihoods, residuals, factor/scaling diagnostics, runtime, memory snapshots. |
| Must not conclude | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness, no broad rejection of Nystrom. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What caused the fixed-policy promotion-stress failure at `N=8192`, and what smallest next action is justified? |
| Exact baseline/comparator | Streaming TF32 route paired in each current-code benchmark artifact. |
| Primary pass/fail criterion | P01 determines whether paired drift is reproducible under the fixed policy; later repair phases may only run if P01 classifies a repairable repeated drift. |
| Veto diagnostics | Missing/malformed artifact, GPU/TF32 evidence missing, fixed-policy metadata mismatch in P01, nonfinite outputs, residual hard veto, paired threshold failure classification mismatch, runtime timeout, unsupported claim. |
| Explanatory diagnostics | Runtime, memory, ESS, residual magnitudes below threshold, factor/scaling ranges, denominator floor hits, paired deltas by seed. |
| Not concluded even if repair passes | No default change, no posterior correctness, no HMC readiness, no statistical superiority, no broad rank/epsilon robustness. |
| Artifacts | Master program, runbook, execution ledger, Claude review ledger, phase subplans/results, benchmark JSON/Markdown/logs, closeout. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance and review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p00-governance-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p00-governance-result-2026-06-23.md` |
| P01 | Fixed-policy replay and seed replication | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p01-fixed-policy-replay-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p01-fixed-policy-replay-result-2026-06-23.md` |
| P02 | Repair candidate selection | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p02-repair-selection-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p02-repair-selection-result-2026-06-23.md` |
| P03 | Focused repair test | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p03-focused-repair-test-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p03-focused-repair-test-result-2026-06-23.md` |
| P04 | Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p04-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p04-closeout-result-2026-06-23.md` |

## Phase Flow

P00 reviews the plan. P01 reruns the failed seed and nearby `N=8192` seeds under
the same fixed policy. If the failed seed does not reproduce, close out as
non-reproduced or inconclusive hard-screen evidence requiring more replication.
If the failed seed reproduces but nearby seeds do not, close out as replayed
single-seed drift requiring more evidence before repair. P02 may select a
repair only if the original failed seed reproduces and at least one nearby seed
also fails with finite/residual-valid artifacts. P03 tests that one selected
repair on the same `N=8192` replay/seed set. P04 classifies the result.

The supervisor should advance automatically after each passed phase. Stop only
for declared stop conditions or true blockers.

## Anticipated Approvals

The supervisor anticipates needing trusted/escalated approval for:

- bounded read-only Claude review through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh`;
- GPU preflight through `nvidia-smi`;
- TensorFlow/CUDA benchmark rows through
  `/home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`.

No approval is requested for destructive filesystem operations, git reset,
package installation, network fetches, detached supervisors, default-policy
changes, commits, or pushes.

## Forbidden Claims And Actions

- Do not change the fixed policy in P01.
- Do not tune after seeing P01 without P02 repair-selection review.
- Do not change paired thresholds after seeing results.
- Do not claim default readiness.
- Do not rank methods using descriptive-only metrics.
- Do not detach execution or launch nested execution agents. Bounded read-only
  Claude review through the approved wrapper is the only allowed cross-agent
  exception.
- Do not modify unrelated dirty worktree changes.
- Do not commit or push.

## Skeptical Plan Audit

Wrong baseline risk: comparing only to the previous failed artifact could hide
current-code or comparator drift. Mitigation: P01 writes fresh paired artifacts.

Proxy-promotion risk: passing a repair on a few one-seed rows could be misread
as default readiness. Mitigation: no default-promotion criterion exists here.

Unfair comparison risk: changing policy during replay would blur diagnosis.
Mitigation: P01 freezes the exact failed fixed policy.

Hidden-assumption risk: the failed `N=8192` seed may be stochastic. Mitigation:
P01 includes replay plus nearby seeds, all interpreted as hard-screen
diagnostics, not statistical ranking.

Environment-mismatch risk: GPU1 may be occupied and GPU0 fallback may be used.
Mitigation: trusted preflight and artifact GPU provenance are required.

Artifact-mismatch risk: repair testing before replication could tune the wrong
thing. Mitigation: P02/P03 are gated behind P01 classification.

Audit status: `PASS_FOR_P00_REVIEW`.
