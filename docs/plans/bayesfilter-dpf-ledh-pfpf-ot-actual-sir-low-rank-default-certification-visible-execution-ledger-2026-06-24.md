# Actual-SIR Low-Rank LEDH Default-Certification Visible Execution Ledger

Date: 2026-06-24

Status: `COMPLETE_LOW_RANK_LEDH_DEFAULT_ENGINEERING_READY_BOUNDED`

## Ledger Entries

### 2026-06-24T01:58:22+08:00 - Program Draft - PRECHECK

Evidence contract:

- Question: can the locked low-rank route become the bounded engineering
  default for actual-SIR d18 GPU/TF32 LEDH-PFPF-OT?
- Baseline/comparator: paired streaming TF32 actual-SIR route under the same
  model, seeds, shape, dtype, TF32 mode, GPU, and timing contract.
- Primary criterion: phase-local artifacts pass hard validity, provenance,
  comparability, no-NumPy/default-path, and review gates.
- Veto diagnostics: missing actual-SIR semantics, route mismatch, hard veto,
  failed comparability, missing provenance, unsupported claim, or default/API
  change without approval.
- Nonclaims: no posterior correctness, HMC readiness, dense equivalence,
  statistical superiority, public API readiness, scientific validity, or formal
  memory scaling.

Actions:

- Drafted master program, visible runbook, review ledger, execution ledger,
  P00 subplan, and P01 subplan.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-visible-gated-execution-runbook-2026-06-24.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run local document checks and Claude Opus/max read-only review.

### 2026-06-24T02:12:00+08:00 - Phase P00 - ASSESS_GATE

Evidence contract:

- Question: is the default-certification program well-scoped, reviewable,
  artifact-complete, and safe to launch through local-check-only P00?
- Baseline/comparator: completed N3072 replicated-evidence closeout and current
  low-rank actual-SIR validation harness/results.
- Primary criterion: required files exist, local checks pass, boundary scan
  passes, Claude review converges, and P00 result preserves nonclaims.
- Veto diagnostics: missing artifact, failed local check, unsupported claim,
  stale anchor, missing repair loop, or unapproved GPU/default/API/HMC/science
  boundary.
- Nonclaims: no low-rank default readiness, speedup, statistical ranking,
  posterior correctness, HMC readiness, dense equivalence, public API readiness,
  N4096 feasibility, formal memory scaling, production readiness, or scientific
  validity.

Actions:

- Ran file-existence check: passed, `missing=[]`.
- Ran `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`: passed.
- Ran `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`: passed, `18 passed`.
- Ran paragraph-aware boundary scan: passed, `errors=[]`.
- Ran Claude Opus/max read-only review round 1: `VERDICT: REVISE`.
- Patched ambiguous `no-runtime` wording to `local-check-only` and explicit
  `no GPU benchmark/default/API/code-changing/HMC/scientific boundary`.
- Reran focused checks: syntax and pytest passed, ambiguous wording grep found
  no remaining hits.
- Ran Claude Opus/max read-only review round 2: `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p00-governance-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-claude-review-ledger-2026-06-24.md`

Gate status:

- `PASSED`

Next action:

- Proceed to P01 local evidence inventory and default-surface audit.

### 2026-06-24T03:10:00+08:00 - Phase P01 - ASSESS_GATE

Evidence contract:

- Question: what exact evidence and implementation-surface gaps remain before
  low-rank can be considered for bounded LEDH engineering default?
- Baseline/comparator: current streaming GPU/TF32 actual-SIR route, current
  low-rank validation harness, and completed N3072 evidence.
- Primary criterion: inventory current evidence, default-surface files, missing
  gates, and next P02/P03 requirements without unsupported claims.
- Veto diagnostics: missing/corrupt evidence anchor, candidate-lock failure,
  unidentified default/API surface, failed local checks, unsupported claim, or
  unapproved GPU/default/API/HMC/science boundary.
- Nonclaims: no default readiness, speedup, statistical ranking, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API readiness,
  N4096 feasibility, formal memory scaling, production readiness, or scientific
  validity.

