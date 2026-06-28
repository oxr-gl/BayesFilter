# SVD-Nystrom No-HMC Promotion Visible Stop Handoff

Date: 2026-06-26

Status: `P04C3_BLOCKED_COMPARATOR_INVALID_FOR_P04C`

Current phase: P03 closed with `P03_PASS_TO_P04_NONLINEAR_GAUSSIAN`. P04
range-bearing harness implementation and local tests passed. Claude
artifact-level review agreed. P04 seed `84000` ran on GPU1/TF32 and both routes
remained deterministic-valid, but the paired quality label used an
uncalibrated nonlinear `0.05` threshold. P04A reproduced similar deterministic
valid descriptive deltas for seed `84000`, but it inherited the same
uncalibrated threshold. P04B governance repair has now closed with
`P04B_PASS_TO_P04C_NONLINEAR_THRESHOLD_SCALE_EXTRACTION`. P04C0 repaired the
local range-bearing benchmark harness so P04C can run with
`--paired-threshold-mode record-only`: the historical uncalibrated `0.05`
paired threshold is recorded as descriptive metadata and no longer acts as a
P04C hard pass/fail gate. P04C then ran seed `84100` successfully, but seed
`84101` produced a deterministic-invalid streaming comparator artifact with
nonfinite log likelihood, filtered means, filtered variances, and ESS. P04C1
then reproduced the seed `84101` streaming nonfinite artifact under
GPU1/TF32/JIT, confirmed seed `84100` streaming passes under the same
GPU/TF32/JIT mode, confirmed the SVD-Nystrom route still passes in the seed
`84101` both-route repro, and confirmed seed `84101` streaming passes under
CPU/no-JIT/TF32-disabled mode. P04C2 then launched the first GPU TF32/no-JIT
streaming isolation row for seed `84101`, but the benchmark exited before
writing JSON/Markdown artifacts. The log reports TensorFlow
`InvalidArgumentError` from `MatrixInverse` with message `Input is not
invertible.` The active diagnostic state is
`P04C2_BLOCKED_INVALID_DIAGNOSTIC_ARTIFACT`. P04C2A then repaired the harness
artifact contract by adding explicit opt-in route exception capture while
preserving default re-raise behavior; focused tests passed. The active state is
`P04C2A_PASS_TO_P04C2_RERUN`. Repaired P04C2 reran all three GPU isolation rows
with structured exception capture. GPU TF32/no-JIT and GPU no-TF32/no-JIT
failed with structured TensorFlow `InvalidArgumentError` route exceptions at
`MatrixInverse`; GPU no-TF32/JIT failed with nonfinite route outputs. Because
the GPU no-TF32/no-JIT row failed while the P04C1 CPU no-TF32/no-JIT control
passed, P04C2 classified GPU/device streaming invalidity. P04C3 then executed a
reviewed narrow comparator robustness repair: it replaced explicit posterior
precision inverse with Cholesky solve on the same already-stabilized path and
kept jitter/stabilization policy unchanged. Focused tests passed after a
TensorArray index dtype fix, but the exact GPU/no-TF32/no-JIT canary still
failed with a structured route exception at `SelfAdjointEigV2`. The active
state is `P04C3_BLOCKED_COMPARATOR_INVALID_FOR_P04C`; P04C calibration remains
blocked pending an owner-reviewed comparator strategy plan. P05 is not eligible
until the nonlinear threshold gate is calibrated or the owner changes the
program boundary.

Safe resume point:

1. read the master program:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-master-program-2026-06-25.md`;
2. read the visible runbook:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-gated-execution-runbook-2026-06-25.md`;
3. read P00 result:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p00-governance-result-2026-06-25.md`;
4. read P01 result:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p01-scope-inventory-result-2026-06-25.md`;
5. read P02 result:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02-lgssm-reference-result-2026-06-25.md`;
6. read P02A subplan and result:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02a-gpu-tf32-svd-repair-subplan-2026-06-25.md` and
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02a-gpu-tf32-svd-repair-result-2026-06-25.md`;
7. read the P03 subplan and result:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p03-actual-sir-stress-subplan-2026-06-25.md`;
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p03-actual-sir-stress-result-2026-06-25.md`;
8. read the P04 subplan and local harness review:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-subplan-2026-06-25.md`;
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-harness-local-review-2026-06-25.md`;
9. read the P04 Claude artifact review log:
   `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-claude-review-p04-artifact-r1.log`;
10. read the P04 result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-result-2026-06-25.md`;
11. read the P04A diagnostic subplan:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04a-range-bearing-failure-diagnostic-subplan-2026-06-25.md`;
12. read the P04A Claude review log:
    `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-claude-review-p04-result-p04a-subplan-r1.log`;
13. read the P04A result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04a-range-bearing-failure-diagnostic-result-2026-06-25.md`;
14. read the final P04A Claude review log:
    `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-claude-review-p04a-result-r1.log`;
