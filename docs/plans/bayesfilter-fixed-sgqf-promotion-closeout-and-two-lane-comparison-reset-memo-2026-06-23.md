# Reset memo: completed fixed-SGQF promotion governance and next two-lane comparison program

## Date
2026-06-23

## Context
This pass completed the **fixed-SGQF leaderboard-promotion governance program**.
The work started from a partially evidenced SGQF lane that had strong local
kernel support but did not yet have the same artifact-governance status as the
repo’s better-developed benchmark lanes. The program’s job was to:
- freeze the SGQF leaderboard scope,
- classify admitted vs blocked family cells,
- certify analytical-score rules,
- reconcile the KSC surrogate wrapper score status,
- propagate the updated SGQF status through deterministic coverage, preflight,
  and runner-governance artifacts,
- and close the program without pretending a real numeric benchmark run had
  occurred.

During the same session, a **new task** was also clarified: build a fresh
performance-comparison program for **SGQF vs UKF vs Zhao-Cui**, with **CUT4 only
in low-dimensional comparisons** and explicitly excluded from high-dimensional
comparison tables. That is a new program and should not be conflated with the
completed SGQF promotion-governance program.

## Decision / policy
Future sessions should assume the following unless a new reviewed artifact
explicitly changes them:

1. **The fixed-SGQF promotion-governance program is complete.**
   Its closeout artifacts are:
   - `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p9-closeout-result-2026-06-23.md`
   - `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-execution-ledger-2026-06-23.md`
   - `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md`

2. **Autodiff remains diagnostic-only for SGQF promotion claims.**
   Promoted SGQF score claims must be backed by explicit analytical derivative
   routes. Autodiff may validate an already implemented analytical route, but is
   not itself a promoted SGQF score path.

3. **KSC surrogate SGQF score admission is real but tightly scoped.**
   The KSC Gaussian-mixture surrogate SGQF route is admitted for:
   - value,
   - analytical score,
   but **only** within the declared **tiny same-target surrogate fixture**.
   Do not widen this into broad KSC support, actual transformed SV support, HMC
   readiness, or production-readiness claims.

4. **Blocked families remain blocked.**
   Under the current additive-state SGQF lane, the following literature-backed
   families remain blocked or not same-target:
   - actual transformed non-Gaussian SV,
   - spatial SIR,
   - predator-prey,
   - generalized SV synthetic from estimated/prior-mean values.

5. **No numeric benchmark execution was performed in the completed SGQF promotion
   program.**
   The refreshed preflight and runner artifacts are governance/status artifacts,
   not benchmark-performance evidence.

6. **The next task is a new comparison program.**
   The new program should be split into two lanes:
   - **low-dimensional lane**: SGQF, UKF, CUT4, Zhao-Cui
   - **high-dimensional/source-scope lane**: SGQF, UKF, Zhao-Cui only
   Do not include CUT4 in high-dimensional comparison tables.

7. **Do not mix actual transformed SV and KSC surrogate SV in a single ranking
   table.**
   Those are distinct target identities and must stay separated in any future
   comparison program.

## What changed
- File: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md`
  - Created and completed the SGQF leaderboard-promotion master program.
  - Final top-level status now records program completion.

- Files under `docs/plans/`
  - Wrote and completed P0–P9 subplans/results/review-ledger/stop-handoff
    artifacts for the SGQF promotion-governance program.
  - Closed the program with an explicit admitted/blocked/scope-qualified summary.

- File: `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-result-2026-06-18.md`
  - Reconciled the stale value-only governance note.
  - Updated it to reflect value + analytical-score admission for the tiny
    same-target surrogate fixture.

- File: `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
  - Added SGQF wrapper-score finite-difference tests for the KSC surrogate row.
  - Repaired an initially overstrong SGQF-vs-UKF score-equality test on blocked
    spectrum cases into the correct SGQF-wrapper finite-difference admission
    test.
  - Renamed stale value-only SGQF KSC test naming.

