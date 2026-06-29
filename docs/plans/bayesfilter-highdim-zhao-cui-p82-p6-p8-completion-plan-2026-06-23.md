# P82 Completion Plan: P6-P8 And Closeout

status: REVIEWED_CLAUDE_R4_AGREE_READY_FOR_P6
date: 2026-06-23
supervisor_executor: Codex
readonly_reviewer: Claude Opus, one-path bounded review only

## Objective

Finish the active P82 FD-only LEDH-PFPF-OT SIR d18 gradient program after the
P5 manual streaming transport-gradient wiring pass.

The active route is:

```text
transport_plan_mode=streaming
transport_gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys
transport_ad_mode=stabilized
```

The old raw/full-AD route remains forbidden for governed P82 validation.
Zhao-Cui remains out of the active pass/fail comparator path.

## Phase Ladder

| Phase | Objective | Subplan | Required result |
|---|---|---|---|
| P6 | Tiny trusted GPU smoke of the manual streaming route. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-result-2026-06-23.md` |
| P7 | Actual-gradient feasibility ladder ending, if feasible, in the N10000 five-seed actual-gradient artifact. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md` |
| P8 | Governed N1000 five-seed 13-point regression-FD comparison against the P7 N10000 actual-gradient artifact. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-consistency-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-consistency-result-2026-06-23.md` |
| P9 | Closeout and execution review. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-result-2026-06-23.md` |

## Standing Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the P5-wired manual streaming LEDH-PFPF-OT route produce finite, GPU-visible, five-seed SIR d18 gradients and a governed FD consistency comparison without using the known-bad full-AD route? |
| Comparator | Same-scalar LEDH regression FD only.  FD is noisy diagnostic evidence, not an oracle. |
| Primary pass criterion | P6 and P7 pass their route/feasibility gates; P8 explicitly runs `--fd-mode enabled`, records `regression_fd.fd_mode=enabled`, finite N10000 actual-gradient components, finite N1000 FD slopes and slope SEs for the raw theta directions, and all discrepancy rows are no more than 2 combined SE or are explicitly downgraded as diagnostic issues. |
| Veto diagnostics | Any `transport_ad_mode=full` governed rerun; missing trusted GPU preflight; wrong route metadata; GPU not visible when expected; nonfinite objective/gradient/slope/SE; missing five seeds for P7/P8; missing 13 raw FD points or 11 value-trimmed fit points; wrong trim mode; OOM or timeout; hidden theta/data/direction mismatch; unsupported Zhao-Cui/oracle/HMC/default/scientific-superiority claims. |
| Explanatory diagnostics | Runtime, TensorFlow warnings, device placement, TF32 mode, chunk metadata, GPU memory metadata where available, gradient MCSE, FD slope SE, regression residuals, and route metadata. |
| Not concluded | Posterior correctness, HMC readiness, default readiness, exact likelihood correctness, scientific superiority, production readiness, Zhao-Cui comparator readiness, or calibrated hypothesis-test validity of the 2-SE heuristic. |
| Preserving artifacts | Phase JSON outputs, progress JSON outputs where used, phase results, updated execution/review ledgers, and final closeout. |

## Skeptical Audit

- Wrong baseline: controlled by keeping Zhao-Cui out of the active comparator
  path and comparing LEDH actual-gradient against same-scalar LEDH FD only.
- Proxy promotion: controlled by treating P6/P7 as mechanics/feasibility only
  and P8 as diagnostic FD consistency, not scientific correctness.
- Known-bad route: controlled by forbidding `transport_ad_mode=full` and
  requiring `transport_ad_mode=stabilized` plus manual gradient-mode metadata.
- Environment mismatch: controlled by trusted/escalated `nvidia-smi`,
  TensorFlow GPU probe, and GPU-output-device validation.
- Runtime risk: controlled by `timeout` wrappers and stop-on-timeout blockers.
- FD noise: controlled by the governed 13-point, five-seed, value-trimmed,
  11-point OLS protocol with explicit slope SE and explicit
  `--fd-mode enabled`.
- SE interpretation: combined SE is a triage heuristic.  It combines P7
  seed-MCSE and P8 line-fit slope SE as a practical issue detector; passing
  within 2 combined SE is not proof of correctness.

Audit result: `READY_FOR_CLAUDE_PLAN_REVIEW`.

## Review And Execution Rules

- Review this completion plan with Claude using exactly this path, not pasted
  code and not a broad artifact packet.
- If Claude returns `REVISE`, patch this plan or the named subplan visibly and
  rerun focused local checks before retrying review.
- Execute phases in order.  Do not start P7 until P6 passes, has a result,
  and the P6 result has one-path Claude review status `VERDICT: AGREE`.  Do
  not start P8 until P7 has a valid N10000 actual-gradient artifact.
- Review the final execution/closeout result with Claude using exactly the P9
  result path.
- If any phase hits a veto, write the result/blocker and stop; do not skip
  forward to the next phase.
