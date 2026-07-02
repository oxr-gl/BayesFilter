# Experiment plan: Meta OT-aligned retained-Sinkhorn evaluation under a better evidence contract

## Question
What evidence would distinguish:
1. donor-aligned implementation success,
2. local low-budget usefulness,
3. primary-budget non-promotion under a saturated baseline,
4. and genuine evidence against the retained-teacher algorithm itself?

## Mechanism being tested
The Meta OT-aligned fixed-target retained-Sinkhorn refit:
- predicts one donor-style dual half (`canonical_log_u`),
- recovers the complementary half teacher-consistently,
- trains with a donor-style dual-objective route plus local half-supervision,
- and deploys through corrected retained Sinkhorn replay.

The experiment is not testing the annealed route. It is testing whether the fixed-target donor-aligned route shows useful behavior under an evaluation contract that does not let a saturated high-budget zero-init baseline masquerade as algorithm failure.

## Scope
- Variant: fixed-target retained-Sinkhorn, Meta OT-aligned one-half refit only
- Objective: separate donor-faithful implementation status from local usefulness and from primary-budget saturation
- Seed(s): keep current deterministic teacher-data seed family first; expand only if the first better-contract run remains ambiguous
- Training steps: current donor-aligned refit route; no annealed-route training
- HMC/MCMC settings: N/A
- XLA/JIT mode: CPU-only current retained-Sinkhorn route unless a later phase justifies acceleration checks
- Expected runtime: short to moderate CPU experiment, depending on whether the heldout ladder and expanded teacher-data artifact are both regenerated

## Evidence contract

### Exact baseline
The baseline is still the same corrected retained Sinkhorn teacher route with zero initialization on the same fixed-target problem family.

### Primary promotion criterion
Promotion is **not** “beat zero-init at a single high corrective budget where zero-init may already be exact.”

Instead, the primary promotion criterion is:
- on a declared budget ladder with at least one **discriminating** budget where zero-init is not already exact,
- the donor-aligned route must improve corrected teacher-cloud fidelity or equivalent replay-sensitive metrics relative to zero-init,
- while preserving the same residual contract and finite corrected route behavior.

### Veto diagnostics
- non-finite corrected outputs,
- residual contract failure,
- route drift away from fixed-target retained Sinkhorn,
- teacher-data / manifest mismatch,
- a “promotion” conclusion drawn from a budget rung where zero-init is already exact or effectively exact.

### Explanatory-only diagnostics
- training objective decrease,
- low-budget wins taken in isolation,
- model size,
- runtime,
- latent one-half loss,
- qualitative replay examples without budget-context.

### What will not be concluded even if the run passes
- no paper-level proof,
- no annealed-route conclusion,
- no broad cross-envelope generalization claim,
- no posterior correctness,
- no HMC readiness,
- no production-default claim.

## Success criteria
- The report explicitly separates:
  - donor-aligned implementation status,
  - local low-budget usefulness,
  - primary-budget non-promotion,
  - and algorithm-level evidence.
- At least one declared **discriminating** budget rung exists where zero-init is not already exact.
- The donor-aligned route either:
  - shows advantage at the discriminating rung, or
  - clearly fails there, in which case the result is a local non-promotion result rather than a paper-failure headline.
- The final write-up must not headline the result as “algorithm failed” unless the evidence contract actually supports that level of conclusion.

## Diagnostics
Primary:
- corrected teacher-cloud RMSE vs zero-init across a budget ladder
- corrected residual contract across the same ladder
- zero-init saturation check at each budget rung
- explicit route identifier and donor-aligned target identifier in the artifact

Secondary:
- one-half prediction loss (`canonical_log_u`)
- donor-style dual-objective trend
- per-example replay breakdown
- heldout example count and route-manifest digest

Sanity checks:
- fixed-target retained-Sinkhorn route only
- donor-aligned one-half prediction path actually used
- teacher-side complementary recovery actually used
- teacher-data artifact and heldout eval artifact have reproducibility digests

## Expected failure modes
- the better evidence contract still shows that the donor-aligned route loses at the discriminating rung,
- the current tiny teacher-data artifact remains too weak to discriminate clearly,
- zero-init saturates too many rungs, making the ladder still poorly informative,
- objective-based donor loss improves but corrected replay does not.

## What would change our mind
- If the donor-aligned route wins only at low budgets but loses whenever the baseline budget is generous, then the right conclusion is “local low-budget usefulness only,” not broad algorithm failure.
- If a discriminating budget ladder still shows no benefit from the donor-aligned route, then the evidence against local usefulness strengthens.
- If expanded teacher-data plus the better ladder shows consistent gain at discriminating budgets, then the current non-promotion should be reclassified as a contract-framing issue rather than an algorithm-failure signal.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_data_range_bearing_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_range_bearing_tf
```

## Skeptical audit before execution
- Baseline check: fair; zero-init uses the same corrected retained-Sinkhorn route on the same fixed-target family.
- Proxy-metric check: promotion is based on replay-sensitive teacher-cloud RMSE on discriminating budgets, not merely training-loss decrease.
- Environment check: this is intentionally a CPU-only retained-Sinkhorn diagnostic; `CUDA_VISIBLE_DEVICES=-1` must be set before TensorFlow import.
- Artifact-answer check: the heldout-eval artifact explicitly records budget regime, residuals, and the no-discriminating-budget vs non-promotion distinction needed to answer the question.
- Audit result: pass for executing the current range-bearing better-contract rung. A no-discriminating-budget outcome for the current rung is informative, but does not by itself prove that no discriminating rung exists anywhere.

## Interpretation rule
- If zero-init is already exact (or effectively exact) at the primary rung, then failure to beat zero-init there is **not** sufficient evidence of algorithm failure.
- If the donor-aligned route improves replay at one or more discriminating budgets while preserving residuals, then the result should be reported as local usefulness under that contract, even if a saturated high-budget rung remains non-promoting.
- If the donor-aligned route fails even on discriminating budgets, then the result is stronger evidence of local non-usefulness.
- In every case, the headline must distinguish local non-promotion from algorithm failure.

## Follow-on governance after the range-bearing result
The 2026-06-29 range-bearing donor-aligned run established only that the current
candidate range-bearing rung (`10`, `20`) is saturated for zero-init. That
result governs the next step as follows:
- do **not** reuse the current range-bearing rung as if it were a valid
  promotion/non-promotion comparator;
- first execute the P6 zero-init ladder probe to determine whether the current
  artifact has any discriminating range-bearing budget at all;
- only if such budgets exist may the range-bearing donor-aligned evaluation be
  rebound to those budgets;
- otherwise, a reviewed harder-artifact amendment is required before further
  range-bearing claims.

Reference: `docs/plans/bayesfilter-neural-ot-metaot-refit-p6-range-bearing-discriminating-rung-subplan-2026-06-29.md`