- File: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json`
  - Added SGQF KSC surrogate value+analytical-score machine-readable readiness.
  - Refreshed evidence-test nodeids and SGQF nonclaims.

- File: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json`
  - Refreshed the SGQF KSC smoke payload so it includes diagnostic analytical
    score information and no longer claims the analytical outer score is absent.

- File: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json`
  - Added `fixed_sgqf` to the frozen preflight roster.
  - Added SGQF preflight cells, value/gradient matrix entries, and explicit
    `scope_qualifier: tiny_same_target_surrogate_fixture_only` on the KSC row.

- File: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json`
  - Added `fixed_sgqf` to the downstream runner-governance layer.
  - Carried the KSC tiny-scope analytical-score qualifier through the runner
    JSON.

- Files:
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.csv`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.csv`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.md`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.md`
  - Regenerated downstream runner/status table exports so `fixed_sgqf` is present
    consistently.

## Bugs / blockers resolved
- Symptom:
  - The SGQF promotion-governance stack could not be closed honestly because the
    KSC row was still described as value-only in stale governance notes.
- Root cause:
  - Code and focused tests already supported the analytical wrapper score, but the
    written governance/result artifacts had not caught up.
- Resolution:
  - Reconciled the KSC result note and family/matrix/preflight/runner artifacts
    to the actual analytical wrapper-score state.

- Symptom:
  - The downstream benchmark-governance stack still had a silent `fixed_sgqf`
    hole because preflight and runner layers did not include the algorithm even
    after deterministic coverage was refreshed.
- Root cause:
  - Older frozen rosters and status-only runner artifacts predated SGQF’s final
    KSC tiny-scope score admission.
- Resolution:
  - Added `fixed_sgqf` into the preflight and runner-governance stack and carried
    the tiny-scope qualifier through those artifacts.

- Symptom:
  - An initial SGQF-vs-UKF score-equality test failed on repeated-spectrum rows
    during KSC wrapper-score certification.
- Root cause:
  - UKF can legitimately block on weak spectral-gap placement cases, so direct
    SGQF-vs-UKF score equality is not the right SGQF promotion oracle on all
    rows.
- Resolution:
  - Replaced it with the correct SGQF-wrapper analytical score vs SGQF-wrapper
    finite-difference admission test.

## Verification already run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p47_generalized_sv_equality.py -k "ksc and (score or fixed_sgqf or ukf)"
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py
```

Observed:
- KSC wrapper packet after repair: `32 passed, 14 deselected, 2 warnings`
- deterministic coverage + gradient semantics checks: `10 passed`
- preflight + deterministic + semantics checks: `15 passed`
- runner-matrix and related governance checks: `21 passed`
- warnings were TensorFlow Probability deprecation warnings, not SGQF failures.

## Current policy
- Treat the SGQF promotion-governance program as complete.
- Treat KSC SGQF value + analytical-score admission as tiny-scope only.
- Keep autodiff diagnostic-only for SGQF score claims.
- Keep blocked literature-backed SGQF families blocked unless a new reviewed
  same-target route is actually implemented.
- Treat the refreshed preflight/runner artifacts as governance/status artifacts,
  not benchmark-performance evidence.

## Known limitations / cautions
- No real numeric benchmark execution was performed by the completed SGQF
  promotion-governance program.
- No ranking claim has been established.
- No broad SGQF family-score admission beyond KSC has been established.
- The new requested comparison program is still only planned, not implemented.
- CUT4 must stay excluded from the high-dimensional lane of that new program.
- Actual transformed SV and KSC surrogate SV must stay separated in future
  comparison tables.

## Suggested next steps
1. Start a **fresh agent/session** for the new comparison-program implementation.
2. Use the new comparison-program plan in:
   - `/.claude/plans/partitioned-questing-valley.md`
   as the starting artifact.
3. First implementation step for the fresh agent:
   - create a new two-lane comparison master program under `docs/plans/`, with:
     - low-dimensional lane: SGQF / UKF / CUT4 / Zhao-Cui
     - high-dimensional lane: SGQF / UKF / Zhao-Cui only
     - explicit separation of actual transformed SV vs KSC surrogate SV
     - explicit same-target stop rules and nonclaims.
