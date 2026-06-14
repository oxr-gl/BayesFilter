# P47 Claude Review Ledger: Remaining Zhao--Cui Filtering Completion

metadata_date: 2026-06-08
phase: P47-plan-review
status: `BLOCKED_AFTER_MAX_5_CLAUDE_REVIEW_ITERATIONS`

## Role Contract

Codex is supervisor and executor. Claude is read-only reviewer only. Claude
must not edit files, run experiments, launch agents, or change state.

## Review Scope

- `docs/plans/bayesfilter-highdim-zhao-cui-p47-remaining-filtering-completion-master-program-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase0-governance-freeze-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase1-adaptive-tt-sirt-route-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase2-paper-scale-filtering-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase3-generalized-sv-equality-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase4-spatial-sir-filtering-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase5-predator-prey-filtering-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase6-score-hmc-readiness-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-subplan-2026-06-08.md`

## Requested Review

Check for:

- wrong baselines;
- target mismatch;
- S&P 500 scope leakage;
- proxy metrics promoted to correctness;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- environment mismatch;
- unsupported HMC/API/paper-scale/adaptive claims;
- missing phase dependencies or pass/block tokens.

End with exactly:

```text
PASS_P47_PLAN_GOVERNANCE
```

or

```text
BLOCK_P47_PLAN_GOVERNANCE
```

## Iterations

### Iteration 1

Verdict:

```text
BLOCK_P47_PLAN_GOVERNANCE
```

Accepted findings:

- M2 was ordered before model-specific filtering baselines and could outrun
  spatial-SIR/predator-prey dense/refined references.
- M2 primary criterion promoted finite paper-scale outputs plus manifests as
  filtering success, which is feasibility evidence, not correctness evidence.
- M2 used lower-rung value-path gates where filtering/target-closure baselines
  are required for some targets.
- M6 mixed stable production score API and HMC readiness without a separate
  API-contract gate.
- M6 did not enumerate per-target upstream dependency tokens.
- M4--M6 needed phase-local resource/trusted-execution stop controls.

Patch response:

- Recast M2 as paper-scale readiness and feasibility-manifest preparation; no
  correctness promotion before model-specific M3--M5 gates.
- Clarified that M3--M5 own model-specific production filtering correctness
  and dense/refined reference gates.
- Added API-contract criteria to M6 and explicit upstream tokens per target.
- Added phase-local long-run/GPU/trusted-execution stop controls to M4--M6.

### Iteration 2

Verdict:

```text
BLOCK_P47_PLAN_GOVERNANCE
```

Accepted findings:

- M3--M6 lacked phase-local prerequisite tokens, leaving target governance,
  scope exclusion, and adaptive-route decisions enforceable only by the master
  program narrative.
- M4 still let finite production manifests contribute to production filtering
  correctness without a model-specific production-scale correctness criterion
  or explicit nonclaim barrier.
- M5 allowed a proposal/preconditioner proxy metric to satisfy the phase gate
  without downstream filtering quality.
- M6 depended on broad M4/M5 tokens even though those tokens could pass without
  value/gradient or downstream filtering-quality evidence.

Patch response:

- Added phase-local prerequisite token sections to M3--M6.
- Reframed M4 so finite production manifests are feasibility/stress evidence
  unless model-specific reference/equality criteria also pass.
- Reframed M5 so proposal/preconditioner metrics are explanatory and cannot
  satisfy the phase gate without downstream filtering quality.
- Hardened M6 dependencies so spatial SIR and predator-prey upstream tokens
  must contain same-target value/gradient or filtering-quality evidence, not
  feasibility/proposal-only evidence.

### Iteration 3

Verdict:

```text
BLOCK_P47_PLAN_GOVERNANCE
```

Accepted findings:

- M2 still lacked local `PASS_P47_M0_GOVERNANCE` and
  `PASS_P47_M1_ADAPTIVE_ROUTE` prerequisite tokens.
- Downstream phases did not force promoted rows to carry forward the M1 route
  label, leaving a leak path where documented-deviation fixed-design evidence
  could be described generically as Zhao--Cui filtering or adaptive
  reproduction.

Patch response:

- Added M2 phase-local prerequisite tokens and route-label requirements.
- Added route-label requirements to M0 registry fields, M2 readiness rows,
  M3 equality rows, M4 filtering/equality rows, M5 filtering/preconditioning
  rows, M6 API/HMC rows, M7 closeout, and the master promotion/veto criteria.

### Iteration 4

Verdict:

```text
BLOCK_P47_PLAN_GOVERNANCE
```

Accepted findings:

- M1 still risked certifying adaptive TT-cross/SIRT reproduction from route
  identity and tiny branch-fixture tests alone.
- The master nonclaim rule said adaptive reproduction needed later evidence,
  but the phase stack had no stronger adaptive-reproduction gate.
- M7 lacked phase-local prerequisite tokens for M0--M6.

Patch response:

- Recast M1 as route-label governance only: `adaptive route candidate` or
  `documented-deviation fixed-design substitute`.
- Added explicit nonclaim language that `adaptive route candidate` is not
  adaptive reproduction without later matched-target filtering evidence and
  closeout approval.
- Updated all downstream route-label requirements to use `adaptive route
  candidate`, not `adaptive reproduction`.
- Added M7 phase-local prerequisite tokens and a rule that blocked upstream
  phases allow only blocker closeout, not `PASS_P47_M7_CLOSEOUT`.

### Iteration 5

Verdict:

```text
BLOCK_P47_PLAN_GOVERNANCE
```

Accepted remaining blockers:

- M4 can still emit `PASS_P47_M4_SPATIAL_SIR_FILTERING` from small-`J`
  reference/equality success without `PASS_P47_M2_PAPER_SCALE_READINESS` or a
  production-scale row, while the master scope says P47 should deliver
  production-grade spatial SIR filtering evidence.
- M5 has the same scale leak: `PASS_P47_M5_PREDATOR_PREY_FILTERING` can be
  earned on small dense/refined work without a production- or paper-scale row.
- M6 depends on the broad M4/M5 tokens, so the scale leak can propagate into
  score/API/HMC readiness for spatial SIR and predator-prey.

Max-loop decision:

- The requested Claude review loop reached the maximum of five iterations
  without convergence.
- Do not emit `PASS_P47_PLAN_GOVERNANCE`.
- Do not launch P47 execution from this packet.

Recommended repair before a fresh review loop:

- Either narrow the master scope from "production-grade spatial SIR and
  predator-prey filtering evidence" to "model-specific lower-rung
  reference/equality gates plus separately planned production-scale runs"; or
  strengthen M4 and M5 so their pass tokens require M2 plus at least one
  production- or near-paper-scale row with model-specific reference guardrails.
- Split M4/M5 tokens if needed, for example lower-rung
  `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY` and production-scale
  `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`, with M6 depending only on
  the appropriate per-target evidence class.
