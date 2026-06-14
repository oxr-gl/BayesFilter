# P37-M2.6a Claude Review Ledger

metadata_date: 2026-06-05
phase: P37-M2.6a fixed-design TT SV adjacent target

review_scope:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-remaining-phases-gated-execution-master-plan-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-subplan-2026-06-05.md`

## Iterations

### Plan Gate Iteration 1

worker: `highdim-p37-m2p6a-plan-review-iter1`

status: `BLOCKED_M2P6A_PLAN`

raw_response:

```text
BLOCKED_M2P6A_PLAN

1. Governance gap: the core fitted object `h_t(z) = sqrt(g_t(T(z)) |det DT(z)| / omega(z))` and the allowed max-log scaling are not traceably anchored at the claim site to exact P30/paper units or explicitly labeled as BayesFilter extensions. The plan cites broad TT/basis and squared-density/SIRT sections, but that is too loose for a gate whose correctness depends on Jacobian/reference-density handling and scaled reconstruction.
Minimal fix: add exact P30/paper equation/section anchors for the reference-space square-root target, and mark max-log scaling plus branch-hash replay as `BAYESFILTER_EXTENSION` with BayesFilter code/test anchors.

2. The primary pass criteria are not executable because the required tolerances are undeclared. "Below declared tolerances" and "within declared relative error tolerance" leave room for post hoc threshold selection.
Minimal fix: pin the exact train RMS, holdout RMS, and heldout target relative-error thresholds in the subplan, and state how the weights are normalized for each metric.

3. The two "fixed adjacent targets" are not actually fixed. The plan does not pin the exact `theta`, observation tuple/time index, coordinate-map window, basis degree/ranks, or the specific M2.5 retained-filter artifact/hash used for the transition target, so the baseline can drift or be cherry-picked after implementation.
Minimal fix: name the exact deterministic fixtures (parameters, observations, `t`, coordinate map/domain, fit config, holdout construction, and retained-filter manifest/hash from M2.5) and require the result ledger to report those IDs unchanged.

4. The skeptical audit says M2.6a must stop on broad M2/M2.5 guardrail regression, but the Evidence Contract does not list that regression as a veto diagnostic. That leaves the formal veto set narrower than the stated stop condition.
Minimal fix: add LGSSM/M2/M2.5 regression to the veto diagnostics, not just the exit checklist.
```

fixes:
- Added traceability text for the reference-space square-root target and
  labeled max-log scaling/branch replay as BayesFilter extensions.
- Pinned deterministic model, target, retained-filter, coordinate-map, basis,
  rank, fit, training, and holdout fixtures.
- Pinned train RMS, holdout RMS, and heldout target relative-error thresholds
  plus metric weight normalization.
- Added LGSSM/M2/M2.5 regression to formal veto diagnostics.

### Plan Gate Iteration 2

worker: `highdim-p37-m2p6a-plan-review-iter2`

status: `BLOCKED_M2P6A_PLAN`

raw_response:

```text
BLOCKED_M2P6A_PLAN

1. The revised subplan still does not satisfy the charter's traceability standard for the core mathematical claim because the claim site names only broad source regions, not exact equation/section anchors for the fitted reference-space object. In `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-subplan-2026-06-05.md:21-28` and `:95-106`, the plan says the square-root/reference-space target is "traceable" and cites "Algorithm 5 dataflow sections" and "TT/basis sections," but unlike the prior blocker's requested fix it still does not pin exact P30/paper equations/sections for: the adjacent target \(g_t\), the pullback/Jacobian/reference-density conversion, and the square-root/squared-density construction. The exact anchors do appear available in the governing note (for example `eq:p25-bridge-1`-`eq:p25-bridge-3`, the reference-coordinate equations around `eq:p25-bridge-8`-`eq:p25-bridge-11`, and the square-root object around the "Object 2" equations in P30), but they are not written into the M2.6a subplan itself. Under the governance charter, a mathematical claim must carry exact anchors or be blocked.
   Minimal fix: in the M2.6a subplan, replace the broad source-language with exact P30 equation labels and exact paper section/equation references for (a) the adjacent target, (b) the reference-space/Jacobian/reference-density conversion, and (c) the square-root-to-squared-density construction, while keeping max-log scaling explicitly marked `BAYESFILTER_EXTENSION`.
