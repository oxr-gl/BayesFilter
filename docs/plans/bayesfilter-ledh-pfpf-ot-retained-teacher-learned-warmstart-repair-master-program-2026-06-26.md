# Master repair program: learned retained-teacher annealed warm-start for LEDH-PFPF-OT

## Purpose
This master repair program exists because the current `learned` retained-teacher arm
for LEDH-PFPF-OT is not yet at a scientifically meaningful working stage.

The immediate problem is not only that the benchmark harness originally allowed a
random-model fallback. We have now fixed that API issue. The deeper problem is that
the end-to-end learned route is still incomplete:
- the exact annealed teacher object is not frozen tightly enough,
- a route-matched teacher-data pipeline is not yet established,
- no trusted trained checkpoint for the annealed route is wired into the benchmark,
- and the current learned arm is already non-promoted on corrected replay fidelity
  relative to the heuristic warm-start.

So this program is not a broad experiment ladder. It is a repair-to-working-state
program whose goal is to determine whether a genuinely trained retained-teacher
annealed warm-start model can become a valid and useful arm for the real LEDH-PFPF-OT
route.

## Governing question
Can we define, train, integrate, and validate a checkpoint-backed learned annealed
warm-start model that:
1. matches the exact batched streaming LEDH-PFPF-OT route,
2. preserves the retained-teacher transport semantics,
3. passes correctness qualification against the frozen cold baseline,
4. and then shows a meaningful effectiveness advantage over the current working
   heuristic warm-start?

## Current evidence baseline
The current state of evidence is:
- Phase 1 baseline passed on the exact 50k streaming route.
- Phase 2 visible correctness initially only partially passed because replay
  discrepancy was missing.
- After harness repair, Phase 2 now emits paired replay discrepancy.
- Under that stronger metric, the `heuristic` arm looks correctness-preserving enough
  to advance descriptively, while the `learned` arm is materially farther from the
  cold reference and is not yet promotable.
- The current `learned` arm in benchmarking has not yet been shown to load a real
  trained annealed-route checkpoint.

## Program boundary
This program is about the **learned retained-teacher annealed warm-start route only**.
It does not reopen:
- positive-feature kernels,
- low-rank couplings,
- direct learned maps,
- dynamic/operator re-architectures,
- or broad production-default promotion.

The `heuristic` warm-start should be treated as the current working retained-teacher
reference arm during this repair effort.

## Frozen external comparator
All correctness and effectiveness claims in this repair program are with respect to the
same frozen comparator:
- exact same-route cold / zero-init batched streaming LEDH-PFPF-OT baseline,
- same GPU device,
- same compiled/JIT mode,
- same precision mode,
- same seed schedule,
- same particle counts,
- same transport settings,
- same cost definition,
- same barycentric output semantics.

## Non-claims
Even if this repair program succeeds, it does **not** conclude:
- posterior correctness,
- HMC readiness,
- broad production/default readiness,
- teacher replacement,
- broad cross-model generalization,
- dense-Sinkhorn equivalence for semantic-changing later branches,
- or universal GPU speedup.

## Working diagnosis of blockers

### Blocker A — target object under-specified
The annealed route’s learned target is not frozen tightly enough. We need an explicit
statement of whether the student predicts the raw annealed warm-start state
`(a_y, b_x, a_x, b_y, valid_mask)` or a normalized/canonicalized equivalent.

### Blocker B — no route-matched teacher-data pipeline
The strongest existing retained-teacher data/eval stack is for the fixed-target
Sinkhorn teacher, not the annealed streaming LEDH route. That is not a safe silent
substitute.

### Blocker C — no trusted trained checkpoint integrated into the real harness
The harness now correctly requires a checkpoint for `learned` mode, but we still do
not have a known-good annealed-route checkpoint wired into it.

### Blocker D — current learned arm is already non-promoted on replay fidelity
The repaired Phase 2 metric shows the current learned arm is materially worse than the
heuristic arm on replay discrepancy and row residual.

### Blocker E — iteration cost on the real 50k rung is high
This means the program must use small cheap intermediate gates before spending too many
full 50k comparisons.

## Phase index

### Phase A — algorithm contract lock
**Purpose:** freeze exactly what the annealed student is supposed to learn.

**Questions to answer:**
- What exact warm-start state is predicted?
- Is normalization/canonicalization required?
- What parts of the state are auxiliary versus required at deployment?
- What exact invariant defines a correct retained-teacher prediction?

**Deliverables:**
- algorithm contract note,
- frozen target-object definition,
- frozen tolerance table.

**Gate A:**
No teacher-data generation or training proceeds until the target object and correctness
criterion are frozen.

### Phase B — annealed teacher-data pipeline
**Purpose:** generate reproducible teacher data from the actual batched streaming
annealed LEDH route.

**Requirements:**
- same route family as the benchmark,
- deterministic fixture and manifest support,
- train/validation/heldout split,
- route metadata,
- target-state export,
- replay-oriented labels or enough state to compute replay discrepancy.

