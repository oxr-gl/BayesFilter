# Phase 9 Result: Trusted GPU Ladder

date: 2026-06-23
phase: P9-GPU-LADDER
decision: BLOCKED_N10000_TIMEOUT
git_commit_at_checks: 97ad05d40676f3fd15a2a2b4d45034ebb657ed97

## Question

Does the exact audited no-production-autodiff `manual-reverse` route produce
finite five-seed SIR actual gradients through N10000 on trusted GPU/TF32?

## Decision

No, not through N10000 under the reviewed P9 command and timeout.

The exact audited route passed N100, N1000, N2500, and N5000 on trusted GPU
with finite objective, finite gradient components, finite seed-gradient MCSE,
GPU output placement, five seeds, `manual-reverse`, `fd-mode ad-only`,
streaming transport, and `transport_ad_mode=stabilized`.

The N10000 rung then hit the reviewed 7200 second timeout before writing either
the required N10000 JSON artifact or the N10000 progress artifact.  The ordered
rung ledger records N10000 as `BLOCKED`, records it as the first non-`PASSED`
rung, and confirms that no higher rung was launched after the blocker.

P10 is not authorized because the required valid N10000 JSON artifact does not
exist.

## Governing Artifacts

| Artifact | Path |
|---|---|
| P8 exact route manifest | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json` |
| P8 exact audit result | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json` |
| P9 evidence contract | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-evidence-contract-2026-06-23.md` |
| P9 GPU preflight | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-preflight-2026-06-23.json` |
| P9 run manifest | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-run-manifest-2026-06-23.json` |
| P9 rung ledger | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-rung-ledger-2026-06-23.json` |

P8 audit binding was revalidated immediately before N100 and printed
`P8_ROUTE_AUDIT_OK`.

## Execution Environment

| Field | Value |
|---|---|
| Working directory | `/home/chakwong/BayesFilter` |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Timeout binary | `/usr/bin/timeout` |
| `MPLCONFIGDIR` | `/tmp` |
| TensorFlow | `2.19.1` |
| Python | `3.11.14` |
| GPU | NVIDIA GeForce RTX 4080 SUPER |
| GPU preflight | Passed: physical and logical GPU visible |

## Route Contract

All rungs used:

- `--ad-evaluation-mode manual-reverse`;
- `--fd-mode ad-only`;
- `--device-scope visible --expect-device-kind gpu --device /GPU:0`;
- `--time-steps 3`;
- `--batch-seeds 81120,81121,81122,81123,81124`;
- `--seed-microbatch-size 1`;
- `--transport-policy active-all`;
- `--transport-plan-mode streaming`;
- `--transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys`;
- `--transport-ad-mode stabilized`;
- `--sinkhorn-iterations 10 --sinkhorn-epsilon 1.0`;
- `--row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512`;
- `--dtype float32 --tf32-mode enabled`;
- `--basis-set raw`.

No finite-difference run was launched.  Zhao-Cui was not used as comparator or
oracle.  `transport_ad_mode=full` was not used.  Diagnostic
`reverse-gradient` and `forward-jvp` modes were not used for P9 rungs.

## Rung Outcomes

| Rung | Decision | Elapsed seconds | Objective | Gradient values | MCSE values | Artifact |
|---|---|---:|---:|---|---|---|
| N100 | `PASSED` | `45.65411602900713` | `-125.5495834350586` | `[-181.6804962158203, 78.67701721191406, 47.452369689941406]` | `[14.84323501586914, 3.5661163330078125, 0.5900697112083435]` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n100-gpu-tf32-2026-06-23.json` |
| N1000 | `PASSED` | `120.33764437299396` | `-125.59486389160156` | `[-157.0895538330078, 70.14373016357422, 47.449344635009766]` | `[6.868458271026611, 1.8717975616455078, 0.12387192994356155]` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n1000-gpu-tf32-2026-06-23.json` |
| N2500 | `PASSED` | `596.2364752149879` | `-125.6163558959961` | `[-150.3473663330078, 68.51795959472656, 47.509605407714844]` | `[4.347273349761963, 1.1901887655258179, 0.07655978947877884]` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n2500-gpu-tf32-2026-06-23.json` |
| N5000 | `PASSED` | `2404.353009808008` | `-125.61854553222656` | `[-154.6905517578125, 69.28536224365234, 47.51017761230469]` | `[7.402919769287109, 1.611832618713379, 0.08166752755641937]` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n5000-gpu-tf32-2026-06-23.json` |
| N10000 | `BLOCKED` | timeout at `7200` seconds | N/A | N/A | N/A | no JSON/progress artifact written |

The N2500 pass is material because the inherited S7R/P82 blocker was an N2500
OOM on a partial manual route with outer autodiff.  This P9 result shows that
the exact P8 audited no-production-autodiff route clears N2500 and N5000 under
the reviewed command.  It does not clear N10000.

## N10000 Blocker

Command:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 7200 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120,81121,81122,81123,81124 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "P9 no-autodiff manual-reverse actual-gradient N10000 GPU TF32" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --progress-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n10000-progress-2026-06-23.json --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n10000-gpu-tf32-2026-06-23.json
```

Observed outcome:

- command exited with code `124`;
- no N10000 JSON exists;
- no N10000 progress JSON exists;
- process was no longer present after timeout;
- rung ledger decision: `BLOCKED`;
- first non-`PASSED` rung: `N10000`;
- no higher rung was launched after the blocker.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Primary criterion | Not met: N10000 did not exit 0 and did not write the required JSON artifact. |
| Veto diagnostics | Triggered: N10000 timeout and missing N10000 output/progress artifacts. |
| Explanatory diagnostics | N100 through N5000 passed; runtime increased steeply from N2500 to N5000; N10000 remained active until timeout but did not reach a progress write. |
| Not concluded | FD agreement, posterior correctness, HMC readiness, production default, statistical superiority, or scientific validity. |

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| `BLOCKED_N10000_TIMEOUT` | Failed at N10000 timeout before output artifact. | N10000 timeout veto fired; no FD/default/scientific drift occurred. | Whether N10000 needs more runtime, smaller chunks, additional streaming within seed/rung, or a new memory/runtime remediation route. | Stop P9; write a new reviewed remediation subplan before any N10000 retry. | FD agreement, HMC readiness, posterior correctness, production default, scientific validity. |

## Handoff

P10 must not run because P9 did not produce a valid N10000 JSON.  Any further
attempt to reach N10000 requires a new reviewed remediation subplan.  Candidate
remediation questions include timeout budget, finer-grained chunking,
additional seed/rung checkpointing, or a deeper streaming/blockwise memory
route, but no retry is authorized by this P9 result.
