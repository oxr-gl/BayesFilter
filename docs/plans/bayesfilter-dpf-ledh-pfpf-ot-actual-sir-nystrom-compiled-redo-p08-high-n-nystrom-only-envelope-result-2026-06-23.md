# Actual-SIR Nystrom Compiled-Redo P08 High-N Nystrom-Only Envelope Result

Date: 2026-06-23

Status: `PASS_HIGH_N_FEASIBILITY_ENVELOPE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to P09 rank/epsilon sensitivity | `PASS`: new P08 Nystrom-only rows at `N=16384,32768,65536` all wrote artifacts with `status=PASS` | No hard vetoes; residual thresholds passed; GPU/TF32/JIT evidence present | Nystrom-only rows do not test paired quality; one seed per row; timing/memory are descriptive | Run P09 sensitivity at moderate shape before any default-readiness discussion | No paired quality at `N>=16384`, no default readiness, no statistical ranking, no superiority, no posterior correctness, no HMC readiness |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p08-high-n-nystrom-only-envelope-plan-2026-06-23.md`
- N16384 JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n16384-2026-06-23.json`
- N32768 JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n32768-2026-06-23.json`
- N65536 JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n65536-2026-06-23.json`

## Row Summary

| N | Seed | Status | Hard vetoes | Compile plus first | Warm median | Max row residual | Max column residual | Wall time |
| ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `16384` | `81620` | `PASS` | `[]` | `12.587190570076928s` | `0.4046340058557689s` | `9.107589721679688e-05` | `2.86102294921875e-06` | `14.055280024884269s` |
| `32768` | `81720` | `PASS` | `[]` | `13.484218016965315s` | `0.8095715930685401s` | `8.690357208251953e-05` | `4.76837158203125e-06` | `15.353491581045091s` |
| `65536` | `81820` | `PASS` | `[]` | `14.494778723921627s` | `1.6103871630039066s` | `9.882450103759766e-05` | `4.76837158203125e-06` | `17.143998679937795s` |

All three rows used:

- `B=1,T=20,D=18,M=9`
- route `nystrom`
- `rank=32`, `epsilon=0.5`, `max_iterations=160`
- `float32`, TF32 enabled, JIT compile enabled
- physical GPU0 because GPU1 was memory-busy

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Commands | The three P08 commands recorded in `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p08-high-n-nystrom-only-envelope-plan-2026-06-23.md`, run with `CUDA_VISIBLE_DEVICES=0` through the harness argument |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Trusted preflight before each row; physical GPU0 selected because GPU1 was memory-busy |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seeds | `81620,81720,81820` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p08-high-n-nystrom-only-envelope-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p08-high-n-nystrom-only-envelope-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for Nystrom-only feasibility through `N=65536` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Runtime, memory, warm timings, and residual magnitudes below threshold |
| Default-readiness | `NO` |
| Next evidence needed | P09 rank/epsilon sensitivity, followed by transport/history stress and gradient/HMC mechanics |

## Interpretation

The repaired compiled Nystrom route is feasible on the actual-SIR harness up to
`N=65536` for one-seed, value-only, active-all, Nystrom-only rows.  The rows
preserve finite outputs, small residuals, route invocation evidence, and GPU
TF32 execution.

This does not establish paired quality for `N>=16384`, nor does it support a
runtime superiority ranking.  It supports continuing the promotion-or-rejection
runbook to sensitivity and stress gates.

## Post-Run Red Team

Strongest alternative explanation: the fixed `rank=32,epsilon=0.5` candidate
may be feasible but brittle; other ranks, epsilons, seeds, history modes,
transport policies, or gradient/HMC use may still fail.

What would overturn continuation: P09 showing rank/epsilon brittleness, P10
history or transport-policy failures, or P11 gradient/HMC mechanics failures.

## Next Action

Plan P09 rank/epsilon sensitivity before running more scale rows.  Suggested
first grid: ranks `16,32,64` and epsilons `0.25,0.5,1.0` at
`B=5,T=20,N=1024`, using paired compiled streaming comparator and treating
timing as descriptive.
