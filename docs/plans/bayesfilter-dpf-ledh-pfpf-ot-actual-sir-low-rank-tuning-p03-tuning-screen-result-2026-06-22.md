# P03 Actual-SIR Tuning Screen Result

Date: 2026-06-22
Status: `NO_FREEZE_CANDIDATE_REPAIR_REQUIRED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P03 Stage A completed, but no candidate was freeze-nominated. Stage B is not allowed under the P03 subplan, and P04 must not start. |
| Primary criterion status | Failed. The primary criterion required at least one freeze-eligible candidate; Stage A recorded `num_freeze_nominated=0`. |
| Veto diagnostic status | Two candidates hard-vetoed on ESS. Seven candidates passed paired comparability but failed the warm-time screen and were labeled `comparable-but-slow`. Eleven candidates were `incomparable`. |
| Main uncertainty | Stage A is one tuning seed/shape, so it does not support a statistical ranking or broad scientific rejection. It does show that this exposed-parameter Stage A grid did not produce a candidate eligible for freeze. |
| Next justified action | Do not run Stage B, P04, held-out support, or large-N. Write a P03 stop handoff. Any continuation should be a separate reviewed repair plan that first classifies whether to pursue route-level performance repair, tuning repair for comparability/ESS failures, or both. |
| Not concluded | No candidate nomination, freeze, held-out support, speedup, posterior correctness, HMC readiness, public API/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or statistical ranking. |

## Evidence Contract Check

| Field | Contract Status |
| --- | --- |
| Question | Answered negatively for the Stage A exposed grid: no setting was viable enough to freeze. |
| Baseline/comparator | Existing compiled streaming actual-SIR route was used as paired comparator through the owned wrapper/harness. |
| Primary pass criterion | Failed: no candidate was `freeze-nominated`. |
| Veto diagnostics | Two ESS hard vetoes fired; no candidate passed warm-time support. |
| Explanatory diagnostics | Runtime ratios, log-likelihood deltas, factor residuals, and labels are recorded in row artifacts and aggregate. |
| Artifact | P03 Stage A aggregate/Markdown, row artifacts/logs, this result, P03 stop handoff, and Claude review ledger. |

## Stage A Artifacts

| Artifact | Path |
| --- | --- |
| Aggregate JSON | `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.json` |
| Aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.md` |
| Row JSON/Markdown artifacts | `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22-b1-t20-n256-*.json` and `.md` |
| Row logs | `docs/benchmarks/logs/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22-b1-t20-n256-*.log` |
| Umbrella log | `docs/benchmarks/logs/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.log` |

The umbrella log is zero bytes because the wrapper redirects each candidate
subprocess to its row-specific log.

## Command Run

```bash
timeout 7200 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --num-particles 256 \
  --time-steps 20 \
  --batch-seeds 81120 \
  --low-rank-ranks 16,32,64,128 \
  --low-rank-assignment-epsilons 0.25,0.125,0.0625,0.03125,0.015625 \
  --low-rank-max-projection-iterations-list 120 \
  --warmups 1 \
  --repeats 2 \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --tf32-mode enabled \
  --output docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.md \
  --quiet
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit recorded | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Python executable | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| Shape | `B=1,T=20,N=256,D=18,M=9`, seed `81120` |
| Device scope | `visible` |
| CUDA visible devices | `1` |
| Recorded GPU UUID | `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| TF32 | requested `enabled`; GPU/TF32 provenance complete for all 20 rows |
| Warmups/repeats | `warmups=1`, `repeats=2` |
| Aggregate wall time | `2201.163734322181` seconds |

## Local Checks

| Check | Result |
| --- | --- |
| Trusted GPU precheck | `PASS`: GPU1 idle before Stage A, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| P03 Stage A execute command | Completed and wrote aggregate/Markdown plus 20 row JSON/Markdown/log artifacts |
| Direct row-artifact integrity check | `PASS`: all 20 row JSON/Markdown/log paths exist; row JSON files parse and match the requested `B=1,T=20,N=256`, seed `81120`, and aggregate row statuses |
| Focused wrapper regression test | `PASS`: `13 passed in 0.39s` |
| Post-run GPU check | `PASS`: GPU1 returned to low memory/utilization state |

## Aggregate Summary

| Field | Value |
| --- | --- |
| Aggregate status | `FAIL` |
| Candidate count | `20` |
| Freeze-nominated | `0` |
| Comparable-but-slow | `7` |
| Incomparable | `11` |
| Hard-vetoed | `2` |
| Row statuses | `18 PASS`, `2 FAIL` |

The wrapper aggregate status is `FAIL` because two row statuses are `FAIL`.
That is a valid P03 result artifact and a phase failure to nominate, not a
wrapper or artifact failure.

## Candidate Summary

