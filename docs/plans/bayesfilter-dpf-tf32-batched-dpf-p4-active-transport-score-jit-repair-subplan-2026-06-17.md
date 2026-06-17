# Phase 4 Repair Subplan - Active Transport Score/JIT - 2026-06-17

## Phase Objective

Repair the active OT transport branch enough that a tiny streaming
relaxed-objective value+score diagnostic can compile under XLA and return
finite value+score, without changing the filtering value contract or making an
HMC/posterior correctness claim.

This is an engineering correctness repair for the active-transport score path.
It is not a performance benchmark and not a production/default-readiness gate.

## Entry Conditions Inherited From Previous Phase

- Phase 0 records `PHASE_0_PASSED`.
- Phase 1 records `PHASE_1_PASSED`.
- Phase 2 records `PHASE_2_PASSED`.
- Phase 3 records `PHASE_3_PASSED`.
- Phase 4 no-resampling score/JIT repair records
  `PHASE_4_SCORE_JIT_REPAIR_PASSED_NO_RESAMPLING`.
- Active-odd score/JIT diagnostic records
  `PHASE_4_BLOCKED_FIXABLE_ACTIVE_TRANSPORT_SCORE_JIT`.
- The active-transport score path is unpromoted.

## Required Artifacts

- Updated implementation only if needed:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- Updated focused tests only if needed:
  `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  or transport-specific tests.
- Passing or failing active-transport score/JIT JSON/Markdown/log artifacts:
  - `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.json`
  - `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.md`
  - `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-repair-2026-06-17.log`
- FP32-no-TF32 active-transport score/JIT guardrail artifact if FP64 passes.
- Loop-bound audit artifact embedded in the repair result with one row per
  reachable TensorList source:
  loop id, source location, construct type, dynamic extent, chunk size when
  applicable, derived cap, realized iterations observed on the active-odd
  fixture or equivalent symbolic proof, and `cap_bound=false`.
- Durable standalone loop-source and bound-audit artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-active-transport-loop-bound-audit-2026-06-17.md`
  This artifact must record source-search evidence for absent constructs
  (`tf.scan`, `tf.map_fn`, and AutoGraph-lowered Python loops), every reachable
  TensorList source, each bound derivation, and the `cap_bound` status.
- Pre-patch source-audit artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-active-transport-prepatch-source-audit-2026-06-17.md`
  This artifact must prove that the first active-transport score/JIT
  TensorList blocker is inside `annealed_transport_tf.py` and belongs to the
  allowed construct set before implementation begins.
- Focused test logs under `docs/benchmarks/logs/`.
- Repair result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-active-transport-score-jit-repair-result-2026-06-17.md`
- Updated execution ledger and stop handoff.
- Draft or refreshed Phase 5 subplan only if active-transport score/JIT passes.

## Required Checks, Tests, And Reviews

Local checks:

1. Confirm the pre-repair active-odd diagnostic fails with the fixed TensorList
   XLA message already recorded in the blocker result.
2. Patch only active-transport JIT blockers that are needed for the tiny score
   diagnostic:
   - add fixed `maximum_iterations` to chunk `tf.while_loop`s whose bounds are
     known from static chunk counts;
   - add fixed `maximum_iterations` to Sinkhorn loops bounded by
     `max_iterations`;
   - make diagnostics graph-safe only if they block JIT after TensorArray loop
     repair.
   If the source audit finds a JIT-reachable TensorList producer that is not a
   `tf.while_loop`/`tf.TensorArray` construct, or finds the first blocker
   outside `annealed_transport_tf.py`, stop and revise this subplan before
   widening the repair.
3. For every added `maximum_iterations`, record why the cap is non-binding for
   the loop:
   - chunk loops must use the same shape-derived number of row/column blocks as
     the loop condition;
   - Sinkhorn loops must use the existing user-specified `max_iterations`
   bound, and the stopping condition must remain unchanged.
   The result must record a per-loop audit table with derived cap, realized
   iterations or equivalent symbolic proof, and an explicit `cap_bound` flag.
   For zero extents, the convention is `ceil(0 / chunk_size) = 0`; the loop
   condition `start < extent` is false initially and the cap is non-binding.
   For positive extents, `ceil(extent / chunk_size)` is the exact number of
   updates required for `start += chunk_size` to make `start >= extent`.
4. Audit every active-transport score/JIT reachable TensorList source in
   forward or reverse mode:
   - explicit `tf.while_loop`;
   - explicit `tf.TensorArray`;
   - `tf.scan`;
   - `tf.map_fn`;
   - Python loops in TensorFlow-traced helpers that AutoGraph may lower.
   If a construct is absent from the active path, record the source-search
   evidence in the result.
   Before code edits, write the pre-patch source-audit artifact. If the first
   blocker is outside `annealed_transport_tf.py` or belongs to a construct not
   covered by this subplan, stop and revise the subplan.
