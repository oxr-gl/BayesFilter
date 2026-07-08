# P91 Visible Execution Ledger

Date: 2026-06-29

Status: `P91_SCOPED_PRODUCTION_READY_CLOSED`

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-identity-hmc-gpu-production-master-program-2026-06-29.md`

Runbook:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-gated-execution-runbook-2026-06-29.md`

## Launch Skeptical Audit

Evidence contract:

- Question: Can P91 safely launch a successor Zhao-Cui production-readiness
  program under score-identity, FD, batched API, GPU/XLA-HMC, and benchmark
  gates?
- Baseline/comparator: P90 final blocked decision and owner P91 amendments.
- Primary criterion: advance only through reviewed phase gates; final promotion
  requires all P91 production gates.
- Veto diagnostics: score identity as exact likelihood proof, FD as oracle,
  GPU as universally fastest, batched performance as scientific validity,
  missing caveats, unreviewed runtime/GPU/HMC/default crossing.
- Non-claims: no production readiness, exact likelihood correctness,
  posterior correctness, universal GPU superiority, or default-policy change.

Skeptical audit result:

- Wrong baseline avoided by inheriting P90 as blocked with retained positives.
- Proxy metric risk controlled by assigning score identity, FD, JIT, benchmark,
  and HMC smoke to separate ledgers.
- Runtime/GPU/HMC/package/default boundaries remain locked until exact reviewed
  phase subplans authorize them.

Next action:

- Run local P91 document hygiene checks and bounded Claude review of the
  master, runbook, and Phase 0 subplan.

### 2026-06-29 - Launch Reviews Closed / Phase 0 Ready

Actions:

- Local P91 document hygiene passed:
  `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md`.
- P90 final decision and reset memo anchors exist.
- Subplan section coverage check passed.
- Claude reviewed P91 master: `VERDICT: AGREE`.
- Claude reviewed P91 runbook iteration 1: `VERDICT: REVISE`.
- Patched runbook release/final authority, probe wording, and material
  artifact-linkage requirements.
- Claude reviewed P91 runbook iteration 2: `VERDICT: AGREE`.
- Claude reviewed Phase 0 subplan iteration 1: `VERDICT: REVISE`.
- Patched Phase 0 subplan production-contract review coverage, exact
  master/runbook paths, and skeptical-plan audit.
- Claude reviewed Phase 0 subplan iteration 2: `VERDICT: AGREE`.

Gate status:

- `P91_MASTER_REVIEWED_AGREE`
- `P91_RUNBOOK_REVIEWED_AGREE`
- `P91_PHASE0_SUBPLAN_REVIEWED_AGREE`
- `P91_PHASE0_READY`

Next action:

- Execute Phase 0 document-only checks and write the production contract,
  Phase 0 result, and refreshed Phase 1 subplan.

### 2026-06-29 - Phase 0 Local Execution Complete / Pending Review

Evidence contract:

- Question: Is the P91 production contract safely reframed from P90 without
  treating score identity as exact likelihood proof, FD as oracle, or GPU as
  universally fastest?
- Baseline/comparator: P90 final blocked decision and user P91 owner
  amendments.
- Primary criterion: production contract states required gates, non-claims,
  owner decisions, runtime boundaries, and next-phase handoff.
- Veto diagnostics: exact-likelihood claim, FD oracle claim, root-solving
  requirement, Hessian requirement, universal GPU-speed claim, missing batched
  route requirement, default-policy change.
- Non-claims: no score correctness, FD pass, GPU/XLA readiness, HMC readiness,
  benchmark result, production readiness, or default-policy change.

Actions:

- Ran Phase 0 document-only anchor and keyword checks.
- Wrote production contract:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-production-contract-2026-06-29.md`.
- Wrote Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-result-2026-06-29.md`.
- Refreshed Phase 1 subplan status and entry conditions:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-subplan-2026-06-29.md`.

Gate status:

- `P91_PHASE0_LOCAL_READY_PENDING_REVIEW`

Next action:

- Send production contract, Phase 0 result, and Phase 1 subplan to one-path
  bounded Claude read-only review.

### 2026-06-29 - Phase 0 Reviewed Closed / Phase 1 Ready

Actions:

- Claude reviewed production contract: `VERDICT: AGREE`.
- Claude reviewed Phase 0 result iteration 1: `VERDICT: REVISE`.
- Patched Phase 0 result artifact coverage.
- Claude reviewed Phase 0 result iteration 2: `VERDICT: AGREE`.
- Claude reviewed Phase 1 score-contract subplan: `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-production-contract-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-subplan-2026-06-29.md`

Gate status:

- `P91_PHASE0_REVIEWED_PRODUCTION_CONTRACT_CLOSED`
- `P91_PHASE1_SUBPLAN_REVIEWED_AGREE`
- `P91_PHASE1_READY`

Next action:

- Execute Phase 1 document/source inventory checks and write score contract,
  Phase 1 result, and refreshed Phase 2 subplan.

### 2026-06-29 - Phase 1 Local Execution Complete / Pending Review

Evidence contract:

- Question: Can P91 freeze an unambiguous Zhao-Cui score contract suitable for
  batched API, FD, score identity, GPU/XLA, HMC, and release notes?
- Baseline/comparator: reviewed P91 production contract and existing highdim
  source-route/score API surfaces.
- Primary criterion: score contract names exact semantics, non-claims, and
  blockers/diagnostics without authorizing runtime promotion.
- Veto diagnostics: ambiguous sign, missing branch identity, ALS revival,
  hidden derivative omission, score identity as exact likelihood proof, or
  batched API mismatch left unspecified.
- Non-claims: no implementation correctness, FD pass, score identity pass,
  GPU/XLA readiness, HMC readiness, benchmark result, or production readiness.

Actions:

- Ran Phase 1 source/API inventory checks and P91 docs diff hygiene.
- Inspected focused source slices in `bayesfilter/highdim/score_api.py` and
  `bayesfilter/highdim/source_route.py`.
- Wrote score contract:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-contract-2026-06-29.md`.
- Wrote Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-result-2026-06-29.md`.
- Refreshed Phase 2 subplan status/entry conditions:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-subplan-2026-06-29.md`.

Gate status:

- `P91_PHASE1_LOCAL_READY_PENDING_REVIEW`

Next action:

- Send score contract, Phase 1 result, and Phase 2 subplan to one-path bounded
  Claude read-only review.

### 2026-06-29 - Phase 1 Review Closed / Phase 2 Ready

Actions:

- Patched score contract after Claude iteration 1 found four boundary issues:
  inherited training/basis policy overreach, derivative-policy evidence
  wording, missing setup-identity metadata channel, and ambiguous batched setup
  identity semantics.
- Ran P91 docs diff hygiene after the patch.
- Claude reviewed repaired score contract iteration 2: `VERDICT: AGREE`.
- Patched Phase 1 result and Phase 2 subplan to align with the repaired score
  contract identity-metadata and batch fail-closed semantics.
- Ran P91 docs diff hygiene after the result/subplan patch.
- Claude reviewed Phase 1 result: `VERDICT: AGREE`.
- Claude reviewed Phase 2 batched API subplan: `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-contract-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-subplan-2026-06-29.md`

Gate status:

- `P91_PHASE1_REVIEWED_SCORE_CONTRACT_CLOSED`
- `P91_PHASE2_SUBPLAN_REVIEWED_AGREE`
- `P91_PHASE2_READY`

Next action:

- Begin Phase 2 source inventory and write the Phase 2 implementation
  design/test manifest for review before any code edit or pytest command.

### 2026-06-29 - Phase 2 Local Implementation Complete / Pending Review

Evidence contract:

- Question: Can the highdim subpackage expose a batched value/score API whose
  outputs match looped single calls and whose setup identity metadata fails
  closed?
- Baseline/comparator: existing `evaluate_highdim_score_api` looped over
  deterministic scalar value functions under the same theta and setup identity.
