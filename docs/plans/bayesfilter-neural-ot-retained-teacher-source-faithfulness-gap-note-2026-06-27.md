# Neural OT Retained-Teacher Source-Faithfulness Gap Note

Date: 2026-06-27

## Status

`CURRENT_BRANCH_NOT_YET_SOURCE_FAITHFUL_PORT_FIRST_POLICY_REQUIRED`

## Decision

BayesFilter's current neural-OT retained-teacher branch is **implementation-bearing but not yet source-faithful** to a named external retained-teacher implementation route.

Historical neural-OT notes and results remain useful as:
- evidence of BayesFilter-native exploration,
- evidence of local training / evaluation behavior,
- evidence of annealed-route integration and repair work,
- evidence that the retained-teacher idea is not yet operationally closed.

They must **not** be cited as evidence that BayesFilter has already completed a source-faithful Meta OT or UNOT implementation.

Going forward, when an official reference implementation exists for the primary target route, **port-first** is the default policy. Custom-first implementation becomes the exception path and requires an explicit blocker note.

## Question

What source-faithfulness gaps remain in the retained-teacher neural-OT lane, why did BayesFilter not port the official reference implementations first, and what policy should govern future work so that a faithful implementation is reached before more custom neural-OT invention proceeds?

## Scope

This note is limited to the retained-teacher neural-OT lane:
- fixed-target retained Sinkhorn first-pass work,
- later batched annealed LEDH transfer / learned warm-start repair work,
- primary external donors `Meta OT` and `UNOT`.

Out of scope:
- direct-map ICNN/Brenier routes,
- dynamic/path/operator-learning routes,
- broad repo-wide source-governance policy outside this lane,
- claims that the external papers themselves are wrong.

## Executive Verdict

### What is true now
1. Official code-backed references **do exist** for the main retained-teacher candidates:
   - `Meta OT` — `https://github.com/facebookresearch/meta-ot`
   - `UNOT` — `https://github.com/GregorKornhardt/UNOT`
   Source: `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md`.

2. BayesFilter's first implementation path was deliberately **BayesFilter-native first**, not direct-port first.
   Source: `docs/plans/bayesfilter-neural-ot-implementation-handoff-memo-2026-06-18.md`.

3. The first trained / evaluated implementation lane was the **local fixed-target retained Sinkhorn route**, not the annealed streaming LEDH route.
   Source: `docs/plans/bayesfilter-neural-ot-retained-teacher-first-pass-implementation-plan-2026-06-18.md`.

4. The later annealed LEDH learned-warmstart branch was initially a **transfer / plumbing branch**, not a faithful route-matched trained implementation.
   Source: `docs/plans/batched-ledh-pfpf-ot-retained-teacher-gpu-transfer-plan-2026-06-18.md`.

5. The annealed branch still required a repair program to freeze the target object, teacher-data contract, and checkpoint provenance before it could even be judged fairly.
   Source: `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-learned-warmstart-repair-master-program-2026-06-26.md` and its Phase A/B/C subplans.

### What is not justified now
- It is **not** justified to say the current branch is source-faithful to Meta OT or UNOT.
- It is **not** justified to say the papers are the problem.
- It is **not** justified to continue treating custom-first as the default when official donor repos exist.

## Source-Support Anchors

| Source object | Local anchor | Current interpretation |
| --- | --- | --- |
| Official donor-repo availability | `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md` | Official repos exist for Meta OT and UNOT; availability was confirmed, but fitness was not fully cleared. |
| Conceptual donor fit and adaptation burden | `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md` | Meta OT and UNOT are high-fit conceptual donors, but adaptation burden, framework mismatch, and exact object fit remained unresolved. |
| First implementation sequencing choice | `docs/plans/bayesfilter-neural-ot-implementation-handoff-memo-2026-06-18.md` | The repo explicitly chose a narrow BayesFilter-native first pass instead of cloning or porting everything. |
| First trained retained-teacher lane | `docs/plans/bayesfilter-neural-ot-retained-teacher-first-pass-implementation-plan-2026-06-18.md` | The first implementation lane was fixed-target retained Sinkhorn, with BayesFilter-defined latent object and verification gates. |
| Annealed transfer branch status | `docs/plans/batched-ledh-pfpf-ot-retained-teacher-gpu-transfer-plan-2026-06-18.md` | The batched annealed LEDH branch was a transfer/speed-test pass with training marked `N/A`; it already acknowledged latent-object mismatch vs the Sinkhorn lane. |
| Annealed learned-branch repair status | `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-learned-warmstart-repair-master-program-2026-06-26.md` | The current annealed learned branch still needed target-object lock, route-matched teacher data, checkpoint hardening, and correctness/effectiveness reruns. |
| Intended conceptual route in the monograph | `docs/chapters/ch32d_retained_teacher_neural_ot.tex` | The intended route is retained-teacher warm-starting: keep the teacher solve, learn solver-relevant latent state, and preserve corrective refinement. |

