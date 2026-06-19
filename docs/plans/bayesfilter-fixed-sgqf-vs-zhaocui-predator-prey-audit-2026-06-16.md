# Fixed-SGQF vs Zhao-Cui Predator-Prey Audit

metadata_date: 2026-06-16
status: EXECUTION_COMPLETE

## Question

Why does fixed SGQF not currently match the correctness level of the Zhao-Cui
lower-rung route on predator-prey, for both value and gradient evidence?

This note is a hypothesis audit, not a final proof. It traces the current code,
math contracts, and test evidence and proposes ranked explanations.

## Audited surfaces

### Fixed-SGQF
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`
- `tests/test_fixed_sgqf_values_tf.py`
- `tests/test_fixed_sgqf_scores_tf.py`
- `tests/highdim/test_p47_predator_prey_filtering.py`

### Zhao-Cui / dense lower-rung comparator
- `bayesfilter/highdim/filtering.py`
- `bayesfilter/highdim/models.py`
- `tests/highdim/test_p47_predator_prey_filtering.py`

## Executive summary

The strongest explanation is **not one small coding mistake** in the repaired
fixed-SGQF lane. The strongest explanation is a **mathematical model-class
mismatch** between the two methods after the first nonlinear update:

- fixed SGQF is a **Gaussian assumed-density moment-closure filter** on a fixed
  sparse-grid cloud,
- the tested Zhao-Cui lower rung is a **retained-grid same-target density
  approximation** that is quantitatively tied to a dense same-target oracle.

So even after the merge fix, fixed SGQF and Zhao-Cui are not approximating the
same intermediate object in the same way.

That difference matters more on predator-prey than it did on the affine and
scalar-quadratic checks, because predator-prey is low-dimensional but genuinely
nonlinear and positivity/domain-sensitive.

## Ranked shared/root-cause hypotheses

### H1. Strongest shared hypothesis: SGQF repeatedly compresses the posterior to mean/covariance, while Zhao-Cui retains a richer density representation

This is the most important difference.

### Fixed-SGQF route
In `tf_fixed_sgqf_filter(...)`:
- factor current covariance,
- place a fixed Smolyak cloud,
- propagate points through deterministic `transition_fn`,
- compute weighted predicted mean/covariance,
- compute weighted observation mean/innovation covariance,
- update to a new filtered mean/covariance,
- discard higher-order shape and continue from only `(mean, covariance)`.

So the next step always starts from a Gaussian surrogate.

### Zhao-Cui route
In the predator-prey lower-rung test:
- a dense same-target reference computes the exact filtering recursion on a dense
  tensor grid,
- the tested Zhao-Cui route (`multistate_nonlinear_fixed_design_tt_value_path`) keeps a
  retained grid/density approximation (`storage_kind == "multistate_tt_grid"`),
- and uses that retained density in the next predictive integral.

That is much richer than a pure Gaussian closure.

### Why this matters
On predator-prey, nonlinear RK4 transport and observation updates can create
posterior skew and shape that are not preserved by only `(mean, covariance)`.
The retained-grid Zhao-Cui route keeps more of that shape than fixed SGQF does.

**Assessment:** strongest explanation for the value gap.

## H2. Strong shared hypothesis: the fixed-SGQF cloud integrates a Gaussian surrogate, while the dense/Zhao-Cui comparator integrates the same-target lower-rung closure more directly

The dense reference in `test_p47_predator_prey_filtering.py` is a same-target
tensor-product quadrature implementation of the declared additive-Gaussian
predator-prey closure.

The fixed-SGQF lane instead evaluates Gaussian moment approximations under a
fixed sparse-grid cloud of standardized GHQ nodes.

So even when the adapter is same-target in the law-of-transition / law-of-
observation sense, the actual numerical object being integrated differs once the
posterior is no longer close to Gaussian.

**Assessment:** strong explanation, closely related to H1.

## H3. Strong shared hypothesis: positivity/domain mismatch hurts SGQF more than the dense lower-rung route

The predator-prey model is biologically positive-state.

### Dense reference side
The dense lower-rung reference uses a bounded physical/reference box in the
predator-prey test, and the grid is chosen in a way that remains in the
positive-state region used by the declared target.

### Fixed-SGQF side
The fixed-SGQF Gaussian cloud is unbounded. The predator-prey adapter does not:
- truncate,
- project,
- or otherwise enforce positivity.

So SGQF quadrature mass can land on negative prey/predator states even when the
dense reference remains within a positive box.

That can distort both:
- value moments,
- and value sensitivities.

**Assessment:** strong and likely important specifically for predator-prey.

## H4. Medium-strong shared hypothesis: the additive Gaussian closure is too crude relative to the dense same-target recursion

The fixed-SGQF predator-prey adapter uses:
- deterministic RK4 transition mean,
- additive Gaussian `Q`,
- direct-state observation with Gaussian `R`.

The same-target dense reference still evaluates the full declared transition and
observation densities on a dense grid at each step.

If uncertainty interacts nonlinearly with the RK4 flow, then a mean+covariance
closure can miss effects that the dense retained-grid route still sees.

This is not a bug; it is a limitation of the closure class.

**Assessment:** medium-strong, likely contributes materially.

## Ranked value-mismatch hypotheses

### V1. Strongest value hypothesis: fixed SGQF is the wrong approximation class if the benchmark target rewards preserved non-Gaussian posterior shape

Predator-prey appears to be exactly the sort of model where the posterior shape
matters after the first update. Zhao-Cui’s retained-grid lower rung is designed
to preserve richer state-density structure. Fixed SGQF is designed to preserve a
Gaussian surrogate.

So the current test outcome — “finite and same-target, but not tight
dense-equality” — is what one should expect if the target family is sensitive to
non-Gaussian posterior shape.

### V2. Strong value hypothesis: low-order sparse-grid moments may be insufficient for the key mixed moments of predator-prey

Even with the repaired cloud, fixed SGQF uses a fixed low-order sparse-grid
quadrature rule. Predator-prey observation/update behavior depends on innovation
covariance and cross-covariance terms after a nonlinear RK4 propagation.

Those mixed moments may simply be underresolved compared with the dense tensor
reference.

### V3. Medium value hypothesis: factorization/veto structure can change the effective numerical path more sharply for SGQF than for the dense route

Fixed SGQF has a branch/failure contract and semidefinite-capable factorization
logic. Even when no branch failure occurs, the numerical factorization path is a
meaningful part of the SGQF computation. The dense reference does not depend on
that same covariance-factor branch structure.

This can create additional value-path divergence on sensitive nonlinear rows.

### V4. Weaker value hypothesis: there may still be useful predator-prey-specific tuning of SGQF sparse level / thresholds that has not been explored

This is weaker because the current gap can already be explained by approximation
class mismatch. But it remains possible that some tuned SGQF settings would
improve value closeness without changing the underlying lane.

That would still not remove H1/H2; it would only reduce the observed gap.

## Ranked gradient-mismatch hypotheses

### G1. Strongest gradient hypothesis: the SGQF score is only the derivative of the SGQF surrogate scalar, not the derivative of the dense target

This is the central point.

`tf_fixed_sgqf_score(...)` differentiates the SGQF Gaussian innovation scalar on
one declared fixed branch.

The dense predator-prey reference defines a different numerical object: the
same-target dense lower-rung filtering scalar.

So even if the SGQF score is internally correct, it can still disagree with a
dense-target derivative because they are derivatives of different functions.

**Assessment:** strongest explanation for why SGQF gradient evidence is weaker
than Zhao-Cui-style value evidence.

### G2. Strong gradient hypothesis: accepted-branch FD checks certify internal consistency, not external target correctness

Our predator-prey SGQF gradient tests now show:
- same scalar,
- same observations,
- same cloud,
- same branch config,
- same accepted branch signature,
- analytic score agrees with centered FD.

That is good evidence, but it is evidence of **internal correctness of the SGQF
surrogate derivative**, not of correctness relative to the dense reference
objective.

So the current gradient evidence is still necessarily weaker than a same-target
reference-gradient test would be.

### G3. Medium-strong gradient hypothesis: the predator-prey derivative adapter is structurally narrow

The current derivative adapter for predator-prey sets:
- `d_initial_mean = 0`
- `d_initial_covariance = 0`
- `d_process_covariance = 0`
- `d_observation_covariance = 0`
- direct observation parameter derivatives = 0

and only differentiates the deterministic transition mean with respect to the
native predator-prey parameter vector.

That is correct for the current chosen closure and parameterization, but it also
means the gradient evidence is tightly tied to that narrow parameterization and
closure contract.

Any hidden or future `theta`-dependence in noise or initialization is simply not
part of this derivative lane.

### G4. Medium gradient hypothesis: branch-valid FD windows are more fragile on predator-prey than on the easier scalar SGQF testbeds

Predator-prey is more nonlinear and more domain-sensitive than the scalar SGQF
fixtures. That means accepted-branch FD rows are inherently more delicate, and a
strict same-branch requirement can make the evidence local and narrow.

That again weakens the strength of gradient correctness evidence compared with a
clean dense-reference derivative oracle.

### G5. Weaker gradient hypothesis: autodiff-generated Jacobians inside the adapter may be noisier than hand-derived formulas

This is weaker and speculative. The current adapter uses autodiff to obtain
transition Jacobians and parameter derivatives from the same RK4 route, which is
good for scalar consistency. But it may be numerically noisier than a carefully
hand-derived Jacobian implementation.

This is not the main explanation; it is a secondary possibility.

## Why Zhao-Cui currently looks stronger

The current predator-prey Zhao-Cui evidence is stronger because it is tested
against the dense same-target reference with explicit quantitative gates on:
- total log likelihood,
- per-step log normalizers,
- mean path,
- covariance path,
- retained mass.

By contrast, fixed SGQF predator-prey currently has:
- same-target value diagnostics,
- accepted-branch FD-based gradient diagnostics,
- but no dense-target equality-grade value promotion,
- and no dense-target gradient oracle.

So part of the difference is a true method-class difference, and part is an
**evidence asymmetry**.

## Ranked strongest hypotheses

1. **Method-class mismatch**: fixed SGQF is a Gaussian assumed-density closure; Zhao-Cui lower rung is a retained-density/grid approximation tied to a dense same-target oracle.
2. **Target-integral mismatch after the first nonlinear update**: SGQF integrates a Gaussian surrogate, while the dense/Zhao-Cui route integrates the same-target closure more directly.
3. **Positivity/domain mismatch**: the SGQF cloud is unbounded and can allocate mass to biologically implausible negative states, unlike the bounded dense lower-rung reference box.
4. **Gradient evidence mismatch**: SGQF score checks currently certify only internal surrogate-derivative correctness, not dense-target derivative correctness.

## Weaker or more speculative hypotheses

1. There may still be useful predator-prey-specific SGQF tuning of sparse level or thresholds.
2. Adapter autodiff Jacobians may add some numerical noise.
3. Some of Zhao-Cui’s apparent advantage may be helped by the fact that its retained-grid route is geometrically aligned with the dense box reference used in the test.

## Practical conclusion

At the moment, the best explanation for why fixed SGQF does not match Zhao-Cui
on predator-prey value and gradient correctness is:

> fixed SGQF is solving a more aggressively collapsed Gaussian moment-closure
> problem, while the tested Zhao-Cui lower rung is preserving a richer density
> approximation on the same target and is being judged directly against a dense
> same-target oracle.

So the current gap is most plausibly a combination of:
- approximation-class difference,
- positivity/domain sensitivity,
- and weaker SGQF evidence relative to the dense same-target predicate.

This does **not** point first to another obvious low-level bug in the repaired
SGQF codepath. It points first to a real algorithmic/evidence difference.

## Nonclaims

This note does **not** conclude:
- that fixed SGQF is wrong,
- that Zhao-Cui is universally superior,
- that predator-prey SGQF is hopeless under all levels/tunings,
- that current SGQF gradient code is incorrect for its own surrogate scalar,
- or that the current gap is fully explained by one single cause.
