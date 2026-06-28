# SVD-Nystrom No-HMC Promotion Visible Execution Ledger

Date: 2026-06-25

Status: `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`

## Ledger

### 2026-06-25 - Program Draft

Evidence contract:

- Question: can fixed SVD-Nystrom be promoted to a bounded internal
  default-candidate recommendation without HMC readiness?
- Baseline/comparator: exact Kalman for LGSSM and compiled streaming TF32 DPF
  route elsewhere.
- Primary criterion: P01-P07 hard gates pass and P08 review converges without
  unsupported claims.
- Veto diagnostics: wrong baseline, deterministic invalidity, exact-reference
  failure, active-path NumPy, dense materialization, GPU/TF32 mismatch,
  malformed artifacts, unsupported claims, or review nonconvergence.
- Nonclaims: no HMC readiness, statistical superiority, dense equivalence,
  public API/package release, funding/product claim, or broad scientific
  validity.

Actions:

- Drafted master program, visible runbook, phase subplans, review ledger, and
  stop handoff.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-master-program-2026-06-25.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-gated-execution-runbook-2026-06-25.md`

Gate status:

- `DRAFT_LOCAL_REVIEW_REQUIRED`

Next action:

- Run local document checks and exact-path Claude read-only review before P00
  execution.

### 2026-06-25T02:08:03+08:00 - P00 Governance Closed

Skeptical audit:

- Wrong baseline: no model comparison in P00; non-LGSSM comparator language was
  repaired to no-regression/operational-viability scope.
- Proxy metrics: none used in P00.
- Stop conditions: repaired to explicit predecessor-gated execution.
- Hidden assumptions: HMC remains excluded as a gate and claim.
- Environment mismatch: no GPU/model-suite execution in P00.
- Artifact mismatch: repaired with phase ownership and in-flight ledger/handoff
  custody.

Local checks:

- Required files exist: PASS.
- Required subplan headings exist: PASS.
- Detached execution ban present: PASS.
- HMC/default/scientific boundary terms are nonclaims/forbidden claims: PASS.

Claude review:

- P00-R1 broad prompt produced empty output; probe returned
  `CLAUDE_PROBE_OK`.
- P00-R1b: `VERDICT: REVISE`; patched predecessor gating,
  no-regression/operational-viability comparator scope, and artifact ownership.
- P00-R2: `VERDICT: REVISE`; patched in-flight custody of execution ledger,
  stop handoff, and material Claude-review-ledger updates.
- P00-R3: `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p00-governance-result-2026-06-25.md`
- `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/claude-review-r3-ownership.log`

Gate status:

- `P00_PASS_TO_P01_SCOPE_INVENTORY`

Next action:

- Launch P01 scope, inventory, and local harness-readiness checks.

### 2026-06-25T02:13:36+08:00 - P01 Scope Inventory Closed

Skeptical audit:

- Wrong baseline: P01 used P06/P07 entry evidence only; no model comparison was
  interpreted.
- Proxy metrics: file inventory and local tests were used only for harness
  readiness, not promotion.
- Stop conditions: P02 remains blocked unless P01 pass handoff is emitted.
- Hidden assumptions: P02 known gap is explicit; low-rank LGSSM evidence cannot
  be substituted for a fair SVD-Nystrom LGSSM exact-reference gate.
- Environment mismatch: focused tests intentionally hid GPU with
  `CUDA_VISIBLE_DEVICES=-1`.
- Artifact mismatch: inventory JSON and P01 result were written.

Checks:

- P06 summary parsed: `P06_PASS_TO_P07_EVIDENCE_PACKAGE`, `14/14`
  deterministic-valid, `0/14` exceedances, CP upper
  `0.1926361756501353 <= 0.20`.
- P07 closeout parsed: status/nonclaims present.
- SVD-Nystrom compiled-redo metadata and transport SVD solver surfaces present.
- Focused local tests: `16 passed` in `30.86s`.

Artifacts:

- `docs/benchmarks/svd-nystrom-nohmc-promotion-p01-scope-inventory-2026-06-25.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p01-scope-inventory-result-2026-06-25.md`
- `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/p01-focused-local-tests.log`

Gate status:

- `P01_PASS_TO_P02_LGSSM_REFERENCE`

Next action:

- Launch P02 trusted GPU preflight and exact-reference LGSSM harness assessment.

### 2026-06-25T02:34:54+08:00 - P02 LGSSM Exact-Reference Blocker

Skeptical audit:

- Wrong baseline: P02 used exact Kalman reference; streaming was not treated as
  the primary baseline.
- Proxy metrics: runtime and residual magnitudes were explanatory except hard
  finite/residual/reference gates.
- Stop conditions: trusted GPU/TF32 nonfinite output is a deterministic
  blocker; P03 must not run.
- Unfair comparison: CPU and GPU-no-TF32 diagnostics are diagnostic only
  because the default target is GPU/TF32.
- Hidden assumptions: the low-rank LGSSM harness was not reused as SVD evidence;
  a dedicated SVD-Nystrom harness was added and tested.
- Environment mismatch: trusted `nvidia-smi` selected physical GPU1; GPU1 was
  used for the default-target run.

Checks and diagnostics:

- Trusted preflight: GPU1 available at launch.
- New harness local tests: `4 passed`.
- CPU shape artifact: PASS.
- GPU1 TF32 enabled, XLA enabled: FAIL with nonfinite route output, factors,
  and particles.
- CPU TF32-disabled same policy: PASS.
- GPU1 TF32-disabled same policy: PASS.
- GPU1 TF32 enabled, XLA disabled, diagnostics disabled: FAIL before artifact
  with CUDA `gesvd` error in actual SVD core.

Artifacts:

- `docs/benchmarks/benchmark_svd_nystrom_lgssm_kalman_gate.py`
- `tests/test_svd_nystrom_lgssm_kalman_gate.py`
- `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-lgssm-reference-small-gpu1-2026-06-25.json`
- `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-lgssm-reference-small-gpu1-tf32disabled-2026-06-25.json`
- `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-lgssm-reference-small-cpu-diagnostic-2026-06-25.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02-lgssm-reference-result-2026-06-25.md`

Gate status:

- `P02_DETERMINISTIC_BLOCKER_GPU_TF32_SVD_NONFINITE`

Next action:

- Stop visible gated execution and draft/review a P02 repair subplan for the
  SVD-Nystrom GPU/TF32 numerical path. Do not launch P03.

### 2026-06-25T03:05:27+08:00 - P02A Repair Diagnostic Pre-Run Audit

Skeptical audit:

- Wrong baseline: the comparator remains the failed P02 GPU/TF32 SVD run;
  CPU and GPU-no-TF32 passes are explanatory controls only.
- Proxy metrics: runtime and core-spectrum metadata are explanatory; the
  decision is finite GPU/TF32 route output, exact-reference thresholds, no
  dense materialization, and matching policy metadata.
- Stop conditions: P03 remains blocked unless P02A repair passes and P02 is
  rerun successfully; another GPU/TF32 nonfinite result is a repair blocker.
- Unfair comparison: no CPU/no-TF32 result will be substituted for the default
  GPU/TF32 target.
- Hidden assumptions: this diagnostic tests the bounded local precision-island
  candidate only and does not authorize rank, epsilon, kernel, scaling, or
  default-policy changes.
- Environment mismatch: trusted GPU preflight found GPU1 saturated, so the
  diagnostic will use GPU0 under the owner rule "GPU1 if available, otherwise
  GPU0".
- Artifact mismatch: command stdout/stderr will be captured in the P02A log and
  pass/fail evidence will be preserved in JSON and markdown benchmark artifacts.

Evidence contract:

- Question: can the bounded factor/core precision-island repair make the
  SVD-Nystrom route finite and exact-reference-valid under GPU/TF32?
- Baseline/comparator: failed P02 GPU/TF32 artifact plus passing CPU/GPU-no-TF32
  diagnostics as controls.
- Primary criterion: repaired GPU/TF32 run status `PASS`, no hard vetoes,
  finite route outputs/factors/particles, exact-reference thresholds pass,
  `core_solver=svd_truncated`, TF32 execution recorded, and no dense transport
  materialization.
- Veto diagnostics: nonfinite output or factors, CUDA solver error, policy
  mismatch, dense materialization, missing metadata, or unsupported default or
  scientific claim.
- Explanatory diagnostics: runtime, memory, residual magnitudes, and core
  metadata.
- Not concluded: no promotion, no statistical superiority, no HMC readiness,
  and no broad model-suite validity.

Next action:

- Launch the repaired GPU0 TF32 diagnostic for P02A.

### 2026-06-25T03:18:00+08:00 - P02A Repair Diagnostic Closed

Checks:

- Focused local tests after factor/core precision repair:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/p02a-local-tests-r3.log`,
  `6 passed`.