Actions:

- Read the N3072 replicated-evidence closeout and confirmed four expected
  N3072 rows for the two rank-16 candidates across seed batches `81137,81138`
  and `81139,81140`.
- Ran a local row-lock validator over the three N3072 aggregate JSONs:
  `errors=[]`.
- Ran targeted source/default-surface searches for current streaming GPU/TF32
  default policy, low-rank route, timing-source, transport-plan, and NumPy /
  `.numpy()` surfaces.
- Read current default streaming surface, low-rank solver surface, older
  low-rank fixture surface, benchmark harness, and focused tests.
- Confirmed the active solver path has no `import numpy`, `np.`, or `.numpy(`
  hits; reporting/tests contain expected `.numpy()`/NumPy fixture usage.
- Confirmed the older low-rank transport-object fixture contains eager
  `.numpy()` diagnostics and is not the locked default-certification candidate.
- Wrote P01 result and drafted P02 implementation/no-NumPy audit subplan.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p01-evidence-surface-audit-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p02-implementation-audit-subplan-2026-06-24.md`

Gate status:

- `PASSED`

Final local checks:

- Syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `18 passed`.
- Boundary scan over P01 result and P02 subplan:
  - Result: pass, `errors=[]`.

Next action:

- Advance to P02 implementation/no-NumPy audit after local subplan review.

### 2026-06-24T03:25:00+08:00 - P02 Subplan Review - REPAIR_LOOP_R1

Actions:

- Ran Claude Opus/max read-only P02 subplan review.
- Claude returned `VERDICT: REVISE`.
- Material issues were fixable in the P02 subplan: literal JIT-source-token
  false-fail risk, missing recorded skeptical audit, missing P03 artifact path,
  and stale status.
- Patched P02 and updated the review ledger.

Gate status:

- `REPAIR_IN_PROGRESS`

Next action:

- Rerun focused local checks and Claude review round 2.

### 2026-06-24T03:32:00+08:00 - P02 Subplan Review - PASS_REVIEW

Actions:

- Reran focused repair checks:
  - syntax check passed;
  - `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
    passed, `18 passed`;
  - boundary scan passed, `errors=[]`;
  - focused scan confirmed no remaining literal `jit_compile=True` or stale
    status hit in P02.
- Ran Claude Opus/max read-only P02 review round 2.
- Claude returned `VERDICT: AGREE`.

Gate status:

- `PASSED`

Next action:

- Execute P02 local implementation/no-NumPy audit.

### 2026-06-24T03:45:00+08:00 - Phase P02 - ASSESS_GATE

Evidence contract:

- Question: is the locked low-rank candidate implementation path clean enough
  to justify moving to an approved trusted-GPU end-to-end benchmark gate?
- Baseline/comparator: current streaming GPU/TF32 implementation path and the
  actual-SIR low-rank validation harness identified in P01.
- Primary criterion: source-anchored inventory shows the candidate route is
  TensorFlow/XLA oriented, has no NumPy or `.numpy()` implementation barriers in
  the active solver path, keeps reporting conversions outside the compiled path,
  and leaves defaults/API untouched.
- Veto diagnostics: active-path NumPy/`.numpy()`, fixture confusion, dense
  materialization, unidentified default surface, failed tests, or unsupported
  claim.
- Nonclaims: no default readiness, speedup, statistical ranking, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API readiness,
  N4096 feasibility, formal memory scaling, production readiness, or scientific
  validity.

Actions:

- Ran solver/compiled-region source audit: passed, `errors=[]`.
- Ran targeted NumPy/`.numpy()` scan:
  - active solver path clean;
  - reporting/test `.numpy()` and NumPy fixture usage identified as outside
    implementation;
  - older low-rank transport fixture `.numpy()` diagnostics identified and
    excluded.
- Ran syntax check over solver, benchmark harness/grid, and focused tests:
  passed.
- Ran focused route-validation/tuning tests:
  `python -m pytest tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `23 passed`.
- Wrote P02 result and drafted P03 benchmark subplan.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p02-implementation-audit-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-subplan-2026-06-24.md`

