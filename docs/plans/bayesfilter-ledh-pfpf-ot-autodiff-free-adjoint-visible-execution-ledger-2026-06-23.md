# LEDH-PFPF-OT Autodiff-Free Adjoint Visible Execution Ledger

date: 2026-06-23
status: OPEN

## Initial State

Inherited reviewed blocker:

- `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED`
- valid N100/N1000 remediated metadata artifacts;
- N2500 GPU OOM before valid JSON;
- no valid N10000 actual-gradient artifact;
- S8/P82 FD prohibited.

## P0 Contract Freeze

Status: PASSED

Skeptical audit:

- Question: can P0 freeze the no-production-autodiff invariant and inherited
  blocker state without treating documentation as implementation evidence?
- Baseline: `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED`, with prior N100/N1000
  partial-route artifacts, N2500 GPU OOM, no valid N10000, and FD prohibited.
- Primary criterion: contract, P0 result, execution ledger, stop handoff, and
  P1 subplan all preserve the same no-production-autodiff invariant, inherited
  blocker state, and no-new-GPU/FD authorization.
- Veto diagnostics: missing forbidden API list, ambiguous
  production-vs-diagnostic boundary, missing blocker lock, or drift between
  required P0 artifacts.
- Explanatory only: artifact existence and text occurrence counts.
- Not concluded: implementation, audit tooling, no-autodiff route, GPU
  feasibility, FD agreement, HMC readiness, or scientific validity.

Evidence contract restatement:

- P0 asks only whether the invariant is explicit enough to govern later phases.
- P0 authorizes no implementation, GPU rung, or FD run.

Result:

- Contract written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-contract-2026-06-23.md`.
- P0 result written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase0-contract-freeze-result-2026-06-23.md`.
- P1 subplan refreshed to preserve the inherited
  `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED` state and no GPU/FD authorization.
- No implementation, GPU, or FD command was run in P0.

## P1 Callgraph Leak Inventory

Status: PASSED_REVIEW_PENDING

Skeptical audit:

- P1 uses the reviewed S7R/P82 route as baseline.
- Search hits are not treated as reachability proof; the ledger separates
  route-reachable leaks, custom-gradient boundaries, diagnostic/test-only
  occurrences, unreachable occurrences, and P2 blockers.
- P1 ran only source search and line inspection; no implementation, GPU, FD, or
  TensorFlow execution command was run.

Result:

- Leak ledger written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-autodiff-leak-ledger-2026-06-23.md`.
- P1 result written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-result-2026-06-23.md`.
- Current route leaks were pinned for P2, including outer
  `tf.GradientTape` in the actual-gradient harness and inner
  `tf.GradientTape` in the manual streaming finite transport custom-gradient
  `grad` body.

## P2 Audit-Tooling Subplan Refresh

Status: PASSED

Result:

