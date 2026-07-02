# Phase 9 Evidence Contract: Trusted GPU Ladder

date: 2026-06-23
phase: P9-GPU-LADDER
status: WRITTEN_BEFORE_GPU_LAUNCH

## Governing Paths

- P8 manifest:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json`
- P8 audit:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json`
- P9 run manifest:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-run-manifest-2026-06-23.json`
- P9 rung ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-rung-ledger-2026-06-23.json`

## Evidence Contract

| Field | Contract |
|---|---|
| Scientific or engineering question | Does the exact audited no-production-autodiff `manual-reverse` route produce finite five-seed SIR actual gradients through N10000 on trusted GPU/TF32? |
| Baseline/comparator | S7R blocker: N2500 OOM on the partial manual route with outer autodiff, plus P8 exact-route audit pass.  Zhao-Cui is not a comparator or oracle. |
| Primary promotion/pass criterion | N10000 exits 0 and validates with manual-reverse, FD disabled, streaming transport, stabilized transport AD mode, selected manual streaming finite transport gradient mode, finite objective/gradient/MCSE, five seeds, GPU placement, P8 manifest/audit binding in the P9 run manifest, and an ordered rung ledger showing no prior non-`PASSED` rung. |
| Diagnostics that can veto | Trusted GPU preflight failure; pre-N100 P8 audit/manifest validation failure; rung OOM/nonzero/timeout; rung validation failure; rung decision `BLOCKED` or `FAILED`; higher rung launched after first non-`PASSED`; missing or mismatched P8 manifest/audit; wrong route; CPU placement; nonfinite values; FD launched; Zhao-Cui comparator introduced; `transport_ad_mode=full` used. |
| Diagnostics that are explanatory only | Runtime and memory trends, allocator warnings, intermediate N100/N1000/N2500/N5000 values if later rungs pass, per-seed gradient spread, and progress-file updates. |
| What will not be concluded | FD agreement, posterior correctness, HMC readiness, production default, statistical superiority, or scientific validity. |
| Artifact preserving the result | P9 run manifest, P9 rung ledger, per-rung JSONs, P9 result, updated stop handoff, and P10 subplan only if N10000 passes. |

## Explicit Boundaries

finite differences are forbidden in P9.

Zhao-Cui is not a comparator or oracle.

`transport_ad_mode=full` is forbidden.

`reverse-gradient` and `forward-jvp` are diagnostic-only and forbidden for P9
rungs.

No posterior, HMC, default-policy, or scientific-validity claim can be made
from P9.
