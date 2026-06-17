# Batched LEDH-PFPF-OT Visible Execution Ledger

Date: 2026-06-15

## Status

`ACTIVE_PHASE_0_PRECHECK`

## Ledger

### 2026-06-15T03:26:00+08:00 - Plan Review - PRECHECK

Evidence contract:

- Question: Can Codex launch Phase 0 visibly under the gated program?
- Baseline/comparator: Master program, visible runbook, launch plan, and Phase
  0/1 subplans.
- Primary criterion: Claude read-only review converges or fixable issues are
  patched before Phase 0 execution.
- Veto diagnostics: Wrong baseline, proxy metrics as correctness, missing stop
  conditions, unsupported claim, boundary mismatch, or Claude nonconvergence.
- Non-claims: No implementation correctness, no batching success, no score
  correctness, no GPU claim, no production readiness.

Skeptical audit:

- Wrong baseline: Guarded; Phase 0 must inventory scalar LEDH-PFPF-OT before
  implementation.
- Proxy metric risk: Guarded; finite values and speed remain explanatory unless
  declared as phase criteria.
- Missing stop condition: Guarded by human-required stops and five-round Claude
  cap.
- Unfair comparison: Guarded; Phase 0 must concretize comparator, seed policy,
  and parity tolerances before Phase 1.
- Hidden assumption: Guarded; score is for the relaxed objective only.
- Stale context: Guarded; Phase 0 reruns repo/test inventory.
- Environment mismatch: Guarded; CPU TensorFlow import is a Phase 0 check.
- Artifact adequacy: Passed; phase result/review artifacts are named.

Actions:

- Ran Claude read-only review through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.
- First path-based review and one narrow retry did not produce a usable verdict.
- Ran a small read-only Claude probe; response was `PROBE_OK`.
- Retried with digest-bounded read-only prompt.
- Claude returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-claude-review-round-01-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-visible-gated-overnight-execution-plan-2026-06-15.md`

Gate status:

- `PASSED`

Next action:

- Start Phase 0 `PRECHECK` and run inventory/local checks.

### 2026-06-15T03:30:36+08:00 - Phase 0 - ASSESS_GATE

Evidence contract:

- Question: Are the current scalar LEDH-PFPF-OT baseline, determinism needs,
  graph blockers, and file boundaries clear enough to begin batch contract
  implementation?
- Baseline/comparator: Existing scalar `run_ledh_pfpf_ot_tf`,
  `ledh_flow_batch_tf`, and `annealed_transport_resample_tf`.
- Primary criterion: Inventory records scalar paths, blockers, available
  tests/imports, dirty-worktree state, and Phase 1 handoff.
- Veto diagnostics: Missing TensorFlow env; no runnable scalar import/smoke;
  missing scalar baseline; conflicting dirty work; Claude nonconvergence.
- Non-claims: No batching correctness, no score correctness, no GPU result, no
  production readiness.

Skeptical audit:

- Wrong baseline: Passed; scalar LEDH-PFPF-OT and transport paths identified.
- Proxy metric risk: Passed; tiny scalar smoke is diagnostic only.
- Missing stop condition: Passed; no Phase 0 stop condition fired.
- Unfair comparison: Guarded; Phase 1 now inherits fixed noise, fixed branch
  mask, and tolerance policy.
- Hidden assumption: Guarded; relaxed fixed-branch objective only.
- Stale context: Passed; inventory reran on current repo.
- Environment mismatch: Passed for CPU import; CUDA warning recorded as
  environment note, not GPU evidence.
- Artifact adequacy: Passed; Phase 0 result written.

Actions:

- Ran repo status, scalar/blocker `rg`, test inventory, CPU TensorFlow import,
  scalar import smoke, tiny scalar execution smoke, heading checks, and
  historical-contract inventory.
- Refreshed Phase 1 subplan with comparator, seed/noise, branch, and tolerance
  handoff.

Artifacts:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p0-inventory-contract-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p1-shape-contract-subplan-2026-06-15.md`

Gate status:

- `PASSED`

Next action:

- Locally review refreshed Phase 1 subplan, then begin Phase 1 `PRECHECK` if no
  consistency or boundary issue is found.

### 2026-06-15T03:38:05+08:00 - Phase 1 - ASSESS_GATE

Evidence contract:

- Question: Does the experimental API express the batched LEDH-PFPF-OT contract
  without changing semantics or production exports?
- Baseline/comparator: Phase 0 scalar path inventory and existing experimental
  batched value+score shape conventions.