Gate status:

- `PASSED_LOCAL_CHECKS_PENDING_P03_REVIEW_AND_GPU_APPROVAL`

Next action:

- Review P03 for consistency/boundary safety and request explicit approval for
  trusted GPU benchmark runtime before execution.

### 2026-06-24T03:58:00+08:00 - P03 Subplan Review - REPAIR_LOOP_R1

Actions:

- Ran Claude Opus/max read-only P03 subplan review.
- Claude returned `VERDICT: REVISE`.
- Material issues were fixable in the P03 subplan: timing/proxy gate ambiguity,
  missing explicit `--jit-compile`, and hardcoded GPU ordinal without
  phase-local selection rule.
- Patched P03 and updated the review ledger.

Gate status:

- `REPAIR_IN_PROGRESS`

Next action:

- Rerun focused local checks and Claude P03 review round 2.

### 2026-06-24T04:10:00+08:00 - P03 Subplan Review - REPAIR_LOOP_R2

Actions:

- Reran local P03 repair checks:
  - boundary scan passed, `errors=[]`;
  - syntax check passed;
  - focused tests passed, `23 passed`;
  - focused scan confirmed descriptive timing role, explicit `--jit-compile`,
    and GPU ordinal selection rule.
- Ran Claude Opus/max read-only P03 review round 2.
- Claude returned `VERDICT: REVISE`.
- Substantive P03 blockers were resolved; remaining issue was artifact
  bookkeeping and stale statuses.
- Patched P03 status and review-ledger status; recorded P03 round-2 review.

Gate status:

- `REPAIR_IN_PROGRESS`

Next action:

- Run focused status/bookkeeping scan and Claude P03 final review.

### 2026-06-24T04:18:00+08:00 - P03 Subplan Review - PASS_REVIEW

Actions:

- Reordered the Claude review ledger chronologically after the P03 repair
  patches.
- Ran focused bookkeeping scan:
  - Result: pass, `errors=[]`.
- Ran Claude Opus/max read-only P03 final review.
- Claude returned `VERDICT: AGREE`.
- Updated P03 subplan status to
  `REVIEW_CONVERGED_PENDING_GPU_RUNTIME_APPROVAL`.
- Updated Claude review ledger status to
  `P03_REVIEW_CONVERGED_PENDING_GPU_RUNTIME_APPROVAL`.

Gate status:

- `PASSED_REVIEW_PENDING_GPU_RUNTIME_APPROVAL`

Next action:

- Stop before P03 runtime and ask the user for explicit trusted GPU approval.

### 2026-06-24T03:11:35+08:00 - P03 Runtime Approval And Trusted GPU Precheck

Actions:

- User gave explicit approval to continue P03 trusted GPU runtime.
- Reran the P03 skeptical runtime audit before execution; no material flaw was
  found because the phase still uses paired route `both`, pinned
  `--jit-compile`, descriptive-only timing, explicit GPU selection, hard-veto
  artifact checks, and stop conditions for unsupported boundaries.
