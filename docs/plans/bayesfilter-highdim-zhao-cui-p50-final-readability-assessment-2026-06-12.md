# P50 Final Readability Assessment

**Target:** `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`

Reading p50 as a mathematically literate academic from a neighboring field, I
would say that it is the strongest Zhao--Cui companion version so far.  It is now
much easier to follow than p30, and it is visibly more chapter-like than p48 or
p49.  The main gains are that the opening is lighter, the chapter purposes are
clearer, and the fixed-branch chapters no longer feel as purely ledger-driven.
However, it still does not fully read like a settled monograph chapter sequence.
The remaining weakness is now one of **selective pressure inside the middle
chapters** rather than overall architecture.

## What improved in p50

### 1. The opening now feels more like a chapter opening
The opening no longer begins by foregrounding the object ledger as its first
rhetorical move.  It now tells the reader what problem is being studied, what
object is being chosen, and why that object matters before returning to later
technical distinctions.  This is a real monograph gain.

### 2. The chapter purposes are clearer
The note now does a better job of letting each chapter answer one dominant
question:
- what is the exact target,
- what is the TT approximation family,
- why are multiple coordinate systems needed,
- what is the fixed-branch scalar,
- what is actually differentiated,
- what evidence would make the lane credible.

This is not perfect yet, but it is much clearer than in p30 or even p48.

### 3. The implementation-facing material is better motivated
The fixed-branch likelihood chapter now more clearly signals why the details
matter.  It is less of a bare inventory and more of a chapter about runtime object
identity, scalar identity, and where an implementation silently redefines the
mathematics.

### 4. The derivative chapter feels more cumulative
The derivative warmups are still long, but they now read more clearly as a ladder
of ideas that feed the fixed-branch derivative rather than as detached side notes.

## What still feels weak

### 1. The running-example chapter is still too busy for its location
The opening improvement helps, but the running-example-and-notation chapter still
has too much to do.  It remains a mixture of:
- source/literature framing,
- notation burden,
- threaded example setup,
- early density-transform logic.
A neighboring-field reader can follow it, but it still feels more crowded than a
chapter this early in the note ideally should.

### 2. The TT toolkit chapter still has one theme too many
The chapter is now better framed, but it still tries to teach:
- what TT form is,
- what rank means,
- why moderate rank is plausible,
- how the exponential example works,
- how least-squares row construction works.
All of this belongs in the note, but it still creates a chapter that is slightly
broader than one calm toolkit chapter wants to be.

### 3. The coordinate / KR / preconditioning chapter remains the hardest stretch
This chapter still asks the reader to hold too many interacting ideas in one long
pass.  The reorganization helped, but it still feels like a difficult tunnel.
That is probably the least natural middle movement of the current note.

### 4. The fixed-branch likelihood chapter is good, but could still spotlight
subtlety more sharply
The chapter is much better than before, yet it still occasionally tells me what is
stored without always emphasizing which detail is mathematically decisive and why.
It is now interesting, but not always maximally pointed.

### 5. The derivative chapter is still large
It is now more coherent, but still big enough that it risks reading like a very
carefully organized derivative dossier rather than a chapter with one calm
center.  The propositions, warmups, teaching layer, and checklists all make sense,
but the chapter still asks a lot of the reader.

## Overall judgment

P50 is now the first Zhao--Cui companion version that I would describe as
**reasonably chapter-like** rather than merely reorganized.  It is not yet fully
polished monograph prose, but it is clearly closer to that standard than the
previous versions.  The main remaining work is now not structural and not even
primarily chapter-level.  It is local selectivity and pressure inside the middle
chapters, especially:
- running example / notation,
- TT toolkit,
- coordinate systems and preconditioning,
- and the derivative chapter.

## Recommendation

If another pass is taken after p50, it should be a **middle-chapter pressure
pass**, not another whole-document redesign.  The main tasks would be:
1. lighten the early running-example chapter,
2. sharpen the TT toolkit to one slightly more singular payoff,
3. shorten or further stage the coordinate/preconditioning tunnel,
4. increase emphasis on the mathematically decisive details in the fixed-branch
   chapter,
5. reduce the derivative chapter’s perceived size without deleting its strongest
   content.
