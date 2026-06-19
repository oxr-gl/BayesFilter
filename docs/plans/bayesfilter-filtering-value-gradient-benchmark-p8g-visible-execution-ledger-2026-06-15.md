# P8g Visible Execution Ledger

Date: 2026-06-15

Status: `PLANNING_GATE_REVIEWED_READY_FOR_G0_LAUNCH_APPROVAL`

## Ledger

### 2026-06-15 - Planning Gate - PRECHECK

Evidence contract:

- Question: Can P8g be launched as a visible gated GPU-first LEDH/DPF
  value-and-gradient program?
- Baseline/comparator: reviewed P8g program and visible gated execution
  runbook template.
- Primary criterion: master program, phase subplans, visible runbook, and
  review loop are created before execution.
- Veto diagnostics: detached launch, GPU execution without approval, Claude
  used as execution authority, or missing subplan fields.
- Non-claims: no GPU result, implementation result, gradient correctness, or
  HMC readiness yet.

Actions:

- Created P8g visible gated master program and phase subplans.
- Created visible execution runbook and stop handoff.
- Ran the required skeptical pre-launch audit before any GPU, long, tuning,
  implementation, or HMC execution.

Skeptical pre-launch audit:

- Wrong-baseline risk: controlled by keeping P8e/P8d current runner, reviewed
  P8g plan, and superseded P8f tuning scope separate.
- Proxy-metric risk: controlled by declaring prefix profiles, smoke tests,
  gradient checks, and HMC tiers as phase gates only, not scientific closure.
- Missing-stop risk: controlled by per-phase stop conditions and the visible
  stop handoff.
- Unfair-comparison risk: controlled by CPU/GPU parity and same-row/same-seed
  command contracts before speed or tuning interpretation.
- Hidden-assumption risk: controlled by explicit G0 GPU trust manifest,
  fixed-randomness/no-resampling scope, and command entry-point existence gates.
- Stale-context risk: controlled by refusing to reuse stale P8d outputs without
  G7 refresh provenance.
- Environment-mismatch risk: controlled by deliberate CPU hiding for CPU checks
  and trusted escalation for GPU/CUDA commands.
- Artifact-answer risk: controlled by phase-local output paths and required
  result artifacts before handoff.

Audit disposition:

