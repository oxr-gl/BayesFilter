# Claude Read-Only Review Bundle: Phase 5 Actual-SV Tiny Result And Full-Row Subplan

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex remains supervisor and executor. Claude is read-only reviewer only.

## Objective

Review whether the Phase 5 actual-SV score result is boundary-safe and whether
the full-row score/memory subplan is safe to execute next.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-full-row-score-subplan-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`
- `tests/highdim/test_ledh_actual_sv_score_phase5_contract.py`
- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-tiny-score-diagnostic-2026-07-07.json`

## Evidence Contract

Admitted LEDH score means no-tape total derivative of:

```text
observed_data_log_likelihood_estimator
```

reported as:

```text
log_likelihood
```

for row:

```text
zhao_cui_sv_actual_nongaussian_T1000
```

with:

- target observation policy: `transformed_actual_sv_log_y_square`;
- theta coordinate system: `synthetic_unconstrained`;
- score parameter names: `[gamma_unconstrained, log_beta]`.

`GradientTape`, `ForwardAccumulator`, hidden autodiff, stopped partials, KSC
target substitution, raw Gaussian target substitution, augmented-noise
Gaussian-closure substitution, tiny diagnostic promotion, and memory/runtime
proxy promotion are blockers.

## Phase 5 Result Summary

Implemented a bounded actual-SV no-tape manual total score route:

```text
manual_total_vjp_no_autodiff_same_scalar_actual_sv_ledh_pfpf_ot
```

Tiny diagnostic:

- `T=2,N=64`, seed `[81120]`;
- `score_admission_status = tiny_score_diagnostic_not_admitted`;
- `score_correctness.status = pass`;
- `score = [-0.13676940977770666, 0.38478205551642064]`;
- finite-difference score:
  `[-0.13676941023277323, 0.3847820563884774]`;
- `max_abs_error = 8.720567601372409e-10`;
- `max_rel_error = 3.3272540035606193e-09`;
- `memory_diagnostics.n10000_memory_pass = false`.

Local checks:

- focused Phase 5 score tests: `7 passed, 2 warnings`;
- combined Phase 5 replay/schema checks: `28 passed, 2 warnings`.

The result explicitly does not admit the full score.

## Full-Row Subplan Summary

The subplan requires a separate memory-risk audit before any full
`N=10000,T=1000` score command. It says to stop and write a blocker if the
current stored-record reverse scan is unsafe. If review allows execution, it
requires a trusted GPU ladder before full row and still requires a validating
full score artifact for admission.

## Review Questions

1. Does the Phase 5 result correctly classify the tiny diagnostic as pass but
   not full score admission?
2. Does the result preserve the exact transformed actual-SV target and avoid
   KSC/raw-Gaussian/augmented-noise substitution?
3. Does the full-row subplan correctly require a memory-risk audit and forbid
   full execution if the stored-record reverse scan is unsafe?
4. Is it boundary-safe to continue to the full-row score/memory subplan?

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
