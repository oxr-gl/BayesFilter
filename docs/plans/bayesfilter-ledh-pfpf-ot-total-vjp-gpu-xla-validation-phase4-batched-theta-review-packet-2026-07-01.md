# Claude Review Packet: Phase 4 Batched-Theta FD Repair

Status: `READY_FOR_REVIEW`

## Role Contract

Codex is supervisor and executor.  Claude is read-only reviewer only.  Claude
must not edit files, run experiments, launch agents, or change state.

## Question

After the Phase 4 serial FD attempt proved too slow, is replacing serial FD
with `--fd-evaluation-mode batched-theta --theta-offset-batch-size 3` a valid
bounded repair for the same-scalar direction diagnostic?

## Scope

Review only:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-subplan-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-execution-ledger-2026-07-01.md`
- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:700-760`
- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:930-980`

## Evidence

The interrupted serial attempt:

- compiled the manual-reverse XLA unit;
- entered the first FD window, `log_kappa_scale`, base step `0.00025`;
- remained in that first FD window after roughly 25 minutes;
- traceback showed `_regression_diagnostic_for_direction` using serial
  `_value_at_theta` calls for each theta offset.

The proposed repair:

- keeps the same runner and same finite scalar;
- keeps GPU visible execution, `float32`, TF32, manual-reverse XLA for the AD
  route, streaming transport, and `transport_ad_mode="full"`;
- changes only FD value evaluation from serial one-theta-at-a-time calls to
  batched theta-offset value calls with chunks of 3.

## Pass/Block Criteria

Pass if:

- the batched-theta mode preserves the same finite scalar for each theta row;
- the command remains a same-scalar FD comparator for the corrected full-route
  total derivative;
- the ledger correctly classifies the serial attempt as a harness/runtime
  blocker, not a derivative failure.

Block if:

- batched-theta changes the scalar, route, fixed seeds, or transport mode;
- the repair weakens the Phase 4 pass/fail rule;
- the plan hides the interrupted serial attempt.

## Requested Verdict

Findings first if any.  End with exactly:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
