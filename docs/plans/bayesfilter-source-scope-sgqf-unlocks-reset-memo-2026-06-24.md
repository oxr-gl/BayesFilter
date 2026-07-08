# Reset memo: source-scope-sgqf-unlocks-and-augmented-noise-pivot

## Date
2026-06-24

## Context
This pass started from the new two-lane leaderboard work, where the highdim
source-scope packet initially over-blocked SGQF. The user correctly pushed back:
SGQF should not be blocked on LGSSM or on every high-dimensional row if the repo
already has executable routes.

The work then split into three threads:
1. repair the highdim leaderboard so SGQF is executed where current code/test
   support already exists,
2. write family-specific unlock plans for the remaining blocked rows,
3. add a source-scope analytical-gradient / analytical-score governance layer so
   score promotion does not drift row by row.

During that process, the intended unlock strategy changed:
- the initial direct same-target unlock direction for actual transformed SV and
  generalized SV was reconsidered,
- the preferred first unlock path became **augmented-noise SGQF precursor routes**
  for those non-Gaussian families,
- spatial SIR remained a route-development problem rather than a simple harness
  problem.

The session then began implementing a **generic non-Gaussian SGQF update** in
code, but that implementation is only partially landed and has not yet been
verified end-to-end.

## Decision / policy
Future sessions should assume the following unless a new reviewed artifact says
otherwise:

1. **One master program should govern the source-scope SGQF unlocks.**
   Use:
   - `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
   as the umbrella artifact rather than treating each family plan as isolated.

2. **Value unlock and analytical-score unlock are separate gates.**
   A row may be `value_only_executed` while still being score-blocked or
   diagnostic-score-only.

3. **Current SGQF source-scope family states are row-specific, not blanket.**
   The current ledger is:
   - LGSSM → `value_only_executed`, score blocked
   - actual transformed SV → blocked for value/score
   - KSC surrogate T1000 → `value_only_executed`, score diagnostic-only
   - spatial SIR → blocked for value, score blocked/no-free-theta
   - predator-prey → `value_only_executed`, score admitted
   - generalized SV source row → blocked for value/score

4. **Augmented-noise-first is now the preferred engineering unlock path for the
   non-Gaussian source rows**:
   - actual transformed SV
   - generalized SV
   This is a precursor route, not automatic same-target source-row admission.

5. **The highdim leaderboard should not blanket-block SGQF.**
   The repaired packet already executes SGQF on:
   - source-scope LGSSM,
   - KSC surrogate T1000,
   - predator-prey.

6. **CUT4 remains excluded from the highdim/source-scope leaderboard lane.**

7. **Actual transformed SV and KSC surrogate SV must stay separate target
   identities and separate rows/tables.**

## What changed
- File: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.json`
  - Repaired the highdim packet so SGQF is not blanket-blocked.
  - Current SGQF execution appears on LGSSM, KSC surrogate T1000, and predator-prey.
  - Added explicit `score_status` and `score_status_reason` fields.

- File: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.md`
  - Regenerated the human-readable highdim table to match the repaired SGQF row
    states and score statuses.

- File: `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
  - Reworked the highdim harness so SGQF runs where existing reviewed routes are
    present:
    - direct affine route for LGSSM,
    - direct KSC surrogate value route,
    - direct predator-prey adapter route.
  - Added score-status fields to emitted rows.

- File: `docs/plans/bayesfilter-source-scope-sgqf-admission-ledger-2026-06-24.md`
  - Wrote the unified source-scope SGQF value/score admission ledger.

- File: `docs/plans/bayesfilter-source-scope-sgqf-analytical-gradient-ledger-2026-06-24.md`
  - Wrote the unified analytical-gradient / score-status ledger.

- Files:
  - `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
  - `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
  - Added checks for the new SGQF ledgers and score-status policy.

