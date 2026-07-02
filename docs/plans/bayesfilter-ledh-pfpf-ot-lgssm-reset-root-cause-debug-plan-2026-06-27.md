# LEDH-PFPF-OT LGSSM Reset Root-Cause Debug Plan

Date: 2026-06-27

## Question

Why does the LEDH-PFPF-OT LGSSM value gate fail after OT/reset while
SIS/no-transport and LEDH/no-OT are close to the FP64 Kalman value?

## Hypotheses

1. `H1_sinkhorn_budget`: finite Sinkhorn row-marginal under-convergence is the
   main value-gap cause.
2. `H2_orientation_normalization`: the transport matrix is applied with the
   wrong row/column normalization for the barycentric reset.
3. `H3_barycentric_covariance_loss`: the current deterministic barycentric
   reset preserves mean but contracts covariance, so the next-step proposal
   cloud no longer represents the Kalman filtering distribution.
4. `H4_invalid_comparator_semantics`: after deterministic OT reset, the scalar
   being estimated is an approximation-specific filter value, not exactly the
   Kalman likelihood; therefore the exact Kalman gate is valid for no-OT arms
   but not for the current reset arm unless second moments are preserved.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | On the same LGSSM/LEDH value loop, which reset variant localizes the value gap: current barycentric, explicit row-normalized barycentric, or affine moment-restored barycentric? |
| Baseline/comparator | FP64 transition-first Kalman value/increments; LEDH no-OT weighted arm; current OT reset arm. |
| Primary criterion | If row-normalization alone leaves the value gap but moment restoration materially reduces the gap and future increment deltas, then `H3/H4` is the leading root cause. |
| Veto diagnostics | Nonfinite values, inability to reproduce current OT value gap on a small fixture, row residual not recorded, or accidental use of generic autodiff/`transport_ad_mode=full` in the tested reset route. |
| Explanatory diagnostics | Row residual, column residual, post/pre covariance trace ratio, pre/post mean shift, per-time increment delta, runtime, CPU/GPU placement. |
| Not concluded | No gradient correctness, SIR correctness, HMC readiness, posterior correctness, production readiness, or claim that a moment-restored reset is approved for production. |

## Skeptical Plan Audit

- Wrong-baseline risk: the diagnostic reuses the existing LGSSM harness
  equations, observations, seeds, and LEDH proposal correction; only the reset
  operation after weight normalization varies.
- Proxy-risk: covariance restoration is a diagnostic intervention, not a
  production patch.  It can identify the cause of the value gap without
  certifying a new algorithm.
- Budget-risk: low Sinkhorn steps can confound the result, so include at least
  one higher-budget setting where row residual is small on the small fixture.
- Environment-risk: initial runs may be CPU-only debugging diagnostics with
  `CUDA_VISIBLE_DEVICES=-1`; they must not be described as GPU/XLA evidence.
- Boundary-risk: do not edit production transport behavior from this diagnostic
  alone.

Audit status: PASS for a focused diagnostic script and small CPU execution.

## Planned Diagnostic

Create `docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py`.

Run a small fixture first:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py \
  --device-scope cpu \
  --num-particles 64 \
  --state-dims 1 2 \
  --time-steps 10 \
  --settings 0.5:20 0.5:100 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-reset-variants-debug-2026-06-27.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-reset-variants-debug-2026-06-27.md
```

If this is too slow, fall back to `--time-steps 3` and record the narrower
scope explicitly.

## Stop Conditions

- Stop and revise if the diagnostic cannot reproduce a current-OT value gap.
- Stop and inspect normalization if row-normalized current transport changes
  the result materially even when row residual is already small.
- Stop and identify `H3/H4` as leading if moment restoration materially reduces
  the value/increment gap while current and row-normalized OT remain biased.

## Phase Result / Close Record

Date: 2026-06-27

Status: `supports_barycentric_covariance_loss_root_cause`

### Commands Run

Syntax check:

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py
```

Tiny CPU smoke:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py \
  --device-scope cpu \
  --num-particles 8 \
  --state-dims 1 \
  --time-steps 2 \
  --settings 0.5:2 \
  --output /tmp/ledh_reset_variants_tiny.json
```

Planned diagnostic:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 900 python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py \
  --device-scope cpu \
  --num-particles 64 \
  --state-dims 1 2 \
  --time-steps 10 \
  --settings 0.5:20 0.5:100 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-reset-variants-debug-2026-06-27.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-reset-variants-debug-2026-06-27.md
```

The diagnostic was intentionally CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
TensorFlow CUDA initialization messages in this run are not GPU evidence.

### Artifacts

- Diagnostic script:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py`
- JSON result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-reset-variants-debug-2026-06-27.json`
- Markdown result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-reset-variants-debug-2026-06-27.md`

### Decision Table

| Question | Evidence | Decision |
| --- | --- | --- |
| Did the diagnostic reproduce the current OT value gap? | At `N=64,T=10`, current OT absolute value deltas were about `0.271` in 1d and `0.855` in 2d. | Yes. The blocker reproduces on the small fixture. |
| Is finite Sinkhorn row under-convergence the leading cause? | Increasing from `20` to `100` steps reduced the 2d current-OT row residual to `1.976e-04`, but the 2d value delta stayed about `0.855`. | No. Sinkhorn budget may matter for quality, but it is not the leading cause of this LGSSM gate failure. |
| Is row/column orientation or missing row normalization the leading cause? | Explicit row normalization drove the reported post-row residual to `2.384e-07`, but value deltas stayed essentially unchanged. | No. Orientation/row-normalization is not the leading cause for this failure. |
| Does deterministic barycentric reset contract covariance enough to explain the gap? | Current OT covariance trace ratio at the first reset was about `0.60` in 1d and `0.36` in 2d. Diagnostic moment restoration moved the covariance ratio back to about `1.0`. | Yes. This is the leading root cause. |
| Does moment restoration reduce the value gap toward the no-OT baseline? | 1d current OT delta `~0.271` dropped to `~0.022`; 2d current OT delta `~0.855` dropped to `~0.101`, close to the no-OT `~0.078` diagnostic scale. | Yes. This supports `H3/H4`. |

### Interpretation

The current deterministic barycentric OT reset changes the particle cloud
moments: it approximately preserves the mean but contracts covariance.  In the
LGSSM harness, that covariance contraction changes future predictive
likelihood increments.  Therefore the exact Kalman likelihood is a valid
comparator for the no-OT weighted arm, but it is not a valid direct value or
gradient oracle for the current deterministic barycentric OT-reset arm unless
the reset route is changed to preserve the required distributional moments or
the comparator is redefined for the approximation-specific scalar.

### Nonclaims

This close record does not claim:

- gradient correctness;
- SIR correctness;
- HMC readiness;
- posterior correctness;
- production readiness;
- approval of the diagnostic moment-restored reset as a production algorithm;
- GPU/XLA performance evidence from the CPU-only diagnostic.

### Next Handoff

The next phase should not keep tuning Sinkhorn iterations as the primary
response to this LGSSM Kalman gate.  The next smallest justified action is to
choose one of two explicit routes:

1. revise the LGSSM value/gradient gate so current deterministic OT reset is
   not compared directly against the exact Kalman likelihood; or
2. design and review a moment-preserving reset candidate, then test whether
   the Kalman value and gradient gates become meaningful for that new route.
