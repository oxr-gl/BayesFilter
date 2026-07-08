# P82 Phase 7 Subplan: Actual-Gradient Feasibility Ladder

status: REVIEWED_CLAUDE_R4_AGREE_WAITING_FOR_P6
date: 2026-06-23
phase: P7-ACTUAL-GRADIENT-FEASIBILITY

## Phase Objective

Run a bounded GPU feasibility ladder for the P5-wired manual streaming
transport-gradient route and produce the N10000 five-seed actual-gradient
artifact only if smaller rungs pass.

This phase is actual-gradient feasibility only.  It does not run regression FD
and does not claim FD consistency.

## Entry Conditions

- P6 tiny trusted GPU smoke passed, has a result artifact, and has one-path
  Claude review status `VERDICT: AGREE`.
- Route is fixed to:
  `transport_gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`.
- `transport_ad_mode=full` remains forbidden.
- GPU commands require trusted/escalated execution.

## Required Artifacts

- N1000 feasibility JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json`
- N10000 actual-gradient JSON, if feasible:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json`
- N10000 progress JSON, required only if the N10000 rung is launched:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-progress-2026-06-23.json`
- Phase 7 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md`
- Updated P82 execution ledger, Claude review ledger if P7 is reviewed, and
  stop handoff.

## Required Checks / Tests / Reviews

Before GPU work:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-*.md
```

Trusted/escalated GPU preflight:

```bash
nvidia-smi
MPLCONFIGDIR=/tmp python -c "import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices()); print(tf.config.list_physical_devices('GPU'))"
```

N1000 feasibility rung:

```bash
MPLCONFIGDIR=/tmp timeout 1800 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 1000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 Phase 7 manual streaming actual-gradient feasibility N1000 GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json
```

N10000 actual-gradient rung:

```bash
MPLCONFIGDIR=/tmp timeout 7200 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 Phase 7 manual streaming actual-gradient N10000 GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-progress-2026-06-23.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json
```

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the manual streaming route produce finite five-seed SIR d18 actual gradients at N10000 under GPU/TF32 without the known-bad full-AD route? |
| Baseline/comparator | P6 tiny GPU smoke and the N1000 feasibility rung; no FD comparator in this phase. |
| Primary criterion | N1000 and N10000 ad-only runs exit 0; output metadata records GPU placement, five seeds, `seed_microbatch_size=1`, `transport_plan_mode=streaming`, `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, finite objective, finite gradient components, and finite seed-gradient MCSE. |
| Veto diagnostics | Timeout, OOM, missing artifact, GPU not visible, wrong route metadata, wrong particle count or seed count, nonfinite objective/gradient/MCSE, `transport_ad_mode=full`, any FD comparison claim, or unsupported HMC/default/scientific-superiority claim. |
| Explanatory diagnostics | Runtime, per-seed gradient contributions, seed SD/SE, device placement, TF32 metadata, chunk sizes, progress file. |
| Not concluded | No FD agreement, no posterior correctness, no HMC/default readiness, no scientific superiority, and no calibrated uncertainty claim. |

## Stop Conditions

Stop after writing a blocker result if N1000 fails.  If P7 stops before
launching N10000, the result must explicitly explain why the N10000 JSON and
progress JSON are absent.  Stop after writing a blocker result if N10000 fails,
times out, OOMs, or emits incomplete/wrong metadata.  Do not proceed to P8
without a valid N10000 JSON artifact.

## Next-Phase Handoff Conditions

P8 may start only if the N10000 JSON exists and satisfies the primary
criterion.  P8 must compare this N10000 actual-gradient artifact against a
separate N1000 governed FD artifact.
