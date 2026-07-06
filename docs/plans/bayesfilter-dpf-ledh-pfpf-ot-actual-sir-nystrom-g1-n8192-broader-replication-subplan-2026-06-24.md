# G1 Subplan: Broader N8192 Fixed-Policy Replication

Date: 2026-06-24

Status: `READY_AFTER_LOCAL_AUDIT`

## Phase Objective

Run a broader `N=8192` actual-SIR fixed-policy seed panel to classify whether
the known paired drift is repeated enough to justify repair selection, or sparse
enough to require an explicit scope/fallback decision instead of immediate
tuning.

## Entry Conditions Inherited From Previous Phase

- G0 governance plan exists and classifies current Nystrom evidence gaps.
- Current fixed policy is frozen:
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`.
- Known seed `82921` failure is accepted as real and reproducible.
- Seeds `82922` and `82923` previously passed; G1 does not rerun them.
- No repair, tuning, threshold change, or default-promotion claim is allowed in
  G1.
- GPU policy: trusted GPU preflight, physical GPU1 if available and suitable,
  otherwise physical GPU0 with fallback note.

## Required Artifacts

For each seed `82924..82931`:

- JSON:
  `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed<SEED>-r32-eps0p5-2026-06-24.json`
- Markdown:
  `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed<SEED>-r32-eps0p5-2026-06-24.md`
- Log:
  `docs/plans/logs/actual-sir-nystrom-g1-n8192-broader-replication-seed<SEED>-r32-eps0p5-2026-06-24.log`

Phase result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-result-2026-06-24.md`

Next subplan or blocker:

- G2 repair-selection or scope-decision subplan, to be drafted after G1 result.

## Required Checks, Tests, And Reviews

Pre-run checks:

- local skeptical plan audit;
- trusted `nvidia-smi` preflight;
- select physical GPU1 if suitable, otherwise GPU0;
- verify the benchmark harness exists and the command template matches prior
  compiled-redo N8192 rows.

Per-row command requirements:

- route `both`;
- `--batch-seeds <one seed>`;
- `--time-steps 20`;
- `--num-particles 8192`;
- `--transport-policy active-all`;
- `--sinkhorn-iterations 10`;
- `--sinkhorn-epsilon 1.0`;
- `--annealed-scaling 0.9`;
- `--annealed-convergence-threshold 0.001`;
- `--row-chunk-size 1024`;
- `--col-chunk-size 1024`;
- `--particle-chunk-size 1024`;
- `--nystrom-diagnostics`;
- `--nystrom-rank 32`;
- `--nystrom-epsilon 0.5`;
- `--nystrom-max-iterations 160`;
- `--nystrom-convergence-threshold 0.0001`;
- `--nystrom-kernel-mode raw`;
- `--nystrom-scaling-normalization none`;
- `--history-mode value-only`;
- `--warmups 0`;
- `--repeats 1`;
- `--dtype float32`;
- `--tf32-mode enabled`;
- `--jit-compile`;
- `--device-scope visible`;
- `--device /GPU:0`;
- `--expect-device-kind gpu`;
- timeout 900 seconds per row.

Post-row checks:

- JSON exists and parses;
- Markdown exists;
- top-level `batch_seeds` matches the seed;
- `shape.time_steps == 20` and `shape.num_particles == 8192`;
- `route_request == "both"`;
- `history_mode == "value-only"`;
- `precision.dtype == "float32"`;
- `precision.tf32_execution_enabled is True`;
- `run_manifest.selected_physical_gpu_argument` matches selected physical GPU;
- `transport.nystrom_rank == 32`;
- `transport.nystrom_epsilon == 0.5`;
- `transport.nystrom_kernel_mode == "raw"`;
- `transport.nystrom_scaling_normalization == "none"`;
- `transport.nystrom_core_solver == "cholesky"`;
- streaming row exists and status is `PASS`;
- Nystrom row exists, has finite outputs, and records finite factors/particles;
- aggregate paired max and mean deltas are recorded;
- aggregate hard vetoes are classified.

Review:

- local review required after all artifacts or on first blocker;
- Claude read-only review is optional unless G1 opens a material repair/scope
  boundary or local review finds a material ambiguity.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | How many of the next eight `N=8192` one-seed rows fail fixed-policy paired thresholds under the unchanged policy? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Primary classification criterion | Count new paired-threshold failures among valid seeds `82924..82931`, after artifact validity checks. |
| Veto diagnostics | Missing/malformed artifact, wrong policy, missing trusted GPU/TF32 evidence, comparator failure, Nystrom nonfinite outputs/factors/particles, residual hard veto, timeout. |
| Explanatory only | Runtime, warm ratio, ESS, residual magnitudes below threshold, paired delta magnitudes, denominator/factor/scaling diagnostics. |
| Not concluded | No statistical failure probability, no default readiness, no ranking, no HMC readiness, no posterior correctness, no dense Sinkhorn equivalence. |
| Artifact | G1 JSON/Markdown/logs, this subplan, execution ledger, and G1 result. |

## Forbidden Claims/Actions

- Do not tune rank, epsilon, solver, thresholds, chunks, model, or seeds after
  seeing G1 results.
- Do not treat eight one-seed rows as a statistical estimate.
- Do not claim default-readiness from G1, even if all rows pass.
- Do not launch repair until G1 handoff explicitly opens a repair lane.
- Do not use old quarantined Python-loop timings as ranking evidence.

## Exact Next-Phase Handoff Conditions

- `G1_REPEATED_N8192_DRIFT`: at least two of eight new seeds fail paired mean or
  max thresholds, or any fixed-policy nonfinite/residual veto appears.  Draft
  G2 repair-selection subplan.
- `G1_SPARSE_N8192_DRIFT`: zero or one of eight new seeds fails paired
  thresholds and no artifact/harness/numerical veto appears.  Draft G2
  scope/fallback decision subplan; do not promote.
- `G1_HARNESS_OR_ENV_BLOCKER`: wrong comparator, malformed artifact, missing
  metadata, trusted GPU failure, timeout, or threshold drift.  Stop and write a
  blocker result before interpreting numbers.

## Stop Conditions

- Trusted GPU unavailable.
- Any row times out after 900 seconds.
- Required artifact missing or malformed.
- Fixed-policy metadata mismatch.
- Streaming comparator failure.
- Continuing would require tuning, threshold changes, or a default-policy
  decision.

## Skeptical Plan Audit

Wrong baseline is controlled by paired route `both` and same-artifact compiled
streaming comparator.  Proxy-promotion is controlled because runtime, ESS, and
residual magnitudes below threshold are explanatory only.  Stop conditions are
explicit.  Comparison fairness is controlled by fixed seeds, model, dtype, TF32,
transport policy, chunk sizes, route request, and policy metadata.  Stale
context is controlled by excluding the quarantined Python-loop timing artifacts.
The command artifacts answer the stated G1 question because each one-seed row
preserves paired thresholds and policy metadata.

Audit status: `PASS_FOR_G1_LAUNCH_AFTER_LOCAL_CHECKS`.
