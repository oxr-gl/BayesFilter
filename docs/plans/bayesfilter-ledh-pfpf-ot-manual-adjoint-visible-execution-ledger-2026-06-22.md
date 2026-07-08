# LEDH-PFPF-OT Manual Adjoint Visible Execution Ledger

Date: 2026-06-22

Status: COMPLETE_MANUAL_ADJOINT_LOCAL_ROUTE_PASSED_P82_WIRING_BLOCKED

## Entries

### 2026-06-22 - Phase M0 - COMPLETE

Evidence contract:

- Question: Is the manual-adjoint lane ready to proceed from verified repo
  state without repeating the known-bad full-AD route?
- Baseline/comparator: Reset memo, inventory result, P8p Phase 3j runtime
  blocker, and P82 full-AD route correction.
- Primary criterion: Artifacts agree that raw/full AD is forbidden for governed
  N10000, no implementation is claimed yet, and M1 has a bounded derivation
  subplan.
- Veto diagnostics: Missing reset/inventory evidence, stale implementation
  claim, executable N10000 full-AD plan, missing next subplan.
- Non-claims: No manual-adjoint correctness, no implementation readiness, no
  streaming memory improvement, no P82 validation.

Actions:

- Created the manual-adjoint master program.
- Created M0 result and M1 derivation subplan.
- Updated P82 docs so the FD-only comparator contract remains, but P82 is
  downstream-blocked until a memory-disciplined actual-gradient route exists.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-master-program-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase0-reentry-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-subplan-2026-06-22.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md`

Gate status:

- PASSED

Next action:

- Execute M1 derivation/chapter-contract phase.

### 2026-06-22 - Planning - ALL_SUBPLANS_AND_RUNBOOK_DRAFTED

Evidence contract:

- Question: Can the whole manual-adjoint program be made visible with concrete
  subplans and a runbook before execution continues?
- Baseline/comparator: Visible gated execution runbook template and P82 runbook
  pattern.
- Primary criterion: M0-M8 subplans, runbook, ledgers, stop handoff, and master
  phase ladder exist with concrete paths and boundary safety.
- Veto diagnostics: Remaining TBD phase paths, missing evidence contracts,
  missing stop conditions, raw full-AD N10000 route reintroduced, or unsupported
  claims.
- Non-claims: Drafting subplans does not implement or validate the gradient.

Actions:

- Drafted M2-M8 subplans.
- Drafted visible gated execution runbook.
- Drafted Claude review ledger and stop handoff.
- Updated master ladder to concrete subplan/result paths.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-visible-gated-execution-runbook-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-visible-execution-ledger-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-claude-review-ledger-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-visible-stop-handoff-2026-06-22.md`

Gate status:

- DRAFTED_PENDING_FOCUSED_LOCAL_CHECKS

Next action:

- Run focused local checks and then begin M1 only if checks pass.

### 2026-06-22 - Phase M1 - ASSESS_GATE

Evidence contract:

- Question: What exact finite LEDH-PFPF-OT transport scalar and primitive
  adjoints should the manual/custom-gradient route implement and test?
- Baseline/comparator: Existing finite dense Sinkhorn/barycentric code path
  and tiny TensorFlow autodiff references for later M2 tests.
- Primary criterion: Derivation contract states scalar, variables, adjoints,
  stopped/frozen quantities, supported modes, unsupported modes, and M2 parity
  tests without claiming implementation.
- Veto diagnostics: Exact-OT conflation, ambiguous scalar, missing primitive
  adjoints, missing stopped/frozen policy, streaming memory claim, or raw
  full-AD N10000 authorization.
- Non-claims: No implementation correctness, no streaming memory improvement,
  no P82 validation, no HMC/default/posterior readiness.

Actions:

- Read the active M1 subplan and visible runbook.
- Inspected dense/streaming Sinkhorn and LEDH transport anchors.
- Wrote the M1 derivation contract.
- Refreshed the M2 primitive VJP subplan with route name, fixtures, and
  tolerances.
