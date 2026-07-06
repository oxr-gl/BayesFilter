# P02 Tiny Actual-SIR Tuning Smoke Result

Date: 2026-06-22
Status: `PASS`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P02 passed. The four-candidate tiny actual-SIR mini-grid executed in trusted GPU context and wrote complete aggregate, row, Markdown, and log artifacts. |
| Primary criterion status | Passed. All four row subprocesses exited `0`; aggregate status is `PASS`; row statuses are `PASS`; hard veto lists are empty; actual-SIR semantics, route-fired evidence, factor validity, and GPU/TF32 provenance are present. |
| Veto diagnostic status | No P02 hard-veto or schema veto fired. |
| Main uncertainty | All four candidates were `comparable-but-slow` on the tiny smoke. This is explanatory only for P02 and does not reject the tuning direction. |
| Next justified action | Advance to P03 after refreshing the tuning-screen subplan with exact row budget, commands, stop conditions, and freeze-nomination semantics. |
| Not concluded | No candidate nomination, tuning success, speedup, posterior correctness, HMC readiness, public API/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or statistical ranking. |

## Evidence Contract Check

| Field | Contract Status |
| --- | --- |
| Question | Answered: the chosen wrapper execution path can run a tiny actual-SIR four-candidate mini-grid and write reviewable artifacts. |
| Baseline/comparator | Existing compiled streaming actual-SIR route paired with low-rank route through the owned validation harness. |
| Primary pass criterion | Passed by artifact completeness and hard-validity diagnostics. |
| Veto diagnostics | Nonfinite output, missing actual-SIR semantics, route-fired mismatch, dense materialization, invalid factors, missing artifact, and missing GPU evidence did not fire. |
| Explanatory diagnostics | Paired deltas, warm-time ratios, projection/factor residuals, and row wall times were recorded but are not promotion evidence. |
| Artifact | P02 JSON, Markdown, row artifacts, row logs, and this result. |

## Artifacts

| Artifact | Path |
| --- | --- |
| Aggregate JSON | `docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.json` |
| Aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.md` |
| Row JSON/Markdown artifacts | `docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22-b1-t3-n128-*.json` and `.md` |
| Row logs | `docs/benchmarks/logs/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22-b1-t3-n128-*.log` |
| Umbrella log | `docs/benchmarks/logs/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.log` |

The umbrella log is zero bytes because the wrapper redirected each subprocess
to its candidate-specific row log. The row logs are present and nonempty.

## Command Run

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --num-particles 128 \
  --time-steps 3 \
  --batch-seeds 81120 \
  --low-rank-ranks 16,32 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --warmups 0 \
  --repeats 1 \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --tf32-mode enabled \
  --output docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.md \
  --quiet
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit recorded | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` |
| Python executable | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| Python version | `3.13.13` |
| Working directory | `/home/ubuntu/python/BayesFilter` |
| Started | `2026-06-21T18:43:14.295820+00:00` |
| Ended | `2026-06-21T18:45:27.837719+00:00` |
| Aggregate wall time | `133.5828427860979` seconds |
| Device scope | `visible` |
| CUDA visible devices | `1` |
| Recorded GPU UUID | `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| TF32 | requested `enabled`; recorded execution true in row precision payloads |
| Shape | `B=1,T=3,N=128,D=18,M=9`, seed `81120` |

## Local Checks

| Check | Result |
| --- | --- |
| P02 execute command | `PASS`, exit `0` |
| Aggregate parse and schema inspection | `PASS`, `schema_version=actual_sir_low_rank_tuning_grid.v1`, `status=PASS`, `mode=execute` |
| Focused wrapper regression test | `PASS`: `13 passed in 0.39s` |
| Row log presence | `PASS`: four candidate row logs are nonempty |

## Candidate Summary

| Candidate | Status | Label | Hard Vetoes | Paired Comparable | Warm-Time Screen | Loglik Max Delta | Factor Residual | Warm Ratio |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `[]` | `true` | `false` | `0.00263214111328125` | `1.4901161193847656e-08` | `0.012154425138772592` |
| `r16_eps0p125_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `[]` | `true` | `false` | `0.0168914794921875` | `1.126900315284729e-07` | `0.01617081738589941` |
| `r32_eps0p25_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `[]` | `true` | `false` | `0.00678253173828125` | `2.2398307919502258e-07` | `0.011736951328262074` |
| `r32_eps0p125_alpha1em08_it120` | `PASS` | `comparable-but-slow` | `[]` | `true` | `false` | `0.04239654541015625` | `2.146698534488678e-07` | `0.006644095295879186` |

All four rows recorded:

- actual-SIR semantics pass;
- low-rank route invocations `3` with `3` active resampling steps;
- no dense low-rank transport materialization;
- finite/nonnegative factors and positive `g`;
- complete visible GPU/TF32 provenance for P02 purposes.

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for all four tiny smoke rows. |
| Statistically supported ranking | Not supported and not attempted. |
| Descriptive-only differences | Warm-time ratios and delta magnitudes are smoke diagnostics only. |
| Candidate nomination | None. `num_freeze_nominated=0`; P02 is not a nomination phase. |
| Default-readiness | Not supported. |
| Next evidence needed | P03 actual-SIR tuning screen with predeclared row budget and explicit freeze-nomination rule. |

## P03 Handoff

P03 may start only after its subplan is refreshed and reviewed. The refreshed
P03 subplan must explicitly state that a `freeze-nominated` candidate requires
hard validity, paired comparability, warm-time screen pass, low-rank provenance,
and visible GPU/TF32 provenance on every P03 tuning row it ran. A valid but
slow P03 outcome should trigger route-repair planning rather than held-out
support.

## Nonclaims

- No speedup claim.
- No candidate freeze or held-out support claim.
- No posterior correctness claim.
- No HMC readiness claim.
- No public API or default-readiness claim.
- No dense Sinkhorn equivalence claim.
- No broad scalable-OT selection claim.
- No statistical ranking claim.