- Primary criterion: batched values/scores equal looped single values/scores
  with stable shape/dtype, branch identities, and setup identity metadata.
- Veto diagnostics: missing setup identity, ambiguous/mixed identity, root
  export, NaN/Inf, shape/dtype drift, disconnected scores, and broader
  readiness claims.
- Non-claims: no FD consistency, score identity, GPU/XLA readiness, HMC
  readiness, benchmark result, or production readiness.

Actions:

- Claude reviewed Phase 2 implementation artifact:
  `VERDICT: AGREE`.
- Added `HighDimBatchedScoreAPIResult` and
  `evaluate_batched_highdim_score_api` in
  `bayesfilter/highdim/score_api.py`.
- Added optional keyword-only `setup_identity` to the existing single
  `evaluate_highdim_score_api` comparator path.
- Exported the new batched API symbols through `bayesfilter.highdim` only.
- Added `tests/highdim/test_p91_batched_score_api.py`.
- Ran Phase 2 local checks:
  `git diff --check` passed; CPU-only pytest passed
  `10 passed, 2 warnings in 7.05s`.
- Wrote Phase 2 result and refreshed Phase 3 subplan.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-implementation-artifact-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-subplan-2026-06-29.md`

Gate status:

- `P91_PHASE2_IMPLEMENTATION_ARTIFACT_REVIEWED_AGREE`
- `P91_PHASE2_BATCHED_API_LOCAL_PASS_PENDING_REVIEW`

Next action:

- Send Phase 2 result and refreshed Phase 3 subplan to one-path bounded Claude
  read-only review.

### 2026-06-29 - Phase 2 Review Closed / Phase 3 Ready

Actions:

- Claude reviewed Phase 2 result iteration 1: `VERDICT: REVISE`.
- Patched Phase 2 result with self-contained cross-artifact consistency,
  preserved local-check output, and manifest-grade fields.
- Claude reviewed Phase 2 result iteration 2: `VERDICT: REVISE`.
- Patched Phase 2 result with explicit `Commands` and `Data version` manifest
  rows.
- Claude reviewed Phase 2 result iteration 3: `VERDICT: AGREE`.
- Claude reviewed Phase 3 subplan iteration 1: `VERDICT: REVISE`.
- Patched Phase 3 subplan to include the FD implementation artifact in the
  evidence-contract artifact row, clarify implementation-artifact versus
  manifest authority, and add package/release/CI plus default-policy
  non-conclusions.
- Claude reviewed Phase 3 subplan iteration 2: `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-local-check-output-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-subplan-2026-06-29.md`

Gate status:

- `P91_PHASE2_REVIEWED_BATCHED_API_CLOSED`
- `P91_PHASE3_SUBPLAN_REVIEWED_AGREE`
- `P91_PHASE3_READY_FOR_FD_IMPLEMENTATION_ARTIFACT`

Next action:

- Begin Phase 3 by writing the FD implementation artifact for review. Do not
  run FD runtime until that artifact receives Claude `VERDICT: AGREE`.

### 2026-06-29 - Phase 3 Limited FD Blocked / Phase 4 Blocker Closed

Actions:

- Wrote Phase 3 FD implementation artifact.
- Claude reviewed Phase 3 FD implementation artifact iteration 1:
  `VERDICT: REVISE`.
- Patched implementation artifact to explicitly authorize preserved local
  check output writing and tighten FD ladder stability.
- Claude reviewed Phase 3 FD implementation artifact iteration 2:
  `VERDICT: AGREE`.
- Implemented `tests/highdim/test_p91_fd_consistency_limited.py`.
- Ran authorized Phase 3 checks:
  `git diff --check` passed; CPU-only pytest passed
  `6 passed, 2 warnings in 5.52s`.
- FD manifest status:
  `BLOCK_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY`.
- Wrote Phase 3 local-check output and Phase 3 result.
- Claude reviewed Phase 3 result iteration 1: `VERDICT: REVISE`.
- Patched Phase 3 result to identify pytest as the manifest-producing harness
  command and narrow artifact wording to FD manifest.
- Claude reviewed Phase 3 result iteration 2: `VERDICT: AGREE`.
- Refreshed Phase 4 score-identity subplan as blocker-only.
- Claude reviewed Phase 4 subplan iteration 1: `VERDICT: REVISE`.
- Patched Phase 4 subplan to explicitly exclude package/release/CI/default
  boundaries and clarify blocker-only versus future executable artifacts.
- Claude reviewed Phase 4 subplan iteration 2: `VERDICT: AGREE`.
- Wrote Phase 4 blocker result.
- Claude reviewed Phase 4 result iteration 1: `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-implementation-artifact-2026-06-29.md`
- `tests/highdim/test_p91_fd_consistency_limited.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-manifest-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-local-check-output-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-subplan-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-result-2026-06-29.md`

Gate status:

- `BLOCK_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY`
- `BLOCK_P91_PHASE4_SCORE_IDENTITY_NOT_RUN_FD_BLOCKED`

Next action:

- Stop the current pass-gate execution path. The next safe action is a reviewed
  Phase 3 FD repair plan, or an explicit reviewed production-standard waiver
  before any score-identity runtime.

### 2026-06-29 - Phase 3 Owner Acceptance / Phase 4 Reopened

Evidence contract:

- Question: Can P91 continue past the Phase 3 limited-FD diagnostic without
  pretending the arbitrary `5e-5` threshold was principled or that FD proved a
  true-gradient oracle?
- Baseline/comparator: Phase 3 manifest, Phase 3 result, and owner direction
  in the current conversation.
- Primary criterion: record the Phase 3 diagnostic as owner-accepted for
  continuation with caveats, then refresh Phase 4 as an executable
  score-identity validation.
- Veto diagnostics: calling the old manifest a full FD pass, hiding the
  arbitrary tolerance issue, hiding previous-marginal/fixed-TTSIRT derivative
  blockers, or running GPU/HMC/package/default commands from this amendment.
- Non-claims: no full source-route FD pass, exact likelihood correctness,
  true-gradient oracle agreement, GPU/XLA readiness, HMC readiness, benchmark
  result, package/release/CI readiness, default-policy change, or production
  readiness.

Skeptical audit result:

- Wrong baseline avoided: the old `5e-5` FD gate is no longer treated as a
  principled statistical or truncation-error threshold.
- Proxy metric risk controlled: accepted limited FD is only a continuation
  gate; score identity remains the Phase 4 validation question.
- Hidden assumption corrected: the owner-requested score-identity finite-sample
  screen is `2 sample SD`; stricter `2 SE` z-scores are advisory diagnostics.
- Runtime boundary preserved: Phase 4 remains CPU-only and GPU/XLA/HMC are
  still deferred to reviewed later phases.

Actions:

- Added an owner acceptance amendment to the Phase 3 result.
- Reopened Phase 4 from blocker-only to executable score-identity validation.
- Preserved the Phase 4 blocker result as historical context to be superseded
  after executable Phase 4 runs.

Gate status:

- `P91_PHASE3_LIMITED_FD_OWNER_ACCEPTED_FOR_CONTINUATION_WITH_CAVEATS`
- `P91_PHASE4_EXECUTABLE_SUBPLAN_REVIEWED_AGREE`
- `P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY_PASS_PENDING_REVIEW`

Next action:

- Send the Phase 4 result and refreshed Phase 5 subplan to bounded Claude
  read-only review.

### 2026-06-29 - Phase 4 Local Execution Complete / Pending Review

Evidence contract:

- Question: Does the implemented local Zhao-Cui SIR d18 component score have
  empirical zero-mean behavior at true parameters across multiple simulated
  regimes/seeds?
- Baseline/comparator: data simulated from each `theta_0`; theoretical
  zero-mean score identity for the same local complete-data scalar components.
- Primary criterion: every regime/component satisfies `abs(mean score) <=
  2 * sample_standard_deviation` across ten seeds.
- Veto diagnostics: exact-likelihood proof claim, full observed-data/filtering
  score-identity claim, hidden previous-marginal/fixed-TTSIRT blocker, strict
  `2 SE` gate substitution, nonfinite scores, or aggregate-only masking.
- Non-claims: no exact likelihood proof, full filtering-score identity,
  GPU/XLA readiness, HMC readiness, package/release/CI readiness,
  default-policy change, or production readiness.

Actions:

- Claude reviewed the refreshed executable Phase 4 subplan: `VERDICT: AGREE`.
- Added `tests/highdim/test_p91_score_identity.py`.
- Ran Phase 4 local checks:
  `git diff --check` passed; CPU-only pytest passed
  `2 passed, 2 warnings in 14.60s`.
- Manifest status:
  `PASS_P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY`.
- Wrote Phase 4 local-check output and Phase 4 result.
- Refreshed Phase 5 subplan entry conditions to use Phase 3 limited-FD
  acceptance with caveats plus Phase 4 local component-score identity.

Artifacts:

- `tests/highdim/test_p91_score_identity.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-local-check-output-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-subplan-2026-06-29.md`

Gate status:

- `P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY_LOCAL_PASS_PENDING_REVIEW`

Next action:

- Send Phase 4 result and refreshed Phase 5 subplan to one-path bounded Claude
  read-only review.

### 2026-06-29 - Phase 4 Review Closed / Phase 5 Executed

Evidence contract:

- Question: Can HMC-facing local complete-data Zhao-Cui SIR d18 value/score
  paths compile and run on GPU/XLA in trusted context?
- Baseline/comparator: Phase 2 single/batched API semantics, Phase 4 local
  complete-data score-identity setup, and CPU parity between the new
  XLA-oriented helper and the existing eager local complete-data value plus
  tape-derived parameter score.
- Primary criterion: single and batched local complete-data value/score
  functions JIT compile and execute on `/GPU:0` with finite outputs, finite
  scores, GPU output devices, stable post-warmup tracing counts, and no OOM.
- Veto diagnostics: non-escalated GPU evidence, no TensorFlow GPU device, CPU
  output device for compiled tensors, compile failure, NaN/Inf, OOM,
  post-warmup retracing, or compile capability treated as speed/scientific
  evidence.
- Non-claims: no full observed-data/filtering score identity,
  previous-marginal/fixed-TTSIRT derivative readiness, GPU speed superiority,
  benchmark pass, HMC posterior validity, packaging/default readiness, or
  production readiness.

Skeptical audit result:

- Wrong-baseline risk reduced by adding a CPU-only parity test comparing the
  XLA-oriented helper value/score against the existing eager local
  complete-data value/score before interpreting GPU runtime.
- Proxy-metric risk controlled: compile success is recorded only as a GPU/XLA
  capability pass, not a benchmark, HMC, posterior, or production pass.
- Hidden CPU fallback risk controlled by trusted execution, forced `/GPU:0`,
  output-device recording, and TensorFlow GPU probe.
- Retracing risk controlled by fixed input signatures and stable post-warmup
  `experimental_get_tracing_count()`.

Actions:

- Claude reviewed refreshed exact-command Phase 5 subplan iteration 1:
  `VERDICT: REVISE`.
- Patched retracing criterion, manifest schema, and touched-file boundary.
- Claude reviewed Phase 5 subplan iteration 2: `VERDICT: AGREE`.
- Added CPU parity test to guard against compiling the wrong scalar.
- Claude reviewed parity amendment iteration 1: `VERDICT: REVISE`.
- Patched the exact `git diff --check` command to include the parity test.
- Claude reviewed focused parity-command repair: `VERDICT: AGREE`.
- Added XLA-oriented local complete-data helpers in
  `bayesfilter/highdim/models.py` and highdim-only exports.
- Added `tests/highdim/test_p91_gpu_xla_local_target.py`.
- Added trusted GPU/XLA manifest-writing harness:
  `scripts/p91_gpu_xla_jit_check.py`.
- Local checks passed: diff hygiene, py_compile, and CPU-only focused pytest
  `4 passed, 2 warnings in 16.83s`.
- Trusted `nvidia-smi` passed.
- Trusted TensorFlow GPU/XLA harness passed with status
  `PASS_P91_PHASE5_GPU_XLA_JIT_LOCAL_COMPLETE_DATA`.
- Wrote Phase 5 result and refreshed Phase 6 benchmark subplan.

Artifacts:

- `bayesfilter/highdim/models.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p91_gpu_xla_local_target.py`
- `scripts/p91_gpu_xla_jit_check.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-subplan-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-subplan-2026-06-29.md`

Gate status:

- `PASS_P91_PHASE5_GPU_XLA_JIT_LOCAL_COMPLETE_DATA_PENDING_RESULT_REVIEW`

Next action:

- Send Phase 5 result and refreshed Phase 6 subplan to one-path bounded Claude
  read-only review.

### 2026-06-29 - Phase 6 Local/GPU Execution Complete / Pending Review

Evidence contract:

- Question: Are CPU/GPU single/batched Zhao-Cui performance profiles
  acceptable and model-specific recommendations evidence-backed?
- Baseline/comparator: CPU single route, CPU batched route, trusted GPU/XLA
  single route, and trusted GPU/XLA batched route on the same deterministic
  local complete-data fixture.
- Primary criterion: all cells complete with finite outputs/scores, no OOM, no
  retries, no post-warmup retracing, explicit compile/warmup versus steady
  timing, and no closed-rule pathology.
- Veto diagnostics: universal GPU-speed claim, untrusted GPU evidence, missing
  XLA status for GPU, missing compile/steady separation, hidden OOM/retry,
  closed-rule pathology, or benchmark treated as scientific validity.
- Non-claims: no score identity proof, exact likelihood correctness, HMC
  posterior validity, universal GPU speed superiority, packaging/default
  readiness, or production readiness.

Skeptical audit result:

- Artifact ambiguity resolved through split CPU/GPU manifests plus exact merge
  command producing the final benchmark JSON.
- Pathology criteria are closed-rule and apply to any evaluated cell.
- GPU command explicitly uses `--xla true`; GPU evidence is trusted/escalated.
- Speed is treated as model/fixture-specific engineering evidence only.

Actions:

- Claude reviewed Phase 6 subplan iteration 1: `VERDICT: REVISE`.
- Patched artifact names, pathology criterion, manifest fields, and XLA
  command semantics.
- Claude reviewed Phase 6 subplan iteration 2: `VERDICT: REVISE`.
- Patched exact merge command and closed pathology vetoes.
- Claude reviewed Phase 6 subplan iteration 3: `VERDICT: REVISE`.
- Patched explicit post-warmup retrace-status manifest requirement.
- Claude reviewed Phase 6 subplan iteration 4: `VERDICT: AGREE`.
- Added benchmark harness: `scripts/p91_performance_benchmark.py`.
- Local implementation checks passed: diff hygiene and py_compile.
- CPU benchmark passed with status `PASS_P91_PHASE6_CPU_BENCHMARK`.
- Trusted `nvidia-smi` passed.
- Trusted GPU/XLA benchmark passed with status
  `PASS_P91_PHASE6_GPU_XLA_BENCHMARK`.
- Final merge passed with status `PASS_P91_PHASE6_PERFORMANCE_BENCHMARK`.
- Wrote Phase 6 result and refreshed Phase 7 subplan.

Artifacts:

- `scripts/p91_performance_benchmark.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-cpu-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-gpu-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-subplan-2026-06-29.md`

Gate status:

- `PASS_P91_PHASE6_PERFORMANCE_BENCHMARK_PENDING_RESULT_REVIEW`

Next action:

- Send Phase 6 result and refreshed Phase 7 subplan to one-path bounded Claude
  read-only review.

### 2026-06-29 - Phase 7 Local/GPU Execution Complete / Pending Review

Evidence contract:

- Question: Can the local complete-data Zhao-Cui SIR d18 target component
  survive a tiny trusted GPU/XLA TFP HMC implementation smoke?
- Baseline/comparator: Phase 5 GPU/XLA local target capability and Phase 6
  model-specific CPU/GPU/batched execution evidence.
- Primary criterion: compiled HMC returns finite samples, target values,
  scalar per-sample gradients, and log-accept ratios on GPU devices, with no
  OOM, retry, or post-warmup retracing.
- Veto diagnostics: untrusted GPU evidence, XLA disabled, nonfinite
  target/sample/gradient/log-accept output, missing GPU output devices, OOM,
  retry, post-warmup retrace, or overclaiming posterior/exact-likelihood/full
  filtering/production readiness.
- Non-claims: no posterior correctness, convergence, exact likelihood
  correctness, full observed-data/filtering HMC target readiness,
  package/default readiness, or production readiness.

Actions:

- Ran Phase 7 local checks: diff hygiene and CPU-only py_compile passed.
- Trusted `nvidia-smi` passed.
- Initial trusted GPU/XLA HMC smoke compiled and ran but blocked on
  `sample gradients nonfinite`.
- Diagnosed the failure as a smoke-harness diagnostic bug: the batched wrapper
  returned finite values but a disconnected gradient in this TensorFlow
  context; scalar value/gradient checks at the same theta points were finite.
- Patched `scripts/p91_hmc_smoke.py` so post-sample diagnostics compute scalar
  value/gradient pairs per sampled theta while leaving the HMC target
  unchanged.
- Reran local checks; both passed.
- Reran trusted GPU/XLA HMC smoke; final manifest status
  `PASS_P91_PHASE7_HMC_SMOKE`.
- Wrote Phase 7 result and refreshed Phase 8 doc-only packaging/release
  subplan.

Artifacts:

- `scripts/p91_hmc_smoke.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-subplan-2026-06-29.md`

Gate status:

- `PASS_P91_PHASE7_HMC_SMOKE_PENDING_RESULT_REVIEW`

Next action:

- Send Phase 7 result and refreshed Phase 8 subplan to one-path bounded Claude
  read-only review.

### 2026-06-29 - Phase 7 Review Closed / Phase 8 Ready

Actions:

- Claude reviewed Phase 7 result: `VERDICT: AGREE`.
- Claude reviewed refreshed Phase 8 subplan: `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-subplan-2026-06-29.md`

Gate status:

- `P91_PHASE7_REVIEWED_HMC_SMOKE_CLOSED`
- `P91_PHASE8_SUBPLAN_REVIEWED_AGREE`
- `P91_PHASE8_READY`

Next action:

- Execute Phase 8 doc/API/test-inventory checks, write the release-note draft,
  Phase 8 result, and refreshed Phase 9 final-decision subplan.

### 2026-06-29 - Phase 8 Local Execution Complete / Pending Review

Evidence contract:

- Question: Are packaging notes, CI split, release notes, caveats, and
  default-readiness recommendation prepared without overclaiming P91 evidence?
- Baseline/comparator: reviewed P91 phase results and repository public API/CI
  conventions.
- Primary criterion: release artifacts explicitly state validation
  scope/caveats, smoke versus deliberate GPU/HMC checks, model-specific
  CPU/GPU recommendations, and final Phase 9 authority.
- Veto diagnostics: exact likelihood claim, posterior correctness claim,
  universal GPU-speed claim, missing score/FD/HMC caveat, unauthorized
  package/release/CI/default action, or production promotion in Phase 8.
- Non-claims: no package publication, release tagging, CI mutation,
  default-policy change, final production promotion, exact likelihood
  correctness, posterior correctness, full observed-data/filtering score
  identity, or universal GPU superiority.

Actions:

- Ran Phase 8 required document/API/caveat inventories after a preliminary
  missing-optional-config `rg` command was replaced with existing-file checks.
- Ran optional CPU-only compile checks for the three P91 runtime harnesses
  because the release draft names those harnesses.
- Ran optional CPU-only focused pytest:
  `7 passed, 2 warnings in 8.40s`.
- Wrote release-note draft.
- Wrote Phase 8 result.
- Refreshed Phase 9 final-decision subplan.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-release-notes-draft-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-subplan-2026-06-29.md`

