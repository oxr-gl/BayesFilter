# Phase 4 Subplan - JIT-Safe Score Path - 2026-06-16

## Phase Objective

Plan and repair the streaming LEDH-PFPF-OT score-gradient path so value+score
evaluation can be tested under JIT before any HMC-facing diagnostics.

This phase is about score-path engineering correctness only. It does not claim
HMC posterior validity.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result records `PHASE_0_PASSED`.
- Phase 1 result records `PHASE_1_PASSED`.
- Phase 2 result records `PHASE_2_PASSED`.
- Phase 3 result records `PHASE_3_PASSED`.
- Value-only single-GPU and row-split GPU artifacts passed finite/JIT/device
  metadata gates.
- The score path remains unpromoted.

## Required Artifacts

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-jit-safe-score-path-result-2026-06-16.md`
- Updated execution ledger entry for Phase 4.
- Any new or updated opt-in score-path code or benchmark artifacts.
- Tiny value+score correctness/JIT artifacts.
- Full command logs under `docs/benchmarks/logs/`, with stdout/stderr
  redirected rather than streamed into the chat session.
- Draft or refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p5-hmc-facing-diagnostics-subplan-2026-06-16.md`

## Required Checks, Tests, And Reviews

Local checks:

1. Identify the current score-path JIT blocker before editing code.
2. Run the smallest value+score fixture that currently demonstrates the
   blocker or passes if no blocker remains.
3. If code is changed, add or update focused tests for JIT-safe value+score.
4. Preserve FP64 and FP32-no-TF32 comparison lanes.
5. Run a tiny no-resampling finite-difference score check before any active
   transport score claim.
6. Use quiet visible execution for every TensorFlow/CUDA/benchmark command:
   predeclare log and artifact paths, redirect full stdout/stderr to the log,
   and print only bounded metadata summaries to the session.

Review:

- Claude read-only review is required if Phase 4 changes score-path code,
  changes gradient semantics, or changes the Phase 5 HMC-facing diagnostic
  scope.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the streaming relaxed-objective value+score path be made JIT-safe on tiny fixtures without changing the filtering/value contract? |
| Baseline/comparator | Current streaming value+score wrapper, fixed-branch value+score tests, no-resampling finite-difference score check, and FP64/FP32-no-TF32 lanes. |
| Primary pass criterion | Tiny value+score path runs under `tf.function(jit_compile=True)`, returns finite value and score, preserves no-resampling finite-difference agreement, and records precision metadata. |
| Veto diagnostics | Non-finite score; JIT compile failure; missing finite-difference guardrail; active-transport score finite-difference equivalence claim without evidence; changed value semantics; missing precision lane; unsupported HMC claim. |
| Explanatory diagnostics | Compile time, gradient norm, per-component precision drift, active-transport finite behavior, and source diagnostics. |
| Not concluded | No HMC readiness, no posterior validity, no production default, no public API readiness, no active-transport score correctness beyond the tested contract. |
| Artifact preserving result | Phase 4 result plus tiny value+score JSON/Markdown artifacts. |

## Quiet Execution Contract

Phase 4 must not stream full TensorFlow, CUDA, benchmark, or JSON output into
the chat session.

Before each command, record:

- log path under `docs/benchmarks/logs/`;
- JSON/Markdown artifact path;
- pass/fail fields to summarize after completion.

Use this shell shape:

```bash
mkdir -p docs/benchmarks/logs
timeout <seconds> <command> > docs/benchmarks/logs/<run-name>.log 2>&1
```

After completion, summarize only:

- exit status;
- artifact paths;
- finite/JIT/device/precision pass fields;
- last 20-40 log lines only on failure.

Full logs must be referenced from the Phase 4 result.

## Skeptical Audit Before Execution

Before running Phase 4 commands, check:

- wrong baseline: score path must compare against score-specific fixtures, not
  value-only GPU success;
- proxy metric risk: finite score is not HMC validity;
- missing stop condition: JIT failure, non-finite score, or finite-difference
  failure must block;
- unfair comparison: precision drift needs matched seed/fixture and explicit
  comparator;
- hidden assumption: relaxed-objective gradient is not categorical PF gradient;
- stale context: inspect current score code before repair;
- environment mismatch: GPU score diagnostics require trusted context;
- artifact adequacy: result must record score semantics and nonclaims.
- stream stability: commands that may emit large output must use log
  redirection and bounded summaries.

## Forbidden Claims And Actions

- Do not claim HMC readiness in Phase 4.
- Do not claim categorical particle-filter gradient correctness.
- Do not claim active-transport finite-difference equivalence unless the exact
  tested contract supports it.
- Do not change production defaults or public APIs.
- Do not modify unrelated dirty worktree files.
- Do not stream full benchmark JSON or TensorFlow logs into the session window.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only after:

- Phase 4 result exists and records `PHASE_4_PASSED`;
- tiny value+score JIT artifact exists with finite value and score;
- no-resampling finite-difference score guardrail passes or a blocker explains
  why it cannot;
- precision metadata and reference lanes are preserved;
- Phase 5 subplan exists and states HMC energy/acceptance diagnostics as
  diagnostics, not automatic proof of posterior correctness;
- no human-required stop condition is active.

## Stop Conditions

Stop and write a blocker result if:

- current score path cannot be made JIT-safe without changing score semantics;
- no-resampling finite-difference score guardrail fails without a local repair;
- TensorFlow/GPU trusted context is unavailable when required;
- continuing requires package installation, network fetch, credentials,
  destructive filesystem/git action, detached execution, or production default
  changes.