5. For traced dynamic shapes, record the actual bound derivation:
   `ceil(dynamic_extent / static_chunk_size)`, implemented as
   `(dynamic_extent + chunk_size - 1) // chunk_size`, and explain why this is
   the exact iteration count for the loop update `start += chunk_size`.
   The loop-bound audit artifact must enumerate all active-path candidate
   loop/TensorList sources searched, present or absent. For any present
   construct that does not receive a new cap, the audit must state why it cannot
   create an unbounded TensorList or bind.
6. Preserve dense-vs-streaming value/score semantics on the tiny fixture.
7. Run one focused active-odd eager-vs-JIT value/score agreement check after
   repair, using the same deterministic fixture and declared tolerances.
8. Run `py_compile` on patched Python files.
9. Run focused streaming/transport tests.
10. Rerun the FP64 active-odd score/JIT diagnostic with the exact artifact
    names below; this harness explicitly compiles the score/gradient entry
    point under `tf.function(jit_compile=True)` in
    `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py::_run_arm`.
    The dense-vs-streaming structure gate is the harness `overall_passed` field
    with:
    - `structure_value_atol = 1.0e-6`;
    - `structure_value_rtol = 1.0e-6`;
    - `structure_score_atol = 1.0e-5`;
    - `structure_score_rtol = 1.0e-5`.
11. If FP64 passes, rerun FP32-no-TF32 active-odd as a precision guardrail and
    descriptive lane, not as a primary promotion criterion.
12. Run the no-resampling score/JIT guardrail again if the repair touches any
   shared transport entry point, Sinkhorn helper, or chunk-loop helper. If the
   patch is limited to a provably active-only helper, record that boundary in
   the result.
   For this planned repair, shared transport/Sinkhorn/chunk helpers are
   expected to change, so the no-resampling guardrail is mandatory.
   Passing requires exit status 0 after executing the same JIT-compiled
   score/gradient harness path, JSON `overall_passed: true`, all arms finite,
   `jit_compile: true`, and the same named value/score structure tolerances as
   the active-odd primary gate.
13. Run `git diff --check` on touched files and plan/result artifacts.

Review:

- Claude read-only review is required for this repair subplan before code
  changes because the repair touches gradient-bearing active OT code.
- Claude is not an execution authority. A review can identify inconsistencies,
  missing checks, unsafe claims, or boundary violations, but cannot authorize
  crossing human, runtime, model-file, funding, product-capability, or
  scientific-claim boundaries.
- If review finds a fixable material issue, visibly patch this subplan and run
  focused checks/review again. Stop after 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the active OT transport score path be made XLA/JIT-safe on a tiny deterministic fixture while preserving dense-vs-streaming value/score agreement? |
| Baseline/comparator | Pre-repair active-odd failure log, no-resampling score/JIT passing artifacts, and original dense tensor arm versus streaming dense/streaming/callback arms in the gradient-structure harness. |
| Primary pass criterion | The FP64 active-odd score/gradient diagnostic command below exits 0 after executing `_run_arm`'s `tf.function(jit_compile=True)` gradient call, emits JSON/Markdown, records `overall_passed: true`, all arms finite, `jit_compile: true`, dense-vs-streaming structure tolerances pass at `1.0e-6` value atol/rtol and `1.0e-5` score atol/rtol, a focused active-odd eager-vs-JIT value/score agreement check passes within declared tolerance, the no-resampling score/JIT regression command exits 0 with the same JIT/finite/overall/tolerance contract, and the repair result plus standalone loop-bound audit artifact record a complete reachable TensorList-source bound audit with every `cap_bound=false`. |
| Veto diagnostics | JIT compile failure; non-finite value or score; missing artifact; dense-vs-streaming value/score drift beyond named tolerance; active-odd eager-vs-JIT mismatch; missing reachable TensorList-source audit; missing standalone loop-bound audit artifact; missing derived cap, realized-iteration/equivalent-proof, or `cap_bound` field; any added iteration cap that can bind before the original loop condition would stop; JIT-reachable non-`tf.while_loop` TensorList producer or first blocker outside `annealed_transport_tf.py` without subplan revision; no-resampling score/JIT regression; unsupported HMC/posterior/default-readiness claim. |
| Explanatory diagnostics | Compile and warm-call time, score preview, drift table, device metadata, precision metadata, and loop-bound source inspection. |
| Not concluded | No HMC readiness, no posterior validity, no production default, no public API readiness, no active-transport finite-difference equivalence beyond the tested structure contract, no performance ranking. |
| Artifact preserving result | Repair result plus active-odd FP64/FP32 JSON/Markdown/log artifacts and focused test logs. |

Primary FP64 command/artifacts:

