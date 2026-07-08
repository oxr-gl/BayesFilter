# Neural OT Retained-Teacher Source-Faithful Closure Master Program

Date: 2026-06-27

## Status

`DRAFT_FOR_VISIBLE_REVIEW`

## Decision

Create a new source-faithfulness closure program for BayesFilter's retained-teacher neural-OT lane.

This program treats the existing 2026-06-18 first-pass retained-Sinkhorn work, the later batched annealed transfer branch, and the 2026-06-26 annealed learned-warmstart repair branch as **implementation history**, not as completed source-faithful closure evidence.

Historical files are not deleted. They remain auditably useful as:
- BayesFilter-native implementation lineage,
- local training/evaluation evidence,
- annealed-route repair lineage,
- and evidence of open source-faithfulness gaps.

They must not be used as evidence that BayesFilter has already completed a source-faithful Meta OT or UNOT implementation.

## Role Contract

The current BayesFilter worker is the visible supervisor and executor for this program.

All substantive implementation, source-audit, adapter-design, faithfulness-audit, and result steps must remain visible in this dialogue. Do not use hidden detached execution, background supervisors, or nested external coding loops as substitutes for phase artifacts.

## Program Files

- Gap note / governance reset anchor: `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithfulness-gap-note-2026-06-27.md`
- Master program: `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-closure-master-program-2026-06-27.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter reach a defensible source-faithful retained-teacher neural-OT implementation by porting or decomposing an official donor route first, then adapting it into BayesFilter only after source anchors, donor choice, and deviation boundaries are explicit? |
| Primary donor set | `Meta OT` and `UNOT`, as recorded in `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md`. |
| Primary pass criterion | A single donor route is selected, source-audited, minimally ported or faithfully decomposed, mapped into BayesFilter with explicit source anchors, and audited so every deviation is classified as `source_faithful`, `fixed_adaptation`, or `extension_or_invention`. |
| Veto diagnostics | No donor decision; no source repo audit; custom implementation started before donor decomposition; no explicit target-object parity table; no route classification between fixed-target Sinkhorn and annealed transport; unrecorded license or framework blocker; hybrid Meta OT / UNOT route created before separate donor audits; usefulness claims made before faithfulness closure. |
| Explanatory diagnostics | Runtime, local heldout metrics, low-budget wins, annealed warm-start timing, scalar smoke tests, partial checkpoint plumbing. These may explain behavior but cannot by themselves close the source-faithfulness gap. |
| Not concluded | No claim that the donor paper is wrong; no claim that BayesFilter should adopt a donor as production default; no posterior/HMC readiness claim; no claim that annealed LEDH adaptation is closed unless the program explicitly reaches that phase. |
| Required artifacts | Phase subplans/results, donor-source maps, repo/file anchors, deviation ledger, adapter design note, faithfulness audit result, and final closeout decision. |

## Port-First Governance Contract

### Default rule
If an official implementation exists for the primary target route, BayesFilter must first attempt the narrowest faithful port or executable source decomposition before building a new custom route.

### Exception rule
Custom-first implementation is allowed only with an explicit blocker artifact recording one or more of:
- un-runnable or unavailable upstream code,
- incompatible or unusable license,
- exact target-object mismatch that makes faithful transfer impossible,
- exact route mismatch that makes the donor route irrelevant,
- framework/runtime mismatch so severe that even a minimal faithful decomposition is not viable.

### Naming rule
Until this program passes, all work must be described as one of:
- `BayesFilter-native retained-teacher prototype`,
- `conceptually aligned retained-teacher route`,
- `fixed_adaptation`,
- `extension_or_invention`.

Do not use `source_faithful` without:
- paper anchors,
- donor repo anchors,
- BayesFilter counterpart anchors,
- and an explicit deviation table.

## Source-Support Anchors

| Source object | Local anchor | Current interpretation |
| --- | --- | --- |
| Donor availability | `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md` | Meta OT and UNOT both have official donor repos; availability alone was confirmed but not fitness. |
| Donor fit and adaptation burden | `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md` | Both donors are high-fit conceptually but carry framework, representation, and adaptation burden. |
| Earlier custom-first recommendation | `docs/plans/bayesfilter-neural-ot-implementation-handoff-memo-2026-06-18.md` | The earlier sequence explicitly recommended BayesFilter-native implementation first rather than direct port-first. |
| First trained local route | `docs/plans/bayesfilter-neural-ot-retained-teacher-first-pass-implementation-plan-2026-06-18.md` | The first implementation lane was local fixed-target retained Sinkhorn with a BayesFilter-owned latent target and verification gates. |
| Annealed transfer status | `docs/plans/batched-ledh-pfpf-ot-retained-teacher-gpu-transfer-plan-2026-06-18.md` | The later annealed LEDH branch began as transfer/plumbing with training marked `N/A`. |
| Current annealed repair boundary | `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-learned-warmstart-repair-master-program-2026-06-26.md` | The current annealed learned branch still requires target-object, teacher-data, checkpoint, correctness, and effectiveness closure. |
| Conceptual chapter route | `docs/chapters/ch32d_retained_teacher_neural_ot.tex` | The intended lane is retained-teacher neural OT: keep correction, learn solver-relevant latent state, do not replace the teacher. |

## Phase Index

| Phase | Name | Required output |
| --- | --- | --- |
| P0 | Governance Reset and Evidence Boundary | P0 result that classifies older notes/results as implementation history rather than source-faithful closure evidence |
| P1 | Donor Source Anchor Audit | P1 note mapping paper claims and official repo modules/functions for both Meta OT and UNOT |
| P2 | Primary Donor Decision | P2 decision result choosing one primary donor and explicitly deferring the other |
| P3 | Minimal Source-Faithful Port / Decomposition | P3 artifact showing the narrowest runnable donor mechanism and a donor-component map |
| P4 | BayesFilter Adapter Design | P4 note defining the TensorFlow/TFP BayesFilter adapter and the boundary between fixed adaptation vs extension |
| P5 | Faithfulness Audit | P5 obligation/deviation ledger classifying every implementation difference |
| P6 | Closeout and Extension Boundary | P6 result deciding whether source-faithful closure has passed and what extensions may now proceed |

## Phase Details

### P0 — Governance Reset and Evidence Boundary
**Purpose:** reset the claim boundary so current implementation lineage is not silently treated as source-faithful closure.

**Must do:**
- classify 2026-06-18 first-pass retained-Sinkhorn work as BayesFilter-native retained-teacher history,
- classify the annealed LEDH transfer branch as transfer/plumbing history,
- classify the 2026-06-26 repair branch as necessary repair lineage, not faithful closure,
- freeze the new port-first policy for this lane.

**Gate:**
No future neural-OT usefulness or faithfulness claim may cite older notes as source-faithful evidence until this reset is recorded.

### P1 — Donor Source Anchor Audit
**Purpose:** inspect both Meta OT and UNOT at the paper and repo level before any further custom design.

**Must answer for each donor:**
- what exact latent object is predicted,
- what teacher/corrective mechanism is retained,
- how training and inference are split,
- what modules/functions implement the core retained-teacher route,
- what parts are benchmark infrastructure versus core algorithm,
- what framework/runtime and license constraints exist.

**Gate:**
No donor may be treated as the primary source until paper and repo anchors are written down explicitly.

### P2 — Primary Donor Decision
**Purpose:** choose one donor route as the primary source-faithful target.

**Decision criteria:**
- closest match to retained-teacher neural-OT semantics,
- smallest adaptation burden consistent with fidelity,
- cleanest target-object mapping into BayesFilter,
- cleanest separation between core method and incidental benchmark scaffolding.

**Rule:**
Do not proceed with two donors at once. Pick one primary donor, defer the other.

### P3 — Minimal Source-Faithful Port / Decomposition
**Purpose:** port or faithfully decompose the narrowest runnable donor route before any new BayesFilter-specific redesign.

**Must include:**
- donor repo component map,
- minimal runnable or reconstructible retained-teacher path,
- explicit distinction between donor-core logic and donor-benchmark logic,
- initial parity note on predicted object, correction mechanism, and deployment object.

**Rule:**
Do not start a new custom latent-target or architecture redesign before this decomposition exists.

### P4 — BayesFilter Adapter Design
**Purpose:** only after donor locking, define the TensorFlow/TFP BayesFilter adapter.

**Must answer:**
- what exact donor object maps to BayesFilter's teacher/student object,
- what representation changes are fixed adaptation rather than invention,
- what route boundary applies (fixed-target retained Sinkhorn versus annealed transport),
- what code stays faithful and what becomes BayesFilter-specific.

**Rule:**
Any move from the donor's retained-teacher route into the annealed LEDH route must be explicitly classified as `fixed_adaptation` or `extension_or_invention`; it may not be smuggled in under a generic faithfulness claim.

### P5 — Faithfulness Audit
**Purpose:** decide whether the resulting BayesFilter route is actually source-faithful.

**Required audit table fields:**
- paper anchor,
- donor repo anchor,
- BayesFilter counterpart,
- same mathematical object?`
- same retained-correction semantics?`
- same deployment object?`
- deviation classification (`source_faithful`, `fixed_adaptation`, `extension_or_invention`),
- open risk / required follow-up.