- Repaired GPU0 TF32 diagnostic:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p02a-lgssm-reference-small-gpu0-factorprecision-2026-06-25.json`.
- Artifact validation: status `PASS`, hard vetoes `[]`, TF32 recorded `True`,
  candidate core solver `svd_truncated`, finite output/factors/particles,
  exact-reference thresholds passed, and transport matrix materialized `False`.

Result:

- `P02A_REPAIR_PASS_TO_P02_RERUN`

Decision:

- The bounded factor/core precision-island repair is sufficient to rerun P02.
- This is not a promotion claim and does not authorize P03 by itself.

Next action:

- Rerun P02 LGSSM exact-reference gate with repaired code and locked policy,
  using GPU1 if available, otherwise GPU0.

### 2026-06-25T03:12:16+08:00 - Repaired P02 Rerun Pre-Run Audit

Skeptical audit:

- Wrong baseline: the primary comparator remains the exact Kalman LGSSM
  reference; original failed GPU/TF32 P02 is repair context only.
- Proxy metrics: runtime, ESS, and residual magnitudes are explanatory except
  where the P02 hard gate explicitly uses finite output, exact-reference
  thresholds, residual thresholds, route metadata, GPU/TF32 provenance, and no
  dense materialization.
- Stop conditions: P03 remains blocked unless this repaired P02 rerun emits
  `P02_PASS_TO_P03_ACTUAL_SIR_STRESS` and material repair review converges.
- Unfair comparison: CPU and no-TF32 controls are not substitutes for the
  default GPU/TF32 target.
- Hidden assumptions: the rerun uses the same locked candidate policy and does
  not retune rank, epsilon, kernel mode, scaling mode, or thresholds.
- Environment mismatch: trusted GPU preflight again found GPU1 saturated, so
  the repaired P02 rerun will use GPU0 under the owner rule.
- Artifact mismatch: the rerun will write fresh `p02-repaired-*` JSON,
  Markdown, and log artifacts, preserving the original failed P02 evidence.

Evidence contract:

- Question: does repaired fixed SVD-Nystrom pass the LGSSM exact-reference P02
  gate under GPU/TF32?
- Baseline/comparator: exact Kalman reference for `lgssm_small_exact_ref`.
- Primary criterion: top-level status `PASS`, hard vetoes `[]`, all rows pass
  deterministic validity and exact-reference thresholds, TF32 recorded, GPU
  outputs recorded, no dense transport materialization, and locked SVD-Nystrom
  policy metadata.
- Veto diagnostics: nonfinite output/factors/particles, exact-reference
  threshold failure, wrong route/policy metadata, GPU/TF32 mismatch, dense
  materialization, malformed artifact, or unsupported promotion/default claim.
- Explanatory diagnostics: runtime, ESS, residuals, factor/core diagnostics,
  and no-TF32/CPU deltas.
- Not concluded: no nonlinear/model-suite validity, no statistical superiority,
  no HMC readiness, no promotion.

Next action:

- Launch repaired P02 GPU0 TF32 exact-reference rerun.

### 2026-06-25T03:22:00+08:00 - Repaired P02 Rerun Closed

Checks:

- Repaired P02 rerun artifact:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-repaired-lgssm-reference-small-gpu0-2026-06-25.json`.
- Validation: status `PASS`, hard vetoes `[]`, TF32 recorded `True`, GPU output
  provenance recorded, locked candidate metadata present, finite
  output/factors/particles, exact-reference thresholds passed, and transport
  matrix materialized `False`.

Result:

- `P02_PASS_REPAIRED_PENDING_REVIEW_TO_P03_ACTUAL_SIR_STRESS`

Decision:

- P02 exact-reference gate is repaired and passes, but P03 remains blocked
  until bounded material repair review converges.

Next action:

- Run exact-path Claude read-only review of the P02A repair result and P02
  repaired rerun boundary, then update the review ledger.

### 2026-06-25T03:24:00+08:00 - Claude Repair Review Approval Blocker

Attempted action:

- Launch bounded Claude Opus/max-effort read-only review of the exact P02A,
  P02, and P03 handoff paths.

Result:

- The launch was rejected by the approval guard because transmitting these
  repair-review documents to the external Claude service was not covered by the
  earlier approval scope.

Decision:

- Do not attempt a workaround or narrower external disclosure without explicit
  path-scoped approval.
- P03 remains blocked until material repair review converges or the user
  explicitly changes the review requirement.

Required approval to continue:

- Permission for Claude Code to read and transmit the exact paths named in the
  next user-facing approval request for read-only review.

### 2026-06-25T03:41:41+08:00 - P02 Repair Review Converged

