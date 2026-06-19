# P75 Phase 3 Result: Opt-In Implementation And Unit Tests

metadata_date: 2026-06-17
status: PHASE3_LOCAL_CHECKS_PASSED_CLAUDE_REVIEW_PENDING
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-subplan-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Does the opt-in P75 implementation correctly expose finite differentiable stochastic density-training mechanics? |
| Exact baseline/comparator | Phase 2 surface map, immutable `SquaredTTDensity` normalizer and density evaluation, and current P73-B blocked evaluator. |
| Primary criterion | Satisfied pending Claude review.  Focused CPU-only tests and smoke commands pass; implementation remains opt-in; exact normalizer, `rho_theta`, and log-density match immutable snapshot density on tiny cases; gradients are finite; audit records are rejected; P72/P73 regression checks pass; Phase 4 subplan is drafted. |
| Veto diagnostics | No target pilot, validation, HMC, scaling, GPU, rank promotion, threshold change, package/network action, or P72/P73 default behavior change was launched. |
| Explanatory only | Synthetic smoke loss values, one-step parameter deltas, TensorFlow initialization messages, runtime. |
| What is not concluded | No target-pilot success, lower-gate repair, validation readiness, HMC readiness, scaling claim, rank/sample policy, or adaptive Zhao--Cui parity. |
| Artifact preserving result | This result, code/tests/runner diffs, smoke JSONs in `/tmp`, Phase 4 subplan, ledgers. |

## Skeptical Plan Audit

Phase 3 passed the skeptical audit before implementation.  It edited only the
new opt-in P75 module, tests, and runner surfaces authorized by Phase 2.  It
kept P72/P73 default code untouched, kept the smoke synthetic and tiny, and
did not treat smoke loss as pilot or lower-gate evidence.

## Implemented Surfaces

Created:

- `bayesfilter/highdim/stochastic_density_training.py`;
- `tests/highdim/test_p75_stochastic_density_training.py`;
- `scripts/p75_stochastic_density_training_pilot.py`.

No top-level `bayesfilter` export was added.  No `bayesfilter.highdim.__all__`
export was added.  Tests import the opt-in module directly as
`bayesfilter.highdim.stochastic_density_training`.

## Implemented Mechanics

The new module implements:

- `P75TrainableTTConfig`;
- `P75ObjectiveBatch`;
- `P75ObjectiveTerms`;
- `TrainableFunctionalTT`;
- pure TensorFlow `evaluate`, `sqrt_square_normalizer`, `normalizer`,
  `rho_theta`, `log_density`, and objective routines;
- weighted empirical target weights
  \(\alpha_i\propto w_i(g_i^2+\tau q_0(z_i))\);
- Adam training step with finite-gradient and clipping checks;
- audit-record and audit-hash rejection;
- snapshot conversion into immutable `FunctionalTT` and `SquaredTTDensity`;
- JSON payload helpers for manifests.

The new runner implements:

- `--schema-only`;
- bounded synthetic `--smoke-only`;
- dormant reviewed command surface for `--target-pilot`, not executed in
  Phase 3.

Resumed review found and repaired one target-pilot preflight bug before Phase
4 execution: source-route diagnostic and guard-line clouds use column-major
shape `[dimension, point_count]`, while P75 objective batches use row-major
shape `[point_count, dimension]`.  The runner now exposes separate helpers for
those two conventions and the line-audit target evaluation uses the
source-route cloud convention.  The resumed patch also simplified
`completed_batches` accounting so it records only successful optimizer steps.

## Tests And Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
```

Initial result:

```text
9 passed, 2 warnings
```

After the target-pilot orientation/accounting repair, the resumed focused test
suite passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
```

Result:

```text
10 passed, 2 warnings
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --schema-only --output /tmp/p75-schema.json
```

Result summary:

```text
p75_status = P75_SCHEMA_READY_PHASE4_NOT_EXECUTED
overall_status = not_executed
phase4_target_pilot_executed = false
smoke_only_not_pilot_evidence = true
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --smoke-only --output /tmp/p75-smoke.json
```

Result summary:

```text
p75_status = P75_SMOKE_COMPLETED_NOT_PILOT_EVIDENCE
overall_status = pass
any_core_changed = true
finite_parameter_deltas = true
p73_b_optimizer_status = P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED
phase4_target_pilot_executed = false
```

TensorFlow emitted CUDA factory/cuInit log messages despite
`CUDA_VISIBLE_DEVICES=-1`.  The run was intentionally CPU-only and the
artifacts record `cpu_only_cuda_visible_devices_minus_1`; these messages are
not treated as GPU evidence.

Passed:

```text
rg -n "P75|TrainableFunctionalTT|tf.Variable|GradientTape|weighted_empirical_cross_entropy|normalizer|audit|nonclaims" ...
git diff --check -- bayesfilter/highdim/stochastic_density_training.py tests/highdim/test_p75_stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py ...
```

## Synthetic Smoke Result

The synthetic smoke used:

- dimension 2;
- degree 2;
- rank 2;
- batch size 4;
- 1 optimizer step;
- no Zhao--Cui fresh target batches;
- no audit gate;
- no validation/HMC/scaling/rank promotion.

The smoke manifest at `/tmp/p75-smoke.json` records:

- finite objective terms;
- finite gradient norm;
- finite parameter deltas;
- P73-B remains blocked;
- `smoke_only_not_pilot_evidence=true`;
- `phase4_target_pilot_executed=false`.

## Dormant Target-Pilot Surface

The runner now exposes a reviewed but unexecuted `--target-pilot` command
surface.  It is intended for Phase 4 review and execution.  It uses:

- author-SIR step-1 fixed-variant target generation;
- independent training seeds from the P72/P73 audit seeds;
- degree/rank/batch/batch-count arguments;
- exact P75 objective training;
- post-training holdout, replay, and audit-line diagnostics.

Phase 3 did not execute this surface.  Phase 4 must run a tiny real target
smoke before any 1024-by-500 target pilot.

## Nonclaims

- No target pilot has run.
- No lower-gate repair is claimed.
- No full sequential Zhao--Cui result is claimed.
- No validation/HMC/scaling/rank-promotion readiness is claimed.
- No source-faithful adaptive Zhao--Cui parity is claimed.

## Phase 4 Handoff

Phase 4 should begin with a tiny real fixed-variant target smoke through the
new `--target-pilot` surface, such as degree 1/rank 1/batch 16/batches 2 with
a short wall-clock cap.  Only if that real target smoke passes should Phase 4
attempt the user-requested degree 2/rank 4/batch 1024/up-to-500-batches run.

## Local Checks

Passed in the resumed visible run:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
```

Result:

```text
9 passed, 2 warnings
```

Passed in the resumed visible run:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --schema-only --output /tmp/p75-schema-resume.json
```

Result summary:

```text
p75_status = P75_SCHEMA_READY_PHASE4_NOT_EXECUTED
overall_status = not_executed
phase4_target_pilot_executed = false
```

Passed in the resumed visible run:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --smoke-only --output /tmp/p75-smoke-resume.json
```

Result summary:

```text
p75_status = P75_SMOKE_COMPLETED_NOT_PILOT_EVIDENCE
overall_status = pass
any_core_changed = true
finite_parameter_deltas = true
p73_b_optimizer_status = P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED
phase4_target_pilot_executed = false
```

Passed in the resumed visible run:

```text
git diff --check -- bayesfilter/highdim/stochastic_density_training.py tests/highdim/test_p75_stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-subplan-2026-06-17.md
```

Result:

```text
no output
```

## Claude Review

Pending.
