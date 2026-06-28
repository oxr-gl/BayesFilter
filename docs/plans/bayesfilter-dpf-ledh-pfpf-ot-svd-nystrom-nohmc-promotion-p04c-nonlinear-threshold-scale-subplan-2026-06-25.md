# P04C Subplan: Nonlinear Threshold Scale Extraction

Date: 2026-06-25

Status: `P04C_READY_FOR_SCALE_EXTRACTION_PREFLIGHT_AFTER_HARNESS_REPAIR`

## Phase Objective

Extract descriptive nonlinear range-bearing paired-delta scale evidence under
the fixed SVD-Nystrom policy so a later reviewed phase can freeze a principled
threshold. P04C must not validate, reject, promote, or freeze a threshold. It
exists to prevent another post-hoc `0.05` style gate.

## Entry Conditions Inherited From Previous Phase

- P04B must emit
  `P04B_PASS_TO_P04C_NONLINEAR_THRESHOLD_SCALE_EXTRACTION`.
- P04/P04A are reclassified as uncalibrated threshold-governance evidence.
- Existing seed `84000` and its P04A control rows are descriptive historical
  evidence only and may not be used as future validation evidence.
- Candidate policy remains the fixed SVD-Nystrom policy unless a separate
  owner-approved repair/candidate-freeze lane is opened.
- P05 remains blocked.
- No HMC readiness claim is in scope.

## Required Artifacts

- P04C subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-subplan-2026-06-25.md`
- P04C result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-result-2026-06-25.md`
- P04C aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-summary-2026-06-25.json`
- P04C per-seed JSON/Markdown/log artifacts listed in the manifest below.
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04d-nonlinear-threshold-freeze-subplan-2026-06-25.md`

## Required Checks, Tests, And Reviews

- Before GPU rows:
  - Verify P04B result emitted the exact P04C handoff token.
  - Verify the benchmark command will not treat the old `0.05` threshold as a
    calibrated P04C pass/fail gate. If the current harness still hardcodes
    `0.05` as a hard paired veto, stop and implement/review a local harness
    control before scale extraction.
  - Verify calibration seeds are disjoint from seed `84000` and from planned
    validation seeds.
  - Verify exact artifact paths exist in this subplan and do not rely on
    wildcards.
- Trusted GPU preflight immediately before rows; use GPU1 if suitable,
  otherwise GPU0.
- Run rows one at a time and parse each JSON before launching the next row.
- Deterministic route validity must pass for a row to enter scale extraction:
  finite outputs, route/policy metadata, GPU/TF32 provenance, no dense
  materialization, residual/log-weight/ESS checks pass.
- P04C may use only pre-existing harness-defined deterministic-validity checks
  recorded in the row artifacts. It must not invent new row-rejection rules
  after seeing outputs.
- P04C result must report descriptive mean, median, q80, q90, q95, max,
  exceedance counts for candidate margins considered only as descriptive
  summaries, and explicit uncertainty limitations.
- Candidate margin summaries may be drafted for later human/Claude review in
  P04D, but no candidate margin is approved, validated, or frozen in P04C.
- Claude read-only review is required before P04D threshold freeze. Claude may
  review P04C result, summary, P04D subplan, and same-prefix artifacts only.
  Claude may not read source code or authorize a threshold by itself.

## Calibration Panel

P04C uses a fixed-observation range-bearing fixture and varies the particle
seed only. That means the descriptive scale is conditional on the fixture
observation path, not broad nonlinear validity.

| Quantity | Value |
| --- | --- |
| Fixture | `range_bearing_gaussian_moderate` |
| Shape | `T=20`, `N=4096`, `state_dim=4`, `obs_dim=2` |
| Calibration seeds | `84100..84111` (`12` seeds) |
| Reserved validation seeds | `84200..84219` (`20` seeds), not executable in P04C |
| Candidate | `rank=32`, `epsilon=0.5`, `kernel_mode=raw`, `scaling_normalization=none`, `core_solver=svd_truncated`, `core_rcond=1e-6` |
| Comparator | Same-artifact compiled streaming TF32 DPF route |
| Threshold status | No threshold frozen in P04C |
| Statistical role | Descriptive scale extraction only |

The historical P04/P04A seed `84000` rows may be shown as context, but P04C
must compute freeze candidates from the P04C calibration panel separately.

## Panel Eligibility And Invalid-Row Handling

P04C is deliberately conservative because it follows a threshold-governance
repair. The pass-to-P04D scale summary requires all 12 planned calibration
seeds `84100..84111` to produce deterministic-valid row artifacts under the
pre-existing harness-defined deterministic-validity checks.

No reduced-panel pass is allowed in P04C. If any planned calibration row is
missing, malformed, deterministic-invalid, GPU/TF32 mismatched, route/policy
mismatched, or rejected by a new non-predeclared rule, P04C must emit
`P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT` and stop for a separate
harness/fixture diagnostic or revised subplan. Deterministic-invalid rows must
not be counted as non-exceedances or silently excluded from descriptive
quantiles.

## P04C Per-Row Artifact Manifest

Only the following artifacts are valid for P04C.