**Deliverables:**
- teacher-data generation runner,
- dataset manifest,
- teacher-data artifact.

**Gate B:**
A sample audit must confirm that the teacher data genuinely come from the same route
family used by the benchmark harness.

### Phase C — checkpointed learned-mode hardening
**Purpose:** make the benchmark and related runners artifact-safe.

**Requirements:**
- `learned` mode requires checkpoint path,
- checkpoint path is recorded in output artifacts,
- checkpoint load success is recorded,
- debug/random-init mode is explicitly separate and cannot be confused with trained
  evaluation,
- route mismatch or missing checkpoint fails loudly.

**Deliverables:**
- benchmark API hardening,
- checkpoint manifest convention,
- artifact provenance fields.

**Gate C:**
No learned-arm result is admissible after this point unless its artifact records a real
checkpoint provenance.

### Phase D — minimal credible training
**Purpose:** produce one reproducible annealed warm-start checkpoint that is meaningful
enough to enter correctness qualification.

**Scope:**
- one architecture family,
- narrow hyperparameter range,
- route-matched teacher data,
- heldout evaluation during training.

**Primary criteria:**
- better than random-init clearly,
- finite and stable,
- heldout replay-sensitive metrics improve,
- no obvious route mismatch.

**Deliverables:**
- checkpoint v1,
- training result note,
- heldout summary.

**Gate D:**
Advance only if one checkpoint is clearly interpretable and better than the random stub.

### Phase E — correctness qualification on the real route
**Purpose:** rerun Phase 2 with the real checkpoint and decide whether the learned arm
is correctness-preserving enough to be a genuine retained-teacher candidate.

**Compared arms:**
- cold,
- heuristic,
- learned(checkpoint-backed).

**Primary correctness metrics:**
- paired replay RMSE,
- paired replay max-abs,
- row residual,
- column residual,
- finite-output flag,
- route metadata.

**Gate E:**
The learned arm must:
- preserve semantics,
- remain finite,
- and be not materially worse than heuristic on retained-teacher preservation metrics.

If it fails here, Phase F is blocked.

### Phase F — effectiveness qualification on the real route
**Purpose:** only after correctness passes, test whether the learned arm is actually
useful on the real 50k route.

**Primary metrics:**
- warm-call median time,
- correction burden,
- stability under repeated runs,
- comparison against both cold and heuristic.

**Gate F:**
The learned arm must preserve correctness **and** show a meaningful advantage over the
frozen comparator and a justified advantage versus heuristic.

If heuristic ties or wins, learned is not promoted.

### Phase G — repair branch
**Purpose:** if the learned arm fails correctness or effectiveness, diagnose and repair
in a bounded order.

**Repair order:**
1. target-object redesign,
2. normalization/canonicalization redesign,
3. teacher-data envelope repair,
4. loss redesign toward replay-preserving targets,
5. modest architecture widening.

**Rule:**
Do not start broad model-family search here.

### Phase H — closeout decision
**Purpose:** issue the final retained-teacher learned-route decision.

**Possible outcomes:**
- `PROMOTE_LEARNED_RETAINED_TEACHER`
- `KEEP_HEURISTIC_AS_WORKING_ROUTE`
- `PAUSE_LEARNED_ROUTE_PENDING_REDESIGN`

## Decision gates summary
- **Gate A:** target object frozen
- **Gate B:** route-matched teacher data exist
- **Gate C:** checkpoint-backed learned mode enforced
- **Gate D:** one minimal credible checkpoint exists
- **Gate E:** learned arm passes correctness qualification on the real route
- **Gate F:** learned arm passes effectiveness qualification on the real route
- **Gate H:** final route recommendation

## Artifact ladder
By the end of this program, the repo should contain:
1. algorithm contract note
2. teacher-data pipeline note + manifest
3. checkpoint manifest convention note
4. trained checkpoint v1 + metadata
5. training result note
6. revised Phase 2 correctness result
7. revised Phase 3 effectiveness result
8. optional repair-branch note if needed
9. final closeout decision memo

## Forbidden moves
- Do not benchmark a random model under the label `learned`.
- Do not train against the fixed-target Sinkhorn teacher and silently claim it covers
  the annealed streaming LEDH route.
- Do not promote runtime differences before correctness qualification passes.
- Do not interpret explanatory-only evidence as effectiveness.
- Do not broaden into positive-feature, low-rank, direct-map, or dynamic/operator
  alternatives inside this repair program.

## Verification checklist
- Does the trained checkpoint provenance exist and appear in the benchmark artifact?
- Does the teacher-data artifact come from the same route family as the benchmark?
- Does the learned arm beat the random stub on heldout replay-oriented metrics?
- Does the learned arm preserve correctness on the real route?
- Does it then beat or clearly justify itself versus heuristic?

## Skeptical audit
This repair master program passes the skeptical audit only if it is treated as a
repair-to-working-state program, not as a broad research expansion. The point is to
make the learned retained-teacher arm scientifically interpretable and operationally
fair before asking whether it is actually effective.
