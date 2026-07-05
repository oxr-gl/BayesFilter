# LEDH-PFPF-OT LGSSM Transport Normalization Step-Ladder Plan

Date: 2026-06-26

## Question

The OT-reset moment smoke stopped because the manual finite transport had large
row residuals while dense and streaming agreed and column residuals were small.
Is the next move a code-level row-normalization fix, or is the LGSSM test simply
using an under-converged finite Sinkhorn budget (`8` steps) relative to the
filterflow-style transport contract?

## Background

The prior stop result is
`docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-ot-reset-moment-hypothesis-test-stop-result-2026-06-26.md`.
It reported on a small shared cloud:

- dense/streaming transported-particle max difference around `1e-7`;
- dense column residual around `6e-7`;
- dense and streaming row residuals around `0.92` and `0.96`;
- post-OT covariance trace about `27%` to `36%` of pre-OT covariance trace.

Historical filterflow gap-closure artifacts record that the corrected
filterflow-style transport mirror can achieve small row residuals when using
the proper annealed transport loop/budget. The current LGSSM statistical
harness is hard-coded to `SINKHORN_ITERATIONS = 8`, much lower than the normal
public default of `80`.

## Hypotheses

H1: Under-converged finite Sinkhorn.

Prediction: row residual falls below the `1e-3` gate as finite steps increase
to `80` or `100`, without changing the transport formula.

H2: Transport-from-potentials formula or barycentric application mismatch.

Prediction: row residual remains large at `80` or `100`; an explicitly
row-normalized barycentric application changes moments/value materially but
breaks column diagnostics or indicates the need for a proper coupling-to-map
conversion rather than a naive patch.

H3: Even after row residual converges, barycentric OT/reset still contracts
covariance enough to explain the LGSSM value gap.

Prediction: row residual passes at high budget, but post/pre covariance trace
ratio remains far below one and value remains biased.

H4: Manual finite route differs from the thresholded annealed transport
contract.

Prediction: the fixed-step manual finite ladder still has large row residuals
at `80` or `100`, but the same shared cloud under the exact/thresholded dense
annealed transport path with `convergence_threshold=1e-3` and `max_iter=100`
has small row and column residuals. In that case, the next target is manual
finite route parity with the thresholded annealed contract, not a naive
row-normalization patch.

## Evidence Contract

Engineering question:

- Decide whether the immediate fix target is the LGSSM harness Sinkhorn budget,
  a transport normalization formula, or a later covariance-preserving reset
  design.

Comparator:

- Same LGSSM fixture and harness definitions as
  `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`.
- Same small CPU/XLA smoke shape: `N=128`, dense parity cloud `64`, `10` seeds,
  state dimensions `1` and `2`.
- Step ladder settings: at least `0.5:8`, `0.5:20`, `0.5:80`, and `0.5:100`.
- Known-contract comparator: on the same dense parity cloud, run the
  exact/thresholded dense annealed transport path with the same target epsilon
  `0.5`, scaling `0.9`, convergence threshold `1e-3`, and `max_iter=100`.
  This is the local comparator for the historical filterflow-style route; it
  tests whether fixed-step manual finite transport is failing to match the
  annealed convergence contract.

Primary decision criteria:

- If row residual is above `1e-3` at `8` but below `1e-3` by `80` or `100`, do
  not patch row normalization. The next fix is to update the LGSSM harness and
  any manual finite route validation to use a converged budget or convergence
  gate.
- If fixed-step row residual remains above `1e-3` at `100` but the
  exact/thresholded annealed comparator passes, do not patch row normalization.
  The next fix target is manual finite route parity with the thresholded
  annealed transport contract.
- If both fixed-step row residual at `100` and the exact/thresholded annealed
  comparator fail, run an explicit row-normalized barycentric diagnostic before
  any production-code patch.
- If row residual passes at high budget but value/moment bias remains, the
  next target is reset semantics/covariance preservation, not transport
  normalization.

Diagnostics that can veto:

- Non-finite values or particles.
- Dense/streaming transported-particle disagreement above `1e-4`.
- Dense column residual above `1e-3` at any ladder setting.
- Exact/thresholded comparator artifact missing row residual, column residual,
  and transported-particle comparison to the fixed-step route.
- CPU smoke command timeout or artifact write failure.

Explanatory-only diagnostics:

- Runtime.
- TF32 status for CPU smoke.
- Per-time covariance trace ratios and ESS.
- Naive row-normalized barycentric arm, if needed after the step ladder.

What will not be concluded:

- No gradient correctness.
- No SIR correctness.
- No HMC readiness, posterior correctness, production readiness, or broad
  scientific validity.
- No claim that naive row normalization is mathematically correct unless a
  follow-up derivation and tests support it.

## Skeptical Plan Audit

- Wrong-baseline risk: the previous smoke used only `8` finite steps, while the
  historical filterflow-style route normally uses larger budgets. The ladder
  must test budget before formula patching.
- Proxy-risk: row residual convergence is necessary for this transport
  application but not sufficient for likelihood correctness.
- Hidden-assumption risk: a naive row-normalized map can destroy the intended
  source marginal, so it is diagnostic only.
- Environment risk: this plan uses CPU-only smoke by design; any GPU conclusion
  is forbidden.
- Boundary risk: no production transport code is changed until the ladder
  indicates a specific fix.
- Annealing-contract risk: a high-budget fixed-step failure is not enough to
  prove a normalization bug unless the exact/thresholded annealed comparator
  also fails or otherwise exposes the same row-mass issue.

Audit status: PASS for a bounded local diagnostic.

## Required Result Artifact Structure

The post-run result must include:

- a decision table with decision, primary criterion status, veto diagnostic
  status, main uncertainty, next justified action, and forbidden conclusions;
- a run manifest with git commit, command, Python/TensorFlow environment,
  CPU/GPU visibility, seeds, particle counts, state dimensions, settings,
  runtime, and output paths;
- one row per state dimension and setting with row residual, column residual,
  dense/streaming max particle difference, value delta, same-time moment
  ratios, and ESS;
- one known-contract comparator row per state dimension with exact/thresholded
  row residual, column residual, max iterations used, and transported-particle
  difference against the fixed-step `100` route;
- an interpretation that explicitly selects H1, H2, H3, H4, or a mixed
  outcome using the evidence contract above.

## Planned Execution

1. Reuse the existing diagnostic script for the step ladder:

```bash
/usr/bin/timeout 600 python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py \
  --device-scope cpu \
  --num-particles 128 \
  --dense-parity-particles 64 \
  --seed-count 10 \
  --state-dims 1 2 \
  --settings 0.5:8 0.5:20 0.5:80 0.5:100 \
  --xla \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-transport-step-ladder-2026-06-26.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-transport-step-ladder-2026-06-26.md
```

2. If the row residual remains above `1e-3` at `100`, add a tiny
   row-normalized diagnostic arm only after checking the exact/thresholded
   annealed comparator on the same cloud.
3. If the row residual passes at high budget, patch only the LGSSM statistical
   harness budget/settings and rerun a bounded CPU smoke first.

## Stop Conditions

- Stop after the step ladder if it distinguishes under-convergence.
- Stop before any production-code patch if high-budget row residual still
  fails.
- Stop if the script artifacts do not record row residual, column residual,
  dense/streaming parity, and same-time moments for every setting.
- Do not launch N1000 GPU/XLA until the small normalization/step ladder is
  resolved.
