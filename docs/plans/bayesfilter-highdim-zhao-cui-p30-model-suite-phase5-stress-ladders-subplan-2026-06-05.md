# P37-M5 Subplan: BayesFilter Dimension, Horizon, Rank, Basis, And Failure Ladders

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

## Purpose

Implement the BayesFilter stress ladders specified in P30 as project-derived
extensions beyond Zhao--Cui paper-model reproduction.  This phase measures
scaling behavior and failure modes; it does not by itself prove correctness.

M5 is split into a first executable gate and later optional ladder runs.  The
first gate may harden the stress-manifest schema, require one-axis-at-a-time
ladder governance, run the existing tiny CPU-only LGSSM stress smoke rows, and
record resource/failure classifications.  It may not claim scalability,
paper-model reproduction, GPU readiness, HMC readiness, DSGE readiness, or
posterior correctness from stress success.

## Mathematical Stress Family

P30 defines the generic nonlinear state-space stress family

```text
X_t = F_theta(X_{t-1}) + Sigma_x^{1/2} eps_t^x
Y_t = H_theta(X_t)     + Sigma_y^{1/2} eps_t^y
```

with ladders:

```text
dimension: m in {2,4,8,16,32,64}
horizon:   T in {10,50,100,500,1000}
rank:      R in {4,8,16,32,64}
basis:     p in {9,17,33,65}
```

Only one ladder is varied at a time unless the interaction itself is the
planned question.

## Source-Governance Status

- P30 anchors: `eq:p27-bf1`--`eq:p27-bf4`, robustness vetoes
  `eq:p27-r1`--`eq:p27-r9`.
- Paper anchor: BayesFilter extension, not direct Zhao--Cui reproduction.
- MATLAB anchors: none required for BayesFilter extension; source model suite
  informs stress shapes only.
- BayesFilter anchors: current `bayesfilter/highdim/validation.py` and
  `tests/highdim/test_scaling_smoke.py`.

## Evidence Contract

Question: how do memory, time, conditioning, rank saturation, and diagnostics
behave when one complexity axis is increased under a fixed test contract?

First-gate question: can BayesFilter enforce the P30 stress-ladder governance
contract for tiny CPU-only rows, including complete resource manifests,
one-axis-at-a-time ladder declarations, stop-condition metadata,
lower-phase-regression blocking, deterministic replay, and diagnostic-only
interpretation where exact references are unavailable?

Decision table:

| Field | Contract |
|---|---|
| Baseline / comparator | prior exact/model phases as guardrails; one-axis-at-a-time stress baseline |
| Primary criterion | complete resource and failure manifests over declared rows without lower-phase regressions |
| Veto diagnostics | missing stop condition, missing memory/time, proxy metric used as correctness, unplanned multiple-axis variation |
| Explanatory only | trend slopes, timing, memory curves, rank saturation counts, raw ESS |

Primary pass criteria:

- every first-gate stress row has a resource manifest and failure
  classification;
- each first-gate ladder declaration identifies exactly one active axis among
  `dimension`, `horizon`, `rank`, and `basis`;
- lower-phase guardrail status is recorded before any stress interpretation;
- exact references are used where available, otherwise accuracy is labeled
  proxy/diagnostic only;
- trend tables or row manifests report memory model, wall time,
  `n_solve_max`, condition numbers when available, rank saturation when
  available, normalizer residuals, branch/replay status, and stop reason;
- Phase 0--4 exact/model tests remain green before stress interpretation.

Vetoes:

- missing memory/time/resource fields;
- unbounded run without stop condition;
- treating wall time or finite residuals as correctness;
- varying more than one ladder axis without a specific interaction contract;
- using stress success to claim DSGE, HMC, or GPU readiness.

## Stop Conditions And Pre-Mortem

Stop a ladder if:

- lower-phase guardrail tests regress;
- memory exceeds the declared budget;
- wall time exceeds the declared budget;
- condition number exceeds the phase ceiling;
- rank saturates with residual above the declared threshold;
- any finite-value, normalizer, mass-residual, or branch/replay veto fires.