- Primary criterion: Shape tests and import smoke pass; deterministic
  fixed-contract fixture is explicit; no public API/default change.
- Veto diagnostics: Ambiguous callback shape, hidden RNG, missing fixed branch
  mask, public export drift, missing deterministic noise contract, or missing
  tolerance policy.
- Non-claims: No scalar value parity, no full recursion, no score correctness,
  no performance claim.

Skeptical audit:

- Wrong baseline: Passed; Phase 1 contract inherits scalar comparator from
  Phase 0.
- Proxy metric risk: Passed; shape/import checks are only Phase 1 criteria.
- Missing stop condition: Passed; no Phase 1 stop condition fired.
- Unfair comparison: Guarded; fixed inputs and masks are required before later
  parity.
- Hidden assumption: Guarded; no categorical PF gradient claim.
- Stale context: Passed; new files created only under experimental/test paths.
- Environment mismatch: Passed for CPU-only focused pytest.
- Artifact adequacy: Passed; Phase 1 result and refreshed Phase 2 subplan
  written.

Actions:

- Added experimental shape-contract module and focused tests.
- Ran focused CPU-only pytest: 6 passed.
- Ran source/export/check-focused validations.
- Refreshed Phase 2 subplan.

Artifacts:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p1-shape-contract-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p2-flow-transport-core-subplan-2026-06-15.md`

Gate status:

- `PASSED`

Next action:

- Locally review refreshed Phase 2 subplan, then begin Phase 2 `PRECHECK` if no
  consistency or boundary issue is found.

### 2026-06-15T03:48:39+08:00 - Phase 2 - ASSESS_GATE

Evidence contract:

- Question: Can per-time LEDH flow and OT transport components run over
  `[B,N,D]` without eager scalar decisions?
- Baseline/comparator: Scalar LEDH flow and existing annealed transport
  behavior.
- Primary criterion: Core tests pass, CPU `tf.function` smoke passes, fixed-mask
  semantics hold, no `.numpy()` in new core functions, row independence holds.
- Veto diagnostics: Nonfinite flow/log-det/transport, row cross-talk,
  scalar-only Python loop in compiled core, runtime ESS branch, or transport
  semantics drift.
- Non-claims: No full value parity, no score correctness, no GPU performance,
  no production readiness.

Skeptical audit:

- Wrong baseline: Passed; one-step LEDH compared to scalar row calls.
- Proxy metric risk: Passed; compile smoke and finiteness are Phase 2
  engineering gates only.
- Missing stop condition: Passed; no Phase 2 stop condition fired.
- Unfair comparison: Guarded; Phase 3 must use fixed scalar-stack recursion.
- Hidden assumption: Guarded; fixed-mask relaxed objective only.
- Stale context: Passed; tests reran after VS Code/Codex restart.
- Environment mismatch: Passed for CPU-only pytest; no GPU claim.
- Artifact adequacy: Passed; Phase 2 result and refreshed Phase 3 subplan
  written.

Actions:

- Added one-step batched LEDH flow core and masked annealed transport core.
- Ran focused CPU-only pytest: 11 passed.
- Ran source/diff checks.
- Refreshed Phase 3 subplan.

Artifacts:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p2-flow-transport-core-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p3-value-parity-subplan-2026-06-15.md`

Gate status:

- `PASSED`

Next action:

- Locally review refreshed Phase 3 subplan, then begin Phase 3 `PRECHECK` if no
  consistency or boundary issue is found.

### 2026-06-15T03:57:20+08:00 - Phase 3 - ASSESS_GATE

Evidence contract:

- Question: Does the batched fixed-branch LEDH-PFPF-OT value recursion preserve
  scalar-row relaxed objective semantics?
- Baseline/comparator: Fixed scalar-row stack using the same deterministic
  fixture, fixed pre-flow particles, fixed masks, and Phase 0 tolerances.
- Primary criterion: B=1 and B=20 scalar-stack parity plus row permutation,
  identical-row, fixed-mask, and CPU graph-smoke tests.
- Veto diagnostics: Value parity failure, row cross-talk, runtime ESS branch,
  RNG call, relaxed-objective drift, or uncompiled-only path.
- Non-claims: No score correctness, GPU speed, production default, HMC/NeuTra
  readiness, or posterior validity.

Skeptical audit:

- Wrong baseline: Initially exposed and repaired in the test fixture; sliced
  scalar rows had been rebuilding transition matrices from local row indices.
- Proxy metric risk: Passed; graph smoke and parity are Phase 3 engineering
  gates only.
- Missing stop condition: Passed; no stop condition fired after comparator
  repair and unchanged tolerances.