- Ran trusted `nvidia-smi`.
- Selected physical CUDA GPU 1 for P03 because it is present and materially
  less busy than GPU 0:
  - GPU 0: UUID `GPU-a008e90f-259e-df57-7988-63b6831fff68`, memory
    `1604/32760 MiB`, utilization `19%`, temperature `73 C`, power
    `79.17 W`.
  - GPU 1: UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`, memory
    `18/32760 MiB`, utilization `0%`, temperature `36 C`, power
    `16.17 W`.

Gate status:

- `P03_GPU_SELECTED_PENDING_DRY_RUN`

Next action:

- Run the P03 dry-run/path-length gate with `--cuda-visible-devices 1` and
  visible TensorFlow device `/GPU:0`.

### 2026-06-24T03:31:52+08:00 - P03 Benchmark Closeout And P04 Draft

Actions:

- Ran the P03 dry-run/path-length gate:
  - status `DRY_RUN`;
  - row count `1`;
  - largest generated path component `255` characters;
  - command included `--jit-compile` and `--cuda-visible-devices 1`.
- Ran the approved P03 trusted-GPU paired benchmark on physical CUDA GPU 1.
- Benchmark result:
  - aggregate status `PASS`;
  - child row status `PASS`;
  - hard vetoes `[]`;
  - actual-SIR semantics passed;
  - paired comparability passed;
  - low-rank and GPU/TF32 provenance passed;
  - route invocations `20` and active resampling steps `20`;
  - dense transport materialization did not occur;
  - aggregate wall time `397.84828382497653` seconds.
- Descriptive timing:
  - streaming warm median `6.769766104524024` seconds;
  - low-rank warm median `0.6633626661496237` seconds;
  - warm median streaming-over-low-rank ratio `10.205226266075517`.
- Ran strict artifact validator:
  - `errors=[]`;
  - metadata warnings only for legacy harness `plan_path` constants in the
    aggregate and child row artifacts.
- Wrote P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-result-2026-06-24.md`.
- Drafted P04 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-subplan-2026-06-24.md`.
- Ran P04 pre-review local checks:
  - boundary/status scan passed, `errors=[]`;
  - syntax check passed;
  - focused tests passed, `23 passed`.

Gate status:

- `P03_PASSED_P04_DRAFT_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude Opus/max read-only P04 subplan review and repair loop if needed.

### 2026-06-24T03:35:54+08:00 - P04 Subplan Review - PASS_REVIEW

Actions:

- Ran Claude Opus/max read-only P04 subplan review.
- Claude returned `VERDICT: AGREE`.
- Non-blocking note only: P04 records the known legacy harness `plan_path`
  metadata caveat from P03.
- Updated P04 subplan status to
  `REVIEW_CONVERGED_PENDING_GPU_RUNTIME_APPROVAL`.
- Updated Claude review ledger status to
  `P04_REVIEW_CONVERGED_PENDING_GPU_RUNTIME_APPROVAL`.

Gate status:

- `P04_REVIEW_CONVERGED_PENDING_GPU_RUNTIME_APPROVAL`

Next action:

- Stop before P04 runtime and ask the user for explicit trusted GPU approval.

### 2026-06-24T03:56:51+08:00 - Provisional Later Subplans And P04 Runtime Approval

Actions:

- User approved drafting all later subplans and continuing the run.
- Drafted provisional conditional subplans:
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-subplan-2026-06-24.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p06-hmc-autodiff-subplan-2026-06-24.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p07-closeout-subplan-2026-06-24.md`
- Ran provisional P04-P07 boundary/status scan:
  - result `errors=[]`.
- Interpreted the user instruction to "continue the run" after explicit
  approval discussion as P04 trusted GPU runtime approval only.
- P05 implementation, P06 HMC/autodiff, and P07 final default-policy switch
  remain separately gated and require their own refreshed subplans and explicit
  approvals.

Gate status:

- `P04_RUNTIME_APPROVED_PENDING_GPU_PRECHECK`

Next action:

- Run trusted P04 GPU precheck, select CUDA ordinal, and execute P04 dry-run
  path-length gate.

### 2026-06-24T04:08:20+08:00 - P04 Benchmark Closeout

Actions:

- Ran trusted P04 GPU precheck and selected physical CUDA GPU 1:
  - GPU 1 UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`;
  - pre-run memory `18/32760 MiB`, utilization `0%`.
- Ran P04 dry-run/path-length gate:
  - status `DRY_RUN`;
  - row count `1`;
  - largest generated path component `255` characters;
  - command included `--jit-compile`, `--cuda-visible-devices 1`, and
    `--num-particles 4096`.
- Ran approved P04 trusted-GPU paired benchmark on physical CUDA GPU 1.
- Benchmark result:
  - aggregate status `PASS`;
  - child row status `PASS`;
  - hard vetoes `[]`;
  - actual-SIR semantics passed;
  - paired comparability passed;
  - low-rank and GPU/TF32 provenance passed;
  - route invocations `20` and active resampling steps `20`;
  - dense transport materialization did not occur;
  - aggregate wall time `416.97745982697234` seconds.
