# Experiment plan: actual-transformed-sv-augmented-noise-sgqf-next-step

metadata_date: 2026-06-26
program_id: actual-transformed-sv-augmented-noise-sgqf-next-step
status: DRAFT_READY_FOR_EXECUTION
master_context:
- `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-actual-transformed-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`
- `docs/plans/bayesfilter-source-scope-sgqf-unlocks-reset-memo-2026-06-24.md`
- `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-precursor-result-2026-06-26.md`
- `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-broader-precursor-ladder-result-2026-06-26.md`

## Question
What is the next honest engineering step for the actual-transformed SV SGQF lane
now that the repo has bounded internal evidence for an exact-transformed,
independent-panel, value-only precursor wrapper?

Decision to inform:
- whether to keep investing in the exact-transformed internal wrapper as if it
  were the main unlock route,
- or to pivot back to the master program’s preferred **augmented-noise-first**
  path for the actual-transformed SV family.

This plan adopts the second option.

## Mechanism being tested
The mechanism is an **augmented-noise SGQF precursor route** for the actual-
transformed SV family, following the master program’s P2 direction rather than
trying to elevate the current exact-transformed internal wrapper into a source-
scope admitted route.

Concretely, the next step is to test whether we can define and validate a
minimal augmented-noise execution path that:
1. preserves the family identity as belonging to the actual-transformed SV lane,
2. is explicitly labeled as a precursor/engineering route rather than a same-
   target admission,
3. can be exercised on short-prefix fixtures with deterministic CPU-only checks,
4. produces governance artifacts that keep value-only precursor status separate
   from source-row admission.

This plan does **not** attempt to prove that the augmented-noise route is already
same-target with the actual transformed SV source row.

## Why this plan is now justified
The two 2026-06-26 precursor result notes establish a bounded ceiling for the
current exact-transformed wrapper:
- it is real,
- it is value-only,
- it works on a small internal ladder,
- but it remains independent-panel and wrapper-specific.

Therefore, continuing to broaden that wrapper alone is no longer the most useful
next move for the program.

The master program already states that the preferred engineering unlock for the
actual-transformed SV family is the augmented-noise-first route. This plan turns
that policy into the next concrete step.

## Scope
- Variant: actual-transformed SV augmented-noise SGQF precursor route
- Objective: minimal value-only engineering unlock aligned with master-program P2
- Seed(s): deterministic in-repo fixtures / short-prefix cases only in the first
  pass
- Training steps: N/A
- HMC/MCMC settings: none
- XLA/JIT mode: none required for the first pass
- Expected runtime: focused CPU-only diagnostics and tests under a few minutes

First-pass scope boundaries:
- short-prefix or short-horizon execution only,
- no leaderboard promotion yet,
- no analytical score path,
- no T1000 full-run promotion in the first pass,
- no claim that the augmented-noise route closes the same-target source-row gap.

## Baseline / comparator
Primary engineering baseline:
- the current blocked state and route requirements in
  `docs/plans/bayesfilter-actual-transformed-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`

Primary numerical comparator for short-prefix diagnostics:
- the existing exact-transformed dense machinery already used in
  `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`

Explanatory comparator only:
- the internal exact-transformed SGQF wrapper evidence from the two 2026-06-26
  precursor result notes

What is explicitly **not** the promotion comparator in this plan:
- KSC surrogate routes,
- CUT4 / UKF approximations,
- runtime or finite execution alone,
- full T1000 runner emission.

## Evidence contract
Engineering question:
- can we add a clearly labeled augmented-noise SGQF precursor path for the
  actual-transformed SV lane and validate it on short-prefix diagnostics without
  confusing that precursor with source-row admission?

Exact baseline / comparator:
- same-target exact-transformed dense reference on short-prefix diagnostics,
  used only to decide whether the precursor route is numerically plausible enough
  to keep pursuing.

Primary promotion criterion:
- a short-prefix augmented-noise SGQF precursor path exists with explicit entry
  points and target metadata;
- it returns finite value outputs on the tested short-prefix cases;
- it shows bounded disagreement versus the exact-transformed dense reference that
  is good enough to justify keeping the precursor route alive as an engineering
  path.

Diagnostics that can veto:
- target-identity drift toward KSC surrogate or some other silent substitute,
- inability to define the precursor route without misleading same-target
  narration,
- non-finite outputs on short-prefix cases,
- disagreement versus the exact-transformed dense reference so large that the
  precursor route would not even be useful as an engineering stepping stone,
- artifacts or tests that silently upgrade value-only precursor execution into
  row admission.

Diagnostics that are explanatory only:
- gap size relative to the internal exact-transformed SGQF wrapper,
- sparse-level sensitivity,
- runtime / point-count details.