```bash
CUDA_VISIBLE_DEVICES=-1 TF_CPP_MIN_LOG_LEVEL=1 \
timeout 240 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --batch-size 1 \
  --time-steps 3 \
  --num-particles 8 \
  --state-dim 2 \
  --obs-dim 2 \
  --transport-policy active-odd \
  --sinkhorn-iterations 3 \
  --repeats 1 \
  --dtype float64 \
  --tf32-mode disabled \
  --structure-value-atol 1.0e-6 \
  --structure-value-rtol 1.0e-6 \
  --structure-score-atol 1.0e-5 \
  --structure-score-rtol 1.0e-5 \
  --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.json \
  --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.md \
  > docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-repair-2026-06-17.log 2>&1
```

The harness pre-parser consumes `--device-scope cpu` before TensorFlow import
and sets `CUDA_VISIBLE_DEVICES=-1`. The shell command also sets
`CUDA_VISIBLE_DEVICES=-1` explicitly for audit clarity. `--tf32-mode disabled`
records TensorFlow TF32 execution as disabled in the artifact.

Mandatory no-resampling regression command/artifacts after shared helper
changes:

```bash
CUDA_VISIBLE_DEVICES=-1 TF_CPP_MIN_LOG_LEVEL=1 \
timeout 240 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --batch-size 1 \
  --time-steps 3 \
  --num-particles 8 \
  --state-dim 2 \
  --obs-dim 2 \
  --transport-policy no-resampling \
  --sinkhorn-iterations 3 \
  --repeats 1 \
  --dtype float64 \
  --tf32-mode disabled \
  --structure-value-atol 1.0e-6 \
  --structure-value-rtol 1.0e-6 \
  --structure-score-atol 1.0e-5 \
  --structure-score-rtol 1.0e-5 \
  --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-rerun-2026-06-17.json \
  --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-rerun-2026-06-17.md \
  > docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-rerun-2026-06-17.log 2>&1
```

No-resampling pass contract:

- exit status `0`;
- JSON `overall_passed: true`;
- every arm records `finite: true`;
- every arm records `jit_compile: true`;
- value and score drift pass the same named tolerances as the primary
  active-odd command;
- log path:
  `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-rerun-2026-06-17.log`.

## Forbidden Claims And Actions

- Do not claim HMC readiness.
- Do not claim posterior correctness.
- Do not claim active-transport finite-difference correctness unless a separate
  finite-difference contract is written and passed.
- Do not claim production or public API readiness.
- Do not change TF32/default numerical policy in this repair.
- Do not add NumPy to BayesFilter-owned algorithmic implementation paths.
- Do not modify unrelated dirty worktree files.
- Do not stream TensorFlow/CUDA/benchmark JSON or logs into the session.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only after:

- repair result exists and records
  `PHASE_4_ACTIVE_TRANSPORT_SCORE_JIT_REPAIR_PASSED`;
- FP64 active-odd score/JIT artifact exists and records `overall_passed: true`;
- the FP64 active-odd artifact compiled the score/gradient entry point with
  `tf.function(jit_compile=True)`;
- focused active-odd eager-vs-JIT value/score agreement check passes within the
  declared tolerance;
- FP32-no-TF32 active-odd score/JIT guardrail artifact exists or a documented
  reason explains why it is not applicable; this lane is descriptive/guardrail
  evidence unless a later plan promotes it explicitly;
- the repair result lists every active-transport score/JIT reachable loop,
  including reverse-mode-sensitive helper loops, and records each bound source;
- the standalone loop-bound audit artifact exists and records source-search
  evidence, absent-construct evidence, bound derivations, realized
  iterations/equivalent proofs, and `cap_bound=false` rows;
- the pre-patch source-audit artifact exists and shows that the first blocker
  is inside `annealed_transport_tf.py` and in the allowed construct set;
- no added iteration cap is binding before the original loop condition would
  stop; for chunk loops this is justified by the
  `ceil(dynamic_extent / static_chunk_size)` derivation and the loop-bound
  audit table has `cap_bound=false` for every row;
- no-resampling score/JIT guardrail rerun exists and remains passing after
  shared transport/Sinkhorn/chunk helper changes;
- focused tests and `git diff --check` pass;
- Phase 5 subplan exists and keeps HMC energy/acceptance diagnostics separate
  from posterior correctness claims;
- no human-required stop condition is active.

## Stop Conditions

Stop and write a blocker result if:

- active transport cannot be made JIT-safe without changing score/value
  semantics;
- an added iteration cap would bind before the original loop condition would
  stop;
- the first JIT-reachable TensorList blocker is a non-`tf.while_loop` construct
  or outside `annealed_transport_tf.py`, unless a revised subplan explicitly
  authorizes that wider repair;
- a reachable active-transport score/JIT loop cannot be audited or bounded
  without a broader redesign;
- graph-safe diagnostics require a broad API redesign rather than a narrow
  repair;
- dense-vs-streaming value/score agreement fails after repair;
- active-odd eager-vs-JIT value/score agreement fails after repair;
- no-resampling score/JIT regresses and a local repair is not obvious;
- TensorFlow trusted context is unavailable when required;
- continuing requires package installation, network fetch, credentials,
  destructive filesystem/git action, detached execution, or default-policy
  changes.