- Wrote the M1 result.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-derivation-contract-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-subplan-2026-06-22.md`

Gate status:

- PASSED_AFTER_CLAUDE_R2_AGREE

Next action:

- Begin M2 primitive dense VJP parity phase under its subplan.

### 2026-06-22 - Phase M2 - PASSED_AFTER_CLAUDE_R1_AGREE

Evidence contract:

- Question: Do the primitive dense manual-adjoint pieces match tiny TensorFlow
  autodiff and finite-difference references within predeclared tolerances?
- Baseline/comparator: TensorFlow autodiff and JVP/VJP on tiny dense fixed
  finite programs; scalar finite difference as explanatory-only spot check.
- Primary criterion: Locally passed for required fixtures and unsupported
  route guards.
- Veto diagnostics: No governed N10000 full AD launched; no production/default
  route edited; no unsupported streaming/warmstart route accepted; no nonfinite
  adjoints observed.
- Non-claims: No memory discipline, no streaming/chunked route, no P82
  validation, no GPU/TF32 evidence, no HMC/default/posterior readiness.

Skeptical audit:

- Baseline is intentionally tiny dense autodiff, not Zhao-Cui and not raw full
  AD at governed scale.
- Finite difference remains explanatory only and is not promoted over the
  autodiff/JVP/VJP oracle.
- The transport-from-potentials test uses the production helper's
  code-defined normalization and log-weight broadcasting.
- Commands answer M2 only; they do not answer streaming memory or SIR d18.

Actions:

- Added `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`.
- Patched the M2 harness after an initial failure so transport log-weight
  broadcasting, scalar `eps`, and reverse-loop replay match the code-defined
  primitive contract.
- Ran focused local checks and diagnostics.
- Wrote the M2 result artifact.

Artifacts:

- `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-result-2026-06-22.md`

Observed maxima:

- barycentric VJP: `0.0`;
- softmin VJP: `6.938893903907228e-18`;
- transport-from-potentials VJP: `8.673617379884035e-18`;
- finite Sinkhorn loop VJP: `2.0816681711721685e-17`;
- finite Sinkhorn loop JVP/VJP: `8.673617379884035e-19`;
- explanatory finite-difference residual: `5.1098448389241824e-15`.

Gate status:

- PASSED_AFTER_CLAUDE_R1_AGREE

Next action:

- Begin M3 dense custom-gradient prototype under its subplan.

### 2026-06-22 - Phase M3 - PASSED_AFTER_CLAUDE_R2_AGREE

Evidence contract:

- Question: Can an opt-in private dense custom-gradient wrapper reproduce the
  verified primitive gradients on tiny dense cases?
- Baseline/comparator: M2 primitive parity and TensorFlow autodiff on the same
  tiny fixed finite dense program.
- Primary criterion: Locally passed for required fixtures, finite
  values/gradients, value equality, gradient parity, and unsupported
  vector-`eps` rejection.
- Veto diagnostics: No public/default route changed, no governed N10000 full
  AD launched, no streaming claim made, and no P82 validation attempted.
- Non-claims: No filter-loop integration, streaming/chunked memory result,
  SIR d18 readiness, P82 validation, GPU/TF32 evidence, or HMC/default
  readiness.

Skeptical audit:

- The existing `filterflow_custom_op` is not treated as the new manual route.
- The new route is private and direct-test only.
- The comparator is tiny raw autodiff of the same fixed finite program, not FD
  or Zhao-Cui.
- The scalar-`eps` and stopped-key scope is explicit; vector-`eps` is rejected.

Actions:

- Added private dense finite manual custom-gradient helpers in
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- Extended `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py` with M3
  value/gradient parity tests and vector-`eps` rejection.
- Ran focused local checks and diagnostics.
- Wrote the M3 result artifact and refreshed the M4 subplan.

Artifacts:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase3-dense-custom-gradient-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase4-loop-adjoint-integration-design-subplan-2026-06-22.md`

Observed M3 maxima:

- dense custom-gradient value error: `0.0`;
- dense custom-gradient gradient error: `5.204170427930421e-18`;
- value finite flag: `1.0`;
- gradient finite flag: `1.0`.

Review and repair:

- Claude R1 returned `VERDICT: REVISE`, requesting negative boundary evidence
  for stopped hyperparameters/public exposure and a tighter M4 replay handoff.
- Added tests for blocked `eps`, `epsilon0`, and `scaling` gradients.
- Added tests that the private route name is not accepted as a public
  `transport_gradient_mode`.
- Tightened M4 default replay contract to recompute
  `C(x, stop_gradient(x))` under the same stopped-key rule.
- Re-ran focused checks: pytest `10 passed`, py_compile passed, diff check
  passed.
- Claude R2 returned `VERDICT: AGREE`.

Gate status:

- PASSED_AFTER_CLAUDE_R2_AGREE

Next action:

- Begin M4 loop-adjoint integration design under its subplan.

### 2026-06-22 - Phase M4 - PASSED_AFTER_CLAUDE_R2_AGREE

Evidence contract:

- Question: What exact filter-loop quantities must the manual/custom-gradient
  route retain, replay, stop, or differentiate?
- Baseline/comparator: Current dense LEDH-PFPF-OT value recursion, transport
  core, and M3 private dense route.
