# Actual-SIR Nystrom Compiled-Redo Promotion-or-Rejection Runbook

Date: 2026-06-23

Status: `BLOCKED_P09_POLICY_DECISION_REQUIRED`

## Purpose

This runbook is the current promotion-or-rejection plan for the repaired
compiled Nystrom lane on the actual-SIR `D=18,M=9,T=20` model.

The older `actual-sir-nystrom-default-promotion-*` runbook remains useful as
history, but it is not sufficient for promotion decisions because its runtime
protocol was later found contaminated by a Python-level route loop and small
chunks.  Old Python-loop timing artifacts are quarantined for speed, ranking,
and default-promotion claims.

Promotion or rejection must now use only the repaired compiled-redo harness and
artifacts unless a later reviewed plan explicitly replaces this runbook.

## Current Trust Boundary

Trusted repaired-lane components:

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
  with `nystrom_transport_resample_tensors_tf`
- `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
- `tests/test_nystrom_transport_tf.py`
- `tests/test_actual_sir_nystrom_compiled_redo.py`
- compiled-redo artifacts beginning with
  `docs/benchmarks/actual-sir-nystrom-compiled-redo-*`

Quarantined for timing/ranking/promotion:

- `docs/benchmarks/actual-sir-nystrom-default-promotion-p05b-*`
- any old result interpreting the Python-loop paired harness runtime as
  candidate speed evidence
- the stopped one-seed `N=4096` launch, which created no valid artifact

The old artifacts may be cited only as historical debugging context or as
validity smoke evidence when the result note already separated them from timing
claims.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the repaired compiled fixed-rank Nystrom transport route pass enough actual-SIR validity, paired comparability, scale, sensitivity, stress, and gradient/integration gates to justify default promotion; if not, should it be rejected or kept optional? |
| Candidate | Compiled tensor-only Nystrom route with default candidate settings `rank=32`, `epsilon=0.5`, `max_iterations=160`, `convergence_threshold=1e-4`, `float32`, TF32 enabled, `jit_compile=True`, `history-mode=value-only` unless a phase says otherwise. |
| Baseline/comparator | Compiled production-style streaming TF32 actual-SIR route under the same process, model, seeds, dtype, TF32 state, transport policy, physical GPU, and timing protocol. |
| Serious model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18`, `M=9`, `T=20`. |
| Expected failure mode | Nystrom may be finite but fail paired log-likelihood thresholds, show seed instability, fail larger-N memory/runtime feasibility, be brittle to rank/epsilon, fail full-history or transport-policy stress, or fail gradient/HMC mechanics. |
| Promotion criterion | All hard gates through P12 pass, replicated actual-SIR evidence supports viability, sensitivity/stress gates do not expose brittleness, and default-readiness review approves the API/default change. Runtime can support promotion only after the timing protocol is replicated and uncertainty is summarized. |
| Promotion veto | Any hard veto, paired-threshold failure not repaired by a predeclared candidate setting, missing GPU/TF32 evidence, stale/quarantined artifact used as support, nonfinite output, residual threshold failure, route invocation mismatch, dense materialization in the Nystrom route, full-history incompatibility, gradient/HMC mechanics failure if default use requires differentiability, or reviewed code/API blocker. |
| Continuation veto | Broken harness artifact, GPU unavailable in trusted context for required GPU gates, repeated timeout before artifact creation, environment mismatch that prevents fair comparison, or an implementation defect that invalidates the current candidate and cannot be repaired without changing the candidate class. |
| Repair trigger | Compile regression, paired deltas near threshold, residual degradation, sensitivity brittleness, stress-policy failure, missing diagnostics, or harness/schema bug. |
| Explanatory diagnostics | Runtime, warm-call median, compile-plus-first-call time, memory, warm-time ratios, Nystrom residuals/iterations, ESS, rank/epsilon response, and per-seed deltas unless classified otherwise by a phase. |
| What must not be concluded | Passing intermediate gates does not prove posterior correctness, dense Sinkhorn equivalence, HMC readiness, statistical superiority, broad scalable-OT selection, or public/default readiness. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is the repaired compiled Nystrom route good enough to become the default actual-SIR scalable transport path, or should it be rejected/deferred? |
| Exact baseline | Compiled streaming TF32 route in `benchmark_actual_sir_nystrom_compiled_redo.py`, same GPU, seeds, model, dtype, TF32 state, and transport policy. |
| Primary pass/fail criterion | Each phase writes JSON/Markdown artifacts and has `status=PASS`, `hard_vetoes=[]`, required GPU/TF32/JIT evidence, and required paired comparability or stress diagnostics. |
| Veto diagnostics | Nonfinite outputs, missing route invocation evidence, residual thresholds, paired log-likelihood thresholds, GPU/TF32 mismatch, artifact/schema mismatch, timeout without artifact, stale artifact support, sensitivity/stress failure, and gradient/HMC failures where required. |
| Explanatory-only diagnostics | Single-run timing, memory, warm ratios, residual magnitudes below threshold, ESS above floor, one-seed high-N envelope results, and any ranking without uncertainty support. |
| Not concluded on pass | No statistical superiority, posterior correctness, dense equivalence, HMC readiness, or public/default readiness until the specific later gate passes. |
| Result preservation | Phase JSON/Markdown under `docs/benchmarks/actual-sir-nystrom-compiled-redo-*` and result notes under this `compiled-redo` plan prefix. |

