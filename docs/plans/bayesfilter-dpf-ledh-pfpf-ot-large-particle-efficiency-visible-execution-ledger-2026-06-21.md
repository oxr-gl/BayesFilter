# LEDH-PFPF-OT Large-Particle Efficiency Visible Execution Ledger

Date: 2026-06-21

Status: STARTED

## Ledger

### 2026-06-21 - P00 - PRECHECK

Evidence contract:

- Question: Can current GPU TF32 streaming LEDH-PFPF-OT make the LGSSM-shaped
  LEDH-PFPF-OT benchmark operational at large particle counts by avoiding dense
  storage, and does TF32 show descriptive same-route runtime benefit?
- Baseline/comparator: streaming FP32+TF32 default for reach; streaming
  FP32-no-TF32 same-route comparator for runtime; dense/non-streaming only
  small-`N` context.
- Primary criterion: required streaming ladder rungs pass hard
  finite/device/storage/default-metadata gates in trusted GPU context.
- Veto diagnostics: non-finite output, CPU fallback, OOM/timeout, missing
  artifacts, dense matrix materialized, full pre-flow storage,
  `return_history=True`, wrong metadata, or unrecorded GPU policy violation.
- Nonclaims: no posterior correctness, no HMC readiness, no statistical
  ranking, no dense Sinkhorn equivalence, and no public API readiness.

Actions:

- Created draft master program, phase subplans, visible runbook, review ledger,
  execution ledger, and stop handoff.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-master-program-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-gated-execution-runbook-2026-06-21.md`

Gate status:

- IN_PROGRESS

Next action:

- Run local content checks and Claude read-only review.

### 2026-06-21 - P00 - REVIEW_R1_REPAIR

Evidence contract:

- Same as P00 precheck.

Actions:

- Claude read-only review round 1 returned `VERDICT: REVISE`.
- Patched the reviewed plan set to define numeric P03/P04 runtime budgets,
  mechanical GPU1/GPU0 busy thresholds, parent-vs-child GPU metadata contract,
  dense-context artifact limitations, and LGSSM-shaped benchmark claim
  boundaries.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-master-program-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-gated-execution-runbook-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p01-harness-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p02-gpu-selection-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-ladder-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-runtime-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-context-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p06-closeout-subplan-2026-06-21.md`

Gate status:

- IN_PROGRESS

Next action:

- Rerun local content checks and request Claude read-only review round 2.

### 2026-06-21 - P00 - PASSED

Evidence contract:

- Question: Is the proposed large-particle efficiency program scoped to answer
  LGSSM-shaped operational large-`N` benchmark scalability without overclaiming?
- Baseline/comparator: streaming GPU TF32 default for reach;
  FP32-no-TF32 same-route runtime comparator; dense small-`N` context only.
- Primary criterion: governance artifacts exist, required fields are present,
  and Claude/Codex review has no unresolved material blocker.
- Veto diagnostics: wrong baseline, proxy promotion, missing stop condition,
  unfair comparison, hidden assumption, environment mismatch, unsupported
  claim, or artifact mismatch.
- Nonclaims: no implementation correctness, no large-`N` pass, no runtime
  benefit, no posterior correctness, no HMC readiness.

Actions:

- Claude review round 2 returned `VERDICT: AGREE`.
- Wrote P00 governance result.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p00-governance-result-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-claude-review-ledger-2026-06-21.md`

Gate status:

- PASSED

Next action:

- Begin P01 harness implementation and focused local checks.

### 2026-06-21 - P01 - PASSED

Evidence contract:

- Question: Does the parent wrapper preserve large-`N` streaming TF32/FP32
  evidence without introducing a misleading comparator or artifact gap?
- Baseline/comparator: wrapper delegates to existing child harnesses and does
  not implement filter math.
- Primary criterion: py_compile, focused tiny CPU test, and static invariant
  scan pass.
- Veto diagnostics: missing artifact path, stdout flood, in-process TensorFlow
  arm reuse, missing invariant check, wrong child harness, or overclaiming
  runtime.
- Nonclaims: no GPU viability, no large-`N` pass, no TF32 benefit, no posterior
  correctness.

Actions:

- Added large-particle efficiency parent wrapper.
- Added focused tiny CPU pytest selected by `-k large_particle_efficiency`.
- Ran required P01 checks.

Artifacts:

- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_large_particle_efficiency.py`
- `tests/test_experimental_batched_benchmark_harness.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p01-harness-result-2026-06-21.md`

Gate status:

- PASSED

Next action:

- Begin P02 trusted GPU selection preflight.

### 2026-06-21 - P02 - BLOCKED

Evidence contract:

