# Actual-SIR Low-Rank N3072 Second-Candidate Validation Review Ledger

Date: 2026-06-23

Status: `EXECUTION_PASS_RESULT_WRITTEN_NEXT_SUBPLAN_DRAFTED`

## Entry-Condition Anchors

- N2048 minimal-rank validation result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-minimal-rank-validation-result-2026-06-23.md`
- N2048 seed-replication result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-seed-replication-result-2026-06-23.md`
- N2048 consolidation/resource-decision result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-consolidation-resource-decision-result-2026-06-23.md`
- N3072 representative resource-smoke result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-result-2026-06-23.md`
- N3072 resource-boundary closeout result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-resource-boundary-closeout-result-2026-06-23.md`
- Human approval: user message after the N3072 resource-boundary closeout,
  `yesI approve`.

## Pre-Review Local Checks

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `18 passed`.
- `n3072-second-candidate-subplan-static-check`
  - Result: pass.
- Exact dry-run for `r16_eps0p125_alpha1em08_it120`
  - Result: pass.
  - Row JSON basename bytes: `254`.
  - Row Markdown basename bytes: `252`.
  - Row log basename bytes: `253`.

## Round 1

Reviewer: Claude Opus/max, read-only.

Scope:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-subplan-2026-06-23.md`

Verdict: `VERDICT: REVISE`

Material findings:

- Commands passed `--low-rank-assignment-epsilons 0.25,0.125` even though the
  phase is exact second-candidate-only.
- Warm-time screen was a phase-defining pass/fail screen even though the phase
  objective is bounded N3072 completion with valid artifacts/provenance.
- Entry-condition traceability needed exact prior artifact pointers.

Patch:

- Dry-run and execution commands now pass only
  `--low-rank-assignment-epsilons 0.125`.
- Warm-time screen is now descriptive/resource-triage evidence only and no
  longer a promotion veto or primary pass criterion.
- This ledger now includes exact entry-condition anchors and the human approval
  note.

Focused checks after patch:

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `18 passed`.
- `n3072-second-candidate-r1-patch-static-check`
  - Result: pass.
- Exact second-candidate dry-run after the patch:
  - Result: pass.
  - Command used `--candidate-ids r16_eps0p125_alpha1em08_it120`.
  - Command used `--low-rank-assignment-epsilons 0.125`.
  - Row JSON basename bytes: `254`.
  - Row Markdown basename bytes: `252`.
  - Row log basename bytes: `253`.

## Round 2 Supporting Review

Reviewer: Claude Sonnet/high, read-only.

Scope:

- Focused R2 sanity review of the patched subplan and this ledger.

Verdict: `VERDICT: AGREE`

Note:

- This review was useful supporting context but did not satisfy the requested
  Opus/max reviewer model. The Opus/max review below is the authority for
  subplan-review convergence.

Material findings:

- Exact second-candidate-only filtering is consistent across the objective,
  dry-run checks, evidence contract, commands, and stop conditions.
- Warm timing is consistently descriptive/resource-triage evidence only.
- Prior artifact and approval anchors are explicit enough for traceability.
- Boundary safety is intact: no forbidden ranking, speedup, default/API/HMC,
  posterior, dense-equivalence, scientific-production, or NumPy backend drift
  claim/action was found.

Residual risks:

- Preserve the exact transcript approval reference verbatim in the later
  result note.
- Artifact basenames remain close to the `255` byte ceiling; any name growth
  requires a fresh dry-run/path-length check.

## Round 2 Opus/Max Review

Reviewer: Claude Opus/max, read-only.

Scope:

- Focused R2 review of the patched subplan and this ledger.
- Checked only the R1 fixes and boundary safety before execution.

Verdict: `VERDICT: AGREE`

Material findings:

- Exact second-candidate-only filtering is consistent end-to-end:
  `r16_eps0p125_alpha1em08_it120` with epsilon `0.125` only.
- Warm timing is correctly demoted out of phase pass/fail and promotion-veto
  status and is now descriptive/resource-triage only.
- Exact prior artifact and approval anchors are present in this ledger and are
  sufficient for this review scope.
- Boundary safety is preserved: no NumPy backend drift, no forbidden ranking,
  speedup, default/API/HMC/posterior/dense-equivalence/scientific-production
  claims, and Claude remains read-only reviewer only.

Residual risks:

- The human approval anchor is conversational rather than file-backed; preserve
  the exact reference in the result note.