- P2 subplan refreshed at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-subplan-2026-06-23.md`.
- Bounded Claude review returned `VERDICT: AGREE`.
- P2 execution is authorized only for audit tooling, sentinel, tests,
  whitelist/manifest, audit-result JSON, result note, and P3 subplan refresh.
- Production-route repair, GPU rungs, and FD validation remain forbidden.
- Audit tooling implemented at `scripts/audit_ledh_no_autodiff.py`.
- Focused tests passed: `7 passed`.
- Audit result decision is `FAIL_CURRENT_ROUTE`, as expected for the negative
  control.
- P2 result passed bounded Claude review with `VERDICT: AGREE`.

## P3 Derivation-Contract Subplan Refresh

Status: PASSED

Skeptical audit:

- Question: can P3 specify the manual adjoint obligations needed to replace or
  block the P1/P2 leaks without drifting into implementation, GPU, FD, or
  scientific claims?
- Baseline: P0 contract, P1 leak ledger, P2 audit tooling/result.
- Primary criterion: every primitive needed by the filter backward pass must
  have an owner, input/output adjoint shape, stop condition, and audit
  requirement tied to P1/P2 leak closure.
- Veto diagnostics: missing outer objective adjoint replacing P1-L001/P1-L003,
  missing log-weight normalization adjoint, missing LEDH flow adjoint, missing
  transport adjoint replacing P1-L013/P1-L015, or hidden autodiff fallback.
- Explanatory only: later tiny autodiff parity obligations for tests.
- Not concluded: implementation correctness, no-autodiff certification, GPU
  feasibility, FD agreement, posterior correctness, HMC readiness, production
  readiness, or scientific superiority.

Result:

- P3 subplan patched after Claude R1 and passed Claude R2 with
  `VERDICT: AGREE`.
- P3 execution is authorized only for derivation-contract documentation,
  local text/label searches, optional derivation-audit tooling, result note,
  and refreshed downstream subplans.
- Production-route repair, GPU rungs, FD validation, and actual-gradient runs
  remain forbidden.

Execution result:

- P3 derivation contract written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-derivation-contract-2026-06-23.md`.
- P3 result written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-result-2026-06-23.md`.
- P4/P5/P6 subplans refreshed to inherit the P3 obligations and no-autodiff
  boundary.
- Local content checks and `git diff --check` passed.
- P3 result passed bounded Claude review with `VERDICT: AGREE`.

## P4 SIR Analytical Derivatives Subplan Refresh

Status: PASSED

Skeptical audit:

- Question: can P4 wire analytical SIR derivatives without drifting into
  Zhao-Cui comparison, production autodiff, transport repair, GPU, FD, or
  actual-gradient validation?
- Baseline: P3 derivation contract and existing analytical derivative/code
  anchors.
- Primary criterion: production route calls analytical SIR derivative functions
  for theta convention, RK4/RHS state sensitivities, observation gather, and
  observation covariance parameter adjoint; audit blocks autodiff fallback.
- Veto diagnostics: production SIR autodiff callback, diagnostic parity
  treated as proof, missing theta-order contract, missing observation
  covariance adjoint, or source-faithfulness claims without anchors.
- Explanatory only: tiny autodiff parity in tests.
- Not concluded: full filter gradient correctness, no-autodiff certification,
  GPU feasibility, FD agreement, HMC readiness, or scientific validity.

Result:

- P4 subplan passed Claude review after one visible repair loop.
- P4 execution is authorized only for analytical SIR derivative wiring,
  focused tests/checks, P4 result, and refreshed P5 subplan.
- Transport repair, filter-level route certification, GPU rungs, FD
  validation, actual-gradient runs, HMC checks, and posterior checks remain
  forbidden.

Execution result:

- Analytical SIR methods added to `bayesfilter/highdim/models.py`.
- Focused tests added to `tests/highdim/test_p81_analytical_sir_score.py`.
- P4 result written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-result-2026-06-23.md`.
- Current-route audit artifact written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-current-route-audit-result-2026-06-23.json`.
- Refreshed P5 subplan updated to inherit the P4 analytical SIR interface.
- Local checks passed: `py_compile`, focused pytest `7 passed`,
  no-autodiff audit negative control `FAIL_CURRENT_ROUTE`, static scan of
  touched model/test files, and `git diff --check`.
- P4 result passed bounded Claude review with `VERDICT: AGREE`.
- Refreshed P5 subplan first returned `VERDICT: REVISE`, was visibly patched
  to remove finite-difference ambiguity, require transition/observation
  log-density and likelihood-increment coverage, and add exact commands, then
  passed bounded Claude review R2 with `VERDICT: AGREE`.

## P5 LEDH Flow And Log-Weight Adjoints Subplan Refresh

Status: PASSED

Skeptical audit:

- Question: can P5 implement non-transport primitive adjoints for the LEDH
  flow/log-density/log-weight layer without drifting into transport repair,
  filter-level certification, GPU, FD, actual-gradient, or scientific claims?
- Baseline: P3 derivation contract, P4 analytical SIR derivative interface,
  and P2 audit tooling negative-control route.
- Primary criterion: primitive adjoint tests pass for transition log-density,
  observation log-density, log-normalization, likelihood-increment
  accumulation, floor-mask handling, and LEDH flow interface boundaries, with
  no new production autodiff leak.
- Veto diagnostics: hidden tape in P5 production primitive; missing shape
  contract; missing transition or observation log-density adjoint; missing
  likelihood-increment adjoint; finite differences in P5; or unexplained audit
  leak.
- Explanatory only: tiny diagnostic autodiff parity residuals in tests.
- Not concluded: transport custom-gradient repair, full route certification,
  GPU feasibility, FD agreement, N10000 actual-gradient validity, HMC
  readiness, or scientific validity.

Result:

- P5 subplan is reviewed and ready for execution at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-subplan-2026-06-23.md`.
- P5 may only implement and test LEDH flow/log-density/log-weight primitive
  adjoints.  P1-L013 and P1-L015 remain P6 transport leaks.

