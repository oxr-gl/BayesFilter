# Master program: LEDH-PFPF-OT retained-teacher neural OT effectiveness

## Purpose
This master program turns the retained-teacher neural OT effectiveness question for
LEDH-PFPF-OT into a phased sequence. The question is narrow and fixed:

> can retained-teacher neural warm starts improve the real LEDH-PFPF-OT route
> without changing its transport semantics?

This is **not** a broad neural-OT competition. The master program is designed to
separate:
- exact-route correctness,
- teacher-preserving warm-start effectiveness,
- explanatory-only precision/runtime extensions,
- and later semantic-changing branches.

## Current evidence baseline
The repo already fixes the current direction strongly enough to support a phased
program:
- the reference transport object is finite entropic OT / Sinkhorn with barycentric
  equal-weight output,
- the default production direction is GPU-oriented LEDH-PFPF-OT TF32 in
  TensorFlow/TFP,
- retained-teacher neural OT is the primary implementation-bearing neural route,
- existing retained-teacher evidence is strongest in narrow / low-budget heldout
  settings,
- semantic-changing scalable-OT routes already exist as separate audited families and
  should not be merged into the primary retained-teacher claim.

## Frozen whole-program evidence contract

### Exact baseline
The baseline for all promotable phases is the exact same-route cold / zero-init
batched streaming LEDH-PFPF-OT lane under:
- same GPU device,
- same JIT/compiled mode,
- same precision mode,
- same seeds,
- same particle counts,
- same transport settings,
- same cost definition,
- same barycentric output rule.

This is the retained entropic reference lane.

### Primary effectiveness criterion
At fixed corrective budget on the real LEDH-PFPF-OT path, a warm-started route must:
- preserve the declared residual/constraint contract,
- preserve teacher-object and barycentric-output semantics,
- and improve the primary runtime or correction-burden metric relative to the frozen
  cold baseline.

### Primary correctness criterion
Before any runtime gain is promotable, the warm-started route must show:
- finite outputs,
- residual parity,
- no teacher/object drift,
- no hidden route change,
- trusted requested device execution,
- same declared transport path and output semantics.

### Veto diagnostics
- non-finite outputs,
- fallback off requested GPU/JIT path,
- route mismatch,
- teacher/object drift,
- residual failure,
- unfair warm-start vs baseline budget mismatch,
- runtime gain without fidelity parity.

### Explanatory-only diagnostics
- compile + first-call time,
- mean/min/max timing,
- memory before/after,
- latent/state prediction loss,
- gradient norms,
- iteration counts without parity,
- TF32 descriptive timing,
- smaller pilot counts.

### Non-claims
Even if the primary effectiveness rung passes, this program does **not** conclude:
- posterior correctness,
- HMC readiness,
- production/default readiness,
- teacher replacement,
- broad cross-model generalization,
- dense-Sinkhorn equivalence for later approximate routes,
- universal GPU speedup.

## Candidate set
Primary candidate set only:
- `cold` / `zero-init`
- `heuristic`
- `learned`
- optionally `learned_base` / `learned_wide` if already supported and cheap to run

Deferred to separate branch plans only:
- positive-feature kernels,
- low-rank couplings,
- direct learned maps,
- dynamic/operator methods.

## Forbidden moves
- Do not compare warm-start and baseline under different corrective budgets.
- Do not silently change transport route, cost, or barycentric output semantics.
- Do not promote explanatory-only timing or precision deltas as main evidence.
- Do not import semantic-changing routes into the retained-teacher claim set.
- Do not let TF32 descriptive evidence become a promotion criterion without a separate
  precision contract.

## Phase index

### Phase 0 — contract lock and skeptical audit
**Purpose:** freeze comparator, semantics, candidate set, precision policy, and
non-claims before performance interpretation begins.

**Inputs:**
- this master program,
- the retained-teacher effectiveness plan,
- current transport-route and precision policy docs.

**Must pass:**
- exact baseline definition frozen,
- candidate set frozen,
- same-route constraint frozen,
- veto diagnostics frozen,
- semantic-changing comparators explicitly deferred.

**Output artifact:**
- this master program itself,
- optional short checklist note if execution planning needs explicit sign-off.

### Phase 1 — exact-route baseline rung
**Purpose:** run only the cold / zero-init exact LEDH-PFPF-OT reference lane and
establish trusted baseline telemetry.

**Key checks:**
- finite outputs,
- trusted requested device evidence,
- memory-growth ordering,
- route metadata,
- residual contract,
- same barycentric semantics.

**Interpretation:**
- no promotion claim here,
- this phase only certifies the reference rung used later.

**Output artifact:**
- baseline result note with runtime, residual, device, precision, and shape metadata.

