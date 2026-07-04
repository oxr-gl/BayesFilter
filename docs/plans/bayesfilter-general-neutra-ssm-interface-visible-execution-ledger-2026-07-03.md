# BayesFilter General NeuTra SSM Interface Visible Execution Ledger

Date: 2026-07-03

Status: `IN_PROGRESS`

## Ledger

### 2026-07-03 - Phase 0 - PRECHECK

Evidence contract:

- Question: Are the generic NeuTra SSM interface program boundary, phase
  artifacts, and review loop complete enough to begin Phase 1 implementation
  safely?
- Baseline/comparator: user-requested protocode plus local visible-gated
  execution template.
- Primary criterion: required artifacts exist, subplan required-section check
  passes, Claude review returns `VERDICT: AGREE` for Phase 0 and Phase 1
  boundary or a documented blocker is written.
- Veto diagnostics: missing section, missing runbook state machine, Claude role
  drift, CPU-hidden training authorization, detached execution authorization, or
  review treated as execution authority.
- Non-claims: no interface implementation, no target correctness, no HMC
  readiness, no NeuTra training readiness, no artifact reuse success.

Actions:

- Draft master program, phase subplans, visible runbook, review ledger, and stop
  handoff.

Artifacts:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-master-program-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-gated-execution-runbook-2026-07-03.md`

Gate status:

- `LOCAL_CHECK_PASSED_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only review.

### 2026-07-03 - Phase 0 - LOCAL_CHECK

Actions:

- Ran local consistency check over master program, runbook, and eight phase
  subplans.

Artifacts:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-result-2026-07-03.md`

Gate status:

- `PLAN_CHECK_PASSED`

Next action:

- Run bounded Claude read-only review for Phase 0 and Phase 1 handoff.

### 2026-07-03 - Phase 0 - CLAUDE_REVIEW_BLOCKED

Actions:

- Requested escalated/trusted Claude read-only review of the exact Phase 0
  subplan path.
- Approval reviewer rejected the action before Claude execution because sending
  local plan-file contents to an external model service requires explicit user
  approval after risk disclosure.

Artifacts:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-result-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-claude-review-ledger-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md`

Gate status:

- `BLOCKED_PENDING_EXPLICIT_CLAUDE_DISCLOSURE_APPROVAL`

Next action:

- Ask the user for explicit approval to send bounded local plan-file contents
  and exact path references to Claude Code for read-only review, or ask whether
  to revise the gate to Codex-only local review.

### 2026-07-03 - Phase 0 - USER_APPROVAL_RECEIVED

Actions:

- User explicitly approved sending bounded local plan-file contents and exact
  path references to Claude Code for read-only review.

Gate status:

- `CLAUDE_REVIEW_APPROVED_PENDING_EXECUTION`

Next action:

- Rerun bounded Claude reviews under the supervised read-only reviewer protocol.

### 2026-07-03 - Phase 0 - REPAIR_ROUND_1

Actions:

- Claude Round 1 returned `VERDICT: REVISE`.
- Patched Phase 0 subplan to define authoritative headings, explicit repair
  loop, strict Claude handoff gates, all phase subplan artifacts, and minimum
  stop-handoff contents.
- Ran focused local repair check.

Artifacts:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-claude-review-ledger-2026-07-03.md`

Gate status:

- `PLAN_CHECK_PASSED_PENDING_CLAUDE_ROUND_2`

Next action:

- Rerun bounded Claude review of the Phase 0 subplan.

### 2026-07-03 - Phase 0 - CLAUDE_ROUND_2_AGREE

Actions:

- Claude Round 2 returned `VERDICT: AGREE` for the Phase 0 subplan.
- Patched the one minor formatting note: added missing bullet marker for the
  Phase 1 subplan path.

Gate status:

- `PHASE0_SUBPLAN_REVIEW_CONVERGED`

Next action:

- Run focused local check, then review Phase 1 subplan before crossing.

### 2026-07-03 - Phase 0 - PHASE1_SUBPLAN_REPAIR_ROUND_1

Actions:

- Claude Phase 1 subplan Round 1 returned `VERDICT: REVISE`.
- Patched Phase 1 subplan to align objective, checks, evidence contract, Phase 0
  inheritance, Phase 2 handoff, and closeout artifact requirements.
- Ran focused local Phase 1 repair check.

Gate status:

- `PHASE1_REPAIR_CHECK_PASSED_PENDING_CLAUDE_ROUND_2`

Next action:

- Rerun bounded Claude review of Phase 1 subplan.

### 2026-07-03 - Phase 0 - PHASE1_REVIEW_TIMEOUT_PROBE

Actions:

- Phase 1 subplan Round 2 review timed out with no output.
- Ran small Claude health probe.

Artifacts:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-claude-review-ledger-2026-07-03.md`