Execution result:

- P5 primitive adjoints were implemented in
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`.
- Focused tests were added at
  `tests/test_ledh_pfpf_ot_p5_primitive_adjoints.py`.
- P5 result was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-result-2026-06-23.md`.
- P5 current-route audit artifact was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-current-route-audit-result-2026-06-23.json`.
- P2 manifest and whitelist were updated to classify the new P5 diagnostic
  test tapes as test-only, not production route evidence.
- Local checks passed: `py_compile`, focused pytest `6 passed`,
  no-autodiff audit negative control `FAIL_CURRENT_ROUTE`, static scan of
  touched production/test files, and `git diff --check`.
- P5 result passed bounded Claude review with `VERDICT: AGREE`.
- Refreshed P6 subplan first returned `VERDICT: REVISE`; it was visibly
  patched to forbid GPU execution in P6 and to externalize any P5 primitive
  boundary defect rather than modifying P5 helpers inside P6.
- Refreshed P6 subplan passed bounded Claude review R2 with `VERDICT: AGREE`.

## P6 Transport No-Autodiff Audit And Repair Subplan Refresh

Status: PASSED

Skeptical audit:

- Question: can P6 audit and repair only the transport custom-gradient route
  for P1-L013/P1-L015 without drifting into P5 primitive repair, filter-level
  certification, GPU, FD, actual-gradient, or scientific claims?
- Baseline: P3 transport contract, P5 primitive boundaries, P2 audit tooling,
  current failed old replay route, and candidate blockwise VJP route.
- Primary criterion: selected transport route passes no-autodiff grad-body
  audit and focused transport tests without `transport_ad_mode=full`; P1-L013
  and P1-L015 are either closed or explicit blockers.
- Veto diagnostics: custom-gradient grad body opens autodiff; dense transport
  storage reappears; candidate route is trusted by name without body audit;
  route scalar/stopped-key/scale semantics change; P6 attempts GPU/FD/full
  filter certification or P5 helper repair.
- Explanatory only: CPU-only timing/allocation notes from focused tests.
- Not concluded: full filter route, N10000 feasibility, FD agreement, HMC
  readiness, posterior correctness, or scientific validity.

Result:

- P6 subplan is reviewed and ready for execution at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-subplan-2026-06-23.md`.

Execution result:

- P6 repaired the selected manual streaming finite transport route in
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  so its custom-gradient `grad` body no longer opens `tf.GradientTape`.
- Focused audit tests in `tests/test_audit_ledh_no_autodiff.py` now guard the
  repaired selected route boundary.
- P6 result was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-result-2026-06-23.md`.
- P6 current-route audit artifact was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-current-route-audit-result-2026-06-23.json`.
- Local checks passed: `py_compile`, focused pytest `22 passed`, focused
  transport pytest `14 passed`, expected current-route audit
  `FAIL_CURRENT_ROUTE`, and `git diff --check`.
- The audit now fails only for P1-L001/P1-L003 in the reviewed manifest.
  P1-L013/P1-L015 are closed for the selected manual streaming finite
  transport route.
- The unselected `filterflow_custom_op` route still has a tape-based grad body
  and remains route-flag-vetoed.
- P6 result and refreshed P7 subplan require bounded review before P7
  execution can begin.
- P6 result passed bounded Claude review with `VERDICT: AGREE`.
- Refreshed P7 subplan passed bounded Claude review with `VERDICT: AGREE`.

## P7 Filter-Level Manual Route Subplan Refresh

Status: REVIEWED_READY_FOR_EXECUTION

Skeptical audit:

- Question: can P7 replace the remaining outer objective tape
  P1-L001/P1-L003 with an opt-in manual reverse-scan route without reopening
  P5/P6 boundaries or drifting into certification/GPU/FD?
- Baseline: P5 primitive adjoints, P6 selected transport grad-body closure,
  and current audit failure limited to P1-L001/P1-L003.