**Gate:**
No `source_faithful` closeout without the full deviation ledger.

### P6 — Closeout and Extension Boundary
**Purpose:** decide what follows after the faithfulness audit.

**Possible outcomes:**
- `SOURCE_FAITHFUL_ROUTE_CLOSED`
- `FIXED_ADAPTATION_ROUTE_CLOSED_BUT_NOT_FULLY_SOURCE_FAITHFUL`
- `CUSTOM_EXTENSION_REQUIRED_SOURCE_FAITHFUL_CLOSURE_FAILED`

**Rule:**
Only after this phase may the program reopen:
- annealed LEDH extension work,
- custom latent redesign,
- or broader usefulness studies framed as post-faithfulness BayesFilter work.

## Required Classification Vocabulary

Every major artifact in this program must classify the current route as one of:
- `source_faithful`
- `fixed_adaptation`
- `extension_or_invention`
- `implementation_history_only`

This vocabulary is mandatory so that later notes cannot blur evidence categories.

## Pre-Mortem

How this program could look successful while still failing its real purpose:

1. **Source-anchor audit without actual donor decomposition**
   - Risk: we summarize papers and repos, then drift back into custom BayesFilter coding.
   - Control: P3 requires a donor component map and minimal runnable or reconstructible route before adapter design.

2. **Two-donor ambiguity persists**
   - Risk: we keep citing both Meta OT and UNOT and never choose a primary source.
   - Control: P2 requires one donor decision and one deferred donor.

