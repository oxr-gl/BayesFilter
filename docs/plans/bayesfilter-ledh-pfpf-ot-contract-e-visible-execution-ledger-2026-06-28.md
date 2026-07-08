# Contract E Visible Execution Ledger

Date: 2026-06-28

Status: `BLOCKED_PHASE3_PRECHECK`

Master program:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-residual-affine-testing-master-program-2026-06-28.md`

Runbook:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-gated-execution-runbook-2026-06-28.md`

## Entries

### 2026-06-28 - Program Draft - INITIALIZED

Evidence contract:

- Question: Can Contract E become a viable moment-preserving differentiable
  reset candidate for LEDH-PFPF-OT?
- Baseline/comparator: old barycentric reset, no-OT weighted arm, exact Kalman
  only for LGSSM, and same-scalar FD for nonlinear gradients.
- Primary criterion: execute reviewed phase gates with artifacts and preserve
  nonclaims.
- Veto diagnostics: wrong comparator, missing uncertainty, hidden full
  transport autodiff, untrusted GPU claims, unsupported production claims.
- Non-claims: no posterior correctness, HMC readiness, production readiness, or
  literature claim for the whole hybrid.

Actions:

- Drafted master program, phase subplans, visible runbook, ledger, review
  ledger, and stop handoff scaffold.

Artifacts:

- See runbook phase index.

Gate status:

- `IN_PROGRESS_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

Next action:

- Run local artifact checks, then bounded Claude review.

### 2026-06-28 - Review Gate - BLOCKED

Evidence contract:

- Question: Can the drafted master program/runbook proceed to Phase 0 launch
  after bounded Claude review convergence?
- Baseline/comparator: local checks plus Claude read-only review.
- Primary criterion: Claude returns `VERDICT: AGREE` after any repairs.
- Veto diagnostics: Claude review unavailable or blocked by policy.
- Non-claims: no Phase 0 launch or Contract E evidence has occurred.

Actions:

- Ran local artifact checks successfully.
- Ran Claude review round 1; Claude returned `VERDICT: REVISE`.
- Patched the plan to address round-1 findings.
- Attempted Claude review round 2 with a bounded exact-path prompt.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`

Gate status:

- `BLOCKED_BY_APPROVAL_POLICY`

Next action:

- Ask the user for explicit approval to send bounded exact-path Contract E plan
  files to Claude for read-only review, or proceed with a no-Claude local-only
  review amendment if the user changes the protocol.

### 2026-06-28 - Review Gate - HUMAN_APPROVAL_RECEIVED

Evidence contract:

- Question: Can Codex resume Claude read-only review after the approval-policy
  blocker?
- Baseline/comparator: explicit user approval in chat.
- Primary criterion: approval is recorded before retrying Claude.
- Veto diagnostics: treating Claude as executor or authority.
- Non-claims: approval does not authorize boundary crossings outside read-only
  review.

Actions:

- Recorded the user's repo-wide approval for bounded Claude read-only review.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`

Gate status:

- `READY_TO_RETRY_CLAUDE_ROUND2`

Next action:

- Retry bounded Claude round 2.

### 2026-06-28 - Plan Review Gate - PASSED

Evidence contract:

- Question: Has the Contract E master/runbook/subplan packet converged under
  bounded Claude review?
- Baseline/comparator: Claude read-only review rounds plus local focused
  checks.
- Primary criterion: Claude returns `VERDICT: AGREE`.
- Veto diagnostics: material plan blocker remains.
- Non-claims: plan convergence is not Contract E implementation or numerical
  evidence.

Actions:

- Claude round 2 returned `VERDICT: REVISE`; Codex patched Phase 4 and Phase 5
  entry-condition loopholes.