15. do not execute P05 under this runbook without explicit owner approval of a
    revised master program;
16. read the P04B threshold-governance repair subplan:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-subplan-2026-06-25.md`;
17. read the P04C nonlinear threshold scale-extraction subplan:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-subplan-2026-06-25.md`;
18. read the P04B result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-result-2026-06-25.md`;
19. read the P04C0 harness-control result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c0-harness-threshold-control-result-2026-06-26.md`;
20. read the P04C result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-result-2026-06-25.md`;
21. read the P04C1 subplan and result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-subplan-2026-06-26.md`;
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-result-2026-06-26.md`;
22. read the P04C2 draft subplan:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-subplan-2026-06-26.md`;
23. read the P04C2 result and P04C2A draft subplan:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-result-2026-06-26.md`;
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2a-harness-exception-artifact-repair-subplan-2026-06-26.md`;
24. read the P04C2A result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2a-harness-exception-artifact-repair-result-2026-06-26.md`;
25. read the repaired P04C2 result and P04C3 draft subplan:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-repaired-streaming-gpu-tf32-jit-isolation-result-2026-06-26.md`;
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c3-streaming-comparator-robustness-subplan-2026-06-26.md`;
26. read the P04C3 result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c3-streaming-comparator-robustness-result-2026-06-26.md`;
27. do not run remaining P04C calibration seeds until a separate reviewed
    calibration repair or revised calibration design authorizes it.

Open risks:

- Original P02 failed the default GPU/TF32 target: `tf.linalg.svd` on GPU/TF32
  produced nonfinite/failing route output and CUDA `gesvd` errors.
- P02A repaired diagnostic and repaired P02 rerun passed on GPU0/TF32 because
  GPU1 was saturated.
- CPU and GPU-no-TF32 diagnostics pass, but those are diagnostic only because
  the default target is GPU/TF32.
- P04 harness source review was local only because current Claude approval
  forbids Claude Code from reading source code.
- P04/P04A used an uncalibrated nonlinear `0.05` paired threshold. The row
  artifacts remain descriptive scale evidence, but their pass/fail labels must
  not be used as statistically meaningful method-failure evidence.
- P04A can diagnose reproducibility/tuning sensitivity but cannot promote the
  method, calibrate a threshold, or authorize P05 by itself.
- P04B governance repair converged. P04C0 harness threshold-control repair
  passed focused local tests. P04C row `84100` passed, but P04C row `84101`
  is deterministic-invalid because the streaming comparator is nonfinite.
  P04C stopped with no aggregate scale summary. P04C1 localizes the issue to
  GPU/TF32/JIT streaming execution but has not isolated TF32 vs JIT/XLA vs GPU
  kernel/device behavior. P04C2 could not classify the issue because the first
  row crashed before the benchmark wrote structured JSON/Markdown artifacts.
  P04C2A repaired the harness artifact contract. Repaired P04C2 then showed
  GPU/device streaming invalidity even with TF32 and JIT disabled. P04C3
  removed the original `MatrixInverse` path but did not make the GPU canary
  valid; the comparator now fails in the stabilization eigensolver path.
- Later model-suite phases may reveal missing or insufficient SVD-Nystrom
  harness coverage; that is a real blocker or repair trigger, not a reason to
  improvise claims.
- Non-LGSSM phases are no-regression/operational-viability checks, not
  absolute correctness claims.

Forbidden shortcuts:

- Do not use HMC readiness as a promotion criterion or claim it.
- Do not change default policy in code without explicit final owner approval.
- Do not tune SVD-Nystrom policy after seeing model-suite results unless a
  reviewed repair phase downgrades promotion claims.
- Do not launch P04C rows in default `gate` paired-threshold mode.
- Do not silently drop seed `84101` or treat it as a non-exceedance.
- Do not interpret P04C1 as a SVD-Nystrom rejection, threshold calibration,
  P04C repair, or P05/default-promotion authorization.
- Do not interpret the P04C2 traceback as a valid isolation classification
  until P04C2A repairs structured exception artifacts and P04C2 is rerun under
  a reviewed command contract.
- Do not interpret P04C2A as a streaming numerical repair, SVD-Nystrom quality
  result, threshold calibration, P04C resume authorization, or promotion
  evidence.
- Do not interpret repaired P04C2 as an SVD-Nystrom rejection; it is a
  streaming comparator validity blocker.
- Do not interpret P04C3 as a successful streaming comparator repair; the exact
  GPU canary remains invalid.
