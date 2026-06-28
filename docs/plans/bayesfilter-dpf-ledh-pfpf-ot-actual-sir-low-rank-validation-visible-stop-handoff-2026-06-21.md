# Actual-SIR Low-Rank Validation Visible Stop Handoff

Date: 2026-06-21

Status: `STOPPED`

Final phase reached: `P03`

Final status: `TUNING_REQUIRED`

Result artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-result-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p03-paired-ladder-result-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-result-2026-06-21.md`
- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21.md`
- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.md`

Claude review trail:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-claude-review-ledger-2026-06-21.md`

Tests/benchmarks actually run:

- P01 compile/test checks recorded in
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p01-harness-result-2026-06-21.md`.
- P02 CPU-hidden tiny route smokes recorded in
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-result-2026-06-21.md`.
- P03 trusted GPU1 paired row:
  `B=5,T=20,N=1024`, seeds `81120,81121,81122,81123,81124`,
  `warmups=1`, `repeats=3`, compiled streaming timing, TF32 enabled.

Unresolved blockers:

- The current low-rank route/configuration failed paired log-likelihood
  comparability and the warm-time support screen on the first required P03 row.
- P04 large-N envelope was not executed because P03 did not satisfy its
  handoff conditions.

Nonclaims:

- No posterior correctness.
- No HMC readiness.
- No public API readiness.
- No production/default readiness.
- No dense Sinkhorn equivalence.
- No broad scalable-OT selection.
- No statistical ranking without uncertainty evidence.

Safest next human decision: decide whether to open a new low-rank tuning/repair
program with predeclared parameters and the same actual-SIR P02/P03 gates, or
defer this route for actual-SIR large-particle efficiency.