- `PASS_PRELAUNCH_PLANNING_AUDIT`; execution may proceed only after the current
  planning review converges and the user approves the exact launch commands.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-gated-master-program-2026-06-15.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-gated-execution-runbook-2026-06-15.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-stop-handoff-2026-06-15.md`

Gate status:

- `IN_PROGRESS_PENDING_LOCAL_CHECKS_AND_REVIEW`

Next action:

- Run local checks and Claude read-only review.

## Review Loop Ledger

Canonical fields for every review round:

- phase;
- artifact;
- blocker key;
- round;
- verdict;
- disposition;
- next action;
- review prompt scope.

| Date | Phase | Artifact | Blocker key | Round | Verdict | Disposition | Next action | Review prompt scope |
|---|---|---|---|---:|---|---|---|---|
| 2026-06-15 | Planning gate | P8g visible master/runbook/subplans | `P8G_VISIBLE_REVIEW_R1_COMMAND_LEDGER_PATHS` | 1 | `REVISE` | Prior review found missing exact command/environment blocks, missing canonical review-ledger storage, and G0 result path mismatch; current artifacts patch those defects by adding command contracts, this canonical ledger section, and a normalized G0 path. | Rerun local checks and Claude review. | Local paths only: visible master, runbook, ledger, source P8g plan, and phase subplans. |
| 2026-06-15 | Planning gate | P8g visible master/runbook/subplans | `P8G_VISIBLE_REVIEW_R2_LEDGER_TERMINOLOGY_G0_REVIEW` | 2 | `REVISE` | Claude accepted the main boundary fixes but found ledger wording stale/self-contradictory, master artifact wording implying a separate Claude ledger, and G0 review wording too optional. | Patch terminology, make G0 review required before G1, rerun local checks, rerun Claude review. | Local paths only: visible master, runbook, ledger, source P8g plan, and phase subplans. |
| 2026-06-15 | Planning gate | P8g visible master/runbook/subplans | `P8G_VISIBLE_REVIEW_R3_G0_GATE_RUNBOOK_RECORD` | 3 | `REVISE` | Claude found that G0 review was mandatory in checks but not in actual G0 handoff/G1 entry gates, and the runbook artifact row still implied a separate Claude review record. | Patch G0 handoff, G1 entry, and runbook artifact wording; rerun local checks and Claude review. | Local paths only: visible master, runbook, ledger, G0, and G1 plus phase subplans as needed. |
| 2026-06-15 | Planning gate | P8g visible master/runbook/subplans | `P8G_VISIBLE_REVIEW_R4_CONVERGED` | 4 | `AGREE` | Claude found the canonical review record, G0 handoff, G1 entry gate, approval boundaries, and Claude read-only role converged with no material launch-readiness ambiguity. | Planning gate may stop at G0 launch approval boundary. | Local paths only: visible master, runbook, ledger, G0, and G1. |
| 2026-06-15 | G0 | G0 GPU probe result | `P8G_G0_GPU_PROBE_RESULT_REVIEW` | 1 | `AGREE` | Claude found the trusted GPU probe result satisfies the G0 evidence contract, avoids overclaims, and is safe to mark `PASS_P8G_G0_GPU_TRUSTED_PROBE_REVIEWED` once recorded. | Mark G0 reviewed and advance only to the G1 subplan gate. | Local paths only: G0 result, G0 subplan, G1 subplan, visible ledger, and runbook. |
| 2026-06-15 | G1 | G1 profile result | `P8G_G1_PROFILE_FEASIBILITY_PROJECTION` | 1 | `REVISE` | Claude found G1 identified a vectorization target and avoided overclaims, but lacked the required full-horizon feasibility projection and recorded budget. | Patch G1 result with projection/budget, rerun focused checks, rerun Claude review. | Local paths only: G1 result/subplan, G2 subplan, profile JSONs, ledger, runner, and tests. |
| 2026-06-15 | G1 | G1 profile result | `P8G_G1_PROFILE_FEASIBILITY_REVIEWED` | 2 | `AGREE` | Claude found the repaired G1 result closes the projection/budget blocker, avoids promoting the slow current GPU route, and constrains G2 to the recorded budget or blocker. | Mark G1 reviewed and advance only to the G2 subplan gate. | Local paths only: G1 result/subplan, G2 subplan, GPU profile JSON, and ledger. |
| 2026-06-15 | G2 | G2 vectorized Algorithm 1 blocker result | `P8G_G2_VECTORIZE_ALG1_SPEED_BLOCKER_REVIEW` | 1 | `AGREE` | Claude found G2 correctly blocks rather than handing off: parity/finiteness/GPU placement pass, but the 5x/30-minute speed/feasibility gate fails; repair recommendation is coherent. | Mark G2 blocker reviewed, write visible stop handoff, and draft focused G2 repair subplan. | Local paths only: G2 result/subplan, G1 result, smoke JSONs, ledger, filter code, runner, and tests. |
| 2026-06-15 | G2b | G2b scalar-SV graph repair subplan | `P8G_G2B_SUBPLAN_TIME_LOOP_ROUTE_LABEL_REPAIR` | 1 | `REVISE` | Claude found the draft subplan was directionally correct but did not explicitly veto a surviving Python/eager time loop and did not require a distinct scalar-SV graph route label separate from `p8g_vectorized_particles`. | Patch the same subplan visibly and rerun focused review. | Local paths only: G2b subplan, G1/G2 results, stop handoff, ledger, runner, filter code, and tests. |
| 2026-06-15 | G2b | G2b scalar-SV graph repair subplan | `P8G_G2B_SUBPLAN_REVIEWED` | 2 | `AGREE` | Claude found the patched subplan now explicitly requires no Python/eager time loop in the serious route and a distinct scalar-SV graph flag/payload/route label, with no remaining material planning blocker. | Execute G2b under the reviewed subplan. | Local paths only: G2b subplan plus G1/G2 results and stop handoff. |
| 2026-06-15 | G2b | G2b scalar-SV graph repair result | `P8G_G2B_RESULT_REVIEWED` | 1 | `AGREE` | Claude found no material blocker: parity, distinct route identity, GPU placement, finite outputs, serious time loop in XLA/`tf.while_loop`, and feasibility-scale speed evidence satisfy the reviewed subplan without overclaiming. Minor non-blocking note: JSON `phase` field inherits `P8G_G1_CURRENT_BOTTLENECK_PROFILE`. | Mark G2b reviewed pass and refresh G3 subplan entry conditions around `p8g_sv_scalar_graph`. | Local paths only: G2b result/subplan, G1/G2 results/JSONs, ledger, stop handoff, code, and tests. |
| 2026-06-15 | G3 | G3 fixed-randomness gradient subplan | `P8G_G3_SUBPLAN_MISSING_SURFACES` | 1 | `REVISE` | Claude found the subplan was boundary-safe but implied the missing gradient CLI/test surfaces already existed and omitted the gradient semantics test from review scope. | Patch the subplan to mark CLI/tests as to-build implementation targets and include the gradient semantics test. | Local paths only: G3 subplan, G2b result, ledger, stop handoff, runner, and tests. |
| 2026-06-15 | G3 | G3 fixed-randomness gradient subplan | `P8G_G3_SUBPLAN_REVIEWED` | 2 | `AGREE` | Claude found the patched G3 subplan now clearly marks the fixed-randomness gradient command/tests as missing surfaces to implement, includes the gradient semantics test, stays actual-SV-only through `p8g_sv_scalar_graph`, and preserves no HMC/tuning/generalized-SV boundary crossing. | Execute G3 under the reviewed subplan. | Local paths only: G3 subplan, G2b result, stop handoff, gradient semantics test, and runner. |
| 2026-06-15 | G3 | G3 fixed-randomness gradient result | `P8G_G3_RESULT_REVIEWED` | 1 | `AGREE` | Claude found G3 satisfies the reviewed subplan without overclaiming: seed/coordinate contract, no-resampling boundary, fixed-randomness-only claim, XLA value/non-XLA gradient split disclosure, CPU/GPU parity, finite-difference residuals, and artifact coverage are adequate. Minor non-blocking note: JSON primary criterion wording omits CPU/GPU parity though result artifacts include it. | Mark G3 reviewed pass and refresh G4 subplan. | Local paths only: G3 result/subplan/contract, CPU/GPU JSONs, G2b result, ledger, code, and tests. |
| 2026-06-15 | G4 | G4 particle tuning subplan | `P8G_G4_SUBPLAN_MISSING_SURFACES` | 1 | `REVISE` | Claude found the initial G4 subplan treated missing particle-tuning CLI/tests as executable evidence. | Patch the subplan to mark CLI/tests as to-build targets before any tuning evidence. | Local paths only: G4 subplan, G3/G2b results, stop handoff, ledger, runner, and tests. |
| 2026-06-15 | G4 | G4 particle tuning subplan | `P8G_G4_SUBPLAN_REVIEWED_BEFORE_IMPLEMENTATION` | 2 | `AGREE` | Claude accepted the repaired pre-implementation subplan. | Implement G4 tuning surfaces and rerun local checks before trusted Stage 0. | Local paths only: G4 subplan and current runner/test surfaces. |
| 2026-06-15 | G4 | G4 particle tuning subplan after implementation | `P8G_G4_DEVICE_AND_STALE_SURFACE_WORDING` | 3 | `REVISE` | Codex found and patched a GPU command contract bug; Claude then required full command pinning to actual-SV LEDH scalar graph and stale missing-surface wording cleanup. | Patch command and wording; rerun local checks. | Local paths only: G4 subplan and runner. |
| 2026-06-15 | G4 | G4 particle tuning subplan after implementation | `P8G_G4_STALE_SURFACE_WORDING_R4` | 4 | `REVISE` | Claude found one remaining stale required-artifact phrase saying implemented CLI surfaces did not exist. | Patch the stale phrase and rerun local checks. | Local paths only: G4 subplan and runner. |
| 2026-06-15 | G4 | G4 particle tuning subplan after implementation | `P8G_G4_REVIEW_LOOP_LIMIT_AFTER_TEXT_FIX` | 5 | `REVISE` | Claude found exact remaining stale wording around "implementation targets" and "implemented and rerun"; Codex patched those exact phrases and local checks passed, but the five-round review-loop ceiling was reached before an `AGREE`. | Stop before trusted GPU Stage 0 and ask for human direction. | Local path: G4 subplan. |
| 2026-06-15 | G4 | G4 particle tuning subplan extra review | `P8G_G4_EXTRA_R1_ARTIFACT_REVIEW_WORDING` | 1 | `REVISE` | User authorized five extra review rounds. Claude found one guardrail sentence omitted artifact writing and result review from the evidence boundary. | Patch the guardrail sentence and rerun focused review. | Local paths: G4 subplan and runner. |
| 2026-06-15 | G4 | G4 particle tuning subplan extra review | `P8G_G4_EXTRA_R2_SUBPLAN_REVIEWED` | 2 | `AGREE` | Claude found the G4 subplan converged: implemented CLI/tests are not evidence until checks/GPU Stage 0/artifact/result review, and commands are pinned to GPU actual-SV LEDH scalar graph. | Launch trusted G4 Stage 0 GPU ladder. | Local path: G4 subplan. |

### 2026-06-15 - G4 - EXECUTE_STAGE0/ASSESS_PENDING_REVIEW

Evidence contract:

- Question: What particle counts are adequate for the actual-SV scalar graph
  LEDH value summary under the reviewed GPU path?
- Baseline/comparator: historical `N=8` wiring evidence and reviewed G2b/G3
  actual-SV scalar-graph route.
- Primary criterion: select the smallest passing count or emit an explicit
  blocker, with non-executed rows preserved.
- Veto diagnostics: nonfinite run, relative ESS collapse, unstable adjacent
  mean, missing next-rung check where required, runtime blowup, or missing
  selected/blocked rows.
- Non-claims: no tuned count until the gate passes, no gradient correctness, no
  HMC readiness, no stochastic PF marginal-gradient correctness, no filter
  ranking.

Actions:

- Added and tested G4 particle-tuning CLI/schema surfaces.
- Ran trusted GPU Stage 0 actual-SV LEDH scalar graph ladder for horizons
  `50,200`, particles `16,32`, and five fixed seeds.
- Repaired the selected/blocked reducer after the first Stage 0 run exposed a
  reporting bug for duplicate particle counts across horizons.
- Regenerated Stage 0 artifacts after the reducer repair.
- Wrote G4 result artifact.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-selected-blocked-2026-06-15.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-result-2026-06-15.md`

