# P82 Phase 7R Subplan: XLA Chunk2500 Actual-Gradient Remediation

status: READY_FOR_CLAUDE_REVIEW
date: 2026-06-24
phase: P7R-XLA-CHUNK2500-ACTUAL-GRADIENT-REMEDIATION

## Phase Objective

Remediate the old P7 N10000 actual-gradient blocker by rerunning the P82
N10000 five-seed actual-gradient gate through the compiled `manual-reverse`
route with XLA and the empirically selected exact moderate transport chunk
`2500 x 2500`.

This phase is actual-gradient feasibility only.  It does not run regression FD
and does not claim FD consistency.

## Entry Conditions Inherited From Previous Phase

- P6 tiny trusted GPU smoke passed and was reviewed.
- P7 N1000 five-seed feasibility rung passed.
- Old P7 N10000 failed under the reviewed `reverse-gradient`/chunk-512 command
  with TensorFlow `ResourceExhaustedError`; P8 was blocked because no valid
  N10000 actual-gradient artifact existed.
- The subsequent N10000 timing/remediation diagnostics established that the
  `manual-reverse` XLA route is viable and that `row_chunk_size=2500`,
  `col_chunk_size=2500` is the current best tested N10000 row/column chunk
  shape for this route.
- `transport_ad_mode=full` remains forbidden.
- GPU commands require trusted/escalated execution.

## Required Artifacts

- P7R N10000 actual-gradient JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-gpu-tf32-2026-06-24.json`
- P7R N10000 progress JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-progress-2026-06-24.json`
- P7R memory sidecar:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-memory-samples-2026-06-24.json`
- P7R result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-xla-chunk2500-actual-gradient-remediation-result-2026-06-24.md`
- Refreshed P8 subplan only if P7R passes:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-consistency-subplan-2026-06-24.md`
- Updated P82 visible stop handoff.

## Required Checks / Tests / Reviews

Before GPU work:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-*.md
```

Trusted/escalated GPU preflight:

```bash
nvidia-smi
MPLCONFIGDIR=/tmp python -c "import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices()); print(tf.config.list_physical_devices('GPU'))"
```

Claude review:

- Use one exact path only: this subplan.
- Do not paste code or artifact packets.
- Ask whether the subplan safely remediates P7 without crossing into P8/FD or
  unsupported claims.

## P7R Command

Run with trusted GPU permissions:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 7200 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --manual-reverse-warmups 0 \
  --manual-reverse-repeats 1 \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 Phase 7R manual-reverse XLA chunk2500 actual-gradient N10000 GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 2500 --col-chunk-size 2500 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-progress-2026-06-24.json \
  --memory-sample-output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-memory-samples-2026-06-24.json \
  --memory-sample-interval-seconds 30 \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-gpu-tf32-2026-06-24.json
```

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the reviewed manual score route produce finite five-seed SIR d18 actual gradients at N10000 under GPU/TF32 with XLA and chunk `2500 x 2500`, without the known-bad full-AD route? |
| Baseline/comparator | Old P7 N1000 passed; old P7 N10000 failed under `reverse-gradient`/chunk-512; N10000 chunk diagnostics identified `manual-reverse` XLA chunk `2500` as the current best tested compute shape. No FD comparator in P7R. |
| Primary criterion | The P7R command exits 0 and writes JSON with `status=pass`, `primary_pass=true`, GPU output devices, five fixed seeds, `num_particles=10000`, `seed_microbatch_size=1`, `ad_evaluation_mode=manual-reverse`, `compiler.mode=xla`, `jit_compile=true`, `transport_plan_mode=streaming`, `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, chunks `2500/2500/512`, finite objective, finite gradient components, and finite seed-gradient MCSE. |
| Veto diagnostics | Timeout, OOM, missing artifact, GPU not visible, wrong route metadata, wrong particle count or seed count, nonfinite objective/gradient/MCSE, `transport_ad_mode=full`, FD comparison launched, or unsupported HMC/default/scientific-superiority claim. |
| Explanatory diagnostics | Runtime, compiler timings, warm-call timings, per-seed gradient contributions, seed SD/SE, device placement, TF32 metadata, chunk sizes, and TensorFlow allocator memory samples. |
| Not concluded | No FD agreement, no posterior correctness, no HMC/default readiness, no scientific superiority, no calibrated uncertainty claim, and no production readiness. |

## Forbidden Claims / Actions

- Do not run P8 FD inside P7R.
- Do not use Zhao-Cui as a comparator or oracle.
- Do not use `transport_ad_mode=full`.
- Do not claim FD agreement or scientific correctness from this actual-gradient
  artifact alone.
- Do not change the 2-SE threshold, theta vector, seed list, Sinkhorn settings,
  or chunk settings inside this phase.

## Exact Next-Phase Handoff Conditions

P8R may be drafted and reviewed only if the P7R JSON exists and satisfies the
primary criterion above.  The P8R subplan must consume the P7R JSON path listed
here, not the old blocked P7 path.

## Stop Conditions

Stop and write a P7R blocker result if local checks fail, Claude review returns
`VERDICT: REVISE` with an unresolved material issue, trusted GPU preflight
fails, the P7R command times out/OOMs/exits nonzero, or the JSON metadata fails
the primary criterion.

## End-Of-Phase Protocol

1. Run required local checks.
2. Run trusted GPU preflight.
3. Run the P7R command.
4. Validate the JSON contract.
5. Write the P7R result.
6. If P7R passes, draft or refresh the P8R subplan and review it before any FD
   command.
7. Update the visible stop handoff.
