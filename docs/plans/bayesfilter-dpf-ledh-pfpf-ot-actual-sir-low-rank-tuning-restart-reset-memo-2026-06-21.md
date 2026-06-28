# Actual-SIR Low-Rank Tuning Restart Reset Memo

Date: 2026-06-21
Timestamp: 2026-06-21T16:25:00+08:00

## Reset Status

The actual-SIR low-rank validation lane stopped at:

`TUNING_REQUIRED`

This is a clean restart memo for continuing the test SIR model work. The next
program should tune the low-rank solver route on the actual-SIR d18 workload
before any renewed promotion, speed, or large-N claim.

## Core Finding

The prior actual-SIR lane applied the existing low-rank solver route to the
real actual-SIR d18 workload without an actual-SIR-specific tuning phase.

The first required paired GPU row ran successfully at the hard-validity level:

- row: `B=5,T=20,N=1024`, seeds `81120,81121,81122,81123,81124`;
- GPU: GPU1, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`;
- TF32: enabled;
- finite outputs: pass;
- low-rank factors: finite/nonnegative, positive `g`;
- no dense transport matrix materialization.

But the current low-rank configuration failed the actual-SIR support gates:

| Gate | Observed | Required |
| --- | ---: | ---: |
| Warm median `streaming / low_rank` | `0.016606596042173186` | `>= 1.25` |
| Log-likelihood max absolute delta | `58.0933837890625` | `<= 10.0` |
| Log-likelihood mean absolute delta | `42.93328857421875` | `<= 5.0` |

Interpretation: this rejects promotion of the current configured candidate,
not the low-rank research direction. The likely next hypothesis is tuning or
route repair, not scientific impossibility.

## Evidence Anchors

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-result-2026-06-21.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-visible-stop-handoff-2026-06-21.md`
- P03 aggregate:
  `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21.json`
- P03 attempted row:
  `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json`