Gate status:

- `PASS_P91_PHASE8_PACKAGING_RELEASE_NOTES_PENDING_REVIEW`

Next action:

- Send release-note draft, Phase 8 result, and refreshed Phase 9 subplan to
  one-path bounded Claude read-only review.

### 2026-06-29 - Phase 8 Review Closed / Phase 9 Ready

Actions:

- Claude reviewed release-note draft iteration 1: `VERDICT: REVISE`.
- Patched the release-note draft to make support scope-first, add
  plain-language glosses, clarify artifact-level `Passed`, and preserve
  Phase 9 final authority.
- Claude reviewed release-note draft iteration 2: `VERDICT: AGREE`.
- Claude reviewed Phase 8 result: `VERDICT: AGREE`.
- Claude reviewed refreshed Phase 9 subplan: `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-release-notes-draft-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-subplan-2026-06-29.md`

Gate status:

- `P91_PHASE8_REVIEWED_PACKAGING_RELEASE_NOTES_CLOSED`
- `P91_RELEASE_NOTES_DRAFT_REVIEWED_AGREE`
- `P91_PHASE9_SUBPLAN_REVIEWED_AGREE`
- `P91_PHASE9_READY`

Next action:

- Execute Phase 9 final document checks, write final decision/reset memo, and
  update the final stop handoff.

