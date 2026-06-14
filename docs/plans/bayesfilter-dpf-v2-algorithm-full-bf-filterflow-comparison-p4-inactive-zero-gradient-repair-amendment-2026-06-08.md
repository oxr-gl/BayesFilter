# DPF V2 Algorithm Full Comparison P4 Inactive Zero-Gradient Repair Amendment

metadata_date: 2026-06-08
phase: P4
status: DRAFT_FOR_CLAUDE_REVIEW

## Blocker Classification

blocker_type: `FIXABLE_DERIVATION_BACKED_INACTIVE_GRADIENT_ENCODING`

The visible P4 bootstrap-OT gradient runner produced a classified mismatch
artifact rather than a pass:

- decision:
  `P4_BOOTSTRAP_OT_GRADIENTS_CLASSIFIED_MISMATCH_PENDING_REVIEW`;
- three rows matched: `lgssm_2d_h25_rich`,
  `range_bearing_4d_h20_rich`, and `predator_prey_rk4`;
- one row remained predeclared excluded: `spatial_sir_j3_rk4`;
- two rows had disconnected AD gradients for transition-scale knobs:
  `sv_1d_h18_rich:sigma` and
  `structural_ar1_quadratic_h16:sigma`;
- max BayesFilter/FilterFlow scalar delta was `0.0`;
- max BayesFilter/FilterFlow AD-gradient delta over connected gradients was
  `0.0`;
- finite differences were recorded as diagnostic-only.

The blocker is not BayesFilter/FilterFlow disagreement. It is that TensorFlow
can return `None` when the P4 scalar is independent of an included physical
knob under the frozen fixed-additive-innovation contract.

## Derivation-Backed Classification

P4 uses the frozen P2 scalar definition:

`fixed-branch sum of per-step predictive log normalizers`.

The fixed branch computes predicted particles from transition means plus the
frozen P2 transition innovations, then accumulates observation log-density
normalizers. The scalar does not include transition log densities and does not
standardize or rescale the frozen transition innovations.

Therefore, for the two affected rows:

- `sv_1d_h18_rich:sigma` parameterizes transition noise scale, but the P4
  scalar path uses fixed additive innovations and observation log density. The
  scalar is independent of `sigma`, so the derivative is exactly zero under
  the frozen P2 contract.
- `structural_ar1_quadratic_h16:sigma` parameterizes the structural AR(1)
  transition scale, but the P4 scalar path uses deterministic mean/completion
  plus fixed additive innovations and observation log density. The scalar is
  independent of `sigma`, so the derivative is exactly zero under the frozen
  P2 contract.

This mirrors the reviewed common-suite P5 inactive-zero-gradient treatment,
after the later finite-difference diagnostic-only correction:

- `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p5-fd-diagnostic-only-contract-amendment-2026-06-07.md`;
- `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p5-claude-review-ledger-2026-06-07.md`.

The prior P5 review records that inactive zero gradients for
`sv_1d_h18_rich:sigma` and `structural_ar1_quadratic_h16:sigma` are
derivation-backed under the frozen fixed-additive-innovation scalar, not
finite-difference gated.

## Proposed Repair

Patch only:

- `experiments/dpf_implementation/tf_tfp/runners/run_v2_bootstrap_ot_gradients_tf.py`.

Required semantics:

1. Keep P2 contracts, P3 value digest, fixtures, particles, observations,
   transition innovations, branch masks, OT settings, scalar definition,
   tolerances, and included knob names unchanged.
2. Keep `spatial_sir_j3_rk4` as `PREDECLARED_EXCLUDED`.
3. Add an explicit `INACTIVE_ZERO_GRADIENT_REASONS` table only for:
   - `("sv_1d_h18_rich", "sigma")`;
   - `("structural_ar1_quadratic_h16", "sigma")`.
4. Convert AD `None` to explicit `0.0` only for those two
   derivation-classified knobs.
5. Record the conversion in per-side fields such as
   `inactive_zero_gradient_knobs`, `inactive_zero_gradient_reasons`, and
   `disconnected_zero_gradient_knobs`.
6. Treat gradient finiteness as satisfied for a derivation-inactive zero
   gradient only for the two exact model/knob pairs above. Scalar finiteness
   remains an independent hard gate for every included row. Connected gradient
   finiteness remains an independent hard gate for every other knob.
7. Preserve finite-difference fields as explanatory diagnostics only.
8. Any other AD `None` remains a veto/classified mismatch and must not be
   converted to a pass.

## Why This Is Not A Contract Change

The repair does not change the comparator, scalar, branch, fixtures, particle
paths, contracts, tolerances, parameter values, included knob list, or OT
settings. It only encodes the derivative of a scalar that is derivably constant
with respect to two transition-scale knobs under the already frozen P2 path.

Finite differences must not decide promotion or veto status. They may remain
in the JSON/report as explanatory diagnostics and numerical-smoke context.

## Skeptical Plan Audit

Status: `PASS_FOR_CLAUDE_REVIEW_AS_NARROW_REPAIR_DRAFT`.

Wrong-baseline risk: controlled by preserving the P2 bundle checksum and P3
reproducibility digest.

Proxy-metric risk: controlled because FD remains diagnostic-only and cannot
promote the two inactive knobs.

Missing stop-condition risk: controlled because only two explicit
model/knob pairs may convert `None` to `0.0`; every other disconnected
gradient still blocks. The conversion waives only the disconnected-gradient
veto for those two exact knobs, not scalar finiteness, connected-gradient
finiteness, BF/FF scalar agreement, BF/FF AD-gradient agreement, row-order
checks, contract checksums, or any governance veto.

Unfair-comparison risk: controlled because both BayesFilter and the
BayesFilter-owned FilterFlow-side adapter consume identical contract bytes and
receive the same inactive-gradient encoding rule.

Hidden-assumption risk: controlled by recording the derivation reason in the
artifact instead of silently replacing `None` with zero.

Stale-context risk: controlled by citing only the reviewed common-suite P5
inactive-zero and FD-diagnostic-only correction as pattern evidence, not as P4
result evidence.

Environment-mismatch risk: controlled by continuing CPU-only TensorFlow with
pre-import `CUDA_VISIBLE_DEVICES=-1` and making no GPU claim.

## Required Fresh Evidence

1. Run a small read-only Claude probe before the amendment review.
2. Run Claude read-only review of this amendment. Continue only if it returns
   `VERDICT: AGREE`.
3. Patch only the P4 runner.
4. Rerun:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_v2_bootstrap_ot_gradients_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_bootstrap_ot_gradients_tf
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_gradients_2026-06-07.json
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_bootstrap_ot_gradients_tf --validate-only
git diff --check docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-inactive-zero-gradient-repair-amendment-2026-06-08.md experiments/dpf_implementation/tf_tfp/runners/run_v2_bootstrap_ot_gradients_tf.py docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-result-2026-06-07.md experiments/dpf_implementation/reports/dpf-v2-bootstrap-ot-gradients-2026-06-07.md
```

5. Run chunked Claude P4 result/governance review and final synthesis.

## Non-Claims

- no bootstrap-OT scientific correctness proof;
- no BayesFilter correctness proof;
- no FilterFlow correctness proof;
- no stochastic resampling gradient claim;
- no gradient-through-random/discrete-branch claim;
- no student implementation claim;
- no TT/SIRT, paper-table, dense-quadrature, simulated-truth, HMC, DSGE, GPU,
  scalability, deployment, or production-readiness claim.
