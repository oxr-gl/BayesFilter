# BayesFilter General NeuTra SSM Interface Claude Review Ledger

Date: 2026-07-03

Status: `PHASE6_RESULT_AND_PHASE7_HANDOFF_REVIEW_CONVERGED`

## Role Contract

Codex is supervisor and executor. Claude is read-only reviewer only.

Claude prompts must reference exact paths or exact line ranges and must not
paste whole files. Claude may not edit, run commands, launch agents, or
authorize phase crossing.

## Review Rounds

### Round 1 Attempt - Phase 0 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-subplan-2026-07-03.md`

Prompt shape:

`READ-ONLY BOUNDED REVIEW`, exact path only, no edits, no commands, no repo-wide
review, end with `VERDICT: AGREE` or `VERDICT: REVISE`.

Execution status:

`REJECTED_BEFORE_CLAUDE_EXECUTION`

Approval-reviewer reason:

External-model disclosure risk for local plan-file contents. The reviewer
requires explicit user approval after risk disclosure before this Claude review
can proceed.

Verdict:

No Claude verdict. Phase 0 remains blocked on human approval or gate revision.

### User Approval

The user explicitly approved sending bounded local plan-file contents and exact
path references from this workspace to Claude Code for read-only review.

Approval message:

`I approve`

### Round 1 - Phase 0 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-subplan-2026-07-03.md`

Verdict:

`VERDICT: REVISE`

Findings:

- Required-subplan-field check was under-specified because the Phase 0 subplan
  did not list the authoritative required headings.
- Repair loop was implicit rather than explicit.
- Phase 1 handoff gate was weakened by an undefined non-material local-review
  exception.
- Required Artifacts named only Phase 1 subplan while checks required all phase
  subplans.
- Stop-handoff artifact was named but not operationalized.

Repair:

- Patched Phase 0 subplan to list all phase subplans, define required headings,
  add explicit repair loop trigger/owner/artifact/re-review/escalation/blocker
  path, remove the review exception, require Claude `AGREE` for Phase 0 and
  Phase 1 subplans, and define minimum stop-handoff contents.

Focused local check:

`PLAN_CHECK_PASSED`, `phase0_repair_tokens=5`.

### Round 2 - Phase 0 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-subplan-2026-07-03.md`

Verdict:

`VERDICT: AGREE`

Findings:

- Required phase-subplan fields are present.
- Evidence contract is explicit and phase-appropriate.
- Repair loop is explicit.
- Stop conditions and next-phase handoff are operationalized.
- Stop handoff is operationalized.
- Boundary safety is adequate for launching Phase 0.
- Minor formatting issue: Phase 1 subplan path was missing a bullet marker.

Repair:

- Added the missing bullet marker for the Phase 1 subplan path.

### Round 1 - Phase 1 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-subplan-2026-07-03.md`

Verdict:

`VERDICT: REVISE`

Findings:

- Objective named priors, filter programs, and frozen transports but pass
  criteria did not state exact contract elements/tests for those surfaces.
- Phase 0 inheritance was too implicit.
- Phase 2 handoff lacked exact exported symbols, internal-only symbols,
  manifest/schema guarantees, validation behaviors, and unresolved nonclaims.
- Checks lacked export allowlist and import/boundary safeguards.
- Result artifact requirements were too thin for auditable handoff.

Repair:

- Patched Phase 1 subplan with objective-surface minimums, concrete inherited
  Phase 0 decisions, export allowlist/import checks, per-surface positive and
  fail-closed tests, stricter evidence/veto fields, exact Phase 2 handoff
  inventory, and expanded closeout requirements.

Focused local check:

`PHASE1_REPAIR_CHECK_PASSED`, `repaired_tokens=7`.

### Round 2 Attempt - Phase 1 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-subplan-2026-07-03.md`

Status:

`TIMEOUT_NO_OUTPUT`

Probe:

`CLAUDE_PROBE_OK`

Interpretation:

Claude was healthy after the timeout. Treat the Round 2 prompt as too broad and
retry with a narrower question focused on whether Round 1 blockers were
repaired.

### Round 2 Narrow - Phase 1 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-subplan-2026-07-03.md`

