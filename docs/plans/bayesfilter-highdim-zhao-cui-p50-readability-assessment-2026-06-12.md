# P50 Readability Assessment

**Target:** `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`

Reading p50 as a mathematically literate academic from a neighboring field, I
would say the document is now meaningfully better than p49, but it still has not
fully crossed the line into a natural monograph chapter.  The main difference is
that p50 has stronger chapter-level signaling and better concentration of themes.
The opening no longer begins as abruptly with technical object inventory, and the
later chapters do a somewhat better job of telling the reader what they are for.
However, the text still retains too much of the explanatory density and local
self-justification of its origin as an internal technical note.

## What improved in p50

1. **The opening voice is stronger.**
   The opening now foregrounds the scientific problem, the computational object,
   and the chapter’s main task before turning to detailed object bookkeeping.
   This is a substantial gain over p48.

2. **The implementation chapter is more intelligible as a chapter.**
   The fixed-branch and implementation-facing material now better signals that the
   real issue is object identity: what is stored, what changes the scalar, and
   what conventions silently redefine the mathematical target.

3. **The chapter hierarchy is easier to infer.**
   A reader can now more clearly distinguish among:
   - the approximation family,
   - the coordinate/transport machinery,
   - the fixed-branch scalar,
   - the derivative chapter,
   - the validation chapter,
   - and the final positioning chapter.

4. **The conclusion feels less like a restart.**
   It synthesizes somewhat better rather than re-arguing the existence of the lane
   from the beginning.

## What still feels weak

### 1. The opening still has too much technical density too early
Even though the voice is better, the opening still moves rather quickly into
formal object distinctions.  A neighboring-field reader now understands the
purpose sooner, but the prose still feels eager to define everything before the
reader has fully settled into the chapter.

### 2. “Running Example And Notation” is still overburdened
The running example is useful, but the notation and reference material around it
are still dense.  The section still tries to do too much:
- literature anchoring,
- symbol setup,
- example setup,
- and density-transform notation.
The result is more coherent than p49, but still somewhat heavy for a chapter this
early in the note.

### 3. The TT toolkit chapter still lacks a single dominant payoff
The chapter is conceptually rich, but it still reads as if it has several
coequal aims:
- explaining TT form,
- explaining rank,
- motivating rank plausibility,
- showing a worked exponential example,
- and explaining marginalization.
All are worthwhile, but the chapter still feels more like a well-curated toolbox
than like one sharply focused chapter.

### 4. The coordinate/preconditioning chapter is still long and effortful
This chapter is now more justified, but it remains rhetorically heavy.  It asks
the reader to digest several sophisticated transform ideas in one sustained
stretch.  The mathematics is coherent, but the pacing still feels like a long
technical climb.

### 5. The derivative chapter is still too large for a single calm arc
The derivative chapter is better motivated than before, but it remains internally
very large: motivation, warmups, teaching layer, forward pass, derivative pass,
propositions, caveats, and checklists all coexist.  The reader can now see why
these materials belong together, but the chapter still has more internal load than
a finished monograph chapter would usually tolerate.

## Main diagnosis

P50 has improved from “reorganized note” to “chapter-shaped technical draft,” but
its remaining weakness is now one of **chapter interior compression of purpose**.
The large-scale order is mostly right.  The remaining problem is that several
chapters still try to achieve too many local objectives at once.

## Recommendation

The next pass should not perform another large structural change.  It should
instead aim for:
1. lighter early notation burden,
2. a more singular TT-toolkit payoff,
3. a slightly shorter and more selective coordinate/preconditioning chapter,
4. a derivative chapter that chooses one clearer internal spine and subordinates
   the rest.

In short: p50 now feels like a serious draft of a monograph chapter sequence.  It
is closer than p49.  The next improvement should come not from new material or new
reordering, but from stronger selectivity within the existing chapter interiors.
