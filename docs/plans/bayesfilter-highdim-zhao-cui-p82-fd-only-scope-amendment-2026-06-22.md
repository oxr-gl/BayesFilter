# P82 Scope Amendment: FD-Only LEDH Consistency Check

status: SUPERSEDED_ACTIVE_COMPARATOR_CONTRACT_ONLY
date: 2026-06-22

## Human Instruction

The human owner instructed:

```text
remove Zhao-cui as the comparator for now and check consistency with FD only.
```

This amendment superseded the P3 Zhao-Cui comparator blocker for the purpose of
continuing P82 execution.  It does not erase the P3 audit result.  The P3
result remains valid for the original Zhao-Cui-comparator scope.

Later on 2026-06-22, the human owner corrected the route choice: raw
`transport_ad_mode=full` autodiff/JVP through the whole Sinkhorn transport solve
had already been established as infeasible for governed `N=10000` evidence.
Therefore this amendment remains active only as the FD comparator contract.
P82 execution is blocked until a memory-disciplined LEDH actual-gradient route
exists.

## Revised Objective

Check same-scalar LEDH-PFPF-OT SIR d=18 gradient consistency using the corrected
regression-FD protocol only.

Zhao-Cui is removed from the P82 pass/fail path for now.  Zhao-Cui artifacts
must not be used as comparator evidence in this amended program.

## Revised Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the differentiable LEDH-PFPF-OT SIR d=18 gradient agree with regression-FD slopes of the same LEDH scalar under the corrected 13-point, five-seed protocol? |
| Baseline/comparator | Regression FD of the same LEDH scalar along predeclared directions.  FD is a noisy diagnostic comparator, not an oracle. |
| Primary criterion | For each predeclared raw theta direction, the N=10000 LEDH actual-gradient component and the N=1000 regression-FD slope are finite, have recorded uncertainty, and differ by no more than 2 combined SE unless residual, linearity, or runtime diagnostics downgrade the row instead of promoting it. |
| Veto diagnostics | Missing trusted GPU preflight, wrong transport AD contract, missing five seeds, missing `--trim-extreme-mode value`, missing 13 raw FD points or 11 retained fit points, nonfinite objective/gradient/slope/SE, FD line too nonlinear to interpret, unbounded runtime/OOM, hidden theta/data/direction mismatch, or unsupported Zhao-Cui/oracle/HMC/default/scientific-superiority claims. |
| Explanatory diagnostics | Runtime, GPU placement, TF32 status, gradient seed MCSE, FD slope SE, FD residuals/R2, dropped value-outlier points, transport mode, progress JSON, and memory/chunk metadata. |
| Not concluded | Posterior correctness, exact likelihood correctness, HMC/NUTS readiness, default-gradient readiness, production readiness, scientific superiority, Zhao-Cui source-faithfulness, or manual-adjoint correctness. |
| Preserving artifacts | This amendment, updated P82 ledgers/handoff, FD-only subplan/result, JSON outputs, and any progress JSON. |

## Fixed FD-Only Protocol

| Decision | Binding rule |
|---|---|
| Theta convention | `log_kappa_scale`, `log_nu_scale`, `log_obs_noise_scale`; use theta `0.02,-0.01,0.01` unless a later subplan changes it before results. |
| Directions | First FD-only gate uses raw parameter directions so N=10000 gradient components compare directly to N=1000 FD slopes. |
| Actual gradient | N=10000 particles, five fixed seeds `81120,81121,81122,81123,81124`, GPU TF32, active-all LEDH-PFPF-OT, using a reviewed memory-disciplined gradient route.  Raw `transport_ad_mode=full` autodiff/JVP through the whole Sinkhorn transport solve is not an executable governed N=10000 route. |
| Regression FD | N=1000 particles, same five fixed seeds, 13 batched theta offsets `-6..6`, `--trim-extreme-offsets 1`, `--trim-extreme-mode value`, OLS on 11 retained mean objective values, slope SE recorded. |
| FD batching | Use `--fd-evaluation-mode batched-theta` when feasible; use `--theta-offset-batch-size` if memory requires chunking. |
| Runtime safety | Start with a tiny trusted GPU smoke before N=10000/N=1000 governed runs.  Use progress JSON for longer FD runs. |
| 2-SE rule | Triage heuristic only.  `<=2` combined SE is not certification; `>2` combined SE is a likely issue requiring investigation. |

## Route Implications

- P3 `BLOCK_P82_P3_ANALYTICAL_COMPARATOR_ROUTE_NOT_READY` remains recorded for
  the original Zhao-Cui-comparator scope.
- P82 may continue under this amended FD-only comparator scope without
  implementing the Zhao-Cui analytical comparator, but not until a
  memory-disciplined LEDH actual-gradient route exists.
- Raw full autodiff/JVP through the whole Sinkhorn transport solve is allowed
  only for tiny/small primitive diagnostics, not for the governed N=10000
  actual-gradient route.
- Regression FD is the comparator diagnostic, not an oracle.

## Skeptical Plan Audit

Superseded by route correction.  The amended plan fixes the wrong-baseline risk by
removing Zhao-Cui from the pass/fail path.  It avoids proxy promotion by
keeping FD diagnostic-only and requiring residual/linearity diagnostics.  It
keeps the earlier user corrections on 13-point value-trim FD, five seeds, N=1000
FD, and N=10000 actual gradient.  The main remaining blocker is the actual
gradient route: the prior raw full-AD route is known infeasible and must be
replaced before P82 FD-only validation can resume.

## Next Artifact

Execute the upstream manual/custom-adjoint program:

`docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-master-program-2026-06-22.md`
