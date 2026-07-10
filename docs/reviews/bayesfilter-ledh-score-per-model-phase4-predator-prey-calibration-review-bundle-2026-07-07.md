# Claude Read-Only Review Bundle: Predator-Prey Full-Row Correctness Calibration

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex remains supervisor and executor. Claude is read-only reviewer only.

## Objective

Review whether the predator-prey full-row correctness calibration subplan is
boundary-safe before any full `N=10000,T=20` score admission run.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase4-predator-prey-repair-rung3-gpu-smoke-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase4-predator-prey-full-row-correctness-calibration-subplan-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_predator_prey_score.py`
- `tests/highdim/test_ledh_predator_prey_score_phase4_contract.py`

## Evidence Contract

Admitted score means no-tape total derivative of:

```text
observed_data_log_likelihood_estimator
```

reported as:

```text
log_likelihood
```

for row `zhao_cui_predator_prey_T20`, physical parameter order
`[r,K,a,s,u,v]`.

The latest evidence is mixed:

- tiny CPU-hidden route passed all-coordinate same-scalar FD;
- bounded FP64 GPU smoke passed tightly;
- bounded float32/TF32 GPU smoke failed strict FD tolerances and now writes
  `blocked_score_not_run`;
- no full `N=10000,T=20` score artifact exists.

## Calibration Subplan Summary

The calibration subplan states:

- no full-row admission may be claimed from tiny FP64 checks alone;
- no full `N=10000,T=20` score admission run may launch before this
  calibration subplan is reviewed;
- FP64 correctness evidence and FP32/TF32 production runtime/memory evidence
  are separate ledgers unless a reviewed result explicitly bridges them;
- runtime and memory cannot substitute for score correctness;
- noisy FP32/TF32 FD cannot be treated as pass by loosening tolerances after
  seeing failures without reviewed justification;
- final full score admission still requires a score artifact that validates
  with `validate_ledh_score_artifact(..., require_admitted=True)`.

The required calibration ladder is:

1. FP64 bounded GPU correctness ladder:
   - `T=2,N=64`;
   - `T=5,N=256`;
   - all six coordinate finite differences;
   - strict default tolerance `atol=5e-3, rtol=5e-3`.
2. FP32/TF32 production-memory smoke:
   - same route and chunking;
   - correctness diagnostic is explanatory unless a reviewed tolerance ladder
     passes;
   - memory and runtime alone cannot admit correctness.
3. If FP64 bounded correctness passes but FP32/TF32 FD remains noisy:
   - write a policy result that separates FP64 correctness evidence,
     FP32/TF32 production runtime/memory evidence, and full-row admission
     status;
   - do not admit the full score unless the policy explicitly requires and
     obtains a validating full score artifact.

The stop conditions are:

- stop if FP64 bounded correctness fails;
- stop if FP32/TF32 tolerance policy cannot be justified;
- stop if full-row memory/correctness evidence cannot be produced within
  bounded execution;
- stop if the score artifact cannot validate against the admitted value
  artifact;
- stop if no-tape provenance becomes ambiguous;
- stop if review finds a material issue that does not converge after five
  rounds.

## Review Questions

1. Does the calibration subplan correctly refuse full-row admission from tiny
   FP64 evidence alone?
2. Does it separate correctness evidence from FP32/TF32 production memory and
   runtime evidence?
3. Does it avoid loosening FD tolerances after seeing failures without reviewed
   justification?
4. Is it safe to execute this calibration subplan before any full score
   admission run?

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
