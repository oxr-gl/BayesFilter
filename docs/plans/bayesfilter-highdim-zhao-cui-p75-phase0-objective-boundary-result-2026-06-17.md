# P75 Phase 0 Result: Objective Boundary And Current Surface

metadata_date: 2026-06-17
status: PHASE0_PASSED_CLAUDE_AGREE_READY_FOR_PHASE1
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-subplan-2026-06-17.md
previous_handoff: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-stop-handoff-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-subplan-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Is P75 correctly scoped as a stochastic density-objective pilot rather than a larger ALS diagnostic? |
| Exact baseline/comparator | P73 blocked diagnostic and P73 Phase 6 handoff. |
| Primary criterion | Satisfied pending Claude review.  P75 is classified as an extension/invention, the current implementation gap is identified, proxy promotion is forbidden, and the Phase 1 design subplan is drafted. |
| Veto diagnostics | No implementation edit, training run, pilot diagnostic, validation, HMC, scaling, GPU, rank promotion, or threshold change was launched. |
| Explanatory only | Parameter/sample counts, current ALS surface, `SquaredTTDensity` evaluator, P73-B blocked status. |
| What is not concluded | No implementation correctness, no pilot success, no lower-gate repair, no validation readiness, no adaptive Zhao--Cui parity. |
| Artifact preserving result | This result, Phase 1 subplan, execution ledger, review ledger. |

## Skeptical Plan Audit

Phase 0 passed the skeptical audit before execution.  It used the actual P73
blocked diagnostic as baseline, targeted the objective mismatch rather than a
larger ALS sample count alone, and remained planning-only.

## Classification

P75 stochastic density training is:

```text
extension_or_invention
```

It is not source-faithful adaptive Zhao--Cui.  The following P75 operations
must not be called source-faithful unless later phases provide paper and
author-source anchors:

- trainable TT variables;
- stochastic fresh-batch optimizer loops;
- Adam or other gradient optimizers;
- empirical KL/cross-entropy objectives;
- differentiable normalizer penalties;
- line/audit penalties inside training;
- stochastic sample-renewal schedules.

The fixed Zhao--Cui target construction, coordinate frame, and P73/P72 gates
may be used as local comparators and evaluation contracts, but they do not
make the optimizer route source-faithful.

## Current Implementation Surface

The current implementation supports:

- whole-batch weighted ridge ALS through `FixedTTFitter`;
- pointwise square-root regression on a fixed finite cloud;
- `SquaredTTDensity.log_density(points)`;
- exact squared-TT normalizer computation through paired-core mass
  contractions;
- an opt-in P73 cross-entropy evaluator on an existing density;
- explicit `P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED`.

The current implementation does not yet support:

- a trainable TT object whose cores are persistent `tf.Variable`s;
- stochastic fresh-batch optimization over many batches;
- a real P73-B/P75 optimizer for
  \(-E_q[\log \rho_\theta(z)] + \log Z_\theta\) or a reviewed surrogate;
- optimizer manifests, checkpoints, gradient diagnostics, or learning-rate
  schedules;
- audit-holdout-safe training/evaluation split for stochastic training.

`FunctionalTT` and `SquaredTTDensity` are differentiable through TensorFlow
operations when evaluated inside a tape, but `TTCore` converts values to
tensors and the existing density wrapper is immutable and manifest-oriented.
Phase 1 should therefore design a small trainable adapter rather than assume
the current density class is already an optimizer surface.

## Objective Boundary

The mathematical issue is not just sample count.  Larger pooled ALS would
still optimize a pointwise regression objective:

\[
\min_\theta \sum_i w_i\{h_\theta(z_i)-g(z_i)\}^2 + \lambda \|\theta\|^2.
\]

P75 should target a density objective.  A candidate form is:

\[
L(\theta)
=
-E_{z\sim q}\log \rho_\theta(z) + \log Z_\theta + R(\theta),
\qquad
p_\theta(z)=\rho_\theta(z)/Z_\theta,
\]

where \(\rho_\theta(z)=h_\theta(z)^2+\tau q_0(z)\), and \(R\) is a reviewed
regularizer or penalty.  Phase 1 must decide the exact pilot objective,
including how \(q\), \(\rho_\theta\), \(Z_\theta\), regularization, training
samples, and fresh audit samples are defined.

## Phase 1 Handoff

Phase 1 must produce a mathematical design contract before implementation.
It must decide:

- the exact training objective;
- whether \(\log Z_\theta\) is exact from TT contractions, Monte Carlo
  estimated, or initially replaced by a safer pilot penalty;
- how trainable cores are initialized from the current fixed branch or from a
  fresh seed;
- batch size, batch count, and pilot schedule;
- CPU-only versus GPU escalation boundaries;
- train/eval/audit separation;
- finite-loss, finite-gradient, and fresh-audit evaluation gates;
- which metrics are pass criteria and which are explanatory only.

## Local Checks

Phase 0 local checks passed:

```text
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-stop-handoff-2026-06-17.md
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
rg -n "P73_PHASE6_PASSED_CLAUDE_AGREE_COMPLETE|fresh audit|P73-B|blocked" ...
rg -n "FixedTTFitter|SquaredTTDensity|log_density|normalizer|GradientTape|Adam|tf.Variable" ...
```

The source scan found no existing P75-style stochastic density optimizer.

## Nonclaims

- No implementation was written.
- No training was run.
- No pilot result exists.
- No lower gate is repaired.
- No validation/HMC/scaling readiness is claimed.
- No source-faithful adaptive Zhao--Cui parity is claimed.

## Claude Review

Claude returned:

```text
VERDICT: AGREE
```

Claude agreed that Phase 0 correctly classifies P75 as
`extension_or_invention`, identifies the missing stochastic density optimizer,
avoids implementation/training claims, preserves audit-holdout exclusion, and
that the Phase 1 subplan has the required governance sections.