- Descriptive timing:
  - streaming warm median `11.6201760196127` seconds;
  - low-rank warm median `0.8781711575575173` seconds;
  - warm median streaming-over-low-rank ratio `13.232245126260159`.
- Ran strict artifact validator:
  - `errors=[]`;
  - metadata warnings only for legacy harness `plan_path` constants in the
    aggregate and child row artifacts.
- Wrote P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-result-2026-06-24.md`.

Gate status:

- `P04_PASSED_PENDING_P05_REFRESH_AND_APPROVAL`

Next action:

- Refresh/review P05 default-implementation subplan before any P05 code or
  default-surface changes.

### 2026-06-24T04:21:00+08:00 - P05/P07 Subplan Review And Repair Loop

Actions:

- Refreshed P05/P06/P07 after P04 closeout and default-surface discovery.
- Ran focused local checks before Claude review:
  - syntax check passed;
  - `python -m pytest tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q`
    passed, `23 passed`;
  - active solver no-NumPy scan passed.
- Ran Claude Opus/max read-only P05/P06/P07 review round 1:
  `VERDICT: REVISE`.
- Fixed three material plan precision issues:
  - removed P05 discovery/write-set contradiction;
  - made P05 approval separate from P04 runtime approval;
  - made P07 documentation-only unless explicit final approval widens scope.
- Reran focused local checks:
  - syntax check passed;
  - focused tests passed, `23 passed`;
  - active solver no-NumPy scan passed.
- Ran Claude Opus/max focused review round 2:
  `VERDICT: AGREE`.

Gate status:

- `P05_SUBPLAN_REVIEW_CONVERGED`

Next action:

- Execute scoped P05 implementation within the reviewed write set.

### 2026-06-24T04:31:29+08:00 - Phase P05 - ASSESS_GATE

Actions:

- Updated the actual-SIR low-rank validation harness metadata to the current
  default-certification master program.
- Set the direct harness default route to `low_rank`.
- Locked direct harness low-rank defaults to
  `r16_eps0p25_alpha1em08_it120`.
- Updated the grid wrapper default candidate grid to the locked candidate and
  current plan metadata while preserving `--route both` as paired comparator
  mode.
- Added focused tests for default candidate/route selection, streaming and
  paired route reachability, current plan metadata, and grid candidate lock.
- Ran required checks:
  - syntax check passed;
  - focused tests passed, `26 passed`;
  - stale metadata scan passed, no hits;
  - active solver no-NumPy scan passed, no hits.
- Wrote P05 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-result-2026-06-24.md`.

Gate status:

- `P05_PASSED`

Next action:

- Skip P06 unless separate HMC/autodiff approval is granted.

### 2026-06-24T04:33:00+08:00 - Phase P06 - SKIP_NONCLAIM

Actions:

- No separate HMC/autodiff approval was granted.
- No HMC/autodiff runtime was run.
- Wrote P06 skipped/nonclaim result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p06-hmc-autodiff-result-2026-06-24.md`.

Gate status:

- `P06_SKIPPED_HMC_NONCLAIM_PRESERVED`

Next action:

- Refresh P07 and run final documentation-only closeout checks/review.

### 2026-06-24T04:36:45+08:00 - Phase P07 - FINAL_CLOSEOUT

Actions:

- Refreshed P07 after P05/P06.
- Ran final local checks:
  - syntax check passed;
  - focused tests passed, `26 passed`;
  - P00-P06 artifact existence scan passed;
  - boundary scan found only explicit nonclaim/forbidden-action language.
- Ran Claude Opus/max final read-only review:
  `VERDICT: AGREE`.
- Wrote final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-result-2026-06-24.md`.

Gate status:

- `LOW_RANK_LEDH_DEFAULT_ENGINEERING_READY_BOUNDED`

Next action:

- Master program complete. Start a new reviewed program before crossing HMC,
  public API, package-level default, posterior correctness, dense equivalence,
  broader-model, or statistical-claim boundaries.