- Question: Which trusted physical GPU should the visible run use, and is the
  choice compliant with user policy?
- Baseline/comparator: GPU1 is preferred; GPU0 fallback only if GPU1 is
  busy/unsuitable and GPU0 is usable.
- Primary criterion: trusted `nvidia-smi` succeeds and selected physical GPU
  plus threshold-based reason is recorded.
- Veto diagnostics: both GPUs busy/unsuitable.
- Nonclaims: no benchmark success, no runtime comparison, no device correctness
  beyond preflight.

Actions:

- Ran trusted `nvidia-smi` GPU status query.
- Ran trusted `nvidia-smi` compute-app query.
- Ran `ps` checks for active GPU process classification.
- Wrote P02 blocker result.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p02-gpu-selection-result-2026-06-21.md`

Gate status:

- BLOCKED

Next action:

- Ask user whether to wait/rerun P02, override the busy-GPU rule, or stop/pause
  the unrelated workload.

### 2026-06-21 - P02 - REPAIR_PLAN

Evidence contract:

- Question: Was the prior P02 stop caused by a valid hardware contention veto
  or by an over-conservative planning rule?
- Baseline/comparator: GPU1 preferred; GPU0 fallback only when GPU1 is
  threshold-busy/unsuitable.
- Primary criterion: GPU busy rule must distinguish light shared-GPU warnings
  from hard launch vetoes.
- Veto diagnostics: total memory at least 2048 MiB, utilization at least 20%,
  or any single non-display compute process using at least 2048 MiB.
- Nonclaims: no GPU benchmark pass yet.

Actions:

- User identified the previous process-presence veto as a planning error.
- Patched the GPU policy so light non-display compute below threshold is a
  recorded warning rather than an automatic stop.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-master-program-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p02-gpu-selection-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-gated-execution-runbook-2026-06-21.md`

Gate status:

- IN_PROGRESS

Next action:

- Get focused Claude read-only review of the repaired GPU-selection rule, then
  rerun P02.

### 2026-06-21 - P02 - PASSED_AFTER_REPAIR

Evidence contract:

- Question: Which trusted physical GPU should the visible run use after
  repairing the over-conservative busy-GPU rule?
- Baseline/comparator: GPU1 preferred; GPU0 fallback only when GPU1 is
  threshold-busy/unsuitable.
- Primary criterion: trusted `nvidia-smi` succeeds and selected physical GPU
  plus threshold reason is recorded.
- Veto diagnostics: GPU1 absent, total memory used at least 2048 MiB,
  utilization at least 20%, any single non-display compute process using at
  least 2048 MiB, or both GPUs threshold-busy/unsuitable.
- Nonclaims: no large-`N` GPU pass, no TF32 runtime benefit, no algorithmic
  scalability verdict.

Trusted evidence:

- GPU0: 1226 MiB / 32760 MiB, 28% utilization, display/remoting compute apps.
- GPU1: 18 MiB / 32760 MiB, 0% utilization, no listed compute apps.

Actions:

- Superseded the stale P02 blocker result.
- Selected physical GPU1 for P03.
- Recorded child mapping: `CUDA_VISIBLE_DEVICES=1`; expected child logical
  device `/GPU:0`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p02-gpu-selection-result-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-stop-handoff-2026-06-21.md`

Gate status:

- PASSED_AFTER_REPAIR

Next action:

- Run focused Claude read-only review of the repaired GPU-selection boundary
  and then launch P03 if review agrees.

### 2026-06-21 - P03 - INTERRUPTED_CONTAMINATED

Evidence contract:

- Question: Can P03 launch a timing/memory-sensitive large-`N` streaming ladder
  on the selected physical GPU without unrelated GPU compute contamination?
- Baseline/comparator: selected physical GPU1 from P02.
- Primary criterion: mandatory rungs must run on selected GPU with hard gates
  and without unrelated compute sharing the selected GPU.
- Veto diagnostics: unrelated compute process on selected GPU during P03 before
  mandatory rungs complete.
- Nonclaims: no P03 large-`N` pass, no runtime/memory-efficiency evidence, no
  TF32 benefit, no algorithmic scalability verdict from this interrupted run.

Actions:

- Launched P03 on physical GPU1 with `CUDA_VISIBLE_DEVICES=1`.
- Monitoring showed a peer low-rank GPU job also running on physical GPU1:
  `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode paired-gpu`.
- Stopped only this lane's P03 parent/child processes.
- Preserved completed child artifacts as contaminated diagnostic-only evidence.

Artifacts:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-children-2026-06-21/streaming_tf32_n1000.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-children-2026-06-21/streaming_tf32_n5000.json`

Gate status:

