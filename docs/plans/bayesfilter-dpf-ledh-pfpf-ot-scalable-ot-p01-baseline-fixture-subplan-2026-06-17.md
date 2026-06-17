# Phase 1 Subplan: Baseline Fixture Contract

Date: 2026-06-17

## Phase Objective

Define deterministic transport fixtures and record dense/streaming baseline
diagnostics from the current TensorFlow FilterFlow-style annealed transport.
These baseline artifacts become the comparator for every scalable OT candidate.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result records `PHASE_0_GOVERNANCE_PASSED`.
- Master program, visible runbook, execution ledger, stop handoff, and this
  Phase 1 subplan exist.
- Claude Phase 0 review artifact ends with `VERDICT: AGREE`.
- Source-lock result records Mini-batch/BoMb as blocked for decision-grade use
  until clean source is available.
- No human-required stop condition is active.

## Required Artifacts

- Fixture specification:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-spec-2026-06-17.md`
- Baseline diagnostic JSON:
  `docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.json`
- Baseline diagnostic log:
  `docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.log`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-result-2026-06-17.md`
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-candidate-audit-notes-subplan-2026-06-17.md`

## Required Checks, Tests, And Reviews

Local checks:

1. Inspect current baseline signatures in
   `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
2. Create or identify a deterministic baseline-fixture diagnostic command that
   uses CPU-only TensorFlow unless a trusted GPU plan is separately approved.
3. Run tiny manually inspectable fixture with `B=1,N<=8,D<=3`.
4. Run small dense-reference parity fixture with `B=2,N<=32,D<=5`.
5. Run one synthetic high-dimensional fixture with configurable low-rank or
   locality structure, sized small enough for a baseline diagnostic, not a
   performance claim.
6. For each fixture, record dense and streaming results or explicitly record why
   streaming cannot provide a dense plan object.
7. Record finite checks, row residual, column residual, transported-particle
   norm, dense-vs-streaming transported-particle error, runtime, dtype, device,
   seed, command, and artifact paths.
8. Run focused tests or import checks sufficient to validate the diagnostic
   script and baseline result schema.

Review:

- Claude review is required if this phase creates or changes baseline
  diagnostic code, changes tolerances, or changes phase handoff criteria.
- Claude review may be skipped only if the phase writes fixture/result docs and
  uses existing tests/scripts unchanged; the Phase 1 result must justify the
  skip.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the current TensorFlow dense/streaming annealed transport baseline deterministic and diagnostically rich enough to compare scalable OT candidates? |
| Baseline/comparator | `annealed_transport_tf.py` dense mode and streaming mode. Dense mode is the materialized matrix reference; streaming mode is the memory-saving current implementation. |
| Primary pass criterion | Baseline fixtures write a JSON/MD artifact with finite transported particles, deterministic fixture metadata, dense and streaming diagnostics, and explicit dense-vs-streaming comparison where applicable. |
| Veto diagnostics | Nonfinite output; missing fixture seed/config; missing dense baseline; invalid residual computation; streaming drift not explained; runtime-only artifact; GPU/trusted-context claim without approved plan. |
| Explanatory diagnostics | Runtime, memory proxy, row/column residuals, transported-particle norm/error, cost scale, iteration count, fixture rank/locality. |
| Not concluded | No scalable candidate correctness, no speedup, no posterior validity, no production default, no statistically supported ranking. |
| Artifact preserving result | Fixture spec, JSON diagnostics, log, Phase 1 result, and ledger entry. |

## Skeptical Plan Audit

- Wrong baseline: use current `annealed_transport_tf.py`; do not use external
  libraries as baseline.
- Proxy metric risk: runtime is explanatory until finite transport and
  residual diagnostics pass.
- Missing stop conditions: nonfinite outputs, missing dense fixture, and missing
  result artifacts stop the phase.
- Unfair comparisons: no candidate is compared in this phase.
- Hidden assumptions: dtype, device, seeds, fixture definitions, and transport
  modes must be recorded.
- Stale context: inspect the baseline code before creating fixtures.
- Environment mismatch: default to CPU-only unless a separate trusted GPU plan
  is approved.
- Artifact adequacy: JSON diagnostics plus result note answer the baseline
  fixture question.

Skeptical audit status: `PASSED_FOR_PHASE_1_BASELINE_PLAN`.

## Forbidden Claims And Actions

- Do not implement or rank scalable OT candidates in this phase.
- Do not change production defaults or public APIs.
- Do not use GPU evidence unless a trusted GPU plan is reviewed and approved.
- Do not relax tolerances after seeing output without writing a blocker note
  and obtaining review.
- Do not treat streaming runtime as a scalable algorithm victory; it is the
  current baseline.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only after:

- Phase 1 result records `PHASE_1_BASELINE_FIXTURE_PASSED`;
- fixture spec, JSON diagnostics, and log exist;
- dense baseline outputs exist for required fixtures;
- streaming diagnostics are recorded or an explicit non-materialization reason
  is recorded;
- local checks pass;
- Phase 2 candidate-audit-notes subplan exists and has been reviewed locally for
  consistency, correctness, feasibility, artifact coverage, and boundary safety;
- any required Claude review has converged to `VERDICT: AGREE`.

## Stop Conditions

Stop and write/update the stop handoff if:

- baseline code cannot be imported in the available environment;
- dense baseline fixture emits nonfinite output;
- fixture determinism cannot be guaranteed;
- required artifacts cannot be written;
- running the necessary diagnostic would require package installation, network
  fetch, destructive action, or unapproved GPU/trusted-context execution;
- review does not converge after five rounds for the same blocker.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 1 result/close record.
3. Draft or refresh the Phase 2 candidate-audit-notes subplan.
4. Review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