- Files under `docs/plans/` created:
  - `bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
  - `bayesfilter-source-scope-sgqf-analytical-gradient-gate-plan-2026-06-24.md`
  - `bayesfilter-generalized-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`
  - `bayesfilter-actual-transformed-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`
  - `bayesfilter-spatial-sir-source-scope-sgqf-unlock-plan-2026-06-24.md`

- File: `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
  - Revised to reflect the augmented-noise-first unlock strategy for actual
    transformed SV and generalized SV.
  - Added a documentation phase and a `docs/main.tex` compile phase.

- File: `docs/plans/bayesfilter-actual-transformed-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`
  - Revised so the first unlock is an augmented-noise SGQF precursor route,
    not immediate same-target admission.

- File: `docs/plans/bayesfilter-generalized-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`
  - Revised similarly: augmented-noise SGQF precursor first, same-target
    admission later.

- File: `bayesfilter/nonlinear/fixed_sgqf_tf.py`
  - Partially modified to introduce a new `TFFixedSGQFNonGaussianModel` type and
    broaden the `tf_fixed_sgqf_filter(...)` type annotation.
  - **Important:** the non-Gaussian SGQF update implementation is not finished.

- File: `bayesfilter/highdim/sv_mixture_cut4.py`
  - Partially modified to add:
    - `ExactTransformedSVPanelFilterResult`
    - `exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)`
  - This is an initial same-target value-path attempt for exact transformed SV,
    but it is **not yet wired, tested, or validated** end-to-end.

## Bugs / blockers resolved
- Symptom:
  - SGQF was shown as blocked for LGSSM and for all highdim rows, which made the
    leaderboard misleading.
- Root cause:
  - The initial highdim harness used an overly conservative route-selection rule
    and did not honor row-specific SGQF support already present in code/tests.
- Resolution:
  - Repaired the highdim harness and packet to execute SGQF on the rows with
    existing reviewed routes.

- Symptom:
  - The family unlock plans lacked a unified score-promotion policy.
- Root cause:
  - They were value-first row plans written independently.
- Resolution:
  - Added a master program, analytical-gradient gate plan, and analytical-gradient
    ledger.

## Verification already run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_predator_prey_filtering.py -k "fixed_sgqf"
```

```bash
python -m compileall -q \
  docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py \
  tests/highdim
```

Observed:
- contract / source-scope tests passed,
- KSC SGQF score-focused tests passed,
- predator-prey SGQF-focused tests passed,
- compile checks passed.
- A larger combined pytest command was killed by the environment, so verification
  was continued in smaller chunks.

## Current policy
- Treat the source-scope SGQF family unlocks as one governed program under the
  master program.
- Treat actual transformed SV and generalized SV as **augmented-noise-first
  precursor-route** unlocks, not as already admitted same-target SGQF rows.
- Treat spatial SIR as a route-development problem first.
- Keep score claims narrower than value claims until explicitly promoted.

## Known limitations / cautions
- The generic non-Gaussian SGQF update is **partially started but not complete**.
- `TFFixedSGQFNonGaussianModel` exists only as a partial type addition right now;
  the filter core still uses the Gaussian innovation-update path.
- `exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)` exists but has
  not yet been fully integrated or verified.
- The highdim harness still has no actual-transformed-SV SGQF execution row.
- The generalized-SV source row is still blocked.
- Spatial SIR remains blocked pending deeper route-development.
- Documentation phase and `docs/main.tex` compile phase were added to the master
  program but have not yet been executed.

## Suggested next steps
1. Start a **fresh agent/session** from this reset memo rather than continuing to
   layer more edits on the current partially modified SGQF core.
2. First action for the fresh agent:
   - audit the partial edits in:
     - `bayesfilter/nonlinear/fixed_sgqf_tf.py`
     - `bayesfilter/highdim/sv_mixture_cut4.py`
   - decide whether to continue the generic non-Gaussian update cleanly or to
     rewrite that work more coherently from the augmented-noise-first strategy.
3. Then continue the master program in this order:
   - actual transformed SV precursor route,
   - generalized SV precursor route,
   - spatial SIR route gate,
   - analytical-gradient gate refresh,
   - documentation phase,
   - `docs/main.tex` compile phase,
   - closeout.
