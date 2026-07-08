# P82 Master Program: LEDH-PFPF-OT SIR d=18 Regression-FD Gradient Test

status: P6_P8_COMPLETION_PLAN_DRAFTED_PENDING_REVIEW
date: 2026-06-22
supervisor_executor: Codex
readonly_reviewer: Claude Opus, bounded fact-packet review only

## Objective

Execute a governed, visible, phase-gated program to test LEDH-PFPF-OT gradient
behavior on the SIR d=18 target using the corrected regression finite-difference
protocol.

As of the 2026-06-22 human amendment, Zhao-Cui is removed from the P82
comparator for now.  The original P3 Zhao-Cui blocker remains recorded, but the
P82 pass/fail path is now same-scalar LEDH actual-gradient versus regression-FD
consistency only.  LEDH-PFPF-OT is approximate, and regression FD is diagnostic,
not an oracle.

As of the later 2026-06-22 full-AD route correction, P82 was
downstream-blocked: the actual-gradient side had to come from a reviewed
memory-disciplined LEDH-PFPF-OT route, not raw `transport_ad_mode=full`
autodiff/JVP through the whole Sinkhorn transport solve at `N=10000`.

As of P5 on 2026-06-23, the manual streaming transport-gradient route is wired
through the P82 benchmark path.  P6-P8 now proceed only through that manual
route and only after the completion plan passes review.

## Required Inputs

- `docs/plans/bayesfilter-highdim-zhao-cui-p81-analytical-derivative-route-correction-2026-06-22.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p81-ledh-pfpf-ot-gradient-testing-protocol-correction-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-reset-memo-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-inventory-result-2026-06-22.md`
- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`

## Standing Evidence Contract

| Field | Contract |
|---|---|
| Question | Can LEDH-PFPF-OT produce SIR d=18 directional gradient estimates that are finite, reproducible over five fixed seeds, and consistent with regression-FD slopes of the same LEDH scalar within stated uncertainty? |
| Baseline/comparator | LEDH-PFPF-OT regression FD for the same scalar.  FD is noisy diagnostic evidence, not an oracle. |
| Primary pass criterion | For predeclared directions, LEDH actual-gradient directional estimates and regression-FD slopes have finite values, finite standard errors, stable diagnostics, and discrepancies no greater than 2 combined standard errors, unless a documented route/linearity explanation downgrades the row instead of promoting it. |
| Veto diagnostics | Reintroducing Zhao-Cui as comparator evidence; treating FD as an oracle; central-difference-only promotion; missing five-seed standard errors; missing 13-point value-outlier-trim regression; nonfinite values/gradients/slopes; missing trusted GPU preflight before GPU work; hidden theta/data/direction mismatch; changing thresholds after results; OOM or unbounded runtime; unsupported oracle/HMC/default/scientific-superiority claims. |
| Explanatory diagnostics | Runtime, device placement, TF32 mode, transport residuals, ESS where available, regression R2, regression max residual, slope SE, per-seed gradient covariance, adjacent step-window slope stability, memory/chunk metadata. |
| Not concluded | Posterior correctness, HMC/NUTS readiness, default-gradient readiness, streaming memory improvement, exact likelihood correctness, scientific superiority, production readiness, Zhao-Cui comparator readiness, or manual-adjoint correctness. |
| Preserving artifacts | This master program, visible runbook, execution ledger, Claude review ledger, phase subplans, phase results, JSON outputs, and final stop handoff. |

## Fixed Protocol Decisions

| Decision | Binding rule |
|---|---|
| Theta convention | `log_kappa_scale`, `log_nu_scale`, `log_obs_noise_scale`; record exact theta vector in every run. |
| Regression FD | 13 line points; evaluate in batched theta-offset form when feasible; five fixed seeds; N=1000 particles per line point; average over seeds at each offset; explicitly pass `--trim-extreme-mode value`; drop highest and lowest mean-over-seed values; OLS on remaining 11 points; report slope SE. |
| LEDH actual gradient | N=10000 particles; same five fixed seeds by default; report seed mean, seed SD, and seed SE.  The route must be memory-disciplined; raw/full AD through the whole Sinkhorn transport solve is forbidden for governed N=10000 validation. |
| Standard-error rule | Discrepancy greater than 2 combined SE is a likely issue requiring investigation, not a proof that either approximation is correct. |
| Autodiff/JVP | Diagnostic-only unless a phase explicitly states and reviews a different non-promoting role. |
| Manual adjoint | Upstream dependency for resuming P82.  P82 may resume only after the manual/custom-adjoint program produces a reviewed handoff. |

Human amendment:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-fd-only-scope-amendment-2026-06-22.md`
- Zhao-Cui is removed from the P82 pass/fail path for now.
- The active P82 comparator is 13-point regression FD of the same LEDH scalar.