## Reference Implementations: What Exists

The repo's own source-code ledger records:
- `Meta OT` as `OFFICIAL_REPO_CONFIRMED` and the closest code-backed route for retained-teacher warm-started acceleration of entropic OT solves.
- `UNOT` as `OFFICIAL_REPO_CONFIRMED` and a strong code-backed route for predicting dual potentials / Sinkhorn initialization across discrete OT problems.

This means BayesFilter cannot justify a custom-first path on the basis that no usable upstream donor code exists.

## Why the Current Branch Is Not Yet Source-Faithful

### 1. BayesFilter chose a BayesFilter-native first implementation lane
The implementation handoff memo explicitly said:
- do **not** start by cloning or porting everything,
- first build a narrow BayesFilter-native teacher pipeline,
- then only later define the student path.

That choice may have been pragmatic, but it means the first branch was not organized as a source-faithful donor implementation from the beginning.

### 2. The first trained route was fixed-target retained Sinkhorn, not the later annealed route
The first-pass retained-teacher plan:
- hard-scoped the first implementation to TensorFlow / TensorFlow Probability,
- attached to the current fixed-target finite Sinkhorn equal-weighting lane,
- excluded the annealed-transport lane from the first pass,
- chose a BayesFilter-defined latent target `(log_u, log_v)` under a local gauge convention.

That is a BayesFilter-owned retained-teacher route. It is not yet a paper+repo faithful implementation proof for Meta OT or UNOT.

### 3. The annealed LEDH branch began as a transfer/plumbing branch, not a faithful training branch
The batched LEDH transfer plan explicitly said:
- the goal was transfer into the actual batched annealed transport path,
- training steps were `N/A` in the first transfer pass,
- warm-start modes were `none`, `heuristic`, or static learned initializer shape only,
- the batched path uses annealed potentials rather than the fixed-target Sinkhorn latent.

So the later branch inherited a route/object mismatch before a source-faithful donor route had been locked.

### 4. The current annealed learned branch still required repair before fair evaluation
The learned warm-start repair program identifies the main blockers as:
- target object under-specified,
- no route-matched teacher-data pipeline,
- no trusted trained checkpoint integrated into the real harness,
- learned arm already non-promoted on replay fidelity,
- high real-route iteration cost.

A branch that still needs those repairs is not yet source-faithful closure.

## Why We Did Not Port the Reference Implementations First

The earlier BayesFilter notes give real reasons. They should be recorded fairly.

### Explicitly recorded reasons
1. **Framework mismatch**
   - Meta OT is described as JAX-based research code.
   - UNOT also carries non-BayesFilter framework/runtime assumptions.
   - BayesFilter's first pass was intentionally TensorFlow / TFP only.

2. **Object mismatch**
   - The repo had not yet frozen what exact latent object BayesFilter should predict.
   - The fit note treats target-object extraction as an unresolved task.
   - The first pass therefore chose a BayesFilter-native latent teacher object rather than first proving parity to a donor implementation object.

3. **Route mismatch**
   - The first learned route was fixed-target retained Sinkhorn.
   - The later production-facing transfer target was annealed LEDH streaming transport.
   - Even inside BayesFilter, those routes do not share the same latent state.

4. **Source-fit questions remained unresolved**
   The source-code ledger and fit note explicitly say availability does **not** establish:
   - license compatibility,
   - maintenance state,
   - exact paper-version match,
   - ease of running today,
   - exact mathematical fit for BayesFilter,
   - or whether code should be ported versus clean-room reimplemented.

### Why those reasons are insufficient now
These reasons explain why a direct port was deferred.

They do **not** justify:
- calling the current branch source-faithful,
- continuing to treat custom-first as the default,
- or hybridizing BayesFilter-native design decisions with paper-level success claims before a donor route has been audited and decomposed.

