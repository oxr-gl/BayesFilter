# Neural OT Implementation Handoff Memo

## Date
2026-06-18

## Purpose

This memo is for the next fresh implementation session.  The literature/survey
phase is complete enough to stop carrying the full survey-editing context.  The
next agent should treat this note as the action-oriented handoff for starting the
first BayesFilter implementation pass.

## Read first

Before doing any implementation work, read these in order:

1. `docs/plans/bayesfilter-neural-ot-survey-closeout-reset-memo-2026-06-18.md`
2. `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md`
3. `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md`
4. The implementation-bearing OT block chapters:
   - `docs/chapters/ch32a_soft_differentiable_resampling.tex`
   - `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`
   - `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
   - `docs/chapters/ch32d_retained_teacher_neural_ot.tex`

Only after the retained-teacher route is scoped should the broader comparison
chapters be reopened:
- `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
- `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`

## Working assumptions

Future implementation work should assume the following unless the user explicitly
changes direction:

- The OT/neural-OT survey phase is closed.
- The six-chapter OT/neural-OT block is the current mathematical reference.
- The **implementation-bearing core** is:
  1. soft differentiable resampling,
  2. deterministic OT equal-weighting,
  3. entropic OT / Sinkhorn plus barycentric projection,
  4. retained-teacher warm-started neural acceleration.
- The **first implementation route** is the retained-teacher neural OT lane,
  not direct-map ICNN/Brenier and not dynamic/operator OT.
- The initial external code-backed candidates are:
  - `Meta OT` — `https://github.com/facebookresearch/meta-ot`
  - `UNOT` — `https://github.com/GregorKornhardt/UNOT`
- Direct-map (`OT-ICNN`) and dynamic-flow/operator repos are secondary branches
  unless the user explicitly asks for them or the retained-teacher route proves
  unsuitable.

## Immediate technical target

The target algorithm to implement first is:

> retained entropic OT / Sinkhorn teacher + learned warm start or dual predictor
> + corrective Sinkhorn refinement still kept in the loop.

In the monograph’s current notation, this means the implementation should stay as
close as possible to the teacher/student story in:
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
- `docs/chapters/ch32d_retained_teacher_neural_ot.tex`

Concretely, the next agent should assume:
- the teacher is the retained finite EOT/Sinkhorn layer,
- the student predicts a solver-relevant latent quantity,
- the corrective Sinkhorn phase is not optional in the first pass,
- downstream scalar checks are part of the implementation scope from the start.

## First implementation questions to answer

The first implementation session should answer these in order:

1. **What exact latent teacher object should BayesFilter predict?**
   Candidate choices include:
   - dual potentials,
   - scaling vectors,
   - or another solver-internal initialization object.

2. **Is `Meta OT` or `UNOT` the closer conceptual match?**
   - `Meta OT` is strongest as an amortized-solver / warm-start framing.
   - `UNOT` is strongest as a discrete entropic OT dual-potential predictor.

3. **What is the smallest BayesFilter teacher-data generation loop?**
   - generate weighted particle clouds,
   - build the cost matrix,
   - solve the retained Sinkhorn teacher,
   - extract the latent target for the student,
   - record the barycentric teacher output and residuals.

4. **What does the first TensorFlow / TFP interface look like?**
   The implementation should define the minimal callable objects clearly before any
   training run begins.

## Strong recommendation for the first implementation pass

Do **not** start by cloning or porting everything.  Start with a narrow,
BayesFilter-native implementation plan.

### Phase 1: target-object extraction
Use the implementation-fit note and the external repos only to answer:
- what object does the paper code actually predict?
- is that object the same as what the BayesFilter chapter wants to predict?
- what parts are teacher generation, what parts are student inference, and what
  parts are optional benchmark infrastructure?

### Phase 2: BayesFilter-native teacher prototype
Implement a minimal local teacher pipeline first:
- weighted cloud in,
- cost matrix,
- retained Sinkhorn solve,
- barycentric teacher output,
- residual reporting.

This should happen before any neural training code is introduced.

### Phase 3: student prototype
Only after the teacher is stable:
- choose the latent object to predict,
- define the student input representation,
- define the training loss,
- implement corrective refinement,
- compare student-plus-correction against the teacher.

## What not to do first

The next agent should explicitly avoid these temptations in the first session:

- Do not start with direct-map ICNN/Brenier implementation.
- Do not start with dynamic-path/geodesic/operator-learning implementation.
- Do not start by generalizing across many OT families at once.
- Do not let benchmark/reproduction code from external repos become the first
  architecture of the BayesFilter implementation.
- Do not remove the corrective Sinkhorn phase in the first pass.
- Do not treat runtime improvement alone as success.

## Minimal success criterion for the first implementation session

A successful first implementation session should end with:

1. a documented choice of **predicted latent object**,
2. a BayesFilter-native **teacher-data generation path**,
3. a clear decision whether `Meta OT` or `UNOT` is the closer match,
4. a concrete implementation plan under `docs/plans/` for the retained-teacher
   route,
5. and ideally a stubbed or minimal code path for the teacher layer.

## Human-facing caution

The survey and monograph work already encode the right conceptual warning:
this is not “replace OT with a neural net.”  It is “retain the declared OT teacher
and learn how to accelerate it.”  The next implementation session should preserve
that discipline.

## Suggested next step

Write a new implementation plan note that answers:
- which latent object BayesFilter will predict,
- why that choice matches either `Meta OT` or `UNOT`,
- what files will implement the teacher and student pieces,
- how the corrective refinement will be preserved,
- what minimal checks will decide whether the first implementation is faithful to
  the intended chapter definition.