Question:

Whether the five prior blockers were fixed.

Verdict:

`VERDICT: AGREE`

Findings:

- Objective/pass-criteria coverage for SSM target identity, parameter chart,
  prior, filter program, and frozen transport is fixed.
- Concrete Phase 0 inherited decisions are fixed.
- Exact Phase 2 handoff inventory is fixed.
- Export/import boundary checks are fixed.
- Auditable Phase 1 result requirements are fixed.

### Round 1 - Phase 2 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-subplan-2026-07-03.md`

Verdict:

`VERDICT: REVISE`

Findings:

- Phase 1 export inheritance list was not anchored to the Phase 1 result or
  export snapshot.
- Compile-check wording said "CPU-hidden" where the intended boundary is
  CPU-only / GPU-hidden with CUDA hidden before TensorFlow import.
- Rank-1 scalar-position rejection needed exact shape wording.
- Handoff phrase "static shape" was underdefined for batch-native targets.

Repair:

- Patched the Phase 2 subplan to cite the Phase 1 result export inventory,
  require `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import for CPU-only toy
  compile checks, state that `[D]` is rejected while `[1, D]` is allowed in
  batch-native mode, and define static-shape handoff as non-batch SSM dimensions
  plus batch-rank policy.

### Round 2 - Phase 2 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-subplan-2026-07-03.md`

Verdict:

`VERDICT: REVISE`

Findings:

- Phase 1 export source anchor was repaired.
- CPU-only/GPU-hidden wording was repaired.
- Scalar-position shape wording was repaired.
- Static-shape wording was improved but still appeared only in the Phase 3
  handoff gate, not in the Phase 2 checks or primary pass criterion.

Repair:

- Patched the Phase 2 subplan to require a metadata/signature check for
  non-batch `SSMStaticShape` dimensions plus explicit batch-rank policy and to
  include that requirement in the primary pass criterion and skeptical audit.

### Round 3 - Phase 2 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-subplan-2026-07-03.md`

Verdict:

`VERDICT: AGREE`

Findings:

- The remaining static-shape blocker is repaired.
- Required checks and primary pass criterion now require non-batch
  `SSMStaticShape` dimensions plus explicit batch-rank policy in the
  manifest/signature path.
- No new boundary-safety regression was identified.

### Round 1 - Phase 3 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-subplan-2026-07-03.md`

Verdict:

`VERDICT: REVISE`

Findings:

- Phase 2 inheritance was anchored only to the Phase 2 result note, not the live
  code export boundary.
- The veto for a missing regularization policy was under-specified because the
  descriptor/manifest field was not defined in Phase 3.
- The `validate_ssm_target_contract` boundary was ambiguous: the subplan did
  not say whether the registry invokes it, returns data later consumed by it, or
  only preserves compatibility with it.

Repair:

- Patched the Phase 3 subplan to anchor Phase 2 inheritance to
  `bayesfilter/ssm/__init__.py` and `bayesfilter/ssm/target_builder.py`, remove
  the regularization-policy veto from Phase 3, and specify that the registry
  returns `FilterProgram`-compatible metadata while tests verify downstream
  `SSMTargetContract` validation through `validate_ssm_target_contract`.

### Round 2 - Phase 3 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-subplan-2026-07-03.md`

Verdict:

`VERDICT: AGREE`

Findings:

- Phase 2 export inheritance is anchored to live code boundaries.
- The underdefined regularization-policy veto is scoped out of Phase 3.
- The `validate_ssm_target_contract` boundary is clear: registry output feeds
  downstream `SSMTargetContract` validation and does not replace the validator.
- No new boundary-safety issue was identified within the bounded review.

### Round 1 - Phase 4 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-subplan-2026-07-03.md`

Verdict:

`VERDICT: AGREE`

Findings:

- The subplan preserves the Phase 3 registry boundary.
- Target-signature binding and fail-closed mismatch behavior are required.
- Scope boundaries are explicit: no training, no large artifact commits, no
  model-specific imports, and no CPU-only loader checks as GPU/training
  evidence.
- Stop conditions are practical for frozen-artifact loading.
- Minor non-blocking note: reusable frozen transports require signature
  binding, while signature-missing artifacts may only be recorded as
  non-reusable.

