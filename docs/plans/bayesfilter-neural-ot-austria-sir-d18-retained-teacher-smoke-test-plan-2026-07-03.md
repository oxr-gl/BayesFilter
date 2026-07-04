# Experiment plan: Austria SIR d18 retained-teacher interface smoke test

## Question
Does the retained-teacher / donor-aligned warm-start interface work correctly on the first genuinely high-dimensional BayesFilter target, the fixed Austria spatial SIR d18 model, before any large-particle or speed claims are attempted?

## Mechanism being tested
This experiment tests interface correctness and the smallest warm-start evidence path on the fixed highdim target
`bayesfilter.highdim.models.zhao_cui_sir_austria_model()`:
- generate or adapt a retained-teacher teacher-data artifact on the Austria SIR d18 state/observation contract,
- train the current donor-aligned one-half retained-Sinkhorn student on that artifact,
- run a small discriminating-budget replay comparison against zero-init,
- and verify that the interface preserves finite behavior, shape correctness, and the retained-Sinkhorn residual contract.

The goal is not to prove large-scale superiority. The goal is to validate that the retained-teacher route can be attached coherently to a real high-dimensional nonlinear structured model already governed in the repo.

## Scope
- Variant: fixed-parameter Austria spatial SIR d18 only via `zhao_cui_sir_austria_model()`
- Objective: first high-dimensional retained-teacher interface smoke test
- Seed(s): one deterministic train/heldout seed family first; expand only after the first smoke test passes
- Training steps: minimal donor-aligned student training only; keep the same one-half route (`meta_ot_log_u`) and objective path initially
- HMC/MCMC settings: N/A
- XLA/JIT mode: CPU-only eager/default TensorFlow for the first smoke test unless interface constraints require an explicitly documented graph helper
- Expected runtime: short diagnostic run; should stay in smoke-test territory rather than benchmark territory

## Evidence contract

### Exact baseline
Zero-initialized corrected retained-Sinkhorn replay on the exact same Austria SIR d18 heldout teacher-data artifact, with the same epsilon, tolerance floor, and budget ladder.

### Primary pass criterion
Pass means all of the following hold on the Austria SIR d18 smoke test artifact:
1. the teacher-data path generates a finite artifact with the correct state/observation shapes;
2. the donor-aligned student training path runs and improves train loss from initialization;
3. at least one declared low corrective budget is discriminating (zero-init not already exact);
4. the replay comparison artifact is finite and residual-safe;
5. the result can be interpreted under the same discriminating-versus-saturated contract already used for LGSSM, SV, and range-bearing.

### Veto diagnostics
- shape mismatch between Austria SIR d18 state/observation tensors and the retained-teacher interface;
- non-finite teacher states, student predictions, or replay outputs;
- residual contract failure on the corrected retained-Sinkhorn replay;
- no heldout examples captured in the artifact;
- use of only saturated budgets so the smoke test cannot furnish a discriminating rung;
- any attempt to convert this smoke test into a large-`N`, speed, or production claim.

### Explanatory-only diagnostics
- train and heldout `log_u` loss,
- student-better-or-equal count,
- exact budget at which saturation begins,
- runtime,
- model size,
- per-example replay breakdown.

### What will not be concluded even if the run passes
- no large-scale runtime claim,
- no `N=10000` or larger-particle success claim,
- no GPU scaling claim,
- no production-readiness claim,
- no broad “works for our problem” claim,
- no parameterized-SIR claim yet.

## Success criteria
- The Austria SIR d18 retained-teacher artifact is generated and validated.
- The smoke-test result clearly distinguishes engineering interface success from any local usefulness result.
- At least one discriminating budget exists on the first Austria artifact, or the run cleanly records that a discriminating-budget recovery plan is needed before further claims.
- If a discriminating budget exists, the donor-aligned route either:
  - shows local usefulness on that rung, or
  - clearly fails there, which is still a valid interface result even if usefulness is not shown.

## Diagnostics
Primary:
- finite teacher-data artifact with reproducibility digest
- train loss improvement from initialization
- zero-init saturation probe on a small low-budget ladder
- corrected replay RMSE vs zero-init on discriminating budgets
- corrected replay residuals on the same budgets

Secondary:
- heldout `log_u` loss
- per-budget student-better-or-equal count
- first saturated budget on the ladder
- train/heldout example counts

Sanity checks:
- CPU-only manifest (`CUDA_VISIBLE_DEVICES=-1` before import)
- state dimension `18`, observation dimension `9`
- route metadata still identifies the donor-aligned fixed-target retained-Sinkhorn family
- result note explicitly separates interface success from scale claims

## Expected failure modes
- the retained-teacher interface assumes lower-dimensional geometry and breaks on the d18 tensor shapes;
- the teacher-data capture rule yields too few or no useful heldout examples on the first Austria artifact;
- the first budget ladder is entirely saturated or entirely too weak, so the rung is not informative;
- donor-aligned training improves the latent loss but does not improve replay at discriminating budgets;
- a graph/eager mismatch appears because some highdim helpers rely on `.numpy()` validation paths.

## What would change our mind
- If the Austria SIR d18 smoke test passes with a discriminating rung and local usefulness, then the retained-teacher route has crossed from small-family evidence into a genuine high-dimensional structured model.
- If the interface passes but usefulness does not appear, the next claim should be engineering viability only, not performance usefulness.
- If the interface fails on shapes, finiteness, or replay residuals, the next step is interface repair, not larger-`N` testing.
- If the interface passes but the budget ladder is non-discriminating, the next step is ladder/artifact calibration before any usefulness conclusion.

## Skeptical audit before execution
Status: `REVIEWED_FOR_SMOKE_TEST_ONLY`

Checked risks:
1. **Jumping too early to scale claims** — prevented by restricting this plan to an interface smoke test and explicitly excluding `N=10000` conclusions.
2. **Wrong target choice** — mitigated by using the repo-native fixed Austria SIR d18 model rather than a new highdim target.
3. **Conflating engineering success with usefulness** — prevented by requiring the result note to separate those ledgers.
4. **Reusing budgets from another family** — prevented by requiring a fresh low-budget saturation probe on the Austria artifact.
5. **Adding parameter-surface complexity too soon** — prevented by using the fixed Austria model first rather than the parameterized variant.

## Command
```bash
# To be filled once the Austria SIR d18 retained-teacher teacher-data and replay runners exist.
# The first execution should follow this order:
# 1. teacher-data generation / capture smoke
# 2. zero-init low-budget probe on the same artifact
# 3. donor-aligned replay evaluation on any discriminating rung identified by step 2
```

## Interpretation rule
- If the interface fails before producing a finite artifact or finite replay outputs, conclude interface failure only.
- If the interface succeeds but no discriminating budget exists, conclude that the first Austria artifact needs ladder/artifact calibration before usefulness can be judged.
- If the interface succeeds and a discriminating budget exists, interpret student-vs-zero-init only on that rung.
- Even if the smoke test passes, do not conclude anything about large-`N` speed or broader production readiness.

## Execution note after first run
The first Austria SIR d18 teacher-data execution hit a real blocker before any probe/eval stage:
- `FloatingPointError: Sinkhorn row residual exceeded tolerance envelope`
- raised during teacher coupling generation in the new teacher-data runner.

Under this plan, execution therefore stops here and classifies the current state as an
Austria SIR d18 teacher-generation / OT numerical-stability blocker. The next justified
step is a reviewed blocker-repair amendment focused on Sinkhorn scale/tolerance/iteration
stability for the teacher-generation stage, not continued replay evaluation.