3. **Annealed extension is treated as faithful by semantic drift**
   - Risk: the annealed branch inherits source-faithfulness language from fixed-target retained Sinkhorn work.
   - Control: P4 and P5 force route-boundary classification and deviation labels.

4. **Port-first becomes slogan only**
   - Risk: the documents endorse port-first but execution continues custom-first.
   - Control: custom-first is allowed only with an explicit blocker artifact.

5. **Frustration is turned into paper blame**
   - Risk: we overread current underperformance as evidence against the papers.
   - Control: evidence contract explicitly forbids concluding paper failure from incomplete source-faithfulness closure.

## Forbidden Moves

- Do not call the current annealed learned-warmstart branch source-faithful before donor audit and deviation classification pass.
- Do not start with a BayesFilter-specific redesign before P2 donor choice and P3 donor decomposition.
- Do not mix Meta OT and UNOT into a hybrid route before each has been source-audited separately.
- Do not use runtime gains, scalar smoke checks, or local heldout wins as proof of source-faithfulness.
- Do not let external donor benchmark scaffolding silently define the BayesFilter architecture without explicit classification.

## Verification

This program is complete only if it produces:
1. a governance reset that classifies prior work correctly,
2. a donor source-anchor audit for both Meta OT and UNOT,
3. a single primary donor decision,
4. a minimal donor port/decomposition artifact,
5. a BayesFilter adapter note,
6. a paper→repo→BayesFilter faithfulness audit table,
7. and a closeout decision that explicitly states whether source-faithful closure was achieved or not.

## Final Handoff Requirement

After this master program exists, no future retained-teacher neural-OT implementation work should proceed casually from the old assumption that BayesFilter-native custom implementation is the default. The default is now:
- donor repo exists -> port/decompose first,
- then adapt,
- then audit,
- then extend.
