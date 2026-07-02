# Reset memo: actual-transformed-sv-sgqf-planning-error-and-value-semantics-reset

## Date
2026-06-26

## Context
This pass began from the idea that the actual-transformed SV SGQF lane needed a
new augmented-noise-first precursor route and that, once that precursor existed,
we could evaluate whether it was good enough for tighter value evidence and then
for an eventual analytical-gradient admission stage.

That framing turned out to be wrong.

The key discovery is that the current augmented-noise SGQF route does not merely
have a “loose approximation” problem. It has a deeper **value-semantics
mismatch**:
- the route was wired through the Gaussian innovation-closure SGQF core,
- so the scalar value it computes is a Gaussian-closure surrogate objective,
- not the intended SGQF-style direct likelihood quadrature for the lane.

Therefore the recent precursor-promotion / precursor-improvement framing was a
major planning error. The right next question is not “how do we improve or score
this precursor?” but rather “how do we correct the SGQF value computation so it
matches the intended lane semantics?”

## Decision / policy
Future sessions should assume the following unless a new reviewed artifact says
otherwise:

1. **Classify the recent augmented-noise precursor effort as a major planning
   error.**
   The core issue is value semantics, not score readiness.

2. **Do not continue the old framing** of:
   - improving the current precursor as if it were a candidate admitted SGQF
     route,
   - or planning analytical-gradient admission on top of it.

3. **Treat the current actual-transformed augmented-noise route as a diagnostic
   artifact only.**
   It showed that a route can be wired and tested, but it does not define the
   right SGQF likelihood object for promotion.

4. **Restart from the value-semantics bug question.**
   The next correct decision is:
   - repair the SGQF core with a true non-Gaussian update branch, or
   - implement a dedicated direct-quadrature actual-SV value path.

5. **Do not restart analytical-gradient work** for this lane until the value
   semantics are corrected.

## What changed
- File: `bayesfilter/highdim/sv_mixture_cut4.py`
  - Added an actual-transformed augmented-noise SGQF precursor route.
  - In hindsight, this route is useful only as a diagnostic artifact because it
    currently routes through Gaussian innovation closure rather than the intended
    SGQF likelihood semantics.

- File: `bayesfilter/highdim/__init__.py`
  - Exported the new actual-transformed augmented-noise precursor route.

- File: `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
  - Added precursor tests and gap checks.
  - These tests remain useful as diagnostic evidence, but they should not be read
    as promotion evidence.

- File: `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-precursor-result-2026-06-26.md`
  - Recorded the internal exact-transformed SGQF precursor result.

- File: `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-broader-precursor-ladder-result-2026-06-26.md`
  - Recorded the broader internal exact-transformed precursor ladder result.

- File: `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-next-step-result-2026-06-26.md`
  - Recorded the augmented-noise precursor route result.
  - Future sessions should reinterpret this note as a diagnostic artifact showing
    the route exists but the value semantics are wrong for promotion.

- File: `docs/plans/bayesfilter-actual-transformed-sv-sgqf-value-semantics-bug-fix-plan-2026-06-26.md`
  - Wrote the corrective plan that reframes the issue as a value-semantics bug.

## Bugs / blockers resolved
- Symptom:
  - The discussion was drifting toward precursor improvement and analytical-score
    admission for the actual-transformed SGQF lane.

- Root cause:
  - We failed to notice early enough that the new augmented-noise route was still
    computing a Gaussian-closure surrogate objective through the SGQF core,
    rather than an SGQF direct likelihood approximation appropriate for the
    intended lane.

- Resolution:
  - Reclassified the issue as a **value-semantics bug** and wrote a corrective
    bug/fix plan.

## Verification already run
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  bayesfilter/highdim/sv_mixture_cut4.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

Observed:
- the current precursor route and surrounding tests pass as code,
- but passing tests did not answer the right question,
- because the implemented scalar value is still the wrong SGQF object for
  promotion.

## Current policy
- Treat the current actual-transformed augmented-noise SGQF route as a
  diagnostic-only artifact.
- Treat all recent “precursor improvement” or “analytical-gradient readiness”
  framing for this lane as superseded.
- Restart from the value-semantics bug-fix plan before any further work on this
  family.

## Known limitations / cautions
- The new route is present in the codebase and exported, but its semantics are
  not the intended final SGQF semantics for this lane.
- The recent result notes are still useful, but only as diagnostics / negative
  evidence; they are not promotion evidence.
- The recent session accumulated a lot of local framing around precursor quality
  and score readiness; a fresh session is recommended to avoid carrying that
  premise forward.

## Suggested next steps
1. Start a **fresh session** from this reset memo and the corrective bug/fix
   plan:
   - `docs/plans/bayesfilter-actual-transformed-sv-sgqf-value-semantics-bug-fix-plan-2026-06-26.md`
2. In that fresh session, begin by writing down the exact scalar value the
   current route computes and the scalar value the SGQF lane is supposed to
   compute.
3. Choose the repair path:
   - true non-Gaussian SGQF core update branch, or
   - dedicated direct-quadrature actual-SV value path.
4. Do not resume analytical-gradient work for this lane until the value
   semantics are corrected.
