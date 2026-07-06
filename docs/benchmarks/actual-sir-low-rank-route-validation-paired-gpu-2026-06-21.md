# Actual-SIR Low-Rank Paired GPU Aggregate

Date: 2026-06-21

Status: `TUNING_REQUIRED`

## Contract

This P03 aggregate tests whether the existing TensorFlow low-rank coupling
solver route can support bounded efficiency evidence on paired actual-SIR d18
LEDH/PFPF-OT rows versus the existing compiled streaming route.

Promotion support required at least two adjacent paired rows with no hard
vetoes, no paired comparability vetoes, same physical GPU UUID, exact
`warmups=1`, `repeats=3`, and warm median `streaming / low_rank >= 1.25`.

## Row Evidence

| Row | Status | GPU UUID | Streaming warm median s | Low-rank warm median s | Ratio streaming/low-rank | Hard vetoes | Support role |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `B=5,T=20,N=1024` | `PASS` | `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` | 0.9723010780289769 | 58.549089503940195 | 0.016606596042173186 | `[]` | fails support gates |

Row artifacts:

- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.md`

## Gate Assessment

| Gate | Status |
| --- | --- |
| Actual-SIR semantics | `PASS` |
| GPU/TF32 provenance | `PASS`; GPU1 UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Hard validity | `PASS`; no hard vetoes |
| Low-rank factors | `PASS`; finite/nonnegative factors, positive `g`, max factor marginal residual `8.986273314803839e-06` |
| Paired log-likelihood comparability | `FAIL`; max absolute delta `58.0933837890625`, mean absolute delta `42.93328857421875` |
| Paired filtered summaries | Mixed descriptive deltas; relative mean and RMS variance alternatives pass, but these do not rescue the log-likelihood comparability failure |
| Warm-time screen | `FAIL`; warm median ratio `0.016606596042173186`, below required `1.25` |
| Adjacent support rows | `FAIL`; zero support rows passed |

## Decision

The first required paired actual-SIR GPU row executed and preserved hard
validity/factor/nonmaterialization evidence, but it failed the paired
comparability and warm-time promotion screens. The P03 ladder stops here as
`TUNING_REQUIRED`; larger P03/P04 rows are not valid support evidence under
this program until a new tuning or route-repair plan re-establishes the P03
entry and handoff conditions.

## Nonclaims

- No speedup claim.
- No large-N executable-envelope claim for this actual-SIR lane.
- No posterior correctness, HMC readiness, public API readiness, or
  production/default readiness claim.
- No dense Sinkhorn equivalence, broad scalable-OT selection, or statistical
  ranking claim.
