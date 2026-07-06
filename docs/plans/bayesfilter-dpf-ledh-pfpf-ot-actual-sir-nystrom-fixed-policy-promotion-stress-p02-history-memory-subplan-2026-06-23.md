# P02 Subplan: Full-History And Memory Gate

Date: 2026-06-23

## Phase Objective

Test whether the fixed Nystrom policy remains valid when the benchmark stores
full history rather than value-only outputs, while preserving paired comparator
evidence and trusted GPU provenance.

## Entry Conditions Inherited From Previous Phase

- P01 required replicated high-N rows passed.
- Fixed policy remains frozen as `rank=32,epsilon=0.5,raw,none,cholesky`.
- GPU policy remains GPU1 if available, otherwise GPU0.
- P02 may test full-history storage and memory/runtime envelope only; it may
  not tune policy or claim default readiness.

## Required Artifacts

- Benchmark JSON/Markdown/log for `N=1024,T=20`, seeds `83920,83921,83922`,
  history mode `full`:
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-full-n1024-r32-eps0p5-2026-06-23.json`
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-full-n1024-r32-eps0p5-2026-06-23.md`
  - `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-full-n1024-r32-eps0p5-2026-06-23.log`
- Optional if `N=1024` full-history passes, exits within its 15-minute timeout,
  and the trusted preflight after `N=1024` shows at least 8 GiB free memory on
  the selected GPU, benchmark JSON/Markdown/log for `N=2048,T=20`, seed
  `83920`, history mode `full`:
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-full-n2048-r32-eps0p5-2026-06-23.json`
  - `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-full-n2048-r32-eps0p5-2026-06-23.md`
  - `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-full-n2048-r32-eps0p5-2026-06-23.log`
- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-memory-result-2026-06-23.md`
- Refreshed P03 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p03-hmc-gradient-mechanics-subplan-2026-06-23.md`

## Required Checks, Tests, And Reviews

- Trusted GPU preflight with `nvidia-smi`.
- Run required full-history `N=1024` paired row.
- Run optional full-history `N=2048` row only if the required row passes, exits
  within its 15-minute timeout, and the selected GPU has at least 8 GiB free
  memory in the trusted preflight immediately before the optional row.
- JSON audit for every launched row:
  - `status == "PASS"`;
  - `hard_vetoes == []`;
  - `history_mode == "full"`;
  - fixed policy metadata matches;
  - trusted GPU/TF32 evidence present;
  - paired thresholds pass;
  - Nystrom finite factors/particles are true;
  - every route row has `history_returned is True`;
  - every route row has `filtered_means`, `filtered_variances`, and
    `ess_by_time`;
  - for required `N=1024`, `filtered_means` and `filtered_variances` have
    nested list shape `[20, 3, 18]`, and `ess_by_time` has nested list shape
    `[20, 3]`;
  - for optional `N=2048`, the same fields have nested list shape
    `[20, 1, 18]` and `[20, 1]`.
- Write P02 result with decision table, inference-status table, run manifest,
  post-run red-team note, and nonclaims.
- Refresh and locally review P03 subplan.
- Claude read-only review is required if P02 creates a material default-review
  interpretation or if full-history artifact semantics are ambiguous.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the fixed policy pass when full history is stored rather than value-only outputs? |
| Baseline/comparator | Compiled streaming TF32 actual-SIR comparator in the same artifact. |
| Primary pass criterion | Required full-history `N=1024` row passes aggregate hard-veto and paired-threshold screens with trusted GPU/TF32 evidence, fixed-policy metadata, and concrete history payload fields/shapes. Optional `N=2048` if launched must pass. If optional `N=2048` is skipped because the predeclared free-memory/runtime entry condition is not met, P02 may still pass but must record the skip as unresolved larger full-history evidence. |
| Veto diagnostics | Any hard veto, missing/malformed artifact, history-mode mismatch, missing `history_returned`, `filtered_means`, `filtered_variances`, or `ess_by_time`, wrong history field shape, GPU/TF32 evidence missing, fixed-policy metadata mismatch, nonfinite outputs, paired threshold failure, runtime timeout, memory failure. |
| Explanatory diagnostics | Memory snapshots, runtime, ESS, residual magnitudes below threshold, factor/scaling diagnostics. |
| Not concluded | No default readiness, no broad memory scalability guarantee, no HMC readiness, no posterior correctness. |
| Artifact | P02 benchmark JSON/Markdown/logs and P02 result. |

## Forbidden Claims/Actions

- Do not infer broad memory scalability from one or two rows.
- Do not tune fixed policy.
- Do not change thresholds.
- Do not claim HMC or posterior readiness.

## Exact Next-Phase Handoff Conditions

Proceed to P03 only if:

- required full-history row passes;
- any launched optional full-history row also passes;
- P02 result and P03 subplan exist;
- P03 subplan has been locally reviewed;
- no human-required stop condition fired.

## Stop Conditions

- Trusted GPU unavailable.
- Required row times out after 15 minutes. Optional `N=2048` is skipped rather
  than launched if its predeclared entry condition fails; if launched, it also
  times out after 15 minutes.
- Required artifact missing or malformed.
- Full-history payload missing or schema-incompatible.
- Any required hard-veto or paired-threshold failure.
- Continuing would require tuning, threshold changes, or default-policy
  decisions.

## Skeptical Plan Audit

The hidden assumption is that value-only success transfers to full-history
downstream use. This phase tests that assumption directly but only at bounded
row sizes. Runtime and memory are explanatory unless they become hard failures.

Audit status: `READY_AFTER_P01_PASS`.