- Claude round 3 returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`

Gate status:

- `PASSED`

Next action:

- Launch Phase 0 visibly.

### 2026-06-28 - Phase 0 - PRECHECK

Evidence contract:

- Question: Are we about to test the documented Contract E candidate with the
  right baselines, boundaries, and artifacts?
- Baseline/comparator: existing barycentric reset diagnostics and Contract E
  LaTeX anchors.
- Primary criterion: Phase 0 result records exact Contract E LaTeX path and
  labels, diagnostic paths, route candidates, forbidden comparators/actions,
  and reviewed Phase 1 handoff.
- Veto diagnostics: missing anchors, missing diagnostic paths, Zhao-Cui oracle,
  full transport autodiff, or CPU smoke treated as GPU evidence.
- Non-claims: no implementation correctness, value/gradient correctness, or
  production readiness.

Actions:

- Skeptical audit passed for inventory-only Phase 0: no GPU, no long run, no
  production code edit, no new numerical claim.

Artifacts:

- Phase 0 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase0-governance-inventory-subplan-2026-06-28.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run local anchor/path inventory checks and write Phase 0 result.

### 2026-06-28 - Phase 0 - ASSESS_GATE_REVIEW

Evidence contract:

- Question: Does the Phase 0 result satisfy the Phase 0 subplan and safely
  hand off to Phase 1?
- Baseline/comparator: Phase 0 subplan, Phase 0 result, Phase 1 subplan, Claude
  read-only review.
- Primary criterion: Phase 0 result and Phase 1 handoff receive Claude
  `VERDICT: AGREE` after repairs.
- Veto diagnostics: artifact mismatch, stale ledger state, missing review
  state, unsupported Phase 1 handoff.
- Non-claims: no Contract E implementation or numerical evidence has run.

Actions:

- Wrote Phase 0 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase0-governance-inventory-result-2026-06-28.md`.
- Claude Phase 0 review round 1 returned `VERDICT: REVISE`.
- Patched Phase 1 metric schema, required case matrix, Phase 2 path, Phase 0
  `sed` inspection evidence, review/ledger evidence, and CPU/GPU wording.
- Claude Phase 0 review round 2 returned `VERDICT: REVISE` for stale/incomplete
  ledger status only.
- Patched this execution ledger and the Claude review ledger to reflect the
  active Phase 0 result review gate.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase0-governance-inventory-result-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-subplan-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`

Gate status:

- `IN_REPAIR_PENDING_CLAUDE_R3`

Next action:

- Run focused checks and request Claude review round 3 of the Phase 0 result /
  Phase 1 handoff.

### 2026-06-28 - Phase 0 - REPAIR_LOOP_R3

Evidence contract:

- Question: Have the latest Phase 0 result / Phase 1 handoff review findings
  been repaired without changing the scientific scope?
- Baseline/comparator: Claude round 3 findings and local focused checks.
- Primary criterion: exact wording/ledger repairs are made and round 4 review
  agrees.
- Veto diagnostics: Phase 1 can start without follow-up review pass; stale stop
  handoff action or missing active artifacts.
- Non-claims: still no Contract E implementation or numerical evidence.

Actions:

- Patched Phase 1 entry condition to require bounded review pass, directly or
  after repair plus `VERDICT: AGREE`.
- Patched stop handoff next-safe-action and active artifact list.
- Patched Claude review ledger with round 3 finding/response.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-subplan-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-stop-handoff-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`

Gate status:

- `IN_REPAIR_PENDING_CLAUDE_R4`

Next action:

- Run focused local checks and request Claude review round 4.

### 2026-06-28 - Phase 0 - PASSED

Evidence contract:

- Question: Did Phase 0 freeze Contract E anchors and provide a safe reviewed
  handoff to Phase 1?
- Baseline/comparator: Phase 0 subplan, Phase 0 result, Phase 1 subplan,
  bounded Claude review.
- Primary criterion: Phase 0 result and Phase 1 handoff receive
  `VERDICT: AGREE`.
- Veto diagnostics: stale ledger state, missing active artifacts, or Phase 1
  start loophole.
- Non-claims: no Contract E implementation or numerical evidence.

Actions:

- Claude Phase 0 result / Phase 1 handoff review round 4 returned
  `VERDICT: AGREE`.
