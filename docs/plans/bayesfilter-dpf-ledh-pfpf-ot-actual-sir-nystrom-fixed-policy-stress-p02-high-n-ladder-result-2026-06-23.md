# Fixed-Policy Stress P02 High-N Ladder Result

Date: 2026-06-23

Status: `P02_PASS_HIGH_N_LADDER`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Treat the fixed `rank=32,epsilon=0.5` policy as passing this one-seed high-N hard screen through `N=8192` | `PASS`: `N=2048`, `N=4096`, and `N=8192` rows passed aggregate hard-veto and paired-threshold gates | `PASS`: no hard vetoes, no missing GPU/TF32 evidence, no selected-policy metadata drift, no runtime stop | One seed per N cannot establish statistical robustness or ranking | Close this stress runbook as fixed-policy viability evidence and require a separate promotion/stress program for default-readiness claims | No default readiness, no broad rank/epsilon robustness, no statistical ranking, no superiority, no posterior correctness, no HMC readiness |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Does fixed `rank=32,epsilon=0.5` remain stable under a one-seed high-N ladder? |
| Baseline/comparator | Compiled streaming TF32 route in each paired artifact. |
| Primary pass/fail criterion | `PASS`: all launched high-N rows have aggregate `status == PASS`. |
| Veto diagnostics | `PASS`: no aggregate hard vetoes, GPU/TF32 evidence present, fixed-policy metadata present, finite outputs, residual and paired thresholds pass, no runtime stop. |
| Explanatory only | Runtime, warm timing ratio, factor/scaling ranges, denominator floor hits. |
| Not concluded | No default readiness, no superiority/ranking, no broad rank/epsilon robustness, no posterior correctness, no HMC readiness. |

## Artifacts

N2048:

- JSON: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p02-n2048-r32-eps0p5-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p02-n2048-r32-eps0p5-2026-06-23.md`
- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-stress-p02-n2048-r32-eps0p5-2026-06-23.log`

N4096:

- JSON: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p02-n4096-r32-eps0p5-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p02-n4096-r32-eps0p5-2026-06-23.md`
- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-stress-p02-n4096-r32-eps0p5-2026-06-23.log`

N8192:

- JSON: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p02-n8192-r32-eps0p5-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p02-n8192-r32-eps0p5-2026-06-23.md`
- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-stress-p02-n8192-r32-eps0p5-2026-06-23.log`

## Row Outcomes

| N | Seed | Status | Hard vetoes | Paired max abs delta | Paired mean abs delta | Row residual | Column residual | Wall seconds |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 2048 | `82920` | `PASS` | `[]` | `4.3642578125` | `4.3642578125` | `9.572505950927734e-05` | `2.384185791015625e-06` | `31.865204110974446` |
| 4096 | `82920` | `PASS` | `[]` | `2.37554931640625` | `2.37554931640625` | `9.47713851928711e-05` | `3.337860107421875e-06` | `30.53900373610668` |
| 8192 | `82920` | `PASS` | `[]` | `2.5208740234375` | `2.5208740234375` | `9.012222290039062e-05` | `3.814697265625e-06` | `32.74824697198346` |

All rows used:

- `T=20`;
- `rank=32`, `epsilon=0.5`;
- `kernel_mode=raw`;
- `scaling_normalization=none`;
- trusted physical GPU1;
- TF32 enabled.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for `N=2048`, `N=4096`, and `N=8192`. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Runtime and warm timing ratios are descriptive only. |
| Default-readiness | `NO`. |
| Next evidence needed | Separate promotion/stress program if the owner wants default-readiness evidence. |

## Post-Run Red Team

Strongest alternative explanation: the one-seed ladder may miss seed-specific
high-N failures, history-mode memory pressure, or HMC/gradient issues.

What would overturn this P02 decision: any repeated high-N fixed-policy artifact
showing nonfinite outputs, residual vetoes, paired threshold failures, or a
runtime envelope failure under the same predeclared policy.

Weakest part of evidence: one seed per N is a hard screen only, not uncertainty
evidence.

## Next Action

Proceed to P03 closeout.  Do not claim default readiness without a separate
reviewed promotion/stress program covering replication, history/memory, and
HMC/gradient gates.