Gate status:

- `CLAUDE_HEALTHY_PROMPT_TOO_BROAD`

Next action:

- Retry Phase 1 review with a narrower blocker-repair question.

### 2026-07-03 - Phase 0 - PHASE0_GATE_PASSED

Actions:

- Narrowed Phase 1 review returned `VERDICT: AGREE`.
- Updated Phase 0 result to `PHASE0_GATE_PASSED`.

Artifacts:

- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-result-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-subplan-2026-07-03.md`

Gate status:

- `PHASE0_GATE_PASSED`

Next action:

- Begin Phase 1 implementation under the reviewed subplan.

### 2026-07-03 - Phase 1 - CONTRACT_SCAFFOLD

Evidence contract:

- Question: Can BayesFilter represent a generic Bayesian SSM target boundary
  with stable manifests and fail-closed metadata checks?
- Baseline/comparator: existing nonlinear SSM adapter contract and stable
  signature discipline.
- Primary criterion: focused tests pass for all five Phase 1 objective surfaces.
- Veto diagnostics: unstable signature, missing dimension, duplicate parameter,
  process-local identity, missing prior/filter/transport binding, unknown target
  policy, or import/export failure.
- Non-claims: no likelihood correctness, filter implementation, XLA readiness,
  HMC readiness, NeuTra training, or artifact compatibility.

Actions:

- Added `bayesfilter/ssm/contracts.py`.
- Added `bayesfilter/ssm/__init__.py`.
- Added `tests/test_general_ssm_contracts.py`.
- Ran required local checks with `CUDA_VISIBLE_DEVICES=-1` because Phase 1 uses
  contract/import checks only and must not touch GPU/CUDA.
- Wrote Phase 1 result.
- Refreshed Phase 2 subplan with actual Phase 1 exported names and skeptical
  audit.

Artifacts:

- `bayesfilter/ssm/contracts.py`
- `bayesfilter/ssm/__init__.py`
- `tests/test_general_ssm_contracts.py`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-result-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-subplan-2026-07-03.md`

Checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py -q -p no:cacheprovider`: 14 passed.
- `CUDA_VISIBLE_DEVICES=-1 python - <<'PY' ... import bayesfilter; import bayesfilter.inference; import bayesfilter.ssm ... PY`: printed `IMPORT_SMOKE_OK`.

Gate status:

- `PHASE1_GATE_PASSED_PENDING_PHASE2_REVIEW`

Next action:

- Run bounded Claude read-only review of the refreshed Phase 2 subplan.

### 2026-07-03 - Phase 1 - PHASE2_SUBPLAN_REPAIR_ROUND_1

Actions:

- Claude Phase 2 subplan Round 1 returned `VERDICT: REVISE`.
- Patched Phase 2 subplan to anchor Phase 1 exports to the Phase 1 result,
  replace ambiguous CPU-hidden wording with CPU-only/GPU-hidden
  `CUDA_VISIBLE_DEVICES=-1` wording, define `[D]` rejection versus `[1, D]`
  allowance, and clarify non-batch static SSM dimensions plus batch-rank policy.

Gate status:

- `PHASE2_SUBPLAN_REPAIR_PENDING_LOCAL_CHECK_AND_CLAUDE_ROUND_2`

Next action:

- Run focused local check, then rerun bounded Claude review on the repaired
  Phase 2 subplan.

### 2026-07-03 - Phase 1 - PHASE2_SUBPLAN_REPAIR_ROUND_2

Actions:

- Claude Phase 2 subplan Round 2 returned `VERDICT: REVISE`.
- Three Round 1 blockers were fixed; the remaining gap was that static-shape
  metadata appeared in the handoff gate but not in the Phase 2 checks/pass
  criterion.
- Patched Phase 2 subplan to require a metadata/signature check for non-batch
  `SSMStaticShape` dimensions plus explicit batch-rank policy.

Gate status:

- `PHASE2_SUBPLAN_REPAIR_PENDING_LOCAL_CHECK_AND_CLAUDE_ROUND_3`

Next action:

- Run focused local check, then rerun bounded Claude review on the remaining
  static-shape blocker only.

### 2026-07-03 - Phase 1 - PHASE1_GATE_PASSED

Actions:

- Focused local Phase 2 static-shape repair check passed.
- Claude Phase 2 subplan Round 3 returned `VERDICT: AGREE`.
- Updated Phase 1 result to `PHASE1_GATE_PASSED`.
- Updated Phase 2 subplan to `REVIEWED_READY_FOR_PHASE2_EXECUTION`.

Gate status:

- `PHASE1_GATE_PASSED`

Next action:

- Begin Phase 2 implementation under the reviewed Phase 2 subplan.

### 2026-07-03 - Phase 2 - TARGET_BUILDER

Evidence contract:

- Question: Can generic SSM contracts produce a deterministic batch-native
  posterior value/score adapter for a toy nonlinear SSM and deterministic
  filter?
- Baseline/comparator: direct prior plus deterministic toy filter likelihood.
- Primary criterion: finite `[B]` values and `[B, D]` scores, reject `[D]`,
  allow `[1, D]`, preserve Phase 1 target signature, carry non-batch static SSM
  dimensions plus batch-rank policy, and produce stable adapter signatures.
- Veto diagnostics: hidden row loop, stochastic fresh randomness, missing
  manifests, fallback authority promoted to XLA, top-level API expansion, or
  nonfinite toy target.
- Non-claims: no real-model correctness, HMC readiness, NeuTra readiness, or
  all-filter support.

Actions:

- Added `bayesfilter/ssm/target_builder.py`.
- Refreshed lazy `bayesfilter.ssm` exports.
- Added `tests/test_general_ssm_target_builder.py`.
- Fixed a sign error in the toy filter fixture score after the finite-difference
  test failed.
- Wrote Phase 2 result.
- Refreshed Phase 3 subplan with actual Phase 2 exported names and skeptical
  audit.

Artifacts:

- `bayesfilter/ssm/target_builder.py`
- `tests/test_general_ssm_target_builder.py`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-result-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-subplan-2026-07-03.md`

Checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py -q -p no:cacheprovider`: 24 passed.
- `CUDA_VISIBLE_DEVICES=-1 python - <<'PY' ... import bayesfilter.ssm ... PY`: printed `SSM_IMPORT_SMOKE_OK`.
- Static AST scan of `bayesfilter/ssm/target_builder.py`: no loops or
  `tf.map_fn`/`tf.vectorized_map`.

Gate status:

- `PHASE2_GATE_PASSED_PENDING_PHASE3_REVIEW`

Next action:

- Run bounded Claude read-only review of the refreshed Phase 3 subplan.

### 2026-07-03 - Phase 2 - PHASE3_SUBPLAN_REPAIR_ROUND_1

Actions:

- Claude Phase 3 subplan Round 1 returned `VERDICT: REVISE`.
- Patched Phase 3 subplan to anchor Phase 2 inheritance to live source/export
  files, remove an under-specified regularization-policy veto, and clarify that
  registry output remains `FilterProgram`-compatible while downstream
  `SSMTargetContract` validation is tested through
  `validate_ssm_target_contract`.

Gate status:

- `PHASE3_SUBPLAN_REPAIR_PENDING_LOCAL_CHECK_AND_CLAUDE_ROUND_2`

Next action:

- Run focused local check, then rerun bounded Claude review on the repaired
  Phase 3 subplan.

### 2026-07-03 - Phase 2 - PHASE2_GATE_PASSED

Actions:

- Focused Phase 3 repair local check passed.
- Claude Phase 3 subplan Round 2 returned `VERDICT: AGREE`.
- Updated Phase 2 result to `PHASE2_GATE_PASSED`.
- Updated Phase 3 subplan to `REVIEWED_READY_FOR_PHASE3_EXECUTION`.

Gate status:

- `PHASE2_GATE_PASSED`

Next action:

- Begin Phase 3 implementation under the reviewed Phase 3 subplan.

### 2026-07-03 - Phase 3 - FILTER_REGISTRY

Evidence contract:

- Question: Can BayesFilter decide whether a model/filter pair is admissible for
  a deterministic HMC target before building the target?
- Baseline/comparator: Phase 2 direct fixture binding with no registry.
- Primary criterion: stable `FilterProgram` manifests, capability compatibility
  checks, and fail-closed missing-capability/stochastic-filter behavior.
- Veto diagnostics: accepting stochastic fresh randomness, missing
  deterministic target policy, capability mismatch, target-evaluation logic in
  registry, or top-level API expansion.
- Non-claims: no filter correctness, all-filter support, production
  particle-filter HMC readiness, or sampler validity.

Actions:

- Added `bayesfilter/ssm/filter_registry.py`.
- Refreshed lazy `bayesfilter.ssm` exports.
- Added `tests/test_general_ssm_filter_registry.py`.
- Wrote Phase 3 result.
- Refreshed Phase 4 subplan with actual Phase 3 exported names and skeptical
  audit.

Artifacts:

- `bayesfilter/ssm/filter_registry.py`
- `tests/test_general_ssm_filter_registry.py`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-result-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-subplan-2026-07-03.md`

Checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py tests/test_general_ssm_filter_registry.py -q -p no:cacheprovider`: 32 passed.
- `CUDA_VISIBLE_DEVICES=-1 python - <<'PY' ... import bayesfilter.ssm ... PY`: printed `SSM_IMPORT_SMOKE_OK` and `True`.
- Static AST scan of `bayesfilter/ssm/filter_registry.py`: no target-evaluation
  attributes.

Gate status:

- `PHASE3_GATE_PASSED_PENDING_PHASE4_REVIEW`

Next action:

- Run bounded Claude read-only review of the refreshed Phase 4 subplan.

### 2026-07-03 - Phase 3 - PHASE3_GATE_PASSED

Actions:

- Focused Phase 4 subplan local check passed.
- Claude Phase 4 subplan Round 1 returned `VERDICT: AGREE`.
- Updated Phase 3 result to `PHASE3_GATE_PASSED`.
- Updated Phase 4 subplan to `REVIEWED_READY_FOR_PHASE4_EXECUTION`.

Gate status:

- `PHASE3_GATE_PASSED`

Next action:

- Begin Phase 4 implementation under the reviewed Phase 4 subplan.

### 2026-07-03 - Phase 4 - NEUTRA_ARTIFACT_LOADER

Evidence contract:

- Question: Can BayesFilter represent frozen NeuTra transports as reusable
  target transforms without retraining or weakening target authority?
- Baseline/comparator: existing `FixedTransportValueScoreAdapter` chain-rule
  behavior and synthetic frozen affine transport fixture.
- Primary criterion: synthetic artifact loads to a stable manifest, mismatches
  fail closed, and fixed-transport wrapper preserves base authority.
- Veto diagnostics: ignored target mismatch, process-local signature,
  missing log-Jacobian, model-specific imports, fallback authority promotion, or
  training-success claims from loader checks.
- Non-claims: no real artifact availability, HMC tuning, posterior convergence,
  NeuTra training readiness, or sampler validity.

Actions:

- Added `bayesfilter/inference/neutra_artifacts.py`.
- Refreshed `bayesfilter.inference` exports.
- Added `tests/test_neutra_artifact_loader.py`.
- Wrote Phase 4 result.
- Refreshed Phase 5 subplan with actual Phase 4 exported names and skeptical
  audit.

Artifacts:

- `bayesfilter/inference/neutra_artifacts.py`
- `tests/test_neutra_artifact_loader.py`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-result-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-subplan-2026-07-03.md`

Checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_neutra_artifact_loader.py tests/test_batched_value_score.py -q -p no:cacheprovider`: 25 passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py tests/test_general_ssm_filter_registry.py tests/test_neutra_artifact_loader.py -q -p no:cacheprovider`: 38 passed.
- Inference export smoke printed `NEUTRA_EXPORT_SMOKE_OK`.
- Static import scan confirmed no external model package imports.