- Runtime correctness still depends on the runner honoring the filtered row at
  execution time; the specified dry-run and artifact-path checks are the
  correct guardrails.

Convergence:

- `SUBPLAN_REVIEW_CONVERGED` for the N3072 second-candidate validation phase.

## Pre-Execution Gate

Timestamp: `2026-06-23T21:51:05+08:00`

Skeptical audit refresh:

- Result: pass.
- Reason: the subplan is still bounded to one exact second-candidate row, uses
  the paired streaming comparator from the same run, treats warm timing only as
  descriptive/resource-triage evidence, has explicit stop conditions, preserves
  no-NumPy implementation and forbidden-claim boundaries, and has converged
  Opus/max read-only review.

Trusted GPU precheck:

- Command:
  `nvidia-smi --query-gpu=index,name,uuid,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits`
- Result:
  - GPU 0: `1493 / 32760 MiB`, utilization `39%`.
  - GPU 1: `18 / 32760 MiB`, utilization `0%`.
- Process snapshot: `nvidia-smi pmon -c 1` showed display/session processes on
  GPU 0 and only `Xorg` on GPU 1.
- Decision: GPU 1 is suitable for the bounded run using
  `--cuda-visible-devices 1 --device /GPU:0`.

Refreshed dry-run:

- Command: the subplan dry-run command with output paths under `/tmp`.
- Result: pass.
- Aggregate keys present: `algorithm_under_test`, `execution_policy`, `grid`,
  `harness_path`, `mode`, `nonclaims`, `plan_path`, `rows`, `run_manifest`,
  `schema_version`, `shape`, `status`, `summary`.
- Summary: `num_candidates=1`, labels `{DRY_RUN: 1}`.
- Row count: `1`.
- Exact candidate id: `r16_eps0p125_alpha1em08_it120`.
- Exact assignment epsilon: `0.125`.
- Exact seeds: `81137,81138`.
- Exact shape: batch `2`, time steps `20`, particles `3072`.
- Command includes `--cuda-visible-devices 1`, `--device /GPU:0`,
  `--expect-device-kind gpu`, `--jit-compile`, compiled-core timing, TF32
  enabled, and route `both`.
- Row JSON basename bytes: `254`.
- Row Markdown basename bytes: `252`.
- Row log basename bytes: `253`.

Execution gate:

- `READY_TO_EXECUTE_N3072_SECOND_CANDIDATE_ROW`.

## Execution And Close Record

Execution command:

- `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81137,81138 --time-steps 20 --num-particles 3072 --low-rank-ranks 16 --low-rank-assignment-epsilons 0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p125_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 7200 --output docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.md --quiet`

Execution result:

- Aggregate status: `PASS`.
- Summary: `num_candidates=1`, `num_freeze_nominated=1`.
- Exact candidate id: `r16_eps0p125_alpha1em08_it120`.
- Exact assignment epsilon: `0.125`.
- Exact seeds: `81137,81138`.
- Exact shape: batch `2`, time steps `20`, particles `3072`.
- Row status: `PASS`.
- Row hard vetoes: `[]`.
- Actual-SIR semantics pass: `true`.
- Paired comparability diagnostics were within the row artifact thresholds.
- Selected GPU: GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID
  `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`.
- GPU/XLA/TF32 provenance: present; `jit_compile=True`, TF32 enabled,
  TensorFlow `2.20.0`, logical GPU `/device:GPU:0`, requested
  `CUDA_VISIBLE_DEVICES=1`.
- Row wall time: `386.48628454096615s`.
- Row JSON basename bytes: `255`.
- Row Markdown basename bytes: `253`.
- Row log basename bytes: `254`.
- Trusted post-run GPU check at `2026-06-23T22:03:14+08:00`: GPU 1 returned
  to `18 / 32760 MiB`, utilization `0%`.

Close artifacts:

- Result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-result-2026-06-23.md`
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-two-row-consolidation-resource-boundary-subplan-2026-06-23.md`

Claim boundary:

- This execution supports only the bounded second-candidate N3072 row pass.
  Warm ratio, wall time, and memory snapshots remain descriptive/resource-triage
  diagnostics only. No speedup, ranking, posterior-correctness, HMC-readiness,
  dense-equivalence, default/API readiness, N4096 feasibility, formal
  memory-scaling, production-readiness, scientific-validity, or
  other-candidate invalidity claim is made.