- Marked Phase 0 result `PHASE0_PASSED`.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase0-governance-inventory-result-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-subplan-2026-06-28.md`

Gate status:

- `PASSED`

Next action:

- Launch Phase 1 precheck.

### 2026-06-28 - Phase 1 - PRECHECK

Evidence contract:

- Question: Does the finite Contract E reset satisfy its stated moment algebra
  on controlled synthetic weighted clouds?
- Baseline/comparator: weighted source cloud moments and old barycentric
  equal-weight cloud moments.
- Primary criterion: required synthetic case matrix passes the predeclared
  moment/support/conditioning gates, with the conditioning case reported as an
  expected veto rather than a pass.
- Veto diagnostics: nonfinite values, negative \(G_+\) eigenvalue below
  tolerance, failed support rank, excessive condition number, missing seed, or
  hidden GPU claim from CPU smoke.
- Non-claims: no LEDH filtering correctness, LGSSM Kalman agreement, gradient
  correctness, or production readiness.

Actions:

- Phase 1 subplan entered after Phase 0 pass and Claude review convergence.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-subplan-2026-06-28.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Implement the scoped synthetic moment diagnostic and run compile/tiny smoke
  checks.

### 2026-06-28 - Phase 1 - ASSESS_GATE

Evidence contract:

- Question: Does the finite Contract E reset satisfy its stated moment algebra
  on controlled synthetic weighted clouds?
- Baseline/comparator: weighted source cloud moments and old barycentric
  equal-weight cloud moments as context.
- Primary criterion: required synthetic case matrix passes predeclared gates,
  with the conditioning case reported as expected veto.
- Veto diagnostics: nonfinite values, \(G_+\) eigenvalue failure, support-rank
  failure, pass-case condition failure, missing seed, or hidden GPU claim.
- Non-claims: no LEDH filtering correctness, LGSSM Kalman agreement, gradient
  correctness, or production readiness.

Actions:

- Added `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py`.
- Ran compile check.
- Ran initial diagnostic; three pass cases passed, expected-veto case failed to
  trigger the veto.
- Repaired the expected-veto handling by tightening `_gate_case` so
  expected-veto status requires all non-conditioning checks to pass, and by
  adjusting only the expected-veto fixture scale.
- Reran compile and diagnostic; final artifact status is `passed`.
- Wrote Phase 1 result.

Artifacts:

- `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-result-2026-06-28.md`

Gate status:

- `PASSED_PENDING_CLAUDE_REVIEW`

Next action:

- Run local checks and request bounded Claude review of Phase 1 result/script.

### 2026-06-28 - Phase 1 - PASSED

Evidence contract:

- Question: Does the finite Contract E reset satisfy its stated moment algebra
  on controlled synthetic weighted clouds?
- Baseline/comparator: weighted source cloud moments, with \(D^+_{ij}=w_i\)
  retained only as barycentric context.
- Primary criterion: three required pass cases pass and the conditioning case
  reports `expected_veto`.
- Veto diagnostics: nonfinite values, \(G_+\) eigenvalue failure, support-rank
  failure, pass-case condition failure, hidden GPU claim, missing manifest, or
  review-discovered closeout blocker.
- Non-claims: no LEDH filtering correctness, LGSSM Kalman agreement, gradient
  correctness, SIR/SV correctness, GPU/XLA performance, production readiness,
  posterior correctness, or HMC readiness.

Actions:

- Added Phase 1 run manifest, CPU/reference provenance, skeptical audit, full
  decision table, and post-run red-team note after Claude review found
  closeout documentation gaps.
- Decoupled Phase 1 close from Phase 2 handoff review so Phase 1 closes on its
  own numerical and governance evidence.
- Reran focused local checks:
  `python -m py_compile`,
  `python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py ...`,
  `/usr/bin/time -p python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py ...`,
  and `git diff --check`.
- Claude result-only close review converged with `VERDICT: AGREE`.

Artifacts:

- `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-result-2026-06-28.md`

Gate status:

- `PASSED`

Next action:

- Run separate bounded Claude review of the Phase 2 handoff subplan before
  launching Phase 2.

### 2026-06-28 - Phase 2 - HANDOFF_PASSED

Evidence contract:

- Question: Is the Phase 2 LGSSM value plan pinned enough to execute without
  post-hoc comparator, seed, scalar, particle-count, or GPU-claim drift?
- Baseline/comparator: Phase 2 subplan plus bounded Claude read-only handoff
  review.
- Primary criterion: Claude returns `VERDICT: AGREE` after repairs.
- Veto diagnostics: unfrozen material `N`, seed schedule, scalar, comparator,
  artifact paths, missing skeptical audit, or unclear stop conditions.
- Non-claims: no Phase 2 value evidence yet.

Actions:

- Patched Phase 2 with Phase 1 close provenance, frozen seed schedule, frozen
  value scalar, exact Phase 3 subplan path, exact pinned script path as the
  first implementation artifact, frozen material `N=1000`, and a skeptical
  audit/pre-mortem.
- Claude Phase 2 handoff review round 3 returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-subplan-2026-06-28.md`