Claude review:

- P02A-R1b after user path-scoped approval: `VERDICT: REVISE`.
- Finding: P02A/P02 repair evidence was internally consistent, but P03 still
  carried stale deterministic-blocker/open-token text.
- Patch: synchronized P02A/P02/P03 around the explicit post-review handoff
  token `P02_REPAIR_REVIEW_AGREE_PASS_TO_P03_ACTUAL_SIR_STRESS`.
- P02A-R2 focused review: `VERDICT: AGREE`.

Result:

- `P02_REPAIR_REVIEW_AGREE_PASS_TO_P03_ACTUAL_SIR_STRESS`

Decision:

- P03 may now enter its own pre-run audit.
- No promotion, default switch, HMC readiness, statistical superiority, or
  broad scientific-validity claim is authorized.

Next action:

- Audit P03 actual-SIR stress subplan, select GPU by trusted preflight, and run
  the first P03 row only if the evidence contract is sufficient.

### 2026-06-25T03:50:00+08:00 - Standing Claude Review Approval Recorded

Approval scope:

- Same-lane read-only Claude review is approved for SVD-Nystrom no-HMC
  promotion files under `docs/plans`, `docs/benchmarks`, and `docs/plans/logs`
  whose filenames start with
  `bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion` or
  `svd-nystrom-nohmc-promotion`, plus directly referenced same-lane benchmark
  artifacts needed for phase-evidence review.

Boundary:

- No source-code reading, unrelated paths, credentials, model files, commands,
  edits, launched agents, or authorization of promotion/default/scientific/HMC
  product/funding boundaries.

Next action:

- Run bounded P03 subplan review under this standing approval.

### 2026-06-25T04:15:18+08:00 - P03 Subplan Review Converged And Pre-Run Audit Passed

Claude review:

- P03-R1: `VERDICT: REVISE`; residual thresholds, terminal artifacts, and
  objective scope needed repair.
- P03-R2: `VERDICT: REVISE`; residual thresholds and objective were fixed, but
  per-row artifacts still needed exact seed-specific pinning.
- P03-R3: `VERDICT: AGREE`; all per-row artifacts for seeds `83000..83029` are
  fully pinned, command output paths map to the manifest, initial/reserved seed
  bounds are clear, and no new boundary-safety issue was found.

Focused local checks:

- No remaining `<JSON>`, `<MD>`, `<LOG>`, `seed<SEED>`, or P03 per-row wildcard
  placeholders in the P03 subplan.
- P03 per-row artifact manifest contains exactly 30 seed rows.

Skeptical audit:

- Wrong baseline: P03 compares the fixed SVD-Nystrom route against the
  same-artifact compiled streaming TF32 actual-SIR route as a no-regression
  value-route comparator, not as posterior truth.
- Proxy metrics: normalized log-likelihood delta is the predeclared bounded
  stress screen; runtime, memory, residual magnitudes, ESS, and factor/core
  diagnostics remain explanatory unless a deterministic threshold names them.
- Stop conditions: malformed artifacts, GPU/TF32 mismatch, seed overlap,
  policy/shape mismatch, nonfinite output, residual/log-weight threshold
  failure, missing SVD metadata, third exceedance, and unapproved scope changes
  are stops.
- Unfair comparison: shape, seeds, candidate policy, dtype, TF32 mode,
  transport policy, harness, and selected physical GPU are frozen before row
  execution.
- Hidden assumptions: passing P03 supports only fresh actual-SIR stress
  viability and cannot authorize default promotion, posterior correctness,
  HMC readiness, statistical superiority, or broad scientific validity.
- Stale context: P03 now uses the compiled-redo harness and repaired
  SVD-Nystrom GPU/TF32 precision path; the old Python-loop harness and old P02
  blocker token are not execution evidence.
- Environment mismatch: trusted GPU preflight is still required immediately
  before launch; use GPU1 if suitable, otherwise GPU0.
- Artifact fit: the seed-specific JSON, Markdown, and log artifacts plus the
  aggregate summary/result answer the P03 question and preserve row-by-row gate
  evidence.

Evidence contract:

- Question: does fixed SVD-Nystrom remain viable on a fresh same-shape
  actual-SIR stress panel beyond P06?
- Baseline/comparator: same-artifact compiled streaming TF32 actual-SIR route.
- Primary criterion: deterministic validity and one-sided 95% Clopper-Pearson
  upper bound for `Pr(abs(delta)/(T*M)>0.03)` is `<= 0.20`.
- Veto diagnostics: deterministic invalidity, seed reuse, GPU/TF32 mismatch,
  shape/policy mismatch, missing SVD metadata, malformed artifacts,
  `max_row_residual > 5.0e-2`, `max_column_residual > 5.0e-2`,
  `final_logsumexp_residual > 1.0e-5`, or third-exceedance futility.
- Explanatory diagnostics: runtime, memory, normalized deltas, residuals, ESS,
  and factor/core diagnostics.
- Not concluded: no non-actual-SIR validity, no default promotion, no
  posterior correctness, no statistical superiority, no HMC readiness.

Gate status:

- `P03_PRE_RUN_AUDIT_PASS_READY_FOR_ROW83000`

Next action:

- Run trusted GPU preflight, then launch only seed `83000` using the exact P03
  manifest paths.

### 2026-06-25T05:05:00+08:00 - P03 Actual-SIR Stress Closed

Result:

- P03 emitted `P03_PASS_TO_P04_NONLINEAR_GAUSSIAN`.
- Initial rows `83000..83013` ran on trusted GPU0 because GPU1 was saturated.
- Deterministic-valid rows: `14/14`.
- Exceedances of `abs(delta)/(T*M) > 0.03`: `0`.
- One-sided 95% Clopper-Pearson upper bound: `0.19263617565013536 <= 0.20`.
- Max normalized absolute delta: `0.00100606282552083`.
- Max row residual: `9.97781753540039e-05`.
- Max column residual: `3.814697265625e-06`.
- Max final logsumexp residual: `9.5367431640625e-07`.

Artifacts:

- `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-summary-2026-06-25.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p03-actual-sir-stress-result-2026-06-25.md`

Claude review:

- P03 result plus refreshed P04 subplan review:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/claude-review-p03-result-p04-subplan-r1.log`
- Verdict: `VERDICT: AGREE`.

Decision:

- P04 may enter its harness implementation/local-test gate.
- No default promotion, posterior correctness, statistical superiority, HMC
  readiness, or broad scientific-validity claim is authorized.

### 2026-06-25T05:19:27+08:00 - P04 Harness Local Tests Passed

Local source-level review:

- The P04 harness and focused tests were reviewed locally because the current
  Claude approval explicitly forbids Claude Code from reading source code.
- Review note:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-harness-local-review-2026-06-25.md`

