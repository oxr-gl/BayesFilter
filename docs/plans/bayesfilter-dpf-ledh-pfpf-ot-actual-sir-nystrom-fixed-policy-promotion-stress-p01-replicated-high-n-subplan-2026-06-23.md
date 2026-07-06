# P01 Subplan: Replicated High-N Gate

Date: 2026-06-23

## Phase Objective

Run replicated high-N actual-SIR paired benchmark rows for the fixed Nystrom
policy, using trusted GPU evidence and the compiled streaming TF32 comparator
in each artifact.

## Entry Conditions Inherited From Previous Phase

- P00 governance and Claude read-only review converged.
- Fixed policy is frozen as `rank=32,epsilon=0.5,raw,none,cholesky`.
- GPU policy: use physical GPU1 if available and suitable, otherwise GPU0.
- No P01 row may tune policy, change thresholds, or claim default readiness.

## Required Artifacts

- Benchmark JSON/Markdown/log for `N=2048`, seeds `82921,82922,82923`:
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.json`
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.md`
  - `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.log`
- Benchmark JSON/Markdown/log for `N=4096`, seeds `82921,82922,82923`:
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.json`
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.md`
  - `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.log`
- Optional, only if the two required rows pass, each required row exits within
  its 15-minute timeout, and the trusted preflight after `N=4096` shows at
  least 8 GiB free memory on the selected GPU, benchmark JSON/Markdown/log for
  `N=8192`, seed `82921`:
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.json`
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.md`
  - `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.log`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-result-2026-06-23.md`
- Refreshed P02 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-memory-subplan-2026-06-23.md`

## Required Checks, Tests, And Reviews

- Trusted GPU preflight with `nvidia-smi`.
- Select GPU1 if usable/available, otherwise GPU0; record
  `--selected-physical-gpu` and `--gpu-selection-note`.
- Run the required `N=2048` and `N=4096` paired benchmark rows with
  `--history-mode value-only`.
- Run the optional `N=8192` one-seed row only if the required rows pass, each
  required row exits within its 15-minute timeout, and the selected GPU has at
  least 8 GiB free memory in the trusted preflight immediately before the
  optional row.
- JSON audit for every launched row:
  - `status == "PASS"`;
  - `hard_vetoes == []`;
  - `history_mode == "value-only"`;
  - fixed policy metadata matches `rank=32`, `epsilon=0.5`, raw kernel, no
    scaling normalization, cholesky solver;
  - `precision.tf32_execution_enabled is True`;
  - GPU output evidence is present;
  - paired max log-likelihood delta <= `10.0`;
  - paired mean log-likelihood delta <= `5.0`;
  - Nystrom finite factors and finite particles are true.
- Write P01 result with decision table, inference-status table, run manifest,
  post-run red-team note, and nonclaims.
- Refresh P02 subplan and review it locally for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.
- Claude review is required only if P01 result interpretation affects
  promotion/default-review classification or if a material plan boundary issue
  appears.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the fixed policy pass replicated high-N hard screens beyond the earlier one-seed ladder? |
| Baseline/comparator | Compiled streaming TF32 actual-SIR comparator in the same paired artifact. |
| Primary pass criterion | Required `N=2048` and `N=4096` rows pass aggregate hard-veto and paired-threshold screens with trusted GPU/TF32 evidence and fixed-policy metadata. Optional `N=8192` if launched must also pass, or P01 is blocked/failed according to its hard-veto status. If optional `N=8192` is skipped because the predeclared free-memory/runtime entry condition is not met, P01 may still pass but must record the skip as unresolved high-N stress evidence. |
| Veto diagnostics | Any aggregate hard veto, missing artifact, malformed JSON, trusted GPU/TF32 evidence missing, fixed-policy metadata mismatch, nonfinite outputs, residual threshold failure, paired threshold failure, runtime timeout. |
| Explanatory diagnostics | Runtime, memory snapshots, ESS, residual magnitudes below threshold, denominator/factor/scaling diagnostics, warm timing ratio. |
| Not concluded | No default readiness, no statistical superiority/ranking, no posterior correctness, no HMC readiness, no broad rank/epsilon robustness. |
| Artifact | P01 benchmark JSON/Markdown/logs and P01 result. |

## Forbidden Claims/Actions

- Do not tune after seeing P01 results.
- Do not change thresholds.
- Do not call runtime or ESS a promotion criterion.
- Do not claim default readiness from P01 alone.
- Do not advance if required rows fail or artifacts are invalid.

## Exact Next-Phase Handoff Conditions

Proceed to P02 only if:

- P01 required rows pass;
- any launched optional row also passes;
- P01 result exists and records commands, artifacts, diagnostics, and
  nonclaims;
- P02 subplan is refreshed and locally reviewed;
- no human-required stop condition fired.

If a valid fixed-policy candidate failure occurs with complete artifacts, write
P01 result and route to P04 closeout classification rather than tuning in P01.

## Stop Conditions

- Trusted GPU unavailable.
- Required row times out after 15 minutes. Optional `N=8192` is skipped rather
  than launched if its predeclared entry condition fails; if launched, it also
  times out after 15 minutes.
- Required artifact missing or malformed.
- Any required hard-veto or paired-threshold failure.
- Fixed-policy metadata mismatch.
- Continuing would require tuning, threshold changes, or default-policy
  decisions.

## Skeptical Plan Audit

Wrong baseline is controlled by paired route `both`. Proxy-promotion is
controlled by treating P01 as a hard screen only. Unfair comparison is
controlled by fixed metadata checks. Environment mismatch is controlled by
trusted GPU preflight and artifact device evidence.

Audit status: `READY_AFTER_P00_PASS`.