### 2026-06-29 - Phase 9 Local Execution Complete / Pending Final Review

Evidence contract:

- Question: What is the final P91 production decision for Zhao-Cui SIR d18?
- Baseline/comparator: reviewed P91 phase results, P90 blocked baseline, and
  owner P91 amendments.
- Primary criterion: decision exactly reflects upstream pass/blocker statuses
  and promotes only if every required scoped P91 gate passed.
- Veto diagnostics: missing blocker, unsupported exact likelihood/posterior/GPU
  default claim, release/default action without authority, or proxy metric
  promoted across ledgers.
- Non-claims: no exact likelihood correctness, posterior correctness,
  convergence, full observed-data/filtering HMC readiness, full source-route
  derivative readiness, universal GPU speed superiority, package publication,
  release tagging, CI-service mutation, or default-policy change.

Actions:

- Ran Phase 9 document inventory and caveat checks.
- Ran P91 document diff hygiene.
- Read old stop handoff and found it stale at the Phase 4 reopened state.
- Wrote final scoped production decision.
- Wrote reset memo.
- Replaced stale stop handoff with current Phase 9 state.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-reset-memo-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-stop-handoff-2026-06-29.md`

Gate status:

- `P91_SCOPED_PRODUCTION_READY_PENDING_FINAL_REVIEW`

Next action:

- Send final decision, reset memo, and stop handoff to one-path bounded Claude
  read-only review.

### 2026-06-29 - Phase 9 Final Review Closed / P91 Closed

Actions:

- Claude reviewed Phase 9 final decision iteration 1: `VERDICT: REVISE`.
- Patched the Phase 9 final decision to path-resolve every phase evidence
  artifact, both ledgers, the reset memo, stop handoff, and document-only wall
  time.
- Claude reviewed Phase 9 final decision iteration 2: `VERDICT: AGREE`.
- Claude reviewed the P91 reset memo: `VERDICT: AGREE`.
- Claude reviewed the P91 stop handoff: `VERDICT: AGREE`.
- Patched closeout statuses from pending final review to closed scoped
  production-ready.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-reset-memo-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-stop-handoff-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-claude-review-ledger-2026-06-29.md`

Gate status:

- `P91_SCOPED_PRODUCTION_READY_CLOSED`

Closed scope:

- highdim subpackage API and local complete-data Zhao-Cui SIR d18 component
  route.

Preserved nonclaims:

- no exact likelihood correctness;
- no posterior correctness or convergence;
- no full observed-data/filtering score identity;
- no full source-route FD derivative readiness;
- no universal GPU superiority;
- no package publication, release tagging, CI-service mutation, root export, or
  default-policy change.
