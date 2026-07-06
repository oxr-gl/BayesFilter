# P03 Subplan: Actual-SIR Stress Replication

Date: 2026-06-25

Status: `P03_READY_FOR_LOCAL_AND_CLAUDE_REVIEW`

## Phase Objective

Stress the fixed SVD-Nystrom policy on actual-SIR beyond the P06 threshold
validation panel, using a same-shape fresh-seed panel under the same
statistical discipline.

## Entry Conditions Inherited From Previous Phase

- P02 repaired exact-reference gate emitted
  `P02_PASS_REPAIRED_PENDING_REVIEW_TO_P03_ACTUAL_SIR_STRESS`.
- Material repair review converged and the execution ledger records
  `P02_REPAIR_REVIEW_AGREE_PASS_TO_P03_ACTUAL_SIR_STRESS`.
- Candidate policy remains locked.
- P06 seeds `82968..82981` are not reused as fresh stress evidence.
- P03 uses the compiled-redo harness
  `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`, not the
  older Python-loop default-promotion harness.

## Required Artifacts

- Per-row JSON/Markdown/log artifacts must be exactly the seed-specific paths
  listed in the P03 per-row artifact manifest below. No wildcard, alternate
  directory, alternate prefix, or unlisted row artifact may be used for P03
  evidence.
- Aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-summary-2026-06-25.json`
- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p03-actual-sir-stress-result-2026-06-25.md`
- Refreshed P04 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-subplan-2026-06-25.md`

## Required Checks, Tests, And Reviews

- Trusted GPU preflight; freeze selected physical GPU for the panel.
- Predeclare stress seeds/shapes and statistical gate before execution.
- Run one row at a time and parse artifacts after every row.
- Verify deterministic validity, SVD metadata, GPU/TF32 provenance, finite
  outputs, residual thresholds, and bounded paired-delta screen.
- Local review and Claude read-only review are required before executing P03
  because this phase can support or reject the actual-SIR stress gate.

## Frozen P03 Panel

| Quantity | Value |
| --- | --- |
| Harness | `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` |
| Shape | `T=20`, `N=8192`, `state_dim=18`, `obs_dim=9` |
| Initial fresh stress seeds | `83000..83013` (`14` seeds) |
| Reserved extension seeds | `83014..83029` (`16` seeds), only if initial panel is inconclusive |
| Forbidden prior seeds | `82920..82950`, `82962..82981` |
| Candidate | `rank=32`, `epsilon=0.5`, `kernel_mode=raw`, `scaling_normalization=none`, `core_solver=svd_truncated`, `core_rcond=1e-6` |
| Threshold | `tau_component=0.03`, so `tau_total=20*9*0.03=5.4` |
| Deterministic Nystrom residual thresholds | `max_row_residual <= 5.0e-2` and `max_column_residual <= 5.0e-2`, inherited from `benchmark_actual_sir_nystrom_compiled_redo.py` field names and `NYSTROM_RESIDUAL_THRESHOLD` |
| Deterministic log-weight threshold | Nystrom row `final_logsumexp_residual <= 1.0e-5`, inherited from the prior threshold-calibration contract |
| Statistical rule | One-sided 95% Clopper-Pearson upper bound for `Pr(abs(delta)/(T*M)>0.03) <= 0.20` |

## P03 Per-Row Artifact Manifest

Only the following per-row artifact paths are valid for P03. Initial-panel rows
are seeds `83000..83013`; reserved-extension rows are seeds `83014..83029` and
may be launched only under the frozen extension rule.

| Seed | Panel | JSON artifact | Markdown artifact | Log artifact |
| --- | --- | --- | --- | --- |
| 83000 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83000-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83000-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83000-r32-eps0p5.log` |
| 83001 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83001-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83001-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83001-r32-eps0p5.log` |
| 83002 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83002-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83002-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83002-r32-eps0p5.log` |
| 83003 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83003-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83003-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83003-r32-eps0p5.log` |
| 83004 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83004-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83004-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83004-r32-eps0p5.log` |
| 83005 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83005-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83005-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83005-r32-eps0p5.log` |
| 83006 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83006-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83006-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83006-r32-eps0p5.log` |
| 83007 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83007-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83007-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83007-r32-eps0p5.log` |
| 83008 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83008-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83008-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83008-r32-eps0p5.log` |
| 83009 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83009-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83009-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83009-r32-eps0p5.log` |
| 83010 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83010-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83010-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83010-r32-eps0p5.log` |
| 83011 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83011-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83011-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83011-r32-eps0p5.log` |
| 83012 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83012-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83012-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83012-r32-eps0p5.log` |
| 83013 | initial | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83013-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83013-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83013-r32-eps0p5.log` |
| 83014 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83014-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83014-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83014-r32-eps0p5.log` |
| 83015 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83015-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83015-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83015-r32-eps0p5.log` |
| 83016 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83016-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83016-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83016-r32-eps0p5.log` |
| 83017 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83017-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83017-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83017-r32-eps0p5.log` |
| 83018 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83018-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83018-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83018-r32-eps0p5.log` |
| 83019 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83019-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83019-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83019-r32-eps0p5.log` |
| 83020 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83020-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83020-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83020-r32-eps0p5.log` |
| 83021 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83021-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83021-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83021-r32-eps0p5.log` |
| 83022 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83022-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83022-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83022-r32-eps0p5.log` |
| 83023 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83023-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83023-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83023-r32-eps0p5.log` |
| 83024 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83024-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83024-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83024-r32-eps0p5.log` |
| 83025 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83025-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83025-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83025-r32-eps0p5.log` |
| 83026 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83026-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83026-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83026-r32-eps0p5.log` |
| 83027 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83027-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83027-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83027-r32-eps0p5.log` |
| 83028 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83028-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83028-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83028-r32-eps0p5.log` |
| 83029 | reserved | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83029-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83029-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83029-r32-eps0p5.log` |

Initial panel rule:

- If all 14 initial deterministic-valid rows have zero exceedances, P03 passes
  the statistical stress screen because the one-sided 95% CP upper bound is
  below `0.20`.
- If the initial panel has one or two exceedances and no deterministic vetoes,
  continue to reserved extension seeds until 30 total deterministic-valid rows
  are complete or a third exceedance occurs.
- Stop for futility if total exceedances reaches three, because `3/30` cannot
  pass the frozen `0.20` CP upper-bound gate.
- Do not declare an early statistical pass from interim extension looks.

Per-row command rule:

For each launched row, `SEED` must be one of the manifest seeds, `GPU` must be
the trusted selected physical GPU, and the output, Markdown, and log paths must
be the exact manifest row for that seed. The command path mapping is:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds ${SEED} --time-steps 20 --num-particles 8192 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P03-ACTUAL-SIR-STRESS-SEED${SEED} --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed${SEED}-r32-eps0p5-2026-06-25.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed${SEED}-r32-eps0p5-2026-06-25.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed${SEED}-r32-eps0p5.log 2>&1
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does fixed SVD-Nystrom remain viable on fresh actual-SIR stress rows beyond P06? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Primary criterion | Deterministic validity and one-sided 95% CP upper bound for `Pr(abs(delta)/(T*M)>0.03)` is `<=0.20`. |
| Veto diagnostics | Deterministic invalidity, seed reuse, GPU/TF32 mismatch, shape/policy mismatch, missing SVD metadata, malformed artifacts, `max_row_residual > 5.0e-2`, `max_column_residual > 5.0e-2`, `final_logsumexp_residual > 1.0e-5`, or third-exceedance futility. |
| Explanatory diagnostics | Runtime, memory, normalized deltas, residuals, ESS/factor/core diagnostics. |
| Not concluded | No non-actual-SIR validity, no default promotion, no posterior correctness, no statistical superiority, no HMC readiness. |
| Artifact | P03 aggregate summary and result. |

## Forbidden Claims And Actions

- Do not change `tau_component=0.03` post hoc.
- Do not reuse P06 validation seeds for fresh evidence.
- Do not use the older Python-loop default-promotion harness for P03 evidence.
- Do not rank SVD against cholesky without a paired uncertainty design.
- Do not claim promotion from actual-SIR alone.

## Exact Next-Phase Handoff Conditions

- `P03_PASS_TO_P04_NONLINEAR_GAUSSIAN`: stress gate passes and P04 subplan
  reviewed.
- `P03_FAIL_OPTIONAL_OR_REPAIR`: deterministic validity passes but statistical
  stress gate fails.
- `P03_DETERMINISTIC_BLOCKER`: artifact/GPU/metadata/numerical validity fails.

## Stop Conditions

- P02 did not emit `P02_PASS_REPAIRED_PENDING_REVIEW_TO_P03_ACTUAL_SIR_STRESS`.
- Material repair review has not converged to the post-review handoff token
  `P02_REPAIR_REVIEW_AGREE_PASS_TO_P03_ACTUAL_SIR_STRESS`.
- Seed overlap with P06 or tuning panels.
- Third-exceedance/futility rule or equivalent predeclared statistical veto.
- Trusted GPU unavailable.
- Missing required artifacts.
- Any need to change threshold, shape, candidate policy, dtype, TF32 mode,
  harness, or default-policy scope.

## Local Self-Review Of Next Subplan

Skeptical audit:

- Wrong baseline: P03 uses same-artifact compiled streaming TF32 actual-SIR as
  a value-route comparator, not a truth oracle.
- Proxy metric: normalized log-likelihood deltas are the predeclared bounded
  value-route screen only, not posterior correctness or promotion.
- Missing stop conditions: deterministic validity, seed overlap, malformed
  artifacts, GPU/TF32 mismatch, policy mismatch, third exceedance, and scope
  changes are stops.
- Unfair comparison: shape, seeds, dtype, TF32 mode, transport policy, SVD
  policy, and selected physical GPU are fixed for included rows.
- Hidden assumption: passing P03 only supports actual-SIR stress viability; it
  does not replace P04-P08.
- Artifact fit: per-row JSON/Markdown/logs plus aggregate summary and P03
  result answer the stated question.

P04 checks a different nonlinear Gaussian fixture so actual-SIR stress does not
silently become broad model evidence.