Focused checks:

- `py_compile` for the harness and focused test: PASS.
- Focused local pytest log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-local-tests.log`
- Pytest result: `4 passed, 14508 warnings in 16.37s`.

Skeptical audit:

- Wrong baseline: P04 uses same-artifact compiled streaming DPF, not a
  sigma-point or UKF proxy.
- Proxy metrics: normalized log-likelihood delta is only the predeclared P04
  screen; timing and residual magnitudes remain descriptive except where
  thresholds are explicitly hard vetoes.
- Stop conditions: invalid harness, malformed artifact, GPU/TF32 mismatch,
  dense materialization, residual/log-weight/ESS failure, post-hoc threshold or
  candidate change, and any exceedance remain stops or repair triggers.
- Unfair comparison: fixture, seed, dtype, TF32, route policy, candidate, and
  artifact schema are fixed before any GPU row.
- Hidden assumption: one nonlinear Gaussian fixture cannot authorize broad
  nonlinear validity, default promotion, posterior correctness, HMC readiness,
  or statistical superiority.
- Environment mismatch: trusted GPU preflight remains required before seed
  `84000`; use GPU1 if suitable, otherwise GPU0.
- Artifact fit: exact P04 per-row JSON, Markdown, and log paths are pinned in
  the subplan.

Gate status:

- `P04_HARNESS_LOCAL_TESTS_PASS_PENDING_CLAUDE_ARTIFACT_REVIEW`

Next action:

- Run bounded Claude artifact-level review of the P04 subplan, local harness
  review note, P04 test log, and P03 result. Do not send harness or test source
  code to Claude. If review agrees, run trusted GPU preflight and launch only
  P04 seed `84000`.

### 2026-06-25T05:24:00+08:00 - P04 Artifact Review Converged

Claude review:

- Artifact review log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-claude-review-p04-artifact-r1.log`
- Scope: P04 subplan, P04 local harness review note, P04 local test log, P03
  result, and P03 summary only. Harness/test source code was explicitly
  excluded.
- Verdict: `VERDICT: AGREE`.

Review findings:

- Entry/handoff, evidence contract, exact per-row artifact gating, forbidden
  claims, and local-check artifact coverage are consistent.
- Review supports proceeding only to trusted GPU preflight and P04 seed
  `84000`, not to P04 interpretation or P05.
- Residual risk: GPU/TF32 readiness for P04 is unverified until trusted
  preflight; no P04 GPU row artifact exists yet.

Gate status:

- `P04_ARTIFACT_REVIEW_AGREE_READY_FOR_ROW84000_PREFLIGHT`

Next action:

- Run trusted GPU preflight, choose GPU1 if suitable and otherwise GPU0, and
  launch only P04 seed `84000` using the exact manifest paths.

### 2026-06-25T05:28:34+08:00 - P04 Seed 84000 Failed Quality Gate

Trusted GPU preflight:

- GPU0: 1192 MiB used of 32760 MiB, 39 percent utilization.
- GPU1: 18 MiB used of 32760 MiB, 0 percent utilization.
- Selected GPU1 under the owner rule "GPU1 if available, otherwise GPU0".

Execution:

- Command: P04 seed `84000`, `T=20`, `N=4096`, GPU1 visible as `/GPU:0`,
  `float32`, TF32 enabled, XLA enabled, locked candidate
  `rank=32`, `epsilon=0.5`, `raw`, `none`, `svd_truncated`, `rcond=1e-6`.
- Exit code: `1` because the harness wrote a structured `FAIL` artifact.
- Wall time: 95.3574289989192 seconds.

Artifact validation:

- JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5-2026-06-25.json`
- Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5-2026-06-25.md`
- Log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5.log`
- Schema: `svd_nystrom_range_bearing_gate.v1`.
- Status: `FAIL`.
- Top-level hard veto: `paired:paired_normalized_log_likelihood_delta`.
- Streaming row: `PASS`, hard vetoes `[]`.
- Nystrom row: `PASS`, hard vetoes `[]`.
- TF32 execution recorded: `True`.
- CUDA visible devices: `1`.
- Selected physical GPU argument: `1`.

Observed metrics:

- Streaming log likelihood: `27.30160140991211`.
- SVD-Nystrom log likelihood: `23.511123657226562`.
- Delta: `-3.790477752685547`.
- Normalized absolute delta: `0.09476194381713868`.
- Frozen threshold: `0.05`.
- Nystrom max row residual: `0.009805679321289062 <= 0.05`.
- Nystrom max column residual: `0.002088785171508789 <= 0.05`.
- Nystrom final logsumexp residual: `0.0 <= 1e-5`.
- ESS fraction min for both routes: `0.253101110458374 >= 0.005`.

Decision:

- P04 cannot pass because the first row exceeded the frozen zero-exceedance
  quality screen.
- Remaining P04 rows were not launched because no later rows can restore the
  required zero-exceedance criterion.
- This is a quality-gate failure for the locked candidate, not a GPU runtime
  failure or deterministic-validity failure.

Result artifacts:

- P04 summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-summary-2026-06-25.json`
- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-result-2026-06-25.md`
- P04A diagnostic subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04a-range-bearing-failure-diagnostic-subplan-2026-06-25.md`

Gate status:

- `P04_FAIL_OPTIONAL_OR_REPAIR_PENDING_P04A_REVIEW`

Next action:

- Run local checks on P04/P04A artifacts and bounded Claude artifact review of
  the P04 result plus P04A subplan. Do not execute P05.

### 2026-06-25T05:40:00+08:00 - P04A Subplan Review Converged

Local checks:

- P04 summary JSON parsed.
- P04 summary matched the P04 seed `84000` row artifact.
- P04A manifest and command-shape local check passed with four exact rows and
  no placeholder paths.

Claude review:

- Review log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-claude-review-p04-result-p04a-subplan-r1.log`
- Verdict: `VERDICT: AGREE`.
- Scope: P04 result, P04 summary, P04 seed row artifact, P04A subplan, and
  ledgers only; harness/test source code was explicitly excluded.

Review findings:

- P04 classification is consistent with the row artifact.
- P05 remains blocked.
- P04A is bounded, exact-artifact gated, statistically humble, and cannot
  backdoor promotion/default/scientific/HMC claims.
- Residual risk: preflight GPU memory and row-artifact GPU memory use different
  sampling times. This is provenance-accounting context, not a gate failure.

Gate status:

- `P04A_PLAN_REVIEW_AGREE_READY_FOR_PREFLIGHT`

Next action:

- Run trusted GPU preflight, choose GPU1 if suitable and otherwise GPU0, then
  run P04A diagnostic rows one at a time starting with `locked-rerun`.

### 2026-06-25T05:55:00+08:00 - P04A Diagnostics Completed

Trusted GPU preflight:

- GPU0: 1197 MiB used of 32760 MiB, 40 percent utilization.
- GPU1: 18 MiB used of 32760 MiB, 0 percent utilization.
- Selected GPU1 under the owner rule.

Rows:

| Row | Status | Normalized abs delta | Threshold | Deterministic route validity |
| --- | --- | ---: | ---: | --- |
| locked-rerun | `FAIL` | 0.09920544624328613 | 0.05 | PASS |
| rank64 | `FAIL` | 0.10152473449707031 | 0.05 | PASS |
| rank128 | `FAIL` | 0.09715399742126465 | 0.05 | PASS |
| eps1p0 | `FAIL` | 0.09851346015930176 | 0.05 | PASS |

Interpretation:

- The locked P04 failure reproduced.
- Simple rank controls (`64`, `128`) and the epsilon `1.0` control did not
  nominate a one-seed repair candidate.
- All rows were deterministic-valid, so this remains a quality-delta failure,
  not a runtime/GPU/TF32/residual/ESS failure.

Artifacts:

- P04A summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-diagnostic-summary-2026-06-25.json`
- P04A result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04a-range-bearing-failure-diagnostic-result-2026-06-25.md`

Gate status:

- `P04A_LOCKED_FAILURE_CONFIRMED_REPAIR_REQUIRED`

Next action:

- Stop the current promotion ladder. Do not execute P05 unless the owner
  explicitly approves a revised master program after a repair/candidate-freeze
  decision.

### 2026-06-25T06:05:00+08:00 - P04A Result Review Converged

Claude review:

- Review log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-claude-review-p04a-result-r1.log`
- Verdict: `VERDICT: AGREE`.

Review findings:

- P04A result matches the frozen diagnostic panel and exact row artifacts.
- Stop/handoff state is correct.
- P05 remains blocked.
- Statistical and nonclaim boundaries are preserved.
- Residual risks: threshold-level reproduction is not bitwise equality, and
  GPU memory snapshots use different sampling times.

Final stopped status:

- `P04A_LOCKED_FAILURE_CONFIRMED_REPAIR_REQUIRED_REVIEW_AGREE`

Next action:

- Await owner direction. The current promotion ladder must not execute P05.

### 2026-06-25T23:29:06+08:00 - P04/P04A Threshold Governance Correction Opened

Skeptical audit:

- Wrong baseline risk: the old P04/P04A interpretation compared observed
  nonlinear deltas against an uncalibrated `0.05` threshold instead of a
  reviewed nonlinear threshold-calibration rule.
- Proxy metric risk: the hardcoded paired delta was treated as a promotion
  gate before nonlinear scale extraction, threshold freeze, disjoint
  validation, and uncertainty analysis.
- Stop-condition repair: P05 remains blocked, but the active blocker is now
  threshold governance rather than calibrated method failure.
- Artifact fit: existing P04/P04A row JSON artifacts remain descriptive scale
  evidence because deterministic validity passed; their pass/fail labels are
  not calibration-grade nonlinear evidence.

Actions:

- Added P04B threshold-governance repair subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-subplan-2026-06-25.md`.
- Added P04C nonlinear threshold scale-extraction subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-subplan-2026-06-25.md`.
- Added correction sections to P04/P04A result artifacts.
- Updated master/runbook/stop status to point to uncalibrated nonlinear
  threshold governance.

Gate status:

- `P04_BLOCKED_UNCALIBRATED_NONLINEAR_THRESHOLD_PENDING_P04B_REVIEW`

Next action:

- Run local artifact/document checks and exact-path Claude review of P04B/P04C
  before writing P04B result. Do not execute P05.

### 2026-06-25T23:59:00+08:00 - P04B Governance Repair Closed

Local checks:

- P04 summary JSON parsed and confirmed `tau_component=0.05`.
- P04 deterministic route validity passed, with normalized absolute delta
  `0.09476194381713868`.
- P04A summary JSON parsed and confirmed diagnostic threshold `0.05`.
- P04A deterministic route validity passed for all four rows, with normalized
  absolute deltas in `[0.09715399742126465, 0.10152473449707031]`.
- Corrected P04/P04A result notes mark the old interpretation as historical
  and the active handoff as threshold-governance repair.

Claude review:

- P04B R1: `VERDICT: REVISE`; tightened handoff to require recorded local
  checks, explicit `VERDICT: AGREE`, exact P04C sections, inherited no-claims
  boundary, and positive replacement status.
- P04B R2 focused review: `VERDICT: AGREE`.
- P04C R1: `VERDICT: REVISE`; clarified invalid-row handling and no reduced
  calibration panel.
- P04C R2 focused review: `VERDICT: AGREE`.

Result:

- P04B result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-result-2026-06-25.md`

Gate status:

- `P04B_PASS_TO_P04C_NONLINEAR_THRESHOLD_SCALE_EXTRACTION`
- Active execution blocker: `P04C_BLOCKED_HARNESS_THRESHOLD_CONTROL_REQUIRED`

Next action:

- Repair/review the range-bearing benchmark harness so P04C scale extraction
  can run without the old hardcoded `0.05` paired veto acting as a pass/fail
  gate. Do not execute P05.

### 2026-06-26 - P04C0 Harness Threshold-Control Repair Closed

Skeptical audit:

- Wrong baseline: this repair compares old always-hard-veto harness behavior
  against explicit gate vs record-only control; it does not compare methods.
- Proxy metric: paired delta remains descriptive in P04C record-only mode and
  is not promoted to a calibrated threshold.
- Stop conditions: P04C remains forbidden if record-only mode is unavailable
  or if the historical `0.05` still acts as a P04C hard gate.
- Hidden assumption: preserving default `gate` behavior does not authorize P05
  or promote the candidate.
- Environment mismatch: focused tests intentionally used CPU-hidden tiny checks;
  P04C GPU evidence has not started.
- Artifact fit: P04C command shape now includes
  `--paired-threshold-mode record-only`.

Checks:

- `pytest -q tests/test_svd_nystrom_range_bearing_gate.py`: `6 passed` in
  `15.83s`.
- `python -m py_compile docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py tests/test_svd_nystrom_range_bearing_gate.py`: PASS.
- Default `gate` mode still emits paired hard veto on threshold exceedance.
- `record-only` mode suppresses only the paired hard veto and records
  descriptive threshold-role metadata.

Artifacts:

- `docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py`
- `tests/test_svd_nystrom_range_bearing_gate.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c0-harness-threshold-control-result-2026-06-26.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-subplan-2026-06-25.md`

Gate status:

- `P04C0_HARNESS_CONTROL_PASS_TO_P04C_PREFLIGHT`
- `P04C_READY_FOR_SCALE_EXTRACTION_PREFLIGHT_AFTER_HARNESS_REPAIR`

Next action:

- Run P04C trusted GPU preflight, then P04C calibration rows `84100..84111`
  one at a time in record-only paired-threshold mode. Do not execute P05,
  freeze a threshold, or make promotion/default/scientific/HMC claims.

### 2026-06-26 - P04C Scale Extraction Pre-Run Audit

Evidence contract:

- Question: what is the descriptive paired-delta scale for fixed SVD-Nystrom on
  the range-bearing fixture under deterministic-valid GPU/TF32 rows?
- Baseline/comparator: same-artifact compiled streaming TF32 DPF route.
- Primary criterion: all 12 calibration seeds `84100..84111` produce
  deterministic-valid row artifacts and an aggregate descriptive summary, with
  no threshold freeze or validation claim.
- Veto diagnostics: missing record-only threshold mode, historical `0.05`
  acting as a hard P04C gate, deterministic invalidity, malformed artifact,
  GPU/TF32 mismatch, route/policy mismatch, dense materialization, residual or
  log-weight or ESS failure, seed overlap, unsupported claim, or trusted GPU
  unavailability.
- Explanatory diagnostics: normalized paired deltas, descriptive quantiles,
  runtime, memory, residuals, ESS, and Nystrom factor/core diagnostics.
- Not concluded: no calibrated nonlinear threshold, no P04 pass/fail, no
  default promotion, no posterior correctness, no HMC readiness, no statistical
  superiority, and no broad nonlinear validity.

Skeptical audit:

- Wrong baseline: comparator remains same-artifact compiled streaming TF32 DPF;
  no exact-reference claim is made for this nonlinear fixture.
- Proxy metric: paired delta is scale-extraction evidence only and is not a
  promotion criterion in P04C.
- Missing stop conditions: stop on any invalid row or missing/malformed
  artifact; no reduced-panel pass is allowed.
- Unfair comparison: fixed fixture, shape, seeds, dtype, TF32 target,
  candidate policy, and artifact manifest are predeclared.
- Hidden assumption: seed variation is particle-seed variation under one fixed
  observation path, not broad nonlinear-model validity.
- Environment mismatch: trusted GPU preflight selected GPU1, with GPU1 at
  18 MiB used and 0 percent utilization.
- Artifact fit: P04C command shape includes
  `--paired-threshold-mode record-only`; rows will be parsed before launching
  the next seed.

Audit status:

- `PASS_FOR_P04C_GPU_SCALE_EXTRACTION_ROWS`

### 2026-06-26 - P04C Scale Extraction Blocked

Rows:

- Seed `84100`: PASS; record-only paired-threshold mode recorded; normalized
  paired delta `0.11204042434692382`; no hard vetoes.
- Seed `84101`: FAIL; record-only paired-threshold mode recorded; streaming
  comparator route emitted nonfinite log likelihood, filtered means, filtered
  variances, and ESS; SVD-Nystrom route passed deterministic checks.

Gate status:

- `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`

Interpretation:

- This is not a threshold exceedance failure and not evidence that the repaired
  threshold-control mode failed.
- The calibration panel is invalid because P04C required all 12 seeds to be
  deterministic-valid and allowed no reduced-panel pass.
- The observed blocker is in the streaming comparator artifact for seed
  `84101`; the Nystrom route passed on that seed.

Artifacts:

- P04C result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-result-2026-06-25.md`
- Seed `84100` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84100-r32-eps0p5-2026-06-25.json`
- Seed `84101` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84101-r32-eps0p5-2026-06-25.json`

Next action:

- Stop P04C and draft/review a separate streaming-comparator nonfinite
  diagnostic subplan or revised calibration design. Do not run remaining P04C
  seeds, do not launch P05, and do not freeze a nonlinear threshold.

### 2026-06-26 - P04C1 Streaming Nonfinite Diagnostic Pre-Run Audit

Local checks:

- P04C1 subplan required headings, handoff tokens, exact artifact paths, and
  forbidden-claim boundaries: PASS.
- P04C seed artifact parse: seed `84100` top-level `PASS`, streaming `PASS`,
  Nystrom `PASS`, `paired_threshold_mode=record-only`.
- P04C seed artifact parse: seed `84101` top-level `FAIL`, streaming `FAIL`
  with `nonfinite_log_likelihood`, `nonfinite_filtered_means`,
  `nonfinite_filtered_variances`, and `nonfinite_ess_by_time`; Nystrom `PASS`;
  `paired_threshold_mode=record-only`.
- The old uncalibrated `0.05` paired threshold remains record-only descriptive
  metadata and is not the P04C1 diagnostic gate.

Claude review:

- P04C1-R1: `VERDICT: REVISE`; fixed missing exact ledger/handoff paths and
  overstrong streaming-row wording.
- P04C1-R2: no verdict; stopped after oversized-artifact read/retry behavior.
- P04C1-R3: `VERDICT: AGREE`; focused review confirmed the R1 repairs.

Evidence contract:

- Question: is the seed `84101` streaming comparator nonfinite artifact
  reproducible, route-specific, and/or GPU/TF32/JIT-specific?
- Baseline/comparator: the P04C seed `84101` failed both-route artifact and
  the P04C seed `84100` passed artifact.
- Primary criterion: produce a diagnostic classification with exact row
  artifacts; do not resume calibration unless a later reviewed plan authorizes
  it.
- Veto diagnostics: malformed artifact, missing artifact, GPU/TF32 mismatch
  for GPU rows, route/policy mismatch, non-predeclared command change, source
  disclosure to Claude, unsupported claim, or need to change calibration
  pass/fail criteria after seeing diagnostics.
- Explanatory diagnostics: route finite status, log likelihood, ESS,
  per-route hard vetoes, runtime, GPU/CPU/JIT differences.
- Not concluded: no calibrated threshold, no repaired P04C panel, no seed
  exclusion, no SVD-Nystrom rejection, no default promotion, no posterior
  correctness, no HMC readiness, no statistical superiority, and no broad
  nonlinear validity.

Skeptical audit:

- Wrong baseline: P04C1 compares against the failed seed `84101` artifact and
  passing seed `84100` control, not against a threshold or promotion claim.
- Proxy metric: finite route status is a diagnostic validity check, not a
  method ranking.
- Missing stop conditions: artifact malformedness, GPU/TF32 mismatch, command
  drift, review nonconvergence, and calibration continuation are explicit
  stops.
- Unfair comparison: diagnostic rows are route/device/JIT controls and are not
  calibration rows.
