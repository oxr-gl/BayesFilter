# G3 Subplan: Fixed-Policy Full-History And Memory Gate

Date: 2026-06-24

Status: `READY_AFTER_LOCAL_AUDIT`

## Phase Objective

Test whether the restricted fixed-policy Nystrom route remains valid when the
actual-SIR paired benchmark stores full history rather than value-only outputs.

This is a diagnostic gate.  It cannot promote Nystrom to default and cannot
erase the unresolved seed `82921` hard-case caveat.

## Entry Conditions Inherited From Previous Phase

- G1 closed as `G1_SPARSE_N8192_DRIFT`.
- G2 closed as `G2_DIAGNOSTIC_CONTINUE_TO_G3`.
- Fixed policy remains frozen:
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`.
- GPU policy remains trusted GPU preflight, physical GPU1 if available and
  suitable, otherwise GPU0 with fallback note.
- No tuning, threshold change, repair, or default-promotion claim is allowed in
  G3.

## Required Artifacts

Required full-history row:

- JSON:
  `docs/benchmarks/actual-sir-nystrom-g3-history-full-n1024-r32-eps0p5-2026-06-24.json`
- Markdown:
  `docs/benchmarks/actual-sir-nystrom-g3-history-full-n1024-r32-eps0p5-2026-06-24.md`
- Log:
  `docs/plans/logs/actual-sir-nystrom-g3-history-full-n1024-r32-eps0p5-2026-06-24.log`

Optional full-history row, only if the required row passes, exits within 900
seconds, and trusted preflight before optional launch shows at least 8 GiB free
memory on the selected GPU:

- JSON:
  `docs/benchmarks/actual-sir-nystrom-g3-history-full-n2048-r32-eps0p5-2026-06-24.json`
- Markdown:
  `docs/benchmarks/actual-sir-nystrom-g3-history-full-n2048-r32-eps0p5-2026-06-24.md`
- Log:
  `docs/plans/logs/actual-sir-nystrom-g3-history-full-n2048-r32-eps0p5-2026-06-24.log`

Phase result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g3-history-memory-result-2026-06-24.md`

Next subplan:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g4-gradient-mechanics-subplan-2026-06-24.md`

## Required Checks, Tests, And Reviews

Pre-run checks:

- local skeptical plan audit;
- trusted `nvidia-smi` preflight;
- select physical GPU1 if suitable, otherwise GPU0.

Required command:

- route `both`;
- `--batch-seeds 83920,83921,83922`;
- `--time-steps 20`;
- `--num-particles 1024`;
- `--history-mode full`;
- same fixed policy, transport, precision, JIT, and diagnostic settings as G1;
- timeout 900 seconds.

Optional command:

- route `both`;
- `--batch-seeds 83920`;
- `--time-steps 20`;
- `--num-particles 2048`;
- `--history-mode full`;
- same fixed policy, transport, precision, JIT, and diagnostic settings as G1;
- timeout 900 seconds.

Post-row checks:

- JSON exists and parses;
- Markdown/log exist;
- `status == "PASS"` and `hard_vetoes == []`;
- `history_mode == "full"`;
- fixed policy metadata matches;
- trusted GPU/TF32 evidence present;
- paired thresholds pass;
- Nystrom finite factors and particles are true;
- every route row has `history_returned is True`;
- every route row has `filtered_means`, `filtered_variances`, and
  `ess_by_time`;
- required `N=1024` row shapes:
  - `filtered_means`: `[20, 3, 18]`;
  - `filtered_variances`: `[20, 3, 18]`;
  - `ess_by_time`: `[20, 3]`;
- optional `N=2048` row shapes if launched:
  - `filtered_means`: `[20, 1, 18]`;
  - `filtered_variances`: `[20, 1, 18]`;
  - `ess_by_time`: `[20, 1]`.

Review:

- local review required;
- Claude read-only review optional unless history artifact semantics are
  ambiguous or G3 changes a material decision boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the fixed policy pass when full history is stored rather than value-only outputs? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Primary pass criterion | Required `N=1024` full-history row passes aggregate hard-veto, paired-threshold, metadata, finite-output, and history-shape checks. Optional `N=2048` if launched must also pass. |
| Veto diagnostics | Missing/malformed artifact, history-mode mismatch, missing history payload, wrong history shape, GPU/TF32 evidence missing, fixed-policy metadata mismatch, nonfinite outputs, residual failure, paired threshold failure, timeout, memory failure. |
| Explanatory diagnostics | Memory snapshots, runtime, ESS, residual magnitudes below threshold, factor/scaling diagnostics. |
| Not concluded | No default readiness, no broad memory scalability guarantee, no HMC readiness, no posterior correctness, no acceptance of seed `82921`. |
| Artifact | G3 JSON/Markdown/log artifacts and G3 result. |

## Forbidden Claims/Actions

- Do not infer broad memory scalability from one or two rows.
- Do not tune fixed policy.
- Do not change thresholds.
- Do not claim default readiness, HMC readiness, posterior correctness, or
  acceptance of seed `82921`.

## Exact Next-Phase Handoff Conditions

- `G3_HISTORY_MEMORY_PASS`: required row passes, any launched optional row
  passes, result exists, and G4 subplan is drafted and locally reviewed.
- `G3_HISTORY_MEMORY_SCOPE_LIMIT`: required row passes but optional row is
  skipped by predeclared memory/runtime preflight; continue only with optional
  larger-history evidence marked unresolved.
- `G3_HISTORY_MEMORY_FAIL`: required row fails or artifact checks fail; write
  blocker/result and return to G2 scope decision or repair planning.

## Stop Conditions

- Trusted GPU unavailable.
- Required row times out after 900 seconds.
- Required artifact missing or malformed.
- Full-history payload missing or schema-incompatible.
- Any hard-veto or paired-threshold failure on a launched row.
- Continuing would require tuning, threshold changes, repair, or default-policy
  decisions.

## Skeptical Plan Audit

The hidden assumption is that value-only success transfers to full-history
downstream use.  G3 tests that assumption directly at bounded row sizes.
Runtime and memory are explanatory unless they become hard failures.  Passing G3
would not establish broad memory scalability, default readiness, HMC readiness,
posterior correctness, or acceptance of seed `82921`.

Audit status: `PASS_FOR_G3_LAUNCH_AFTER_LOCAL_CHECKS`.
