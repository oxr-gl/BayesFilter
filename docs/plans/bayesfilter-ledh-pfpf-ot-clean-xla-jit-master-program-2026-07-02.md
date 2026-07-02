# Clean XLA JIT Master Program

Date: 2026-07-02

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Role Contract

Codex is supervisor and executor.  Claude Opus is a read-only reviewer only.
Claude may inspect bounded paths and return `VERDICT: AGREE` or
`VERDICT: REVISE`, but it cannot edit files, run experiments, authorize
scientific claims, authorize runtime boundary crossings, or change this
program.

## Program Objective

Repair the LEDH-PFPF-OT corrected full total-derivative route so the compiled
GPU/XLA code is clean: dynamic loops are represented as TensorFlow/XLA loops,
not as large Python-unrolled graphs.  Then add tests that mechanically detect
unclean compiled-path code before future agents can call it "XLA clean".

## Clean-XLA Definition

For the score-bearing corrected full total-derivative route, "clean XLA" means:

- time recursion is represented with `tf.while_loop` or an equivalent
  TensorFlow loop in the compiled function;
- reverse recursion is represented with `tf.while_loop`, not
  `reversed(records)` over Python lists;
- forward records needed by the reverse pass are stored in TensorFlow state,
  typically `TensorArray`, not Python lists of tensors;
- RK4 substeps in the SIR transition and its VJP are represented by TensorFlow
  loop state, not Python-unrolled loops;
- fixed randomness is supplied as tensors, not generated in seed-by-seed Python
  loops inside the compiled function;
- finite Sinkhorn iteration loops in the streaming full route are represented
  by TensorFlow loop state, not Python `for _ in range(steps)` inside the
  compiled path;
- the corrected full route computes the total derivative of the executed
  finite-Sinkhorn scalar; stopped partial derivatives must not be called the
  score.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the corrected LEDH-PFPF-OT full total-derivative route be made clean for GPU/XLA compilation, with tests that detect Python-unrolled compiled-path regressions? |
| Baseline/comparator | Current 2026-07-01 corrected full route, which passed numerical direction checks but has compiler hygiene problems. |
| Primary pass criterion | Static guardrails pass, HLO/compiler-size gates show loop representation instead of graph unrolling, GPU/XLA smoke passes, same-scalar FD sentinel passes, and material validation remains consistent with the 2026-07-01 result. |
| Veto diagnostics | Hidden stopped partial derivative in the score route, Python list/time/reverse/RK4/Sinkhorn unrolling in the compiled route, non-GPU or non-XLA execution for GPU gates, nonfinite objective/gradient/MCSE, HLO size scaling like unrolled time, same-scalar FD failure, or Claude/Codex review nonconvergence. |
| Explanatory diagnostics | Cold compile+first-call time, warm-call time, HLO text/op size, while-op count, memory, route metadata, FD slope errors, and MCSE. |
| Not concluded | No posterior correctness, no exact nonlinear likelihood correctness, no production HMC readiness, no validation of every model family, and no claim that the historical stopped route is a score. |
| Artifacts | This master program, phase subplans/results, visible runbook, execution ledger, Claude review ledger, stop handoff, static audit JSON, HLO/compile metrics JSON, validation JSON/markdown. |

## Approval And Boundary Needs

The following approvals are required for smooth execution and are treated as
covered by the user's standing instruction unless the sandbox reviewer denies a
specific command:

- Claude Code bounded read-only review through
  `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh` with
  trusted/escalated permissions.
- Trusted GPU/CUDA/TensorFlow/XLA commands, including device probes,
  HLO/compiler diagnostics, and GPU benchmark smoke tests.
- Scoped edits under this repository to `docs/plans`, `scripts`, `tests`,
  `docs/benchmarks`, and the relevant TensorFlow implementation files.

This program does not request package installation, network data fetches,
destructive git operations, broad filesystem mutation, detached nested Codex
agents, or production/default-policy changes.  If any of those become
necessary, Codex must stop and ask.

## Phase Index

| Phase | Name | Objective | Subplan | Required result |
| --- | --- | --- | --- | --- |
| 0 | Inventory And Target Freeze | Identify current unclean compiled-path surfaces and freeze the exact clean-XLA target. | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-subplan-2026-07-02.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-result-2026-07-02.md` |
| 1 | Static Guardrails | Add a static audit that detects Python-unrolled compiled-path patterns and score-bearing stop-gradient misuse. | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-subplan-2026-07-02.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-result-2026-07-02.md` |
| 2 | Fixed Randomness Tensorization | Move seed/time noise generation out of the compiled manual route into fixed tensors. | TBD before execution | TBD |
| 3 | RK4 Loop Hygiene | Replace SIR RK4 forward and reverse Python substep loops with TensorFlow loop state. | TBD before execution | TBD |
| 4 | Manual Scan Hygiene | Replace manual forward/reverse Python time scans and Python record lists with `tf.while_loop`/`TensorArray`. | TBD before execution | TBD |
| 5 | Streaming Sinkhorn Loop Hygiene | Replace streaming finite Sinkhorn full-route Python step loops with TensorFlow loops and preserve total derivative semantics. | TBD before execution | TBD |
| 6 | Compiler Metrics Gate | Add HLO/compiler-size/timing diagnostics proving loop representation and bounded scaling. | TBD before execution | TBD |
| 7 | Numerical Validation | Rerun same-scalar FD sentinel, LGSSM entry check, and SIR GPU/XLA validation gates. | TBD before execution | TBD |
| 8 | Closeout | Decide final status and remaining nonclaims. | TBD before execution | TBD |

## Repair Loop

For each phase, Codex must:

1. read the phase subplan;
2. run a skeptical pre-execution audit;
3. execute only the scoped work in the subplan;
4. run required local checks;
5. write a phase result/close record;
6. draft or refresh the next subplan;
7. send material plans/results to Claude read-only review;
8. repair visibly when review finds a fixable problem;
9. stop after five Claude rounds for the same blocker.

## Skeptical Launch Audit

Result: `PASS_TO_CLAUDE_REVIEW_BEFORE_PHASE0`

- Wrong baseline: avoided by naming the current 2026-07-01 corrected full route
  as the numerical baseline and clean-XLA as a separate engineering target.
- Proxy metric risk: avoided by making HLO/static/timing gates compiler
  hygiene evidence only, not scientific correctness evidence.
- Missing stop conditions: phase subplans must stop on unclean compiled-path
  patterns, numerical mismatches, wrong route metadata, or review
  nonconvergence.
- Unfair comparison: validation phases must use same scalar, route, seeds,
  theta, dtype, and GPU/XLA policy as stated in their subplans.
- Hidden assumptions: the program explicitly separates "XLA compiled" from
  "clean XLA".
- Environment mismatch: GPU/CUDA and Claude commands require trusted/escalated
  execution.
- Artifact mismatch: every phase has a required result artifact and a next
  handoff condition.

## Forbidden Claims

Until Phase 8 explicitly closes them, the following claims are forbidden:

- the route is production HMC ready;
- the nonlinear particle-filter score is exact;
- posterior correctness is established;
- every model family is validated;
- a stopped partial derivative is a score;
- a short smoke test proves clean XLA;
- an HLO loop-count proxy proves scientific correctness.