- Unfair comparison: Passed; scalar rows now close over row-owned transition
  tensors after slicing and permutation.
- Hidden assumption: Guarded; value remains fixed-branch relaxed objective.
- Stale context: Passed after VS Code/Codex restart.
- Environment mismatch: Passed for CPU-only TensorFlow tests.
- Artifact adequacy: Passed; Phase 3 result and refreshed Phase 4 subplan
  written.

Actions:

- Added batched value recursion and focused tests.
- Repaired row-owned transition callback fixture.
- Ran focused CPU-only pytest: 16 passed.
- Ran `git diff --check` for the experimental module and test file.
- Refreshed Phase 4 subplan with score target, finite-difference tolerance, and
  custom-gradient boundary.

Artifacts:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p3-value-parity-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p4-value-score-subplan-2026-06-15.md`

Gate status:

- `PASSED`

Next action:

- Locally review refreshed Phase 4 subplan, then begin Phase 4 `PRECHECK` if no
  consistency or boundary issue is found.

### 2026-06-15T04:02:00+08:00 - Phase 4 - PRECHECK

Evidence contract:

- Question: Does TensorFlow autodiff produce finite row-local scores for the
  relaxed batched LEDH-PFPF-OT objective?
- Baseline/comparator: Batched value recursion plus central finite differences
  on tiny deterministic DPF fixtures with identical fixed tensors and masks.
- Primary criterion: Score shape `[B,p]`, finite scores, row-locality, CPU graph
  smoke, and finite-difference diagnostic within `rtol=2e-4, atol=2e-4`.
- Veto diagnostics: Nonfinite scores, cross-row gradient leakage,
  finite-difference mismatch, categorical PF-gradient claim, or runtime
  stochastic branch.
- Non-claims: No classical PF score, no HMC/NeuTra readiness, no large-model
  validity, no GPU performance, and no production default.

Skeptical audit:

- Wrong baseline: Passed; comparator is the same relaxed batched value
  recursion and fixed deterministic fixture.
- Proxy metric risk: Guarded; finite differences certify only this fixed
  TensorFlow objective.
- Missing stop condition: Passed; subplan stops on nonfinite score,
  cross-row coupling, or failed finite differences.
- Unfair comparison: Guarded; `raw` transport gradients are used for
  finite-difference equivalence.
- Hidden assumption: Guarded; no classical PF likelihood score claim.
- Stale context: Passed after Phase 3 close record.
- Environment mismatch: CPU-only checks only in Phase 4.
- Artifact adequacy: Passed; result and Phase 5 subplan are named.

Claude boundary review:

- Read-only compact digest review returned `VERDICT: AGREE`.
- Caveat: row-locality must be enforced before interpreting
  `grad(sum(value), theta_batch)` as `[B,p]`.
- Artifact:
  `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p4-claude-boundary-review-2026-06-15.md`

Gate status:

- `PASSED`

Next action:

- Implement experimental value+score wrapper and row-locality/finite-difference
  tests.

### 2026-06-15T04:07:57+08:00 - Phase 4 - ASSESS_GATE

Evidence contract:

- Question: Does TensorFlow autodiff produce finite row-local scores for the
  relaxed batched LEDH-PFPF-OT objective?
- Baseline/comparator: Batched value recursion plus central finite differences
  on a no-resampling deterministic DPF fixture with identical fixed tensors and
  masks.
- Primary criterion: Score shape `[B,p]`, finite scores, active-transport
  row-locality, CPU graph smoke, and no-resampling finite-difference agreement
  within `rtol=2e-4, atol=2e-4`.
- Veto diagnostics: Nonfinite score, cross-row gradient leakage, no-resampling
  finite-difference mismatch, categorical PF-gradient claim, or runtime
  stochastic branch.
- Non-claims: No active-transport finite-difference equivalence, no classical
  PF score, no HMC/NeuTra readiness, no large-model validity, no GPU
  performance, and no production default.

Skeptical audit:

- Wrong baseline: Repaired; active transport was removed from the
  finite-difference pass/fail gate after diagnostics showed a distinct backward
  contract.
- Proxy metric risk: Passed; active-transport finite-difference delta is
  explanatory only.
- Missing stop condition: Passed; no-resampling FD remains a continuation
  veto, active-transport finiteness and row-locality remain gates.
- Unfair comparison: Passed; finite differences now compare the no-resampling
  same scalar.
- Hidden assumption: Guarded; no classical PF likelihood score claim.
- Stale context: Passed.
- Environment mismatch: Passed for CPU-only Phase 4 checks; no GPU claim.
- Artifact adequacy: Passed; Phase 4 result and refreshed Phase 5 subplan
  written.

Actions:

- Added experimental value+score wrapper and focused tests.
- Ran diagnostic showing active-transport FD max delta about `4.33e-3`, while
  no-resampling FD max delta was about `5e-11`.
- Patched the Phase 4 subplan visibly to make no-resampling finite differences
  the pass/fail gate and active-transport FD delta explanatory.
- Ran focused CPU-only pytest: 20 passed.
- Ran `git diff --check`.
- Ran Claude read-only repair review: `VERDICT: AGREE`.

Artifacts:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p4-value-score-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p5-compiled-benchmark-subplan-2026-06-15.md`