Gate status:

- `PHASE4_GATE_PASSED_PENDING_PHASE5_REVIEW`

Next action:

- Run bounded Claude read-only review of the refreshed Phase 5 subplan.

### 2026-07-03 - Phase 4 - PHASE5_SUBPLAN_REPAIR_ROUND_1

Actions:

- Claude Phase 5 subplan Round 1 returned `VERDICT: REVISE`.
- Patched manifest wording to require HMC policy label and hash consistently.
- Narrowed objective wording from broad tuning policy to existing HMC
  policy/config binding with no new tuning-policy/default change.

Gate status:

- `PHASE5_SUBPLAN_REPAIR_PENDING_LOCAL_CHECK_AND_CLAUDE_ROUND_2`

Next action:

- Run focused local check, then rerun bounded Claude review on repaired Phase 5
  policy/manifest wording.

### 2026-07-03 - Phase 4 - PHASE4_GATE_PASSED

Actions:

- Focused Phase 5 repair local check passed.
- Claude Phase 5 subplan Round 2 returned `VERDICT: AGREE`.
- Updated Phase 4 result to `PHASE4_GATE_PASSED`.
- Updated Phase 5 subplan to `REVIEWED_READY_FOR_PHASE5_EXECUTION`.

Gate status:

- `PHASE4_GATE_PASSED`

Next action:

- Begin Phase 5 implementation under the reviewed Phase 5 subplan.

### 2026-07-03 - Phase 5 - FIXED_TRANSPORT_HMC_BINDING

Evidence contract:

- Question: Can a generic frozen-transport target be passed to BayesFilter HMC
  mechanics with complete target/transport/HMC manifests and fail-closed
  authority checks?
- Baseline/comparator: existing fixed-transport value/score adapter and HMC
  policy metadata.
- Primary criterion: tiny CPU-only mechanics binding passes, manifest fields are
  complete, and fallback value/score authority cannot enter XLA HMC.
- Veto diagnostics: missing target/transport/policy manifest fields, scalar
  fallback, fallback authority promotion, unlabeled CPU-only run, or sampling
  drift.
- Non-claims: no serious HMC convergence, default sampler readiness,
  real-artifact reuse success, performance claim, or posterior validity.

Actions:

- Added `bayesfilter/inference/fixed_transport_hmc.py`.
- Refreshed `bayesfilter.inference` exports.
- Added `tests/test_fixed_transport_hmc_binding.py`.
- Wrote Phase 5 result.
- Refreshed Phase 6 subplan with actual Phase 5 exported names and skeptical
  audit.

Artifacts:

- `bayesfilter/inference/fixed_transport_hmc.py`
- `tests/test_fixed_transport_hmc_binding.py`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-result-2026-07-03.md`
- `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-reuse-subplan-2026-07-03.md`

Checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_fixed_transport_hmc_binding.py tests/test_batched_value_score.py -q -p no:cacheprovider`: 25 passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py tests/test_general_ssm_filter_registry.py tests/test_neutra_artifact_loader.py tests/test_fixed_transport_hmc_binding.py -q -p no:cacheprovider`: 44 passed.
- Export smoke printed `FIXED_TRANSPORT_HMC_EXPORT_SMOKE_OK`.
- Static AST scan of `bayesfilter/inference/fixed_transport_hmc.py`: no
  `sample_chain` calls.

Gate status:

- `PHASE5_GATE_PASSED_PENDING_PHASE6_REVIEW`

Next action:

- Run bounded Claude read-only review of the refreshed Phase 6 subplan.

### 2026-07-03 - Phase 5 - PHASE5_GATE_PASSED

Actions:

- Focused Phase 6 subplan local check passed.
- Claude Phase 6 subplan Round 1 returned `VERDICT: AGREE`.
- Updated Phase 5 result to `PHASE5_GATE_PASSED`.
- Updated Phase 6 subplan to `REVIEWED_READY_FOR_PHASE6_EXECUTION`.

Gate status:

- `PHASE5_GATE_PASSED`

Next action:

- Begin Phase 6 artifact reuse classification under the reviewed subplan.
