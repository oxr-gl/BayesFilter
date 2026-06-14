# Result: DPF OT Resampling Math Source Audit

## Decision

`OT_DPF_SOURCE_SUPPORTS_BOUNDED_DET_ERROR_CURRENT_STRUCTURAL_FAILURE_REQUIRES_IMPLEMENTATION_CALIBRATION_AUDIT`

The BayesFilter TF/TFP Sinkhorn resampler implements the same mathematical
object as the differentiable ensemble transform (DET) barycentric projection in
Corenflos et al. 2021: a finite entropy-regularized OT coupling with weighted
source marginal, uniform target marginal, and output cloud obtained by
barycentric projection.  The implementation is therefore not wrong because it
uses a barycentric relaxed OT cloud.

The serious correction is interpretive and implementation-facing: the inspected
source explicitly says ET/DET only satisfy the usual resampling identity for
affine test functions at finite particle count, and that DPF gives a biased
likelihood estimate relative to standard PF.  But Corenflos et al. also prove a
finite DET error bound in Proposition 4.2 and show in Section 5.1 that, on their
linear Gaussian state-space model, PF and DPF likelihood estimates are
practically very close for `epsilon` values `0.25`, `0.5`, and `0.75`.

Therefore the structural AR(1) MLE shift under the current BayesFilter Sinkhorn
policy must not be dismissed as merely "expected finite-N bias."  It is a
red-flag result requiring a focused implementation/calibration audit against
the Corenflos construction: resampling trigger semantics, cost scaling,
epsilon choice, time horizon, particle count, common-random-number protocol,
and whether the transform is being applied to the correct pre-/post-weighting
particle measures.

## Local Sources Downloaded

All sources below were downloaded or confirmed under `.localsource/dpf_ot_audit/`.

| Source | Local path | Status |
|---|---|---|
| Corenflos et al. 2021, main paper | `.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot.pdf` | full PDF |
| Corenflos et al. 2021, supplement | `.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot_supp.pdf` | full PDF |
| Zhu et al. 2020 | `.localsource/dpf_ot_audit/zhu2020_towards_differentiable_resampling.pdf` | full PDF |
| Cuturi 2013 | `.localsource/dpf_ot_audit/cuturi2013_sinkhorn_distances.pdf` | full PDF |
| Peyre and Cuturi 2019 | `.localsource/dpf_ot_audit/peyre_cuturi2019_computational_ot.pdf` | full PDF |
| Schmitzer 2019 | `.localsource/dpf_ot_audit/schmitzer2019_stabilized_sparse_scaling.pdf` | full PDF |
| Reich 2013 | `.localsource/dpf_ot_audit/reich2013_nonparametric_ensemble_transform.pdf` | full PDF copied from existing local source cache |

ResearchAssistant has no local structured record for these papers; its
summary-level claim audit returned insufficient evidence.  The support below is
therefore from locally downloaded primary PDFs and extracted text.

## Source Anchors