- Primary criterion: Passed after R1 repair: design note states integration
  point, tensor flow, route boundaries, stopped/differentiated quantities,
  replay contract, mask/randomness policy, retained/recomputed ledger,
  canonical M5 comparators/tolerances, and explicit M5 stop rules.
- Veto diagnostics: No implementation performed; no public/default route
  changed; no raw full-AD N10000 route reintroduced.
- Non-claims: No implementation correctness, memory discipline,
  streaming/chunked route, SIR d18 readiness, P82 validation, GPU/TF32
  evidence, or HMC/default/posterior readiness.

Actions:

- Wrote the M4 integration design note.
- Wrote the M4 result artifact.
- Refreshed the M5 subplan with canonical comparators, tolerances, branch
  ownership, mask/log-weight ownership, and halt rules.
- Claude R1 returned `VERDICT: REVISE`; patched the handoff.
- Claude R2 returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-loop-integration-design-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase4-loop-adjoint-integration-design-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase5-small-sir-smoke-subplan-2026-06-22.md`

Gate status:

- PASSED_AFTER_CLAUDE_R2_AGREE

Next action:

- Begin M5 opt-in tiny integration/smoke under its subplan.

### 2026-06-22 - Phase M5 - PASSED_AFTER_CLAUDE_R1_AGREE

Evidence contract:

- Question: Can the private manual/custom-gradient route be invoked through an
  opt-in filter-loop path on small bounded cases without changing defaults?
- Baseline/comparator: M3 stopped-key value helper for transport values, tiny
  raw AD of the same helper for transport gradients, and existing tiny
  fixed-branch LEDH value/score fixture for integration smoke.
- Primary criterion: Locally passed for opt-in routing, default preservation,
  unsupported-combination rejection, mixed masks, transport value/gradient
  parity, finite value/score, and graph/eager parity.
- Veto diagnostics: No generic resampling API exposure; no governed N10000 or
  P82 run; no streaming/memory claim; no nonfinite values/gradients.
- Non-claims: No N10000 feasibility, no streaming/chunked memory improvement,
  no SIR d18 validation, no P82 validation, no GPU/TF32 evidence, no HMC/default
  readiness.

Actions:

- Added opt-in experimental route in `batched_annealed_transport_core_tf`.
- Added focused transport value/gradient parity, mixed-mask, route-boundary,
  and unsupported-combination tests.
- Added tiny fixed-branch LEDH value/score smoke for the opt-in route.
- Wrote M5 result and refreshed M6 subplan.

Observed M5 maxima:

- transport value error: `0.0`;
- transport gradient error: `5.0306980803327406e-17`.

Gate status:

- PASSED_AFTER_CLAUDE_R1_AGREE

Next action:

- Begin M6 streaming/chunked memory route evaluation under its subplan.

### 2026-06-22 - Phase M6 - PASSED_AFTER_CLAUDE_R3_ONE_PATH_AGREE

Evidence contract:

- Question: Does a streaming/chunked manual-adjoint route preserve small-case
  parity while materially reducing dense transport-matrix exposure enough to
  justify P82 handoff preparation?
- Baseline/comparator: M5 opt-in dense route on the same tiny fixed finite
  programs; dense-vs-streaming transported-particle and gradient parity; empty
  returned transport-matrix shape/size evidence.
- Primary criterion: Local tiny CPU/float64 checks passed; Claude R3 one-path
  review agreed.
- Veto diagnostics: No raw full-AD N10000 run; no P82 validation launched; no
  unsupported dense/warmstart/full/vector-epsilon route accepted; no nonfinite
  tiny value/score smoke.
- Non-claims: No N10000 feasibility, no P82 FD agreement, no GPU/TF32 evidence,
  no HMC/default/posterior readiness, and no production readiness.

Skeptical audit:

- The comparator is the M5 dense opt-in route, not Zhao-Cui and not raw full AD.
- The empty returned transport matrix is memory-shape evidence only; it is not
  a full large-N memory proof because the backward pass recomputes through the
  streaming helper.
- The commands answer M6 parity and route-boundary questions only; they do not
  answer P82 SIR d18 FD agreement.
- CPU-only checks are labeled with `CUDA_VISIBLE_DEVICES=-1`; GPU claims remain
  forbidden.

Actions:

- Added/verified the opt-in
  `manual_streaming_finite_sinkhorn_stopped_scale_keys` route.
- Verified dense-vs-streaming transported-particle and gradient parity on tiny
  fixtures.
- Verified the streaming route returns `transport_matrix.shape == (B,0,0)` and
  zero returned transport-matrix size in diagnostics.
- Verified unsupported combinations reject.
- Ran focused local checks and wrote the M6 result artifact.
- Attempted to launch the compact M6 Claude read-only review packet through
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh`; approval was
  rejected because the packet would disclose private workspace context to an
  external model service.