- Actual-SIR validation harness:
  `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
- Existing low-rank route:
  `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- Synthetic/proxy low-rank efficiency result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-result-2026-06-21.md`

## What Went Wrong

The previous actual-SIR program correctly asked the real-workload question, but
it did not insert a tuning phase before applying the existing low-rank
configuration to the real actual-SIR row.

The default actual-SIR low-rank parameters were:

- `rank=64`;
- `assignment_epsilon=0.015625`;
- `alpha=1e-8`;
- `max_projection_iterations=240`;
- `convergence_threshold=1e-6`;
- `denominator_floor=1e-30`.

Those settings were not selected by an actual-SIR tuning screen. Prior positive
low-rank evidence came from a synthetic/proxy LEDH/PFPF-OT benchmark and does
not transfer automatically to actual-SIR d18.

## Restart Research Intent

| Field | Contract |
| --- | --- |
| Main question | Can a tuned low-rank solver route make actual-SIR d18 LEDH/PFPF-OT more efficient at large particle counts while preserving predeclared engineering comparability? |
| Candidate | Existing TensorFlow low-rank route, with actual-SIR-specific tuning of exposed parameters. |
| Comparator | Existing compiled streaming actual-SIR TF32/GPU route from `benchmark_p8j_tf32_batched_actual_sir.py` through the owned validation harness. |
| Tuning target | Actual-SIR d18 rows only; no proxy-only promotion. |
| Promotion criterion | A frozen tuned candidate must pass held-out paired actual-SIR rows with hard validity, paired comparability, same physical GPU UUID, TF32 provenance, and predeclared warm-time support. |
| Promotion veto | Nonfinite outputs, invalid factors, dense materialization, missing actual-SIR semantics, route-fired mismatch, paired comparability failure on support rows, or speed screen failure. |
| Continuation veto | Shared contract/API change, package install/network/POT, trusted GPU unavailable for GPU evidence, corrupted artifacts, or inability to preserve evidence answering the question. |
| Repair trigger | Tuning rows show finite valid factors but fail comparability or speed in a parameter-dependent way. |
| Not concluded | No posterior correctness, HMC readiness, public API/default/production readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or statistical ranking. |

## Tuning Parameters

The restart should tune only parameters already exposed by the actual-SIR
validation harness unless a reviewed subplan explicitly authorizes a route
repair.

Primary tuning knobs:

- `low_rank_rank`: start with a bounded grid such as `16,32,64,128`, respecting
  `rank <= N`;
- `low_rank_assignment_epsilon`: tune over a coarse log/scale grid, for example
  `0.25,0.125,0.0625,0.03125,0.015625`;
- `low_rank_alpha`: tune only within the constraint `alpha * rank < 1`;
- `low_rank_max_projection_iterations`: test whether `120,240,480` changes
  factor residual, comparability, or time;
- `low_rank_convergence_threshold`: test only if projection iterations hit the
  cap or residuals are near threshold;
- `low_rank_denominator_floor`: keep fixed unless nonfinite/floor diagnostics
  show it is active.

Potential route-repair knobs requiring a separate reviewed implementation plan:

- deterministic landmark selection strategy;
- cost scaling or whitening before assignment-kernel construction;
- adaptive rank schedule by `N` or by actual-SIR state spread;
- a compiled/graph implementation of the low-rank loop if eager overhead is
  the dominant cost after comparability is fixed.

## Required Restart Structure

The next program should not jump directly to `N=50000` or `N=100000`.

Recommended phases:

| Phase | Objective | Key artifact |
| ---: | --- | --- |
| P00 | Governance, skeptical audit, and evidence contract | master program plus subplans |
| P01 | Harness/tuning-grid readiness | focused tests and CLI checks |
| P02 | Tiny actual-SIR tuning smoke | CPU-hidden or small GPU rows proving grid execution |
| P03 | Actual-SIR tuning screen | tuning aggregate with candidate viability labels |
| P04 | Freeze one or more candidates before holdout | frozen-candidate record |
| P05 | Held-out paired actual-SIR support ladder | paired GPU aggregate |
| P06 | Large-N envelope only if P05 passes | low-rank-only or paired large-N artifacts |
| P07 | Closeout and claim classification | final result and stop handoff |

## Tuning Discipline

The restart must separate tuning evidence from promotion evidence.

- Tuning rows may nominate a candidate but cannot promote it.
- The final tuned candidate must be frozen before held-out support rows.
- The failed prior row `B=5,T=20,N=1024` may be reused as a regression row, but
  promotion should include at least one held-out paired shape/seed set not used
  to choose parameters.
- Runtime/memory may guide tuning, but promotion still requires hard validity
  and paired comparability first.
- If a tuning candidate improves speed but fails paired comparability, it is
  not promotable.
- If a tuning candidate improves comparability but remains slower than compiled
  streaming, it may justify route repair, not promotion.

## Suggested Initial Tuning Rows

Use the same actual-SIR semantics as the prior harness.

Cheap screens:

- `B=1,T=3,N=128`, one or two seeds;
- `B=1,T=20,N=256`, one or two seeds;
- `B=2,T=20,N=512`, two seeds if runtime permits.

First support/holdout rows after freezing:

- `B=5,T=20,N=1024`, seeds held out or partly held out from tuning;
- `B=5,T=20,N=4096`, only if `N=1024` passes;
- larger rows only after two adjacent paired support rows pass.

GPU policy:

- Use GPU1 unless busy; use GPU0 only if GPU1 is busy/unavailable.
- Every support row must record physical GPU UUID.
- Do not mix physical GPU UUIDs within a paired support row.

## Gates To Preserve

Carry forward the prior gates unless a reviewed plan changes them before
execution:

- finite log likelihood, filtered means/variances, ESS, final particles, and
  final log weights;
- actual-SIR semantics: row id `zhao_cui_spatial_sir_austria_j9_T20`,
  `D=18`, `M=9`, actual callback metadata;
- route-fired invocation count equals active resampling steps;
- no dense low-rank transport materialization;
- low-rank factor validity: finite factors, `Q,R >= 0`, `g > 0`, factor
  marginal residual `<= 5e-3`;
- final log-weight normalization residual `<= 1e-5`;
- ESS fraction min `>= 0.01`;
- paired log-likelihood max absolute delta `<= 10.0` and mean absolute delta
  `<= 5.0`;
- paired filtered-mean and variance gates using the prior OR thresholds;
- warm-time support only after hard validity and paired comparability pass.

## Forbidden Claims And Actions

- Do not claim speedup before held-out paired support rows pass.
- Do not use tuning rows as promotion evidence.
- Do not claim posterior correctness.
- Do not claim HMC readiness.
- Do not change public API/default behavior.
- Do not claim dense Sinkhorn equivalence.
- Do not claim broad scalable-OT selection.
- Do not use POT, external solvers, package installs, or network.
- Do not treat low-rank-only large-N rows as same-row speed comparison.
- Do not continue to large-N envelope if held-out paired support fails.

## Next Safe Action

Create a new reviewed master program for:

`actual-SIR low-rank tuning and held-out validation`

The first material phase should build the tuning-grid plan and artifact schema,
not run large-N. The plan must explicitly name tuning rows, held-out support
rows, tuning parameters, promotion vetoes, and the exact artifact paths before
execution.