Run the cheapest discriminating row first: smallest dimension, shortest
horizon, lowest rank, and smallest basis that still exercises the planned
code path.

Misleading-pass risks:

- finite rows are mistaken for accuracy evidence;
- one-axis trends hide interaction failures;
- CPU-only smoke is mistaken for GPU production readiness;
- resource success is promoted while exact/model guardrails fail.

## Implementation Tasks

1. Add first-gate stress-ladder manifest tests that reject incomplete resource
   fields, missing ladder-axis declarations, multiple-axis variation,
   missing lower-phase guardrail status, and unsupported promotion decisions.
2. Reuse the existing CPU-only short LGSSM rows for small `m,T` as first-gate
   evidence, with exact-reference status only where the Kalman comparator is
   actually used.
3. Add optional long ladders only through separate experiment plans with
   wall-time and memory budgets.
4. Add failure-mode tests for resource, tuning, approximation, numerical
   veto, and implementation failures.
5. Defer full result tables matching P30 response surface
   `(E_acc, ESS, M_peak, T_wall, n_solve_max, kappa_max, rho_mass)` to a later
   reviewed ladder run; the first gate records the schema and tiny-row
   diagnostics only.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/validation.py
tests/highdim/test_p30_stress_ladders.py
tests/highdim/test_scaling_smoke.py
docs/plans/*p37*phase5*claude-review-ledger*.md
docs/plans/*p37*phase5*result*.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Planned Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_p30_stress_ladders.py

git diff --check
```

Long or GPU stress runs require a separate experiment plan, run manifest, and
trusted GPU execution when GPU is used.

## Exit Criteria

- short stress ladders produce complete manifests;
- failures are classified and not hidden;
- result ledger clearly labels BayesFilter extension status;
- no paper-model reproduction or production-scalability overclaim.

## First-Gate Stress Manifest Contract

The first gate adds or verifies a stress-ladder manifest layer over each
`StressRunManifest`.  A valid row must record:

- `phase_id = P37-M5`;
- `ladder_axis` in `{dimension, horizon, rank, basis, none}`;
- `varied_axes`, with at most one axis other than fixture bookkeeping;
- `fixed_axes`, containing the non-varied ladder controls;
- `lower_phase_guardrail_status`, which must be `PASS` for interpretation and
  must block the row when regressions are detected;
- `evidence_interpretation` in `{EXACT_REFERENCE, DIAGNOSTIC_ONLY}`;
- `promotion_decision` in `{STRESS_SCHEMA_ONLY, RECORD_DIAGNOSTIC_ROW}`;
- `non_claims`, including no correctness, scalability, GPU, HMC, DSGE, or
  paper-reproduction claim.

Rows with `ladder_axis != none` must vary exactly that single axis.  Rows with
`ladder_axis = none` are fixture/schema smoke rows and must be labeled
`DIAGNOSTIC_ONLY` unless an exact comparator is named.  `PROMOTE_SCALABILITY`,
`PROMOTE_CORRECTNESS`, and similar decisions are invalid in the first gate.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_AFTER_SCOPE_HARDENING`.

The original M5 wording risked treating finite stress-smoke rows as evidence of
correctness or scalability.  That would be a proxy-metric error.  Stress rows
can reveal resource behavior and failure modes, and exact LGSSM rows can also
guard against regressions, but neither proves that nonlinear high-dimensional
filtering is generally accurate, scalable, or production-ready.

The first gate is therefore narrowed to governance and tiny-row evidence:
complete resource manifests, one-axis-at-a-time declarations, stop-condition
metadata, lower-phase guardrail status, deterministic replay, and explicit
diagnostic-only interpretation when no exact reference is present.  Full
dimension/horizon/rank/basis ladders, GPU runs, and response-surface tables
require separate reviewed experiment plans with wall-time and memory budgets.

One nomenclature issue is known and accepted for this gate: some existing
BayesFilter stress helpers say "Phase-6" because they predate this P30 runbook.
M5 may preserve public symbol names for compatibility, but any new result
ledger must describe the current runbook phase as P37-M5.

No material flaw remains in sending this narrowed M5 plan to Claude plan
review.  Implementation may not begin until `PASS_M5_PLAN`.