Gate status:

- `BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS_REVIEWED`

Next action:

- Review the G4b ESS-repair subplan before any further GPU tuning or HMC
  diagnostics.

| 2026-06-15 | G4 | G4 particle tuning result | `P8G_G4_RESULT_RELATIVE_ESS_BLOCKER_REVIEWED` | 1 | `AGREE` | Claude found the G4 result blocker supported and boundary-safe: trusted GPU Stage 0 is artifact-backed, no count is selected, the corrected selected/blocked table records `BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS`, and no HMC/filter-ranking/stochastic-gradient overclaim is made. | Mark G4 blocker reviewed and draft G4b ESS-repair subplan. | Local paths: G4 result/subplan/JSON/CSVs, ledger, stop handoff, runner, and tests. |
| 2026-06-15 | G4b | G4b ESS-repair subplan | `P8G_G4B_ESS_REPAIR_SUBPLAN_REVIEWED` | 1 | `AGREE` | Claude found the G4b subplan starts from the reviewed relative-ESS blocker, separates resampling-route repair from larger-N diagnostic, preserves the G3 no-resampling gradient boundary, requires checks/artifacts/reviews, and avoids HMC/filter-ranking/stochastic-gradient overclaims. | G4b may execute only through the reviewed subplan and trusted GPU/check contracts. | Local paths: G4b subplan, G4 result/JSON, ledger, stop handoff, runner, filter code, and tests. |

