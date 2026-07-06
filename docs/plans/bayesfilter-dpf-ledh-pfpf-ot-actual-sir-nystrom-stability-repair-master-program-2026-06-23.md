# Actual-SIR Nystrom Stability Repair Master Program

Date: 2026-06-23

Status: `READY_FOR_VISIBLE_GATED_LAUNCH_AFTER_REVIEW`

## Purpose

This master program systematically investigates why the compiled Nystrom route
became nonfinite in P09 around `rank=32,epsilon=0.25` and
`rank=64,epsilon=0.3`, while `rank=32,epsilon=0.5` remained viable.

This is a repair and diagnosis program.  It does not promote Nystrom to a
default route and does not reject the Nystrom direction.

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.  Claude may inspect files and report
findings, but it may not edit files, run experiments, launch agents, approve
crossing boundaries, change criteria, or authorize scientific/product claims.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Where does the Nystrom nonfinite failure originate, and which smallest repair class can make the failing rows finite without breaking the viable control? |
| Candidate mechanism | Existing compiled fixed-rank Nystrom transport plus diagnostic/repair variants for factor/scaling numerics. |
| Known failing rows | `rank=32,epsilon=0.25`; `rank=64,epsilon=0.3` at `B=5,T=20,N=1024,D=18,M=9`, seeds `81920..81924`. |
| Control row | `rank=32,epsilon=0.5` at the same shape/seeds. |
| Baseline/comparator | Compiled streaming TF32 actual-SIR route in `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` when paired quality is tested. |
| Expected failure modes | Core conditioning, factor diagonal/sign defects, Sinkhorn denominator collapse, scale mismatch, landmark pathology, precision/TF32 sensitivity, or unsupported narrow policy region. |
| Promotion criterion | None in this program.  A repair may only reopen P09/P10 gates under the promotion runbook. |
| Promotion veto | Any statement that a diagnostic pass proves default readiness, superiority, posterior correctness, HMC readiness, or broad policy stability. |
| Continuation veto | Invalid artifact, implementation test failure, trusted GPU unavailable for required GPU phase, Claude/Codex review non-convergence after five rounds for the same blocker, or a human direction decision not already in this program. |
| Repair trigger | Diagnostics localize a fixable failure source; a subplan/test/review finds an implementation or artifact defect; a planned repair fails but exposes a smaller discriminating next check. |
| Explanatory diagnostics | Spectra, condition proxies, factor diagonals, denominator minima/hits, first nonfinite location, timing, memory, and per-seed/per-time summaries unless promoted by a subplan. |
| What must not be concluded | No default readiness, no statistical ranking, no dense Sinkhorn equivalence, no posterior correctness, no HMC readiness, no proof that Nystrom is broadly robust or unusable. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we localize and repair the P09 Nystrom nonfinite failure using gated diagnostics rather than uncontrolled tuning? |
| Exact baseline | Existing P09/P09B/P09C/P09D artifacts and the compiled streaming TF32 comparator for paired repair validation. |
| Primary pass criterion | Each phase writes required artifacts, passes local checks, has no forbidden claim, and reaches explicit handoff conditions. |
| Veto diagnostics | Nonfinite outputs in a repair-validation row, missing artifact, missing trusted GPU/TF32 evidence for GPU phases, stale/quarantined evidence, changed criteria after results, or unsupported scientific/default claim. |
| Explanatory-only diagnostics | Runtime, warm ratios, spectra without a predeclared threshold, one-seed probes, and single-run descriptive differences. |
| Not concluded | This program cannot by itself promote default policy or rank methods. |
| Artifacts | Subplans/results under `docs/plans/*nystrom-stability-repair-*`, benchmark JSON/Markdown under `docs/benchmarks/*nystrom-stability-repair-*`, and logs under `docs/plans/logs/`. |

## Skeptical Plan Audit

Status: `PASS_FOR_VISIBLE_GATED_REPAIR_PROGRAM`

- Wrong baseline risk: paired validation continues to use the compiled streaming
  TF32 actual-SIR route, not old Python-loop timing artifacts.
- Proxy metric risk: spectra, denominator stats, and timing are diagnostic
  until a subplan declares a hard veto threshold.
- Missing stop conditions: every phase has explicit stop and handoff conditions.
- Unfair comparison risk: paired repair-validation rows keep shape, seeds,
  dtype, TF32 state, transport policy, and GPU protocol fixed.
- Hidden assumptions: GPU1 preference with GPU0 fallback is recorded per GPU
  artifact; Claude is read-only and not execution authority.
- Stale context: P09D showed SVD core solve did not rescue; this program targets
  factor/scaling/landmark/scale diagnostics before further tuning.
- Environment mismatch: GPU/CUDA work must run in trusted context.
- Artifact mismatch: each phase result must cite exact JSON/Markdown/log paths.

## Phase Index

| Phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| P00 | Program review and launch gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-program-review-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-program-review-result-2026-06-23.md` |
| P01 | Instrumentation implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p01-instrumentation-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p01-instrumentation-result-2026-06-23.md` |
| P02 | Failure localization diagnostics | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-result-2026-06-23.md` |
| P03 | Minimal one-change ablations | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-minimal-ablations-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-minimal-ablations-result-2026-06-23.md` |
| P04 | Repair candidate selection | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-result-2026-06-23.md` |
| P05 | Focused repair implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-result-2026-06-23.md` |
| P06 | P09 repair gate and decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-result-2026-06-23.md` |
| P07 | Closeout handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p07-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p07-closeout-result-2026-06-23.md` |

## Phase Flow

1. P00 reviews the master program, visible runbook, and P01 subplan with local
   checks plus Claude read-only review.
2. P01 adds diagnostics without changing default behavior.
3. P02 runs the failing rows and control to locate the first nonfinite source.
4. P03 runs minimal one-change ablations selected by P02.
5. P04 chooses one focused repair class or blocks with evidence.
6. P05 implements only the selected focused repair and runs local checks.
7. P06 reruns the P09 repair gate on failing rows plus control.
8. P07 writes final handoff and updates the promotion runbook.

## Repair Loop Protocol

For each phase:

1. Read the subplan and record the evidence contract in the ledger.
2. Run required local checks before material execution.
3. Execute only the phase's allowed actions.
4. Write a phase result or blocker record.
5. Draft or refresh the next subplan.
6. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
7. For material issues, request Claude read-only review at Opus/max effort.
8. If review finds a fixable problem, patch the same subplan visibly and rerun
   focused checks.
9. Stop after five Claude review rounds for the same blocker.
10. Continue automatically to the next phase only when the current subplan's
    exact handoff conditions are met.

## Anticipated Trusted Commands

- Claude read-only review: `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --model opus --effort max ...`
- GPU preflight: `nvidia-smi --query-gpu=index,name,memory.used,utilization.gpu --format=csv,noheader,nounits`
- GPU TensorFlow diagnostics: `/home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/...`

No package install, network fetch, destructive git command, detached supervisor,
or default-policy change is authorized by this master program.

## Required GPU Run Manifest

Every GPU or CUDA-initializing phase artifact must preserve, either directly in
the benchmark JSON or in the phase result:

- git commit and `git status --short`;
- exact command;
- conda/Python executable and TensorFlow version when applicable;
- CUDA visibility, selected physical GPU, and GPU selection note;
- trusted `nvidia-smi` preflight summary;
- dtype, TF32 state, and JIT state;
- seeds, shape, model/data row, and transport policy;
- stdout/stderr log path and structured artifact path;
- wall time and exit status.