Gate status:

- `PASSED_WITH_BOUNDARY_REPAIR`

Next action:

- Locally review refreshed Phase 5 subplan, obtain/confirm trusted GPU
  permissions, and run benchmark prechecks.

### 2026-06-15T04:23:53+08:00 - Phase 5 - ASSESS_GATE

Evidence contract:

- Question: What are graph/compiled CPU/GPU timing and capacity characteristics
  for experimental batched LEDH-PFPF-OT value and value+score?
- Baseline/comparator: Scalar compiled CPU value loop where feasible, batched
  CPU/GPU with identical deterministic inputs, and device/JIT metadata.
- Primary criterion: GPU timings are reported only from `tf.function` with
  `jit_compile=True`; artifacts record shape, device, compile time, warm-call
  time, and metadata; no speed claim exceeds evidence.
- Veto diagnostics: Uncompiled GPU timing, wrong device placement, missing
  correctness rerun, missing artifact metadata, or unsupported production/speed
  claim.
- Non-claims: No universal GPU speedup, no production/default readiness, no
  posterior validity, no HMC/NeuTra readiness, no classical PF score.

Skeptical audit:

- Wrong baseline: Passed; B=20 active value parity compared batched compiled
  value to scalar compiled value loop.
- Proxy metric risk: Passed; timings are descriptive single-shape evidence.
- Missing stop condition: Passed; GPU benchmark was allowed only after trusted
  GPU probe.
- Unfair comparison: Guarded; compile times are recorded separately and warm
  medians exclude compile.
- Hidden assumption: Guarded; value+score benchmark uses no-resampling score
  boundary from Phase 4.
- Stale context: Passed.
- Environment mismatch: Passed; CPU runs hid GPU, GPU runs used trusted
  `CUDA_VISIBLE_DEVICES=1` and GPU tensor placement.
- Artifact adequacy: Passed; JSON/MD artifacts written.

Actions:

- Added compiled benchmark harness.
- Added harness tests and ran focused pytest: 8 passed.
- Ran Phase 5 CPU/GPU benchmark artifacts.
- Ran Claude benchmark interpretation review: `VERDICT: AGREE`.

Gate status:

- `PASSED_DESCRIPTIVE_BENCHMARKS`

Next action:

- Run Phase 6 artifact existence/status checks and write final closeout.

### 2026-06-15T04:26:00+08:00 - Phase 6 - ASSESS_GATE

Evidence contract:

- Question: What can be safely concluded about experimental batched
  LEDH-PFPF-OT value+score after the gated program?
- Baseline/comparator: Phase 0-5 results and artifacts.
- Primary criterion: Closeout separates correctness, score, performance,
  API/default policy, and nonclaims.
- Veto diagnostics: Missing phase artifacts, unsupported production/default
  claim, benchmark overclaim, or unresolved correctness blocker.
- Non-claims: No production default, categorical PF gradient, HMC/NeuTra
  readiness, posterior correctness, or universal GPU speedup.

Checks:

- Artifact existence check: passed for required Phase 0-5 docs, implementation,
  tests, and benchmark harness.
- Benchmark artifact check: passed for expected CPU/GPU JSON artifacts.
- `git status --short --branch`: recorded; unrelated modified HMC files remain
  present and untouched by this DPF closeout.

Actions:

- Wrote Phase 6 closeout result.
- Updated visible stop handoff.

Gate status:

- `READY_FOR_FINAL_CLAUDE_REVIEW`

Next action:

- Obtain Claude final read-only review and then finalize.

### 2026-06-15T04:28:00+08:00 - Final Review - COMPLETE

Claude final read-only review:

```text
VERDICT: AGREE
```

Final status:

- `COMPLETE_EXPERIMENTAL_OPT_IN`

Final closeout artifact:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p6-closeout-result-2026-06-15.md`