### Round 1 - Phase 5 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-subplan-2026-07-03.md`

Verdict:

`VERDICT: REVISE`

Findings:

- Phase 4 inheritance was correct.
- Manifest requirements were inconsistent: local checks said `HMC policy`, while
  veto diagnostics said `HMC policy hash`.
- Objective wording said `tuning policy`, which was broader than the supported
  mechanics-binding evidence and could imply new policy tuning/default changes.

Repair:

- Patched the Phase 5 subplan to require both HMC policy label and hash in
  manifests and to narrow objective wording to existing HMC policy/config
  binding with no new tuning-policy/default change.

### Round 2 - Phase 5 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-subplan-2026-07-03.md`

Verdict:

`VERDICT: AGREE`

Findings:

- The HMC policy label/hash manifest wording is consistent.
- Objective wording is mechanics/binding scoped and explicitly does not tune a
  new HMC policy or change defaults.
- No new boundary-safety issue was identified within the bounded review.

### Round 1 - Phase 6 Subplan

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-reuse-subplan-2026-07-03.md`

Verdict:

`VERDICT: AGREE`

Findings:

- Phase 5 mechanics-binding boundary is inherited explicitly.
- Checks are ordered safely: existence/hash/signature first, then bounded
  load/value smoke.
- Evidence contract classifies artifacts and forbids overclaims.
- Action bans and handoff gate close retraining, serious-HMC, and
  signature-absent reuse loopholes.
- Minor non-blocking ambiguity: "eligible" is not locally defined at one step,
  but the classification/veto rules make the intended meaning clear enough.

## Prompt Template

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <path>. Do not edit,
run commands, launch agents, or review the whole repo. Question: <question>.
End with VERDICT: AGREE or VERDICT: REVISE.
```

## Probe Template

```text
Return exactly CLAUDE_PROBE_OK.
```

### Round 1 - Phase 6 Result And Phase 7 Handoff

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-reuse-result-2026-07-03.md`

Question:

Whether the Phase 6 result satisfies the artifact inventory/reuse gate,
preserves nonclaims, and supports crossing only to Phase 7 synthetic/interface
validation closeout with real-artifact reuse blocked.

Verdict:

`VERDICT: AGREE`

Findings:

- The Phase 6 result is fail-closed: checked artifacts are classified and no
  missing or signature-absent artifact is treated as reusable.
- Historical NeuTra evidence/design input is separated from generic-loader
  reuse.
- Nonclaims are preserved for training, real-artifact loader reuse, HMC
  convergence, posterior validity, method ranking, and default readiness.
- Phase 7 scope is appropriately constrained to focused interface tests,
  validation ledger, closeout, and a later migration bridge/restoration plan.

Limitation:

Claude reviewed the result note for internal sufficiency and consistency only;
it did not independently inspect the inventory JSON or external artifacts.

### Round 1 - Phase 7 Final Closeout

Target path:

`docs/plans/bayesfilter-general-neutra-ssm-interface-phase7-validation-closeout-result-2026-07-03.md`

Question:

Whether the Phase 7 closeout consistently states the implemented generic NeuTra
SSM interface evidence, preserves the Phase 6 real-artifact migration blocker,
avoids unsupported HMC/posterior/default claims, and provides a feasible next
program boundary.

Verdict:

`VERDICT: AGREE`

Findings:

- Implemented BayesFilter-owned surfaces are separated from broader claims.
- Focused validation evidence is specific to `44` CPU-only/GPU-hidden tests.
- The Phase 6 real-artifact blocker remains explicit throughout the status,
  real-artifact table, decision table, inference table, and follow-up boundary.
- Unsupported sampler superiority, posterior correctness, all-filter HMC
  readiness, default-policy, and scientific claims are avoided.
- The next program boundary is feasible: dense IAF schema/export,
  target-signature bridge, restored payload hashes, loader tests, then a
  real-artifact canary.

Non-blocking note:

Claude noted that "good historical evidence" was a little stronger than the
surrounding wording. Codex patched it to "the intended historical evidence
cells" in the closeout.
