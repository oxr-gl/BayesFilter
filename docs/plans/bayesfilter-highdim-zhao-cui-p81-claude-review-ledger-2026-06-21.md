# P81 Claude Review Ledger

status: PHASE9_SUBPLAN_REVIEWED_READY
date: 2026-06-21

## Review Protocol

Claude Opus is read-only reviewer.  Review packets must be bounded summaries
with paths and concise excerpts, not whole-file dumps.  Claude cannot authorize
execution, GPU use, default changes, scientific claims, or boundary crossings.

Each material review asks Claude to check:

- wrong baseline or comparator;
- proxy metric promoted as correctness;
- horizon-0 boundary overclaim;
- unsupported source-faithfulness claims;
- missing artifacts or tests;
- unsafe runbook continuation;
- whether Phase 4 is justified by Phase 3 evidence.

## Reviews

### Round 1

The first prompt hung without output.  A small `PROBE_OK` prompt returned, so
the issue was prompt shape rather than Claude availability.

### Round 2

Verdict: `BLOCK`.

Required fixes:

1. Qualify or replace overbroad analytical wording.
2. Add an explicit evidence limitation for the horizon-0 engineering smoke.
3. Add run-manifest/artifact references for the reported passes.
4. Tighten Phase 4 GPU continuation with trusted `nvidia-smi` and TensorFlow
   device-probe logs.
5. State Phase 4 pass/veto criteria around bounded horizon-0 behavior, branch
   stability, tolerance failure, OOM, and one-row boundary.

Patch status: applied; Round 3 pending.

### Round 3

Verdict: `AGREE`.

Claude agreed that the R2 block items were fixed: fixed-branch/JVP-backed
wording replaced overbroad analytical claims, the horizon-0 one-row engineering
scope and non-claims are explicit, run manifest and branch-hash evidence are
present, and Phase 4 now requires trusted/escalated GPU preflight with concrete
bounded pass/veto criteria.

### Phase 4 Execution Review

Verdict: `AGREE`.

Guardrails:

- Scope result as trusted GPU-visible backend feasibility for the Phase 3
  candidate at one-row horizon-0.
- Preserve non-claims: no full likelihood correctness, LEDH agreement, HMC
  readiness, posterior/scientific validity, source-faithfulness, scaling, or
  default readiness.
- Cite GPU evidence only because `nvidia-smi`, TensorFlow GPU probe, and both
  GPU-visible pytests were trusted/escalated.
- Treat plugin-registration and TFP warnings as observed but non-vetoing only
  for this backend-feasibility question.
- Phase 5 is justified only as drafting/reviewing a new subplan.

### Phase 5 Subplan Review

Round 1 verdict: `BLOCK`.

Claude agreed the core scientific guardrails were present but blocked on
artifact/test completeness: the Phase 5 result needed a decision table, run
manifest, and skeptical-audit pass/fail note, and the Phase 6 target tests/files
needed to be concrete.

Patch status: applied to
`docs/plans/bayesfilter-highdim-zhao-cui-p81-phase5-full-history-score-surface-subplan-2026-06-21.md`.

Round 2 verdict: `AGREE`.

Claude agreed the previous blocker was resolved.  Phase 5 execution and Phase 6
subplan drafting proceeded under the audit-only boundary.

### Phase 5 Result And Phase 6 Subplan Review

Verdict: `AGREE`.

Claude agreed the Phase 5 result identified the missing surface, preserved
non-claims, and the Phase 6 subplan was bounded with tiny regression first and
no LEDH/P8p comparison.

### Phase 6 Execution Result And Phase 7 Subplan Review

Verdict: `AGREE` on the Phase 6 conclusion and Phase 7 direction.

Claude agreed that the d=2 two-row regression supports only tiny wiring, while
the SIR d=18 two-row all-grid route is blocked by
`O(N_current * N_previous * d)` transition scaling and must be handled by a
scaling-blocker audit/design phase rather than LEDH/P8p comparison.

Pre-execution fixes requested and patched in the Phase 7 subplan:

1. Preserve a fail-fast preallocation guard and record its formula/threshold.
2. Require a quantitative route artifact: peak bytes, chunk size, chunk count,
   and asymptotic runtime.
3. Require Phase 8 readiness tests covering the unbounded-route gate, tiny d=2
   regression, and bounded d=18 two-row smoke without materializing all pairs.

### Phase 7 Result And Phase 8 Subplan Review

Round 1 verdict: `BLOCK`.

Claude found Phase 8 governance was too permissive in ways that could lead to
wrong continuation:

1. Phase 9 comparator readiness could not depend on a d=18 two-row smoke.
2. A bounded d=18 smoke could not establish d=18 full-history correctness.
3. The chunk memory guard priced only tiled point tensors and needed a
   conservative summed/safety-multiplied peak bound.