- Primary criterion: new opt-in route computes finite tiny manual scores and
  route-bound audit closes P1-L001/P1-L003 while P1-L013/P1-L015 remain closed.
- Veto diagnostics: outer tape remains required; hidden fallback; route default
  changed; audit bypassed; P5/P6 helper repair; `transport_ad_mode=full`;
  GPU/FD/actual-gradient/certification work.
- Explanatory only: tiny diagnostic parity, CPU-only timing, runtime sentinel
  traces.
- Not concluded: N10000 feasibility, FD agreement, HMC readiness, posterior
  correctness, production default, or scientific validity.

Execution result:

- P7 added an opt-in `manual-reverse` route in
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py` and
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`.
- The route computes manual SIR/RK4, LEDH flow/log-weight, transport, and
  parameter-score adjoints without the selected outer objective tape.
- Focused tests passed: `12 passed, 2 warnings` for
  `tests/test_audit_ledh_no_autodiff.py` and
  `tests/test_ledh_pfpf_ot_p7_manual_score.py`.
- CPU-only manual smoke passed with finite objective and gradient.
- Runtime sentinel smoke passed for the selected manual route.
- P7 audit artifact was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-current-route-audit-result-2026-06-23.json`.
- P7 audit decision remains `FAIL_CURRENT_ROUTE`, but `failed_p1_ids: []` and
  `bad_route_flag_vetoes: []`; this is a route-bound P7 pass, not full
  no-autodiff certification.
- P7 result was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-filter-custom-gradient-result-2026-06-23.md`.
- Refreshed P8 subplan was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-certification-tests-subplan-2026-06-23.md`.
- P7 result passed bounded Claude review with `VERDICT: AGREE`.

## P8 Certification Tests Subplan Refresh

Status: DRAFT_READY_FOR_REVIEW

Skeptical audit:

- Question: can P8 certify the exact selected `manual-reverse` route as
  no-autodiff by static and runtime audit, without using P7's broad
  `FAIL_CURRENT_ROUTE` as a pass?
- Baseline: P7 manual route and P2/P7 audit artifacts.
- Primary criterion: exact P8 route manifest passes
  `PASS_NO_AUTODIFF_AUDIT`, runtime sentinel executes the selected route
  without forbidden API calls, and focused tests pass.
- Veto diagnostics: selected-route forbidden API; custom-gradient grad body
  opens autodiff; broad whitelist; bad route flags including
  `reverse-gradient`, `forward-jvp`, `filterflow_custom_op`, or
  `transport_ad_mode=full`; incomplete manifest; diagnostic autodiff promoted
  as proof; GPU/FD/N10000/default/scientific drift.
- Explanatory only: tiny diagnostic parity, CPU-only timings, old diagnostic
  helper locations.
- Not concluded: GPU feasibility, N10000 feasibility, FD agreement, HMC
  readiness, posterior correctness, production default, or scientific
  validity.
- Refreshed P8 subplan passed bounded Claude review with `VERDICT: AGREE`.
- The review's only nit was traceability polish: predeclare the exact manifest
  filename.  The P8 subplan was patched to name
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json`
  as the required route manifest.

Execution result:

- P8 exact-route audit support was added to
  `scripts/audit_ledh_no_autodiff.py`.
- The selected manual route now calls the selected finite streaming transport
  helper directly in
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`.
- P8 route manifest was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json`.
- P8 audit result was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json`.
- P8 audit decision is `PASS_NO_AUTODIFF_AUDIT`; active production findings
  are zero; selected custom-gradient boundary line 1960 passes grad-body scan.
- Focused tests passed: `15 passed, 2 warnings`.
- CPU-hidden manual route smoke passed and wrote
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-manual-route-runtime-sentinel-smoke-2026-06-23.json`.
- P8 result was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-certification-tests-result-2026-06-23.md`.
- Refreshed P9 subplan was written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-ladder-subplan-2026-06-23.md`.

## P9 Trusted GPU Ladder Subplan Refresh

Status: DRAFT_READY_FOR_REVIEW

Skeptical audit:

- Question: can P9 run a trusted GPU ladder for the exact audited
  `manual-reverse` route through N10000, stopping at the first non-`PASSED`
  rung?
- Baseline: S7R N2500 OOM on partial manual route with outer autodiff; P8 exact
  route audit pass.