```

fixes:
- Replaced broad source-language at the claim site with exact P30 equation
  labels for adjacent target, retained/evidence normalization,
  physical-to-reference pullback, reference-measure correction, square-root
  fitting values, and squared-density reconstruction.

### Plan Gate Iteration 3

worker: `highdim-p37-m2p6a-plan-review-iter3`

status: `PASS_M2P6A_PLAN`

raw_response:

```text
PASS_M2P6A_PLAN
```

### Fixture Revision After Initial Implementation Attempt

status: `REVISION_PENDING_REVIEW`

evidence:

```text
Focused implementation run failed degree-12 fixture:
- initial train RMS: 0.006158834878663081 > 2e-5
- transition train RMS: 0.006376784097517419 > 2e-5

Bounded diagnostic over same target/metrics:
- degree 64 initial train RMS: 9.731925961886445e-12
- degree 64 initial holdout RMS: 9.731913175401359e-12
- degree 64 initial max heldout relative target error: 2.0825048112607124e-05
- degree 64 transition train RMS: 4.284141828074127e-13
- degree 64 transition holdout RMS: 4.283704913934066e-13
- degree 64 transition max heldout relative target error: 3.4017456603229e-07
```

fix:
- Revised the fitting fixture from `max_degree=12` and `column_budget>=13` to
  `max_degree=64` and `column_budget>=65` without changing target, data,
  coordinate map, scaling, or pass tolerances.

### Fixture Revision Review Iteration 1

worker: `highdim-p37-m2p6a-fixture-revision-review-iter1`

status: `BLOCKED_M2P6A_FIXTURE_REVISION`

raw_response:

```text
BLOCKED_M2P6A_FIXTURE_REVISION

1. The revision uses the same holdout evidence for both tuning and promotion. The bounded diagnostic that justifies `max_degree=64` explicitly inspects the same holdout RMS and heldout relative target error that remain primary pass criteria in `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-subplan-2026-06-05.md:177,208-212,275-287` and `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-claude-review-ledger-2026-06-05.md:88-100`. Once those holdout points were consulted to choose capacity, they are no longer independent promotion evidence for the claim at `...subplan-2026-06-05.md:195-197`.
   Minimal fix: freeze degree-64 as a pre-promotion tuning correction, but add a fresh untouched audit holdout fixture for the final promotion gate; or explicitly demote the current holdout metrics to tuning diagnostics and promote only on a newly declared audit set.

2. The plan says fixture changes must be recorded as a new fixture version rather than silently substituted, but the fitting fixture is revised in place without a new fitting-fixture ID/version in `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-subplan-2026-06-05.md:124-125,167-179,275-287` and `...claude-review-ledger-2026-06-05.md:97-100`. That makes the promoted artifact less traceable than the plan's own governance rule requires.
   Minimal fix: assign the revised fitting configuration its own fixture version/ID and require the result ledger to report both the failed original fixture and the revised promotion fixture explicitly.
```

fixes:
- Added revised fitting fixture ID
  `p37.m2p6a.sv.fixed-design-fit.degree64.v2` and failed original fixture ID
  `p37.m2p6a.sv.fixed-design-fit.degree12.v1`.
- Demoted the consulted Gauss-Legendre order-121 holdout to tuning evidence.
- Added a fresh audit holdout fixture: deterministic midpoint-shifted uniform
  grid with 149 points and uniform probability weights.
- Changed primary promotion wording from holdout metrics to audit metrics.

### Fixture Revision Review Iteration 2

worker: `highdim-p37-m2p6a-fixture-revision-review-iter2`

status: `PASS_M2P6A_FIXTURE_REVISION`

raw_response:

```text
PASS_M2P6A_FIXTURE_REVISION
```

### Code/Governance Gate Iteration 1

worker: `highdim-p37-m2p6a-code-governance-review-iter1`

status: `PASS_M2P6A_CODE_GOVERNANCE`

raw_response:

```text
PASS_M2P6A_CODE_GOVERNANCE
```

## Final Status

`PASS_M2P6A_PLAN`; `PASS_M2P6A_FIXTURE_REVISION`;
`PASS_M2P6A_CODE_GOVERNANCE`.