- Hidden assumption: CPU/no-JIT finite output cannot substitute for GPU/TF32
  calibration evidence.
- Environment mismatch: GPU rows still require trusted preflight; use GPU1 if
  suitable, otherwise GPU0.
- Artifact fit: exact row artifacts and result/summary paths are named before
  execution.

Gate status:

- `P04C1_PLAN_REVIEW_AGREE_READY_FOR_PREFLIGHT`

Next action:

- Run trusted GPU preflight, then execute P04C1 diagnostic rows one at a time
  with JSON parsing after each row. Do not resume P04C seeds `84102..84111`,
  launch P05, freeze a threshold, or make promotion/default/scientific/HMC
  claims.

### 2026-06-26 - P04C1 Streaming Nonfinite Diagnostic Closed

Trusted GPU preflight:

- GPU0: 1242 MiB used of 32760 MiB, 23 percent utilization.
- GPU1: 18 MiB used of 32760 MiB, 0 percent utilization.
- Selected GPU1 under the owner rule "GPU1 if available, otherwise GPU0".

Rows:

| Row | Status | Route | Seed | Device / mode | Streaming hard vetoes | Nystrom status |
| --- | --- | --- | ---: | --- | --- | --- |
| `gpu-streaming-repro-84101` | `FAIL` | `streaming` | 84101 | GPU1, TF32 enabled, JIT on | `nonfinite_log_likelihood`, `nonfinite_filtered_means`, `nonfinite_filtered_variances`, `nonfinite_ess_by_time` | N/A |
| `gpu-both-repro-84101` | `FAIL` | `both` | 84101 | GPU1, TF32 enabled, JIT on | `nonfinite_log_likelihood`, `nonfinite_filtered_means`, `nonfinite_filtered_variances`, `nonfinite_ess_by_time` | `PASS` |
| `gpu-streaming-control-84100` | `PASS` | `streaming` | 84100 | GPU1, TF32 enabled, JIT on | `[]` | N/A |
| `cpu-streaming-control-84101` | `PASS` | `streaming` | 84101 | CPU hidden, TF32 disabled, JIT off | `[]` | N/A |

Interpretation:

- The seed `84101` streaming comparator nonfinite artifact is reproducible
  under GPU/TF32/JIT execution.
- The same seed remains deterministic-valid for the SVD-Nystrom route in the
  both-route repro.
- The passing seed `84100` GPU streaming control argues against a blanket
  streaming-route failure.
- The passing seed `84101` CPU/no-JIT/no-TF32 control argues against broad
  fixture or seed invalidity.
- P04C1 does not distinguish TF32, JIT/XLA, GPU kernel/device behavior, or
  their interaction; that is the P04C2 scope.

Artifacts:

- P04C1 summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-summary-2026-06-26.json`
- P04C1 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-result-2026-06-26.md`
- P04C2 draft subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-subplan-2026-06-26.md`

Gate status:

- `P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`

Next action:

- Run local checks and bounded Claude read-only review of P04C2 before any
  P04C2 GPU rows. Do not resume P04C seeds `84102..84111`, launch P05, freeze
  a threshold, or make promotion/default/scientific/HMC claims.

### 2026-06-26 - P04C2 Streaming GPU TF32/JIT Isolation Pre-Run Audit

Local checks:

- P04C2 subplan required headings, handoff tokens, exact artifact paths, and
  forbidden-claim boundaries: PASS.
- P04C1 result parsed/reviewed and emits
  `P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`.
- P04C1 aggregate summary parsed locally: calibration resume, threshold
  freeze, and promotion are not authorized.
- P04C2 row manifest contains exactly three JSON, three Markdown, and three log
  artifacts with no wildcard paths.
- P04C2 review scope now forbids Claude benchmark JSON, log, source, test, and
  unrelated-path reads unless separately authorized.

Claude review:

- P04C2-R1: `VERDICT: REVISE`; fixed over-broad Claude review scope and
  clarified P04C1 summary parsing as execution-side local evidence.
- P04C2-R2: `VERDICT: AGREE`; focused repair review converged.

Evidence contract:

- Question: which execution factor explains the seed `84101` streaming
  comparator nonfinite artifact: TF32, JIT/XLA, GPU/device behavior, or a
  TF32+JIT interaction?
- Baseline/comparator: P04C1 GPU/TF32/JIT-on seed `84101` streaming failure
  and P04C1 CPU/no-JIT/TF32-disabled seed `84101` streaming pass.
- Primary criterion: produce an isolation classification with exact row
  artifacts; do not resume calibration unless a later reviewed plan authorizes
  it.
- Veto diagnostics: malformed artifact, missing artifact, GPU/TF32/JIT
  mismatch, route/policy mismatch, non-predeclared command change, unsupported
  claim, or need to change calibration pass/fail criteria after seeing
  diagnostics.
- Explanatory diagnostics: route finite status, log likelihood, ESS,
  per-route hard vetoes, runtime, GPU/TF32/JIT differences.
- Not concluded: no calibrated threshold, no repaired P04C panel, no seed
  exclusion, no SVD-Nystrom rejection, no default promotion, no posterior
  correctness, no HMC readiness, no statistical superiority, and no broad
  nonlinear validity.

Skeptical audit:

- Wrong baseline: P04C2 compares against P04C1 reproduced failure and P04C1
  CPU/no-JIT pass, not against a threshold or promotion claim.
- Proxy metric: finite route status is a diagnostic validity check, not a
  method ranking.
- Missing stop conditions: artifact malformedness, GPU/TF32/JIT mismatch,
  command drift, review nonconvergence, and calibration continuation are
  explicit stops.
- Unfair comparison: diagnostic rows are execution-factor controls and are not
  calibration rows.
- Hidden assumption: no single factor will be named unless the predeclared row
  pattern supports it.
- Environment mismatch: GPU rows still require trusted preflight; use GPU1 if
  suitable, otherwise GPU0.
- Artifact fit: exact row artifacts and result/summary paths are named before
  execution.

Gate status:

- `P04C2_PLAN_REVIEW_AGREE_READY_FOR_PREFLIGHT`

Next action:

- Run trusted GPU preflight, then execute P04C2 diagnostic rows one at a time
  with JSON parsing after each row. Do not resume P04C seeds `84102..84111`,
  launch P05, freeze a threshold, or make promotion/default/scientific/HMC
  claims.

### 2026-06-26 - P04C2 Streaming GPU TF32/JIT Isolation Blocked

Executed row:

| Row | Status | Route | Seed | Device / mode | Structured artifact | Log |
| --- | --- | --- | ---: | --- | --- | --- |
| `gpu-tf32-nojit-84101` | `BLOCKED` | `streaming` | 84101 | GPU1, TF32 enabled, JIT off | missing JSON/Markdown | present |

The first P04C2 row exited code `1` before writing the required JSON and
Markdown artifacts. The log reports TensorFlow `InvalidArgumentError` from
`MatrixInverse` inside the streaming route with message `Input is not
invertible.`

Gate status:

- `P04C2_BLOCKED_INVALID_DIAGNOSTIC_ARTIFACT`

Interpretation:

- P04C2 did not produce a valid isolation classification.
- The traceback is explanatory only until the harness can serialize planned
  route exceptions as structured row evidence.
- This is not an SVD-Nystrom failure classification; the executed row was
  streaming-only.

Artifacts:

- P04C2 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-result-2026-06-26.md`
- P04C2A draft subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2a-harness-exception-artifact-repair-subplan-2026-06-26.md`

Next action:

- Review and execute P04C2A harness exception-artifact repair before rerunning
  any P04C2 rows. Do not resume P04C calibration seeds, launch P05, freeze a
  threshold, drop seed `84101`, or make promotion/default/scientific/HMC claims.

### 2026-06-26 - P04C2A Harness Exception Artifact Repair Closed

Plan review:

- Local skeptical audit: PASS.
- Claude P04C2A-R1: `VERDICT: AGREE`; exact P04C2A subplan plus exact P04C2
  result only, no source/test/log reads.

Implementation:

- Added explicit `--capture-route-exceptions` option to
  `docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py`.
- Default behavior remains to re-raise route exceptions.
- Opt-in capture writes structured row-level `FAIL` artifacts with
  `hard_vetoes: ["route_exception"]`.
- Paired comparability is not computed from exception rows.

Required local check:

```text
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_svd_nystrom_range_bearing_gate.py -q
8 passed, 14572 warnings in 17.16s
```

Gate status:

- `P04C2A_PASS_TO_P04C2_RERUN`

Artifacts:

- P04C2A result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2a-harness-exception-artifact-repair-result-2026-06-26.md`