- After the user correction, read repo-root `memory.md` and retried with a
  bounded path/range-only Claude prompt with no pasted code chunks; approval was
  again rejected because even bounded external inspection of private workspace
  paths is forbidden by the current execution policy.
- Performed a bounded local fallback review of the cited paths/ranges and
  patched M6/M7 artifacts to state that M6 does not satisfy or claim the
  `memory.md` Zhao-Cui source-faithfulness gate.
- After the user clarified to use one exact path and no artifacts/big prompt,
  launched Claude R3 on exactly
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-result-2026-06-22.md`.
  Claude returned `VERDICT: AGREE`, finding no new technical parity or
  memory-shape blocker beyond the now-resolved procedural review gate.

Artifacts:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-subplan-2026-06-22.md`

Observed maxima:

- M6 particle value error: `1.1102230246251565e-16`;
- M6 particle/log-weight gradient error: `4.163336342344337e-17`;
- M6 returned transport-matrix size: `0.0`.

Local checks:

- `py_compile`: passed.
- `git diff --check`: passed.
- diagnostics script: passed.
- focused pytest bundle: `23 passed in 46.28s`.

Gate status:

- PASSED_AFTER_CLAUDE_R3_ONE_PATH_AGREE

Next action:

- Begin M7 handoff preparation only.  Do not run P82 validation from M6/M7.

### 2026-06-22 - Phase M7 - P82_RETURN_BLOCKED_BY_BENCHMARK_WIRING

Evidence contract:

- Question: Is there enough reviewed evidence to hand P82 a bounded streaming
  actual-gradient route candidate and preserve the 13-point FD comparator
  protocol?
- Baseline/comparator: M2-M6 parity/memory evidence, P82 FD-only correction,
  P82 full-AD route correction, and current P82 benchmark wiring.
- Primary criterion: Blocked, because exact executable P82 manual-streaming
  commands cannot be stated until the benchmark path exposes and forwards
  `transport_gradient_mode`.
- Veto diagnostics: No P82 validation launched; raw full-AD N10000 not
  reintroduced; FD protocol preserved; tiny M6 evidence not promoted to N10000
  feasibility.
- Non-claims: No P82 FD agreement, N10000 feasibility, GPU/TF32 evidence,
  HMC/default/posterior readiness, production readiness, or Zhao-Cui
  source-faithfulness.

Skeptical audit:

- The handoff cannot pretend to be ready because
  `streaming_batched_ledh_pfpf_ot_value_core_tf` currently calls
  `batched_annealed_transport_core_tf` with `transport_gradient_mode="raw"`.
- The M6 route exists in the experimental batched core only.
- P82 benchmark CLIs expose plan/ad modes but not gradient mode.
- The correct M7 output is a blocker plus candidate non-executable command
  shape after future wiring.

Actions:

- Wrote the P82 handoff artifact.
- Wrote the M7 result artifact.
- Refreshed the M8 closeout subplan.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-p82-validation-handoff-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-subplan-2026-06-22.md`

Gate status:

- P82_RETURN_BLOCKED_BY_BENCHMARK_WIRING_PASSED_AFTER_CLAUDE_R2_AGREE

Next action:

- Begin M8 closeout.

### 2026-06-22 - Phase M8 - COMPLETE

Evidence contract:

- Question: Are the manual-adjoint artifacts, code, tests, docs, limitations,
  and downstream handoff internally consistent?
- Baseline/comparator: M0-M7 phase results, implementation diffs, focused
  tests, and P82 downstream correction artifacts.
- Primary criterion: Passed for closeout with explicit downstream P82 wiring
  blocker.
- Veto diagnostics: No unsupported P82-ready claim; no raw full-AD N10000 route
  reintroduced; no HMC/default/posterior/production claim; final focused tests
  and diff hygiene passed.
- Non-claims: No P82 FD agreement, N10000 feasibility, GPU/TF32 success,
  HMC/default/posterior readiness, production readiness, scientific
  superiority, or Zhao-Cui source-faithfulness.

Actions:

- Ran final diff hygiene, py_compile, unsupported-claim scan, and focused
  pytest bundle.
- Wrote M8 closeout result.
- Updated final visible stop handoff.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-result-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-visible-stop-handoff-2026-06-22.md`

Final checks:

- diff hygiene: passed;
- `py_compile`: passed;
- unsupported-claim scan: no active readiness overclaim found;
- focused pytest bundle: `23 passed in 51.89s`.

Final status:

- MANUAL_ADJOINT_LOCAL_ROUTE_PASSED_P82_WIRING_BLOCKED

Next action:

- Start a separate P82 wiring subplan for `transport_gradient_mode`
  propagation before any P82 validation.
