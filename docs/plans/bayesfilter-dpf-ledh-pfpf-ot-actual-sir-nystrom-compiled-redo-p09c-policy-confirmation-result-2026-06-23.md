# Actual-SIR Nystrom Compiled-Redo P09C Policy Confirmation Result

Date: 2026-06-23

Status: `PARTIAL_PASS_POLICY_TOO_NARROW_FOR_DEFAULT_READINESS`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Stop before P10 unless the owner accepts a narrow fixed policy or we repair numerical stability | `PARTIAL`: `rank=32,epsilon=0.3/0.5` passed, but `rank=64,epsilon=0.3` failed | Nonfinite Nystrom factors/particles/log-likelihood at `rank=64,epsilon=0.3` | The intended default `rank=32,epsilon=0.5` remains viable, but the policy neighborhood is narrow and rank sensitivity is unstable | Decide between narrow fixed-policy validation and implementation stabilization before stress gates | No default readiness, no broad robust policy, no statistical ranking, no superiority, no posterior correctness, no HMC readiness |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09c-policy-confirmation-plan-2026-06-23.md`
- Passing row JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09c-policy-r32-eps0p3-2026-06-23.json`
- Passing row JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09c-policy-r32-eps0p5-2026-06-23.json`
- Failing row JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09c-policy-r64-eps0p3-2026-06-23.json`

## Row Outcomes

| Row | Status | Hard vetoes | Max abs delta | Mean abs delta | Interpretation |
| --- | --- | --- | ---: | ---: | --- |
| `rank=32,epsilon=0.3` | `PASS` | `[]` | `1.51568603515625` | `0.731591796875` | Safe under this gate |
| `rank=32,epsilon=0.5` | `PASS` | `[]` | `3.67596435546875` | `2.21041259765625` | Intended default remains viable |
| `rank=64,epsilon=0.3` | `FAIL` | `['nystrom:nonfinite_log_likelihood', 'nystrom:nonfinite_nystrom_factors', 'nystrom:nonfinite_nystrom_particles']` | `nan` | `nan` | Numerical instability |

The grid stopped on the failing `rank=64,epsilon=0.3` row per the automatic
gate.  The planned `rank=64,epsilon=0.5` row was not launched.

## Classification

P09B showed that `epsilon=0.25` is unsafe and that raising epsilon rescues
`rank=32`.  P09C shows that the rescue does not generalize across rank: even
`epsilon=0.3` fails at `rank=64`.

Therefore this is not merely a one-knob epsilon tuning issue.  The repaired
compiled Nystrom route remains viable at the intended fixed setting
`rank=32,epsilon=0.5`, but the surrounding policy is numerically brittle.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | Sequential P09C policy-confirmation wrapper launching `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Trusted preflight selected physical GPU0 because GPU1 was memory-busy |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seeds | `81920,81921,81922,81923,81924` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09c-policy-confirmation-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09c-policy-confirmation-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for `rank=32,epsilon=0.3/0.5`; `FAIL` for `rank=64,epsilon=0.3` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Runtime, warm ratios, and relative deltas |
| Default-readiness | `NO` |
| Next evidence needed | Owner/research decision: narrow to a fixed `rank=32,epsilon=0.5` policy and stress-test, or repair rank/epsilon numerical instability first |

## Post-Run Red Team

Strongest alternative explanation: the intended default may be acceptable as a
fixed policy despite nearby settings failing, but default promotion usually
requires enough robustness that small configuration changes do not create
nonfinite outputs.

What would justify continuing to P10: explicitly narrow the candidate to a
fixed policy `rank=32,epsilon=0.5` and treat other rank/epsilon settings as
unsupported, with that limitation recorded in the runbook and final nonclaims.

What would justify repair first: require a broader stable policy neighborhood
before any stress/history/gradient gates.

## Next Action

Do not automatically continue to P10 under a broad Nystrom policy.  Choose one:

1. fixed-policy path: continue with `rank=32,epsilon=0.5` only, recording that
   P09 found nearby numerical brittleness;
2. stabilization path: repair the Nystrom factor/scaling numerics so the
   default neighborhood is stable, then rerun P09.
