# Actual-SIR Low-Rank N3072 Seed-Replication Review Ledger

Date: 2026-06-23

Status: `EXECUTION_PASS_RESULT_WRITTEN_CLOSEOUT_SUBPLAN_CREATED`

## Entry-Condition Anchors

- N2048 minimal-rank validation result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-minimal-rank-validation-result-2026-06-23.md`
- N2048 seed-replication result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-seed-replication-result-2026-06-23.md`
- N3072 representative resource-smoke result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-result-2026-06-23.md`
- N3072 second-candidate validation result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-result-2026-06-23.md`
- N3072 two-row consolidation/resource-boundary result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-two-row-consolidation-resource-boundary-result-2026-06-23.md`
- Human approval for this next phase: user message `do as you suggested`.

## Draft Scope

Subplan:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-subplan-2026-06-23.md`

Planned candidate set:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`

Planned seed batch: `81139,81140`.

Planned aggregate prefix:

- `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623`

Reason for shortened prefix:

- both prior N3072 row JSON basenames reached exactly `255` bytes, so this
  phase must preserve path-length headroom before any GPU runtime.

## Local Checks

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `18 passed`.
- Exact dry-run for the two-candidate N3072 seed-replication plan:
  - Result: pass.
  - Aggregate status: `DRY_RUN`.
  - `summary.num_candidates = 2`.
  - Exact candidate ids:
    - `r16_eps0p25_alpha1em08_it120`
    - `r16_eps0p125_alpha1em08_it120`
  - Exact assignment epsilons: `0.25` and `0.125`.
  - Exact seeds: `81139,81140`.
  - Exact shape: batch `2`, time steps `20`, particles `3072`.
  - Row JSON/Markdown/log paths are present and distinct.
  - Row path basename bytes:
    - `r16_eps0p25_alpha1em08_it120`: JSON `240`, Markdown `238`, log `239`.
    - `r16_eps0p125_alpha1em08_it120`: JSON `241`, Markdown `239`, log `240`.
  - This restores path-length headroom relative to the prior N3072 exact
    `255` byte row JSON basename boundary.

## Claude Review

- Reviewer: Claude Opus/max, read-only.
- Scope:
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-subplan-2026-06-23.md`
  - this review ledger.
- Verdict: `VERDICT: AGREE`

Material findings:

- Scope is consistent and bounded to exactly the two rank-16 candidates and
  fresh seeds `81139,81140`.
- Evidence contract is explicit and properly bounded: both rows must pass, warm
  timing is descriptive only, and forbidden claims are excluded.
- Stop conditions and continuation vetoes are concrete, especially path-length
  overflow, stale-row mismatch, provenance loss, timeouts, and forbidden-claim
  boundaries.
- Artifact coverage is adequate for aggregate JSON/Markdown, row
  JSON/Markdown/logs, review ledger, and result/blocker note.
- Path-length boundary handling is present and feasible because dry-run basename
  lengths are below `255` bytes for both candidates.
- BayesFilter policy compliance is maintained: no NumPy implementation backend
  is authorized, TensorFlow/TFP GPU/TF32 execution is preserved, and Claude is
  read-only reviewer only.

Residual risks:

- Execution should rely on the preserved dry-run JSON/Markdown artifacts and
  not only on the prose summary in this ledger.
- Any timeout in the eventual result must be classified carefully as
  `low-rank-arm`, `streaming-arm`, or `shared-harness/resource`.

Convergence:

- `SUBPLAN_REVIEW_CONVERGED`.

## Pre-Execution Gate

Timestamp: `2026-06-23T23:33:04+08:00`

Skeptical audit refresh:

- Result: pass.
- Reason: the subplan remains bounded to two exact rank-16 candidates, fresh
  seeds `81139,81140`, paired streaming comparators from the same run, warm
  timing descriptive-only, explicit path-length gate, explicit stop conditions,
  no-NumPy implementation policy, and converged Opus/max read-only review.

Trusted GPU precheck:

- Command:
  `nvidia-smi --query-gpu=index,name,uuid,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits`
- Result:
  - GPU 0: `1561 / 32760 MiB`, utilization `28%`.
  - GPU 1: `18 / 32760 MiB`, utilization `0%`.
- Process snapshot: `nvidia-smi pmon -c 1` showed display/session processes on
  GPU 0 and only `Xorg` on GPU 1.
- Decision: GPU 1 is suitable for the bounded run using
  `--cuda-visible-devices 1 --device /GPU:0`.

Execution gate:

- `READY_TO_EXECUTE_N3072_SEED_REPLICATION_TWO_ROWS`.

## Execution Result

Execution command:

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81139,81140 \
  --time-steps 20 \
  --num-particles 3072 \
  --low-rank-ranks 16 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120 \
  --phase-id-prefix ASLR-N3072-SR \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 7200 \
  --output docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.json \
  --markdown-output docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.md \
  --quiet
```

Structured execution validation:

- Result: pass, `errors=[]`.
- Aggregate JSON: `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.json`.
- Aggregate Markdown: `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.md`.
- Aggregate status: `PASS`.
- Aggregate summary: `summary.num_candidates = 2`,
  `summary.num_freeze_nominated = 2`,
  `summary.num_comparable_but_slow = 0`.
- Exact seed batch: `81139,81140`.
- Exact shape: batch `2`, time steps `20`, particles `3072`.
- Both rows used GPU/XLA/TF32 compiled-core provenance with selected GPU 1,
  NVIDIA GeForce RTX 4080 SUPER, UUID
  `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`.
- Post-run trusted GPU snapshot recorded GPU 1 back at `18 / 32760 MiB`,
  utilization `0%`; this is resource context only.

Row outcomes:

| Candidate | Epsilon | Status | Label | Hard vetoes | Actual-SIR semantics | Warm ratio | Mean abs loglik delta | Max abs loglik delta | Filtered mean rel L2 | Filtered variance rel L2 | Final particle mean rel L2 | ESS min fraction | Final logsumexp residual | Row wall time | Filename max bytes |
| --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | 0.25 | `PASS` | `freeze-nominated` | `[]` | `true` | 9.829297316594772 | 0.050994873046875 | 0.08428955078125 | 0.00012149695949770663 | 0.00875657653186016 | 0.00025625437559379134 | 0.6346776882807413 | 9.5367431640625e-07 | 393.62865215400234s | 232 |
| `r16_eps0p125_alpha1em08_it120` | 0.125 | `PASS` | `freeze-nominated` | `[]` | `true` | 10.091529125979234 | 1.7257080078125 | 2.97552490234375 | 0.0008683099090988481 | 0.08734641149471267 | 0.0005612295217771006 | 0.6346776882807413 | 9.5367431640625e-07 | 392.60985371191055s | 233 |

Interpretation boundaries:

- Both rank-16 candidates remain viable under this exact N3072 fresh
  seed-replication screen.
- Warm ratios, wall times, log-likelihood deltas, ESS values, and GPU memory
  snapshots are descriptive/resource-triage diagnostics only.
- This execution does not establish statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, N4096 feasibility, formal memory scaling, production readiness,
  scientific validity, or invalidity of deferred rank-32/64/128 candidates.

## Post-Execution Handoff

Required result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-result-2026-06-23.md`

Next subplan:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-replicated-evidence-resource-boundary-subplan-2026-06-23.md`

Next action:

- Run a no-runtime local replicated-evidence/resource-boundary closeout that
  validates the two prior N3072 seed-batch rows plus the fresh seed-replication
  two-row aggregate, then stop automatic runtime escalation unless the user
  requests a fresh reviewed runtime subplan.