| Candidate | Status | Label | Comparable | Warm Screen | Mean Loglik Delta | Max Loglik Delta | Warm Ratio | Factor Residual |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `true` | `false` | `0.02410888671875` | `0.02410888671875` | `0.01661578978962335` | `1.4901161193847656e-08` |
| `r16_eps0p125_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `true` | `false` | `1.53289794921875` | `1.53289794921875` | `0.016465951404671726` | `2.9802322387695312e-08` |
| `r16_eps0p0625_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `true` | `false` | `4.40484619140625` | `4.40484619140625` | `0.01371426686468479` | `9.266659617424011e-08` |
| `r16_eps0p03125_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `6.12896728515625` | `6.12896728515625` | `0.010586529849848493` | `1.7415732145309448e-07` |
| `r16_eps0p015625_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `10.53973388671875` | `10.53973388671875` | `0.007728729030651798` | `2.9209069907665253e-05` |
| `r32_eps0p25_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `true` | `false` | `0.0255126953125` | `0.0255126953125` | `0.01766084069007282` | `2.8405338525772095e-07` |
| `r32_eps0p125_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `9.51336669921875` | `9.51336669921875` | `0.007290621135404812` | `0.00308467959985137` |
| `r32_eps0p0625_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `36.07684326171875` | `36.07684326171875` | `0.013609631240984243` | `0.000149591825902462` |
| `r32_eps0p03125_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `28.3297119140625` | `28.3297119140625` | `0.010218159471208453` | `9.532598778605461e-05` |
| `r32_eps0p015625_alpha1em08_it120` | `FAIL` | `hard-vetoed` | `false` | `false` | `6.08831787109375` | `6.08831787109375` | `0.008455183993493414` | `0.0005669957026839256` |
| `r64_eps0p25_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `true` | `false` | `0.00677490234375` | `0.00677490234375` | `0.016513046517512397` | `1.3969838619232178e-08` |
| `r64_eps0p125_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `true` | `false` | `2.3192138671875` | `2.3192138671875` | `0.014444945345756707` | `6.278511136770248e-06` |
| `r64_eps0p0625_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `9.66400146484375` | `9.66400146484375` | `0.012559786023742145` | `1.942063681781292e-05` |
| `r64_eps0p03125_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `22.84820556640625` | `22.84820556640625` | `0.010172186965038408` | `4.311325028538704e-06` |
| `r64_eps0p015625_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `26.3184814453125` | `26.3184814453125` | `0.007521710582940997` | `0.0004259762354195118` |
| `r128_eps0p25_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `true` | `false` | `0.0496826171875` | `0.0496826171875` | `0.018582506337490805` | `9.266659617424011e-08` |
| `r128_eps0p125_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `9.50115966796875` | `9.50115966796875` | `0.01278534657612099` | `5.702255293726921e-06` |
| `r128_eps0p0625_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `26.31585693359375` | `26.31585693359375` | `0.012694673876031218` | `4.752073436975479e-07` |
| `r128_eps0p03125_alpha1em08_it120` | `FAIL` | `hard-vetoed` | `false` | `false` | `45.3990478515625` | `45.3990478515625` | `0.007414628863153121` | `0.001975179184228182` |
| `r128_eps0p015625_alpha1em08_it120` | `PASS` | `incomparable` | `false` | `false` | `58.295166015625` | `58.295166015625` | `0.0074395950652360425` | `0.000388601009035483` |

Hard-vetoed candidates:

- `r32_eps0p015625_alpha1em08_it120`: `low_rank:ess_fraction_min_threshold`
- `r128_eps0p03125_alpha1em08_it120`: `low_rank:ess_fraction_min_threshold`

## Gate Assessment

| Gate | Status |
| --- | --- |
| Artifact completeness | `PASS`: aggregate, Markdown, 20 row artifacts, and row logs exist. |
| Actual-SIR semantics | `PASS` for reviewable rows; direct row-artifact integrity check confirmed the requested shape and seed in all row JSON files. |
| Low-rank provenance | `PASS`: complete for all 20 rows. |
| GPU/TF32 provenance | `PASS`: complete for all 20 rows on GPU1 UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`. |
| Hard-veto screen | `FAIL`: two candidates hard-vetoed on ESS. |
| Paired comparability | Mixed: seven candidates passed, thirteen did not pass or hard-vetoed. |
| Warm-time screen | `FAIL`: zero candidates passed. |
| Freeze nomination | `FAIL`: zero candidates were `freeze-nominated`. |

## Handoff Decision

Stage B must not run because Stage A produced no `freeze-nominated` candidate.
P04 must not start because no freeze-eligible candidate exists. The correct
handoff is the P03 stop handoff:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-stop-handoff-2026-06-22.md`

This is not classified as pure `ROUTE_REPAIR_REQUIRED` under the P03 subplan
because the Stage A outcome was mixed, not solely "comparable but warm-time
failed." Seven candidates were comparable-but-slow, eleven were incomparable,
and two hard-vetoed on ESS. The safest label is therefore
`NO_FREEZE_CANDIDATE_REPAIR_REQUIRED`, with a follow-on repair plan required to
separate route-performance repair from tuning repair.

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto evidence | Supported only for the two ESS-vetoed Stage A candidates. |
| Statistically supported ranking | Not supported. Stage A is one tuning seed/shape with no uncertainty analysis. |
| Descriptive-only differences | Runtime ratios and delta differences are descriptive except for the predeclared hard screens. |
| Default-readiness | Not supported. |
| Next evidence needed | A separately reviewed repair-classification plan that distinguishes low-rank route execution cost from exposed-parameter comparability/ESS failures before more held-out support. |

## Post-Run Red Team

The strongest alternative explanation is that the current low-rank route has
large Python/eager overhead or route-level inefficiency on actual-SIR for the
otherwise comparable candidates, while other regions of the parameter grid have
comparability or ESS problems. The result therefore triggers repair
classification rather than held-out support.

The weakest part of the evidence is that Stage A used one tuning seed/shape and
one iteration setting. That is enough to reject freezing under this P03 contract
because no candidate passed the required warm-time screen, but it is not enough
to rank all possible repairs or reject the research direction.

## Nonclaims

- No candidate was nominated or frozen.
- No held-out support was run.
- No speedup claim is supported.
- No posterior correctness claim is supported.
- No HMC readiness claim is supported.
- No public API/default readiness claim is supported.
- No dense Sinkhorn equivalence claim is supported.
- No broad scalable-OT selection claim is supported.
- No statistical ranking is supported.
