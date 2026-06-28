# Actual-SIR Nystrom Fixed-Policy Promotion-Stress Master Program

Date: 2026-06-23

Status: `DRAFT_FOR_P00_REVIEW`

## Supervisor Contract

Codex is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only. Claude may review bounded
paths and concise excerpts, but may not edit files, run experiments, launch
agents, change state, authorize boundary crossings, or change evidence
thresholds.

## Program Objective

Decide whether the currently viable fixed Nystrom actual-SIR policy has enough
promotion-stress evidence to be considered for a default-policy decision, while
preserving strict boundaries around what is and is not proven.

Fixed policy under test:

- `rank=32`;
- `epsilon=0.5`;
- `kernel_mode=raw`;
- `scaling_normalization=none`;
- `core_solver=cholesky`;
- `float32`, TF32 enabled, JIT compiled;
- trusted GPU, using GPU1 if available and otherwise GPU0.

This program tests a restricted fixed policy. It does not tune rank, epsilon,
kernel mode, solver, or scaling normalization.

## Prior Evidence

Closed repair lane:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-result-2026-06-23.md`

Closed fixed-policy validation/stress lanes:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-validation-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-stress-closeout-result-2026-06-23.md`

Relevant prior facts:

- Balanced scaling was implemented as an opt-in diagnostic/repair candidate,
  but failed the serious brittle row by nonfinite factors/particles/log
  likelihood.
- The fixed policy `rank=32,epsilon=0.5,raw,none` passed:
  - `N=1024,T=20`, seeds `81920..81924`;
  - two extra `N=1024,T=20` seed batches, seeds `81925..81934`;
  - one-seed high-N rows at `N=2048,4096,8192`.
- Those passes support viability only. They do not establish default readiness,
  posterior correctness, HMC readiness, broad rank/epsilon robustness, or
  statistical superiority.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the fixed Nystrom policy survive promotion-stress gates that were missing from the earlier viability lane: replicated high-N, full-history/memory, and Nystrom-specific gradient mechanics? |
| Candidate/mechanism | Compiled tensor-only fixed-rank Nystrom actual-SIR route with raw kernel and no scaling normalization. |
| Baseline/comparator | Compiled production-style streaming TF32 actual-SIR route, paired in the same artifacts. |
| Expected failure mode | High-N replication may reveal nonfinite factors/particles, residual failures, paired log-likelihood drift, memory/history issues, or Nystrom gradient-mechanics blockers. |
| Promotion criterion | Passing all phases only permits a final classification of `PROMOTION_STRESS_PASSED_FOR_HUMAN_DEFAULT_REVIEW`. It does not itself change defaults. |
| Promotion veto | Any default-readiness, superiority, posterior-correctness, HMC-readiness, broad robustness, or production-safety claim without the final evidence package and human/default-policy decision. |
| Continuation veto | Invalid/missing artifact, trusted GPU unavailable for GPU phases, missing fixed-policy metadata, criteria drift after observing results, hard-veto failure, runtime stop, or Nystrom gradient artifact invalidity. |
| Repair trigger | A valid candidate failure with complete artifacts triggers classification and a separate repair/tuning plan, not silent retuning inside this fixed-policy lane. |
| Explanatory diagnostics | Runtime, memory reports, warm timings, residual magnitudes below threshold, denominator/factor/scaling diagnostics, ESS, gradient norm, and tiny gradient-smoke shape. |
| Must not conclude | No default change, no statistical ranking/superiority, no posterior correctness, no dense Sinkhorn equivalence, no HMC readiness, no broad robust rank/epsilon policy. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the restricted fixed Nystrom policy pass replicated high-N, full-history/memory, and Nystrom-specific gradient-mechanics gates against the compiled streaming TF32 comparator? |
| Exact baseline/comparator | The streaming TF32 actual-SIR route executed in the same benchmark artifact for paired rows. |
| Primary pass/fail criterion | Every launched phase writes required artifacts and passes its hard-veto screen without criteria drift. Final pass requires P01 replicated high-N, P02 full-history/memory, P03 Nystrom-specific gradient mechanics, and P04 closeout review to pass. |
| Veto diagnostics | Any aggregate hard veto, nonfinite route output, Nystrom residual threshold failure, paired max delta above `10.0`, paired mean delta above `5.0`, missing GPU/TF32 provenance, missing fixed-policy metadata, missing artifact, runtime timeout, malformed JSON, missing or nonfinite Nystrom gradient, or unsupported claim. |
| Explanatory diagnostics | Runtime, memory snapshots, warm-call timing ratios, ESS, residual magnitudes below threshold, factor/scaling ranges, denominator floor hits, gradient norm, tiny gradient-smoke shape. |
| Not concluded even if pass | No default change, no posterior correctness, no HMC readiness, no statistical superiority, no broad rank/epsilon robustness, no dense Sinkhorn equivalence. |
| Artifacts | Master program, visible runbook, execution ledger, Claude review ledger, phase subplans/results, benchmark JSON/Markdown/logs, final closeout. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance, local audit, and Claude review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p00-governance-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p00-governance-result-2026-06-23.md` |
| P01 | Replicated high-N gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-result-2026-06-23.md` |
| P02 | Full-history/memory gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-memory-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-memory-result-2026-06-23.md` |
| P03 | Nystrom-specific gradient mechanics gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p03-hmc-gradient-mechanics-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p03-hmc-gradient-mechanics-result-2026-06-23.md` |
| P04 | Closeout and default-review classification | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-result-2026-06-23.md` |

## Phase Flow

P00 reviews this program and the visible runbook. If it converges, P01 runs
replicated high-N rows at the fixed policy. If P01 passes, P02 runs
full-history/memory rows at the same fixed policy. If P02 passes, P03 runs a
Nystrom-specific gradient mechanics screen and explicitly avoids HMC readiness
claims.
P04 synthesizes the evidence and classifies the lane.

The supervisor should advance automatically after each passed phase. Stop only
for declared stop conditions or true blockers.

## Anticipated Approvals

The supervisor anticipates needing trusted/escalated approval for:

- bounded read-only Claude review through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh`;
- GPU preflight through `nvidia-smi`;
- TensorFlow/CUDA benchmark rows through
  `/home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`;