Gate status:

- `PASSED`

Next action:

- Implement `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py`.

### 2026-06-28 - Phase 2 - PASSED

Evidence contract:

- Question: Does the Contract E reset reduce the LGSSM value gap relative to
  old barycentric OT and match exact Kalman within stated Monte Carlo
  uncertainty on 1d and 2d \(T=10\) fixtures?
- Baseline/comparator: exact FP64 Kalman value, no-OT weighted LEDH arm, and
  old barycentric OT reset.
- Primary criterion: Contract E mean within two MCSE of Kalman and smaller
  absolute Kalman-value error than old barycentric OT on both fixtures.
- Veto diagnostics: nonfinite values, missing MCSE, untrusted GPU/XLA claim,
  covariance restoration failure, conditioning failure, seed drift, wrong
  scalar, or review-discovered artifact mismatch.
- Non-claims: no gradient correctness, no SIR/SV correctness, no production
  readiness, no posterior correctness, and no HMC readiness.

Actions:

- Added `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py`.
- Ran focused compile/static checks.
- Regenerated the CPU-hidden wiring smoke:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-smoke-2026-06-28.json`
  and matching Markdown.
- Regenerated the material trusted GPU/XLA/TF32 gate:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-2026-06-28.json`
  and matching Markdown.
- Material gate passed with `/usr/bin/time -p` reporting `real 29.18`,
  `user 37.38`, `sys 5.83`.
- Patched the Phase 2 result to keep `arms_distinguishable_metadata`
  explanatory only, and patched the Phase 3 subplan to freeze FD step sizes
  before execution.
- Claude Phase 2 result review round 3 returned `VERDICT: AGREE`.

Artifacts:

- `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-smoke-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-smoke-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-result-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-subplan-2026-06-28.md`

Gate status:

- `PASSED`

Next action:

- Launch Phase 3 precheck: create/compile the LGSSM gradient diagnostic under
  the reviewed Phase 3 subplan, then run the CPU-hidden wiring smoke before any
  material GPU/XLA gradient run.

### 2026-06-28 - Phase 3 - BLOCKED_PRECHECK

Evidence contract:

- Question: Can the Contract E LGSSM gradient gate be launched with a finite
  reverse diagnostic and the frozen same-scalar 13-point FD protocol?
- Baseline/comparator: exact Kalman gradient and same-scalar 13-point FD
  regression on the frozen LGSSM scalar.
- Primary criterion: precheck must produce finite reverse gradients and valid
  FD regression artifacts before a material GPU/XLA gradient gate is launched.
- Veto diagnostics: nonfinite gradients, wrong scalar, FD protocol mismatch,
  central FD promoted to primary evidence, or unreviewed repair.
- Non-claims: no Contract E gradient correctness, no SIR/SV correctness, no
  production/HMC/posterior claim.

Actions:

- Added `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`.
- Ran compile/static checks.
- Ran CPU-hidden Phase 3 smoke at `N=32`; FD regression slopes were finite,
  but reverse diagnostic gradients were `NaN`.
- Ran non-promotable localization probes varying value-only transport,
  XLA/non-XLA, stopped reset branches, and skip-reset computation.  The current
  reverse diagnostic remained `NaN`.
- A broad Claude review prompt hung; the small Claude probe returned
  `PROBE_OK`; a smaller bounded exact-path review returned `VERDICT: REVISE`
  only on overclaim wording.  The blocker result incorporates Claude's
  correction.
- Wrote Phase 3 precheck blocker result.

Artifacts:

- `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-smoke-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-smoke-value-only-probe-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-smoke-nonxla-value-only-probe-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-probe-stop-affine-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-probe-stop-residual-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-probe-stop-reset-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-probe-skip-reset-computation-2026-06-28.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-precheck-blocker-result-2026-06-28.md`

Gate status:

- `BLOCKED_BEFORE_MATERIAL_GATE`

Next action:

- Draft a reviewed Phase 3 repair subplan.  Do not run the material GPU/XLA
  gradient gate or advance to Phase 4 until Phase 3 is repaired or explicitly
  closed as blocked by human direction.
