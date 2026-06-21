# LEDH-PFPF-OT Large-Particle Efficiency Claude Review Ledger

Date: 2026-06-21

Status: CONVERGED_FOR_P03

Claude is a read-only reviewer only. Claude cannot authorize human, runtime,
model-file, funding, product-capability, or scientific-claim boundary crossings.

## Review Rounds

### Round 1

Reviewer: Claude Code worker `large-particle-efficiency-plan-review-r1`

Verdict: `VERDICT: REVISE`

Material findings:

- Missing numeric visible-run budget and optional-rung decision rule.
- GPU1/GPU0 busy or unsuitable rule was underspecified.
- Parent selected-physical-GPU metadata was required from child artifacts even
  though the child harness only records remapped `CUDA_VISIBLE_DEVICES` and
  logical devices.
- Dense context interpretation exceeded the older dense harness artifact
  surface.
- Some wording risked claiming full LEDH-filter operational readiness rather
  than LGSSM-shaped benchmark feasibility.
- P01 test selector needed to be deliberately added.

Repair:

- Patched the master program, runbook, P01, P02, P03, P04, P05, and P06
  subplans to address all findings.

Status: awaiting round 2 review.

### Round 2

Reviewer: Claude Code worker `large-particle-efficiency-plan-review-r2`

Verdict: `VERDICT: AGREE`

Summary:

- Confirmed numeric P03/P04 runtime budgets and optional/downgrade rules.
- Confirmed mechanical GPU1/GPU0 busy-or-unsuitable thresholds.
- Confirmed parent-vs-child GPU metadata distinction.
- Confirmed dense-context artifact limitation.
- Confirmed LGSSM-shaped benchmark claim boundary.
- Confirmed deliberate `large_particle_efficiency` test selector.

Status: converged.

### GPU Selection Rule Repair

Trigger: user identified the previous "any unrelated compute process" GPU
selection veto as a planning error after GPU1 showed only light usage
(`453 MiB / 32760 MiB`, `3%` utilization, one Python process using `430 MiB`).

Patch:

- A GPU is now busy/unsuitable if total memory used is at least 2048 MiB,
  utilization is at least 20%, or any single non-display compute process uses at
  least 2048 MiB.
- Light non-display compute below those thresholds is a recorded shared-GPU
  warning, not a hard veto.

Status: awaiting focused review.

### GPU Selection Rule Repair Review

Reviewer: Claude Code worker `large-particle-gpu-rule-repair-review`

Verdict: `VERDICT: AGREE`

Summary:

- Confirmed the repaired GPU1/GPU0 threshold rule is internally consistent
  across the master program, P02 subplan/result, and visible runbook.
- Confirmed current trusted GPU1 evidence (`18 MiB / 32760 MiB`, `0%`
  utilization, no listed compute apps) is usable under the repaired rule.
- Confirmed GPU0 fallback remains forbidden unless GPU1 is threshold-busy or
  unsuitable.
- Confirmed `CUDA_VISIBLE_DEVICES=1` with child logical `/GPU:0` is the correct
  parent/child mapping statement.

Status: converged for P03 launch.

### P03 GPU Lease/Contamination Repair Review

Reviewer: Claude Code worker `large-particle-p03-gpu-lease-review`

Verdict: `VERDICT: AGREE`

Summary:

- Confirmed the repair distinguishes P02 GPU selection from a durable GPU
  lease.
- Confirmed P03 now requires just-in-time uncontaminated selected-GPU checks
  before launch and during startup/rungs.
- Confirmed peer-lane independence is preserved: stop only this lane's launched
  processes unless the user explicitly approves broader process control.
- Confirmed partial artifacts are downgraded to contaminated diagnostic-only
  evidence and cannot support runtime, memory-efficiency, TF32, or scalability
  claims.

Status: P03 repair converged; rerun remains gated on a clean selected GPU.
