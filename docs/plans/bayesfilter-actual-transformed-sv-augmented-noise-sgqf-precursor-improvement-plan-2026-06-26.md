# Experiment plan: actual-transformed-sv-augmented-noise-sgqf-precursor-improvement

metadata_date: 2026-06-26
program_id: actual-transformed-sv-augmented-noise-sgqf-precursor-improvement
status: DRAFT_READY_FOR_EXECUTION
master_context:
- `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-next-step-result-2026-06-26.md`
- `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-next-step-plan-2026-06-26.md`
- `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`

## Question
Can we materially tighten the **short-prefix, value-only augmented-noise SGQF
precursor** for the actual-transformed SV family without changing its claim
class or blurring target identity?

What decision will this inform?
- whether the current augmented-noise precursor should remain a viable
  engineering stepping stone, or
- whether its looseness is large enough that the honest next action is to leave
  the row blocked rather than keep polishing this route.

## Mechanism being tested
The mechanism is the current precursor route in:
- `bayesfilter/highdim/sv_mixture_cut4.py`
  - `actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_filter(...)`

The pass is limited to **numerical-policy improvement** of that precursor, not a
change in its conceptual status.

Candidate knobs to test:
1. `sparse_level`
2. `observation_variance_floor`

The route remains:
- independent-panel,
- value-only,
- short-prefix,
- augmented-noise-first,
- not a same-target admission route.

## Scope
- Variant: short-prefix augmented-noise SGQF precursor improvement
- Objective: reduce the current short-prefix gap profile while preserving the
  precursor-only claim class
- Seed(s): deterministic in-repo tiny fixture only in the first pass
- Training steps: N/A
- HMC/MCMC settings: none
- XLA/JIT mode: none required
- Expected runtime: focused CPU-only diagnostics and tests under a few minutes

Planned search scope:
- keep the current tiny deterministic fixture,
- compare a small ladder of `sparse_level` values,
- compare a small ladder of `observation_variance_floor` values,
- avoid broad parameter/horizon expansion in this pass.

## Baseline / comparator
Primary numerical comparator:
- `highdim.exact_transformed_sv_independent_panel_dense_reference(...)`
  on the same short-prefix fixture

Baseline for improvement judgment:
- the currently recorded precursor gaps from
  `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-next-step-result-2026-06-26.md`

Current baseline gaps to beat or materially tighten:
- log-likelihood gap: `0.23655605513577171`
- log-normalizer gap: `0.23655605513577171`
- mean-path gap: `0.5564179786156743`
- variance-path gap: `0.2618274684216835`

What is explicitly not the comparator:
- runner/leaderboard status,
- KSC surrogate routes,
- score routes,
- generic non-Gaussian SGQF behavior.

## Evidence contract
Engineering question:
- Is the current precursor loose because its current SGQF policy is obviously
  suboptimal, or because the route itself is inherently weak at this claim
  level?

Exact baseline:
- same exact-transformed dense reference on the same tiny short-prefix fixture

Primary promotion criterion:
- there is a materially improved setting of the current precursor that reduces
  the current gap profile while preserving finiteness and governance-clean
  target metadata.

Diagnostics that can veto:
- improvements are marginal and do not materially change the current gap scale,
- outputs become highly sensitive to `observation_variance_floor`,
- the best apparent setting only works by numerically unstable behavior,
- any implementation change muddies the target identity or non-claims.

Diagnostics that are explanatory only:
- whether `sparse_level` or `observation_variance_floor` matters more,
- runtime differences between tested settings.

What will not be concluded even if the pass succeeds:
- no same-target admission,
- no analytical score claim,
- no source-row promotion,
- no generic non-Gaussian SGQF core support.

Artifact that will preserve the result:
- a result note under `docs/plans/` recording before/after gaps and the chosen
  setting (or the decision to stop).

## Success criteria
Primary:
- identify either:
  1. a clearly better short-prefix precursor setting, or
  2. evidence that no small policy change materially improves the route.

Secondary:
- preserve all current p41/p43/source-scope contract tests,
- keep the route precursor-only in naming and diagnostics.

Sanity checks:
- no target-identity drift,
- no new score-path claim,
- no public narration suggesting source-row admission.

## Diagnostics
Primary:
- before/after `log_likelihood` gap
- before/after `log_normalizers` gap
- before/after `mean_path` gap
- before/after `variance_path` gap
- off-diagonal covariance leakage

Secondary:
- sensitivity of those metrics to `observation_variance_floor`
- sensitivity to `sparse_level`

## Expected failure modes
- `observation_variance_floor` dominates the route and makes the precursor too
  fragile to justify keeping alive;
- higher sparse levels do not improve the route materially;
- one metric improves while another worsens enough that the route is not really
  better overall.

## Pre-mortem
How the run could pass while misleading us:
- a small numerical improvement might look meaningful even though the precursor
  remains far too loose for any serious downstream use.

How the run could fail for tuning rather than conceptual reasons:
- the tested ladder may be too narrow or the chosen fixture may understate where
  one knob actually helps.

Cheap diagnostic to distinguish those explanations:
- compare whether the best setting improves several metrics together or only one
  while leaving the rest essentially unchanged.

## Skeptical audit
Wrong-baseline risk:
- do not compare the precursor only to its previous self; the exact-transformed
  dense reference remains the real comparator.

Proxy-promotion risk:
- a numerically improved precursor is still not a source-row admission route.

Artifact-answer mismatch risk:
- if the result note or tests start implying row promotion, the pass fails its
  governance objective even if the numeric gap shrinks.

Audit verdict:
- proceed with a small knob-only improvement pass, then decide whether to keep
  or stop the precursor route.

## Files likely to modify
Primary implementation:
- `bayesfilter/highdim/sv_mixture_cut4.py`

Primary tests:
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`

Likely result artifact:
- `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-precursor-improvement-result-2026-06-26.md`

## Execution order
1. Probe a small `sparse_level` and `observation_variance_floor` ladder on the
   current short-prefix tiny fixture.
2. Choose either the best materially improved setting or conclude that no small
   knob change helps enough.
3. Update implementation/tests only if a setting is clearly better.
4. Re-run focused compile and p41/p43/source-scope verification.
5. Record a result note with before/after metrics and a go/stop decision.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  bayesfilter/highdim/sv_mixture_cut4.py \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

## Interpretation rule
- If one small policy setting materially improves the precursor across multiple
  metrics, keep the precursor alive at the same claim class and record the
  improved setting.
- If improvements are marginal or unstable, stop improving this route and leave
  the row blocked.
- If improvement pressure starts forcing target-identity drift or score-claim
  creep, stop immediately and treat that as evidence against continuing this
  precursor line.