The 2-SE rule is a triage heuristic, not a calibrated hypothesis test unless a
later phase explicitly justifies its variance assumptions.  A discrepancy no
greater than 2 combined SE is not certification of correctness for either
method.  P7 must state whether seed pairing, independence, and value-outlier
trimming assumptions are being used before interpreting combined SE.

Every governed P82 regression-FD command must explicitly pass
`--trim-extreme-mode value` and record `raw_point_count = 13`,
`fit_point_count = 11`, and that trimming was performed on mean-over-seed
objective values rather than offset magnitude.  The harness default remains
backward compatible for older diagnostics, so omission of this flag blocks any
claim that the run followed the P82 governed FD protocol.

## Phase Ladder

| Phase | Objective | Subplan | Required result |
|---|---|---|---|
| P0 | Governance bootstrap, approval register, and visible runbook readiness. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase0-governance-bootstrap-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase0-governance-bootstrap-result-2026-06-22.md` |
| P1 | Route/protocol/harness inventory and reconciliation before code or GPU work. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase1-route-protocol-inventory-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase1-route-protocol-inventory-result-2026-06-22.md` |
| P2 | Patch or wrap the regression-FD harness for 13 offsets, batched theta rows, five-seed aggregation, and value-outlier trimming. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase2-regression-fd-harness-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase2-regression-fd-harness-result-2026-06-22.md` |
| P3 | Audit or repair the Zhao-Cui analytical derivative route so it is the comparator and autodiff/JVP remains diagnostic-only. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase3-zhaocui-analytical-route-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase3-zhaocui-analytical-route-result-2026-06-22.md` |
| P4 | FD-only LEDH consistency: GPU preflight, tiny smoke, N=10000 actual gradient, N=1000 13-point raw-direction regression FD, and SE-unit comparison. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase4-fd-only-ledh-consistency-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase4-fd-only-ledh-consistency-result-2026-06-22.md` |
| P4b | Full-AD route correction: close P82 as downstream-blocked until a memory-disciplined actual-gradient route exists. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md` | This correction and updated stop handoff. |
| P5 | Manual streaming transport-gradient wiring through the P82 benchmark path. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-result-2026-06-23.md` |
| P6 | Tiny trusted GPU smoke of the manual streaming route. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-result-2026-06-23.md` |
| P7 | Actual-gradient feasibility ladder ending, if feasible, in the N10000 five-seed actual-gradient artifact. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md` |
| P8 | Governed N1000 five-seed 13-point regression-FD comparison against the P7 N10000 actual-gradient artifact. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-consistency-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-consistency-result-2026-06-23.md` |
| P9 | Closeout, limitations, execution review, and next handoff. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-result-2026-06-23.md` |

## Repair Loop

For every material subplan:

1. Codex performs a skeptical plan audit before execution.
2. Claude may review as read-only reviewer using a compact fact packet, not a
   whole-file prompt.
3. Claude must end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.
4. If Claude does not respond, Codex probes with `READ-ONLY PROBE. Reply exactly PROBE_OK.`
5. If the probe works, Codex redesigns the review prompt.
6. Fixable findings are patched visibly in the same subplan or result, then
   focused checks are rerun.
7. Stop after five review rounds for the same blocker and write a blocker
   result.
8. Do not stop for non-blockers.  Advance when gates pass.

Claude is not an execution authority and cannot authorize crossing human,
runtime, model-file, funding, product-capability, GPU, or scientific-claim
boundaries.

## Anticipated Approvals

The program will need explicit/trusted approval for:

- Claude Code read-only review through
  `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`;
- `nvidia-smi`;
- TensorFlow GPU device probes;
- GPU LEDH smoke, N=10000 gradient, and N=1000 regression-FD commands;
- any long-running GPU diagnostic beyond the reviewed phase budget.

No package installation, network fetch, destructive git action, detached
supervisor, or default-policy change is authorized by this program.

## Launch Boundary

Creating and reviewing P0/P1 artifacts is safe immediately.  P2 may edit
benchmark harness code only after the P2 subplan exists and passes review.
P4 and later GPU phases require trusted/escalated GPU commands and reviewed
phase budgets.  No further P82 GPU validation should launch until the upstream
manual/custom-adjoint program has produced a reviewed memory-disciplined
actual-gradient handoff.