4. The optional d=18 smoke needed an exact subset/timing-probe mode and hard
   timeout/chunk-product aborts.
5. Phase 8 needed an integration test proving the streaming path is actually
   exercised, not only helper-level parity.
6. Tiny dense-vs-streaming parity needed to be scoped as implementation
   evidence only.

Patch status: applied to
`docs/plans/bayesfilter-highdim-zhao-cui-p81-phase8-streamed-transition-prototype-subplan-2026-06-21.md`.

Round 2 verdict: `AGREE`.

Claude agreed the patched subplan fixed the wrong-baseline, proxy-promotion,
unsafe d=18 budget, memory-guard, artifact/test-coverage, stop-condition, and
boundary non-claim issues.

### Phase 8 Execution Result And Phase 9 Subplan Review

Verdict: `AGREE`.

Claude agreed that Phase 8's baseline, proxy-metric boundaries, code chunk
product gate, non-claims, evidence artifacts, and tests match the claimed
scope.  Claude also agreed that Phase 9 is correctly framed as a read-only
representation/scaling phase rather than LEDH/P8p comparison, and did not find
a missing concrete fix before Phase 9 execution.

Reviewed artifacts:
`docs/plans/bayesfilter-highdim-zhao-cui-p81-phase7-d18-transition-scaling-blocker-result-2026-06-21.md`
and
`docs/plans/bayesfilter-highdim-zhao-cui-p81-phase8-streamed-transition-prototype-subplan-2026-06-21.md`;
plus:
`docs/plans/bayesfilter-highdim-zhao-cui-p81-phase8-streamed-transition-prototype-result-2026-06-21.md`
and
`docs/plans/bayesfilter-highdim-zhao-cui-p81-phase9-representation-scaling-subplan-2026-06-21.md`.

### Phase 9 Result And Phase 10 Subplan Review

Round 1 prompt attempts:

- First broad review prompt hung with no output and was interrupted.
- A small read-only probe returned `PROBE_OK`, so Claude availability was
  confirmed and the prompt was redesigned.
- A shorter file-inspection prompt also hung and was interrupted.
- A minimal gate review prompt eventually returned a substantive review.

Round 1 verdict: `BLOCK`.

Claude agreed the transition-mean signature issue is real, but found the Phase
10 subplan too narrow because the local route also assumes direct access to
`process_covariance`, `neighbor_sets`, and `_rk4_substeps`.  The
`ParameterizedZhaoCuiSIRSSM` wrapper exposes these through `base_model` or
`scaled_model(theta)`, not as direct fields.  The subplan was patched to require
a small route-accessor layer for theta-independent route metadata and a
theta-dependent transition-mean path for derivatives.

Round 2 verdict: `AGREE`.

Claude found no further material blocker before implementation after the
route-accessor patch.  One implementation caution was recorded: dispatch should
be wrapper-aware and should raise on unknown wrappers rather than guessing only
from `parameter_dim()`.

### Phase 10 Execution Result And Phase 11 Subplan Review

Verdict: `AGREE`.

Claude agreed that the wrapper-aware helper is materially correct for the Phase
10 claim: theta-independent route structure is read from the base structural
model, while transition means use the theta-dependent parameterized wrapper.
Claude also agreed that the new tests exercise nonzero-theta coordinate factors,
dense transition/predictive value parity, and theta-gradient parity.

Claude found no d=18, LEDH, source-faithful, HMC/posterior/default, or
production overclaim in the Phase 10 result.  Claude also agreed that the Phase
11 evidence contract and stop conditions are tight enough for a read-only
route-selection phase.

Non-blocking note: the new tests establish the stated tiny-fixture
parameterized claim, not broad generic-wrapper polymorphism.

### Phase 11 Result And Phase 12 Subplan Review

Round 1 verdict: `BLOCK`.

Claude agreed that blocking direct implementation is justified and that Phase
12 is correctly scoped as read-only derivation/design.  Claude blocked because
Phase 12 allowed approximate routes to be selected with only
exact/approximation status and lower-rung tests, but did not require an
explicit approximation/error contract.  The subplan was patched to require an
approximation/error contract and claim limits in the result contents, veto
diagnostics, Phase 13 handoff conditions, and stop conditions.

Round 2 verdict: `AGREE`.

Claude agreed the approximation/error-contract blocker was resolved and found no
remaining material blocker before Phase 12 read-only execution.

### Phase 12 Result Review

Verdict: `AGREE`.

Claude agreed that the Phase 12 blocker is substantively justified and that
stopping P81 pending a lane decision is correct.  Claude found no major
overclaim or missing artifact.  Non-blocking wording note: absolute "no
implementation" statements should be scoped to "not found in audited paths"
unless a wider repo audit is run.  The Phase 12 result was patched accordingly.
