# Candidate Audit: Direct Low-Rank Coupling OT

Date: 2026-06-17

## Status

`source_locked`; semantic class: semantic replacement.  Execution value is
`execution_value_pending`.

This lane constrains or parameterizes the coupling itself as a low-rank
nonnegative object.  It is not a low-rank approximation to the Gibbs kernel and
should not be judged by exact dense Sinkhorn parity alone.

## Paper-Note-Code-Execution Matrix

| Comparison item | Original paper | Local note | Downloaded code | Execution-value test | Required resolution |
| --- | --- | --- | --- | --- | --- |
| Problem solved | Forrow factored couplings and Scetbon low-rank Sinkhorn constrain the coupling as low nonnegative rank. Local paper OCR for `2103.04737.txt` is present but messy; the survey equations are cleaner. | Survey lines 628-760 define nonnegative rank, `Pi_{a,b}(r)`, `P = Q diag(1/g) R^T`, transport application, latent-coupling extension, and rank diagnostics. | POT `ot/lowrank.py` lines 322-527 implements `lowrank_sinkhorn` returning `Q,R,g` and lazy plan. POT `ot/factored.py` lines 17-170 implements factored OT returning `Ga,Gb,X` and lazy plan. OTT-JAX `sinkhorn_lr.py` lines 153-180 defines `LRSinkhornOutput`; lines 228-250 expose cost/mass; lines 716-735 builds output from `q,r,g`. | Tiny factorized-coupling fixture with `rank < N`; compare finite factors, marginal residuals, transported particles, and semantic delta from dense baseline. | Treat dense-reference error as explanatory, not a hard veto, because this solves a different constrained problem. |
| Transport object | Coupling is `P = Q diag(1/g) R^T`; transport is `Q diag(1/g) R^T X`. | Survey equations `eq:factored-coupling` and `eq:factored-transport` define the required BayesFilter object. | POT `lowrank_sinkhorn` returns `Q,R,g`; log mode stores `lazy_plan` at lines 519-525. POT factored OT stores `lazy_plan` at lines 146-157. OTT-JAX stores `q,r,g`. | Candidate wrapper must expose factors and transported particles. | Factor orientation and the `g` convention must be reconciled before any comparison. |
| Marginals/orientation | Factor constraints require `Q in Pi(a,g)` and `R in Pi(b,g)`. | Survey equations `eq:factored-coupling-constraints` and `eq:fc-set` define local marginal constraints. | OTT-JAX `solution_error` lines 120-150 computes marginal deviation for `q` and `r`; POT Dykstra enforces factor marginals. | Record factor marginal residuals and induced coupling residuals if materialized on tiny fixtures. | Marginal residuals are hard vetoes for coupling validity. |
| Cost/kernel/epsilon | Direct low-rank coupling optimizes transport cost under rank constraints, with optional entropic regularization in implementations. | Local note separates this from kernel approximation and flags it as a real algorithmic change. | POT code uses sample locations and low-rank cost decomposition at `lowrank.py` lines 446-517. | Candidate config must record rank, regularization, initialization, and cost scaling. | Do not use dense Sinkhorn epsilon semantics as if unchanged. |
| Approximation knob | Nonnegative rank, latent rank, initialization, and lower bound on `g`. | Survey lines 697-756 describe latent-coupling and rank-sufficiency diagnostics. | POT exposes `rank`, `init`, `seed_init`, `alpha`, `gamma_init`; OTT-JAX exposes low-rank state. | Freeze rank/init/seed for deterministic tests; later rank ladder is explanatory and repair-oriented. | One favorable rank does not justify general rank choice. |
| Backend and gradients | Algorithm is backend independent in math; source implementations use POT/JAX. | BayesFilter implementation must be TensorFlow/TFP unless exception approved. | POT is backend-dispatched but generic; OTT-JAX is JAX. | Phase 6 should be a declared TensorFlow semantic-replacement prototype. | Non-TF source remains reference unless reviewed exception exists. |
| Execution value | Low-rank coupling reduces storage/application when low rank is adequate. | Local note says this is promising but semantically different. | Code exposes factors, so the transport object is inspectable. | First execution-value artifact must show finite factors, residuals, transported particles, downstream diagnostic, and dense semantic delta. | No ranking, no speedup, and no execution-value claim from static source inspection. |

## Source And Semantic Classification

- Source status: `source_locked`.
- Semantic class: semantic replacement over low-rank couplings.
- BayesFilter posture: viable but should be tested after the common harness
  because it changes the optimization problem.
- Required transport: low-rank factors and transported particles.

## First Execution-Value Contract

Question: can a low-rank coupling route provide a valid resampling transform
with acceptable downstream diagnostics on deterministic fixtures?

Baseline/comparator: Phase 1 dense/streaming baseline for descriptive semantic
delta, not as an exact parity promotion criterion.

Primary criterion: finite `Q,R,g`, valid factor marginals, finite transported
particles, and a documented semantic replacement interpretation.

Vetoes: invalid factor marginals, negative/zero invalid `g`, missing
transported particles, dense-error treated as exact-parity criterion, or
non-TensorFlow source promoted to default.

Not concluded: no exact dense Sinkhorn equivalence, no posterior correctness,
no default change, no statistically supported ranking.

## Decision

Advance as a semantic-replacement candidate with strong source support.  It
should have its own Phase 6 prototype and should not be mixed into the
Nystrom/positive-feature approximate-kernel parity ladder.