- INTERRUPTED_CONTAMINATED

Repair:

- Patch P03 and the master/runbook with a just-in-time GPU lease/contamination
  gate. P02 remains a selection gate, not a durable GPU reservation.

Next action:

- Write P03 interrupted result, review the P03 repair, then rerun only when the
  selected GPU is uncontaminated at launch and during startup.

### 2026-06-21 - P04 - PRE-RUN SKEPTICAL AUDIT

Evidence contract:

- Question: At matched `N=10000` large-particle shape, is the production
  default FP32+TF32 streaming route descriptively faster than the same FP32
  streaming route with TF32 disabled?
- Baseline/comparator: same-route FP32 with TF32 disabled.
- Candidate: same-route FP32 with TF32 enabled.
- Primary criterion: both arms pass finite/device/storage/precision hard gates
  and produce matched-shape timing summaries.
- Veto diagnostics: failed arm, mismatched shape/config other than TF32 mode,
  CPU fallback, non-finite output, dense transport storage, full pre-flow
  storage, missing artifact, wrong TF32 metadata, or selected-GPU
  contamination.
- Explanatory diagnostics: warm-call median, compile plus first-call time, GPU
  memory metadata, and timing ratio.
- Nonclaims: no statistical speedup claim, no dense-vs-streaming speed verdict,
  no posterior correctness, no HMC readiness, no public API readiness.

Skeptical audit:

- Wrong baseline check: pass. P04 uses FP32 with TF32 disabled as the same-route
  comparator, not FP64 or dense/non-streaming.
- Proxy metric check: pass. Timing ratio is descriptive only.
- Stop-condition check: pass. Hard-gate failures, mismatched route/config, GPU
  fallback, and contamination remain vetoes.
- Artifact-answer check: pass. The parent wrapper emits P04 JSON/Markdown plus
  child artifacts for both arms.
- Environment check: pass. Trusted preflight showed physical GPU1 at 18 MiB
  used, 0% utilization, and no listed compute apps; child commands must use
  `CUDA_VISIBLE_DEVICES=1`.

Gate status:

- AUDIT_PASSED_READY_TO_RUN

### 2026-06-21 - P04 - PASSED

Execution:

- Ran P04 on physical GPU1 with `CUDA_VISIBLE_DEVICES=1`.
- Parent wall time: `79.41282888804562` seconds.
- Both child arms passed hard finite/device/storage/precision gates.

Artifacts:

- Parent JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.json`
- Parent Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.md`
- Child directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-children-2026-06-21/`
- Result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-runtime-result-2026-06-21.md`

Results:

- TF32 enabled warm median: `11.870695133926347` seconds.
- TF32 disabled warm median: `12.24538614996709` seconds.
- Warm-median ratio `enabled / disabled`: `0.9694014536208195`.
- Interpretation: descriptive only; no statistical speedup claim.

Checks:

- `py_compile` passed for the P04 parent wrapper and streaming child harness.
- JSON hard-gate audit passed for both arms.

Gate status:

- PASSED

Next-subplan review:

- P05 subplan reviewed for consistency, correctness, feasibility, artifact
  coverage, and boundary safety.
- Review result: consistent if P05 remains context-only. P05 must not run large
  dense jobs to force OOM and must not treat small-`N` dense timing as a
  large-`N` speed ranking.

### 2026-06-21 - P05 - SKIPPED JUSTIFIED

Decision:

- Skipped P05 dense breakpoint context because it was explicitly contextual and
  not required to certify the streaming GPU TF32 route for the large-particle
  storage/capacity question.

Artifact:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-context-result-2026-06-21.md`

Gate status:

- SKIPPED_JUSTIFIED

### 2026-06-21 - P06 - CERTIFIED ACCEPTABLE DEFAULT

Decision:

- Certified GPU streaming TF32 LEDH-PFPF-OT as the acceptable default
  operational route for BayesFilter DPF LEDH-PFPF-OT work whenever GPU
  execution and the streaming fixed-branch contract are applicable.

Evidence:

- P03 clean GPU1 large-particle ladder passed mandatory `N=1000`, `5000`, and
  `10000`; optional `N=20000` also passed.
- P03 avoided dense transport matrix storage, full pre-flow particle storage,
  and history output.
- P04 same-route `N=10000` TF32-on/off comparison passed hard gates; TF32-on
  warm-median ratio was `0.9694014536208195`, descriptive only.

Artifact:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p06-closeout-result-2026-06-21.md`

Nonclaims:

- No posterior correctness, dense Sinkhorn equivalence, HMC readiness, public
  API readiness, or statistical speedup claim.

Gate status:

- CERTIFIED_ACCEPTABLE_DEFAULT
