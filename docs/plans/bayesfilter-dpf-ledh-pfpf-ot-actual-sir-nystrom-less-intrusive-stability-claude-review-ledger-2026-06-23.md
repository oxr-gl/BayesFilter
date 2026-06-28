# Actual-SIR Nystrom Less-Intrusive Stability Claude Review Ledger

Date: 2026-06-23

Status: `P03_IMPLEMENTATION_REVIEW_CONVERGED`

## Review Rules

Claude Opus max effort is a read-only reviewer only.  Claude may inspect bounded
paths and report findings, but may not edit files, run experiments, launch
agents, change state, or authorize crossing human, runtime, model-file,
funding, product-capability, default-policy, or scientific-claim boundaries.

Every material review prompt must require a final line of exactly
`VERDICT: AGREE` or `VERDICT: REVISE`.

## Reviews

### P00 Review Round 1

Log:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-claude-review-r1-2026-06-23.log`

Verdict: `VERDICT: REVISE`

Material findings:

- P04/P05 routed valid candidate failures too directly to closeout, conflicting
  with the declared repair-loop and automatic-continuation contract.
- P06 had a failure-classification branch that was partly unreachable from
  P04/P05 handoffs.

Minor finding:

- P02 referenced `P03/P06 prior artifacts` ambiguously instead of naming them as
  closed-lane artifacts.

Patch applied:

- P04/P05 valid candidate failures now route to P06 classification or a reviewed
  repair loop rather than automatic closeout.
- P06 entry conditions and decisions now explicitly cover pass, candidate
  failure, neighborhood failure, return-to-P02 repair loop, fixed-policy, and
  closeout paths.
- P02 comparator wording now says `closed-lane P03/P06 artifacts`.

### P00 Review Round 2

Log:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-claude-review-r2-2026-06-23.log`

Verdict: `VERDICT: AGREE`

Claude confirmed:

- P04/P05 valid candidate failures now route to P06 classification or
  next-loop decision.
- P06 is reachable from pass, P04 valid candidate-failure, and P05
  neighborhood/control-failure paths.
- P02 closed-lane artifact wording is unambiguous.
- No new material threshold drift, default-promotion authority, detached
  execution authority, unsupported claim, or artifact-handoff issue was found.

### P02 Review Round 1

Log:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-claude-review-r1-2026-06-23.log`

Verdict: `VERDICT: REVISE`

Material findings:

- P03 did not state the exact implementation, harness, and test file scope.
- The balanced scaling formula was directionally plausible but
  under-specified; axes and formula were not exact enough for two implementers
  to produce the same update.

Minor finding:

- P03 made Claude implementation review conditional, but this selected repair
  changes transport-update math and validation metadata, so the implementation
  review should be unconditional before P04.

Patch applied:

- P02 and P03 now specify the exact `[B,N]` batchwise balancing formula:
  `mean_log_u`, `mean_log_v`, `log_c = 0.5 * (mean_log_u - mean_log_v)`,
  `c = exp(log_c)`, `u <- u / c`, and `v <- v * c`.
- P02 and P03 now restrict P03 code scope to
  `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`,
  `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`,
  `tests/test_nystrom_transport_tf.py`, and
  `tests/test_actual_sir_nystrom_compiled_redo.py`.
- P03 now requires Claude implementation review before P04.

### P02 Review Round 2

Log:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-claude-review-r2-2026-06-23.log`

Verdict: `VERDICT: AGREE`

Claude confirmed:

- exact P03 code scope is now explicit;
- balanced scaling formula and axes are specified enough for implementation;
- Claude implementation review before P04 is unconditional;
- no new threshold drift, default-policy drift, positive-projection promotion,
  proxy-promotion, missing artifact handoff, or unsupported scientific/default
  readiness claim was introduced.

### P03 Implementation Review Round 1

Log:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-claude-review-r1-2026-06-23.log`

Verdict: `VERDICT: AGREE`

Claude confirmed:

- implementation is opt-in and defaults to `none` throughout tensor, Python,
  and benchmark CLI surfaces;
- balanced formula matches the reviewed P02 contract and is applied only after
  a full `u/v` Sinkhorn update;
- required diagnostics propagate through tensor diagnostics, Python
  diagnostics, compiled benchmark rows, and transport metadata;
- focused tests cover default `none`, XLA/tensor `balanced`, positive
  gauge-shift diagnostics, and benchmark propagation;
- no threshold drift, default drift, positive-projection promotion, or scope
  expansion was found.