| Seed | JSON artifact | Markdown artifact | Log artifact |
| ---: | --- | --- | --- |
| 84100 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84100-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84100-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84100-r32-eps0p5.log` |
| 84101 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84101-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84101-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84101-r32-eps0p5.log` |
| 84102 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84102-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84102-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84102-r32-eps0p5.log` |
| 84103 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84103-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84103-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84103-r32-eps0p5.log` |
| 84104 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84104-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84104-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84104-r32-eps0p5.log` |
| 84105 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84105-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84105-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84105-r32-eps0p5.log` |
| 84106 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84106-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84106-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84106-r32-eps0p5.log` |
| 84107 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84107-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84107-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84107-r32-eps0p5.log` |
| 84108 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84108-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84108-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84108-r32-eps0p5.log` |
| 84109 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84109-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84109-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84109-r32-eps0p5.log` |
| 84110 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84110-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84110-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84110-r32-eps0p5.log` |
| 84111 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84111-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84111-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84111-r32-eps0p5.log` |

## Per-Row Command Shape

The command shape below uses `--paired-threshold-mode record-only` so the
historical `0.05` paired threshold is recorded as descriptive metadata and
cannot act as a P04C hard pass/fail gate. `${GPU}` and `${GPU_NOTE}` must come
from the immediately preceding trusted GPU preflight.

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route both --seed ${SEED} --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --paired-threshold-mode record-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04C-RANGE-BEARING-SCALE-SEED${SEED} --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed${SEED}-r32-eps0p5-2026-06-25.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed${SEED}-r32-eps0p5-2026-06-25.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed${SEED}-r32-eps0p5.log 2>&1
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the descriptive paired-delta scale for fixed SVD-Nystrom on the range-bearing fixture under deterministic-valid GPU/TF32 rows? |
| Baseline/comparator | Same-artifact compiled streaming TF32 DPF route. |
| Primary criterion | Produce a deterministic-valid calibration summary on all 12 planned disjoint calibration seeds, without freezing or validating a threshold. |
| Veto diagnostics | Missing/unavailable record-only paired-threshold mode, historical `0.05` still acting as P04C pass/fail, deterministic invalidity, malformed/missing artifact, GPU/TF32 mismatch, route/policy mismatch, dense materialization, residual/log-weight/ESS failure, seed overlap with validation, or unsupported claim. |
| Explanatory diagnostics | Observed normalized deltas, descriptive quantiles, runtime, memory, residuals, ESS, factor/core diagnostics. |
| Not concluded | No calibrated threshold, no P04 pass/fail, no default promotion, no posterior correctness, no HMC readiness, no statistical superiority, no broad nonlinear validity. |
| Artifact | P04C aggregate summary and result. |

## Forbidden Claims And Actions

- Do not freeze `tau_component`.
- Do not validate or reject SVD-Nystrom based on P04C.
- Do not rank SVD-Nystrom as superior or inferior from descriptive deltas.
- Do not count seed `84000` or any P04C calibration seed as future validation.
- Do not launch P05.
- Do not change candidate policy, fixture, shape, dtype, TF32 target, or seed
  split after seeing results.
- Do not send source code or tests to Claude without explicit approval.

## Exact Next-Phase Handoff Conditions

- `P04C_PASS_TO_P04D_NONLINEAR_THRESHOLD_FREEZE`: all 12 planned calibration
  rows are deterministic-valid under pre-existing harness-defined checks,
  artifacts parse, seed splits are intact, descriptive candidate margin
  summaries are labeled unapproved/unvalidated/unfrozen, and P04D is drafted
  for a reviewed threshold freeze.
- `P04C_BLOCKED_HARNESS_THRESHOLD_CONTROL_REQUIRED`: the harness cannot execute
  P04C in record-only paired-threshold mode, or it still treats `0.05` as an
  active hard P04C gate and needs a local code/test repair before scale
  extraction.
- `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`: required artifacts are missing,
  malformed, deterministic-invalid, or have GPU/TF32/route/policy mismatch.

## Stop Conditions

- P04B has not closed with the exact P04C handoff.
- The benchmark cannot run scale extraction with paired deltas in record-only
  mode, or still uses the old `0.05` as a hard pass/fail gate.
- Trusted GPU unavailable.
- Any planned calibration row is deterministic-invalid, malformed, missing, or
  excluded by a non-predeclared rule.
- Any need arises to alter the seed split, candidate policy, fixture, shape,
  dtype, TF32 mode, or threshold after seeing P04C results.
- Continuing would require P05 execution, threshold freeze, default-policy
  change, source-code disclosure to Claude, package installation, network
  fetches, commits, pushes, or destructive actions.

## End-Of-Phase Requirements

At P04C close, Codex must:

1. run required local checks;
2. write the P04C result/close record;
3. draft or refresh P04D;
4. review P04D locally and, for material threshold-freeze issues, with Claude;
5. update ledgers and stop handoff.

## Local Self-Review Of This Subplan

Skeptical audit:

- Wrong baseline: same-artifact streaming DPF remains the comparator.
- Proxy metric: paired deltas are descriptive scale evidence only in P04C.
- Missing stop conditions: hardcoded threshold, invalid artifacts, GPU/TF32
  mismatch, seed overlap, and post-hoc threshold/candidate changes are stops.
- Unfair comparison: fixed fixture, shape, dtype, TF32 target, comparator, and
  candidate.
- Hidden assumption: seed variation is particle-seed variation under one fixed
  observation path, not broad nonlinear-model uncertainty.
- Environment mismatch: trusted GPU preflight is required before rows.
- Artifact fit: exact per-row and aggregate paths are predeclared.

Audit status: `PASS_AFTER_P04C0_HARNESS_CONTROL_REPAIR_FOR_PREFLIGHT`.