- TensorFlow CPU-hidden HMC mechanics smoke if sandbox blocks framework caches
  or device initialization.

No approval is requested for destructive filesystem operations, git reset,
package installation, network fetches, detached supervisors, default-policy
changes, commits, or pushes.

## Forbidden Claims And Actions

- Do not change the fixed policy inside this lane.
- Do not tune rank, epsilon, solver, kernel mode, or scaling normalization
  after seeing results.
- Do not change paired thresholds after seeing results.
- Do not claim default readiness from a subset of phases.
- Do not claim HMC readiness from the gradient mechanics smoke.
- Do not rank methods using descriptive-only metrics.
- Do not detach execution or launch nested execution agents. Bounded read-only
  Claude review through the approved wrapper is the only allowed cross-agent
  exception.
- Do not modify unrelated dirty worktree changes.
- Do not commit or push.

## Skeptical Plan Audit

Wrong baseline risk: comparing only to previous Nystrom artifacts would miss
paired semantic drift. Mitigation: P01/P02 require route `both` and streaming
TF32 comparator in the same artifact.

Proxy-promotion risk: one-seed high-N and finite residuals could be misread as
default readiness. Mitigation: P01 uses replication; P04 can only recommend
human default review, not change default.

Missing stop-condition risk: a hard-veto failure could be treated as a tuning
prompt. Mitigation: this fixed-policy lane stops on hard-veto failure and
routes to a separate repair/tuning plan.

Unfair-comparison risk: changing rank/epsilon or solver mid-lane would make
the result incomparable. Mitigation: fixed-policy metadata is a hard check.

Hidden-assumption risk: full-history downstream use might be broken while
value-only artifacts pass. Mitigation: P02 explicitly runs `--history-mode
full`.

Stale-context risk: previous viability pass was not promotion evidence.
Mitigation: this lane has new subplans, ledgers, and phase artifacts.

Environment-mismatch risk: sandbox GPU failures can be misleading. Mitigation:
GPU phases require trusted GPU preflight and artifact provenance.

Artifact-mismatch risk: commands might write artifacts that do not answer the
phase question. Mitigation: every phase predeclares JSON/Markdown/log/result
paths and has a focused JSON audit.

Audit status: `PASS_FOR_P00_REVIEW`. Execution begins only after P00 local
checks and Claude read-only review converge.
