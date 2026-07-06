# P04 Closeout Result: N8192 Paired-Drift Diagnostic

Date: 2026-06-23

Status: `CLOSED_REPLAYED_SINGLE_SEED_DRIFT_NOT_REPAIR_READY`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Close the lane as replayed single-seed drift: seed `82921` reproducibly fails, but nearby seeds `82922` and `82923` pass. |
| Primary criterion status | P01 completed and classified the drift. P02/P03 were not reached because `REPRODUCED_AND_REPEATED_DRIFT` did not occur. |
| Veto diagnostic status | Seed `82921` failed paired mean threshold; no harness, finite-output, residual, GPU/TF32, or metadata veto invalidated the artifacts. |
| Main uncertainty | Failure probability at `N=8192` is unknown; only two nearby seeds were checked. |
| Next justified action | If further action is desired, create a broader replication plan for additional `N=8192` seeds before repair/tuning. |
| What is not being concluded | No default readiness, no repair success, no statistical ranking, no posterior correctness, no HMC readiness, no broad rejection of Nystrom. |

## Phase Summary

| Phase | Status | Key evidence |
| --- | --- | --- |
| P00 Governance/review | `PASS` | Claude review round 2 returned `VERDICT: AGREE` after plan repair and explicit user approval for bounded review. |
| P01 Fixed-policy replay | `REPLAYED_SINGLE_SEED_DRIFT` | Seed `82921` failed again; seeds `82922` and `82923` passed. |
| P02 Repair selection | `NOT_REACHED` | Repair selection requires `REPRODUCED_AND_REPEATED_DRIFT`; P01 did not meet that condition. |
| P03 Focused repair test | `NOT_REACHED` | No repair was selected. |
| P04 Closeout | `COMPLETE` | This result closes the lane. |

## Artifact Index

Plan and ledgers:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-master-program-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-visible-gated-execution-runbook-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-visible-execution-ledger-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-claude-review-ledger-2026-06-23.md`

Phase results:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p00-governance-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p01-fixed-policy-replay-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p04-closeout-result-2026-06-23.md`

Benchmark artifacts:

- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.log`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82922-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82922-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-n8192-drift-p01-seed82922-r32-eps0p5-2026-06-23.log`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.log`

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Seed `82921` reproducibly fails paired mean threshold; nearby seeds passed. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Runtime, residual magnitudes, paired deltas on passing seeds, and factor/scaling diagnostics are descriptive only. |
| Default-readiness | No. |
| Next evidence needed | Broader `N=8192` replication before repair/tuning, if the owner wants to continue. |

## Interpretation

The original `N=8192` failure is real and reproducible for seed `82921`; it was
not caused by GPU0 selection, because the replay failed again on physical GPU1.
However, the failure did not repeat on the two nearby seeds. Under the reviewed
plan, that blocks repair selection and closes the lane as replayed single-seed
drift.

## Recommended Next Plan

The safest next plan, if continuing, is a broader replication gate at `N=8192`
under the same fixed policy before any repair:

- choose additional one-seed rows, for example seeds `82924..82931`;
- keep policy fixed;
- use the same paired comparator and thresholds;
- classify failure frequency descriptively only;
- open repair selection only if a predeclared repeated-drift threshold is met.

## Post-Run Red-Team Note

Strongest alternative explanation: seed `82921` may be a deterministic hard
case for this fixed low-rank approximation rather than representative high-N
behavior.

What would overturn this closeout: more predeclared `N=8192` seeds showing a
repeated failure pattern, or discovering artifact inconsistency in the replay.

Weakest part of the evidence: only two nearby seeds were tested, so failure
frequency is not estimated.