Next action:

- Rerun P04C2 rows one at a time with `--capture-route-exceptions` added to
  the predeclared commands and parse each JSON before launching the next row.
  Do not resume P04C calibration seeds, launch P05, freeze a threshold, drop
  seed `84101`, or make promotion/default/scientific/HMC claims.

### 2026-06-26 - Repaired P04C2 Streaming GPU TF32/JIT Isolation Closed

Trusted GPU preflight:

- GPU0: 1226 MiB used of 32760 MiB, 40 percent utilization.
- GPU1: 18 MiB used of 32760 MiB, 0 percent utilization.
- Selected GPU1 under the owner rule "GPU1 if available, otherwise GPU0".

Rows:

| Row | Status | Route | Seed | Device / mode | Route hard vetoes |
| --- | --- | --- | ---: | --- | --- |
| `gpu-tf32-nojit-84101` | `FAIL` | `streaming` | 84101 | GPU1, TF32 enabled, JIT off | `route_exception` |
| `gpu-notf32-jit-84101` | `FAIL` | `streaming` | 84101 | GPU1, TF32 disabled, JIT on | `nonfinite_log_likelihood`, `nonfinite_filtered_means`, `nonfinite_filtered_variances`, `nonfinite_ess_by_time` |
| `gpu-notf32-nojit-84101` | `FAIL` | `streaming` | 84101 | GPU1, TF32 disabled, JIT off | `route_exception` |

Interpretation:

- The repaired P04C2 rows are structured-valid artifacts.
- The GPU no-TF32/no-JIT control fails while the P04C1 CPU no-TF32/no-JIT
  control passed for the same seed, so P04C2 classifies this as GPU/device
  streaming invalidity rather than a pure TF32 or pure JIT issue.
- This is a streaming comparator validity blocker, not an SVD-Nystrom
  rejection or promotion/default/scientific/HMC claim.

Artifacts:

- Repaired P04C2 summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-summary-2026-06-26.json`
- Repaired P04C2 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-repaired-streaming-gpu-tf32-jit-isolation-result-2026-06-26.md`
- P04C3 draft subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c3-streaming-comparator-robustness-subplan-2026-06-26.md`

Gate status:

- `P04C2_GPU_DEVICE_STREAMING_INVALID`

Next action:

- Review P04C3 before changing the streaming route or resuming P04C. Do not
  resume P04C calibration seeds, launch P05, freeze a threshold, drop seed
  `84101`, or make promotion/default/scientific/HMC claims.

### 2026-06-26 - P04C3 Streaming Comparator Robustness Diagnostic Closed

Plan review:

- P04C3-R1: `VERDICT: REVISE`; repaired over-strong inverse-to-Cholesky
  wording, no-jitter/no-stabilization-policy boundary, and exact canary
  artifacts.
- P04C3-R2: `VERDICT: AGREE`; review converged on exact subplan only.

Implementation:

- Replaced explicit posterior precision `tf.linalg.inv` in the shared LEDH
  flow core with `tf.linalg.cholesky_solve` against identity on the same
  already-stabilized precision path.
- Kept jitter, stabilization policy, thresholds, fixture, seed, dtype,
  particle count, transport policy, and SVD-Nystrom policy unchanged.
- Fixed streaming TensorArray chunk writer index dtype exposed by focused
  tests.

Required local checks:

```text
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_svd_nystrom_range_bearing_gate.py -q
First run: 4 failed, 41 passed
Second run after index dtype fix: 45 passed, 18193 warnings in 55.74s
```

Trusted GPU canary:

| Row | Status | Route | Seed | Device / mode | Route hard vetoes |
| --- | --- | --- | ---: | --- | --- |
| `gpu-notf32-nojit-streaming-canary-seed84101` | `FAIL` | `streaming` | 84101 | GPU1, TF32 disabled, JIT off | `route_exception` |

Interpretation:

- The original `MatrixInverse` failure path was removed, but the exact GPU
  canary still failed in the comparator stabilization path, now at
  `SelfAdjointEigV2` with GPU Cholesky/eigensolver diagnostics.
- P04C3 did not make the streaming comparator valid for P04C calibration.
- This remains a comparator validity blocker, not an SVD-Nystrom rejection.

Artifacts:

- P04C3 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c3-streaming-comparator-robustness-result-2026-06-26.md`
- P04C3 canary JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101-2026-06-26.json`
- P04C3 canary Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101-2026-06-26.md`
- P04C3 canary log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101.log`

Gate status:

- `P04C3_BLOCKED_COMPARATOR_INVALID_FOR_P04C`

Next action:

- Stop P04C calibration and draft an owner-reviewed comparator strategy plan
  before any further runtime ladder. Do not resume P04C calibration seeds,
  launch P05, freeze a threshold, drop seed `84101`, or make promotion/default/
  scientific/HMC claims.