## Planning Gate Close Record

Decision: `PASS_P8G_VISIBLE_PLANNING_GATE_READY_FOR_G0_LAUNCH_APPROVAL`.

Primary criterion status: passed. The visible master program, phase subplans,
runbook, command/artifact contracts, canonical review ledger, skeptical audit,
and stop handoff are present before execution.

Veto diagnostic status: no planning veto remains. No GPU, tuning, long,
implementation, or HMC run has been launched. Claude was used only as a
read-only reviewer.

Main uncertainty: the G0 trusted GPU/CUDA/TensorFlow/XLA state is not yet known
because launch approval has not been requested or granted in this close record.

Next justified action: ask the user for explicit approval to launch G0 trusted
GPU probes using the exact commands in the G0 subplan.

What is not concluded: GPU usability, speedup, vectorized implementation
correctness, tuned particle counts, gradient correctness, HMC readiness,
callback closure, final filter ranking, or stochastic PF marginal HMC validity.

## G0 Ledger

### 2026-06-15 - G0 - PRECHECK/EXECUTE_MINIMAL

Evidence contract:

- Question: Is the trusted GPU backend usable for P8g serious execution?
- Baseline/comparator: local CPU-only P8e diagnostics plus local GPU policy.
- Primary criterion: trusted GPU probe sees at least one usable GPU and
  TensorFlow can run a tiny GPU matmul and XLA probe.
