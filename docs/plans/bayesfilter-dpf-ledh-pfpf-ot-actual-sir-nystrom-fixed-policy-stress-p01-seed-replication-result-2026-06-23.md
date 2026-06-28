# Fixed-Policy Stress P01 Seed Replication Result

Date: 2026-06-23

Status: `P01_PASS_SEED_REPLICATION`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Continue fixed-policy stress validation to the one-seed high-N ladder | `PASS`: both additional `N=1024,T=20` seed batches passed aggregate hard-veto and paired-threshold gates | `PASS`: no hard vetoes, no missing GPU/TF32 evidence, no selected-policy metadata drift | These are still finite seed batches without uncertainty analysis; they support viability, not superiority | Run P02 high-N ladder at fixed `rank=32,epsilon=0.5` | No default readiness, no broad rank/epsilon robustness, no statistical ranking, no posterior correctness, no HMC readiness |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Does fixed `rank=32,epsilon=0.5` remain stable under extra seed batches at `N=1024,T=20`? |
| Baseline/comparator | Compiled streaming TF32 route in each paired artifact. |
| Primary pass/fail criterion | `PASS`: both launched rows have aggregate `status == PASS`. |
| Veto diagnostics | `PASS`: no aggregate hard vetoes, GPU/TF32 evidence present, fixed-policy metadata present, finite outputs, residual and paired thresholds pass. |
| Explanatory only | Runtime, warm timing ratio, factor/scaling ranges, denominator floor hits. |
| Not concluded | No default readiness, no superiority/ranking, no broad rank/epsilon robustness, no posterior correctness, no HMC readiness. |

## Artifacts

P01A:

- JSON: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p01a-r32-eps0p5-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p01a-r32-eps0p5-2026-06-23.md`
- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-stress-p01a-r32-eps0p5-2026-06-23.log`

P01B:

- JSON: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p01b-r32-eps0p5-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p01b-r32-eps0p5-2026-06-23.md`
- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-stress-p01b-r32-eps0p5-2026-06-23.log`

## Row Outcomes

| Row | Seeds | Status | Hard vetoes | Paired max abs delta | Paired mean abs delta | Row residual | Column residual | Wall seconds |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| P01A | `81925..81929` | `PASS` | `[]` | `2.5533447265625` | `2.08074951171875` | `9.679794311523438e-05` | `2.86102294921875e-06` | `37.1398170478642` |
| P01B | `81930..81934` | `PASS` | `[]` | `3.33306884765625` | `2.1892333984375` | `9.393692016601562e-05` | `2.86102294921875e-06` | `36.23106087720953` |

Both rows used:

- `N=1024`, `T=20`;
- `rank=32`, `epsilon=0.5`;
- `kernel_mode=raw`;
- `scaling_normalization=none`;
- trusted physical GPU1;
- TF32 enabled.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for both additional seed batches. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Runtime and warm timing ratios are descriptive only. |
| Default-readiness | `NO`. |
| Next evidence needed | P02 one-seed high-N ladder at the fixed policy. |

## Post-Run Red Team

Strongest alternative explanation: the fixed policy may be stable at `N=1024`
but fail at larger particle counts or under history/gradient/HMC use.

What would overturn this P01 decision: invalid artifact evidence or a rerun of
the same fixed-policy rows producing hard vetoes without changing thresholds or
metadata.

Weakest part of evidence: pass/fail seed replication without uncertainty
analysis does not justify ranking or default promotion.

## Next Action

Run P02 high-N ladder at fixed `rank=32,epsilon=0.5`, beginning with
`N=2048`, seed `82920`.