### Phase 2 — warm-start correctness rung
**Purpose:** compare `cold`, `heuristic`, and `learned` only on correctness-preservation
before discussing effectiveness.

**Key checks:**
- teacher-preservation discrepancy within envelope,
- residual parity,
- no route drift,
- no non-finite outputs,
- same output semantics.

**Advancement rule:**
- Phase 3 cannot be interpreted as a success if Phase 2 fails.

**Output artifact:**
- correctness rung result note.

### Phase 3 — warm-start effectiveness rung
**Purpose:** under fixed budget and preserved semantics, test whether the learned
warm-start route reduces warm-call median time or effective correction burden.

**Promotable phase:** yes — this is the main claim-supporting phase.

**Primary reading rule:**
- performance gain is promotable only if Phase 2 passed.

**Preferred metrics:**
- warm-call median seconds,
- corrected replay discrepancy,
- residual parity,
- iteration burden where meaningful.

**Output artifact:**
- primary effectiveness result note and decision table.

### Phase 4 — within-family ablation rung
**Purpose:** compare already-supported retained-teacher variants such as
`learned_base` vs `learned_wide`.

**Status:** explanatory unless the comparison is explicitly tied back to the frozen
cold baseline under the same evidence contract.

**Output artifact:**
- ablation note with explicit non-promotion status unless elevated by matching
  baseline comparison.

### Phase 5 — descriptive extension rungs
**Purpose:** collect explanatory-only evidence such as:
- FP64 reference checks,
- TF32 descriptive timing,
- smaller pilot particle counts,
- compile + first-call timing,
- memory snapshots.

**Status:** explicitly non-promoting.

**Interpretation rule:**
- these rungs explain behavior,
- they do not strengthen the primary effectiveness claim by themselves.

**Output artifact:**
- extension result note(s) with explicit explanatory-only label.

### Phase 6 — closeout decision phase
**Purpose:** write the final staged conclusion.

**Must include:**
- what passed,
- what failed,
- what remains unresolved,
- what next branch is justified,
- preserved non-claims,
- whether semantic-changing comparators are now justified as a new branch plan.

**Output artifact:**
- closeout result note / decision memo.

## Advancement rules
- Phase 0 must pass before any execution.
- Phase 1 must pass before any retained-teacher comparison is interpreted.
- Phase 2 must pass before Phase 3 runtime or correction-burden gains are promotable.
- Only Phase 3 can support the main retained-teacher effectiveness claim.
- Phase 4 and Phase 5 are explanatory unless explicitly tied back to the baseline
  under the frozen contract.
- Semantic-changing routes require separate plans, not a later rung in this master
  program.

## Recommended result-note ladder
This master program will be easiest to execute if each phase emits its own result
note under `docs/plans/`, for example:
- baseline result,
- correctness rung result,
- effectiveness result,
- ablation result,
- extension result,
- closeout result.

## Expected failure modes
- learned warm start reduces latent loss but not corrected replay discrepancy,
- warm start helps only at tiny budgets and not on the real LEDH-PFPF-OT path,
- heuristic warm start matches learned warm start closely enough that the neural route
  is not justified,
- GPU/JIT path nullifies practical savings,
- route or semantic drift appears under batched streaming execution,
- TF32 appears faster descriptively but introduces unresolved precision concerns,
- semantic-changing approximations outperform on one proxy while violating the
  retained-teacher contract.

## What would change our mind
- If learned warm start fails teacher-preservation or residual parity, retained-teacher
  promotion is blocked.
- If learned warm start is teacher-consistent but not more effective than heuristic,
  the simpler route should remain preferred.
- If learned warm start is teacher-consistent but not more effective than cold-start,
  the retained-teacher lane stays unpromoted.
- If later semantic-changing branches pass their own contracts and show compelling
  benefits, the repo-wide ranking can be revisited — but only under separate plans.

## Grounding references
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
- `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
- `docs/plans/batched-ledh-pfpf-ot-retained-teacher-gpu-transfer-plan-2026-06-18.md`
- `docs/plans/bayesfilter-neural-ot-retained-teacher-first-pass-implementation-plan-2026-06-18.md`
- `docs/plans/bayesfilter-neural-ot-retained-teacher-heldout-eval-result-2026-06-18.md`
- `docs/plans/bayesfilter-neural-ot-retained-teacher-low-budget-eval-result-2026-06-18.md`
- `docs/plans/bayesfilter-neural-ot-retained-teacher-low-budget-ablation-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-fp32-tf32-vs-fp64-precision-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-runtime-result-2026-06-21.md`

## Verification checklist
- old single effectiveness plan is logically inherited by this master program,
- each phase has a distinct purpose,
- only Phase 3 supports the main effectiveness claim,
- semantic-changing routes are deferred to separate branch plans,
- the frozen baseline and evidence contract appear once at the top and govern all
  later phases.