## Skeptical Plan Audit

Status: `PASS_FOR_P05_REPLICATION_AND_SEQUENTIAL_LADDER`

- Wrong baseline risk: controlled by using compiled streaming TF32 as the
  comparator, not the old Python-loop streaming path.
- Proxy metric risk: controlled by classifying timing and memory as
  descriptive until replicated timing and uncertainty summaries exist.
- Missing stop conditions: each phase has hard veto, repair trigger, and
  continuation-veto rules.
- Unfair comparison risk: paired rows use the same model, seeds, dtype, TF32,
  GPU, transport policy, JIT setting, and process.
- Hidden assumption risk: GPU1 preference and GPU0 fallback must be recorded in
  every GPU artifact.
- Stale context risk: old default-promotion timing artifacts are quarantined.
- Environment mismatch risk: GPU/CUDA preflight is required in trusted context
  before GPU phases.
- Artifact mismatch risk: promotion support must cite compiled-redo JSON and
  matching result notes only.

## Completed Gates

| Gate | Artifact | Status |
| --- | --- | --- |
| P02 GPU smoke | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p02-gpu-smoke-2026-06-22.json` | `PASS`, `hard_vetoes=[]` |
| P03 moderate before repair | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03-moderate-b1-t20-n1024-2026-06-22.json` | `PASS`, but exposed compile-latency repair trigger |
| P03B while-loop repair | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03b-while-loop-repair-b1-t20-n1024-2026-06-23.json` | `PASS`, compile-plus-first reduced from `804.52s` to `12.19s` |
| P04 serious B5 row | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p04-serious-b5-t20-n1024-2026-06-23.json` | `PASS`, `hard_vetoes=[]`, paired max delta `3.85498046875` |
| P05 same-shape disjoint replication | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-2026-06-23.json` | `PASS`, `hard_vetoes=[]`, paired max delta `7.10369873046875` |
| P06 same-shape replication summary | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p06-same-shape-replication-summary-result-2026-06-23.md` | `PASS`, combined 10-seed mean abs delta `2.591357421875` |
| P07 larger-N `N=2048` paired row | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-larger-n-b5-t20-n2048-2026-06-23.json` | `PASS`, `hard_vetoes=[]`, paired max delta `4.65521240234375` |
| P07 one-seed `N=4096` paired diagnostic | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-2026-06-23.json` | `PASS`, `hard_vetoes=[]`, paired delta `0.57757568359375` |
| P07 one-seed `N=8192` paired diagnostic | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n8192-diagnostic-2026-06-23.json` | `PASS`, `hard_vetoes=[]`, paired delta `0.0142822265625` |
| P08 Nystrom-only high-N envelope | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p08-high-n-nystrom-only-envelope-result-2026-06-23.md` | `PASS`, Nystrom-only rows through `N=65536` passed |
| P09 rank/epsilon sensitivity full grid | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09-rank-epsilon-sensitivity-partial-result-2026-06-23.md` | `STOPPED`: `rank=16,epsilon=1.0` failed paired thresholds |
| P09 default-neighborhood repair | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09-default-neighborhood-repair-result-2026-06-23.md` | `BLOCKED`: `rank=32,epsilon=0.25` produced nonfinite Nystrom outputs |
| P09B rescue tuning | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09b-rescue-tuning-result-2026-06-23.md` | `EPSILON_FLOOR_RESCUE_IDENTIFIED`: `epsilon=0.25` unsafe, `epsilon=0.3/0.375` passed |
| P09C policy confirmation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09c-policy-confirmation-result-2026-06-23.md` | `PARTIAL`: `rank=32,epsilon=0.3/0.5` passed; `rank=64,epsilon=0.3` failed nonfinite |
| P09D spectral-core repair | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09d-spectral-core-repair-result-2026-06-23.md` | `SVD_CORE_REPAIR_DID_NOT_RESCUE`: `svd_truncated,rcond=1e-6` failed nonfinite for `rank=32,epsilon=0.25` and `rank=64,epsilon=0.3` |

Current inference status:

| Ledger | Status |
| --- | --- |
| Hard veto screen | Passed through P04 on repaired compiled lane |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Timing, warm ratio, per-seed deltas, and old timing artifacts |
| Default-readiness | `NO` |
| Next evidence needed | Policy decision: fixed `rank=32,epsilon=0.5` path versus factor/scaling numerical stabilization before P10 |

## GPU Selection Protocol

GPU commands must run in trusted/elevated context.

Before each GPU phase, run:

```bash
nvidia-smi --query-gpu=index,memory.used,utilization.gpu,name --format=csv,noheader,nounits
```

Selection rule:

1. Use physical GPU1 if available and suitable.
2. Otherwise use physical GPU0.
3. Record `--cuda-visible-devices`, `--selected-physical-gpu`, and
   `--gpu-selection-note`.
4. Use one physical GPU inside each paired artifact.
5. If GPU selection changes mid-phase, that phase is explanatory only until
   rerun on one physical GPU.

## Phase Ladder

### P05 Same-Shape Disjoint Replication

Question: does the P04 serious `B=5,T=20,N=1024` result replicate on a disjoint
seed batch?

Command template:

```bash
timeout 1800 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81220,81221,81222,81223,81224 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P05-REPL-B5-T20-N1024 --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-2026-06-23.md
```

Pass: JSON `status=PASS`, `hard_vetoes=[]`, paired thresholds pass, GPU/TF32/JIT
evidence present, no compile regression that exceeds the timeout policy.

Fail or repair: if paired thresholds fail, residuals degrade, or compile latency
regresses, stop before larger-N and write a result note classifying the failure
as implementation, tuning, stochastic instability, or evidence against the
current candidate.

### P06 Replication Summary

Combine P04 and P05 into a 10-seed same-shape summary.

Required output:

- decision table
- inference-status table
- per-seed paired deltas
- hard-veto status
- uncertainty statement
- default-readiness remains `NO`

Ranking rule: no claim that Nystrom is faster, better, or superior unless a
predeclared uncertainty analysis supports that ranking.  If only two five-seed
batches exist, treat timing and delta differences as descriptive.

### P07 Larger-N Paired Ladder

Only after P05 and P06 pass.

Rows:

| Row | Seeds | Role |
| --- | --- | --- |
| `B=5,T=20,N=2048` | `81320..81324` | First repaired larger-N paired validity/comparability row |
| `B=1,T=20,N=4096` | one seed | Cheap paired feasibility probe before bigger rows |
| `B=1,T=20,N=8192` | one seed | Optional paired feasibility if `N=4096` passes within budget |

The user explicitly approved one-seed evidence for `N>=4096` as diagnostic
rather than rigorous promotion evidence.  Therefore `N>=4096` paired rows can
support feasibility and repair decisions, but not statistical ranking or final
default promotion by themselves.

Stop: hard veto, paired-threshold failure, timeout without artifact, or GPU
memory failure.  A one-seed high-N fail does not reject the scientific idea by
itself; it triggers scale/tuning repair classification.

### P08 High-N Nystrom-Only Envelope

Only after P07 identifies no immediate scale blocker.

Rows: `N=4096,8192,16384,32768,65536`, one seed each, Nystrom route only.

Purpose: memory/runtime feasibility and shape stability.  These rows do not
establish paired quality, dense equivalence, or default readiness.

Pass: finite outputs, residual thresholds pass, GPU/TF32/JIT evidence present,
artifact written.

### P09 Rank/Epsilon Sensitivity

Only after same-shape replication and at least one larger-N paired row pass.

Candidate grid:

- ranks: `16,32,64`
- epsilons: `0.25,0.5,1.0`
- shape: at least `B=5,T=20,N=1024`; add `N=2048` if the first grid is stable

Purpose: determine whether the default candidate is robust or whether the lane
requires a different fixed policy.  This is a brittleness and repair gate, not a
leaderboard unless uncertainty analysis is added.

### P10 Transport-Policy And History Stress

Required stress rows:

- `transport-policy=no-resampling`
- `transport-policy=active-all`
- a mixed/conditional active mask if supported by the harness
- `history-mode=full` smoke or paired row

Purpose: ensure the route is not only viable in the value-only active-all path.

Pass: artifacts written, finite outputs, no route invocation mismatch, no
history/schema incompatibility, paired thresholds where a paired comparator is
run.

### P11 Gradient And HMC Mechanics

This gate is required before claiming default readiness for any differentiable
or inference-facing default.

Minimum checks:

- finite gradient through compiled Nystrom actual-SIR value path
- no NaN/Inf in value or gradient for a small serious-model row
- if HMC/NUTS uses this path, a tiny mechanics gate with fixed shape and clear
  nonclaims

Pass here means mechanics viability only.  It does not prove posterior
correctness or HMC convergence.

### P12 Integration And Default-Readiness Review

Only after P05 through P11 pass or are explicitly declared not applicable by a
reviewed result note.

Required:

- focused tests pass
- code review of implementation and harness
- API/default policy proposal
- documentation update
- run manifest with git commit, command, environment, GPU, seeds, wall time,
  artifacts, plan, and result file
- final result note with decision and inference-status tables

Promotion decision options:

- `PROMOTE_DEFAULT`: all gates pass, uncertainty and review support the default
  change, and no unresolved veto remains.
- `PROMOTE_OPTIONAL_ONLY`: validity/scale are promising but default evidence is
  insufficient.
- `DEFER_FOR_REPAIR`: a repairable implementation, tuning, or evidence gap
  remains.
- `REJECT_CURRENT_CANDIDATE`: a hard or replicated failure shows the current
  fixed-rank Nystrom candidate is unsuitable under this model/threshold.

## Artifact Naming

Use this prefix for new artifacts:

- JSON/Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-pXX-*.{json,md}`
- result notes:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-pXX-*-result-2026-06-23.md`

Every serious result note must include:

- decision table
- inference-status table
- run manifest
- hard-veto status
- statistical humility statement
- nonclaims
- next justified action

## Immediate Next Action

Stop automatic execution before P10 under a broad Nystrom policy.  P09D showed
that replacing the core inverse with `svd_truncated,rcond=1e-6` did not rescue
the known nonfinite rows, so the next stabilization target should instrument and
repair factor/scaling numerics rather than only swapping Cholesky for SVD.

Decide whether to continue with a fixed `rank=32,epsilon=0.5` policy despite
nearby numerical brittleness, or repair rank/epsilon numerical stability and
rerun P09.