| Claim | Source support | Status |
|---|---|---|
| Corenflos DET computes entropy-regularized OT and returns a barycentric cloud. | Main paper Section 3.2, Algorithm 3, extracted text lines around 520--551: potentials from weighted particles and uniform target; return `X_tilde = N P_OT_epsilon X`. | `PRIMARY_TECHNICAL_SUPPORT` |
| ET/DET only satisfy the resampling identity for affine functions at finite N. | Main paper Section 2.2 and 3.2, extracted text lines around 413 and 568. | `PRIMARY_TECHNICAL_SUPPORT` |
| DPF/DET provides a biased likelihood estimate relative to standard PF. | Main paper Section 4.3 and 5.1, extracted text lines around 794--837. | `PRIMARY_TECHNICAL_SUPPORT` |
| DET has a finite error bound relative to the weighted particle measure. | Main paper Proposition 4.2, extracted text lines around 640--720, and supplement proof of Proposition 4.2. | `PRIMARY_TECHNICAL_SUPPORT` |
| Consistency is asymptotic and assumption-bound, not finite-N equality. | Main paper Proposition 4.3 and supplement Assumptions B.1--B.4, extracted text lines around 721--790 and supplement lines around 438--449. | `PRIMARY_TECHNICAL_SUPPORT` |
| In the paper's LGSSM experiment, DPF and PF likelihood estimates are practically close. | Main paper Section 5.1 and Table 1; layout extraction shows PF means `-1.13`, `-0.93`, `-1.05` and DPF means around `-1.14`, `-0.94`, `-1.07/-1.08`. | `PRIMARY_TECHNICAL_SUPPORT` |
| Entropic regularization gives a unique smooth coupling and Sinkhorn scaling. | Corenflos Section 3.1; Cuturi 2013 Section 3--4; Peyre--Cuturi ch. 4; Schmitzer 2019 stabilization discussion. | `PRIMARY_TECHNICAL_SUPPORT` |
| Small Sinkhorn marginal residuals imply likelihood preservation. | No inspected source supports this. | `FORBIDDEN_CLAIM` |
| Finite DET/Sinkhorn equals categorical resampling or produces an unbiased PF likelihood estimate. | Corenflos explicitly says the opposite for likelihood bias. | `FORBIDDEN_CLAIM` |

## Project Derivation

Let a coupling `P` have source marginal `w` and target marginal `u`, and define
the barycentric output

```text
y_j = sum_i P_ij x_i / u_j .
```

For any affine test function `phi(x)=a+b'x`,

```text
sum_j u_j phi(y_j)
= a + b' sum_j u_j y_j
= a + b' sum_j sum_i P_ij x_i
= a + b' sum_i w_i x_i
= sum_i w_i phi(x_i).
```

MathDevMCP checked the two-particle affine identity

```text
u1*((P11*x1 + P21*x2)/u1) + u2*((P12*x1 + P22*x2)/u2)
= (P11 + P12)*x1 + (P21 + P22)*x2
```

as equivalent.

For nonlinear test functions, equality fails.  A concrete quadratic
counterexample is

```text
(0.5*0 + 0.5*2)^2 != 0.5*0^2 + 0.5*2^2.
```

MathDevMCP simplified the difference to `-1`.  Thus a barycentric DET step
can preserve affine summaries while changing second and higher moments.
However, Corenflos Proposition 4.2 is precisely a quantitative control result
for this non-affine mismatch under stated assumptions.  The derivation therefore
justifies caution about exact finite-N preservation, but it does not justify
accepting a large BayesFilter MLE shift without checking whether our
implementation and hyperparameters are in the paper's controlled regime.

## Code Consistency

Code inspected:

- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/resampling_policies_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/structural_filter_tf.py`

MathDevMCP `compare_label_code` on `eq:bf-dr-barycentric-map` against
`sinkhorn_tf.py` returned `consistent`: the code contains the coupling,
uniform target, column mass, relaxed particles, and pairwise squared Euclidean
cost terms.

Manual code audit:

- `sinkhorn_resample_tf` normalizes source weights and sets target weights to
  uniform.
- It computes a log-domain finite Sinkhorn coupling with row and column
  residual checks.
- It returns `relaxed_particles = coupling^T x / column_mass`, which equals
  the Corenflos `N P^T X` formula when the column marginal is uniform.
- Diagnostics label the object as `finite_budget_entropic_ot_coupling` and
  `relaxed_finite_sinkhorn_not_categorical`.
- The structural policy `sinkhorn_current_z` applies the barycentric map to the
  current stochastic block and then recompletes deterministic state; this
  preserves the structural residual but does not preserve the filtering law.
- The structural policy `sinkhorn_full_context` is correctly labelled as the
  old/ad hoc comparator.

No row/column orientation bug was found in the barycentric map.  No hidden
categorical-equivalence claim was found in these implementation files.

But several source-consistency gaps remain:

- Corenflos rescales the cost matrix to make `epsilon` approximately
  independent of state scale and dimension; the BayesFilter helper currently
  uses raw pairwise squared Euclidean costs unless a caller supplies a cost.
- Corenflos evaluates DET in a particle-filter setting with resampling/DET
  triggered by ESS in the relevant experiments; the structural interface policy
  ladder applies the selected policy every time step.
- Corenflos Section 5.1 uses a 2D LGSSM with `T=150`, `N=25`, 100 replicates,
  and compares rescaled log-likelihood estimates.  The structural AR(1) MLE
  test is a different model and criterion.
- The current generic helper receives a single particle cloud plus weights and
  uses that same cloud on both sides of the cost.  This matches Algorithm 3's
  DET formula only if the intended alpha/beta empirical measures are represented
  in that convention for the current filter state.  This needs a dedicated
  pre-/post-weighting measure audit for LEDH-PF-PF.

## LaTeX Consistency

Target chapter:

- `docs/chapters/ch32_diff_resampling_neural_ot.tex`

The chapter is broadly consistent with the inspected primary source:

- it states that differentiability is obtained by changing the resampling map;
- it distinguishes categorical resampling, unregularized OT, entropic OT,
  finite Sinkhorn, and solver-differentiated objectives;
- it gives the same barycentric projection convention as Corenflos Algorithm 3;
- it says marginal residuals do not remove entropic bias or target change;
- it says the gradient belongs to the selected relaxed numerical object, not
  automatically to a categorical-resampling likelihood estimator.

One improvement should be made in a future patch register: add an explicit
source-anchored sentence near the DET/entropic OT section saying both sides of
the Corenflos result: DET is finite-N biased and affine-exact only, but
Proposition 4.2 gives a quantitative error bound and Section 5.1 shows practical
LGSSM closeness under their calibration.

No monograph chapter was edited in this audit.

## Consequence For The Structural AR(1) Failure

The observed linear structural AR(1) result:

- no resampling and categorical ancestor resampling match the exact Kalman grid
  MLE for `b`;
- `sinkhorn_current_z` and `sinkhorn_full_context` shift the DPF median MLE.

This is not enough to conclude that Corenflos-style DET is unsuitable.  It
indicates that the current BayesFilter structural Sinkhorn policy changes the
MLE criterion under the tested particle count, epsilon, raw cost scale, and
every-step resampling policy.  Given Proposition 4.2 and the paper's LGSSM
experiment, this should be treated first as an implementation/calibration
blocker, not as a mathematical refutation of OT-DPF.

## What Must Not Be Concluded

- Do not claim finite Sinkhorn DET is an exact categorical resampler.
- Do not claim finite Sinkhorn DET gives an unbiased likelihood estimate.
- Do not claim small Sinkhorn residuals validate posterior or MLE correctness.
- Do not claim the current OT policy is production-ready or HMC-ready.
- Do not claim Corenflos et al. guarantees equality in the finite structural
  AR(1) fixture.
- Do not claim the current BayesFilter structural Sinkhorn failure is explained
  by theory until the Corenflos calibration details are reproduced.

## Recommended Next Action

Run a focused reviewed calibration audit before changing the architecture
decision:

1. reproduce Corenflos Section 5.1 LGSSM as closely as possible in TF/TFP;
2. add paper-style cost scaling to `sinkhorn_resample_tf` or its caller;
3. compare ESS-triggered DET against every-step DET;
4. run epsilon and particle-count ladders on the structural AR(1) linear Kalman
   gate;
5. audit whether LEDH-PF-PF passes the correct alpha/beta particle measures to
   DET.

Until that audit is done, the safe status is: "BayesFilter's current structural
Sinkhorn policy is blocked by calibration/source-consistency risk," not
"Corenflos-style OT resampling fails mathematically."
