# Phase 0 Subplan: Inventory And Target Freeze

Date: 2026-07-02

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Identify the current unclean compiled-path surfaces and freeze the exact
clean-XLA target before any code refactor.  Phase 0 is an inventory and
definition phase only.

## Entry Conditions Inherited From Previous Phase

- User requested a master program with gated subplans and Claude read-only
  review.
- Master program and visible runbook exist in `docs/plans`.
- Current known baseline: corrected full total-derivative route passed the
  2026-07-01 same-scalar raw-direction gate but has long XLA compile time and
  Python-unrolled compiled-path surfaces.

## Required Artifacts

- Phase 0 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-subplan-2026-07-02.md`
- Phase 0 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-result-2026-07-02.md`
- Phase 1 draft subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-subplan-2026-07-02.md`
- Updated execution ledger and Claude review ledger.

## Required Checks, Tests, Reviews

- Local inventory command over the current compiled-path files:
  - `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  - `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- CPU-hidden focused static tests that already exist for while-loop hygiene,
  if their names are discoverable without changing code.
- Claude read-only review of this subplan before execution and of the Phase 1
  subplan before handoff.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exactly is unclean in the current compiled path, and what must later phases repair? |
| Baseline/comparator | Current source tree; no code changes in Phase 0. |
| Primary pass criterion | Inventory identifies concrete file/line surfaces for time-scan unrolling, reverse-scan unrolling, record-list tensor storage, seed-loop randomness, RK4 substep unrolling, streaming Sinkhorn step unrolling, and score-bearing stop-gradient risks. |
| Veto diagnostics | Missing target files, inability to inspect sources, unsupported claim that current code is clean, or Phase 1 handoff without concrete forbidden patterns. |
| Explanatory diagnostics | Existing tests that already assert `tf.while_loop` in nearby routes. |
| Not concluded | No code is fixed; no performance improvement; no numerical correctness claim; no production readiness claim. |
| Artifact | Phase 0 result markdown with target table and next-phase exact guardrail requirements. |

## Forbidden Claims And Actions

- Do not claim any compiler issue is fixed in Phase 0.
- Do not edit implementation code in Phase 0.
- Do not run long GPU benchmarks in Phase 0.
- Do not treat existing `tf.while_loop` in the value core as proof that the
  manual score path is clean.
- Do not call stopped partial derivatives scores.

## Exact Next-Phase Handoff Conditions

Phase 0 may hand off to Phase 1 only if:

- the inventory result names concrete forbidden patterns;
- the clean-XLA definition is frozen in plain language;
- the Phase 1 subplan states exact static-audit artifacts and tests;
- Claude read-only review of the Phase 1 subplan returns `VERDICT: AGREE`, or
  any `VERDICT: REVISE` has been patched and rereviewed.

## Stop Conditions

Stop and write a blocker result if:

- Claude and Codex do not converge after five rounds on this subplan;
- required source files cannot be read;
- the inventory cannot identify concrete surfaces;
- Phase 1 would require broad policy changes, package installation, detached
  execution, or unrelated file edits.

## Skeptical Pre-Execution Audit

Result: `PASS_PENDING_CLAUDE_REVIEW`

- Wrong baseline: avoided by inventorying current source, not comparing
  runtime claims.
- Proxy promotion: avoided because Phase 0 cannot pass any compiler-cleanliness
  implementation claim.
- Missing stop conditions: explicit above.
- Unfair comparison: no comparisons are made in Phase 0.
- Hidden assumption: separates clean value core from unclean manual score path.
- Environment mismatch: CPU-hidden static tests only; no GPU evidence in
  Phase 0.
- Artifact mismatch: Phase 0 result must contain line-anchored surfaces and
  exact Phase 1 guardrail requirements.
