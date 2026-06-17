# Phase 4 Repair Subplan - Score JIT TensorArray Repair - 2026-06-16

## Phase Objective

Repair the streaming relaxed-objective value+score path so a tiny
no-resampling score diagnostic can compile with XLA.

The suspected blocker is TensorArray/tensor-list state in gradient-bearing
`tf.while_loop` paths. The first repair target is the likelihood-only
`return_history=False` path.

## Entry Conditions Inherited From Previous Phase

- Phase 4 result records `PHASE_4_BLOCKED_FIXABLE_SCORE_JIT`.
- Value-only streaming JIT passed in earlier phases.
- HMC-facing diagnostics are blocked until score JIT is repaired.
- Full command output must be redirected to logs under `docs/benchmarks/logs/`.

## Required Artifacts

- This repair subplan.
- Patched streaming implementation and focused tests if needed.
- Quiet logs under `docs/benchmarks/logs/`.
- Score/JIT JSON/Markdown artifacts under `docs/benchmarks/`.
- Repair result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-score-jit-repair-result-2026-06-16.md`

## Required Checks, Tests, And Reviews

Local checks:

1. Patch only the streaming score/JIT path and adjacent tests.
2. Add fixed `maximum_iterations` to relevant `tf.while_loop` calls when static
   loop counts are known.
3. Avoid carrying history TensorArrays through the `return_history=False`
   gradient-bearing value path.
4. Run the tiny FP64 no-resampling score/JIT diagnostic quietly.
5. Run focused pytest for streaming DPF tests quietly.
6. Run `git diff --check`.

Review:

- Claude review is not required for this small local repair unless the fix
  changes score semantics, transport semantics, or Phase 5 scope.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a focused TensorArray/loop repair make the tiny no-resampling streaming score path XLA/JIT-safe without changing value semantics? |
| Baseline/comparator | The failing Phase 4 log and current streaming value/score tests. |
| Primary pass criterion | The tiny FP64 no-resampling score/JIT diagnostic exits 0, emits finite value/score artifacts, and focused streaming tests pass. |
| Veto diagnostics | JIT compile failure persists; non-finite value/score; no-resampling finite-difference score regression; value parity regression; unsupported HMC claim. |
| Explanatory diagnostics | Compile time, warm-call time, score values, and source diagnostics. |
| Not concluded | No active-transport score correctness, no HMC readiness, no posterior validity, no production/public API readiness. |
| Artifact preserving result | Repair result plus logs and JSON/Markdown artifacts. |

## Forbidden Claims And Actions

- Do not claim HMC readiness.
- Do not claim categorical PF score correctness.
- Do not change production defaults or public APIs.
- Do not modify unrelated dirty worktree files.
- Do not stream full TensorFlow logs or benchmark JSON into the session.

## Exact Next-Phase Handoff Conditions

The main Phase 4 gate may continue only after:

- repair result records pass or blocker;
- tiny score/JIT diagnostic is either passing or a sharper blocker is recorded;
- focused tests/checks are recorded;
- no HMC-facing diagnostics have been run from value-only evidence.

## Stop Conditions

Stop and write a blocker result if:

- the score path cannot be made JIT-safe without changing semantics;
- focused tests fail in a way that is not local to the repair;
- TensorFlow diagnostic commands cannot run in trusted/quiet mode;
- repair would require a broader redesign, package install, destructive git
  action, or unrelated worktree edits.
