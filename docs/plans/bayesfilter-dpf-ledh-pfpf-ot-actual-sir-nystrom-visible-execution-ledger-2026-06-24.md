# Actual-SIR Nystrom Visible Execution Ledger

Date: 2026-06-24

## Ledger

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the fixed-policy Nystrom route show repeated `N=8192` paired-threshold failures across seeds `82924..82931`? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Primary criterion | Valid per-seed artifacts, then predeclared failure-count classification. |
| Veto diagnostics | Missing/malformed artifacts, wrong policy metadata, missing GPU/TF32 evidence, nonfinite outputs, residual hard veto, comparator failure, timeout. |
| Explanatory diagnostics | Runtime, warm ratio, ESS, residual magnitudes below threshold, paired delta magnitudes, factor/scaling diagnostics. |
| Not concluded | No statistical failure probability, no default readiness, no ranking, no HMC readiness, no posterior correctness. |

## Skeptical Plan Audit

Audit before launch: the G1 command uses route `both`, same model and seed
panel, compiled streaming comparator in the same artifact, fixed Nystrom policy,
`float32`, TF32 enabled, trusted GPU preflight, and old quarantined runtime
artifacts are excluded from ranking evidence.

## Forbidden Claims/Actions

- Do not claim default readiness.
- Do not claim HMC readiness.
- Do not claim posterior correctness.
- Do not claim statistical ranking or statistical failure probability.
- Do not tune rank, epsilon, solver, thresholds, chunks, model, or seeds in G1.

## Stop Conditions

- Trusted GPU unavailable.
- Any launched row times out.
- Required artifact missing or malformed.
- Fixed-policy or comparator metadata mismatch.
- Continuing would require tuning, threshold changes, or a default-policy
  decision.

### 2026-06-24 - G0/G1 - PRECHECK

Evidence contract:

- Question: classify whether the current fixed-policy `N=8192` paired drift is
  repeated across a broader seed panel.
- Baseline/comparator: compiled streaming TF32 actual-SIR route in the same
  paired artifact.
- Primary criterion: valid artifacts for seeds `82924..82931`, then
  predeclared failure-count classification.
- Veto diagnostics: malformed/missing artifacts, wrong policy metadata, missing
  GPU/TF32 evidence, nonfinite outputs, residual failure, comparator failure,
  timeout.
- Nonclaims: no default readiness, no HMC readiness, no posterior correctness,
  no statistical ranking or failure probability.

Actions:

- Created visible master program and runbook.
- Created G1 subplan.
- Before launch, run local skeptical audit and trusted GPU preflight.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-governed-gap-execution-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-visible-gated-execution-runbook-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-subplan-2026-06-24.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run local plan checks and GPU preflight.

### 2026-06-24 - G1 - EXECUTE_MINIMAL

Evidence contract restated before launch:

- Question: count paired-threshold failures across seeds `82924..82931` under unchanged fixed policy.
- Baseline/comparator: same-artifact compiled streaming TF32 actual-SIR route.
- Primary criterion: valid artifacts first, then predeclared failure-count classification.
- Veto diagnostics: missing/malformed artifacts, wrong metadata, missing GPU/TF32 evidence, nonfinite/residual/comparator failure, timeout.
- Nonclaims: no default readiness, no HMC readiness, no posterior correctness, no statistical ranking or failure probability.

Actions:

- Local plan check passed.
- Trusted GPU preflight selected physical GPU1.
- Launching sequential visible G1 rows with quiet logs.

Gate status: `IN_PROGRESS`

### 2026-06-24 - G1/G2 - ASSESS_GATE

Actions:

- G1 completed as `G1_SPARSE_N8192_DRIFT`: 0/8 new seeds failed paired thresholds.
- G1 result and G2 subplan passed local checks.
- G2 closed as `G2_DIAGNOSTIC_CONTINUE_TO_G3`, preserving seed `82921` as unresolved hard-case caveat.
- G3 history/memory subplan drafted for local audit before launch.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g2-scope-fallback-decision-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g3-history-memory-subplan-2026-06-24.md`

Gate status: `G2_COMPLETE_G3_PRECHECK`

### 2026-06-24 - G3 - PRECHECK

Evidence contract:

- Question: does fixed-policy Nystrom pass bounded full-history storage checks?
- Baseline/comparator: same-artifact compiled streaming TF32 actual-SIR route.
- Primary criterion: required N=1024 full-history row passes hard-veto, paired-threshold, metadata, finite-output, and history-shape checks.
- Veto diagnostics: missing/malformed artifact, wrong history shapes, metadata mismatch, nonfinite/residual/comparator failure, timeout.
- Nonclaims: no default readiness, no HMC readiness, no posterior correctness, no broad memory scalability, no acceptance of seed 82921.

Actions:

- G2/G3 local checks passed.
- Trusted GPU preflight selected physical GPU1.
- Launching required G3 full-history N=1024 row.

Gate status: `IN_PROGRESS`

### 2026-06-24 - G3 - OPTIONAL_N2048_ENTRY

Actions:

- Required G3 N=1024 full-history row passed.
- History shape audit passed for both routes.
- Trusted preflight after required row showed GPU1 with more than 8 GiB free memory.
- Launching optional N=2048 full-history row.

Gate status: `OPTIONAL_ROW_IN_PROGRESS`

### 2026-06-24 - G3/G4 - ASSESS_GATE

Actions:

- G3 required `N=1024` full-history row passed.
- G3 optional `N=2048` full-history row passed.
- G3 result written as `G3_HISTORY_MEMORY_PASS`.
- G4 gradient mechanics script added and checked.
- G4 CPU-hidden gradient mechanics smoke passed.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g3-history-memory-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g4-gradient-mechanics-result-2026-06-24.md`
- `docs/benchmarks/actual-sir-nystrom-g4-gradient-mechanics-cpu-2026-06-24.json`

Gate status:

- `G4_COMPLETE`

Next action:

- Draft G5 evidence package/default-readiness review plan; human approval is
  required for any default-policy change.