- Veto diagnostics: non-escalated GPU failure used as evidence; no trusted GPU
  visible; TensorFlow GPU probe fails; XLA probe fails without reviewed
  exception; missing manifest.
- Non-claims: no speedup, algorithm correctness, gradient correctness, HMC
  readiness, or filter ranking.

Actions:

- Ran `git rev-parse HEAD`, `git status --short`, and `git diff --check`.
- Ran trusted/escalated `nvidia-smi`.
- Ran trusted/escalated TensorFlow/TFP GPU, matmul, and XLA probe.
- Wrote G0 result artifact.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md`

Gate status:

- `PASS_P8G_G0_GPU_TRUSTED_PROBE_REVIEWED`

Next action:

- G1 may proceed only through its subplan and command/artifact contract.

### 2026-06-15 - G1 - PRECHECK/EXECUTE_MINIMAL

Evidence contract:

- Question: Is there a concrete batched TensorFlow rewrite target that can
  plausibly make P8g GPU execution useful?
- Baseline/comparator: current CPU reference and trusted GPU profile of the
  existing implementation.
- Primary criterion: identify vectorizable hotspots and project feasibility for
  at least five-seed full-horizon `N=32` LEDH SV-style gate within a recorded
  budget.
- Veto diagnostics: silent CPU fallback; profile missing G0 citation; commands
  not answering the bottleneck question; unvectorizable Python loops.
- Non-claims: no post-rewrite speedup, no tuning adequacy, no gradient
  correctness, no HMC readiness, no filter ranking.

Actions:

- Added focused P8g prefix-profile entry point and tests in the P8d runner lane.
- Ran compile, `git diff --check`, and focused CPU-hidden pytest.
- Ran CPU-hidden and trusted GPU prefix profiles for the LEDH SV row with
  horizon `50`, particles `32`, and five fixed seeds.
- Wrote G1 result artifact.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-cpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-gpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md`

Gate status:

- `PASS_PROFILE_VECTOR_TARGET_IDENTIFIED_REVIEWED`

Next action:

- G2 may proceed only through its subplan and command/artifact contract.

### 2026-06-15 - G2 - EXECUTE_MINIMAL/ASSESS_GATE

Evidence contract:

- Question: Does P8g have a real batched GPU Algorithm 1 route rather than a CPU
  loop wrapped in TensorFlow?
- Baseline/comparator: current looped CPU/GPU Algorithm 1 implementation and
  G1 recorded `30` minute/5x feasibility gate.
- Primary criterion: short-horizon CPU/GPU parity plus batched GPU kernels with
  at least `5x` speedup or a reviewed feasible exception.
- Veto diagnostics: Python particle loop remains in serious path; GPU fallback;
  parity failure; nonfinite particles/determinants/weights/covariances;
  speed/feasibility gate failure.
- Non-claims: no serious GPU implementation, no tuned particle count, no
  gradient correctness, no HMC readiness, no filter ranking.

Actions:

- Added opt-in `tf.vectorized_map` particle route for Algorithm 1 time-step.
- Added P8g profile flag `--p8g-vectorized-particles`.
- Added focused parity/profile tests.
- Ran CPU-hidden focused tests.
- Ran trusted GPU looped and vectorized tiny profile smokes.
- Wrote G2 blocker result.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-smoke-cpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-smoke-gpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-looped-alg1-smoke-gpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md`

Gate status:

- `BLOCK_P8G_VECTORIZE_ALG1_SPEED_FEASIBILITY_REVIEWED`

Next action:

- Stop before G3. Draft a focused G2 repair subplan for graph/XLA time-loop
  vectorization and kernel coalescing, or ask for human direction if the
  feasibility gate should change.

### 2026-06-15 - G2b - REPAIR_EXECUTE/ASSESS_PENDING_REVIEW

Evidence contract:

- Question: Can the reviewed G2 speed blocker be repaired for the actual SV
  LEDH row by moving the scalar Algorithm 1 time loop and particle computation
  into TensorFlow graph operations?
- Baseline/comparator: G1/G2 generic Algorithm 1 route on
  `zhao_cui_sv_actual_nongaussian_T1000`, same horizon, particles, and seeds.
- Primary criterion: graph route preserves value parity, records a distinct
  scalar-SV graph route variant, and meets the `5x`/`30` minute feasibility
  gate or records a reviewed blocker.
- Veto diagnostics: nonfinite values, silent CPU fallback, value parity failure,
  Python/eager time loop in serious graph route, missing route label, or speed
  below the feasibility gate.
- Non-claims: no tuned particle count, no gradient correctness, no HMC
  readiness, no generic high-dimensional GPU implementation, no filter ranking.

Actions:

- Added opt-in scalar-SV graph route `run_ledh_pfpf_alg1_scalar_sv_graph_tf`.
- Added `--p8g-sv-scalar-graph` profile flag and distinct
  `p8g_sv_scalar_graph` route variant.
- Added focused parity/payload tests.
- Preserved the reviewed reference random stream by precomputing stateless
  normal draws outside XLA and feeding them to the deterministic graph kernel.
- Ran CPU-hidden checks, trusted GPU tiny smoke, and trusted GPU T50/5seed
  feasibility diagnostic.
- Wrote G2b result artifact.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-smoke-cpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-smoke-gpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-prefix50-5seed-gpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md`

Gate status:

- `PASS_P8G_G2B_SV_SCALAR_GRAPH_FEASIBILITY_REVIEWED`

Next action:

- G3 may proceed only through the refreshed G3 subplan, initially scoped to the
  actual scalar SV row and route variant `p8g_sv_scalar_graph`.

### 2026-06-15 - G3 - EXECUTE_MINIMAL/ASSESS_PENDING_REVIEW

Evidence contract:

- Question: Does the fixed-randomness/no-resampling LEDH surrogate objective
  provide stable, finite, coordinate-consistent gradients?
- Baseline/comparator: reviewed G2b scalar-SV graph route and finite-difference
  checks on the same fixed random draws.
- Primary criterion: finite stable gradients pass repeatability, CPU/GPU parity,
  and directional finite-difference checks in `canonical_unconstrained`
  coordinate.
- Veto diagnostics: gradient through resampling branch; missing seed/salt
  contract; parameterization mismatch; finite value treated as gradient
  correctness; non-finite or unstable gradients.
- Non-claims: no stochastic PF target gradient correctness, no HMC readiness,
  no tuned particle count, no generic high-dimensional Algorithm 1 gradient
  readiness, no filter ranking.

Actions:

- Added a value-only scalar-SV graph objective for fixed-randomness gradients.
- Kept XLA for G2b value profiling and used a non-XLA TensorFlow graph variant
  for reverse-mode gradients after XLA `tf.while_loop` reverse-mode raised
  TensorList boundary errors.
- Added `--p8g-fixed-randomness-gradient-check`, `--route-variant`,
  `--coordinate`, and `--output-csv` runner support.
- Added focused tests for G3 payload/guardrails.
- Wrote seed/coordinate contract artifact and CPU/GPU gradient diagnostics.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-contract-2026-06-15.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-cpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-cpu-2026-06-15.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-gpu-2026-06-15.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-gpu-2026-06-15.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md`

Gate status:

- `PASS_P8G_G3_FIXED_RANDOMNESS_GRADIENT_REVIEWED`

Next action:

- Refresh G4 particle-count tuning subplan around the reviewed actual-SV scalar
  graph route and G3 nonclaims before any tuning execution.