- Primary criterion: N10000 exits 0 and validates with the same P8 route
  identity/audit, finite objective/gradient/MCSE, GPU placement, five seeds,
  and no prior non-`PASSED` rung.
- Veto diagnostics: trusted GPU preflight failure; rung OOM/nonzero/timeout;
  route/audit mismatch; CPU placement; wrong route; nonfinite values; FD
  launched; higher rung launched after any non-`PASSED` rung.
- Explanatory only: runtime, memory trends, allocator warnings.
- Not concluded: FD agreement, posterior correctness, HMC readiness,
  production default, or scientific validity.
- P8 result review R1 returned `VERDICT: REVISE` for wording/traceability
  fixes.  P8 result was patched to clarify GPU-hidden / CPU-only checks, exact
  P2/P7 comparator artifacts, and no production-route whitelist exemption.
- P8 result review R2 returned `VERDICT: AGREE`.

P9 subplan review R1 returned `VERDICT: REVISE`.  Claude agreed the intended
P9 boundary was safe but found the plan insufficiently execution-self-contained
for a trusted GPU ladder.  The P9 subplan was patched to add exact
commands/environment, explicit P9 evidence-contract and run-manifest
artifacts, pre-N100 P8 manifest/audit validation, concrete sequential rung
commands, and per-rung JSON validation.  GPU rungs remain forbidden until the
patched P9 subplan passes bounded Claude review.

P9 subplan review R2 returned `VERDICT: REVISE`.  Claude agreed the
boundary-safety guards were good, but requested exact artifact-creation
procedures and an ex-ante interpreter/environment binding.  The P9 subplan was
patched to bind `/home/chakwong/anaconda3/envs/tf-gpu/bin/python`,
`/usr/bin/timeout`, `/home/chakwong/BayesFilter`, and `MPLCONFIGDIR=/tmp`, and
to add exact writers/validators for the evidence contract, GPU preflight JSON,
run manifest, initialized rung ledger, passed/non-`PASSED` rung ledger updates,
P9 result, stop handoff, and conditional P10 refresh.  GPU rungs remain
forbidden until the patched P9 subplan passes bounded Claude review.

P9 subplan review R3 returned `VERDICT: AGREE`.

## P9 Trusted GPU Ladder Execution

Status: BLOCKED_N10000_TIMEOUT_REVIEW_PENDING

Skeptical audit:

- Question: can the exact audited no-production-autodiff `manual-reverse`
  route produce finite five-seed SIR actual gradients through N10000 on
  trusted GPU/TF32?
- Baseline: S7R/P82 N2500 OOM on the partial manual route with outer autodiff;
  P8 exact-route audit `PASS_NO_AUTODIFF_AUDIT`.
- Primary criterion: N10000 exits 0 and validates with the exact P8 route
  identity, manual-reverse, FD disabled, streaming/stabilized transport,
  selected manual streaming finite gradient mode, finite objective/gradient
  and MCSE, GPU placement, five seeds, and ordered rung ledger with no prior
  non-`PASSED` rung.
- Veto diagnostics: GPU preflight failure, P8 audit mismatch, rung
  nonzero/timeout/OOM, CPU placement, wrong route, nonfinite values, FD launch,
  Zhao-Cui comparator, `transport_ad_mode=full`, or launching higher rung
  after first non-`PASSED`.
- Explanatory only: runtime/memory trends and intermediate passed rungs.
- Not concluded: FD agreement, posterior correctness, HMC readiness,
  production default, statistical superiority, or scientific validity.

Execution result:

- P9 evidence contract written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-evidence-contract-2026-06-23.md`.
- Trusted GPU preflight passed and wrote
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-preflight-2026-06-23.json`.
- P9 run manifest written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-run-manifest-2026-06-23.json`.
- P9 rung ledger written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-rung-ledger-2026-06-23.json`.
- N100, N1000, N2500, and N5000 passed and validated.
- N10000 timed out with exit code `124` before writing JSON or progress
  artifact.
- Rung ledger records first non-`PASSED` rung as `N10000` and confirms no
  higher rung was launched after the blocker.
- P9 result written at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-ladder-result-2026-06-23.md`.
- P10 is not authorized because no valid N10000 JSON exists.