## Why BayesFilter Did Its Own Implementation

The repo's documented logic was:
- control the teacher object locally,
- preserve the retained-teacher semantics inside BayesFilter,
- avoid inheriting unrelated benchmark infrastructure from research repos,
- keep the first pass narrow and executable in the project's native TensorFlow / TFP stack,
- avoid direct-map or dynamic-path routes before the retained-teacher route was well specified.

That logic is understandable.

But it had a cost:
- BayesFilter spent substantial time inventing local interfaces, local latent targets, local teacher-data routines, and later a separate annealed transfer branch **before** a faithful donor decomposition had been completed.

The result is implementation history, but not yet a source-faithful closure artifact.

## Faithfulness Gap Ledger

| Gap | Evidence | Why it matters | Required closure action |
| --- | --- | --- | --- |
| No primary donor route locked | Meta OT and UNOT both remained high-fit donors in notes | Without one chosen donor, “faithful” has no concrete target | Force a primary donor decision before further custom route work |
| No donor repo decomposition before custom implementation | Handoff memo recommended BayesFilter-native first | BayesFilter built its own route before proving source parity | Perform minimal donor decomposition / port-first audit |
| BayesFilter-defined latent object chosen before donor parity | First-pass plan chooses local gauge-fixed `(log_u, log_v)` | Prevents a direct claim that the student predicts the same object as donor code | Produce a paper→repo→BayesFilter target-object mapping |
| First learned route scoped to fixed-target Sinkhorn only | First-pass plan excludes annealed transport | Later annealed conclusions cannot inherit faithfulness from the first pass | Audit fixed-target and annealed routes separately |
| Annealed transfer began before route-matched training closure | Transfer plan marks training as `N/A` | Means the production-facing learned branch started as plumbing, not faithful training | Complete source-faithful donor route before annealed extension |
| Route-matched annealed teacher-data not yet closed | 2026-06-26 repair program Phase B | Learned-route evaluation remains under-specified | Build route-matched teacher-data pipeline |
| Trusted checkpoint lineage not yet closed until repair work | 2026-06-26 repair program Phase C | Learned results were too easy to misread | Keep fail-closed checkpoint/dataset provenance discipline |
| No paper+repo+BayesFilter obligation table yet | No current artifact performs this full mapping | Prevents precise deviation classification | Add a source-faithfulness audit phase |

## What Must Not Be Concluded

1. Do **not** conclude that Meta OT or UNOT are the problem.
2. Do **not** conclude that BayesFilter has already produced a faithful retained-teacher neural-OT implementation.
3. Do **not** conclude that the annealed learned route has failed on paper-level grounds.
4. Do **not** cite the current branch as paper-faithful evidence until a donor route, source decomposition, and faithfulness audit have passed.
5. Do **not** let future custom neural-OT work proceed as if port-first were optional when official code exists.

## Port-First Policy Going Forward

### Default rule
When an official implementation exists for the primary method family BayesFilter wants to use, the default order is:
1. inspect the paper,
2. inspect the official repo,
3. decompose or port the narrowest faithful route first,
4. only then decide what BayesFilter-specific adaptation is required,
5. only after that allow custom extension or invention.

### Exception rule
Custom-first implementation is allowed only with an explicit blocker artifact that records at least one of:
- un-runnable or unavailable upstream code,
- incompatible or unusable license,
- exact object mismatch that prevents faithful transfer,
- exact route mismatch that makes the donor route irrelevant to the target lane,
- framework/runtime mismatch so severe that even a minimal decomposition is not viable.

### Required terminology
Until a source-faithful program passes, describe work as one of:
- `BayesFilter-native retained-teacher prototype`,
- `conceptually aligned retained-teacher route`,
- `fixed adaptation`,
- `extension_or_invention`.

Reserve `source_faithful` for work that is anchored to:
- paper sections/equations,
- donor repo modules/functions,
- BayesFilter implementation counterparts,
- and an explicit deviation ledger.

## Immediate Next Action

Start a new source-faithful closure program that:
- picks one primary donor route,
- performs source-anchor audit and minimal port/decomposition first,
- blocks further custom neural-OT invention until donor parity is mapped,
- and only then reopens BayesFilter-specific adaptation and the annealed LEDH extension path.

That program is defined in:
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-closure-master-program-2026-06-27.md`