What will not be concluded even if this plan succeeds:
- no same-target source-row admission,
- no analytical-score claim,
- no generic non-Gaussian SGQF core support,
- no HMC or production-readiness claim,
- no guarantee that the eventual source-scope row becomes admissible.

Artifact that will preserve the result:
- a result note under `docs/plans/` for the augmented-noise next step,
- focused tests in the actual-transformed SV evidence lane,
- any necessary row-status artifact updates kept explicitly at precursor/value-
  only status.

## Success criteria
Primary:
- a minimal augmented-noise SGQF precursor path is implemented or explicitly
  outlined with concrete entry points;
- short-prefix deterministic checks pass and return finite outputs;
- the route’s metadata and tests preserve precursor/value-only wording;
- no artifact falsely treats the route as same-target row admission.

Secondary:
- the route can be compared against the exact-transformed dense reference on a
  small short-prefix case without numerical collapse;
- the resulting evidence is strong enough to justify a later runner/leaderboard
  integration phase under explicit precursor status.

Sanity checks:
- no KSC surrogate substitution,
- no silent use of the current internal exact-transformed wrapper as if it were
  already the mainline source-scope unlock,
- no public export or score-path addition in the first pass unless separately
  reviewed.

## Diagnostics
Primary:
- short-prefix value finiteness,
- short-prefix SGQF-vs-exact-transformed dense gap,
- target metadata / row-status correctness,
- whether the implementation remains clearly precursor-only in naming and tests.

Secondary:
- sparse-level sensitivity on the precursor route,
- gap comparison against the existing internal exact-transformed wrapper,
- whether the short-prefix route seems stable enough to justify a later longer
  prefix or runner integration step.

## Expected failure modes
- the augmented-noise route may be difficult to define cleanly without blurring
  target identity;
- the short-prefix disagreement against the exact-transformed dense reference may
  be too large to justify even precursor status;
- the implementation may try to lean on the unfinished generic non-Gaussian SGQF
  core and become scope-unsafe;
- tests may accidentally promote “value executes” into “row admitted”.

## Pre-mortem
How the run could pass while misleading us:
- a finite augmented-noise route could look like progress even if its target
  identity or interpretation is unclear;
- a short-prefix match could be good enough to keep the precursor alive but still
  be narratively overstated as same-target evidence.

How the run could fail for implementation/tuning rather than scientific reasons:
- the first precursor implementation may use a sparse level or short-prefix setup
  that is too weak;
- the route may need a cleaner metadata / test harness split rather than a major
  mathematical rethink.

Cheap diagnostic to distinguish those explanations:
- inspect whether failures are target-identity/governance failures,
  implementation-path failures, or purely numerical disagreement on a single
  short-prefix case.

## Skeptical audit
Wrong-baseline risk:
- do not treat the internal exact-transformed SGQF wrapper as if it were the
  target admission oracle for this plan.

Proxy-promotion risk:
- finite precursor execution is not source-row promotion.

Hidden-assumption risk:
- do not assume the augmented-noise route inherits the same numerical behavior as
  the internal exact-transformed wrapper.

Artifact-answer mismatch risk:
- if any tests or result notes use language suggesting row admission, the plan
  fails its governance goal even if the code runs.

Audit verdict:
- proceed, but keep the first pass strictly at the precursor/value-only,
  short-prefix level.

## Files likely to modify
Primary implementation candidates:
- `bayesfilter/highdim/sv_mixture_cut4.py`
- possibly a new helper adjacent to the actual-transformed SGQF lane if that is
  cleaner than further growing the current exact-transformed wrapper section

Primary tests:
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`

Possible later artifact surfaces (not necessarily first-pass edits):
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`

## Execution order
1. Identify the minimal short-prefix augmented-noise SGQF precursor API and its
   target metadata.
2. Add a short-prefix deterministic test in the actual-transformed evidence lane.
3. Compare the precursor numerically against the exact-transformed dense
   reference on the small short-prefix case.
4. Keep any resulting status at precursor/value-only and do not touch row
   admission artifacts unless the precursor test pass is clean and its wording is
   explicit.
5. Record a result note describing whether the augmented-noise-first path is now
   genuinely opened as an engineering route.

## Command
First-pass verification commands once implementation exists:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  bayesfilter/highdim/sv_mixture_cut4.py \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

## Interpretation rule
- If a short-prefix augmented-noise SGQF precursor path can be implemented with
  clear precursor-only metadata and numerically plausible same-target comparison
  behavior, then keep pursuing the augmented-noise-first route in later phases.
- If the route only works by blurring target identity or by narratively treating
  precursor execution as admission, stop and keep the row blocked.
- If the precursor is numerically poor but governance-clean, record that as an
  engineering limit rather than as evidence against the whole family program.
