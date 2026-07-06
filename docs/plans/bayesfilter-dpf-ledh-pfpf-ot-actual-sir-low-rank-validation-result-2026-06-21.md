# Actual-SIR Low-Rank LEDH/PFPF-OT Validation Result

Date: 2026-06-21

Status: `TUNING_REQUIRED`

Final phase reached: P03 paired actual-SIR ladder.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | The current low-rank route/configuration is not promotable for actual-SIR d18 LEDH/PFPF-OT efficiency. It requires tuning or route repair before further large-N validation. |
| Primary criterion status | Failed. The first required paired row `B=5,T=20,N=1024` did not pass paired log-likelihood comparability and did not pass the warm-time support screen. |
| Veto diagnostic status | No hard finite/factor/nonmaterialization veto fired on the attempted row, but paired comparability and speed support gates failed. |
| Main uncertainty | The result rejects promotion of the current configured candidate, not the whole low-rank research direction. |
| Next justified action | Stop this program. Open a separate tuning/repair plan only if the next lane predeclares candidate parameters and reruns the actual-SIR gates. |
| Not concluded | No speedup, no large-N actual-SIR envelope support, no posterior correctness, no HMC readiness, no public API/default/production readiness, no dense Sinkhorn equivalence, no broad scalable-OT selection, and no statistical ranking. |

## Evidence Summary

P00-P02 established governance, focused harness compile/test checks, preserved
actual-SIR route semantics, and tiny actual-SIR route smoke evidence. P03 then
ran the first required paired GPU row on the real actual-SIR d18 workload.

| Artifact | Status |
| --- | --- |
| Master program | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-master-program-2026-06-21.md` |
| P00 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p00-governance-result-2026-06-21.md` |
| P01 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p01-harness-result-2026-06-21.md` |
| P02 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-result-2026-06-21.md` |
| P03 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p03-paired-ladder-result-2026-06-21.md` |
| P03 aggregate | `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21.json` |
| P03 attempted row | `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json` |
| P04 blocked result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-result-2026-06-21.md` |

## P03 Row Metrics

| Metric | Value |
| --- | --- |
| Shape | `B=5,T=20,N=1024,D=18,M=9` |
| Seeds | `81120,81121,81122,81123,81124` |
| GPU | GPU1, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| TF32 | enabled and recorded true |
| Streaming warm median | `0.9723010780289769` seconds |
| Low-rank warm median | `58.549089503940195` seconds |
| Warm median ratio | `0.016606596042173186` |
| Required ratio | `>= 1.25` |
| Log-likelihood max absolute delta | `58.0933837890625`; threshold `<= 10.0` |
| Log-likelihood mean absolute delta | `42.93328857421875`; threshold `<= 5.0` |
| Low-rank factor marginal residual | `8.986273314803839e-06`; threshold `<= 5e-3` |
| Low-rank projection iterations max | `240.0` |
| Row wall time | `633.6386418200564` seconds |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the attempted P03 row. |
| Paired comparability | Failed due to log-likelihood delta thresholds. |
| Warm-time support screen | Failed; low-rank was descriptively much slower than compiled streaming on the attempted row and failed the predeclared support ratio. |
| Statistically supported ranking | Not supported; no uncertainty analysis or multi-row support. |
| Large-N executable envelope | Not run and not supported in this actual-SIR program because P03 handoff conditions failed. Although the master contract allowed low-rank-only `N=50000/100000` rows to support executable-envelope-only language after a valid P03 basis, P03 failed before that handoff, so running P04 would have created proxy-only evidence outside the stopped program. |
| Default-readiness | Not supported. |
| Next evidence needed | A new tuning/repair plan with predeclared low-rank parameters, focused P02 smoke, and rerun P03 paired actual-SIR gates. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit recorded in P03 row | `c4690d153e6a73173e20f33f55c44827ee5f298d` |
| Python executable | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| TensorFlow version | `2.20.0` |
| Python version | `3.13.13` |
| Device policy | GPU1 preferred; GPU1 used |
| P03 command | `timeout 3600 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --streaming-timing-source compiled_core --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 1024 --transport-policy active-all --warmups 1 --repeats 3 --dtype float32 --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --tf32-mode enabled --phase-id ACTUAL-SIR-LR-P03-GPU1-PAIRED-B5-T20-N1024 --output docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json --markdown-output docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.md` |
| P03 timeout policy | Exact `3600s` outer timeout; row completed before timeout |

## Post-Run Red Team

The strongest alternative explanation is that the low-rank route is badly
tuned for the real actual-SIR workload rather than intrinsically unsuitable.
That is consistent with hard validity passing while paired log-likelihood and
runtime support fail. The result would be overturned only by a new reviewed
tuning/repair program that predeclares candidate settings and then passes the
same actual-SIR paired gates.

The weakest part of the evidence is that only the first required P03 row was
run. That is intentional under the stop rule: larger paired rows would not
repair the failed paired support basis, and low-rank-only large-N rows would
only produce executable-envelope diagnostics. The master contract allowed that
executable-envelope language only when P03 supplied a valid continuation basis;
after P03 failed, P04 would not answer the stated efficiency question. The
pre-execution P03 subplan explicitly controlled this handoff: advance to P04
only after a valid paired basis, and stop as `TUNING_REQUIRED` if low-rank runs
but paired comparability or practical resource evidence fails.

## Claude Review Trail

Claude read-only review rounds and repair actions are recorded in:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-claude-review-ledger-2026-06-21.md`

## Nonclaims

- No speedup claim.
- No large-N actual-SIR executable-envelope claim for this lane.
- No posterior correctness claim.
- No HMC readiness claim.
- No public API readiness claim.
- No production/default readiness claim.
- No dense Sinkhorn equivalence claim.
- No broad scalable-OT selection claim.
- No statistical ranking claim.
